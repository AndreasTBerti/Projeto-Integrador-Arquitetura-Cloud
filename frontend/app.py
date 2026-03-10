import json
import polars as pl
from requests import post
import streamlit as st

def main() -> None:
    Frontend()

class Frontend():

    def __init__(self):
        self.API_URL = "https://pi-cloud.onrender.com/analyze"
        
        st.set_page_config(
            page_title="ClimateDataViewer",
            page_icon="📊",
            layout="wide"
        )

        file = st.file_uploader("Envie o CSV", type="csv")

        if file:
            self.data_mapping(file)


    def data_mapping(self, file) -> None:

        file.seek(0)
        df = pl.read_csv(file, separator=",")

        columns = df.columns
        st.write("Colunas encontradas:", columns)

        mapping = {}

        options = [
            "Ignorar",
            "Data",
            "Precipitação",
            "Temperatura",
        ]

        with st.container(border=True):
            st.subheader("Mapeamento de colunas")

            col1, col2 = st.columns(2)

            for i, col in enumerate(columns):

                target = col1 if i % 2 == 0 else col2

                with target:
                    selected = st.selectbox(
                        f"Coluna '{col}' representa:",
                        options,
                        key=f"map_{col}_{i}"
                    )

                mapping[col] = selected


        if st.button("Analisar dados"):

            file.seek(0)

            files = {
                "file": (file.name, file.getvalue(), "text/csv")
            }

            data = {
                "mapping": json.dumps(mapping)
            }

            try:

                response = post(
                    self.API_URL,
                    files=files,
                    data=data
                )

                if response.status_code == 200:

                    result = response.json()

                    stats = result["estatisticas"]

                    st.subheader("Resultados da análise")

                    c1, c2, c3, c4 = st.columns(4)

                    c1.metric(
                        "🌧 Total precipitação",
                        f"{stats['total_precipitacao']:.2f} mm"
                    )

                    c2.metric(
                        "📊 Média",
                        f"{stats['media_precipitacao']:.2f} mm"
                    )

                    c3.metric(
                        "📉 Desvio padrão",
                        f"{stats['desvio_padrao_precipitacao']:.2f}"
                    )

                    c4.metric(
                        "☀ Dias secos",
                        stats["dias_secos"]
                    )

                else:

                    st.error("Erro ao processar os dados.")
                    st.error(response.text)

            except Exception as e:
                st.error(str(e))

if __name__ == "__main__":
    main()