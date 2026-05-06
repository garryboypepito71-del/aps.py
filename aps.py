import os
import time
from datetime import datetime
import streamlit as st

# ═════════════════ CONFIGURATION ═════════════════
APP_VERSION = "AILY OS v30000 — GREEN EMERALD CORE"
RECEIVER_AILYN = "ailyn_peps0678@yahoo.com"

# ═════════════════ PAGE CONFIG ═════════════════
st.set_page_config(
    page_title="Ailyn Construction Management",
    page_icon="🧊",
    layout="wide",
)

# ═════════════════ SESSION STATE ═════════════════
if "records" not in st.session_state:
    st.session_state.records = []

if "budget" not in st.session_state:
    st.session_state.budget = 0.0

if "view" not in st.session_state:
    st.session_state.view = "home"

# ═════════════════ CORE LOGIC ═════════════════
def set_view(v):
    st.session_state.view = v
    st.rerun()

def total_materials():
    return sum(r["amount"] for r in st.session_state.records if r["type"] == "material")

def total_expenses():
    return sum(r["amount"] for r in st.session_state.records if r["type"] == "expense")

def total_excess():
    return sum(r["amount"] for r in st.session_state.records if r["type"] == "excess")

def get_total():
    return total_materials() + total_expenses()

def get_balance():
    return float(st.session_state.budget) + total_excess() - get_total()

def get_all_records():
    return st.session_state.records

def clear_all():
    st.session_state.records = []
    st.session_state.budget = 0.0

def add_tx(name, price, qty, delivery, ttype, sender):
    if float(price) <= 0 or int(qty) <= 0:
        return False

    amount = (float(price) * int(qty)) + float(delivery) if ttype == "material" else float(price)

    st.session_state.records.append({
        "id": str(time.time()),
        "date": datetime.now().strftime("%b %d, %Y"),
        "name": name.upper(),
        "price": float(price),
        "qty": int(qty),
        "delivery": float(delivery),
        "amount": float(amount),
        "type": ttype,
        "sender": sender
    })
    return True

