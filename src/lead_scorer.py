from src.ai_message import gerar_mensagem


def classificar_lead(score):
    if score >= 70:
        return "Quente"
    if score >= 50:
        return "Bom"
    if score >= 30:
        return "Médio"
    return "Frio"


def calcular_score_analitico(lead):
    # Divide o score em partes para deixar a análise mais fácil de explicar.
    score_contato, motivos_contato = calcular_score_contato(lead)
    score_presenca, motivos_presenca = calcular_score_presenca_digital(lead)
    score_oportunidade, motivos_oportunidade = calcular_score_oportunidade(lead)
    score_dados, motivos_dados = calcular_score_qualidade_dados(lead)

    score_final = round(
        (score_contato * 0.25)
        + (score_presenca * 0.35)
        + (score_oportunidade * 0.30)
        + (score_dados * 0.10)
    )

    motivos = motivos_contato + motivos_presenca + motivos_oportunidade + motivos_dados

    if lead.filial:
        score_final = max(score_final - 35, 0)
        motivos.append(f"Possível filial/rede: {lead.motivo_filial}")

    lead.score_contato = score_contato
    lead.score_presenca_digital = score_presenca
    lead.score_oportunidade = score_oportunidade
    lead.score_qualidade_dados = score_dados
    lead.motivos_score = motivos[:8]

    return min(score_final, 100)


def calcular_score_contato(lead):
    score = 0
    motivos = []

    if lead.telefone:
        score += 70
        motivos.append("Possui telefone para contato.")
    else:
        motivos.append("Não possui telefone cadastrado.")

    if lead.endereco and lead.endereco != "Endereço não informado":
        score += 20
        motivos.append("Possui endereço cadastrado.")

    if lead.site or lead.instagram:
        score += 10

    return min(score, 100), motivos


def calcular_score_presenca_digital(lead):
    score = 0
    motivos = []

    if not lead.site:
        score += 45
        motivos.append("Não possui site cadastrado.")
    elif not lead.site.startswith("https://"):
        score += 25
        motivos.append("Site cadastrado não usa HTTPS.")

    if not lead.instagram:
        score += 30
        motivos.append("Não possui Instagram cadastrado no OpenStreetMap.")

    if lead.site_basico:
        score += 25
        if lead.site_motivos:
            motivos.append(f"Site pode melhorar: {lead.site_motivos[0]}")
        else:
            motivos.append("Site aparenta ser básico, lento ou instável.")

    return min(score, 100), motivos


def calcular_score_oportunidade(lead):
    score = 0
    motivos = []

    if not lead.filial:
        score += 30
        motivos.append("Não parece ser uma grande rede.")

    if lead.telefone:
        score += 20

    if not lead.site:
        score += 25

    if not lead.instagram:
        score += 15

    if lead.site_basico:
        score += 10

    return min(score, 100), motivos


def calcular_score_qualidade_dados(lead):
    score = min(lead.quantidade_avaliacoes * 12, 70)
    motivos = [f"Cadastro possui {lead.quantidade_avaliacoes} dado(s) útil(eis) no OSM."]

    if lead.endereco and lead.endereco != "Endereço não informado":
        score += 15

    if lead.telefone:
        score += 15

    return min(score, 100), motivos


def processar_lead(lead):
    lead.score = calcular_score_analitico(lead)
    lead.classificacao = classificar_lead(lead.score)
    lead.mensagem_gerada = gerar_mensagem(lead)
    return lead
