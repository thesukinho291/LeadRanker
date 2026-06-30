def gerar_mensagem(lead):
    contexto = montar_contexto(lead)
    oportunidade = montar_oportunidade(lead)

    return (
        f"Boa tarde, tudo bem? Estava pesquisando {contexto} e percebi uma "
        f"oportunidade de {oportunidade}. Trabalho com soluções simples para "
        "empresas locais e posso te mostrar uma ideia rápida, sem compromisso."
    )


def montar_contexto(lead):
    nicho = lead.nicho.lower() if lead.nicho else "empresas locais"
    cidade = lead.cidade if lead.cidade else "sua região"

    return f"sobre empresas de {nicho} em {cidade}"


def montar_oportunidade(lead):
    if not lead.site and not lead.instagram:
        return "criar uma presença digital mais forte para captar clientes locais"

    if not lead.site:
        return "ter uma página simples e profissional para facilitar o contato dos clientes"

    if lead.site_basico and lead.site_motivos:
        motivo = lead.site_motivos[0].lower().rstrip(".")
        return f"melhorar o site atual, principalmente porque {motivo}"

    if lead.site_basico:
        return "melhorar o site atual e deixar a presença digital mais clara"

    if not lead.instagram:
        return "fortalecer a presença digital e melhorar os canais de contato"

    return "melhorar a captação de clientes pela presença digital"
