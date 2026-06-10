import streamlit as st
import base64

from modules.document_reader import read_pdf
from modules.summarizer import load_summarizer, generate_summary
from modules.classifier import classify_document
from modules.qa_engine import load_qa, answer_question

st.set_page_config(
    page_title="Legal-Ease AI",
    page_icon="⚖️",
    layout="wide"
)

@st.cache_resource
def get_summarizer():
    return load_summarizer()

@st.cache_resource
def get_qa():
    return load_qa()

summarizer = get_summarizer()
qa_model = get_qa()

# Session state initialization
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if "document_info" not in st.session_state:
    st.session_state.document_info = None

if "classification_result" not in st.session_state:
    st.session_state.classification_result = None

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "document_name" not in st.session_state:
    st.session_state.document_name = ""

if "selected_question" not in st.session_state:
    st.session_state.selected_question = ""

if "qa_answer" not in st.session_state:
    st.session_state.qa_answer = ""

if "qa_question" not in st.session_state:
    st.session_state.qa_question = ""

def get_base64(image_path):
    with open(image_path, "rb") as image:
        return base64.b64encode(image.read()).decode()

background_image = get_base64("assets/background.jpg")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(10,20,40,0.85), rgba(10,20,40,0.85)),
        url("data:image/jpg;base64,{background_image}");
        background-size: cover;
        background-attachment: fixed;
    }}

    .stButton > button {{
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59,130,246,0.3);
        width: 100%;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59,130,246,0.5);
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
    }}

    .stButton {{
        margin-bottom: 0.5rem;
    }}
    
    .sub-header {{
        font-size: 2rem;
        color: #FFFFFF;
        margin: 1.5rem 0rem 1rem 0rem;
        font-weight: 600;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.8);
        border-bottom: 3px solid #3B82F6;
        padding-bottom: 0.5rem;
    }}
    
    .success-box {{
        background: linear-gradient(135deg, #10B981, #059669);
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0rem;
        color: white;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        text-align: center;
        border-left: 5px solid #047857;
    }}
    
    .summary-box {{
        background-color: #1E293B;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #3B82F6;
        color: #FFFFFF;
        font-size: 1rem;
        line-height: 1.6;
        height: 400px;
        overflow-y: auto;
    }}
    
    .stats-card-blue {{
        background: linear-gradient(135deg, #3B82F6, #2563EB);
        padding: 1rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(59,130,246,0.3);
    }}
    
    .stats-number {{
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }}
    
    .stats-label {{
        font-size: 0.85rem;
        opacity: 0.95;
        margin: 0;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ================= SIDEBAR =================

with st.sidebar:
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #1E293B, #334155);
            border-right: 1px solid #3B82F6;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #0F172A, #1E293B);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            border: 1px solid #3B82F6;
            margin-bottom: 20px;
        ">
            <h2 style="color: #3B82F6; margin: 0; font-size: 1.5rem;">⚖️ LegalEase AI</h2>
            <p style="color: #94A3B8; margin: 0.5rem 0 0 0; font-size: 0.8rem;">
                Legal Document Analysis
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <p style="color: #94A3B8; font-size: 0.8rem; letter-spacing: 1px; margin-bottom: 0.5rem;">📍 NAVIGATION</p>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = "Home"
    with col2:
        if st.button("📝 Summary", use_container_width=True):
            st.session_state.page = "Summary"

    col3, col4 = st.columns(2)
    with col3:
        if st.button("🏷️ Classify", use_container_width=True):
            st.session_state.page = "Classification"
    with col4:
        if st.button("❓ Q&A", use_container_width=True):
            st.session_state.page = "Q&A"

    st.markdown("---")

    st.markdown(
        """
        <p style="color: #94A3B8; font-size: 0.8rem; letter-spacing: 1px; margin-bottom: 0.5rem;">📁 DOCUMENT UPLOAD</p>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Drag and drop file here",
        type=["pdf"],
        label_visibility="collapsed"
    )

page = st.session_state.page

# ================= PROCESS UPLOADED FILE =================

if uploaded_file is not None:
    if st.session_state.document_name != uploaded_file.name:
        st.session_state.document_text = ""
        st.session_state.document_info = None
        st.session_state.classification_result = None
        st.session_state.summary = ""
        st.session_state.document_name = ""

        text, info = read_pdf(uploaded_file)

        if text:
            st.session_state.document_text = text
            st.session_state.document_info = info
            st.session_state.document_name = uploaded_file.name
            
            with st.spinner("Generating summary..."):
                st.session_state.summary = generate_summary(text, summarizer)
            
            with st.spinner("Classifying document..."):
                st.session_state.classification_result = classify_document(text)
            
            st.success("✅ Document processed successfully!")

# ================= HOME PAGE =================

if page == "Home":
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 50px;">
            <h1 style="color: white; font-size: 70px; font-weight: 700; text-shadow: 2px 2px 8px rgba(0,0,0,0.7); margin: 0; padding: 0;">⚖️ LegalEase AI</h1>
            <p style="color: white; font-size: 20px; text-shadow: 2px 2px 4px rgba(0,0,0,0.7); margin: 10px 0 0 0; padding: 0; opacity: 0.9;">Advanced Legal Document Analysis Platform</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div style="background-color:#F3F4F6; border-radius:20px; border:2px solid #3B82F6; height:220px; padding:15px; text-align:center;">
                <h2 style="color:#1F2937; font-weight:700; margin: 0 0 10px 0;">📝 Smart Summarization</h2>
                <p style="color:#4B5563; font-size:17px; line-height:1.6; margin: 0;">Generate concise, meaningful summaries of complex legal documents.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Use Summary Tool", key="summary_card", use_container_width=True):
            st.session_state.page = "Summary"
            st.rerun()

    with col2:
        st.markdown(
            """
            <div style="background-color:#F3F4F6; border-radius:20px; border:2px solid #3B82F6; height:220px; padding:15px; text-align:center;">
                <h2 style="color:#1F2937; font-weight:700; margin: 0 0 10px 0;">🏷️ Legal Classification</h2>
                <p style="color:#4B5563; font-size:17px; line-height:1.6; margin: 0;">Automatically categorize documents into legal domains.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Use Classification", key="classification_card", use_container_width=True):
            st.session_state.page = "Classification"
            st.rerun()

    with col3:
        st.markdown(
            """
            <div style="background-color:#F3F4F6; border-radius:20px; border:2px solid #3B82F6; height:220px; padding:15px; text-align:center;">
                <h2 style="color:#1F2937; font-weight:700; margin: 0 0 10px 0;">❓ Intelligent Q&A</h2>
                <p style="color:#4B5563; font-size:17px; line-height:1.6; margin: 0;">Ask questions and get precise answers from your documents.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Use Q&A", key="qa_card", use_container_width=True):
            st.session_state.page = "Q&A"
            st.rerun()

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="background-color:rgba(31,41,55,0.85); border-radius:20px; padding:35px;">
            <h1 style="color:white; margin: 0 0 15px 0;">About LegalEase AI</h1>
            <p style="color:white; font-size:18px; line-height:1.9; margin: 0;">
            LegalEase AI is an intelligent legal document analysis platform developed
            to simplify the understanding of complex legal documents. It enables users
            to automatically generate concise summaries, classify documents into legal
            domains, and obtain precise answers through question answering.
            <br><br>
            The system helps students, researchers, and legal professionals save time
            and improve accessibility by transforming lengthy documents into meaningful
            and easily understandable information.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align:center; color:white; font-size:16px; opacity: 0.8;">
        ⚖️ LegalEase AI - Professional Legal Document Analysis
        </div>
        """,
        unsafe_allow_html=True
    )

# ================= SUMMARY PAGE =================

if page == "Summary":
    st.markdown('<div class="sub-header">📝 AI-Powered Document Summary</div>', unsafe_allow_html=True)

    col_back, _ = st.columns([1, 5])
    with col_back:
        if st.button("← Back to Home", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()

    if st.session_state.document_text == "":
        st.warning("Please upload a PDF from the sidebar.")
    else:
        st.markdown(
            f"""
            <div class="success-box">
            📄 Document: {st.session_state.document_name}
            </div>
            """,
            unsafe_allow_html=True
        )
        
        col_summary, col_stats = st.columns([3, 1])

        with col_summary:
            st.markdown("#### 📋 Legal Document Summary")
            summary_text = st.session_state.summary if st.session_state.summary else "Generating summary..."
            st.markdown(
                f"""
                <div class="summary-box">
                {summary_text}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_stats:
            st.markdown("#### 📊 Quick Stats")
            
            summary_word_count = len(st.session_state.summary.split()) if st.session_state.summary else 0
            
            total_words = 0
            total_pages = 0
            if st.session_state.document_info:
                total_words = st.session_state.document_info.get('words', 0)
                total_pages = st.session_state.document_info.get('pages', 0)
            
            st.markdown(
                f"""
                <div class="stats-card-blue">
                    <p class="stats-number">{total_words}</p>
                    <p class="stats-label">Total Words</p>
                </div>
                
                <div class="stats-card-blue">
                    <p class="stats-number">{total_pages}</p>
                    <p class="stats-label">Pages</p>
                </div>
                
                <div class="stats-card-blue">
                    <p class="stats-number">{summary_word_count}</p>
                    <p class="stats-label">Summary Length (words)</p>
                </div>
                """,
                unsafe_allow_html=True
            )

# ================= CLASSIFICATION PAGE =================

if page == "Classification":
    st.markdown('<div class="sub-header">🏷️ Legal Document Classification</div>', unsafe_allow_html=True)

    col_back, _ = st.columns([1, 5])
    with col_back:
        if st.button("← Back to Home", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()

    if st.session_state.document_text == "":
        st.warning("Please upload a PDF from the sidebar.")
    elif st.session_state.classification_result is None:
        st.info("🔄 Processing document... Please wait.")
    else:
        st.markdown(
            f"""
            <div class="success-box">
            📄 Document: {st.session_state.document_name}
            </div>
            """,
            unsafe_allow_html=True
        )
        
        category = st.session_state.classification_result["category"]
        confidence = st.session_state.classification_result["confidence"]
        
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #1E293B, #0F172A); border: 2px solid #3B82F6; border-radius: 12px; padding: 1.25rem; margin-bottom: 1.5rem; text-align: center;">
                <p style="color: #94A3B8; font-size: 0.9rem; margin: 0; letter-spacing: 1px;">PRIMARY CATEGORY</p>
                <p style="color: #3B82F6; font-size: 2rem; font-weight: 700; margin: 0.25rem 0;">{category}</p>
                <p style="color: #FFFFFF; font-size: 1.1rem; margin: 0;">{confidence}% confidence</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <h4 style="color: #FFFFFF; border-bottom: 2px solid #3B82F6; padding-bottom: 0.5rem; display: inline-block; margin-bottom: 1.5rem;">📈 Confidence Scores</h4>
            """,
            unsafe_allow_html=True
        )
        
        all_scores = st.session_state.classification_result.get("all_scores", [])
        
        if all_scores:
            cols = st.columns(2)
            for idx, score_data in enumerate(all_scores):
                cat = score_data["category"]
                percentage = score_data["percentage"]
                
                if cat == "Other" and percentage == 0:
                    continue
                
                with cols[idx % 2]:
                    st.markdown(
                        f"""
                        <div style="background: #1E293B; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.75rem; border-left: 3px solid #3B82F6;">
                            <span style="color: #FFFFFF; font-weight: 500;">{cat}</span>
                            <span style="color: #3B82F6; font-weight: 600; float: right;">{percentage}%</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

# ================= SUGGESTED QUESTIONS =================

SUGGESTED_QUESTIONS = {
    "Criminal Law": [
        "Who filed the complaint?",
        "What items were stolen?",
        "When did the incident occur?",
        "Who are the accused?",
        "Which police station handled the case?"
    ],
    "Contract Law": [
        "Who are the parties involved?",
        "What is the agreement about?",
        "What are the obligations of the parties?",
        "What is the duration of the contract?",
        "What are the payment terms?"
    ],
    "Corporate Law": [
        "What company is involved?",
        "Who are the directors?",
        "What is the purpose of the company?",
        "Are shareholders mentioned?",
        "Is there any merger or acquisition?"
    ],
    "Property Law": [
        "Who owns the property?",
        "Where is the property located?",
        "What type of property is involved?",
        "Is there a lease agreement?",
        "What are the ownership details?"
    ],
    "Intellectual Property Law": [
        "What intellectual property is involved?",
        "Is a patent mentioned?",
        "Is a trademark mentioned?",
        "Who owns the rights?",
        "Is infringement discussed?"
    ],
    "Employment Law": [
        "Who is the employee?",
        "What is the salary mentioned?",
        "Is there a termination clause?",
        "What are the working conditions?",
        "Is an employment agreement present?"
    ],
    "Other": [
        "What is this document about?",
        "Who are the parties involved?",
        "What important dates are mentioned?",
        "What amounts are mentioned?",
        "What is the purpose of the document?"
    ]
}

# ================= Q&A PAGE =================

if page == "Q&A":
    st.markdown('<div class="sub-header">💬 Document Q&A Assistant</div>', unsafe_allow_html=True)

    col_back, _ = st.columns([1, 5])
    with col_back:
        if st.button("← Back to Home", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()

    if st.session_state.document_text == "":
        st.warning("Please upload a PDF from the sidebar.")
    elif st.session_state.classification_result is None:
        st.info("🔄 Processing document... Please wait.")
    else:
        category = st.session_state.classification_result["category"]
        
        st.markdown(
            """
            <h4 style="color: #FFFFFF; border-bottom: 2px solid #3B82F6; padding-bottom: 0.5rem; display: inline-block; margin-bottom: 1.5rem;">💡 Suggested Questions</h4>
            """,
            unsafe_allow_html=True
        )
        
        questions = SUGGESTED_QUESTIONS.get(category, SUGGESTED_QUESTIONS["Other"])
        
        cols = st.columns(3)
        for idx, question in enumerate(questions):
            with cols[idx % 3]:
                if st.button(question, key=f"suggested_{idx}", use_container_width=True):
                    with st.spinner("Finding answer..."):
                        answer = answer_question(question, st.session_state.document_text, qa_model)
                    st.session_state.qa_answer = answer
                    st.session_state.qa_question = question
                    st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(
            """
            <h4 style="color: #FFFFFF; border-bottom: 2px solid #3B82F6; padding-bottom: 0.5rem; display: inline-block; margin-bottom: 1rem;">✏️ Ask Your Own Question</h4>
            """,
            unsafe_allow_html=True
        )
        
        custom_question = st.text_input(
            "Enter your question:",
            placeholder="Type your question here...",
            label_visibility="collapsed"
        )
        
        if st.button("🔍 Get Answer", use_container_width=True):
            if custom_question.strip() == "":
                st.warning("Please enter a question.")
            else:
                with st.spinner("Finding answer..."):
                    answer = answer_question(custom_question, st.session_state.document_text, qa_model)
                st.session_state.qa_answer = answer
                st.session_state.qa_question = custom_question
                st.rerun()
        
        if "qa_answer" in st.session_state and st.session_state.qa_answer:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #1E293B, #0F172A); border-left: 4px solid #3B82F6; border-radius: 10px; padding: 1rem; margin-top: 1rem;">
                    <p style="color: #3B82F6; font-weight: 600; margin: 0 0 0.5rem 0;">✅ Answer</p>
                    <p style="color: #FFFFFF; margin: 0; line-height: 1.6;">{st.session_state.qa_answer}</p>
                </div>
                """,
                unsafe_allow_html=True
            )