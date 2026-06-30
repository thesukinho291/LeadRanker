import re

import requests

from src.lead_scorer import processar_lead
from src.models import Lead


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OSM_USER_AGENT = "LeadRankerAI/1.0 (portfolio project)"

CHAIN_BRANDS = [
    "drogasil",
    "droga raia",
    "raia drogasil",
    "pague menos",
    "drogaria sao paulo",
    "drogaria são paulo",
    "drogaria araujo",
    "drogaria araújo",
    "carrefour",
    "extra",
    "assai",
    "assaí",
    "atacadao",
    "atacadão",
    "mcdonald",
    "burger king",
    "subway",
    "habib",
    "cacaushow",
    "cacau show",
    "o boticario",
    "o boticário",
    "renner",
    "riachuelo",
    "magazine luiza",
]


def buscar_leads_openstreetmap(cidade, nicho, quantidade):
    # Busca a cidade primeiro para limitar a consulta ao mapa daquela região.
    quantidade = max(1, min(quantidade, 50))
    bbox = buscar_bbox_cidade(cidade)
    consulta = montar_consulta_overpass(nicho, bbox, quantidade)

    resposta = requests.post(
        OVERPASS_URL,
        data={"data": consulta},
        timeout=45,
        headers={"User-Agent": OSM_USER_AGENT},
    )
    resposta.raise_for_status()
    dados = resposta.json()

    leads = []
    vistos = set()

    for elemento in dados.get("elements", []):
        if len(leads) >= quantidade:
            break

        tags = elemento.get("tags", {})
        nome = tags.get("name", "").strip()
        if not nome:
            continue

        chave = normalizar_texto(
            f"{nome}-{tags.get('addr:street', '')}-{tags.get('phone', '')}"
        )
        if chave in vistos:
            continue

        vistos.add(chave)
        leads.append(processar_lead(criar_lead_osm(elemento, cidade, nicho)))

    return sorted(leads, key=lambda item: item.score, reverse=True)


def buscar_bbox_cidade(cidade):
    resposta = requests.get(
        NOMINATIM_URL,
        params={
            "q": f"{cidade}, Brasil",
            "format": "json",
            "limit": 1,
            "addressdetails": 1,
        },
        timeout=20,
        headers={"User-Agent": OSM_USER_AGENT},
    )
    resposta.raise_for_status()
    resultados = resposta.json()

    if not resultados:
        raise RuntimeError(f"Não encontrei a cidade '{cidade}' no OpenStreetMap.")

    sul, norte, oeste, leste = resultados[0]["boundingbox"]
    return float(sul), float(oeste), float(norte), float(leste)


def montar_consulta_overpass(nicho, bbox, quantidade):
    # Monta a consulta que o Overpass usa para encontrar empresas no OpenStreetMap.
    sul, oeste, norte, leste = bbox
    blocos = []

    for filtro in filtros_osm_por_nicho(nicho):
        blocos.append(f"node{filtro}({sul},{oeste},{norte},{leste});")
        blocos.append(f"way{filtro}({sul},{oeste},{norte},{leste});")
        blocos.append(f"relation{filtro}({sul},{oeste},{norte},{leste});")

    limite = max(quantidade * 5, 40)
    return f"""
[out:json][timeout:35];
(
  {' '.join(blocos)}
);
out tags center {limite};
"""


