import streamlit as st
import google.generativeai as genai
import re

# --- إعدادات الواجهة (الاستايل الفخم المستوحى من React) ---
st.set_page_config(page_title="فِراسة AI", page_icon="👁️", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Playfair+Display:wght@700&family=Courier+Prime:wght@400;700&display=swap');
    .main { background-color: #f5f5f3; color: #111; }
    .bar-container { margin-bottom: 20px; direction: rtl; }
    .bar-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 7px; }
    .bar-label { font-family: 'Amiri', serif; font-size: 16px; font-weight: 700; color: #111; }
    .bar-value { font-family: 'Courier Prime', monospace; font-size: 13px; font-weight: 700; color: #111; }
    .bar-bg { height: 4px; background: #ebebeb; position: relative; overflow: hidden; }
    .bar-fill { height: 100%; background: #111; transition: width 1.3s ease; }
    .card { background: white; border: 1.5px solid #e8e8e8; padding: 22px; margin-bottom: 12px; direction: rtl; text-align: right; border-radius: 4px; }
    .card-dark { background: #111 !important; border: 1.5px solid #111; color: #ccc !important; }
    .card-type { font-family: 'Courier Prime', monospace; font-size: 10px; letter-spacing: 2px; color: #999; margin-bottom: 10px; text-transform: uppercase; }
    .header-box { background: #111; color: white; padding: 60px 20px; text-align: center; margin-bottom: 40px; }
    </style>
    """, unsafe_allow_html=True)

# --- وظيفة معالجة الرد (Parser) ---
def parse_firasah_response(text):
    data = {"traits": [], "hidden": "", "replies": [], "advice": ""}
    traits = re.findall(r"([^:\n*]+):\s*(\d+)%", text)
    for label, val in traits:
        clean_label = label.replace("*", "").strip()
        data["traits"].append({"label": clean_label, "value": int(val)})
    hidden_match = re.search(r"قراءة ما بين السطور[\s\S]*?(?=الرد|$)", text)
    if hidden_match: data["hidden"] = hidden_match.group(0).replace("**", "").strip()
    dip = re.search(r"الرد الدبلوماسي[^:]*:([\s\S]*?)(?=الرد الحازم|$)", text)
    firm = re.search(r"الرد الحازم[^:]*:([\s\S]*?)(?=الرد الودي|$)", text)
    friend = re.search(r"الرد الودي[^:]*:([\s\S]*?)(?=نصيحة|$)", text)
    if dip: data["replies"].append({"type": "دبلوماسي", "icon": "🤝", "content": dip.group(1).strip(), "dark": False})
    if firm: data["replies"].append({"type": "حازم", "icon": "⚡", "content": firm.group(1).strip(), "dark": True})
    if friend: data["replies"].append({"type": "ودّي", "icon": "✨", "content": friend.group(1).strip(), "dark": False})
    adv = re.search(r"نصيحة[\s\S]*?الذهبية[^:]*:([\s\S]*?)(?=$)", text)
    if adv: data["advice"] = adv.group(1).strip()
    return data

# --- الربط بالمفتاح ---
try:
    api_key = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("تأكد من ضبط مفتاح الخزنة (GEMINI_KEY) في Settings > Secrets.")
    st.stop()

# --- واجهة المستخدم ---
st.markdown("""
<div class="header-box">
    <h1 style="font-family: 'Playfair Display', serif; font-size: 55px; margin:0; color: white;">فِراسة <span style="color: #555; font-style: italic;">AI</span></h1>
    <p style="font-family: 'Courier Prime', monospace; font-size: 10px; letter-spacing: 5px; color: #555;">DIGITAL PHYSIOGNOMY ENGINE v2.0</p>
</div>
""", unsafe_allow_html=True)

user_input = st.text_area("النص المراد تحليله", height=150, placeholder="الصق هنا النص...")

if st.button("ابدأ تحليل الفِراسة ←"):
    if user_input:
        with st.spinner("جاري كشف النوايا..."):
            prompt = f"أنت كبير خبراء الفِراسة. حلل النص التالي وقدم تقريراً يشمل: 1- السمات بنسب مئوية (الصدق، الثقة، التوتر، العقلانية). 2- قراءة ما بين السطور. 3- الرد الدبلوماسي، الرد الحازم، الرد الودي. 4- نصيحة الفراسة الذهبية. النص: {user_input}"
            response = model.generate_content(prompt)
            data = parse_firasah_response(response.text)
            st.write("---")
            if data["traits"]:
                st.markdown("### 01 السمات الشخصية")
                for t in data["traits"]:
                    st.markdown(f'<div class="bar-container"><div class="bar-header"><span class="bar-label">{t["label"]}</span><span class="bar-value">{t["value"]}%</span></div><div class="bar-bg"><div class="bar-fill" style="width: {t["value"]}%"></div></div></div>', unsafe_allow_html=True)
            if data["hidden"]:
                st.markdown("### 02 قراءة ما بين السطور")
                st.markdown(f'<div class="card">{data["hidden"]}</div>', unsafe_allow_html=True)
            if data["replies"]:
                st.markdown("### 03 اقتراحات الرد الذكي")
                for r in data["replies"]:
                    cls = "card card-dark" if r["dark"] else "card"
                    st.markdown(f'<div class="{cls}"><div class="card-type">{r["icon"]} {r["type"]}</div><div style="font-family: Amiri; font-size: 17px;">{r["content"]}</div></div>', unsafe_allow_html=True)
            if data["advice"]:
                st.markdown('### 04 نصيحة "الفِراسة" الذهبية')
                st.markdown(f'<div style="background: #111; padding: 30px; color: #ccc; direction: rtl; text-align: right; font-style: italic; border-right: 4px solid white;">"{data["advice"]}"</div>', unsafe_allow_html=True)
    else:
        st.warning("يرجى إدخال نص.")