# ═════════════════ REPORT MANAGER ═════════════════
def build_html_report(records, budget):
    material_total = total_materials()
    expense_total = total_expenses()
    excess_total = total_excess()
    remaining_balance = get_balance()
    date_now = datetime.now().strftime("%B %d, %Y")

    sobra_amount = 0.0
    kulang_amount = 0.0

    if remaining_balance > 0:
        sobra_amount = remaining_balance
    elif remaining_balance < 0:
        kulang_amount = abs(remaining_balance)

    if budget <= 0:
        balance_color = "#ffffff"
    else:
        balance_color = "#e57373" if remaining_balance < 0 else "#a5d6a7"

    html = f"""
    <html>
    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            body {{ font-family: 'Inter', sans-serif; background-color: #f0f4f0; margin: 0; padding: 20px; color: #333; }}
            .receipt-container {{ max-width: 1000px; margin: auto; background: #fff; padding: 30px; border-radius: 4px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-top: 10px solid #1b5e20; }}
            .header {{ display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-start; margin-bottom: 30px; border-bottom: 2px solid #f0f0f0; padding-bottom: 15px; }}
            .company-info h1 {{ color: #1b5e20; margin: 0; font-size: 24px; letter-spacing: -1px; }}
            .company-info p {{ margin: 4px 0; font-size: 12px; color: #666; }}
            .receipt-meta {{ text-align: left; margin-top: 10px; }}
            @media (min-width: 768px) {{ .receipt-meta {{ text-align: right; margin-top: 0; }} }}
            .receipt-meta h2 {{ margin: 0; font-size: 16px; text-transform: uppercase; color: #1b5e20; }}
            .receipt-meta p {{ margin: 4px 0; font-size: 12px; font-weight: bold; }}

            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 12px; }}
            th {{ background-color: #1b5e20; color: #ffffff; text-align: left; padding: 10px; text-transform: uppercase; letter-spacing: 1px; }}
            td {{ padding: 10px 8px; border-bottom: 1px solid #f0f0f0; }}
            .qty-col, .desccol, .pricecol, .deliverycol, .totalcol {{ text-align: left; }}
            .desccol {{ font-weight: 700; color: #1b5e20; }}

            .summary-container {{ display: flex; justify-content: flex-end; }}
            .summary-table {{ width: 100%; }}
            @media (min-width: 768px) {{ .summary-table {{ width: 420px; }} }}
            .grand-total {{ background: #1b5e20; color: white; padding: 20px; border-radius: 4px; margin-top: 15px; }}

            .balance-info {{ font-size: 13px; line-height: 1.8; }}
            .balance-row {{ display: flex; justify-content: space-between; }}
            .material-row {{ font-size: 18px; font-weight: bold; }}
            .final-balance-row {{ display: flex; justify-content: space-between; border-top: 1px dashed rgba(255,255,255,0.4); margin-top: 8px; padding-top: 8px; font-size: 18px; font-weight: bold; }}

            .footer {{ margin-top: 30px; text-align: center; font-size: 9px; color: #aaa; text-transform: uppercase; letter-spacing: 1px; }}
        </style>
    </head>
    <body>
        <div class="receipt-container">
            <div class="header">
                <div class="company-info">
                    <h1>AILYN HOUSE PROJECT</h1>
                    <p>Official Material & Expense Inventory</p>
                    <p>Management System {APP_VERSION}</p>
                    <p>Backup Receiver: <i>{RECEIVER_AILYN}</i></p>
                </div>
                <div class="receipt-meta">
                    <h2>Inventory Receipt</h2>
                    <p>Date: {date_now}</p>
                </div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th class="qty-col">Qty</th>
                        <th class="desccol">Description</th>
                        <th class="pricecol">Unit Price</th>
                        <th class="deliverycol">Delivery</th>
                        <th class="totalcol">Total</th>
                    </tr>
                </thead>
                <tbody>
    """

    for r in records:
        html += f"""
                    <tr>
                        <td>{r['date']}</td>
                        <td class="qty-col">{r['qty']}</td>
                        <td class="desccol">{r['name']}</td>
                        <td class="pricecol">{float(r.get('price', r['amount'])):,.2f}</td>
                        <td class="deliverycol">{float(r['delivery']):,.2f}</td>
                        <td class="totalcol">PHP {float(r['amount']):,.2f}</td>
                    </tr>
        """

    html += f"""
                </tbody>
            </table>

            <div class="summary-container">
                <div class="summary-table">
                    <div class="grand-total">
                        <div class="balance-info">
                            <div class="balance-row material-row">
                                <span>Material/Expense Total:</span>
                                <span>PHP {total_materials() + total_expenses():,.2f}</span>
                            </div>
                            <div class="balance-row" style="font-size: 13px;">
                                <span>Excess Money Total:</span>
                                <span>PHP {total_excess():,.2f}</span>
                            </div>
                            <div class="balance-row" style="font-size: 13px;">
                                <span>Total Budget:</span>
                                <span>PHP {budget:,.2f}</span>
                            </div>
    """

    if sobra_amount > 0:
        html += f"""
                            <div class="final-balance-row">
                                <span>EXCESS</span>
                                <span style="color: #a5d6a7;">PHP {sobra_amount:,.2f}</span>
                            </div>
        """

    if kulang_amount > 0:
        html += f"""
                            <div class="final-balance-row">
                                <span>SHORTAGE</span>
                                <span style="color: #e57373;">PHP {kulang_amount:,.2f}</span>
                            </div>
        """

    html += f"""
                            <div class="final-balance-row">
                                <span>FINAL BALANCE</span>
                                <span style="color: {balance_color};">PHP {remaining_balance:,.2f}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="footer">
                This document was electronically generated and is valid without signature.
            </div>
        </div>
    </body>
    </html>
    """
    return html

