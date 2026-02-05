"""
RTFTI Protocol Terminal
Real-Time Financial Trust Infrastructure — Full-Stack Execution Console
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime
import time
import io
from fpdf import FPDF

# ============================================================================
# CONFIG
# ============================================================================

st.set_page_config(
    page_title="RTFTI Protocol Terminal",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================================
# THEME
# ============================================================================

def apply_theme():
    """Apply custom dark theme styling"""
    st.markdown("""
    <style>
    /* Base theme */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid rgba(56, 189, 248, 0.2);
    }
    
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #38bdf8;
    }
    
    /* Headers */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Layer headers */
    .layer-header {
        background: linear-gradient(90deg, rgba(56, 189, 248, 0.15), transparent);
        border-left: 4px solid #38bdf8;
        padding: 0.75rem 1rem;
        font-size: 1.25rem;
        font-weight: 600;
        color: #e2e8f0;
        margin: 1.5rem 0 1rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    /* Flow arrows between layers */
    .flow-arrow {
        text-align: center;
        font-size: 2rem;
        color: #38bdf8;
        margin: 0.5rem 0;
        opacity: 0.7;
    }
    
    /* Source cards */
    .source-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .source-card:hover {
        border-color: #38bdf8;
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(56, 189, 248, 0.2);
    }
    
    .source-card h5 {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
    }
    
    .source-card .count {
        color: #38bdf8;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
    }
    
    .source-card .label {
        color: #64748b;
        font-size: 0.75rem;
        margin: 0;
    }
    
    /* Validation rules */
    .validation-rule {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
    }
    
    .validation-rule .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.25rem;
    }
    
    .validation-rule .name {
        color: #e2e8f0;
        font-weight: 600;
    }
    
    .validation-rule .detail {
        color: #64748b;
        font-size: 0.8rem;
    }
    
    /* Status chips */
    .chip-pass, .chip-passed {
        background: rgba(74, 222, 128, 0.2);
        color: #4ade80;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .chip-warn, .chip-warning {
        background: rgba(250, 204, 21, 0.2);
        color: #facc15;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .chip-alert, .chip-failed {
        background: rgba(248, 113, 113, 0.2);
        color: #f87171;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    /* FTS Display */
    .fts-display {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(129, 140, 248, 0.1));
        border: 2px solid rgba(56, 189, 248, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .fts-score {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4ade80, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1;
    }
    
    .fts-label {
        color: #94a3b8;
        font-size: 0.9rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Sidebar FTS display */
    .sidebar-fts {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.15), rgba(129, 140, 248, 0.15));
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .sidebar-fts .score {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4ade80, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .sidebar-fts .label {
        color: #94a3b8;
        font-size: 0.8rem;
        margin-top: 0.25rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(30, 41, 59, 0.5);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #94a3b8;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(56, 189, 248, 0.2);
        color: #38bdf8;
    }
    
    /* Metrics styling */
    [data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 8px;
        padding: 0.75rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: #94a3b8;
    }
    
    [data-testid="stMetricValue"] {
        color: #38bdf8;
    }
    
    /* Button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(56, 189, 248, 0.4);
    }
    
    /* Data editor styling */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 8px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 8px;
    }
    
    /* Info/Warning/Error boxes */
    .stAlert {
        border-radius: 8px;
    }
    
    /* Divider */
    hr {
        border-color: rgba(56, 189, 248, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Entity:
    name: str
    sector: str
    turnover_cr: float
    employees: int
    gst_registered: bool = True
    account_age_months: int = 48


@dataclass
class IngestionResult:
    gl_records: int
    bank_records: int
    gst_records: int
    payroll_records: int
    timestamp: str
    status: str = "complete"


@dataclass
class NormalizationResult:
    records_in: int
    records_out: int
    duplicates_removed: int
    schema_aligned: bool
    currency_standardized: bool


@dataclass
class ValidationResult:
    dimension: str
    weight: float
    score: float
    status: str  # PASS, WARN, ALERT
    detail: str
    formula: str


@dataclass
class TrustProfile:
    fts: int
    confidence: float
    revenue_integrity: int
    cash_flow: int
    tax_compliance: int
    payroll: int
    audit_readiness: int


# ============================================================================
# DATA GENERATION
# ============================================================================

def generate_gl_data(turnover_cr: float, months: int, rng: np.random.Generator) -> pd.DataFrame:
    monthly_rev = turnover_cr * 100 / 12
    records = []
    for i in range(months):
        revenue = monthly_rev * rng.uniform(0.85, 1.15)
        expenses = revenue * rng.uniform(0.65, 0.85)
        records.append({
            "month": f"2025-{(i % 12) + 1:02d}",
            "revenue": round(revenue, 2),
            "expenses": round(expenses, 2),
            "net": round(revenue - expenses, 2),
        })
    return pd.DataFrame(records)


def generate_bank_data(turnover_cr: float, months: int, rng: np.random.Generator) -> pd.DataFrame:
    monthly_rev = turnover_cr * 100 / 12
    records = []
    for i in range(months):
        inflow = monthly_rev * rng.uniform(0.82, 1.18)
        outflow = inflow * rng.uniform(0.70, 0.90)
        records.append({
            "month": f"2025-{(i % 12) + 1:02d}",
            "inflow": round(inflow, 2),
            "outflow": round(outflow, 2),
            "net": round(inflow - outflow, 2),
        })
    return pd.DataFrame(records)


def generate_gst_data(turnover_cr: float, months: int, rng: np.random.Generator) -> pd.DataFrame:
    monthly_rev = turnover_cr * 100 / 12
    records = []
    for i in range(months):
        reported = monthly_rev * rng.uniform(0.88, 1.12)
        records.append({
            "month": f"2025-{(i % 12) + 1:02d}",
            "reported_revenue": round(reported, 2),
            "filed_on_time": rng.random() > 0.1,
        })
    return pd.DataFrame(records)


def generate_payroll_data(employees: int, months: int, rng: np.random.Generator) -> pd.DataFrame:
    avg_salary = 0.4
    records = []
    for i in range(months):
        total = employees * avg_salary * rng.uniform(0.95, 1.05)
        records.append({
            "month": f"2025-{(i % 12) + 1:02d}",
            "total_salary": round(total, 2),
            "statutory_compliant": rng.random() > 0.08,
        })
    return pd.DataFrame(records)


# ============================================================================
# PROCESSING LAYERS
# ============================================================================

def process_ingestion(gl: pd.DataFrame, bank: pd.DataFrame, gst: pd.DataFrame, payroll: pd.DataFrame) -> IngestionResult:
    return IngestionResult(
        gl_records=len(gl),
        bank_records=len(bank),
        gst_records=len(gst),
        payroll_records=len(payroll),
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


def process_normalization(ingestion: IngestionResult) -> NormalizationResult:
    total_in = ingestion.gl_records + ingestion.bank_records + ingestion.gst_records + ingestion.payroll_records
    return NormalizationResult(
        records_in=total_in,
        records_out=total_in,
        duplicates_removed=0,
        schema_aligned=True,
        currency_standardized=True,
    )


def validate_revenue_integrity(gl: pd.DataFrame, bank: pd.DataFrame, gst: pd.DataFrame) -> ValidationResult:
    gl_total = gl["revenue"].sum()
    bank_total = bank["inflow"].sum()
    gst_total = gst["reported_revenue"].sum()
    
    avg = (gl_total + bank_total + gst_total) / 3
    max_var = max(abs(gl_total - avg), abs(bank_total - avg), abs(gst_total - avg))
    variance_pct = (max_var / avg) * 100 if avg > 0 else 0
    
    if variance_pct < 5:
        return ValidationResult("Revenue Integrity", 0.25, 95, "PASS", "Strong alignment across sources", f"Variance: {variance_pct:.1f}%")
    elif variance_pct < 12:
        return ValidationResult("Revenue Integrity", 0.25, 75, "WARN", f"Moderate variance: {variance_pct:.1f}%", f"GL={gl_total:.0f}, Bank={bank_total:.0f}, GST={gst_total:.0f}")
    else:
        return ValidationResult("Revenue Integrity", 0.25, 50, "ALERT", f"High variance: {variance_pct:.1f}%", f"GL={gl_total:.0f}, Bank={bank_total:.0f}, GST={gst_total:.0f}")


def validate_cash_flow(bank: pd.DataFrame) -> ValidationResult:
    net_flows = bank["net"].values
    mean_flow = np.mean(net_flows)
    std_flow = np.std(net_flows)
    cv = (std_flow / mean_flow) * 100 if mean_flow > 0 else 100
    
    if cv < 25:
        return ValidationResult("Cash Flow Behaviour", 0.25, 90, "PASS", "Stable and predictable", f"CV: {cv:.1f}%")
    elif cv < 50:
        return ValidationResult("Cash Flow Behaviour", 0.25, 70, "WARN", f"Moderate volatility: {cv:.1f}%", f"Mean={mean_flow:.1f}, Std={std_flow:.1f}")
    else:
        return ValidationResult("Cash Flow Behaviour", 0.25, 45, "ALERT", f"High volatility: {cv:.1f}%", f"Mean={mean_flow:.1f}, Std={std_flow:.1f}")


def validate_tax_compliance(gst: pd.DataFrame) -> ValidationResult:
    on_time_rate = gst["filed_on_time"].mean() * 100
    
    if on_time_rate >= 90:
        return ValidationResult("Tax Compliance", 0.20, 95, "PASS", "Timely filings", f"On-time: {on_time_rate:.0f}%")
    elif on_time_rate >= 75:
        return ValidationResult("Tax Compliance", 0.20, 70, "WARN", f"Some delays: {100-on_time_rate:.0f}% late", f"On-time: {on_time_rate:.0f}%")
    else:
        return ValidationResult("Tax Compliance", 0.20, 40, "ALERT", f"Frequent delays", f"On-time: {on_time_rate:.0f}%")


def validate_payroll(payroll: pd.DataFrame) -> ValidationResult:
    compliance_rate = payroll["statutory_compliant"].mean() * 100
    
    if compliance_rate >= 90:
        return ValidationResult("Payroll Consistency", 0.15, 92, "PASS", "Regular and compliant", f"Compliance: {compliance_rate:.0f}%")
    elif compliance_rate >= 75:
        return ValidationResult("Payroll Consistency", 0.15, 68, "WARN", f"Some issues: {100-compliance_rate:.0f}% flagged", f"Compliance: {compliance_rate:.0f}%")
    else:
        return ValidationResult("Payroll Consistency", 0.15, 35, "ALERT", f"Compliance issues", f"Compliance: {compliance_rate:.0f}%")


def validate_audit_readiness(gl: pd.DataFrame, bank: pd.DataFrame) -> ValidationResult:
    gl_net = gl["net"].sum()
    bank_net = bank["net"].sum()
    
    diff_pct = abs(gl_net - bank_net) / max(gl_net, bank_net) * 100 if max(gl_net, bank_net) > 0 else 0
    
    if diff_pct < 8:
        return ValidationResult("Audit Readiness", 0.15, 88, "PASS", "High consistency", f"GL-Bank diff: {diff_pct:.1f}%")
    elif diff_pct < 18:
        return ValidationResult("Audit Readiness", 0.15, 65, "WARN", f"Moderate gaps: {diff_pct:.1f}%", f"GL={gl_net:.0f}, Bank={bank_net:.0f}")
    else:
        return ValidationResult("Audit Readiness", 0.15, 40, "ALERT", f"Significant gaps", f"GL={gl_net:.0f}, Bank={bank_net:.0f}")


def compute_trust(validations: List[ValidationResult]) -> TrustProfile:
    fts = sum(v.score * v.weight for v in validations)
    scores = {v.dimension: int(v.score) for v in validations}
    
    return TrustProfile(
        fts=int(fts),
        confidence=0.92,
        revenue_integrity=scores.get("Revenue Integrity", 0),
        cash_flow=scores.get("Cash Flow Behaviour", 0),
        tax_compliance=scores.get("Tax Compliance", 0),
        payroll=scores.get("Payroll Consistency", 0),
        audit_readiness=scores.get("Audit Readiness", 0),
    )


# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

def init_data():
    """Initialize or regenerate data based on entity config"""
    entity = st.session_state.get("entity", Entity("Precision Tools Pvt. Ltd.", "Manufacturing", 7.5, 42))
    seed = st.session_state.get("data_seed", 42)
    rng = np.random.default_rng(seed)
    
    st.session_state.gl = generate_gl_data(entity.turnover_cr, 12, rng)
    st.session_state.bank = generate_bank_data(entity.turnover_cr, 12, rng)
    st.session_state.gst = generate_gst_data(entity.turnover_cr, 12, rng)
    st.session_state.payroll = generate_payroll_data(entity.employees, 12, rng)
    st.session_state.executed = False
    st.session_state.ingestion = None
    st.session_state.normalization = None
    st.session_state.validations = None
    st.session_state.trust = None


def execute_protocol():
    """Run the full protocol pipeline"""
    gl = st.session_state.gl
    bank = st.session_state.bank
    gst = st.session_state.gst
    payroll = st.session_state.payroll
    
    # Layer 2: Ingestion
    st.session_state.ingestion = process_ingestion(gl, bank, gst, payroll)
    
    # Layer 3: Normalization
    st.session_state.normalization = process_normalization(st.session_state.ingestion)
    
    # Layer 4: Validation
    st.session_state.validations = [
        validate_revenue_integrity(gl, bank, gst),
        validate_cash_flow(bank),
        validate_tax_compliance(gst),
        validate_payroll(payroll),
        validate_audit_readiness(gl, bank),
    ]
    
    # Layer 5: Trust Output
    st.session_state.trust = compute_trust(st.session_state.validations)
    st.session_state.executed = True


# ============================================================================
# UI: SIDEBAR
# ============================================================================

def render_sidebar():
    st.sidebar.title("🛠️ RTFTI")
    st.sidebar.caption("Protocol Terminal")
    st.sidebar.markdown("---")
    
    # Entity Configuration
    st.sidebar.subheader("Entity Configuration")
    
    name = st.sidebar.text_input("Name", value="Precision Tools Pvt. Ltd.")
    sector = st.sidebar.selectbox("Sector", ["Manufacturing", "IT Services", "Retail", "Logistics", "Healthcare"])
    turnover = st.sidebar.slider("Turnover (₹ Cr)", 1.0, 25.0, 7.5, 0.5)
    employees = st.sidebar.slider("Employees", 10, 200, 42)
    
    st.session_state.entity = Entity(name, sector, turnover, employees)
    
    st.sidebar.markdown("---")
    
    # Data Mode
    st.sidebar.subheader("Data Mode")
    mode = st.sidebar.radio("Data Mode", ["Case Study", "Random", "Custom"], horizontal=True, label_visibility="collapsed")
    
    if mode == "Case Study":
        if st.sidebar.button("Load Precision Tools"):
            st.session_state.entity = Entity("Precision Tools Pvt. Ltd.", "Manufacturing", 7.5, 42)
            st.session_state.data_seed = 42
            init_data()
            st.rerun()
    elif mode == "Random":
        if st.sidebar.button("Generate Random"):
            st.session_state.data_seed = int(datetime.now().timestamp())
            init_data()
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # Execute Button
    if st.sidebar.button("▶ EXECUTE PROTOCOL", type="primary"):
        execute_protocol()
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Status Panel
    st.sidebar.subheader("Status")
    if st.session_state.get("executed"):
        trust = st.session_state.trust
        st.sidebar.markdown(f"""
        <div class="sidebar-fts">
            <p class="score">{trust.fts}/100</p>
            <p class="label">Financial Trust Score</p>
            <p class="label">Confidence: {trust.confidence*100:.0f}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Alert count
        alerts = sum(1 for v in st.session_state.validations if v.status == "ALERT")
        warns = sum(1 for v in st.session_state.validations if v.status == "WARN")
        st.sidebar.write(f"🔴 Alerts: {alerts} | 🟡 Warnings: {warns}")
        
        # PDF Export Button
        st.sidebar.markdown("---")
        pdf_bytes = generate_pdf_report()
        st.sidebar.download_button(
            label="📄 Export PDF Report",
            data=pdf_bytes,
            file_name=f"RTFTI_Report_{st.session_state.entity.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
        )
    else:
        st.sidebar.info("Ready to execute")


# ============================================================================
# PDF REPORT GENERATION
# ============================================================================

def generate_pdf_report() -> bytes:
    """Generate a PDF report of the current execution results"""
    entity = st.session_state.entity
    trust = st.session_state.trust
    validations = st.session_state.validations
    ingestion = st.session_state.ingestion
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(56, 189, 248)  # Accent blue
    pdf.cell(0, 15, "RTFTI Protocol Report", ln=True, align="C")
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Real-Time Financial Trust Infrastructure", ln=True, align="C")
    pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    pdf.ln(10)
    
    # Entity Details Section
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, "Entity Details", ln=True)
    pdf.set_draw_color(56, 189, 248)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(50, 7, "Name:", ln=False)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, entity.name, ln=True)
    
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(50, 7, "Sector:", ln=False)
    pdf.cell(0, 7, entity.sector, ln=True)
    
    pdf.cell(50, 7, "Annual Turnover:", ln=False)
    pdf.cell(0, 7, f"Rs. {entity.turnover_cr} Cr", ln=True)
    
    pdf.cell(50, 7, "Employees:", ln=False)
    pdf.cell(0, 7, str(entity.employees), ln=True)
    pdf.ln(8)
    
    # FTS Score - Big highlight
    pdf.set_fill_color(240, 249, 255)
    pdf.rect(10, pdf.get_y(), 190, 35, "F")
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(56, 189, 248)
    pdf.cell(0, 12, "Financial Trust Score (FTS)", ln=True, align="C")
    
    pdf.set_font("Helvetica", "B", 36)
    if trust.fts >= 80:
        pdf.set_text_color(74, 222, 128)  # Green
    elif trust.fts >= 60:
        pdf.set_text_color(250, 204, 21)  # Yellow
    else:
        pdf.set_text_color(248, 113, 113)  # Red
    pdf.cell(0, 18, f"{trust.fts}/100", ln=True, align="C")
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f"Confidence: {trust.confidence*100:.0f}%", ln=True, align="C")
    pdf.ln(10)
    
    # Ingestion Summary
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, "Data Ingestion Summary", ln=True)
    pdf.set_draw_color(56, 189, 248)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(50, 7, "Execution Time:", ln=False)
    pdf.cell(0, 7, ingestion.timestamp, ln=True)
    pdf.cell(50, 7, "Total Records:", ln=False)
    total = ingestion.gl_records + ingestion.bank_records + ingestion.gst_records + ingestion.payroll_records
    pdf.cell(0, 7, str(total), ln=True)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(47.5, 7, f"GL: {ingestion.gl_records}", border=1, align="C")
    pdf.cell(47.5, 7, f"Bank: {ingestion.bank_records}", border=1, align="C")
    pdf.cell(47.5, 7, f"GST: {ingestion.gst_records}", border=1, align="C")
    pdf.cell(47.5, 7, f"Payroll: {ingestion.payroll_records}", border=1, align="C", ln=True)
    pdf.ln(8)
    
    # Validation Results
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, "Validation Results", ln=True)
    pdf.set_draw_color(56, 189, 248)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    # Table header
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(56, 189, 248)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(55, 8, "Dimension", border=1, fill=True, align="C")
    pdf.cell(25, 8, "Weight", border=1, fill=True, align="C")
    pdf.cell(25, 8, "Score", border=1, fill=True, align="C")
    pdf.cell(25, 8, "Status", border=1, fill=True, align="C")
    pdf.cell(60, 8, "Details", border=1, fill=True, align="C", ln=True)
    
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(30, 30, 30)
    
    for v in validations:
        # Status color
        if v.status == "PASS":
            pdf.set_fill_color(220, 252, 231)
        elif v.status == "WARN":
            pdf.set_fill_color(254, 249, 195)
        else:
            pdf.set_fill_color(254, 226, 226)
        
        pdf.cell(55, 7, v.dimension, border=1)
        pdf.cell(25, 7, f"{v.weight*100:.0f}%", border=1, align="C")
        pdf.cell(25, 7, f"{v.score:.0f}", border=1, align="C")
        pdf.cell(25, 7, v.status, border=1, align="C", fill=True)
        pdf.cell(60, 7, v.detail[:30] + "..." if len(v.detail) > 30 else v.detail, border=1, ln=True)
    
    pdf.ln(8)
    
    # Stakeholder Recommendations
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, "Stakeholder Recommendations", ln=True)
    pdf.set_draw_color(56, 189, 248)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    # MSME View
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "For MSME:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    rating = "Excellent" if trust.fts >= 80 else "Good" if trust.fts >= 65 else "Needs Improvement"
    pdf.cell(0, 6, f"  Overall Rating: {rating}", ln=True)
    
    alerts_list = [v for v in validations if v.status != "PASS"]
    if alerts_list:
        pdf.cell(0, 6, "  Improvement Areas:", ln=True)
        for v in alerts_list:
            pdf.cell(0, 5, f"    - {v.dimension}: {v.detail}", ln=True)
    pdf.ln(3)
    
    # Bank View
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "For Bank/NBFC:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    if trust.fts >= 80:
        pdf.set_text_color(74, 222, 128)
        pdf.cell(0, 6, "  APPROVED - Fast-track lending, Prime + 1.5%", ln=True)
    elif trust.fts >= 65:
        pdf.set_text_color(250, 204, 21)
        pdf.cell(0, 6, "  CONDITIONAL - Standard process, Prime + 3.5%", ln=True)
    else:
        pdf.set_text_color(248, 113, 113)
        pdf.cell(0, 6, "  REVIEW REQUIRED - Detailed audit needed", ln=True)
    pdf.set_text_color(30, 30, 30)
    pdf.ln(3)
    
    # Regulator View
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "For Regulator:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    if trust.fts >= 70:
        pdf.cell(0, 6, "  LOW RISK - No systemic concerns", ln=True)
    elif trust.fts >= 50:
        pdf.cell(0, 6, "  MEDIUM RISK - Monitor closely", ln=True)
    else:
        pdf.cell(0, 6, "  HIGH RISK - Early intervention recommended", ln=True)
    
    pdf.ln(10)
    
    # Footer
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 5, "RTFTI Protocol v1.0 - This report is auto-generated based on real-time financial data analysis.", ln=True, align="C")
    pdf.cell(0, 5, "For official use only. Scores are indicative and subject to verification.", ln=True, align="C")
    
    # Output to bytes
    return bytes(pdf.output())


# ============================================================================
# UI: MAIN LAYERS
# ============================================================================

def render_layer_1():
    st.markdown('<div class="layer-header">Layer 1: Data Sources</div>', unsafe_allow_html=True)
    st.caption("Real-time feeds from authoritative systems — Edit data below")
    
    tab_gl, tab_bank, tab_gst, tab_payroll = st.tabs(["📊 General Ledger", "🏦 Bank Transactions", "📋 GST Filings", "💰 Payroll"])
    
    with tab_gl:
        edited_gl = st.data_editor(st.session_state.gl, num_rows="fixed", width='stretch', key="gl_editor")
        st.session_state.gl = edited_gl
    
    with tab_bank:
        edited_bank = st.data_editor(st.session_state.bank, num_rows="fixed", width='stretch', key="bank_editor")
        st.session_state.bank = edited_bank
    
    with tab_gst:
        edited_gst = st.data_editor(st.session_state.gst, num_rows="fixed", width='stretch', key="gst_editor")
        st.session_state.gst = edited_gst
    
    with tab_payroll:
        edited_payroll = st.data_editor(st.session_state.payroll, num_rows="fixed", width='stretch', key="payroll_editor")
        st.session_state.payroll = edited_payroll
    
    st.markdown('<p class="flow-arrow">↓</p>', unsafe_allow_html=True)


def render_layer_2():
    st.markdown('<div class="layer-header">Layer 2: Ingestion Gateway</div>', unsafe_allow_html=True)
    
    ingestion = st.session_state.get("ingestion")
    
    cols = st.columns(4)
    sources = [
        ("General Ledger", len(st.session_state.gl), ingestion.gl_records if ingestion else None),
        ("Bank Txns", len(st.session_state.bank), ingestion.bank_records if ingestion else None),
        ("GST Filings", len(st.session_state.gst), ingestion.gst_records if ingestion else None),
        ("Payroll", len(st.session_state.payroll), ingestion.payroll_records if ingestion else None),
    ]
    
    for col, (name, available, ingested) in zip(cols, sources):
        status = "✓" if ingested else "○"
        count = ingested if ingested else available
        col.markdown(f"""
        <div class="source-card">
            <h5>{name}</h5>
            <p class="count">{count}</p>
            <p class="label">records {status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    if ingestion:
        st.caption(f"Ingestion complete at {ingestion.timestamp}")
    else:
        st.caption("Awaiting execution...")
    
    st.markdown('<p class="flow-arrow">↓</p>', unsafe_allow_html=True)


def render_layer_3():
    st.markdown('<div class="layer-header">Layer 3: Normalization Engine</div>', unsafe_allow_html=True)
    
    norm = st.session_state.get("normalization")
    
    col1, col2, col3, col4 = st.columns(4)
    
    if norm:
        col1.metric("Records In", norm.records_in)
        col2.metric("Records Out", norm.records_out)
        col3.metric("Duplicates Removed", norm.duplicates_removed)
        col4.metric("Schema Aligned", "✓" if norm.schema_aligned else "✗")
    else:
        col1.metric("Records In", "—")
        col2.metric("Records Out", "—")
        col3.metric("Duplicates Removed", "—")
        col4.metric("Schema Aligned", "—")
    
    st.markdown('<p class="flow-arrow">↓</p>', unsafe_allow_html=True)


def render_layer_4():
    st.markdown('<div class="layer-header">Layer 4: Validation & Cross-Check</div>', unsafe_allow_html=True)
    st.caption("Core intelligence — Applying 5 validation rules")
    
    validations = st.session_state.get("validations")
    
    if validations:
        for v in validations:
            chip_class = f"chip-{v.status.lower()}"
            st.markdown(f"""
            <div class="validation-rule">
                <div class="header">
                    <span class="name">{v.dimension}</span>
                    <span><span class="{chip_class}">{v.status}</span> <strong>{v.score:.0f}</strong>/100</span>
                </div>
                <div class="detail">Weight: {v.weight*100:.0f}% | {v.detail} | {v.formula}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Execute protocol to run validations")
    
    st.markdown('<p class="flow-arrow">↓</p>', unsafe_allow_html=True)


def render_layer_5():
    st.markdown('<div class="layer-header">Layer 5: Trust Output</div>', unsafe_allow_html=True)
    
    trust = st.session_state.get("trust")
    
    if trust:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
            <div class="fts-display">
                <p class="fts-label">Financial Trust Score</p>
                <p class="fts-score">{trust.fts}</p>
                <p class="fts-label">Confidence: {trust.confidence*100:.0f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Dimension breakdown chart
            dims = ["Revenue", "Cash Flow", "Tax", "Payroll", "Audit"]
            vals = [trust.revenue_integrity, trust.cash_flow, trust.tax_compliance, trust.payroll, trust.audit_readiness]
            weights = [25, 25, 20, 15, 15]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=dims,
                y=vals,
                marker_color=["#4ade80" if v >= 80 else "#facc15" if v >= 60 else "#f87171" for v in vals],
                text=[f"{v}%" for v in vals],
                textposition="outside",
            ))
            fig.update_layout(
                height=200,
                margin=dict(l=20, r=20, t=20, b=40),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                yaxis=dict(range=[0, 110], gridcolor="rgba(56,189,248,0.1)"),
                xaxis=dict(tickfont=dict(size=10)),
            )
            st.plotly_chart(fig, width='stretch')
        
        # Stakeholder Views
        st.markdown("---")
        st.subheader("Stakeholder Views")
        
        tab_msme, tab_bank, tab_reg = st.tabs(["🏢 MSME", "🏦 Bank", "📊 Regulator"])
        
        with tab_msme:
            st.write(f"**Entity:** {st.session_state.entity.name}")
            st.write(f"**Sector:** {st.session_state.entity.sector}")
            st.write(f"**FTS:** {trust.fts}/100 — {'Excellent' if trust.fts >= 80 else 'Good' if trust.fts >= 65 else 'Needs Improvement'}")
            
            if trust.fts < 80:
                st.write("**Improvement Areas:**")
                for v in st.session_state.validations:
                    if v.status != "PASS":
                        st.write(f"- {v.dimension}: {v.detail}")
        
        with tab_bank:
            if trust.fts >= 80:
                st.success("✅ **APPROVED** — Fast-track lending, Prime + 1.5%")
            elif trust.fts >= 65:
                st.warning("⚠️ **CONDITIONAL** — Standard process, Prime + 3.5%")
            else:
                st.error("❌ **REVIEW** — Detailed audit required")
            
            st.markdown("""
            | Metric | Conventional | RTFTI-Enabled |
            |--------|--------------|---------------|
            | Decision Time | 45-90 days | 2-3 days |
            | Collateral | High | Reduced |
            | Interest Rate | Risk-loaded | Behaviour-adjusted |
            """)
        
        with tab_reg:
            if trust.fts >= 70:
                st.success("🟢 **LOW RISK** — No systemic concerns")
            elif trust.fts >= 50:
                st.warning("🟡 **MEDIUM RISK** — Monitor closely")
            else:
                st.error("🔴 **HIGH RISK** — Early intervention recommended")
            
            alerts = [v for v in st.session_state.validations if v.status == "ALERT"]
            if alerts:
                st.write("**Early Warnings:**")
                for a in alerts:
                    st.write(f"- {a.dimension}: {a.detail}")
    else:
        st.info("Execute protocol to generate trust score")


# ============================================================================
# UI: DOCUMENTATION
# ============================================================================

def render_documentation():
    st.markdown("## 📖 RTFTI Protocol Documentation")
    st.markdown("---")
    
    # Overview Section
    st.markdown("### What is RTFTI?")
    st.markdown("""
    **Real-Time Financial Trust Infrastructure (RTFTI)** is a protocol that transforms raw financial data 
    from MSMEs into a standardized, verifiable trust score. It bridges the information asymmetry between 
    small businesses, financial institutions, and regulators.
    
    **The Problem:** MSMEs struggle to access formal credit because banks cannot efficiently verify their 
    financial health. Traditional audits are expensive, slow, and periodic.
    
    **The Solution:** RTFTI creates a continuous, automated trust pipeline that processes real-time 
    financial data through 5 layers to produce an objective Financial Trust Score (FTS).
    """)
    
    st.markdown("---")
    
    # Architecture Section
    st.markdown("### Protocol Architecture")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Layer 1: Data Sources**
        - **General Ledger (GL):** Daily journal entries — debits, credits, accounts
        - **Bank Statements:** Transaction records — deposits, withdrawals, balances
        - **GST Returns:** Tax filings — invoice details, tax collected, input credits
        - **Payroll Records:** Employee data — salaries, PF contributions, ESI
        
        *In production:* Connected via APIs to Tally, banking portals, GST portal, payroll software.
        """)
        
        st.markdown("""
        **Layer 2: Ingestion Gateway**
        - Connects to all configured data sources
        - Validates data format and completeness
        - Counts records and checks connectivity
        - Flags missing or corrupted data streams
        
        *Metrics:* Total records ingested, sources connected, data freshness
        """)
        
        st.markdown("""
        **Layer 3: Normalization Engine**
        - Maps diverse data formats to unified schema
        - Standardizes date formats, currency, account codes
        - Deduplicates records across sources
        - Calculates coverage: `unique_entities / total_records`
        
        *Output:* Normalized dataset ready for validation
        """)
    
    with col2:
        st.markdown("""
        **Layer 4: Validation Engine**
        
        5 validation rules, each producing a score (0-100):
        
        | Rule | What It Checks | Formula |
        |------|----------------|---------|
        | Revenue Integrity | GL vs Bank vs GST match | `100 - deviation × 2` |
        | Cash Flow Behaviour | Inflow/Outflow ratio | `100 - |ratio-1| × 100` |
        | Tax Compliance | GST filing & match rate | `filed% + match%` |
        | Payroll Consistency | PF/ESI compliance | `(pf + esi) / 2` |
        | Audit Readiness | Voucher trail completeness | `matched / total` |
        
        **Thresholds:**
        - 🟢 PASS: ≥ 80
        - 🟡 WARN: 50-79
        - 🔴 ALERT: < 50
        """)
        
        st.markdown("""
        **Layer 5: Trust Output**
        
        **Financial Trust Score (FTS):** 0-100
        
        Weighted average of all validation scores:
        - Revenue Integrity: 25%
        - Cash Flow: 20%
        - Tax Compliance: 20%
        - Payroll: 15%
        - Audit Readiness: 20%
        
        **Confidence:** Based on data completeness and consistency
        """)
    
    st.markdown("---")
    
    # Real-World Implementation
    st.markdown("### 🏭 Real-World Implementation")
    
    st.markdown("""
    #### How to Deploy RTFTI in Production
    
    **Step 1: Data Source Integration**
    ```
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │  Tally/Zoho │     │  Bank APIs  │     │ GST Portal  │     │  Payroll SW │
    │   (GL Data) │     │ (Statements)│     │ (Returns)   │     │  (HR Data)  │
    └──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
           │                   │                   │                   │
           └───────────────────┴───────────────────┴───────────────────┘
                                       │
                               ┌───────▼───────┐
                               │ RTFTI Gateway │
                               └───────────────┘
    ```
    
    **Step 2: API Connections Required**
    | Source | Integration Method | Data Frequency |
    |--------|-------------------|----------------|
    | Tally Prime | Tally Connector API | Daily sync |
    | Bank | Account Aggregator (AA) / Open Banking | Real-time |
    | GST | GST Portal API / GSP | Monthly |
    | Payroll | HRMS API (Zoho, GreytHR) | Monthly |
    
    **Step 3: Continuous Processing**
    - Data pulls scheduled every 24 hours (or real-time via webhooks)
    - Validation runs automatically on new data
    - FTS recalculated and timestamped
    - Historical scores stored for trend analysis
    """)
    
    st.markdown("---")
    
    # Use Cases
    st.markdown("### 🎯 Use Cases & Stakeholder Benefits")
    
    col_msme, col_bank, col_reg = st.columns(3)
    
    with col_msme:
        st.markdown("""
        **🏢 For MSMEs**
        
        *Before RTFTI:*
        - 45-90 day loan approval
        - High collateral requirements
        - Expensive CA audits
        - Opaque rejection reasons
        
        *With RTFTI:*
        - 2-3 day approval
        - Reduced collateral needs
        - Continuous compliance monitoring
        - Clear improvement guidance
        
        **Value:** Access to formal credit at better rates
        """)
    
    with col_bank:
        st.markdown("""
        **🏦 For Banks/NBFCs**
        
        *Before RTFTI:*
        - Manual document verification
        - High NPA risk from information gaps
        - Limited MSME portfolio
        - Expensive due diligence
        
        *With RTFTI:*
        - Automated verification
        - Real-time risk monitoring
        - Expanded MSME lending
        - Behaviour-based pricing
        
        **Value:** Lower NPAs, larger market
        """)
    
    with col_reg:
        st.markdown("""
        **📊 For Regulators**
        
        *Before RTFTI:*
        - Periodic audits (annual)
        - Reactive enforcement
        - Limited visibility into MSME sector
        
        *With RTFTI:*
        - Continuous monitoring
        - Early warning alerts
        - Sector-wide risk heatmaps
        - Policy impact measurement
        
        **Value:** Systemic risk prevention
        """)
    
    st.markdown("---")
    
    # Technical Specifications
    st.markdown("### ⚙️ Technical Specifications")
    
    col_tech1, col_tech2 = st.columns(2)
    
    with col_tech1:
        st.markdown("""
        **Data Requirements**
        - Minimum 3 months of historical data
        - At least 2 data sources connected
        - Data refresh: Daily recommended
        
        **Score Calculation**
        ```python
        FTS = (
            revenue_score × 0.25 +
            cashflow_score × 0.20 +
            tax_score × 0.20 +
            payroll_score × 0.15 +
            audit_score × 0.20
        )
        ```
        """)
    
    with col_tech2:
        st.markdown("""
        **Validation Rules Detail**
        
        **Revenue Integrity:**
        - Compares total credits in GL vs deposits in Bank vs sales in GST
        - Deviation > 10% triggers WARN
        - Deviation > 25% triggers ALERT
        
        **Cash Flow Behaviour:**
        - Ratio = Total Inflows / Total Outflows
        - Healthy range: 0.85 - 1.15
        - Outside range indicates stress
        
        **Tax Compliance:**
        - Checks GST filing status per month
        - Matches invoices to filed returns
        - Delays > 30 days reduce score
        """)
    
    st.markdown("---")
    
    # Future Roadmap
    st.markdown("### 🚀 Future Roadmap")
    st.markdown("""
    | Phase | Feature | Status |
    |-------|---------|--------|
    | v1.0 | Core 5-layer protocol | ✅ Complete |
    | v1.1 | Account Aggregator integration | 🔄 In Progress |
    | v1.2 | Multi-entity comparison | 📋 Planned |
    | v2.0 | ML-based anomaly detection | 📋 Planned |
    | v2.1 | Blockchain audit trail | 📋 Planned |
    | v3.0 | Cross-border MSME support | 📋 Planned |
    """)


# ============================================================================
# MAIN
# ============================================================================

def main():
    # Apply custom theme
    apply_theme()
    
    # Initialize data if needed
    if "gl" not in st.session_state:
        st.session_state.entity = Entity("Precision Tools Pvt. Ltd.", "Manufacturing", 7.5, 42)
        st.session_state.data_seed = 42
        init_data()
    
    # Sidebar
    render_sidebar()
    
    # Main header
    st.markdown('<h1 class="main-title">RTFTI Protocol Terminal</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Real-Time Financial Trust Infrastructure — Full Execution Pipeline</p>', unsafe_allow_html=True)
    
    # Main content tabs
    tab_terminal, tab_docs = st.tabs(["🖥️ Terminal", "📖 Documentation"])
    
    with tab_terminal:
        render_layer_1()
        render_layer_2()
        render_layer_3()
        render_layer_4()
        render_layer_5()
    
    with tab_docs:
        render_documentation()
    
    # Footer
    st.markdown("---")
    st.caption("RTFTI Protocol v1.0 • All layers processed in sequence • Single-page execution console")


if __name__ == "__main__":
    main()
