import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Optimización Multiobjetivo · Unidad HDS",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# ESTILOS VISUALES
# ==============================================================================
st.markdown(
    """
    <style>
        /* Fondo general claro con matiz crema-rosado muy sutil */
        .stApp {
            background-color: #FAF6F8;
            color: #2D1E26;
        }

        /* Barra lateral elegante en rosa empolvado */
        section[data-testid="stSidebar"] {
            background-color: #F3E9EE;
            border-right: 1px solid #E5D3DC;
        }
        section[data-testid="stSidebar"] * {
            color: #2D1E26;
        }

        /* Color ciruela en sliders y botones primarios */
        div[data-baseweb="slider"] div[role="slider"] {
            background-color: #8C3B60 !important;
            border-color: #8C3B60 !important;
        }
        button[kind="primary"] {
            background-color: #8C3B60 !important;
            border-color: #8C3B60 !important;
            color: #FFFFFF !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }
        button[kind="primary"]:hover {
            background-color: #702C4B !important;
            border-color: #702C4B !important;
        }

        /* Banner principal (Hero) */
        .hero-banner {
            background: linear-gradient(135deg, #6E2B4B 0%, #9E4C72 58%, #C47D99 100%);
            padding: 26px 32px;
            border-radius: 18px;
            color: #FFFFFF;
            margin-bottom: 18px;
            box-shadow: 0 8px 24px rgba(110, 43, 75, 0.16);
        }
        .hero-tag {
            display: inline-block;
            background: rgba(255, 255, 255, 0.18);
            border: 1px solid rgba(255, 255, 255, 0.30);
            padding: 4px 12px;
            border-radius: 999px;
            font-size: 0.78rem;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .hero-title {
            font-size: 1.9rem;
            font-weight: 700;
            margin: 0 0 6px 0;
            line-height: 1.2;
            color: #FFFFFF;
        }
        .hero-subtitle {
            font-size: 0.98rem;
            margin: 0 0 14px 0;
            color: #FBEFF4;
            max-width: 860px;
        }
        .hero-authors {
            display: inline-block;
            background: rgba(255, 255, 255, 0.92);
            color: #6E2B4B;
            padding: 6px 14px;
            border-radius: 10px;
            font-size: 0.88rem;
            font-weight: 600;
        }

        /* Tarjetas KPI */
        .kpi-card {
            background: #FFFFFF;
            border: 1px solid #EADCE3;
            border-top: 4px solid #8C3B60;
            border-radius: 14px;
            padding: 15px 18px;
            box-shadow: 0 3px 10px rgba(110, 43, 75, 0.05);
            height: 100%;
        }
        .kpi-label {
            font-size: 0.80rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: #7A5C6A;
            font-weight: 600;
            margin-bottom: 6px;
        }
        .kpi-value {
            font-size: 1.55rem;
            font-weight: 700;
            color: #2D1E26;
            line-height: 1.15;
        }
        .kpi-sub {
            font-size: 0.82rem;
            color: #6E5863;
            margin-top: 6px;
        }

        /* Caja explicativa académica */
        .guide-box {
            background: #FFFFFF;
            border-left: 4px solid #A8577D;
            border-top: 1px solid #EFE2E8;
            border-right: 1px solid #EFE2E8;
            border-bottom: 1px solid #EFE2E8;
            border-radius: 12px;
            padding: 14px 18px;
            margin: 10px 0 16px 0;
            font-size: 0.92rem;
            color: #3A2731;
            box-shadow: 0 2px 8px rgba(110, 43, 75, 0.04);
        }
        .guide-box b {
            color: #6E2B4B;
        }

        /* Diagrama de flujo interactivo del proceso */
        .flow-wrapper {
            background: #FFFFFF;
            border: 1px solid #EADCE3;
            border-radius: 16px;
            padding: 18px 20px;
            margin: 14px 0 18px 0;
            box-shadow: 0 3px 12px rgba(110, 43, 75, 0.05);
        }
        .flow-title {
            font-size: 0.88rem;
            font-weight: 700;
            color: #6E2B4B;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 12px;
        }
        .flow-grid {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
        }
        .flow-node {
            flex: 1 1 140px;
            background: #FCF8FA;
            border: 1px solid #E3CDD8;
            border-radius: 12px;
            padding: 10px 12px;
            text-align: center;
        }
        .flow-node.highlight {
            background: #F6E9F0;
            border: 1.5px solid #8C3B60;
        }
        .flow-code {
            font-size: 0.72rem;
            font-weight: 700;
            color: #8C3B60;
            letter-spacing: 0.05em;
        }
        .flow-name {
            font-size: 0.90rem;
            font-weight: 700;
            color: #2D1E26;
            margin: 2px 0 4px 0;
        }
        .flow-data {
            font-size: 0.79rem;
            color: #5E4652;
        }
        .flow-arrow {
            font-size: 1.25rem;
            color: #A8577D;
            font-weight: 700;
        }

        /* Pestañas estilizadas */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            border-bottom: 1px solid #E5D3DC;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #F4EBF0;
            border-radius: 10px 10px 0 0;
            padding: 10px 18px;
            color: #5C3A4B;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background-color: #8C3B60 !important;
            color: #FFFFFF !important;
        }

        /* Pie de página */
        .footer-note {
            text-align: center;
            color: #7A5C6A;
            font-size: 0.84rem;
            margin-top: 26px;
            padding-top: 14px;
            border-top: 1px solid #E8D9E1;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# PALETA DE COLORES PARA GRÁFICOS
# ==============================================================================
COLOR_PARETO = "#7D2E54"                        # Borgoña académico
COLOR_FACTIBLE = "rgba(208, 134, 168, 0.40)"    # Rosa empolvado
COLOR_NO_FACTIBLE = "rgba(182, 176, 194, 0.30)" # Lavanda suave
COLOR_KNEE = "#D99B26"                          # Dorado cálido
COLOR_ACTUAL_OK = "#2E8B75"                     # Verde salvia
COLOR_ACTUAL_ERR = "#C4455A"                    # Frambuesa
COLOR_BAR_MENOS = "#C57BA0"                     # Malva rosado
COLOR_BAR_MAS = "#6E2B4B"                       # Ciruela oscuro

# ==============================================================================
# CONSTANTES Y MODELO MATEMÁTICO
# ==============================================================================
R_GAS = 8.314       # J/(mol·K)
T_ALIM = 300.0      # K
DT_AD_MAX = 15.0    # K
S_SPEC = 10.0       # ppm

DEFAULTS = {
    "T_in": 614.0,
    "eps": 0.90,
    "m_dot": 100000.0,
    "S_in": 500.0,
    "Cp": 2.50,
    "Ea": 80000.0,
    "k0_factor": 1.00,
    "tau": 0.50,
    "n_T": 101,
    "n_eps": 61,
}

for clave, valor in DEFAULTS.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor


def restaurar_base():
    for clave, valor in DEFAULTS.items():
        st.session_state[clave] = valor


def calcular_k0_base(Ea_ref=80000.0, tau_ref=0.5):
    """Calibra el factor preexponencial para cumplir conversión de 0.985 a 600 K."""
    return -np.log(1.0 - 0.985) / (tau_ref * np.exp(-Ea_ref / (R_GAS * 600.0)))


K0_BASE = calcular_k0_base()


def evaluar_punto(T_in, eps, m_dot, S_in, Cp, Ea, k0, tau):
    """Evalúa cinética aparente de primer orden y balance térmico de la unidad HDS."""
    k = k0 * np.exp(-Ea / (R_GAS * T_in))
    Xs = 1.0 - np.exp(-k * tau)
    S_out = S_in * (1.0 - Xs)

    dT_ad = DT_AD_MAX * Xs
    T_efluente = T_in + dT_ad
    T_interc = T_ALIM + eps * (T_efluente - T_ALIM)

    # No se recortan valores negativos: representan excedente de calor recuperado
    Q_kJh = m_dot * Cp * (T_in - T_interc)
    Q_kW = Q_kJh / 3600.0
    factible = S_out <= S_SPEC

    return {
        "T_in": T_in,
        "eps": eps,
        "k": k,
        "Xs": Xs,
        "S_out": S_out,
        "dT_ad": dT_ad,
        "T_efluente": T_efluente,
        "T_interc": T_interc,
        "Q_kJh": Q_kJh,
        "Q_kW": Q_kW,
        "factible": factible,
    }


@st.cache_data(show_spinner="Generando malla y calculando frontera de Pareto...")
def ejecutar_optimizacion(m_dot, S_in, Cp, Ea, k0, tau, n_T, n_eps):
    """Ejecuta Grid Search, filtra puntos no dominados y calcula el punto de rodilla."""
    T_vals = np.linspace(550.0, 650.0, n_T)
    eps_vals = np.linspace(0.60, 0.90, n_eps)
    TT, EE = np.meshgrid(T_vals, eps_vals, indexing="ij")

    T_flat = TT.ravel()
    E_flat = EE.ravel()

    k_arr = k0 * np.exp(-Ea / (R_GAS * T_flat))
    Xs_arr = 1.0 - np.exp(-k_arr * tau)
    S_out_arr = S_in * (1.0 - Xs_arr)

    T_efl_arr = T_flat + DT_AD_MAX * Xs_arr
    T_int_arr = T_ALIM + E_flat * (T_efl_arr - T_ALIM)
    Q_kJh_arr = m_dot * Cp * (T_flat - T_int_arr)
    Q_kW_arr = Q_kJh_arr / 3600.0
    fact_arr = S_out_arr <= S_SPEC

    df_malla = pd.DataFrame({
        "T_in": T_flat,
        "eps": E_flat,
        "Xs": Xs_arr,
        "S_out": S_out_arr,
        "T_efluente": T_efl_arr,
        "T_interc": T_int_arr,
        "Q_kJh": Q_kJh_arr,
        "Q_kW": Q_kW_arr,
        "factible": fact_arr,
    })

    df_fact = df_malla[df_malla["factible"]].copy()
    if df_fact.empty:
        return df_malla, pd.DataFrame(), None

    df_fact["f1"] = 1.0 - df_fact["Xs"]
    df_fact["f2"] = df_fact["Q_kW"]

    df_ord = df_fact.sort_values(by=["f1", "f2"], ascending=[True, True]).reset_index(drop=True)
    indices_pareto = []
    min_f2 = np.inf
    for idx, fila in df_ord.iterrows():
        if fila["f2"] < min_f2:
            indices_pareto.append(idx)
            min_f2 = fila["f2"]

    df_pareto = df_ord.loc[indices_pareto].copy().reset_index(drop=True)

    if len(df_pareto) >= 2:
        f1_min, f1_max = df_pareto["f1"].min(), df_pareto["f1"].max()
        f2_min, f2_max = df_pareto["f2"].min(), df_pareto["f2"].max()

        rango_f1 = f1_max - f1_min if f1_max > f1_min else 1.0
        rango_f2 = f2_max - f2_min if f2_max > f2_min else 1.0

        df_pareto["f1_norm"] = (df_pareto["f1"] - f1_min) / rango_f1
        df_pareto["f2_norm"] = (df_pareto["f2"] - f2_min) / rango_f2

        x1, y1 = df_pareto["f1_norm"].iloc[0], df_pareto["f2_norm"].iloc[0]
        x2, y2 = df_pareto["f1_norm"].iloc[-1], df_pareto["f2_norm"].iloc[-1]

        num = np.abs((y2 - y1) * df_pareto["f1_norm"] - (x2 - x1) * df_pareto["f2_norm"] + x2 * y1 - y2 * x1)
        den = np.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        df_pareto["dist_knee"] = num / den if den > 0 else 0.0

        knee_point = df_pareto.loc[df_pareto["dist_knee"].idxmax()]
    else:
        df_pareto["f1_norm"] = 0.0
        df_pareto["f2_norm"] = 0.0
        df_pareto["dist_knee"] = 0.0
        knee_point = df_pareto.iloc[0]

    return df_malla, df_pareto, knee_point


def calcular_sensibilidad(T_ref, eps_ref, m_dot, S_in, Cp, Ea, k0, tau):
    """Evalúa perturbaciones de ±10% en los parámetros alrededor del punto de referencia."""
    base = evaluar_punto(T_ref, eps_ref, m_dot, S_in, Cp, Ea, k0, tau)

    parametros = [
        ("Flujo másico (ṁ)", "m_dot", m_dot, "kg/h"),
        ("Capacidad calorífica (Cp)", "Cp", Cp, "kJ/(kg·K)"),
        ("Energía de activación (Ea)", "Ea", Ea, "J/mol"),
        ("Factor preexponencial (k₀)", "k0", k0, "h⁻¹"),
        ("Tiempo espacial (τ)", "tau", tau, "h"),
        ("Azufre en alimentación", "S_in", S_in, "ppm"),
    ]

    filas = []
    for nombre, clave, val_base, unidad in parametros:
        args_menos = dict(m_dot=m_dot, S_in=S_in, Cp=Cp, Ea=Ea, k0=k0, tau=tau)
        args_mas = dict(m_dot=m_dot, S_in=S_in, Cp=Cp, Ea=Ea, k0=k0, tau=tau)
        args_menos[clave] = val_base * 0.90
        args_mas[clave] = val_base * 1.10

        r_menos = evaluar_punto(T_ref, eps_ref, **args_menos)
        r_mas = evaluar_punto(T_ref, eps_ref, **args_mas)

        filas.append({
            "Parámetro": nombre,
            "Valor base": val_base,
            "Unidad": unidad,
            "Carga (-10%) [kW]": r_menos["Q_kW"],
            "Carga (+10%) [kW]": r_mas["Q_kW"],
            "ΔQ (-10%) [kW]": r_menos["Q_kW"] - base["Q_kW"],
            "ΔQ (+10%) [kW]": r_mas["Q_kW"] - base["Q_kW"],
            "Azufre (-10%) [ppm]": r_menos["S_out"],
            "Azufre (+10%) [ppm]": r_mas["S_out"],
            "Factible (-10%)": "Sí" if r_menos["factible"] else "No",
            "Factible (+10%)": "Sí" if r_mas["factible"] else "No",
        })

    return base, pd.DataFrame(filas)


def aplicar_estilo_grafico(fig, titulo, titulo_x, titulo_y, altura=470):
    """Estilo editorial claro con márgenes generosos para evitar cualquier cruce de texto."""
    fig.update_layout(
        title=dict(
            text=titulo,
            font=dict(size=15, color="#6E2B4B"),
            x=0.0,
            xanchor="left",
            y=0.97,
        ),
        xaxis=dict(
            title=dict(text=titulo_x, standoff=12),
            showgrid=True,
            gridcolor="#F1E4EA",
            zerolinecolor="#DFC8D4",
            automargin=True,
        ),
        yaxis=dict(
            title=dict(text=titulo_y, standoff=10),
            showgrid=True,
            gridcolor="#F1E4EA",
            zerolinecolor="#DFC8D4",
            automargin=True,
        ),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(color="#2D1E26", size=12),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
            bgcolor="rgba(255,255,255,0.9)",
        ),
        margin=dict(l=55, r=25, t=55, b=105),
        height=altura,
    )
    return fig


# ==============================================================================
# BARRA LATERAL DE CONTROLES
# ==============================================================================
with st.sidebar:
    st.markdown("### Panel de Control")
    st.caption("Modifique las variables de decisión y los parámetros del modelo para explorar el comportamiento de la unidad.")

    st.markdown("#### Variables de decisión")
    T_in = st.slider(
        "Temperatura de entrada al reactor (K)",
        550.0, 650.0, step=1.0, key="T_in",
        help="Controla la constante cinética de Arrhenius y la conversión de azufre.",
    )
    eps = st.slider(
        "Efectividad del intercambiador (ε)",
        0.60, 0.90, step=0.01, key="eps",
        help="Fracción de calor recuperado del efluente del reactor hacia la alimentación.",
    )

    st.divider()
    st.markdown("#### Parámetros del proceso")
    m_dot = st.slider("Flujo másico de nafta (kg/h)", 90000.0, 110000.0, step=1000.0, key="m_dot")
    S_in = st.slider("Azufre en alimentación (ppm)", 450.0, 550.0, step=5.0, key="S_in")
    Cp = st.slider("Capacidad calorífica (kJ/kg·K)", 2.25, 2.75, step=0.05, key="Cp")
    Ea = st.slider("Energía de activación (J/mol)", 72000.0, 88000.0, step=500.0, key="Ea")
    k0_factor = st.slider("Ajuste de k₀ (base ±10%)", 0.90, 1.10, step=0.01, key="k0_factor")
    tau = st.slider("Tiempo espacial, τ (h)", 0.45, 0.55, step=0.01, key="tau")

    with st.expander("Resolución del Grid Search"):
        st.caption("Define cuántos puntos se evalúan para construir la frontera de Pareto.")
        n_T = st.slider("Nodos en temperatura", 41, 201, step=10, key="n_T")
        n_eps = st.slider("Nodos en efectividad", 21, 101, step=10, key="n_eps")

    st.divider()
    st.button("Restaurar condiciones base", on_click=restaurar_base, type="primary")
    st.caption("Realizado por: E. Nicole Palencia y Gabriela Ziegler")

k0_actual = K0_BASE * k0_factor

# ==============================================================================
# CÁLCULOS PRINCIPALES
# ==============================================================================
punto_actual = evaluar_punto(T_in, eps, m_dot, S_in, Cp, Ea, k0_actual, tau)
df_malla, df_pareto, knee = ejecutar_optimizacion(m_dot, S_in, Cp, Ea, k0_actual, tau, n_T, n_eps)

# ==============================================================================
# ENCABEZADO HERO
# ==============================================================================
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-tag">Optimización de Procesos · Escuela de Ingeniería Química · UCV</div>
        <div class="hero-title">Optimización Multiobjetivo de una Unidad de Hidrodesulfuración (HDS)</div>
        <div class="hero-subtitle">
            Estudio interactivo del compromiso entre maximizar la conversión de azufre y minimizar la demanda térmica del horno,
            respetando la especificación ambiental de producto (≤ 10 ppm de azufre).
        </div>
        <div class="hero-authors">Realizado por: E. Nicole Palencia y Gabriela Ziegler</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Aviso visible de cumplimiento de calidad
if punto_actual["factible"]:
    st.success(
        f"**Especificación de calidad cumplida:** El producto tratado alcanza **{punto_actual['S_out']:.3f} ppm de azufre** "
        f"(por debajo del límite de 10 ppm) operando a **{T_in:.1f} K** y efectividad **ε = {eps:.2f}**."
    )
else:
    st.error(
        f"**Producto fuera de especificación:** El azufre de salida es **{punto_actual['S_out']:.2f} ppm** "
        f"(supera el límite de 10 ppm) a **{T_in:.1f} K** y **ε = {eps:.2f}**. "
        "Aumente la temperatura de entrada al reactor para entrar en la región factible."
    )

# ==============================================================================
# TARJETAS DE INDICADORES (KPIs)
# ==============================================================================
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Conversión de azufre</div>
            <div class="kpi-value">{punto_actual['Xs'] * 100:.3f} %</div>
            <div class="kpi-sub">Constante cinética k = {punto_actual['k']:.2f} h⁻¹</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with k2:
    estado_txt = "Cumple (≤ 10 ppm)" if punto_actual["factible"] else "Excede límite (> 10 ppm)"
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Azufre en producto</div>
            <div class="kpi-value">{punto_actual['S_out']:.3f} ppm</div>
            <div class="kpi-sub">{estado_txt}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with k3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Carga térmica del horno</div>
            <div class="kpi-value">{punto_actual['Q_kW']:,.1f} kW</div>
            <div class="kpi-sub">{punto_actual['Q_kJh']:,.0f} kJ/h</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with k4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Precalentamiento E-101</div>
            <div class="kpi-value">{punto_actual['T_interc']:.1f} K</div>
            <div class="kpi-sub">Efluente R-101: {punto_actual['T_efluente']:.1f} K (+{punto_actual['dT_ad']:.2f} K)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==============================================================================
# DIAGRAMA DE FLUJO VIVO DEL PROCESO HDS
# ==============================================================================
st.markdown(
    f"""
    <div class="flow-wrapper">
        <div class="flow-title">Esquema operativo en tiempo real de la unidad HDS (condiciones actuales)</div>
        <div class="flow-grid">
            <div class="flow-node">
                <div class="flow-code">CORRIENTE 1</div>
                <div class="flow-name">Alimentación fresca</div>
                <div class="flow-data">T = {T_ALIM:.0f} K · {S_in:.0f} ppm S</div>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-node">
                <div class="flow-code">E-101 · ε = {eps:.2f}</div>
                <div class="flow-name">Intercambiador</div>
                <div class="flow-data">Sale a {punto_actual['T_interc']:.1f} K</div>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-node highlight">
                <div class="flow-code">H-101 · HORNO</div>
                <div class="flow-name">Calentamiento</div>
                <div class="flow-data">Q = {punto_actual['Q_kW']:,.1f} kW → {T_in:.1f} K</div>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-node highlight">
                <div class="flow-code">R-101 · τ = {tau:.2f} h</div>
                <div class="flow-name">Reactor HDS</div>
                <div class="flow-data">X = {punto_actual['Xs']*100:.2f}% · Sale a {punto_actual['T_efluente']:.1f} K</div>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-node">
                <div class="flow-code">V-101 / K-101</div>
                <div class="flow-name">Separador y reciclo</div>
                <div class="flow-data">Nafta tratada: {punto_actual['S_out']:.3f} ppm S</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# PESTAÑAS DE ANÁLISIS
# ==============================================================================
tab_pareto, tab_sens, tab_valid = st.tabs([
    "1. Frontera de Pareto y Punto de Rodilla",
    "2. Análisis de Sensibilidad (±10%)",
    "3. Validación y Modelo Matemático",
])

# ==================== TAB 1: PARETO ====================
with tab_pareto:
    st.markdown(
        """
        <div class="guide-box">
            <b>¿Qué estamos haciendo en esta sección?</b><br>
            Se evalúa una malla sistemática (<i>Grid Search</i>) sobre todo el dominio de operación
            (<b>550–650 K</b> y <b>ε entre 0.60–0.90</b>). Primero se separan las combinaciones que cumplen la especificación
            (<b>azufre ≤ 10 ppm</b>). Luego se eliminan las soluciones dominadas para obtener la <b>Frontera de Pareto</b>:
            el conjunto de puntos donde no es posible aumentar la conversión sin incrementar la carga térmica del horno.
            Finalmente, se normalizan ambos objetivos de minimización y se determina el <b>Punto de Rodilla (Knee Point)</b>
            como el punto de mayor distancia perpendicular a la recta que une los extremos de la frontera.
        </div>
        """,
        unsafe_allow_html=True,
    )

    frac_factible = df_malla["factible"].mean() * 100
    st.markdown(
        f"**Resumen de la malla:** {len(df_malla):,} puntos evaluados · "
        f"**{df_malla['factible'].sum():,} factibles ({frac_factible:.2f}%)** · "
        f"Rango azufre salida: **{df_malla['S_out'].min():.4f} – {df_malla['S_out'].max():.2f} ppm** · "
        f"Rango carga térmica: **{df_malla['Q_kW'].min():,.1f} – {df_malla['Q_kW'].max():,.1f} kW** "
        f"({df_malla['Q_kJh'].min():,.0f} – {df_malla['Q_kJh'].max():,.0f} kJ/h)"
    )

    if df_pareto.empty:
        st.warning("No existen puntos factibles (≤ 10 ppm) con los parámetros actuales del modelo.")
    else:
        col_g1, col_g2 = st.columns(2, gap="medium")

        df_no_fact = df_malla[~df_malla["factible"]]
        df_fact_bg = df_malla[df_malla["factible"]]
        df_no_fact_plot = df_no_fact.sample(1500, random_state=42) if len(df_no_fact) > 1500 else df_no_fact
        df_fact_plot = df_fact_bg.sample(1500, random_state=42) if len(df_fact_bg) > 1500 else df_fact_bg

        with col_g1:
            fig_obj = go.Figure()
            fig_obj.add_trace(go.Scatter(
                x=df_no_fact_plot["Q_kW"], y=df_no_fact_plot["Xs"] * 100,
                mode="markers", name="No factible",
                marker=dict(color=COLOR_NO_FACTIBLE, size=5),
                hovertemplate="Carga: %{x:.1f} kW<br>Conversión: %{y:.3f}%<extra>No factible</extra>",
            ))
            fig_obj.add_trace(go.Scatter(
                x=df_fact_plot["Q_kW"], y=df_fact_plot["Xs"] * 100,
                mode="markers", name="Factible",
                marker=dict(color=COLOR_FACTIBLE, size=5),
                hovertemplate="Carga: %{x:.1f} kW<br>Conversión: %{y:.3f}%<extra>Factible</extra>",
            ))
            fig_obj.add_trace(go.Scatter(
                x=df_pareto["Q_kW"], y=df_pareto["Xs"] * 100,
                mode="lines+markers", name="Pareto",
                line=dict(color=COLOR_PARETO, width=3),
                marker=dict(size=6, color=COLOR_PARETO),
                customdata=np.stack([df_pareto["T_in"], df_pareto["eps"], df_pareto["S_out"]], axis=-1),
                hovertemplate=(
                    "Carga: %{x:.1f} kW<br>Conversión: %{y:.4f}%<br>"
                    "Entrada: %{customdata[0]:.1f} K · ε: %{customdata[1]:.2f}<br>"
                    "Azufre: %{customdata[2]:.4f} ppm<extra>Pareto</extra>"
                ),
            ))
            fig_obj.add_trace(go.Scatter(
                x=[knee["Q_kW"]], y=[knee["Xs"] * 100],
                mode="markers", name="Punto de rodilla",
                marker=dict(color=COLOR_KNEE, size=15, symbol="star", line=dict(color="#3A1D2C", width=1.2)),
                hovertemplate=(
                    f"<b>Punto de rodilla</b><br>Entrada: {knee['T_in']:.1f} K · ε: {knee['eps']:.2f}<br>"
                    f"Carga: {knee['Q_kW']:.1f} kW<br>Conversión: {knee['Xs']*100:.4f}%<br>"
                    f"Azufre: {knee['S_out']:.3f} ppm<extra></extra>"
                ),
            ))
            fig_obj.add_trace(go.Scatter(
                x=[punto_actual["Q_kW"]], y=[punto_actual["Xs"] * 100],
                mode="markers", name="Actual",
                marker=dict(
                    color=COLOR_ACTUAL_OK if punto_actual["factible"] else COLOR_ACTUAL_ERR,
                    size=12, symbol="diamond", line=dict(color="#3A1D2C", width=1.2),
                ),
            ))
            aplicar_estilo_grafico(
                fig_obj,
                "Espacio de Objetivos (Conversión vs. Carga Térmica)",
                "Carga térmica del horno (kW)",
                "Conversión de azufre (%)",
            )
            st.plotly_chart(fig_obj)

        with col_g2:
            fig_dec = go.Figure()
            fig_dec.add_trace(go.Scatter(
                x=df_no_fact_plot["T_in"], y=df_no_fact_plot["eps"],
                mode="markers", name="No factible",
                marker=dict(color=COLOR_NO_FACTIBLE, size=6, symbol="square"),
            ))
            fig_dec.add_trace(go.Scatter(
                x=df_fact_plot["T_in"], y=df_fact_plot["eps"],
                mode="markers", name="Factible",
                marker=dict(color=COLOR_FACTIBLE, size=6, symbol="square"),
            ))
            fig_dec.add_trace(go.Scatter(
                x=df_pareto["T_in"], y=df_pareto["eps"],
                mode="lines+markers", name="Pareto",
                line=dict(color=COLOR_PARETO, width=3),
                marker=dict(size=6, color=COLOR_PARETO),
            ))
            fig_dec.add_trace(go.Scatter(
                x=[knee["T_in"]], y=[knee["eps"]],
                mode="markers", name="Punto de rodilla",
                marker=dict(color=COLOR_KNEE, size=15, symbol="star", line=dict(color="#3A1D2C", width=1.2)),
            ))
            fig_dec.add_trace(go.Scatter(
                x=[T_in], y=[eps],
                mode="markers", name="Actual",
                marker=dict(
                    color=COLOR_ACTUAL_OK if punto_actual["factible"] else COLOR_ACTUAL_ERR,
                    size=12, symbol="diamond", line=dict(color="#3A1D2C", width=1.2),
                ),
            ))
            aplicar_estilo_grafico(
                fig_dec,
                "Espacio de Decisión (Región Factible y Frontera)",
                "Temperatura de entrada al reactor (K)",
                "Efectividad del intercambiador (ε)",
            )
            st.plotly_chart(fig_dec)

        st.subheader("Puntos representativos de la frontera de Pareto")
        st.caption("Comparación directa entre los extremos de la curva óptima y el punto de rodilla recomendado.")

        extremo_min_Q = df_pareto.iloc[-1]
        extremo_max_Xs = df_pareto.iloc[0]

        df_rep = pd.DataFrame([
            {
                "Escenario": "Mínima carga térmica",
                "Temp. entrada (K)": extremo_min_Q["T_in"],
                "Efectividad (ε)": extremo_min_Q["eps"],
                "Conversión (%)": extremo_min_Q["Xs"] * 100,
                "Azufre salida (ppm)": extremo_min_Q["S_out"],
                "Carga horno (kW)": extremo_min_Q["Q_kW"],
                "Carga horno (kJ/h)": extremo_min_Q["Q_kJh"],
            },
            {
                "Escenario": "Punto de rodilla (mejor compromiso)",
                "Temp. entrada (K)": knee["T_in"],
                "Efectividad (ε)": knee["eps"],
                "Conversión (%)": knee["Xs"] * 100,
                "Azufre salida (ppm)": knee["S_out"],
                "Carga horno (kW)": knee["Q_kW"],
                "Carga horno (kJ/h)": knee["Q_kJh"],
            },
            {
                "Escenario": "Máxima conversión",
                "Temp. entrada (K)": extremo_max_Xs["T_in"],
                "Efectividad (ε)": extremo_max_Xs["eps"],
                "Conversión (%)": extremo_max_Xs["Xs"] * 100,
                "Azufre salida (ppm)": extremo_max_Xs["S_out"],
                "Carga horno (kW)": extremo_max_Xs["Q_kW"],
                "Carga horno (kJ/h)": extremo_max_Xs["Q_kJh"],
            },
        ])
        st.dataframe(
            df_rep,
            hide_index=True,
            column_config={
                "Temp. entrada (K)": st.column_config.NumberColumn(format="%.1f"),
                "Efectividad (ε)": st.column_config.NumberColumn(format="%.3f"),
                "Conversión (%)": st.column_config.NumberColumn(format="%.4f"),
                "Azufre salida (ppm)": st.column_config.NumberColumn(format="%.4f"),
                "Carga horno (kW)": st.column_config.NumberColumn(format="%.2f"),
                "Carga horno (kJ/h)": st.column_config.NumberColumn(format="%.0f"),
            },
        )

        col_exp, col_dl = st.columns([3, 1])
        with col_exp:
            with st.expander("Interpretación de ingeniería: resolución, efectividad y punto de rodilla"):
                st.markdown("""
                - **Resolución elegida (101 × 61 = 6,161 nodos):** Corresponde a pasos de **1.0 K** en temperatura y **0.005** en efectividad. Logra una curva suave con respuesta inmediata; su limitación es la discretización del borde exacto donde el azufre alcanza 10 ppm (alrededor de 597.4 K en el caso base).
                - **¿Por qué toda la frontera se ubica en ε = 0.90?** Porque una mayor efectividad recupera más calor del efluente y reduce la carga del horno sin afectar la cinética ni el azufre de salida. Así, ε = 0.90 domina a cualquier valor menor.
                - **Utilidad del punto de rodilla:** Más allá de 614 K, aumentar la temperatura exige mucha más energía en el horno para ganar apenas décimas porcentuales de conversión.
                """)
        with col_dl:
            df_export = df_pareto[["T_in", "eps", "Xs", "S_out", "Q_kW", "Q_kJh"]].rename(columns={
                "T_in": "Temperatura entrada (K)",
                "eps": "Efectividad",
                "Xs": "Conversion",
                "S_out": "Azufre salida (ppm)",
                "Q_kW": "Carga horno (kW)",
                "Q_kJh": "Carga horno (kJ/h)",
            })
            st.download_button(
                "Descargar frontera (CSV)",
                data=df_export.to_csv(index=False).encode("utf-8"),
                file_name="frontera-pareto-hds.csv",
                mime="text/csv",
            )

        with st.expander("Análisis opcional: impacto del precio de la energía en la decisión"):
            st.caption("Estimación ilustrativa del ahorro operativo al operar en el punto de rodilla en lugar del extremo de máxima conversión.")
            precio_kwh = st.slider("Precio referencial de energía térmica (USD/kWh)", 0.02, 0.25, 0.08, step=0.01)
            ahorro_h = (extremo_max_Xs["Q_kW"] - knee["Q_kW"]) * precio_kwh
            st.write(
                f"Elegir el **punto de rodilla** ({knee['T_in']:.1f} K) frente a la máxima conversión "
                f"({extremo_max_Xs['T_in']:.1f} K) ahorra **{ahorro_h:.2f} USD/h** "
                f"(~**{ahorro_h * 8000:,.0f} USD/año** en 8,000 h/año), manteniendo el producto en **{knee['S_out']:.2f} ppm**."
            )

# ==================== TAB 2: SENSIBILIDAD ====================
with tab_sens:
    st.markdown(
        """
        <div class="guide-box">
            <b>¿Qué estamos haciendo en esta sección?</b><br>
            Se aplica un análisis de sensibilidad local perturbando cada parámetro del modelo en <b>−10%</b> y <b>+10%</b>
            de forma individual, manteniendo el punto de operación fijo. Esto permite identificar qué incertidumbre
            (cinética, térmica o de alimentación) tiene mayor impacto sobre la <b>carga térmica del horno</b>
            y sobre el riesgo de incumplir la especificación de <b>10 ppm de azufre</b>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    opciones_ref = (
        ["Punto de rodilla (recomendado)", "Punto actual del panel lateral"]
        if knee is not None
        else ["Punto actual del panel lateral"]
    )
    ref_sel = st.radio("Punto de operación de referencia:", opciones_ref, horizontal=True)

    if ref_sel.startswith("Punto de rodilla") and knee is not None:
        T_ref, eps_ref = float(knee["T_in"]), float(knee["eps"])
    else:
        T_ref, eps_ref = T_in, eps

    base_sens, df_sens = calcular_sensibilidad(T_ref, eps_ref, m_dot, S_in, Cp, Ea, k0_actual, tau)
    st.caption(
        f"Evaluado en Entrada = {T_ref:.1f} K y ε = {eps_ref:.2f} · "
        f"Base: Carga = {base_sens['Q_kW']:,.2f} kW · Azufre salida = {base_sens['S_out']:.4f} ppm"
    )

    col_s1, col_s2 = st.columns(2, gap="medium")
    with col_s1:
        fig_sq = go.Figure()
        fig_sq.add_trace(go.Bar(
            y=df_sens["Parámetro"], x=df_sens["ΔQ (-10%) [kW]"],
            name="Perturbación -10%", orientation="h", marker_color=COLOR_BAR_MENOS,
        ))
        fig_sq.add_trace(go.Bar(
            y=df_sens["Parámetro"], x=df_sens["ΔQ (+10%) [kW]"],
            name="Perturbación +10%", orientation="h", marker_color=COLOR_BAR_MAS,
        ))
        aplicar_estilo_grafico(
            fig_sq,
            "Efecto en la carga térmica (ΔQ)",
            "Variación respecto a la base (kW)",
            "",
            altura=410,
        )
        fig_sq.update_layout(barmode="group")
        st.plotly_chart(fig_sq)

    with col_s2:
        fig_ss = go.Figure()
        fig_ss.add_trace(go.Bar(
            y=df_sens["Parámetro"], x=df_sens["Azufre (-10%) [ppm]"],
            name="Perturbación -10%", orientation="h", marker_color=COLOR_ACTUAL_OK,
        ))
        fig_ss.add_trace(go.Bar(
            y=df_sens["Parámetro"], x=df_sens["Azufre (+10%) [ppm]"],
            name="Perturbación +10%", orientation="h", marker_color=COLOR_ACTUAL_ERR,
        ))
        fig_ss.add_vline(x=S_SPEC, line_dash="dash", line_color="#6E2B4B", annotation_text="Límite 10 ppm")
        aplicar_estilo_grafico(
            fig_ss,
            "Efecto en el azufre de salida",
            "Azufre de salida (ppm)",
            "",
            altura=410,
        )
        fig_ss.update_layout(barmode="group")
        st.plotly_chart(fig_ss)

    st.dataframe(
        df_sens,
        hide_index=True,
        column_config={
            "Valor base": st.column_config.NumberColumn(format="%.4g"),
            "Carga (-10%) [kW]": st.column_config.NumberColumn(format="%.2f"),
            "Carga (+10%) [kW]": st.column_config.NumberColumn(format="%.2f"),
            "ΔQ (-10%) [kW]": st.column_config.NumberColumn(format="%+.2f"),
            "ΔQ (+10%) [kW]": st.column_config.NumberColumn(format="%+.2f"),
            "Azufre (-10%) [ppm]": st.column_config.NumberColumn(format="%.4f"),
            "Azufre (+10%) [ppm]": st.column_config.NumberColumn(format="%.4f"),
        },
    )

    st.subheader("Exploración del azufre en la alimentación (450 – 550 ppm)")
    st.caption("Muestra la relación lineal entre el contenido de azufre de entrada y el producto a conversión fija.")
    s_in_grid = np.linspace(450.0, 550.0, 21)
    s_out_grid = s_in_grid * (1.0 - base_sens["Xs"])
    fig_sin = go.Figure()
    fig_sin.add_trace(go.Scatter(
        x=s_in_grid, y=s_out_grid, mode="lines+markers",
        name="Azufre de salida", line=dict(color=COLOR_PARETO, width=2.5),
    ))
    fig_sin.add_hline(y=S_SPEC, line_dash="dash", line_color=COLOR_ACTUAL_ERR, annotation_text="Límite 10 ppm")
    aplicar_estilo_grafico(
        fig_sin,
        "Respuesta del producto ante variaciones de azufre en alimentación",
        "Azufre en la alimentación (ppm)",
        "Azufre de salida (ppm)",
        altura=340,
    )
    st.plotly_chart(fig_sin)

# ==================== TAB 3: VALIDACIÓN Y MODELO ====================
with tab_valid:
    st.markdown(
        """
        <div class="guide-box">
            <b>¿Qué estamos haciendo en esta sección?</b><br>
            Se verifican los tres casos de control (<i>Sanity Checks</i>) solicitados para comprobar que el modelo
            cinético y el balance de energía responden de manera físicamente consistente en condiciones extremas
            (alta temperatura, baja temperatura y límite ideal de efectividad <b>ε → 1</b>).
        </div>
        """,
        unsafe_allow_html=True,
    )

    sc1 = evaluar_punto(650.0, 0.90, 100000.0, 500.0, 2.5, 80000.0, K0_BASE, 0.5)
    sc2 = evaluar_punto(550.0, 0.75, 100000.0, 500.0, 2.5, 80000.0, K0_BASE, 0.5)
    sc3 = evaluar_punto(600.0, 1.00, 100000.0, 500.0, 2.5, 80000.0, K0_BASE, 0.5)

    df_sc = pd.DataFrame([
        {
            "Caso de prueba": "1) Alta temperatura: 650 K, ε = 0.90",
            "Conversión": sc1["Xs"],
            "Azufre salida (ppm)": sc1["S_out"],
            "Factible": "Sí" if sc1["factible"] else "No",
            "Temp. efluente (K)": sc1["T_efluente"],
            "Temp. intercambiador (K)": sc1["T_interc"],
            "Carga horno (kJ/h)": sc1["Q_kJh"],
            "Carga horno (kW)": sc1["Q_kW"],
        },
        {
            "Caso de prueba": "2) Baja temperatura: 550 K, ε = 0.75",
            "Conversión": sc2["Xs"],
            "Azufre salida (ppm)": sc2["S_out"],
            "Factible": "Sí" if sc2["factible"] else "No",
            "Temp. efluente (K)": sc2["T_efluente"],
            "Temp. intercambiador (K)": sc2["T_interc"],
            "Carga horno (kJ/h)": sc2["Q_kJh"],
            "Carga horno (kW)": sc2["Q_kW"],
        },
        {
            "Caso de prueba": "3) Límite ideal: ε → 1 (a 600 K)",
            "Conversión": sc3["Xs"],
            "Azufre salida (ppm)": sc3["S_out"],
            "Factible": "Sí" if sc3["factible"] else "No",
            "Temp. efluente (K)": sc3["T_efluente"],
            "Temp. intercambiador (K)": sc3["T_interc"],
            "Carga horno (kJ/h)": sc3["Q_kJh"],
            "Carga horno (kW)": sc3["Q_kW"],
        },
    ])
    st.dataframe(
        df_sc,
        hide_index=True,
        column_config={
            "Conversión": st.column_config.NumberColumn(format="%.6f"),
            "Azufre salida (ppm)": st.column_config.NumberColumn(format="%.4f"),
            "Temp. efluente (K)": st.column_config.NumberColumn(format="%.2f"),
            "Temp. intercambiador (K)": st.column_config.NumberColumn(format="%.2f"),
            "Carga horno (kJ/h)": st.column_config.NumberColumn(format="%.1f"),
            "Carga horno (kW)": st.column_config.NumberColumn(format="%.2f"),
        },
    )

    st.info(
        "**Interpretación del caso límite (ε → 1):** Cuando la efectividad tiende a la unidad, "
        "la temperatura de salida del intercambiador iguala a la del efluente del reactor. "
        "Como la reacción es exotérmica (el efluente sale 15·X K más caliente que la entrada), "
        "la carga térmica del horno resulta negativa (−1,026.04 kW a 600 K), lo que representa un excedente "
        "de calor recuperado: en ese escenario ideal, el horno no necesitaría suministrar energía."
    )

    with st.container(border=True):
        st.subheader("Ecuaciones implementadas en el modelo")
        st.latex(r"k(T) = k_0 \exp\left(-\frac{E_a}{RT}\right), \quad X_S(T_{\text{in}}) = 1 - \exp\left[-k(T_{\text{in}})\tau\right], \quad S_{\text{out}} = S_{\text{in}}(1 - X_S)")
        st.latex(r"\Delta T_{\text{ad}} = 15\,X_S, \quad T_{\text{efluente}} = T_{\text{in}} + \Delta T_{\text{ad}}, \quad T_{\text{intercambiador}} = T_{\text{alimentación}} + \varepsilon(T_{\text{efluente}} - T_{\text{alimentación}})")
        st.latex(r"Q_{\text{horno}} = \dot{m}\,C_p\,(T_{\text{in}} - T_{\text{intercambiador}}) \quad [\text{kJ/h}], \qquad Q_{\text{horno, kW}} = \frac{Q_{\text{horno}}}{3600}")
        st.caption(f"Factor preexponencial calibrado para una conversión de 0.985 a 600 K: k₀ = {K0_BASE:.6e} h⁻¹")

# ==============================================================================
# PIE DE PÁGINA
# ==============================================================================
st.markdown(
    """
    <div class="footer-note">
        Proyecto Final · Curso de Optimización de Procesos · Escuela de Ingeniería Química (UCV)<br>
        <b>Realizado por: E. Nicole Palencia y Gabriela Ziegler</b>
    </div>
    """,
    unsafe_allow_html=True,
)
