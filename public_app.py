
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

ROOT = Path(__file__).parent
scores = pd.read_csv(ROOT / "data" / "scores.csv")
econ = pd.read_csv(ROOT / "data" / "team_economy.csv")

st.set_page_config(page_title="Futmondo · Liga", page_icon="🏆", layout="wide")
st.title("🏆 Rates 2026–2027")
st.caption("Dashboard público de la liga")

latest = scores.sort_values("round").groupby("team", as_index=False).tail(1)
latest = latest.sort_values(["total_points","team"], ascending=[False, True])

c1, c2, c3 = st.columns(3)
c1.metric("Participantes", latest["team"].nunique())
c2.metric("Jornada actual", int(scores["round"].max()))
leader = latest.iloc[0]["team"] if len(latest) else "—"
c3.metric("Líder", leader)

st.subheader("Clasificación")
rank = latest[["team","total_points"]].copy()
rank.insert(0, "Pos.", range(1, len(rank)+1))
rank.columns = ["Pos.","Equipo","Puntos"]
st.dataframe(rank, use_container_width=True, hide_index=True)

st.subheader("Progreso de puntos acumulados")
fig = px.line(
    scores, x="round", y="total_points", color="team", markers=True,
    labels={"round":"Jornada","total_points":"Puntos acumulados","team":"Equipo"}
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Puntos por jornada")
fig2 = px.line(
    scores, x="round", y="round_points", color="team", markers=True,
    labels={"round":"Jornada","round_points":"Puntos de la jornada","team":"Equipo"}
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Fantasy Stats")
if scores["round"].max() == 0:
    st.info("Todavía no hay jornadas puntuadas. Estas estadísticas se activarán automáticamente a partir de J1.")
    cols = st.columns(4)
    cols[0].metric("Récord de jornada", "—")
    cols[1].metric("Más veces >100", "—")
    cols[2].metric("Más jornadas líder", "—")
    cols[3].metric("Mayor remontada", "—")
else:
    real = scores[scores["round"] > 0]
    rec = real.loc[real["round_points"].idxmax()]
    over100 = real.assign(over=real["round_points"]>100).groupby("team")["over"].sum().sort_values(ascending=False)
    cols = st.columns(4)
    cols[0].metric("Récord de jornada", rec["team"], f"J{int(rec['round'])} · {int(rec['round_points'])} pts")
    cols[1].metric("Más veces >100", over100.index[0], f"{int(over100.iloc[0])} jornadas")
    cols[2].metric("Más jornadas líder", "Calculable", "Con histórico")
    cols[3].metric("Mayor remontada", "Calculable", "Con histórico")

st.subheader("Valor de plantillas · Snapshot 18/08/2026")
fig3 = px.bar(
    econ.sort_values("squad_value_eur", ascending=False),
    x="team", y="squad_value_eur",
    labels={"team":"Equipo","squad_value_eur":"Valor de plantilla (€)"}
)
st.plotly_chart(fig3, use_container_width=True)

st.caption("El dashboard público no muestra la estimación privada de liquidez.")
