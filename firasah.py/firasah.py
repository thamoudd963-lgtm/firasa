import streamlit as st
import google.generativeai as genai
import re

# --- إعدادات الصفحة كاملة العرض ---
st.set_page_config(page_title="فِراسة AI", page_icon="👁️", layout="wide")

# --- التصميم الفخم (Gold & Dark) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title { font-family: 'Amiri', serif; font-size: 70px; color: #d4af37; text-align: center; margin-top: -50px; }
    .sub-title { text-align: center; color: #666; letter-spacing: 5px; font-size: 12px; margin-bottom: 40px; }
    .stTextArea textarea { background-color: #111 !important; color: #fff !important; border: 1px solid #333 !important; border-radius: 10px; font-size: 18px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #d4af37, #aa8a2e) !important; color: black !important; font-weight: bold !important; height: 55px; border-radius: 10px; border: none !important; font-size: 20px !important; }
    .result-box { background: #111; border-right: 5px solid #d4af37; padding: 25px; border-radius: 5px; direction: rtl; text-align: right; line-height: 1.8; font-size: 19px; }
    .stat-bar { height: 8px; background: #222; border-radius: 5px; margin-bottom: 20px; }
    .stat-fill { height: 100%; background: #d4af37; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- ربط الذكاء الاصطناعي ---
try:
    api_key = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("خطأ في المفتاح السري.")
    st.stop()

# --- الواجهة ---
st.markdown('<h1 class="main-title">فِراسة</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">DIGITAL PHYSIOGNOMY ENGINE</p>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 6, 1])
with c2:
    text = st.text_area("", placeholder="أدخل النص هنا للتحليل العميق...", height=200)
    if st.button("كشف النوايا بالذكاء الاصطناعي"):
        if text:
            with st.spinner("يتم الآن استنطاق الحروف..."):
                prompt = f"حلل هذا النص بأسلوب خبير فراسة: استخرج النوايا، والصدق، والتوتر، وقدم ردوداً (دبلوماسي، حازم، ودي) ونصيحة. النص: {text}"
                response = model.generate_content(prompt)
                
                st.write("---")
                st.markdown(f'<div class="result-box">{response.text}</div>', unsafe_allow_html=True)
        else:
            st.warning("الرجاء إدخال نص.")
