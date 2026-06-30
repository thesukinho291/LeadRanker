import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from src.lead_scorer import processar_lead
from src.places_api import OSM_USER_AGENT


def analisar_sites(leads):
    for lead in leads:
        if lead.site:
            aplicar_analise_site(lead)
        else:
            limpar_analise_site(lead)
        processar_lead(lead)
    return sorted(leads, key=lambda item: item.score, reverse=True)


def analisar_site_basico(site):
    return analisar_site(site)["site_basico"]


def aplicar_analise_site(lead):
    resultado = analisar_site(lead.site)
    lead.site_basico = resultado["site_basico"]
    lead.site_status_code = resultado["status_code"]
    lead.site_tempo_resposta = resultado["tempo_resposta"]
    lead.site_titulo = resultado["titulo"]
    lead.site_tem_whatsapp = resultado["tem_whatsapp"]
    lead.site_tem_formulario = resultado["tem_formulario"]
    lead.site_tem_instagram = resultado["tem_instagram"]
    lead.site_motivos = resultado["motivos"]


def limpar_analise_site(lead):
    lead.site_basico = False
    lead.site_status_code = 0
    lead.site_tempo_resposta = 0
    lead.site_titulo = ""
    lead.site_tem_whatsapp = False
    lead.site_tem_formulario = False
    lead.site_tem_instagram = False
    lead.site_motivos = []


def analisar_site(site):
    # Faz uma checagem simples, mas com sinais mais fáceis de explicar.
    resultado = {
        "site_basico": False,
        "status_code": 0,
        "tempo_resposta": 0,
        "titulo": "",
        "tem_whatsapp": False,
        "tem_formulario": False,
        "tem_instagram": False,
        "motivos": [],
    }

    if not site:
        return resultado

    if not site.startswith("https://"):
        resultado["motivos"].append("Site não usa HTTPS.")

    try:
        inicio = time.perf_counter()
        resposta = requests.get(
            normalizar_url(site),
            timeout=8,
            headers={"User-Agent": OSM_USER_AGENT},
        )
        resultado["tempo_resposta"] = round(time.perf_counter() - inicio, 2)
        resultado["status_code"] = resposta.status_code
    except requests.RequestException:
        resultado["site_basico"] = True
        resultado["motivos"].append("Site não respondeu durante a análise.")
        return resultado

    if resposta.status_code >= 400:
        resultado["motivos"].append(f"Site retornou erro HTTP {resposta.status_code}.")

    if resultado["tempo_resposta"] > 3:
        resultado["motivos"].append(
            f"Site demorou {resultado['tempo_resposta']}s para responder."
        )

    html = resposta.text or ""
    soup = BeautifulSoup(html, "html.parser")
    titulo = soup.title.get_text(" ", strip=True) if soup.title else ""
    texto = soup.get_text(" ", strip=True)
    links = " ".join(link.get("href", "") for link in soup.find_all("a")).lower()

    resultado["titulo"] = titulo[:120]
    resultado["tem_formulario"] = bool(soup.find("form"))
    resultado["tem_whatsapp"] = "wa.me" in links or "api.whatsapp.com" in links
    resultado["tem_instagram"] = "instagram.com" in links

    if not titulo:
        resultado["motivos"].append("Site não possui título claro.")

    if len(texto) < 500:
        resultado["motivos"].append("Site tem pouco conteúdo textual.")

    if not resultado["tem_formulario"] and not resultado["tem_whatsapp"]:
        resultado["motivos"].append("Não encontrei formulário ou WhatsApp visível no site.")

    problemas_fortes = [
        resposta.status_code >= 400,
        resultado["tempo_resposta"] > 3,
        not site.startswith("https://"),
    ]
    problemas_conteudo = [
        not titulo,
        len(texto) < 500,
        not resultado["tem_formulario"] and not resultado["tem_whatsapp"],
    ]
    resultado["site_basico"] = any(problemas_fortes) or sum(problemas_conteudo) >= 2
    resultado["motivos"] = resultado["motivos"][:6]
    return resultado


def normalizar_url(site):
    if urlparse(site).scheme:
        return site

    return f"https://{site}"
