# LeadRanker

Projeto desktop em Python para ajudar na prospecção de empresas locais.

Fiz esse projeto para treinar Python com interface gráfica, consumo de API pública, organização de dados, score de leads e exportação para Excel.

A ideia é simples: buscar empresas por cidade e nicho, analisar algumas informações básicas e ajudar a decidir quais leads parecem valer mais a pena chamar primeiro.

## Status

O projeto está em fase de MVP funcional.

Já dá para buscar leads reais usando dados públicos do OpenStreetMap, ver os resultados na tela, analisar sites, gerar uma mensagem de abordagem e exportar os dados para Excel.

Ainda não é um sistema pronto para uso profissional diário, mas já está funcionando como projeto de portfólio e base para evoluir.

## O que ele faz

- busca empresas por cidade e nicho;
- usa dados públicos do OpenStreetMap, Nominatim e Overpass;
- mostra os leads em uma interface feita com CustomTkinter;
- calcula um score de prioridade;
- classifica os leads como quente, bom, médio ou frio;
- tenta identificar empresas que parecem ser filiais ou redes grandes;
- filtra empresas com ou sem site, Instagram e telefone;
- analisa alguns sinais simples do site;
- gera uma mensagem pronta para contato;
- abre o WhatsApp com a mensagem preenchida, mas o envio é manual;
- exporta os leads para Excel.

## Por que usei OpenStreetMap

No começo pensei em usar Google Maps, mas a API oficial pode ter custo e scraping do Google não é uma boa ideia para esse tipo de projeto.

Por isso usei OpenStreetMap com Overpass API. Os dados nem sempre vêm completos, mas isso também faz parte da proposta: quando uma empresa não tem site, telefone ou presença digital bem cadastrada, pode existir uma oportunidade de abordagem.

## Como o score funciona

O score não diz se a empresa é boa ou ruim.

Ele tenta medir oportunidade de contato.

Hoje o cálculo considera:

- dados de contato;
- presença digital;
- oportunidade comercial;
- qualidade dos dados encontrados;
- sinais básicos do site;
- possibilidade de ser filial ou rede grande.

Empresas que parecem ser redes grandes recebem uma penalização, porque normalmente não faz sentido tentar vender site ou presença digital para uma unidade de uma grande marca.

## Análise dos sites

A análise ainda é simples, mas já olha alguns pontos úteis:

- se o site usa HTTPS;
- tempo de resposta;
- status HTTP;
- título da página;
- se existe formulário;
- se existe link de WhatsApp;
- se existe link de Instagram;
- se a página tem pouco conteúdo.

Essas informações aparecem nos detalhes do lead e também entram na exportação.

## Tecnologias

- Python
- CustomTkinter
- Requests
- BeautifulSoup
- OpenPyXL
- Pillow
- OpenStreetMap
- Nominatim
- Overpass API

## Estrutura

```text
LeadRanker/
├── main.py
├── requirements.txt
├── README.md
├── src/
│   ├── ai_message.py
│   ├── excel_exporter.py
│   ├── lead_scorer.py
│   ├── models.py
│   ├── places_api.py
│   ├── site_analyzer.py
│   └── whatsapp.py
├── imagens/
└── exports/
```

O `main.py` ficou mais focado na interface. A lógica principal foi separada nos arquivos da pasta `src`.

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

O envio pelo WhatsApp não é automático. O programa só abre a conversa com a mensagem pronta para revisão.

Os dados vêm do OpenStreetMap, então alguns leads podem aparecer sem telefone, site ou Instagram.

## Próximos passos

- salvar leads em SQLite;
- melhorar o histórico de status dos leads;
- gerar executável `.exe`;
- melhorar ainda mais as mensagens;
- testar melhor a busca em cidades e nichos diferentes.
