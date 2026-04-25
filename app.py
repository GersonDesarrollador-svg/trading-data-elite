import streamlit as st

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
    [data-testid="stSidebar"] { background-color: #0D1B2A; border-right: 1px solid #1E3A5F; }
    [data-testid="stSidebar"] * { color: #E8F4FD !important; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# MENÚ LATERAL
st.sidebar.markdown("""
<div style="padding: 20px 0 10px 0;">
    <div style="font-size:18px;font-weight:700;color:#4DA6FF;">📊 Trading Elite</div>
    <div style="font-size:11px;color:#5B8DB8;margin-top:3px;">XAUUSD · Nasdaq · Scanner IA</div>
</div>
""", unsafe_allow_html=True)

pagina = st.sidebar.radio(
    "Navegación",
    ["🏠 Inicio", "📓 Diario de Trades", "📊 Dashboard", "🔬 Backtesting"]
)

st.sidebar.markdown("""
<div style="margin-top:20px;padding:12px;background:#111D2E;border-radius:8px;
border:1px solid #1E3A5F;font-size:11px;color:#5B8DB8;">
    <div style="font-weight:600;color:#4DA6FF;margin-bottom:6px;">Estado del sistema</div>
    ✅ Diario activo<br>
    ✅ Dashboard activo<br>
    ✅ Backtesting activo
</div>
""", unsafe_allow_html=True)

# PÁGINAS
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
        padding:24px;text-align:center;">
            <div style="font-size:36px;">📓</div>
            <div style="font-size:16px;font-weight:600;color:#E8F4FD;margin:10px 0 6px;">
            Diario de Trades</div>
            <div style="font-size:12px;color:#5B8DB8;">
            Registra cada operación con las 5 leyes y el checklist de tu estrategia</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:#0D1B2A;border:1px solid #1E3A5F;border-radius:12px;
        padding:24px;text-align:center;">
            <div style="font-size:36px;">📊</div>
            <div style="font-size:16px;font-weight:600;color:#E8F4FD;margin:10px 0 6px;">
            Dashboard</div>
            <div style="font-size:12px;color:#5B8DB8;">
            Visualiza tu winrate, R:R, curva de capital y estadísticas en tiempo real</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background:#0D1B2A;border:1px solid #1E3A5F;border-radius:12px;
        padding:24px;text-align:center;">
            <div style="font-size:36px;">🔬</div>
            <div style="font-size:16px;font-weight:600;color:#E8F4FD;margin:10px 0 6px;">
            Backtesting</div>
            <div style="font-size:12px;color:#5B8DB8;">
            Prueba tu estrategia Fibonacci contra datos históricos 2022-2024</div>
        </div>
        """, unsafe_allow_html=True)

elif pagina == "📓 Diario de Trades":
    st.markdown("""
    <div style="background:#0D1B2A;border:1px solid #1E3A5F;border-radius:12px;
    padding:16px 20px;margin-bottom:16px;">
        <div style="font-size:16px;font-weight:600;color:#E8F4FD;">📓 Diario de Trades</div>
        <div style="font-size:12px;color:#5B8DB8;margin-top:4px;">
        El diario se abre en una ventana separada para mayor comodidad</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <a href="http://127.0.0.1:5000" target="_blank">
    <button style="background:#185FA5;color:white;border:none;padding:12px 24px;
    border-radius:8px;font-size:14px;font-weight:bold;cursor:pointer;width:100%;">
    📓 Abrir Diario de Trades
    </button>
    </a>
    """, unsafe_allow_html=True)

elif pagina == "📊 Dashboard":
    exec(open("dashboard.py").read())

elif pagina == "🔬 Backtesting":
    exec(open("backtesting.py").read())