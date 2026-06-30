from urllib.parse import quote


def montar_link_whatsapp(telefone, mensagem):
    numero = "".join(caractere for caractere in telefone if caractere.isdigit())

    if not numero:
        return ""

    numero_whatsapp = numero if numero.startswith("55") else f"55{numero}"
    return f"https://wa.me/{numero_whatsapp}?text={quote(mensagem)}"
