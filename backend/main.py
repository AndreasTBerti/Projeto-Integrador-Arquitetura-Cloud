import json
from fastapi import FastAPI, UploadFile, File, Form
import polars as pl

from models import RainStats, AnalysisResponse
from processing import analisar_dados, apply_data_mapping

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

    df = pl.read_csv(content)

    df = apply_data_mapping(df, mapping)

    stats = analisar_dados(df)

    return AnalysisResponse(
        sucesso=True,
        estatisticas=RainStats(**stats)
    )