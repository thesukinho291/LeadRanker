from dataclasses import dataclass, field


@dataclass
class Lead:
    nome: str
    telefone: str
    cidade: str
    nicho: str
    endereco: str
    site: str
    nota_google: float
    quantidade_avaliacoes: int
    site_basico: bool
    instagram: str = ""
    filial: bool = False
    motivo_filial: str = ""
    site_status_code: int = 0
    site_tempo_resposta: float = 0
    site_titulo: str = ""
    site_tem_whatsapp: bool = False
    site_tem_formulario: bool = False
    site_tem_instagram: bool = False
    site_motivos: list[str] = field(default_factory=list)
    status: str = "Novo"
    score: int = 0
    score_contato: int = 0
    score_presenca_digital: int = 0
    score_oportunidade: int = 0
    score_qualidade_dados: int = 0
    classificacao: str = "Frio"
    mensagem_gerada: str = ""
    motivos_score: list[str] = field(default_factory=list)
