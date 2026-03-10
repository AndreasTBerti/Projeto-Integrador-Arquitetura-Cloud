import numpy as np
import polars as pl

def apply_data_mapping(df: pl.DataFrame, mapping: dict) -> pl.DataFrame:

    rename_dict: dict = {}

    for original, meaning in mapping.items():

        if meaning == "Data":
            rename_dict[original] = "data"

        elif meaning == "Precipitação":
            rename_dict[original] = "precipitacao_mm"

        elif meaning == "Temperatura":
            rename_dict[original] = "temperatura"

    df = df.rename(rename_dict)

    return df


def analisar_dados(df: pl.DataFrame) -> dict:

    #primeiro filtro - retirar caracteres indesejados
    df = df.with_columns(
        pl.col(pl.String).str.strip_chars()
    )

    #segundo filtro - data
    df = df.with_columns(
        pl.col("data").str.strptime(pl.Date, "%y-%m-%d")
    )

    #terceiro filtro - precipitação
    df = df.with_columns(
        pl.col("precipitacao_mm").cast(pl.Float64)
    )

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

if __name__ == "__main__":
    pass