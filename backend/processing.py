import numpy as np
import polars as pl

def apply_data_mapping(df: pl.DataFrame, mapping: dict) -> pl.DataFrame:

    rename_dict: dict = {}

    for original, meaning in mapping.items():

        if meaning == "Data":
            rename_dict[original] = "data"

        elif meaning == "Precipitação":
            rename_dict[original] = "precipitacao_mm"

        elif meaning == "Temperatura Média":
            rename_dict[original] = "temperatura"

    df = df.rename(rename_dict)

    return df


def filter_data_frame(df: pl.DataFrame) -> pl.DataFrame:
    #primeiro filtro - retirar caracteres indesejados
    df = df.with_columns(
        pl.col(pl.String).str.strip_chars()
    )

    #segundo filtro - data
    df = df.with_columns(
        pl.col("data").str.strptime(pl.Date, "%Y-%m-%d")
    )

    #terceiro filtro - precipitação
    df = df.with_columns(
        pl.col("precipitacao_mm").cast(pl.Float64)
    )

    return df


def analisar_dados_precipitacao(df: pl.DataFrame) -> dict:

    total_precipit = df["precipitacao_mm"].sum()
    media_precipit = df["precipitacao_mm"].mean()
    desvio_precipit = df["precipitacao_mm"].std()
    dias_secos = np.sum(df["precipitacao_mm"].to_numpy() == 0)

    return {
        "total_precipitacao": float(total_precipit),
        "media_precipitacao": float(media_precipit),
        "desvio_padrao_precipitacao": float(desvio_precipit),
        "dias_secos": int(dias_secos)
    }


def analisar_dados_temperatura(df: pl.DataFrame) -> dict:
    media_temp = df["temperatura"].mean()
    desvio_temp = df["temperatura"].std()
    min_temp = df["temperatura"].min()
    max_temp = df["temperatura"].max()

    return {
        "media_temperatura": media_temp,
        "desvio_padrao_temperatura": desvio_temp,
        "temperatura_minima": min_temp,
        "temperatura_maxima": max_temp
    }

def analisar_por_mes(df: pl.DataFrame) -> list:

    df = df.with_columns(
        pl.col("data").dt.month().alias("mes")
    )

    aggs: list = []

    if "precipitacao" in df.columns:
        aggs.append = [
            pl.col("precipitacao_mm").sum().alias("total_precipitacao"),
            pl.col("precipitacao_mm").mean().alias("media_precipitacao")
        ]

    if "temperatura" in df.columns:
        aggs.append(
            pl.col("temperatura").mean().alias("media_temperatura")
        )

    resultado = (
        df.group_by("mes")
        .agg(aggs)
        .sort("mes")
    )

    return resultado.to_dicts()

if __name__ == "__main__":
    pass