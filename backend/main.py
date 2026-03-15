import json
from io import BytesIO
from fastapi import FastAPI, UploadFile, File, Form
import polars as pl

from models import RainStats, TemperatureStats, AnalysisResponse
from processing import analisar_dados_precipitacao, analisar_dados_temperatura, analisar_por_mes, analisar_por_dia
from processing import apply_data_mapping, filter_data_frame

app = FastAPI(
    title="DataViewer API",
    description="API para análise pluviométrica",
    version="1.0"
)


@app.get("/")
def root():
    return {"status": "API online"}


@app.post("/analyze", response_model=AnalysisResponse)
async def analisar(
    file: UploadFile = File(...),
    mapping: str = Form(...)
):
    
    mapping = json.loads(mapping)

    content = await file.read()

    df = pl.read_csv(
        BytesIO(content),
        separator=",",
        ignore_errors=True
    )

    df = apply_data_mapping(df, mapping)
    
    df = filter_data_frame(df)

    precipitacao_stats = None
    temperatura_stats = None 
    mensal_stats = None

    if "precipitacao_mm" in df.columns:
        stats = analisar_dados_precipitacao(df)
        precipitacao_stats = RainStats(**stats)
    
    if "temperatura" in df.columns:
        stats = analisar_dados_temperatura(df)
        temperatura_stats = TemperatureStats(**stats)

    if "data" in df.columns:
        mensal_stats = analisar_por_mes(df)
        diary_stats = analisar_por_dia(df)

    return AnalysisResponse(
        sucesso=True,
        precipitacao=precipitacao_stats,
        temperatura=temperatura_stats,
        dados_mensais=mensal_stats,
        dados_diarios=diary_stats
    )