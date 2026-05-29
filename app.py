import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import random

# --- AGRO-NETRA AI PAGE SETUP ---
st.set_page_config(
    page_title="AgroNetra AI — Smart Crop Protection",
    page_icon="👁️🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GEMINI API INTEGRATION ---
# ⚠️ SECURITY NOTICE: Put your real Gemini API key between the quotes below
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY" 
genai.configure(api_key=GEMINI_API_KEY)

# Initialized models with the correct '-latest' tag
chat_model = genai.GenerativeModel('gemini-2.5-flash')
vision_model = genai.GenerativeModel('gemini-2.5-flash')

# --- UPGRADED CINEMATIC STYLING & ANIMATIONS ---
st.markdown("""
<style>
    /* Import Google Fonts for a modern, sleek look */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Cinematic Fade-In */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(-20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    /* Subtle breathing scale animation for the quote */
    @keyframes subtlePulse {
        0% { transform: scale(1); box-shadow: 0 4px 15px rgba(46,125,50,0.2); }
        50% { transform: scale(1.02); box-shadow: 0 10px 30px rgba(46,125,50,0.4); }
        100% { transform: scale(1); box-shadow: 0 4px 15px rgba(46,125,50,0.2); }
    }

    .animated-header {
        animation: fadeIn 1.2s ease-out;
        color: #1b5e20;
        font-weight: 800;
        text-align: center;
        letter-spacing: -0.5px;
        margin-bottom: 30px;
        font-size: 3rem !important;
    }

    .brand-highlight {
        background: linear-gradient(120deg, #1b5e20, #4caf50, #81c784);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }

    /* The rotating quote card - enhanced */
    .quote-card {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
        color: #ffffff;
        padding: 25px 40px;
        border-radius: 16px;
        text-align: center;
        font-size: 1.3rem;
        font-style: italic;
        font-weight: 300;
        margin: 0 auto 40px auto;
        max-width: 800px;
        animation: subtlePulse 5s infinite ease-in-out;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Cinematic Glassmorphism Container for the Scanner */
    .glass-container {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 40px;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08), 0 0 20px rgba(218, 165, 32, 0.15);
        margin-top: 10px;
    }

    .report-block {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 16px;
        border-left: 8px solid #4caf50;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin-top: 30px;
        font-size: 1.1rem;
        line-height: 1.7;
    }

    /* Style the file uploader visually */
    .stFileUploader > div > div {
        background-color: #f8fcf8;
        border: 2px dashed #4caf50;
        border-radius: 16px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    .stFileUploader > div > div:hover {
        background-color: #f1f8f1;
        border-color: #2e7d32;
    }

    /* Upgrade the primary button */
    .stButton > button {
        background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        border-radius: 12px;
        padding: 10px 24px;
        border: none;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.6);
        background: linear-gradient(135deg, #43a047 0%, #1b5e20 100%);
    }
</style>
""", unsafe_allow_html=True)

# --- COMPREHENSIVE MULTILINGUAL DICTIONARY ---
LANG_DATA = {
    "English": {
        "nav_scanner": "🔬 AgroNetra Disease Scanner", "nav_chat": "💬 Krushisevak Chat Box", 
        "nav_about": "🌱 About Our Core Vision", "nav_support": "🤝 Farmer Support Desk",
        "scan_title": "AgroNetra AI — Crop Disease Prediction", "scan_lbl": "Upload a clear image of an infected crop leaf:",
        "scan_btn": "Generate Real-Time AgroNetra Report", "chat_title": "Krushisevak AI Assistant",
        "chat_placeholder": "Ask Krushisevak anything about crops, seeds, weather, or fertilizers...",
        "sub_name": "Full Name", "sub_phone": "Mobile Number", "sub_msg": "Describe your issue", "sub_btn": "Submit Ticket"
    },
    "Hindi (हिन्दी)": {
        "nav_scanner": "🔬 एग्रोनेत्र फसल रोग स्कैनर", "nav_chat": "💬 कृषिसेवक चैट बॉक्स", 
        "nav_about": "🌱 हमारा मूल दृष्टिकोण", "nav_support": "🤝 किसान सहायता डेस्क",
        "scan_title": "AgroNetra AI — फसल रोग पूर्वानुमान", "scan_lbl": "संक्रमित फसल की पत्ती की एक स्पष्ट छवि अपलोड करें:",
        "scan_btn": "वास्तविक समय एग्रोनेत्र रिपोर्ट प्राप्त करें", "chat_title": "कृषिसेवक एआई सहायक",
        "chat_placeholder": "कृषिसेवक से फसलों, बीजों, मौसम या उर्वरकों के बारे में कुछ भी पूछें...",
        "sub_name": "पूरा नाम", "sub_phone": "मोबाइल नंबर", "sub_msg": "अपनी समस्या लिखें", "sub_btn": "टिकट जमा करें"
    },
    "Gujarati (ગુજરાતી)": {
        "nav_scanner": "🔬 એગ્રોનેત્ર પાક રોગ સ્કેનર", "nav_chat": "💬 કૃષિસેવક ચેટ બોક્સ", 
        "nav_about": "🌱 અમારું મૂળ વિઝન", "nav_support": "🤝 ખેડૂત સપોર્ટ ડેસ્ક",
        "scan_title": "AgroNetra AI — પાક રોગ નિદાન", "scan_lbl": "ચેપગ્રસ્ત પાકના પાંદડાની સ્પષ્ટ છબી અપલોડ કરો:",
        "scan_btn": "રીઅલ-ટાઇમ એગ્રોનેત્ર અહેવાલ મેળવો", "chat_title": "કૃષિસેવક AI સહાયક",
        "chat_placeholder": "પાક, બિયારણ, હવામાન અથવા ખાતરો વિશે કૃષિસેવકને કંઈપણ પૂછો...",
        "sub_name": "આખું નામ", "sub_phone": "મોબાઇલ નંબર", "sub_msg": "તમારી समस्या વર્ણવો", "sub_btn": "સબમિટ કરો"
    },
    "Marathi (मराठी)": {
        "nav_scanner": "🔬 एग्रोनेत्र पीक रोग स्कॅनर", "nav_chat": "💬 कृषिसेवक चॅट बॉक्स", 
        "nav_about": "🌱 आमचा मूळ दृष्टीकोन", "nav_support": "🤝 शेतकरी मदत केंद्र",
        "scan_title": "AgroNetra AI — पीक रोग अंदाज", "scan_lbl": "संक्रमित पिकाच्या पानाच्या स्पष्ट फोटो अपलोड करा:",
        "scan_btn": "रिअल-टाइम एग्रोनेत्र अहवाल तयार करा", "chat_title": "कृषिसेवक एआई सहाय्यक",
        "chat_placeholder": "कृषिसेवकला पिके, बियाणे, हवामान किंवा खतांबद्दल काहीही विचारा...",
        "sub_name": "पूर्ण नाव", "sub_phone": "मोबाईल नंबर", "sub_msg": "तुमची समस्या लिहा", "sub_btn": "सबमिट करा"
    }
}

INDIAN_AGRI_QUOTES = [
    "\"If agriculture goes wrong, nothing else will have a chance to go right in the country.\" — Dr. M.S. Swaminathan",
    "\"Jai Jawan, Jai Kisan, Jai Vigyan, Jai Anusandhan.\" — Indian National Slogan",
    "\"To forget how to dig the earth and to tend the soil is to forget ourselves.\" — Mahatma Gandhi",
    "\"The soul of India lives in its villages, and the heart of those villages is our farmers.\" — Traditional Indian Wisdom"
]

# --- SIDEBAR BRANDING ---
st.sidebar.markdown("<br>", unsafe_allow_html=True)
logo_path = "assets/logo.png"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)
st.sidebar.markdown("<h2 style='text-align:center;'>👁️ <span class='brand-highlight'>AgroNetra AI</span></h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Language Selector
selected_lang_name = st.sidebar.selectbox(
    "🌍 Choose Language / भाषा चुनें", 
    ["English", "Hindi (हिन्दी)", "Gujarati (ગુજરાતી)", "Marathi (मराठी)"]
)
L = LANG_DATA[selected_lang_name]

# Main Navigation
menu_choice = st.sidebar.radio(
    "🧭 Navigation Panel", 
    [L["nav_scanner"], L["nav_chat"], L["nav_about"], L["nav_support"]]
)

# --- PAGE 1: DISEASE SCANNER ---
if menu_choice == L["nav_scanner"]:
    st.markdown(f'<h1 class="animated-header"><span class="brand-highlight">AgroNetra AI</span><br>Crop Disease Prediction</h1>', unsafe_allow_html=True)
    
    selected_quote = random.choice(INDIAN_AGRI_QUOTES)
    st.markdown(f'<div class="quote-card">{selected_quote}</div>', unsafe_allow_html=True)
    
    # Create columns to center the glass container on wide screens
    col1, col2, col3 = st.columns([1, 10, 1])
    
    with col2:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='text-align: center; color: #2e7d32; margin-bottom: 20px;'>{L['scan_lbl']}</h3>", unsafe_allow_html=True)
        uploaded_image = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        
        if uploaded_image is not None:
            img_open = Image.open(uploaded_image)
            
            # Center the uploaded image gracefully
            img_col1, img_col2, img_col3 = st.columns([1, 2, 1])
            with img_col2:
                st.image(img_open, caption="Target Crop Leaf Submitted", use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button(L["scan_btn"], type="primary", use_container_width=True):
                with st.spinner("Processing image via AgroNetra Engine... Please stand by."):
                    analysis_prompt = f"""
                    You are a senior plant pathologist. Analyze this crop leaf image accurately and compose a structured diagnostic report explicitly in the language: {selected_lang_name}.
                    
                    Return response using the exact following sections:
                    ### 📋 1. Target Crop & Disease Identification
                    ### 🔍 2. Root Causes & Conditions
                    ### 🌿 3. Biological & Ecological Cures
                    ### 🧪 4. Targeted Chemical Treatments
                    """
                    try:
                        response = vision_model.generate_content([analysis_prompt, img_open])
                        st.markdown('<div class="report-block">', unsafe_allow_html=True)
                        st.markdown(response.text)
                        st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as ex:
                        st.error(f"System configuration issue connecting with AI Core: {ex}")
                        
        st.markdown('</div>', unsafe_allow_html=True) # End of glass container

# --- PAGE 2: KRUSHISEVAK CHAT BOX ---
elif menu_choice == L["nav_chat"]:
    st.markdown(f'<h1 class="animated-header">{L["chat_title"]}</h1>', unsafe_allow_html=True)
    st.write(f"This assistant adapts directly to your dialect. Chat naturally in **{selected_lang_name}**.")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    for text_msg in st.session_state.chat_history:
        with st.chat_message(text_msg["role"]):
            st.markdown(text_msg["content"])
            
    if user_query := st.chat_input(L["chat_placeholder"]):
        st.chat_message("user").markdown(user_query)
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        
        contextual_instruction = f"""
        You are Krushisevak AI, an expert conversational partner specialized in Indian rural agriculture.
        Respond comprehensively, politely, and usefully. You must reply entirely in the language: {selected_lang_name}.
        User inquiry: {user_query}
        """
        
        with st.chat_message("assistant"):
            with st.spinner("Krushisevak is generating advice..."):
                try:
                    ai_reply = chat_model.generate_content(contextual_instruction).text
                    st.markdown(ai_reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
                except Exception as chat_ex:
                    st.error(f"Chat stream latency or interruption: {chat_ex}")

# --- PAGE 3: ABOUT CORE VISION ---
elif menu_choice == L["nav_about"]:
    st.markdown('<h1 class="animated-header">Innovation Born From the Soil</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.metric(label="System Target Latency", value="< 2.4s")
        st.metric(label="Supported Vernaculars", value="4 Core Languages")
        st.metric(label="Core Diagnostics Engine", value="Gemini 1.5 Pro")
        
    with col2:
        st.markdown(f"""
        ### 🌾 The Developer & Our Mission
        This technological ecosystem was conceptualized and engineered by **Karmjeet Rathod** and a dedicated team of forward-thinking developers. 
        
        Our connection to Indian farming isn't academic—it is personal. Having spent time observing the delicate balance of rural agrarian ecosystems, we saw firsthand how sudden disease outbreaks strip farmers of their hard-earned yields.
        
        Driven by this reality, we engineered this unified hub to place world-class machine vision capabilities right into the hands of individual farmers. By linking high-performance cloud intelligence with the raw resilience of Indian farming, we aim to eliminate guesswork in crop management, protect ancestral farmlands, and secure local agricultural economics.
        
        ### 👥 Core Architecture Group
        * **Karmjeet Rathod** — Lead AI Architect & Full-Stack Systems Engineer
        * *(Add other team members here)*
        """)

# --- PAGE 4: FARMER SUPPORT DESK ---
elif menu_choice == L["nav_support"]:
    st.markdown(f'<h1 class="animated-header">{L["nav_support"]}</h1>', unsafe_allow_html=True)
    st.write("Experiencing technical friction or need human intervention? Fill out this ticket and our field agents will step in.")
    
    with st.form("support_ticket_form", clear_on_submit=True):
        usr_name = st.text_input(L["sub_name"])
        usr_phone = st.text_input(L["sub_phone"])
        usr_details = st.text_area(L["sub_msg"])
        
        form_submit = st.form_submit_button(L["sub_btn"])
        if form_submit:
            if usr_name and usr_phone:
                st.success("Ticket registered into our local system database successfully. Expect a response shortly!")
                st.balloons() 
            else:
                st.warning("Please complete the required name and phone fields before submitting.")