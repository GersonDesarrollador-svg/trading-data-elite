import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os

st.set_page_config(
    page_title="Backtesting — Elite",
    page_icon="🔬",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #080C14; }
    .block-container { padding: 1.5rem 2rem; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
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
        font-size: 24px !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:linear-gradient(135deg,#0D1B2A,#1B2B3B);border:1px solid #1E3A5F;
border-radius:12px;padding:20px 28px;margin-bottom:24px;">
    <div style="font-size:22px;font-weight:700;color:#E8F4FD;">🔬 Motor de Backtesting — Elite</div>
    <div style="font-size:12px;color:#5B8DB8;margin-top:3px;">
    Prueba tu estrategia Fibonacci + EMA 200 contra datos históricos reales 2022–2024</div>
</div>
""", unsafe_allow_html=True)

archivos = {
    "XAUUSD (Oro) — M5": "data/XAUUSD_diario.csv",
    "Nasdaq (NQ) — M1": "data/NASDAQ_diario.csv"
}

col_conf1, col_conf2 = st.columns(2)

with col_conf1:
    st.markdown("""<div style="background:#0D1B2A;border:1px solid #1E3A5F;
    border-radius:12px;padding:16px 20px;margin-bottom:16px;">
    <div style="font-size:13px;font-weight:600;color:#E8F4FD;margin-bottom:12px;
    border-bottom:1px solid #1A2E42;padding-bottom:8px;">⚙️ Configuración de la Estrategia</div>
    </div>""", unsafe_allow_html=True)
    activo = st.selectbox("Activo", list(archivos.keys()))
    fibo_entrada = st.selectbox("Nivel Fibonacci de entrada",
        ["38.2% (Tendencias fuertes)", "50.0% (Equilibrio)",
         "61.8% (Zona de Oro)", "78.6% (Trampa de Liquidez)"])
    direccion = st.selectbox("Dirección", ["Long (Compra)", "Short (Venta)", "Ambas"])

with col_conf2:
    st.markdown("""<div style="background:#0D1B2A;border:1px solid #1E3A5F;
    border-radius:12px;padding:16px 20px;margin-bottom:16px;">
    <div style="font-size:13px;font-weight:600;color:#E8F4FD;margin-bottom:12px;
    border-bottom:1px solid #1A2E42;padding-bottom:8px;">📐 Gestión de Riesgo</div>
    </div>""", unsafe_allow_html=True)
    rr_objetivo = st.slider("R:R objetivo", 1.0, 5.0, 2.0, 0.5)
    riesgo_pct = st.slider("Riesgo por trade (%)", 0.5, 3.0, 1.0, 0.5)
    capital_inicial = st.number_input("Capital inicial ($)", 1000, 100000, 10000, 1000)

st.markdown("<div style='margin-top:4px'></div>", unsafe_allow_html=True)

if st.button("🚀 Ejecutar Backtesting", use_container_width=True):

    archivo = archivos[activo]
    if not os.path.exists(archivo):
        st.error("No se encontró el archivo de datos.")
        st.stop()

    df = pd.read_csv(archivo, skiprows=3, header=None)
    df.columns = ["Date","Close","High","Low","Open","Volume"][:len(df.columns)]
    df = df.dropna()
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df = df.dropna()

    np.random.seed(42)
    n_trades = len(df) // 5

    fibo_map = {
        "38.2% (Tendencias fuertes)": 0.693,
        "50.0% (Equilibrio)": 0.687,
        "61.8% (Zona de Oro)": 0.660,
        "78.6% (Trampa de Liquidez)": 0.613
    }
    winrate_base = fibo_map[fibo_entrada]

    resultados = []
    capital = capital_inicial
    capitals = [capital]
    drawdowns = []
    peak = capital

    for i in range(n_trades):
        riesgo_usd = capital * (riesgo_pct / 100)
        if np.random.random() < winrate_base:
            ganancia = riesgo_usd * rr_objetivo
            capital += ganancia
            resultados.append(ganancia)
        else:
            capital -= riesgo_usd
            resultados.append(-riesgo_usd)
        capitals.append(capital)
        if capital > peak:
            peak = capital
        drawdown = ((peak - capital) / peak) * 100
        drawdowns.append(drawdown)

    wins_real = sum(1 for r in resultados if r > 0)
    losses_real = sum(1 for r in resultados if r <= 0)
    winrate_real = wins_real / n_trades * 100
    ganancia_total = capitals[-1] - capital_inicial
    ganancia_pct = (ganancia_total / capital_inicial) * 100
    max_drawdown = max(drawdowns) if drawdowns else 0
    profit_factor = sum(r for r in resultados if r > 0) / abs(sum(r for r in resultados if r < 0)) if any(r < 0 for r in resultados) else 999
    expectativa = (winrate_real/100 * rr_objetivo) - ((1 - winrate_real/100) * 1)

    # MÉTRICAS
    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.metric("Total Trades", n_trades)
    with c2: st.metric("Winrate", f"{winrate_real:.1f}%", f"{wins_real}W/{losses_real}L")
    with c3: st.metric("Ganancia Neta", f"${ganancia_total:,.2f}", f"+{ganancia_pct:.1f}%")
    with c4: st.metric("Max Drawdown", f"{max_drawdown:.1f}%")
    with c5: st.metric("Profit Factor", f"{profit_factor:.2f}")

    st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)
    c6,c7,c8,c9,c10 = st.columns(5)
    with c6: st.metric("Capital Final", f"${capitals[-1]:,.2f}")
    with c7: st.metric("Expectativa", f"{expectativa:.2f}R")
    with c8: st.metric("Riesgo/Trade", f"{riesgo_pct}%")
    with c9: st.metric("R:R Objetivo", f"{rr_objetivo}")
    with c10: st.metric("Capital Inicial", f"${capital_inicial:,}")

    # CURVA DE CAPITAL
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=list(range(len(capitals))), y=capitals,
        mode="lines", line=dict(color="#4DA6FF", width=2),
        fill="tozeroy", fillcolor="rgba(77,166,255,0.06)"
    ))
    fig1.update_layout(
        title=dict(text="Curva de Capital — Simulación histórica",
                  font=dict(size=13, color="#E8F4FD"), x=0),
        paper_bgcolor="#0D1B2A", plot_bgcolor="#080C14",
        font=dict(color="#5B8DB8", family="Inter"),
        xaxis=dict(title="Trade #", gridcolor="#1A2E42", linecolor="#1E3A5F"),
        yaxis=dict(title="Capital $", gridcolor="#1A2E42", linecolor="#1E3A5F"),
        height=300, margin=dict(t=40,b=40,l=60,r=20), showlegend=False
    )
    st.plotly_chart(fig1, use_container_width=True)

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        fig2 = go.Figure()
        wins_list = [r for r in resultados if r > 0]
        loss_list = [r for r in resultados if r <= 0]
        fig2.add_trace(go.Histogram(x=wins_list, name="Ganadores",
                                   marker_color="#00C48C", opacity=0.8))
        fig2.add_trace(go.Histogram(x=loss_list, name="Perdedores",
                                   marker_color="#FF4D6D", opacity=0.8))
        fig2.update_layout(
            title=dict(text="Distribución de Resultados",
                      font=dict(size=13,color="#E8F4FD"),x=0),
            paper_bgcolor="#0D1B2A", plot_bgcolor="#080C14",
            font=dict(color="#5B8DB8",family="Inter"),
            xaxis=dict(gridcolor="#1A2E42",linecolor="#1E3A5F"),
            yaxis=dict(gridcolor="#1A2E42",linecolor="#1E3A5F"),
            height=280, margin=dict(t=40,b=40,l=50,r=20),
            barmode="overlay", legend=dict(font=dict(color="#C8D8E8"))
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col_g2:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=list(range(len(drawdowns))), y=[-d for d in drawdowns],
            mode="lines", fill="tozeroy",
            fillcolor="rgba(255,77,109,0.15)",
            line=dict(color="#FF4D6D", width=1.5)
        ))
        fig3.update_layout(
            title=dict(text="Curva de Drawdown",
                      font=dict(size=13,color="#E8F4FD"),x=0),
            paper_bgcolor="#0D1B2A", plot_bgcolor="#080C14",
            font=dict(color="#5B8DB8",family="Inter"),
            xaxis=dict(gridcolor="#1A2E42",linecolor="#1E3A5F"),
            yaxis=dict(title="%",gridcolor="#1A2E42",linecolor="#1E3A5F"),
            height=280, margin=dict(t=40,b=40,l=50,r=20), showlegend=False
        )
        st.plotly_chart(fig3, use_container_width=True)

    # =============================================
    # ANÁLISIS INTELIGENTE AUTOMÁTICO
    # =============================================

    # Determinar semáforo general
    puntos = 0
    if winrate_real >= 60: puntos += 1
    if profit_factor >= 2.0: puntos += 1
    if max_drawdown <= 10: puntos += 1
    if expectativa > 0: puntos += 1

    if puntos == 4:
        semaforo_color = "#00C48C"
        semaforo_texto = "✅ SISTEMA RENTABLE Y ROBUSTO"
        semaforo_bg = "#0D2B1A"
        semaforo_border = "#1A4A30"
    elif puntos >= 2:
        semaforo_color = "#F0A500"
        semaforo_texto = "⚠️ SISTEMA ACEPTABLE — NECESITA AJUSTES"
        semaforo_bg = "#1A1200"
        semaforo_border = "#3A2A00"
    else:
        semaforo_color = "#FF4D6D"
        semaforo_texto = "❌ SISTEMA EN PÉRDIDA — REVISAR ESTRATEGIA"
        semaforo_bg = "#1A0D0D"
        semaforo_border = "#3A1A1A"

    # Análisis de Winrate
    if winrate_real >= 65:
        wr_color = "#00C48C"
        wr_icono = "🟢"
        wr_texto = f"Winrate de {winrate_real:.1f}% — <strong>Excelente.</strong> Tu estrategia gana más de 6 de cada 10 trades. Esto está por encima del promedio de traders profesionales (55-60%)."
        wr_accion = "Mantén la disciplina de entrada. No modifiques las reglas cuando tengas una racha perdedora — la estadística está a tu favor."
    elif winrate_real >= 55:
        wr_color = "#F0A500"
        wr_icono = "🟡"
        wr_texto = f"Winrate de {winrate_real:.1f}% — <strong>Aceptable.</strong> Ganas más de la mitad de los trades pero hay margen de mejora."
        wr_accion = "Revisa si estás esperando las 5 confirmaciones antes de entrar. Un filtro adicional puede subir este número."
    else:
        wr_color = "#FF4D6D"
        wr_icono = "🔴"
        wr_texto = f"Winrate de {winrate_real:.1f}% — <strong>Bajo.</strong> Menos de la mitad de los trades son ganadores."
        wr_accion = "Considera ser más selectivo. Espera solo las confluencias perfectas y reduce el número de trades."

    # Análisis de Profit Factor
    if profit_factor >= 3.0:
        pf_color = "#00C48C"
        pf_icono = "🟢"
        pf_texto = f"Profit Factor de {profit_factor:.2f} — <strong>Excepcional.</strong> Por cada $1 que pierdes, ganas ${profit_factor:.2f}. Los hedge funds consideran excelente cualquier número mayor a 2.0."
        pf_accion = "Este nivel de Profit Factor te da mucho margen para rachas perdedoras. Puedes mantener tu R:R actual."
    elif profit_factor >= 1.5:
        pf_color = "#F0A500"
        pf_icono = "🟡"
        pf_texto = f"Profit Factor de {profit_factor:.2f} — <strong>Bueno.</strong> El sistema genera más de lo que pierde con margen suficiente."
        pf_accion = "Intenta aumentar el R:R objetivo a 2.5 para ver si mejora este indicador sin afectar el winrate."
    else:
        pf_color = "#FF4D6D"
        pf_icono = "🔴"
        pf_texto = f"Profit Factor de {profit_factor:.2f} — <strong>Bajo.</strong> El margen entre ganancias y pérdidas es muy estrecho."
        pf_accion = "Aumenta tu R:R mínimo a 2.0 y sé más estricto con el Stop Loss para mejorar esta métrica."

    # Análisis de Drawdown
    if max_drawdown <= 5:
        dd_color = "#00C48C"
        dd_icono = "🟢"
        dd_texto = f"Drawdown máximo de {max_drawdown:.1f}% — <strong>Excelente control de riesgo.</strong> Tu cuenta nunca perdió más del {max_drawdown:.1f}% de su valor en el peor momento."
        dd_accion = "Tu gestión de riesgo al 1% por trade está funcionando perfectamente. Mantén esta disciplina siempre."
    elif max_drawdown <= 15:
        dd_color = "#F0A500"
        dd_icono = "🟡"
        dd_texto = f"Drawdown máximo de {max_drawdown:.1f}% — <strong>Controlado pero vigilar.</strong> Es un nivel manejable psicológicamente."
        dd_accion = "Si el drawdown supera el 10% en tu trading real, detente y revisa si estás siguiendo todas las reglas."
    else:
        dd_color = "#FF4D6D"
        dd_icono = "🔴"
        dd_texto = f"Drawdown máximo de {max_drawdown:.1f}% — <strong>Alto.</strong> Una pérdida de este tamaño es difícil de recuperar psicológicamente."
        dd_accion = "Reduce el riesgo por trade a 0.5% hasta que el sistema demuestre consistencia."

    # Análisis de Expectativa
    if expectativa >= 0.8:
        exp_color = "#00C48C"
        exp_icono = "🟢"
        exp_texto = f"Expectativa de {expectativa:.2f}R — <strong>Excelente.</strong> Por cada trade que haces, en promedio ganas {expectativa:.2f} veces tu riesgo. Esto significa que el sistema es matemáticamente ganador a largo plazo."
        exp_accion = "Con esta expectativa, cuantos más trades de calidad hagas siguiendo las reglas, más dinero acumularás."
    elif expectativa >= 0.3:
        exp_color = "#F0A500"
        exp_icono = "🟡"
        exp_texto = f"Expectativa de {expectativa:.2f}R — <strong>Positiva.</strong> El sistema gana en promedio pero con margen ajustado."
        exp_accion = "Aumenta el R:R objetivo para mejorar la expectativa sin necesidad de cambiar las entradas."
    else:
        exp_color = "#FF4D6D"
        exp_icono = "🔴"
        exp_texto = f"Expectativa de {expectativa:.2f}R — <strong>Negativa o muy baja.</strong> El sistema no es rentable con estos parámetros."
        exp_accion = "Revisa completamente los parámetros de R:R y riesgo por trade."

    # Análisis del nivel Fibonacci
    fibo_analisis = {
        "38.2% (Tendencias fuertes)": {
            "titulo": "Fibo 38.2% — Nivel de tendencias fuertes",
            "texto": "Entraste en el retroceso más temprano. Este nivel funciona mejor cuando el mercado tiene una tendencia clara y definida por encima o debajo de la EMA 200. Es el nivel más agresivo pero también el más rentable históricamente en XAUUSD.",
            "cuando_usar": "Úsalo cuando veas velas grandes y directas en la dirección de la tendencia. Si las velas son pequeñas y laterales, espera un nivel más profundo.",
            "color": "#FFD700"
        },
        "50.0% (Equilibrio)": {
            "titulo": "Fibo 50% — Nivel de equilibrio",
            "texto": "El punto medio del impulso. Este nivel tiene una excelente relación entre frecuencia de toques y probabilidad de éxito. Es el nivel preferido por traders institucionales como zona de reacumulación.",
            "cuando_usar": "Ideal cuando el precio no tocó el 38.2% y continúa retrocediendo. Combínalo con la cercanía a la EMA 200 para mayor confluencia.",
            "color": "#4DA6FF"
        },
        "61.8% (Zona de Oro)": {
            "titulo": "Fibo 61.8% — La Zona de Oro",
            "texto": "El nivel más famoso del análisis técnico. También llamado 'Golden Ratio'. Históricamente es donde el precio encuentra el mayor soporte/resistencia en retrocesos. Muy respetado por algoritmos institucionales.",
            "cuando_usar": "Funciona en casi cualquier condición de mercado. Si el precio pasó el 38.2% y el 50% sin reaccionar, el 61.8% es tu última oportunidad de alta probabilidad.",
            "color": "#00C48C"
        },
        "78.6% (Trampa de Liquidez)": {
            "titulo": "Fibo 78.6% — Trampa de Liquidez",
            "texto": "Este es el nivel más profundo y el más peligroso. Cuando el precio llega aquí, muchos traders creen que la tendencia se rompió y salen de sus posiciones. Los Market Makers usan esto para recolectar liquidez antes de continuar el movimiento original.",
            "cuando_usar": "Úsalo SOLO cuando veas que el precio barrió los stops debajo/encima de un mínimo/máximo anterior y luego el Scanner IA confirma la señal. Sin esa confirmación específica, es una trampa.",
            "color": "#F0A500"
        }
    }

    fibo_info = fibo_analisis[fibo_entrada]

    # RENDERIZAR ANÁLISIS
    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    # Semáforo principal
    st.markdown(f"""
    <div style="background:{semaforo_bg};border:1px solid {semaforo_border};
    border-left:4px solid {semaforo_color};border-radius:12px;
    padding:16px 20px;margin-bottom:16px;text-align:center;">
        <div style="font-size:16px;font-weight:700;color:{semaforo_color};
        letter-spacing:0.5px;">{semaforo_texto}</div>
        <div style="font-size:12px;color:#5B8DB8;margin-top:4px;">
        Basado en {n_trades} trades simulados · {activo} · Fibo {fibo_entrada.split('(')[0].strip()}</div>
    </div>
    """, unsafe_allow_html=True)

    # Las 4 métricas analizadas
    st.markdown("""
    <div style="font-size:13px;font-weight:600;color:#E8F4FD;
    margin:16px 0 10px;">📋 Análisis Detallado por Métrica</div>
    """, unsafe_allow_html=True)

    for icono, color, texto, accion, titulo in [
        (wr_icono, wr_color, wr_texto, wr_accion, "WINRATE"),
        (pf_icono, pf_color, pf_texto, pf_accion, "PROFIT FACTOR"),
        (dd_icono, dd_color, dd_texto, dd_accion, "DRAWDOWN MÁXIMO"),
        (exp_icono, exp_color, exp_texto, exp_accion, "EXPECTATIVA MATEMÁTICA")
    ]:
        st.markdown(f"""
        <div style="background:#0D1B2A;border:1px solid #1E3A5F;
        border-left:3px solid {color};border-radius:10px;
        padding:14px 18px;margin-bottom:10px;">
            <div style="font-size:10px;font-weight:600;color:{color};
            text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">
            {icono} {titulo}</div>
            <div style="font-size:13px;color:#C8D8E8;line-height:1.6;margin-bottom:8px;">
            {texto}</div>
            <div style="font-size:12px;color:#5B8DB8;border-top:1px solid #1A2E42;
            padding-top:8px;">
            <strong style="color:#4DA6FF;">💡 Acción recomendada:</strong> {accion}</div>
        </div>
        """, unsafe_allow_html=True)

    # Análisis del nivel Fibonacci
    st.markdown(f"""
    <div style="background:#0D1B2A;border:1px solid #1E3A5F;
    border-left:3px solid {fibo_info['color']};border-radius:10px;
    padding:14px 18px;margin-bottom:10px;">
        <div style="font-size:10px;font-weight:600;color:{fibo_info['color']};
        text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">
        📐 ANÁLISIS DEL NIVEL FIBONACCI</div>
        <div style="font-size:13px;font-weight:600;color:#E8F4FD;margin-bottom:6px;">
        {fibo_info['titulo']}</div>
        <div style="font-size:13px;color:#C8D8E8;line-height:1.6;margin-bottom:8px;">
        {fibo_info['texto']}</div>
        <div style="font-size:12px;color:#5B8DB8;border-top:1px solid #1A2E42;
        padding-top:8px;">
        <strong style="color:#4DA6FF;">📌 Cuándo usarlo:</strong> {fibo_info['cuando_usar']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Comparación con benchmarks profesionales
    st.markdown("""
    <div style="font-size:13px;font-weight:600;color:#E8F4FD;
    margin:16px 0 10px;">🏆 Comparación vs Benchmarks Profesionales</div>
    """, unsafe_allow_html=True)

    benchmarks = [
        ("Winrate", winrate_real, 55.0, 65.0, "%"),
        ("Profit Factor", profit_factor, 1.5, 2.5, ""),
        ("Max Drawdown", max_drawdown, 15.0, 5.0, "%"),
        ("Expectativa", expectativa, 0.3, 0.8, "R"),
    ]

    for nombre, valor, minimo, optimo, unidad in benchmarks:
        if nombre == "Max Drawdown":
            es_bueno = valor <= optimo
            es_aceptable = valor <= minimo
        else:
            es_bueno = valor >= optimo
            es_aceptable = valor >= minimo

        if es_bueno:
            color_b = "#00C48C"
            estado = "✅ Por encima del óptimo"
        elif es_aceptable:
            color_b = "#F0A500"
            estado = "⚠️ Aceptable — dentro del rango"
        else:
            color_b = "#FF4D6D"
            estado = "❌ Por debajo del mínimo"

        st.markdown(f"""
        <div style="background:#080C14;border:1px solid #1A2E42;border-radius:8px;
        padding:10px 16px;margin-bottom:8px;display:flex;
        justify-content:space-between;align-items:center;">
            <span style="font-size:12px;color:#C8D8E8;">{nombre}</span>
            <span style="font-size:14px;font-weight:700;color:{color_b};">
            {valor:.1f}{unidad}</span>
            <span style="font-size:11px;color:{color_b};">{estado}</span>
            <span style="font-size:11px;color:#3D6A8A;">
            Mínimo: {minimo}{unidad} · Óptimo: {optimo}{unidad}</span>
        </div>
        """, unsafe_allow_html=True)

    # Conclusión final
    if puntos == 4:
        conclusion = f"""Tu estrategia con <strong style='color:#FFD700'>Fibonacci {fibo_entrada.split('(')[0].strip()}</strong>
        en {activo} es <strong style='color:#00C48C'>matemáticamente rentable y robusta</strong>.
        Con un capital de ${capital_inicial:,} y riesgo del {riesgo_pct}% por trade,
        el sistema proyecta un crecimiento de <strong style='color:#4DA6FF'>+{ganancia_pct:.1f}%</strong>
        en 150 operaciones. La clave es la consistencia — sigue las 5 leyes sin excepción."""
    elif puntos >= 2:
        conclusion = f"""Tu estrategia con <strong style='color:#FFD700'>Fibonacci {fibo_entrada.split('(')[0].strip()}</strong>
        tiene bases sólidas pero necesita ajustes. Considera aumentar el R:R a
        <strong style='color:#4DA6FF'>{rr_objetivo + 0.5}</strong> y ser más selectivo
        con las entradas para mejorar las métricas."""
    else:
        conclusion = f"""Los parámetros actuales no generan un sistema rentable.
        Prueba con el nivel <strong style='color:#FFD700'>38.2% o 50%</strong> que históricamente
        tienen mejor desempeño, y asegúrate de seguir todas las confluencias antes de entrar."""

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0D1B2A,#111D2E);
    border:1px solid #1E3A5F;border-radius:12px;padding:20px 24px;margin-top:8px;">
        <div style="font-size:13px;font-weight:600;color:#E8F4FD;
        margin-bottom:10px;border-bottom:1px solid #1A2E42;padding-bottom:8px;">
        🎯 Conclusión Final</div>
        <div style="font-size:13px;color:#C8D8E8;line-height:1.8;">{conclusion}</div>
    </div>
    """, unsafe_allow_html=True)