# ═════════════════ CSS & 3D GREEN INTERFACE ═════════════════
st.markdown("""
<style>
@media (max-width: 768px) {
    .block-container {
        padding: 10px !important;
    }
    h1, h2, h3 {
        font-size: 18px !important;
        text-align: center;
    }
    button {
        width: 100% !important;
        margin-bottom: 8px !important;
        font-size: 16px !important;
        padding: 12px !important;
    }
    input {
        font-size: 16px !important;
    }
    .stColumns {
        flex-direction: column !important;
    }
}

.stApp {
    background: url("https://images.unsplash.com/photo-1600585154340-be6161a56a0c") no-repeat center center fixed;
    background-size: cover;
    background-position: center;
}

.block-container {
    background: rgba(20, 50, 35, 0.65) !important;
    backdrop-filter: blur(16px);
    border-radius: 20px;
    border: 1px solid rgba(135, 255, 180, 0.2);
    box-shadow: 0 12px 48px rgba(0, 0, 0, 0.6);
    padding: 24px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.block-container:hover {
    transform: scale(1.01);
    box-shadow: 0 16px 64px rgba(72, 239, 127, 0.15);
}

section[data-testid="stSidebar"] {
    background: rgba(10, 30, 20, 0.85) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(135, 255, 180, 0.1);
}

button {
    background: linear-gradient(145deg, #0b4e2f, #167a44);
    color: #ffffff !important;
    border-radius: 14px !important;
    transition: all 0.15s ease-in-out;
    border: 1px solid rgba(135, 255, 180, 0.4);
    font-weight: bold;
    min-height: 45px;
}

button:hover {
    transform: scale(1.02);
    box-shadow: 0 6px 18px rgba(72, 239, 127, 0.3);
    border-color: #a3e635;
    background: linear-gradient(145deg, #167a44, #14a44d);
}

button:active {
    transform: scale(0.98);
}

input, textarea, select {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(135, 255, 180, 0.3) !important;
    color: #4ade80 !important;
    border-radius: 10px !important;
    backdrop-filter: blur(8px);
    font-size: 16px !important;
    min-height: 40px;
    padding: 6px 12px;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

input:focus, textarea:focus, select:focus {
    border-color: #22c55e !important;
    box-shadow: 0 0 10px rgba(34, 197, 94, 0.4);
}

h1, h2, h3 {
    color: #4ade80 !important;
    text-shadow: 0 0 6px rgba(34, 197, 94, 0.3);
    letter-spacing: 0.5px;
}

[data-testid="stMetric"] {
    background: rgba(15, 45, 30, 0.7);
    border-radius: 16px;
    padding: 12px;
    border: 1px solid rgba(135, 255, 180, 0.2);
    margin-bottom: 12px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    transition: transform 0.2s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    border-color: #4ade80;
}

[data-testid="stMetric"] label {
    color: #a3e635 !important;
    font-weight: 600;
}

[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    color: #ffffff !important;
}

.intro {
    text-align: center;
    padding: 16px;
    color: #ffffff;
}

.intro h1 {
    font-size: 28px;
    font-weight: 800;
    color: #4ade80;
}

.intro p {
    font-size: 13px;
    color: #a3e635;
    opacity: 0.9;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="intro">
    <h1>🏗️ AILYN HOUSE PROJECT</h1>
    <p>Mobile Operating Engine v30000</p>
</div>
""", unsafe_allow_html=True)

# 🎛 CONTROL HUB
with st.sidebar:
    st.markdown("## 📱 AILY MOBILE CONTROL")
    
    budget_input = st.number_input("Set Budget", min_value=0.0, key="budget_input_sidebar", value=0.0)
    if st.button("APPLY BUDGET", use_container_width=True):
        st.session_state.budget = float(budget_input)
        st.success("Budget applied!")
        st.rerun()
        
    st.caption(f"{datetime.now().strftime('%I:%M %p | %b %d')}")
    st.divider()

    if st.button("🏠 HOME", use_container_width=True):
        set_view("home")
    if st.button("➕ MATERIAL", use_container_width=True):
        set_view("material")
    if st.button("📝 EXPENSE", use_container_width=True):
        set_view("expense")
    if st.button("💰 EXCESS", use_container_width=True):
        set_view("excess")
    if st.button("📋 LEDGER", use_container_width=True):
        set_view("ledger")
    if st.button("📤 EXPORT", use_container_width=True):
        set_view("export")
    
    st.divider()
    
    if st.button("🔄 RESET SYSTEM", use_container_width=True):
        clear_all()
        set_view("home")

# 🖥 VIEWS
view = st.session_state.view

# 🏠 HOME
if view == "home":
    st.subheader("📊 QUICK STATS")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("BUDGET", f"PHP {st.session_state.budget:,.2f}")
    col2.metric("USED", f"PHP {get_total():,.2f}")
    col3.metric("BALANCE", f"PHP {get_balance():,.2f}")
    
    st.markdown("---")
    
    st.subheader("📋 MATERIALS LEDGER PREVIEW")
    if not st.session_state.records:
        st.info("No materials yet.")
    else:
        materials = [r for r in st.session_state.records if r["type"] == "material"]
        for r in materials[-5:]:
            st.markdown(f"""
            ---
            🧱 **{r['name']}** 💰 PHP {float(r['amount']):,.2f}  
            👤 {r['sender']}  
            📅 {r['date']}
            """)

