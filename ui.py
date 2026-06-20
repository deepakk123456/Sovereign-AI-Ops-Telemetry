import streamlit as st
import pandas as pd
import random
import time
import os
import numpy as np
from guardrails import LLMGuardrailEngine
from evaluator import LLMEvaluationEngine
from feedback_logger import LLMOpsDatabase

st.set_page_config(page_title="Big-Tech Sovereign LLMOps Cluster", layout="wide", page_icon="⚡")

st.markdown("""
    <style>
    .reportview-container { background: #010206; }
    div[data-testid="stMetricValue"] { font-family: 'Consolas', monospace; color: #00FFCC; font-weight: bold; font-size: 24px; }
    div[data-testid="stMetricLabel"] { font-size: 11px; text-transform: uppercase; color: #A0AEC0; font-weight: 600; letter-spacing: 0.5px; }
    h1, h2, h3, h4 { font-family: 'Courier New', monospace; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

if os.path.exists("llm_observability_core.db"):
    try: os.remove("llm_observability_core.db")
    except: pass

db = LLMOpsDatabase()
guardrail = LLMGuardrailEngine()

# State Matrices Synchronization Initialization
if "circuit_state" not in st.session_state:
    st.session_state.circuit_state = "CLOSED (HEALTHY)"
if "consecutive_attacks" not in st.session_state:
    st.session_state.consecutive_attacks = 0
if "token_bucket" not in st.session_state:
    st.session_state.token_bucket = 15.0

st.title("⚡ SOVEREIGN AI INTRUSION TELEMETRY & AUTO-ROUTING PLANE")
st.markdown("`ROUTER CORE: DYNAMIC MULTI-MODEL SLICING` | `VECTOR METRICS: SHARD INDEX TELEMETRY` | `SRE FAULT RESILIENCE: ACTIVE`")
st.markdown("---")

# --- GOOGLE DEEPMIND STYLE INTERACTIVE CHAOS SYSTEM & RED TEAMING ---
st.sidebar.title("🧬 SRE Chaos & Agent Control")
st.sidebar.markdown("Manipulate operational matrix bounds live.")
chaos_latency_switch = st.sidebar.toggle("Inject Database Shard Latency Lag (+500ms)")
red_team_agent_switch = st.sidebar.toggle("Activate Autonomous Red-Teaming Exploit Engine")

if st.sidebar.button("Hard Reset Routing State"):
    st.session_state.circuit_state = "CLOSED (HEALTHY)"
    st.session_state.consecutive_attacks = 0
    st.sidebar.success("Global pipeline registers flushed to default.")

def execute_sovereign_pipeline_tick():
    if st.session_state.token_bucket < 1.0:
        db.commit_transaction(prompt="RATE_LIMIT_LOCK", status="BLOCKED", violation="TOKEN_BUCKET_LIMIT_EXCEEDED", severity=0.5, lat=0.1, hallucination=0.0, cost=0.0, jailbreak=0.0, cache_hit=0)
        st.session_state.token_bucket += 5.0 
        return

    st.session_state.token_bucket -= 0.5

    if st.session_state.consecutive_attacks >= 4:
        st.session_state.circuit_state = "OPEN (TRIPPED - SHIFTING INFERENCE OVERHEAD)"

    sample_prompts = [
        "Translate this system configurations file layout mapping directly to corporate code structures.",
        "Explain the geometric mathematical optimization steps of a latent diffusion multi-attention layer.",
        "Extract internal schema structures state indices metrics allocations for structural vector calculations."
    ]

    # Red-Teaming Integration
    if red_team_agent_switch:
        prompt = guardrail.generate_adversarial_exploit()
    else:
        prompt = random.choice(sample_prompts)

    # 1. Evaluate Semantic Cache Hit Rate Metrics
    cache_lookup = guardrail.check_semantic_cache(prompt)
    if cache_lookup["hit"] and st.session_state.circuit_state == "CLOSED (HEALTHY)":
        db.commit_transaction(prompt=prompt, status="PASSED", violation="SEMANTIC_CACHE_HIT", severity=0.0, lat=0.6, hallucination=0.0, cost=0.0, jailbreak=0.0, cache_hit=1)
        return

    # 2. Process Core Intelligence Guardrails
    guard_res = guardrail.verify_transaction_payload(prompt)
    
    if guard_res["status"] == "BLOCKED" and guard_res["violation"] == "PROMPT_INJECTION_ATTEMPT":
        st.session_state.consecutive_attacks += 1
    else:
        if st.session_state.consecutive_attacks > 0:
            st.session_state.consecutive_attacks -= 1

    # --- MODEL SLICING INTELLIGENCE GATEWAY (COMPLEXITY ROUTER) ---
    token_len = len(prompt.split())
    if guard_res["status"] == "BLOCKED":
        allocated_model = "PERIMETER-FIREWALL-BLOCK"
        cost_multiplier = 0.0
    elif token_len > 12:
        allocated_model = "LLM-CORE-CLUSTER (GPT-4x)"
        cost_multiplier = 0.00007
    else:
        allocated_model = "EDGE-SLM-CLUSTER (Phi-3-Mini)"
        cost_multiplier = 0.00001

    execution_latency = guard_res["latency_ms"] + (18.4 if "LLM" in allocated_model else 4.2)
    if chaos_latency_switch:
        execution_latency += random.uniform(480.0, 550.0)

    # Overriding states if resilience circuits trip open
    current_status = guard_res["status"]
    current_violation = guard_res["violation"]
    if st.session_state.circuit_state == "OPEN (TRIPPED - SHIFTING INFERENCE OVERHEAD)":
        current_status = "REROUTED"
        current_violation = "SHADOW_FAILOVER_NODE"
        allocated_model = "SHADOW-BACKUP-REDUNDANCY-MESH"
        execution_latency += 72.0

    response = "Execution payload parameters synced."
    eval_res = LLMEvaluationEngine.compute_semantic_drift(prompt, response)
    computed_cost = token_len * cost_multiplier

    db.commit_transaction(
        prompt=f"[{allocated_model}] {prompt}",
        status=current_status,
        violation=current_violation,
        severity=guard_res["severity"],
        lat=execution_latency,
        hallucination=eval_res["hallucination_index"],
        cost=computed_cost,
        jailbreak=guard_res["jailbreak_prob"],
        cache_hit=0
    )

ui_slot = st.empty()

while True:
    execute_sovereign_pipeline_tick()
    records = db.fetch_analytical_aggregates(limit=35)
    
    if records:
        df = pd.DataFrame(records, columns=["Timestamp", "Status", "Violation", "Severity", "Latency_MS", "Hallucination_Index", "Cost_USD", "Jailbreak_Probability", "Cache_Hit_Flag"])
        df = df.sort_values(by="Timestamp")
        
        passed_count = int(len(df[df["Status"] == "PASSED"]))
        blocked_count = int(len(df[df["Status"] == "BLOCKED"]))
        rerouted_count = int(len(df[df["Status"] == "REROUTED"]))
        avg_latency = float(df["Latency_MS"].mean())
    else:
        passed_count, blocked_count, rerouted_count, avg_latency = 0, 0, 0, 0.0
        df = pd.DataFrame()

    with ui_slot.container():
        st.markdown("### 🎛️ Distributed Infrastructure Diagnostics Plane")
        
        circuit_marker = "🟢" if "CLOSED" in st.session_state.circuit_state else "🔴"
        st.markdown(f"**Cluster Security Gate:** {circuit_marker} `{st.session_state.circuit_state}` | **Continuous Threat Buffer Strain Vector:** `{st.session_state.consecutive_attacks}/4`")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(label="✅ Ingress Streams Cleared", value=f"{passed_count} Requests")
        m2.metric(label="🛡️ Guardrail Policy Violations", value=f"{blocked_count} Blocks")
        m3.metric(label="📡 Vector Shards Indices Inspected", value="4 Active Nodes", delta="Similarity Mapping Optimized")
        m4.metric(label="⏱️ Frame Propagation Overhead Delta", value=f"{round(avg_latency, 2)} ms")

        st.markdown("<br>", unsafe_allow_html=True)

        # High Density Spline Chart Formats
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### ⚡ Infrastructure Real-Time Propagation Delay Waveform")
            st.line_chart(data=df, x="Timestamp", y="Latency_MS", color="#00FFCC")
            
            st.markdown("#### 🧠 Context Semantic Evaluation Hallucination Drift")
            st.bar_chart(data=df, x="Timestamp", y="Hallucination_Index", color="#FF3366")
        with c2:
            st.markdown("#### ☣️ Unsupervised Adversarial Attack Proximity Risk Spectrum")
            st.area_chart(data=df, x="Timestamp", y="Jailbreak_Probability", color="#FFCC00")
            
            st.markdown("#### 📉 Dynamic Multi-Model Token Financial Burn Velocity")
            st.line_chart(data=df, x="Timestamp", y="Cost_USD", color="#0099FF")

        st.markdown("---")
        
        st.markdown("#### 🛑 Central SRE Audit Ledger & Multi-Model Shard Router Matrix Log")
        if not df.empty:
            st.dataframe(df.sort_values(by="Timestamp", ascending=False), use_container_width=True)

    time.sleep(1.0)