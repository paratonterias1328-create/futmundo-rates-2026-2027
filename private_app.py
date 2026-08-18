
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

ROOT = Path(__file__).parent
df = pd.read_csv(ROOT / "data" / "team_economy.csv")

st.set_page_config(page_title="Futmondo · Economía", page_icon="💰", layout="wide")
st.title("💰 Futmondo · Dashboard privado")
st.caption("Rates 2026–2027 · Snapshot T0: 18/08/2026")

st.info(
    "La liquidez es una estimación relativa basada en el gasto neto visible en mercado. "
    "No representa el saldo exacto en euros porque no conocemos el valor de plantilla inicial "
    "ni toda la revalorización/devaluación histórica."
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Valor total plantillas", f"{df.squad_value_eur.sum()/1e9:.2f} B€")
c2.metric("Valor medio plantilla", f"{df.squad_value_eur.mean()/1e6:.1f} M€")
top = df.loc[df.squad_value_eur.idxmax()]
c3.metric("Plantilla más valiosa", top["team"], f"{top['squad_value_eur']/1e6:.1f} M€")
aggr = df.loc[df.visible_net_spend_m.idxmax()]
c4.metric("Mayor gasto neto visible", aggr["team"], f"{aggr['visible_net_spend_m']:.1f} M€")

st.subheader("Valor actual de plantilla")
fig = px.bar(
    df.sort_values("squad_value_eur"),
    x="squad_value_eur", y="team", orientation="h",
    labels={"squad_value_eur":"Valor de plantilla (€)","team":""},
    hover_data={"visible_net_spend_m":True, "liquidity_index":True}
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Liquidez relativa estimada")
liq = df.sort_values("liquidity_index", ascending=False)
fig2 = px.bar(
    liq, x="team", y="liquidity_index",
    labels={"liquidity_index":"Índice de liquidez (0–100)","team":""},
    hover_data={"visible_net_spend_m":True, "squad_value_eur":True, "liquidity_band":True}
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Valor de plantilla vs. gasto neto visible")
fig3 = px.scatter(
    df, x="visible_net_spend_m", y="squad_value_eur", text="team", size="squad_value_eur",
    labels={"visible_net_spend_m":"Gasto neto visible (M€)","squad_value_eur":"Valor de plantilla (€)"}
)
fig3.update_traces(textposition="top center")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Tabla económica")
view = df.copy()
view["Valor plantilla"] = (view["squad_value_eur"]/1e6).map(lambda x: f"{x:.2f} M€")
view["Gasto neto visible"] = view["visible_net_spend_m"].map(lambda x: f"{x:.2f} M€")
view["Liquidez"] = view["liquidity_index"].astype(str) + "/100 · " + view["liquidity_band"]
st.dataframe(
    view[["team","Valor plantilla","Gasto neto visible","Liquidez"]]
    .rename(columns={"team":"Equipo"})
    .sort_values("Valor plantilla", ascending=False),
    use_container_width=True, hide_index=True
)

st.caption("T0 = 18/08/2026. Las futuras capturas se incorporarán como nuevos snapshots para construir históricos.")