# ➕ MATERIAL
elif view == "material":
    st.subheader("➕ MATERIAL (LOOP MODE)")

    with st.form(key="material_form", clear_on_submit=True):
        name = st.text_input("Material Name")
        price = st.number_input("Price", min_value=0.01, value=0.01)
        qty = st.number_input("Qty", min_value=1, value=1)
        delivery = st.number_input("Delivery", min_value=0.0, value=0.0)
        sender = st.selectbox("Sender", ["Garr", "Aily"])
        
        submitted = st.form_submit_button(label="SAVE MATERIAL")

    if submitted:
        ok = add_tx(name, price, qty, delivery, "material", sender)
        if ok:
            st.success("Saved! Ready for next order.")
            st.rerun()
        else:
            st.warning("Invalid data, please check amounts.")

    st.divider()
    if st.button("🏁 FINISH LOOP", use_container_width=True):
        st.session_state.view = "home"
        st.rerun()

# 📝 EXPENSE
elif view == "expense":
    st.subheader("📝 EXPENSE (LOOP MODE)")

    with st.form(key="expense_form", clear_on_submit=True):
        name = st.text_input("Expense Name")
        amount = st.number_input("Amount", min_value=0.01, value=0.01)
        sender = st.selectbox("Sender", ["Garr", "Aily"])
        
        submitted = st.form_submit_button(label="SAVE EXPENSE")

    if submitted:
        if amount > 0:
            add_tx(name, amount, 1, 0, "expense", sender)
            st.success("Expense Added → Ledger Updated")
            st.rerun()
        else:
            st.warning("Amount must be greater than zero.")

    st.divider()
    if st.button("🏁 FINISH LOOP", use_container_width=True):
        st.session_state.view = "home"
        st.rerun()

# 💰 EXCESS
elif view == "excess":
    st.subheader("💰 EXCESS (LOOP MODE)")

    with st.form(key="excess_form", clear_on_submit=True):
        name = st.text_input("Reason")
        amount = st.number_input("Amount", min_value=0.01, value=0.01)
        sender = st.selectbox("Sender", ["Garr", "Aily"])
        
        submitted = st.form_submit_button(label="ADD EXCESS")

    if submitted:
        if amount > 0:
            st.session_state.records.append({
                "id": str(time.time()),
                "date": datetime.now().strftime("%b %d, %Y"),
                "name": name.upper(),
                "price": float(amount),
                "qty": 1,
                "delivery": 0.0,
                "amount": float(amount),
                "type": "excess",
                "sender": sender
            })
            st.success("Excess Added")
            st.rerun()
        else:
            st.warning("Please enter a valid amount.")

    st.divider()
    if st.button("🏁 FINISH LOOP", use_container_width=True):
        st.session_state.view = "home"
        st.rerun()

# 📋 LEDGER
elif view == "ledger":
    st.subheader("📋 LEDGER (MOBILE VIEW)")

    if not st.session_state.records:
        st.info("No transaction records found in ledger.")
    else:
        for r in list(st.session_state.records):
            st.markdown(f"""
            ---
            **{r['name']}** 💰 PHP {float(r['amount']):,.2f}  
            👤 {r['sender']}  
            📦 {r['type']}  
            📅 {r['date']}
            """)

            if st.button("❌ DELETE", key=f"del_{r['id']}", use_container_width=True):
                st.session_state.records = [
                    x for x in st.session_state.records if x["id"] != r["id"]
                ]
                st.rerun()

# 📤 EXPORT
elif view == "export":
    st.subheader("📤 EXPORT (MOBILE SAFE)")

    html = build_html_report(st.session_state.records, st.session_state.budget)

    st.download_button(
        label="DOWNLOAD REPORT",
        data=html,
        file_name="aily_mobile_report.html",
        mime="text/html",
        use_container_width=True
    )

    st.markdown("📧 **Receivers Enabled:**")
    st.write("Garry ✔")
    st.write("Aily ✔")
    st.write(f"{RECEIVER_AILYN} ✔")

else:
    st.info("Welcome to AILY OS. Use the sidebar to navigate.")