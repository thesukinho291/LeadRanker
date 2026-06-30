def gerar_mensagem(lead):
    oportunidade = (
        "melhorar a presença digital"
        if lead.site
        else "criar uma presença digital mais forte para captar clientes locais"
    )

    return (
        "Boa tarde, tudo bem? Estava pesquisando sobre a empresa de vocês "
        f"e percebi uma oportunidade de {oportunidade}. Trabalho com soluções "
        "simples para empresas e posso te mostrar uma ideia rápida, sem compromisso."
    )
