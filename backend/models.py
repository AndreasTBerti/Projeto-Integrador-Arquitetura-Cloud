from pydantic import BaseModel


class RainStats(BaseModel):
    total_precipitacao: float
    media_precipitacao: float
    desvio_padrao_precipitacao: float
    dias_secos: int

class TemperatureStats(BaseModel):
    media_temperatura: float
    desvio_padrao_temperatura: float
    temperatura_minima: float
    temperatura_maxima: float

class AnalysisResponse(BaseModel):
    sucesso: bool
    precipitacao: RainStats
    temperatura: TemperatureStats
    dados_mensais: list | None = None