def filtros_osm_por_nicho(nicho):
    texto = normalizar_texto(nicho)
    filtros = []

    mapas = [
        (["restaurante", "lanchonete", "pizza", "hamburguer", "cafe"], '["amenity"~"restaurant|fast_food|cafe|bar|pub"]'),
        (["clinica", "medico", "dentista", "saude"], '["healthcare"~"clinic|doctor|dentist|physiotherapist"]'),
        (["clinica", "medico", "dentista", "saude"], '["amenity"~"clinic|doctors|dentist"]'),
        (["estetica", "beleza", "salao", "barbearia"], '["shop"~"beauty|hairdresser|cosmetics"]'),
        (["academia", "fitness", "musculacao"], '["leisure"="fitness_centre"]'),
        (["pet", "veterinario", "veterinaria"], '["shop"="pet"]'),
        (["pet", "veterinario", "veterinaria"], '["amenity"="veterinary"]'),
        (["mercado", "supermercado", "padaria", "acougue"], '["shop"~"supermarket|convenience|bakery|butcher"]'),
        (["farmacia", "drogaria"], '["amenity"="pharmacy"]'),
        (["farmacia", "drogaria"], '["shop"="chemist"]'),
        (["hotel", "pousada"], '["tourism"~"hotel|guest_house|hostel"]'),
        (["escola", "curso"], '["amenity"~"school|college|language_school"]'),
        (["loja", "comercio"], '["shop"]'),
    ]

    for palavras, filtro in mapas:
        if any(palavra in texto for palavra in palavras):
            filtros.append(filtro)

    if not filtros:
        termo = re.escape(nicho.strip())
        filtros.append(f'["name"~"{termo}",i]')

    return list(dict.fromkeys(filtros))


def criar_lead_osm(elemento, cidade, nicho):
    tags = elemento.get("tags", {})
    site = tags.get("website") or tags.get("contact:website") or ""
    telefone = tags.get("phone") or tags.get("contact:phone") or tags.get("mobile") or ""
    filial, motivo_filial = detectar_filial(tags)

    return Lead(
        nome=tags.get("name", "Empresa sem nome"),
        telefone=telefone,
        cidade=cidade.title(),
        nicho=nicho.title(),
        endereco=montar_endereco_osm(tags),
        site=site,
        nota_google=0,
        quantidade_avaliacoes=contar_dados_osm(tags),
        site_basico=bool(site and not site.startswith("https://")),
        instagram=extrair_instagram(tags),
        filial=filial,
        motivo_filial=motivo_filial,
    )


def extrair_instagram(tags):
    instagram = (
        tags.get("contact:instagram")
        or tags.get("instagram")
        or tags.get("social_media:instagram")
        or ""
    )
    return instagram.strip()


def detectar_filial(tags):
    # Tenta identificar redes grandes para evitar priorizar empresas que já têm estrutura.
    nome = normalizar_texto(tags.get("name", ""))
    marca = normalizar_texto(tags.get("brand", ""))
    operador = normalizar_texto(tags.get("operator", ""))

    for campo, valor in [("nome", nome), ("marca", marca), ("operador", operador)]:
        for rede in CHAIN_BRANDS:
            if normalizar_texto(rede) in valor:
                return True, f"{campo} contém '{rede}'"

    if tags.get("brand:wikidata") or tags.get("brand:wikipedia"):
        return True, "possui marca cadastrada no OSM"

    if normalizar_texto(tags.get("branch", "")) in ["yes", "sim"]:
        return True, "tag branch indica filial"

    return False, ""


def montar_endereco_osm(tags):
    rua = tags.get("addr:street", "")
    numero = tags.get("addr:housenumber", "")
    bairro = tags.get("addr:suburb") or tags.get("addr:neighbourhood") or ""
    cidade = tags.get("addr:city", "")

    partes = []
    if rua:
        partes.append(f"{rua}, {numero}".strip().strip(","))
    if bairro:
        partes.append(bairro)
    if cidade:
        partes.append(cidade)

    return " - ".join(partes) or "Endereço não informado"


def contar_dados_osm(tags):
    campos = [
        "name",
        "phone",
        "contact:phone",
        "website",
        "contact:website",
        "addr:street",
        "addr:housenumber",
        "opening_hours",
    ]
    return sum(1 for campo in campos if tags.get(campo))


def normalizar_texto(texto):
    substituicoes = str.maketrans(
        "áàãâéêíóôõúçÁÀÃÂÉÊÍÓÔÕÚÇ",
        "aaaaeeioooucAAAAEEIOOOUC",
    )
    return texto.translate(substituicoes).lower().strip()
