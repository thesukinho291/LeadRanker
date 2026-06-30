import time

import requests

from src.lead_scorer import processar_lead
from src.places_api import OSM_USER_AGENT


def analisar_sites(leads):
    for lead in leads:
        if lead.site:
            lead.site_basico = analisar_site_basico(lead.site)
        processar_lead(lead)
    return sorted(leads, key=lambda item: item.score, reverse=True)


def analisar_site_basico(site):
    # Faz uma checagem simples para descobrir se o site parece antigo ou instável.
    if not site:
        return False

    if not site.startswith("https://"):
        return True

    try:
        inicio = time.perf_counter()
        resposta = requests.get(site, timeout=8, headers={"User-Agent": OSM_USER_AGENT})
        tempo = time.perf_counter() - inicio
    except requests.RequestException:
        return True

    return resposta.status_code >= 400 or tempo > 3
