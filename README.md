# LeadRanker

LeadRanker é um projeto desktop feito em Python para ajudar na prospecção de empresas locais.

A ideia do programa é buscar possíveis leads usando dados públicos do OpenStreetMap, organizar essas empresas em uma lista, calcular uma prioridade de contato e gerar uma mensagem pronta para abordagem manual pelo WhatsApp.

Esse projeto foi feito como estudo e portfólio, tentando juntar interface gráfica, consumo de API, análise de dados simples e exportação para Excel.

## O que o programa faz

- Busca empresas por cidade e nicho usando OpenStreetMap, Nominatim e Overpass.
- Mostra os leads em uma interface feita com CustomTkinter.
- Calcula score de prioridade para cada lead.
- Analisa presença digital básica, como site, telefone e Instagram cadastrado.
- Tenta identificar empresas que parecem ser filiais ou redes grandes.
- Permite filtrar leads com ou sem site, Instagram e telefone.
- Gera uma mensagem pronta para contato.
- Abre o WhatsApp com a mensagem preenchida, mas o envio fica manual.
- Exporta os leads para Excel.

## Por que usei OpenStreetMap

No começo pensei em usar Google Maps, mas a API oficial pode ter custo e scraping não é uma boa prática.

Por isso escolhi OpenStreetMap com Overpass API, que permite buscar dados públicos sem depender de login ou chave paga.

Os dados podem vir incompletos, mas isso também faz parte da análise: uma empresa sem site ou com poucas informações pode ser uma oportunidade melhor para oferecer presença digital.

## Como o score funciona

O score não mede se a empresa é "melhor" ou "pior". Ele tenta medir se existe uma oportunidade de abordagem.

O cálculo considera:

- Score de contato
- Score de presença digital
- Score de oportunidade
- Score de qualidade dos dados

Depois disso o programa gera um score final e classifica o lead como:

- Quente
- Bom
- Médio
- Frio

Empresas que parecem ser filiais ou redes grandes recebem uma penalização, porque normalmente não faz sentido vender um site para uma grande rede.

## Tecnologias usadas

- Python
- CustomTkinter
- Requests
- OpenPyXL
- Pillow
- OpenStreetMap
- Nominatim
- Overpass API

## Como rodar

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Rode o programa:

```bash
python main.py
```

## Observações

O programa depende dos dados disponíveis no OpenStreetMap. Algumas empresas podem não ter telefone, site ou Instagram cadastrados.

O envio de mensagens não é automático. O sistema apenas abre o WhatsApp com a mensagem pronta para revisão.

## Próximas melhorias

- Salvar leads em SQLite.
- Separar o código em módulos dentro de uma pasta `src`.
- Melhorar a análise dos sites.
- Gerar executável `.exe` com PyInstaller.
- Melhorar a personalização das mensagens.
