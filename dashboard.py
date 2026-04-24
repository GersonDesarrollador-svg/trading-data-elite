import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Trading Dashboard — Elite",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #080C14; }
    .block-container { padding: 1.5rem 2rem; max-width: 1400px; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #0D1B2A 0%, #111D2E 100%);
        border: 1px solid #1E3A5F;
        border-radius: 12px;
        padding: 16px 20px;
    }
    div[data-testid="metric-container"] label {
        color: #5B8DB8 !important;
        font-size: 11px !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #E8F4FD !important;
        font-size: 26px !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:linear-gradient(135deg,#0D1B2A,#1B2B3B);border:1px solid #1E3A5F;
border-radius:12px;padding:20px 28px;margin-bottom:24px;display:flex;
justify-content:space-between;align-items:center;">
    <div>
        <div style="font-size:22px;font-weight:700;color:#E8F4FD;">📊 Trading Dashboard — Elite</div>
        <div style="font-size:12px;color:#5B8DB8;margin-top:3px;">
        XAUUSD · Nasdaq NQ/MNQ · Scanner IA + Fibonacci Pro</div>
    </div>
    <div style="background:#0F3460;color:#4DA6FF;font-size:11px;font-weight:600;
    padding:5px 12px;border-radius:20px;border:1px solid #1E5A9C;">LIVE TRACKING</div>
</div>
""", unsafe_allow_html=True)

ARCHIVO = "data/trades.csv"
COLUMNAS = [
    "fecha","activo","direccion","entrada","stop_loss","take_profit",
    "resultado","rr_obtenido","setup","sesion",
    "ley_ema","ley_cierre","ley_espacio","ley_scanner","ley_stop",
    "emocional","notas"
]

if not os.path.exists(ARCHIVO):
    st.warning("⚠️ Aún no tienes trades registrados. Ve al Diario y registra tu primer trade.")
    st.stop()

try:
    df = pd.read_csv(ARCHIVO, names=COLUMNAS, skiprows=1, encoding="utf-8")
except Exception:
    df = pd.read_csv(ARCHIVO, names=COLUMNAS, skiprows=1, encoding="latin-1")

if len(df) == 0:
    st.warning("⚠️ Aún no tienes trades registrados.")
    st.stop()

# Limpiar resultado y rr
def limpiar(v):
    try:
        return float(str(v).strip().replace("+","").replace(",","."))
    except:
        return 0.0

df["resultado_num"] = df["resultado"].apply(limpiar)
df["rr_num"] = df["rr_obtenido"].apply(limpiar)
df["win"] = df["resultado_num"] > 0

total = len(df)
wins = int(df["win"].sum())
losses = total - wins
winrate = (wins / total * 100) if total > 0 else 0
ganancia_total = df["resultado_num"].sum()
rr_promedio = df["rr_num"].mean()
mejor_trade = df["resultado_num"].max()
peor_trade = df["resultado_num"].min()
expectativa = (winrate/100 * rr_promedio) - ((1 - winrate/100) * 1)

# MÉTRICAS FILA 1
col1,col2,col3,col4,col5 = st.columns(5)
with col1: st.metric("📁 Total Trades", total)
with col2: st.metric("🎯 Winrate", f"{winrate:.1f}%", f"{wins}W / {losses}L")
with col3: st.metric("💰 Ganancia Neta", f"${ganancia_total:.2f}")
with col4: st.metric("⚖️ R:R Promedio", f"{rr_promedio:.2f}")
with col5: st.metric("🧮 Expectativa", f"{expectativa:.2f}R")

st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)

# MÉTRICAS FILA 2
col6,col7,col8,col9,col10 = st.columns(5)
with col6: st.metric("🏆 Mejor Trade", f"${mejor_trade:.2f}")
with col7: st.metric("⚠️ Peor Trade", f"${peor_trade:.2f}")
with col8: st.metric("📈 Ganadores", wins)
with col9: st.metric("📉 Perdedores", losses)
with col10: st.metric("🔥 Total", total)

st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)

# CURVA DE CAPITAL
df["acumulado"] = df["resultado_num"].cumsum()
fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=list(range(1, len(df)+1)), y=df["acumulado"],
    mode="lines+markers",
    line=dict(color="#4DA6FF", width=2.5),
    marker=dict(size=6, color="#4DA6FF", line=dict(color="#0D1B2A", width=2)),
    fill="tozeroy", fillcolor="rgba(77,166,255,0.08)"
))
fig1.update_layout(
    title=dict(text="Curva de Capital Acumulada", font=dict(size=13, color="#E8F4FD"), x=0),
    paper_bgcolor="#0D1B2A", plot_bgcolor="#080C14",
    font=dict(color="#5B8DB8", family="Inter"),
    xaxis=dict(title="Trade #", gridcolor="#1A2E42", linecolor="#1E3A5F"),
    yaxis=dict(title="$ Acumulado", gridcolor="#1A2E42", linecolor="#1E3A5F"),
    height=280, margin=dict(t=40,b=40,l=50,r=20), showlegend=False
)
st.plotly_chart(fig1, use_container_width=True)

col_a, col_b = st.columns(2)

with col_a:
    setup_stats = df.groupby("setup")["win"].agg(["sum","count"])
    setup_stats["winrate"] = (setup_stats["sum"] / setup_stats["count"] * 100).round(1)
    setup_stats = setup_stats.reset_index()
    fig2 = go.Figure(go.Bar(
        x=setup_stats["setup"], y=setup_stats["winrate"],
        marker=dict(color=setup_stats["winrate"],
                   colorscale=[[0,"#FF4D6D"],[0.5,"#F0A500"],[1,"#00C48C"]],
                   line=dict(color="#0D1B2A", width=1))
    ))
    fig2.update_layout(
        title=dict(text="🎯 Winrate por Setup", font=dict(size=13, color="#E8F4FD"), x=0),
        paper_bgcolor="#0D1B2A", plot_bgcolor="#080C14",
        font=dict(color="#5B8DB8", family="Inter"),
        xaxis=dict(gridcolor="#1A2E42", linecolor="#1E3A5F", tickfont=dict(size=10)),
        yaxis=dict(title="%", gridcolor="#1A2E42", linecolor="#1E3A5F"),
        height=280, margin=dict(t=40,b=80,l=50,r=20), showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

with col_b:
    sesion_stats = df.groupby("sesion")["win"].agg(["sum","count"])
    sesion_stats["winrate"] = (sesion_stats["sum"] / sesion_stats["count"] * 100).round(1)
    sesion_stats = sesion_stats.reset_index()
    fig3 = go.Figure(go.Bar(
        x=sesion_stats["sesion"], y=sesion_stats["winrate"],
        marker=dict(color=sesion_stats["winrate"],
                   colorscale=[[0,"#FF4D6D"],[0.5,"#F0A500"],[1,"#00C48C"]],
                   line=dict(color="#0D1B2A", width=1))
    ))
    fig3.update_layout(
        title=dict(text="🕐 Winrate por Sesión", font=dict(size=13, color="#E8F4FD"), x=0),
        paper_bgcolor="#0D1B2A", plot_bgcolor="#080C14",
        font=dict(color="#5B8DB8", family="Inter"),
        xaxis=dict(gridcolor="#1A2E42", linecolor="#1E3A5F", tickfont=dict(size=10)),
        yaxis=dict(title="%", gridcolor="#1A2E42", linecolor="#1E3A5F"),
        height=280, margin=dict(t=40,b=80,l=50,r=20), showlegend=False
    )
    st.plotly_chart(fig3, use_container_width=True)

col_c, col_d = st.columns(2)

with col_c:
    activo_stats = df.groupby("activo")["resultado_num"].sum().reset_index()
    activo_stats = activo_stats[activo_stats["resultado_num"] != 0]
    if len(activo_stats) > 0:
        fig4 = go.Figure(go.Pie(
            labels=activo_stats["activo"],
            values=activo_stats["resultado_num"].abs(),
            hole=0.55,
            marker=dict(colors=["#4DA6FF","#00C48C","#F0A500"],
                       line=dict(color="#0D1B2A", width=2))
        ))
        fig4.update_layout(
            title=dict(text="💰 Ganancia por Activo", font=dict(size=13, color="#E8F4FD"), x=0),
            paper_bgcolor="#0D1B2A", font=dict(color="#5B8DB8", family="Inter"),
            height=280, margin=dict(t=40,b=20,l=20,r=20),
            legend=dict(font=dict(color="#C8D8E8"))
        )
        st.plotly_chart(fig4, use_container_width=True)

with col_d:
    emo_stats = df.groupby("emocional")["resultado_num"].mean().reset_index()
    fig5 = go.Figure(go.Bar(
        x=emo_stats["emocional"], y=emo_stats["resultado_num"],
        marker=dict(color=emo_stats["resultado_num"],
                   colorscale=[[0,"#FF4D6D"],[0.5,"#F0A500"],[1,"#00C48C"]],
                   line=dict(color="#0D1B2A", width=1))
    ))
    fig5.update_layout(
        title=dict(text="🧠 Emoción vs Resultado", font=dict(size=13, color="#E8F4FD"), x=0),
        paper_bgcolor="#0D1B2A", plot_bgcolor="#080C14",
        font=dict(color="#5B8DB8", family="Inter"),
        xaxis=dict(gridcolor="#1A2E42", linecolor="#1E3A5F", tickfont=dict(size=10)),
        yaxis=dict(title="$ Promedio", gridcolor="#1A2E42", linecolor="#1E3A5F"),
        height=280, margin=dict(t=40,b=80,l=50,r=20), showlegend=False
    )
    st.plotly_chart(fig5, use_container_width=True)

# TABLA HISTORIAL
st.markdown("""
<div style="background:#0D1B2A;border:1px solid #1E3A5F;border-radius:12px;
padding:16px 20px;margin-bottom:8px;">
<div style="font-size:13px;font-weight:600;color:#E8F4FD;
border-bottom:1px solid #1A2E42;padding-bottom:10px;margin-bottom:4px;">
📋 Historial de Trades
</div>
</div>
""", unsafe_allow_html=True)

df_display = df[["fecha","activo","direccion","setup","sesion",
                  "resultado","rr_obtenido","emocional"]].copy()
df_display.columns = ["Fecha","Activo","Dirección","Setup","Sesión",
                       "Resultado $","R:R","Emoción"]
st.dataframe(df_display, use_container_width=True, height=300)