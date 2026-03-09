import json
import polars as pl
from requests import post
import streamlit as st

def main() -> None:
    frontend = Frontend()

class Frontend():

    def __init__(self):
        self.API_URL = "https://pi-cloud.onrender.com/analisar"
        
        st.title("DataViewer")

        file = st.file_uploader("Envie o CSV", type="csv")

        if file:
            self.data_mapping(file)


    def data_mapping(self, file) -> None:

        df = pl.read_csv(file, separator=",")

        columns = df.columns
        st.write("Colunas encontradas:", columns)

        mapping = {}

        options = [
            "Ignorar",
            "Data",
            "Precipitacao",
            "Temperatura",
        ]

        for col in columns:

            selected = st.selectbox(
                f"O que representa a coluna '{col}'?",
                options,
                key=col
            )

            mapping[col] = selected

        if st.button("Analisar dados"):

            files = {
                "file": file.getvalue()
            }

            data = {
                "mapping": json.dumps(mapping)
            }

            response = post(
                self.API_URL,
                files=files,
                data=data
            )

            if response.status_code == 200:

                result = response.json()

                stats = result["estatisticas"]

                st.subheader("Resultados da análise")

                col1, col2 = st.columns(2)

                col1.metric(
                    "Total de precipitação",
                    f"{stats['total_precipitacao']:.2f} mm"
                )

                col2.metric(
                    "Média de precipitação",
                    f"{stats['media_precipitacao']:.2f} mm"
                )

                col1.metric(
                    "Desvio padrão",
                    f"{stats['desvio_padrao']:.2f}"
                )

                col2.metric(
                    "Dias secos",
                    stats["dias_secos"]
                )

            else:

                st.error("Erro ao processar os dados.")


if __name__ == "__main__":
    main()