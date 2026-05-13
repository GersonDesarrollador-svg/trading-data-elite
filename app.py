import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import requests
import json
from datetime import datetime

# CONFIGURACIÓN SUPABASE
SUPABASE_URL = "https://ujurmsvhlmtncuhabwkr.supabase.co"
SUPABASE_KEY = "sb_publishable_joBF5glo4cmQofaeQ3gNNA__ByU6sxM"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def guardar_trade(data):
    url = f"{SUPABASE_URL}/rest/v1/trades"
    response = requests.post(url, headers=HEADERS, json=data)
    return response.status_code in [200, 201]

def obtener_trades():
    url = f"{SUPABASE_URL}/rest/v1/trades?select=*&order=created_at.desc"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return []

st.set_page_config(
    page_title="Trading Elite — Sistema de Data",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #080C14; }
    .block-container { padding: 1.5rem 2rem; }
    [data-testid="stSidebar"] { background-color: #0D1B2A; border-right: 1px solid #1E3A5F; }
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
    .stButton > button {
        background: #185FA5;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 600;
        width: 100%;
        padding: 12px;
    }
    .stButton > button:hover { background: #4DA6FF; }
</style>
""", unsafe_allow_html=True)

# MENÚ LATERAL
st.sidebar.markdown("""
<div style="padding:20px 0 10px 0;">
    <div style="font-size:18px;font-weight:700;color:#4DA6FF;">📊 Trading Elite</div>
    <div style="font-size:11px;color:#5B8DB8;margin-top:3px;">XAUUSD · Nasdaq · Scanner IA</div>
</div>
""", unsafe_allow_html=True)

pagina = st.sidebar.radio(
    "Navegación",
    ["🏠 Inicio", "📓 Diario de Trades", "📊 Dashboard", "🔬 Backtesting"],
    key="navegacion"
)

st.sidebar.markdown("""
<div style="margin-top:20px;padding:12px;background:#111D2E;border-radius:8px;
border:1px solid #1E3A5F;font-size:11px;color:#5B8DB8;">
    <div style="font-weight:600;color:#4DA6FF;margin-bottom:6px;">Estado del sistema</div>
    ✅ Diario activo<br>✅ Dashboard activo<br>✅ Backtesting activo
</div>
""", unsafe_allow_html=True)

# ==================== INICIO ====================
if pagina == "🏠 Inicio":
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0D1B2A,#1B2B3B);border:1px solid #1E3A5F;
    border-radius:12px;padding:30px;margin-bottom:24px;text-align:center;">
        <div style="font-size:32px;font-weight:700;color:#E8F4FD;margin-bottom:8px;">
        📊 Sistema de Data Trading — Elite</div>
        <div style="font-size:14px;color:#5B8DB8;">
        XAUUSD · Nasdaq NQ/MNQ · Scanner IA + Fibonacci Pro</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background:#0D1B2A;border:1px solid #1E3A5F;border-radius:12px;
        padding:24px;text-align:center;margin-bottom:12px;">
            <div style="font-size:36px;">📓</div>
            <div style="font-size:16px;font-weight:600;color:#E8F4FD;margin:10px 0 6px;">Diario de Trades</div>
            <div style="font-size:12px;color:#5B8DB8;">Registra cada operación con las 5 leyes</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:#0D1B2A;border:1px solid #1E3A5F;border-radius:12px;
        padding:24px;text-align:center;margin-bottom:12px;">
            <div style="font-size:36px;">📊</div>
            <div style="font-size:16px;font-weight:600;color:#E8F4FD;margin:10px 0 6px;">Dashboard</div>
            <div style="font-size:12px;color:#5B8DB8;">Visualiza tus estadísticas en tiempo real</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background:#0D1B2A;border:1px solid #1E3A5F;border-radius:12px;
        padding:24px;text-align:center;margin-bottom:12px;">
            <div style="font-size:36px;">🔬</div>
            <div style="font-size:16px;font-weight:600;color:#E8F4FD;margin:10px 0 6px;">Backtesting</div>
            <div style="font-size:12px;color:#5B8DB8;">Prueba tu estrategia contra datos históricos</div>
        </div>
        """, unsafe_allow_html=True)

# ==================== DIARIO ====================
elif pagina == "📓 Diario de Trades":
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0D1B2A,#1B2B3B);border:1px solid #1E3A5F;
    border-radius:12px;padding:20px 28px;margin-bottom:24px;">
        <div style="font-size:22px;font-weight:700;color:#E8F4FD;">📓 Diario de Trades — Elite</div>
        <div style="font-size:12px;color:#5B8DB8;margin-top:3px;">XAUUSD · Nasdaq · Método Scanner IA + Fibonacci</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_trade", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            activo = st.selectbox("Activo", ["XAUUSD (Oro) M5", "Nasdaq NQ M1", "Nasdaq MNQ M1"])
        with col2:
            direccion = st.selectbox("Dirección", ["Long", "Short"])

        col3, col4, col5 = st.columns(3)
        with col3:
            entrada = st.text_input("Precio entrada", placeholder="2334.50")
        with col4:
            stop_loss = st.text_input("Stop Loss", placeholder="2320.00")
        with col5:
            take_profit = st.text_input("Take Profit", placeholder="2363.00")

        col6, col7 = st.columns(2)
        with col6:
            resultado = st.text_input("Resultado ($)", placeholder="374.80 o -150.00")
            st.caption("Ganancia: 374.80 · Pérdida: -150.00")
        with col7:
            rr_obtenido = st.text_input("R:R obtenido", placeholder="2.1")

        col8, col9 = st.columns(2)
        with col8:
            setup = st.selectbox("Setup principal", [
                "Fibo 38.2% + EMA 200", "Fibo 50% + EMA 200",
                "Fibo 61.8% + EMA 200", "Scanner IA + Rechazo Vela",
                "Fibo 61.8% + Scanner IA", "Fibo 78.6% + Trampa Liquidez",
                "Orden Limitada 61.8%", "Otro"
            ])
        with col9:
            sesion = st.selectbox("Sesión", [
                "NY Open 9:30-10:30", "NY Mid 10:30-11:00",
                "London", "New York", "Asia"
            ])

        st.markdown("**Checklist — Las 5 Leyes**")
        ley_ema = st.selectbox("Ley 1 — EMA 200", ["SI", "NO"])
        ley_cierre = st.selectbox("Ley 2 — Cierre de vela", ["SI", "NO"])
        ley_espacio = st.selectbox("Ley 3 — Zona Fibonacci válida", ["SI", "NO"])
        ley_scanner = st.selectbox("Ley 4 — Flecha del Scanner IA", ["SI", "NO"])
        ley_stop = st.selectbox("Ley 5 — Stop Loss colocado", ["SI", "NO"])

        emocional = st.selectbox("Estado emocional", [
            "Confiado", "Neutral", "Ansioso", "FOMO", "Revenge"
        ])
        notas = st.text_area("Notas del trade", placeholder="¿Qué confluencias viste?")

        guardar = st.form_submit_button("💾 Guardar Trade")

        if guardar:
            if entrada and stop_loss and take_profit and resultado and rr_obtenido:
                try:
                    resultado_num = float(str(resultado).replace("+","").replace(",","."))
                    rr_num = float(str(rr_obtenido).replace(",","."))
                except:
                    st.error("El resultado y R:R deben ser números.")
                    st.stop()

                data = {
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "activo": activo,
                    "direccion": direccion,
                    "entrada": entrada,
                    "stop_loss": stop_loss,
                    "take_profit": take_profit,
                    "resultado": resultado_num,
                    "rr_obtenido": rr_num,
                    "setup": setup,
                    "sesion": sesion,
                    "ley_ema": ley_ema,
                    "ley_cierre": ley_cierre,
                    "ley_espacio": ley_espacio,
                    "ley_scanner": ley_scanner,
                    "ley_stop": ley_stop,
                    "emocional": emocional,
                    "notas": notas
                }
                if guardar_trade(data):
                    st.success(f"✅ Trade guardado correctamente — {data['fecha']}")
                else:
                    st.error("❌ Error al guardar. Verifica la conexión.")
            else:
                st.error("Por favor completa todos los campos obligatorios.")

# ==================== DASHBOARD ====================
elif pagina == "📊 Dashboard":
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0D1B2A,#1B2B3B);border:1px solid #1E3A5F;
    border-radius:12px;padding:20px 28px;margin-bottom:24px;display:flex;
    justify-content:space-between;align-items:center;">
        <div>
            <div style="font-size:22px;font-weight:700;color:#E8F4FD;">📊 Trading Dashboard — Elite</div>
            <div style="font-size:12px;color:#5B8DB8;margin-top:3px;">XAUUSD · Nasdaq NQ/MNQ · Scanner IA + Fibonacci Pro</div>
        </div>
        <div style="background:#0F3460;color:#4DA6FF;font-size:11px;font-weight:600;
        padding:5px 12px;border-radius:20px;border:1px solid #1E5A9C;">LIVE TRACKING</div>
    </div>
    """, unsafe_allow_html=True)

    trades = obtener_trades()

    if not trades:
        st.warning("⚠️ Aún no tienes trades registrados. Ve al Diario y registra tu primer trade.")
        st.stop()

    df = pd.DataFrame(trades)
    df["resultado"] = pd.to_numeric(df["resultado"], errors="coerce").fillna(0)
    df["rr_obtenido"] = pd.to_numeric(df["rr_obtenido"], errors="coerce").fillna(0)
    df["win"] = df["resultado"] > 0

    total = len(df)
    wins = int(df["win"].sum())
    losses = total - wins
    winrate = (wins / total * 100) if total > 0 else 0
    ganancia_total = df["resultado"].sum()
    rr_promedio = df["rr_obtenido"].mean()
    mejor_trade = df["resultado"].max()
    peor_trade = df["resultado"].min()
    expectativa = (winrate/100 * rr_promedio) - ((1 - winrate/100) * 1)

    col1,col2,col3,col4,col5 = st.columns(5)
    with col1: st.metric("📁 Total Trades", total)
    with col2: st.metric("🎯 Winrate", f"{winrate:.1f}%", f"{wins}W / {losses}L")
    with col3: st.metric("💰 Ganancia Neta", f"${ganancia_total:.2f}")
    with col4: st.metric("⚖️ R:R Promedio", f"{rr_promedio:.2f}")
    with col5: st.metric("🧮 Expectativa", f"{expectativa:.2f}R")

    st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)

    col6,col7,col8,col9,col10 = st.columns(5)
    with col6: st.metric("🏆 Mejor Trade", f"${mejor_trade:.2f}")
    with col7: st.metric("⚠️ Peor Trade", f"${peor_trade:.2f}")
    with col8: st.metric("📈 Ganadores", wins)
    with col9: st.metric("📉 Perdedores", losses)
    with col10: st.metric("🔥 Total", total)

    df["acumulado"] = df["resultado"].cumsum()
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
        if "setup" in df.columns:
            setup_stats = df.groupby("setup")["win"].agg(["sum","count"])
            setup_stats["winrate"] = (setup_stats["sum"]/setup_stats["count"]*100).round(1)
            setup_stats = setup_stats.reset_index()
            fig2 = go.Figure(go.Bar(
                x=setup_stats["setup"], y=setup_stats["winrate"],
                marker=dict(color=setup_stats["winrate"],
                           colorscale=[[0,"#FF4D6D"],[0.5,"#F0A500"],[1,"#00C48C"]],
                           line=dict(color="#0D1B2A", width=1))
            ))
            fig2.update_layout(
                title=dict(text="🎯 Winrate por Setup", font=dict(size=13,color="#E8F4FD"),x=0),
                paper_bgcolor="#0D1B2A", plot_bgcolor="#080C14",
                font=dict(color="#5B8DB8",family="Inter"),
                xaxis=dict(gridcolor="#1A2E42",linecolor="#1E3A5F",tickfont=dict(size=10)),
                yaxis=dict(title="%",gridcolor="#1A2E42",linecolor="#1E3A5F"),
                height=280, margin=dict(t=40,b=80,l=50,r=20), showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        if "sesion" in df.columns:
            sesion_stats = df.groupby("sesion")["win"].agg(["sum","count"])
            sesion_stats["winrate"] = (sesion_stats["sum"]/sesion_stats["count"]*100).round(1)
            sesion_stats = sesion_stats.reset_index()
            fig3 = go.Figure(go.Bar(
                x=sesion_stats["sesion"], y=sesion_stats["winrate"],
                marker=dict(color=sesion_stats["winrate"],
                           colorscale=[[0,"#FF4D6D"],[0.5,"#F0A500"],[1,"#00C48C"]],
                           line=dict(color="#0D1B2A", width=1))
            ))
            fig3.update_layout(
                title=dict(text="🕐 Winrate por Sesión", font=dict(size=13,color="#E8F4FD"),x=0),
                paper_bgcolor="#0D1B2A", plot_bgcolor="#080C14",
                font=dict(color="#5B8DB8",family="Inter"),
                xaxis=dict(gridcolor="#1A2E42",linecolor="#1E3A5F",tickfont=dict(size=10)),
                yaxis=dict(title="%",gridcolor="#1A2E42",linecolor="#1E3A5F"),
                height=280, margin=dict(t=40,b=80,l=50,r=20), showlegend=False
            )
            st.plotly_chart(fig3, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        activo_stats = df.groupby("activo")["resultado"].sum().reset_index()
        activo_stats = activo_stats[activo_stats["resultado"] != 0]
        if len(activo_stats) > 0:
            fig4 = go.Figure(go.Pie(
                labels=activo_stats["activo"],
                values=activo_stats["resultado"].abs(),
                hole=0.55,
                marker=dict(colors=["#4DA6FF","#00C48C","#F0A500"],
                           line=dict(color="#0D1B2A",width=2))
            ))
            fig4.update_layout(
                title=dict(text="💰 Ganancia por Activo", font=dict(size=13,color="#E8F4FD"),x=0),
                paper_bgcolor="#0D1B2A", font=dict(color="#5B8DB8",family="Inter"),
                height=280, margin=dict(t=40,b=20,l=20,r=20),
                legend=dict(font=dict(color="#C8D8E8"))
            )
            st.plotly_chart(fig4, use_container_width=True)

    with col_d:
        emo_stats = df.groupby("emocional")["resultado"].mean().reset_index()
        fig5 = go.Figure(go.Bar(
            x=emo_stats["emocional"], y=emo_stats["resultado"],
            marker=dict(color=emo_stats["resultado"],
                       colorscale=[[0,"#FF4D6D"],[0.5,"#F0A500"],[1,"#00C48C"]],
                       line=dict(color="#0D1B2A",width=1))
        ))
        fig5.update_layout(
            title=dict(text="🧠 Emoción vs Resultado", font=dict(size=13,color="#E8F4FD"),x=0),
            paper_bgcolor="#0D1B2A", plot_bgcolor="#080C14",
            font=dict(color="#5B8DB8",family="Inter"),
            xaxis=dict(gridcolor="#1A2E42",linecolor="#1E3A5F",tickfont=dict(size=10)),
            yaxis=dict(title="$ Promedio",gridcolor="#1A2E42",linecolor="#1E3A5F"),
            height=280, margin=dict(t=40,b=80,l=50,r=20), showlegend=False
        )
        st.plotly_chart(fig5, use_container_width=True)

    # TABLA Y EXPORTACIÓN
    st.markdown("""
    <div style="background:#0D1B2A;border:1px solid #1E3A5F;border-radius:12px;
    padding:16px 20px;margin-bottom:8px;">
    <div style="font-size:13px;font-weight:600;color:#E8F4FD;
    border-bottom:1px solid #1A2E42;padding-bottom:10px;margin-bottom:4px;">
    📋 Historial de Trades</div></div>
    """, unsafe_allow_html=True)

    cols_mostrar = ["fecha","activo","direccion","setup","sesion","resultado","rr_obtenido","emocional"]
    cols_disponibles = [c for c in cols_mostrar if c in df.columns]
    df_display = df[cols_disponibles].copy()
    df_display.columns = ["Fecha","Activo","Dirección","Setup","Sesión","Resultado $","R:R","Emoción"][:len(cols_disponibles)]
    st.dataframe(df_display, use_container_width=True, height=300)

    # EXPORTAR EXCEL
    import io
    buffer = io.BytesIO()
    df_display.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)
    st.download_button(
        label="📥 Descargar Track Record en Excel",
        data=buffer,
        file_name=f"track_record_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ==================== BACKTESTING ====================
elif pagina == "🔬 Backtesting":
    exec(open("backtesting.py").read())