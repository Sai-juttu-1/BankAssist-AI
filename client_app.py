import streamlit as st
import requests

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Northwind Bank | BankAssist AI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

import os

BACKEND_URL = os.getenv("API_URL", "http://127.0.0.1:8001")

API_URL = f"{BACKEND_URL}/chat"
HEALTH_URL = f"{BACKEND_URL}/health"

# ==================================================
# 2. BANKING IMAGE URLS
# ==================================================

HERO_IMAGE = (
    "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d"
    "?auto=format&fit=crop&w=1400&q=85"
)

HOME_LOAN_IMAGE = (
    "https://images.unsplash.com/photo-1560518883-ce09059eeffa"
    "?auto=format&fit=crop&w=900&q=85"
)

EMI_IMAGE = (
    "https://images.unsplash.com/photo-1554224155-6726b3ff858f"
    "?auto=format&fit=crop&w=900&q=85"
)

ELIGIBILITY_IMAGE = (
    "https://images.unsplash.com/photo-1554224154-26032ffc0d07"
    "?auto=format&fit=crop&w=900&q=85"
)

# ==================================================
# 3. CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>
        .stApp {
            background: #f4f7fb;
        }

        .block-container {
            max-width: 1250px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: #102a43;
        }

        [data-testid="stSidebar"] * {
            color: white;
        }

        [data-testid="stSidebar"] .stButton button {
            background: #1d4967;
            color: white;
            border: 1px solid #315b78;
            border-radius: 9px;
            text-align: left;
        }

        [data-testid="stSidebar"] .stButton button:hover {
            background: #26749a;
            border-color: #26749a;
        }

        /* Navigation */
        .bank-navbar {
            background: #123b67;
            padding: 16px 22px;
            border-radius: 12px;
            margin: 12px 0 24px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }

        .bank-navbar-title {
            color: white;
            font-size: 20px;
            font-weight: 800;
        }

        .bank-navbar-subtitle {
            color: #d6b45c;
            font-size: 12px;
        }

        .nav-links {
            color: white;
            font-size: 13px;
            font-weight: 600;
        }

        /* Hero */
        .hero-title {
            color: #102a43;
            font-size: 39px;
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 12px;
        }

        .hero-description {
            color: #64748b;
            font-size: 16px;
            line-height: 1.7;
        }

        .hero-label {
            color: #147d92;
            font-size: 13px;
            font-weight: 800;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 12px;
        }

        /* Section headings */
        .section-title {
            color: #102a43;
            font-size: 25px;
            font-weight: 800;
            margin-top: 20px;
            margin-bottom: 5px;
        }

        .section-subtitle {
            color: #64748b;
            font-size: 14px;
            margin-bottom: 18px;
        }

        /* Highlights */
        .highlight-card {
            background: white;
            border: 1px solid #e1e8f0;
            border-radius: 12px;
            padding: 18px 12px;
            min-height: 112px;
            text-align: center;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.04);
        }

        .highlight-icon {
            font-size: 27px;
            margin-bottom: 5px;
        }

        .highlight-title {
            color: #123b67;
            font-size: 16px;
            font-weight: 700;
        }

        .highlight-description {
            color: #526579;
            font-size: 12px;
            margin-top: 4px;
        }

        /* Service cards */
        .service-card {
            background: white;
            border: 1px solid #e5eaf1;
            border-radius: 15px;
            padding: 17px;
            min-height: 145px;
            box-shadow: 0 5px 18px rgba(15, 40, 65, 0.05);
        }

        .service-card h3 {
            color: #102a43;
            font-size: 19px;
            margin-top: 3px;
            margin-bottom: 8px;
        }

        .service-card p {
            color: #64748b;
            font-size: 13px;
            line-height: 1.6;
        }

        /* Chat */
        [data-testid="stChatMessage"] {
            background: white;
            border: 1px solid #e5eaf1;
            border-radius: 13px;
            padding: 12px;
            color: #1f2937 !important;
        }

        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] li,
        [data-testid="stChatMessage"] span,
        [data-testid="stChatMessage"] div {
            color: #1f2937 !important;
        }

        .stChatInput textarea,
        .stChatInput textarea:focus {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            background-color: #ffffff !important;
            caret-color: #000000 !important;
        }

        .stChatInput textarea::placeholder {
            color: #777777 !important;
            -webkit-text-fill-color: #777777 !important;
        }

        /* Buttons */
        .stButton button {
            border-radius: 9px;
            font-weight: 600;
        }

        /* Footer */
        .footer {
            color: #64748b;
            text-align: center;
            font-size: 13px;
            padding: 20px 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==================================================
# 4. SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "suggested_question" not in st.session_state:
    st.session_state.suggested_question = None

# ==================================================
# 5. API CONNECTION
# ==================================================

def check_api_status():
    try:
        response = requests.get(HEALTH_URL, timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False


def get_ai_response(question):
    try:
        response = requests.post(
            API_URL,
            json={"question": question},
            timeout=90,
        )
        response.raise_for_status()

        data = response.json()
        answer = data.get("answer")

        if not answer:
            return "The API responded, but no answer was returned."

        return str(answer)

    except requests.exceptions.ConnectionError:
        return (
            "Cannot connect to the BankAssist backend. "
            "Please check whether FastAPI is running."
        )
    except requests.exceptions.Timeout:
        return "The request timed out. Please try again."
    except requests.exceptions.HTTPError as error:
        return f"API error: {error}"
    except requests.exceptions.RequestException as error:
        return f"Connection error: {error}"
    except ValueError:
        return "The backend returned an invalid response."


# ==================================================
# 6. SIDEBAR
# ==================================================

with st.sidebar:
    st.image("assets/northwind_logo.png", width=130)

    st.markdown(
        """
        <h2 style="color:white; text-align:center;">
            NORTHWIND BANK
        </h2>
        <h4 style="color:#d6b45c; text-align:center;">
            BankAssist AI
        </h4>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Your intelligent banking companion")
    st.divider()

    st.markdown("### Quick Actions")

    quick_questions = [
        "What are the home loan interest rates?",
        "What is the floating home loan rate?",
        "Calculate EMI for a 25 lakh loan",
        "Check my personal loan eligibility",
        "Show account details for customer CUST001",
    ]

    for i, item in enumerate(quick_questions):
        if st.button(item, key=f"quick_{i}", width="stretch"):
            st.session_state.suggested_question = item
            st.rerun()

    st.divider()

    if st.button("🗑️ Clear Chat", width="stretch"):
        st.session_state.messages = []
        st.session_state.suggested_question = None
        st.rerun()

    st.divider()
    st.markdown("### About BankAssist")

    st.caption(
        "An AI-powered banking demonstration built using "
        "Python, Streamlit, FastAPI, LangChain and LLMs."
    )

    st.caption(
        "Never enter real banking passwords, PINs or OTPs."
    )

# ==================================================
# 7. BANKING NAVIGATION BAR
# ==================================================

st.markdown(
    """
    <div class="bank-navbar">
        <div>
            <div class="bank-navbar-title">NORTHWIND BANK</div>
            <div class="bank-navbar-subtitle">
                Your Trusted Digital Banking Partner
            </div>
        </div>
        <div class="nav-links">
            HOME &nbsp; | &nbsp; ACCOUNTS &nbsp; | &nbsp;
            LOANS &nbsp; | &nbsp; DEPOSITS &nbsp; | &nbsp; SUPPORT
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==================================================
# 8. HERO SECTION
# ==================================================

hero_left, hero_right = st.columns(
    [1.15, 1],
    vertical_alignment="center",
)

with hero_left:
    st.markdown(
        '<div class="hero-label">WELCOME TO NORTHWIND BANK</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="hero-title">Banking made simpler with AI.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-description">
            Get clear answers to your banking questions, explore loan
            services and calculate your monthly payments with the help
            of BankAssist AI.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.info(
        "Ask BankAssist about loans, EMI calculations and banking policies."
    )

with hero_right:
    st.image(HERO_IMAGE, width="stretch")

st.write("")

# ==================================================
# 9. BACKEND STATUS
# ==================================================

api_online = check_api_status()

status_col, info_col = st.columns([1, 3])

with status_col:
    if api_online:
        st.markdown(
            """
            <div style="
                display:inline-flex;
                align-items:center;
                gap:9px;
                background:#E8F7EF;
                color:#167A45;
                padding:10px 18px;
                border-radius:30px;
                font-size:14px;
                font-weight:600;
                border:1px solid #B7E4CA;
            ">
                <span style="
                    height:9px;
                    width:9px;
                    background:#20A464;
                    border-radius:50%;
                    display:inline-block;
                "></span>
                System Operational
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style="
                display:inline-flex;
                align-items:center;
                gap:9px;
                background:#FFF0F0;
                color:#B42318;
                padding:10px 18px;
                border-radius:30px;
                font-size:14px;
                font-weight:600;
                border:1px solid #F2C5C5;
            ">
                <span style="
                    height:9px;
                    width:9px;
                    background:#DC4444;
                    border-radius:50%;
                    display:inline-block;
                "></span>
                Service Unavailable
            </div>
            """,
            unsafe_allow_html=True,
        )

with info_col:
    st.caption(
        "BankAssist uses the FastAPI backend to process "
        "your questions and return AI-generated answers."
    )

# ==================================================
# 10. BANKING HIGHLIGHTS
# ==================================================

st.markdown(
    "<div class='section-title'>Banking at a glance</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='section-subtitle'>"
    "Simple digital assistance for your everyday banking needs."
    "</div>",
    unsafe_allow_html=True,
)

h1, h2, h3, h4 = st.columns(4, gap="medium")

highlights = [
    ("🛡️", "Secure Banking", "Security-focused experience"),
    ("⚡", "Quick Services", "Simple banking assistance"),
    ("💬", "AI Assistant", "AI-powered support"),
    ("🏦", "Loan Services", "Explore banking options"),
]

for column, (icon, title, description) in zip(
    [h1, h2, h3, h4], highlights
):
    with column:
        st.markdown(
            f"""
            <div class="highlight-card">
                <div class="highlight-icon">{icon}</div>
                <div class="highlight-title">{title}</div>
                <div class="highlight-description">
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")
# ==================================================
# 11. BANKING SERVICES
# ==================================================

st.markdown(
    "<div class='section-title'>Explore Our Services</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='section-subtitle'>"
    "Discover banking services available through BankAssist."
    "</div>",
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.image(HOME_LOAN_IMAGE, width="stretch")

    st.markdown(
        """
        <div class="service-card">
            <h3>🏠 Home Loans</h3>
            <p>
                Explore home loan interest rates and get information
                about loan options.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "Explore Home Loans →",
        key="home_loan",
        width="stretch",
    ):
        st.session_state.suggested_question = (
            "What are the home loan interest rates?"
        )
        st.rerun()

with col2:
    st.image(EMI_IMAGE, width="stretch")

    st.markdown(
        """
        <div class="service-card">
            <h3>🧮 EMI Calculator</h3>
            <p>
                Estimate your monthly loan payments using the principal,
                interest rate and tenure.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "Calculate EMI →",
        key="emi",
        width="stretch",
    ):
        st.session_state.suggested_question = (
            "Calculate EMI for a 25 lakh loan at 8.5% "
            "annual interest for 20 years."
        )
        st.rerun()

with col3:
    st.image(ELIGIBILITY_IMAGE, width="stretch")

    st.markdown(
        """
        <div class="service-card">
            <h3>💳 Loan Eligibility</h3>
            <p>
                Check basic loan eligibility based on income, age
                and credit score.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "Check Eligibility →",
        key="eligibility",
        width="stretch",
    ):
        st.session_state.suggested_question = (
            "Check my personal loan eligibility."
        )
        st.rerun()

# ==================================================
# 12. AI CHAT ASSISTANT
# ==================================================

st.divider()

st.markdown(
    "<div class='section-title'>💬 Chat with BankAssist AI</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='section-subtitle'>"
    "Ask your banking questions and get assistance."
    "</div>",
    unsafe_allow_html=True,
)

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input(
    "Ask BankAssist anything about banking..."
)

# Handle service-card and sidebar questions
if st.session_state.suggested_question:
    question = st.session_state.suggested_question
    st.session_state.suggested_question = None

# ==================================================
# 13. PROCESS USER QUESTION
# ==================================================

if question:
    question = question.strip()

    if question:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner(
                "BankAssist is preparing your answer..."
            ):
                answer = get_ai_response(question)

            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

# ==================================================
# 14. FOOTER
# ==================================================

st.divider()

st.markdown("### 🏦 Northwind Bank | BankAssist AI")
st.caption("Intelligent Banking Assistant")

st.caption(
    "Built with Python · Streamlit · FastAPI · LangChain · LLMs"
)

st.caption(
    "Demonstration project. Banking information and customer "
    "records are sample data, not live banking services."
)
