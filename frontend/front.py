import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import random
import time


st.set_page_config(
    page_title="Climate Data Dashboard",
    page_icon="🌦️",
    layout="wide"
)


st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}

h1 {
    color: #1f2937;
}

</style>
""", unsafe_allow_html=True)


st.title("🌦️ Dashboard Climático")
st.markdown("Monitoramento de sensores climáticos em tempo real")


API_URL = "http://127.0.0.1:8000"



def get_climate_data():
    """
    Simulação temporária de dados.
    Substituir futuramente pela API real.
    """

    sensores = ["sensor_01", "sensor_02", "sensor_03"]

    dados = []

    for i in range(20):
        dados.append({
            "sensor_id": random.choice(sensores),
            "temperatura": round(random.uniform(18, 35), 2),
            "precipitacao_mm": round(random.uniform(0, 50), 2),
            "timestamp": datetime.now()
        })

    return pd.DataFrame(dados)


st.sidebar.header("⚙️ Configurações")

sensor_selecionado = st.sidebar.selectbox(
    "Selecione o sensor",
    ["Todos", "sensor_01", "sensor_02", "sensor_03"]
)

auto_refresh = st.sidebar.checkbox("Atualização automática")


df = get_climate_data()

# filtro
if sensor_selecionado != "Todos":
    df = df[df["sensor_id"] == sensor_selecionado]


temperatura_media = round(df["temperatura"].mean(), 2)
temperatura_max = round(df["temperatura"].max(), 2)
precipitacao_total = round(df["precipitacao_mm"].sum(), 2)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="🌡️ Temperatura Média",
        value=f"{temperatura_media} °C"
    )

with col2:
    st.metric(
        label="🔥 Temperatura Máxima",
        value=f"{temperatura_max} °C"
    )

with col3:
    st.metric(
        label="🌧️ Precipitação Total",
        value=f"{precipitacao_total} mm"
    )



st.subheader("📋 Dados Recebidos")

st.dataframe(
    df,
    use_container_width=True
)



st.subheader("📈 Temperatura por Leitura")

fig_temp = px.line(
    df,
    x=df.index,
    y="temperatura",
    color="sensor_id",
    markers=True,
    title="Variação de Temperatura"
)

st.plotly_chart(fig_temp, use_container_width=True)



st.subheader("🌧️ Precipitação")

fig_prec = px.bar(
    df,
    x=df.index,
    y="precipitacao_mm",
    color="sensor_id",
    title="Precipitação por Leitura"
)

st.plotly_chart(fig_prec, use_container_width=True)


st.subheader("🌡️ Distribuição de Temperatura")

fig_hist = px.histogram(
    df,
    x="temperatura",
    nbins=10,
    color="sensor_id",
    title="Distribuição das Temperaturas"
)

st.plotly_chart(fig_hist, use_container_width=True)


st.subheader("🚨 Alertas Climáticos")

if temperatura_max > 30:
    st.warning("Temperatura acima do limite recomendado!")

if precipitacao_total > 200:
    st.error("Volume elevado de precipitação detectado!")

if temperatura_media < 20:
    st.info("Temperatura média abaixo de 20°C")


csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Baixar Dados CSV",
    data=csv,
    file_name="dados_climaticos.csv",
    mime="text/csv"
)

if auto_refresh:
    time.sleep(5)
    st.rerun()