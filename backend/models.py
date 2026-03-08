from pydantic import BaseModel

class RainStats(BaseModel):
    total: float
    media: float
    desvio_padrao: float
    dias_secos: int


class AnalysisResponse(BaseModel):
    sucesso: bool
    estatisticas: RainStats