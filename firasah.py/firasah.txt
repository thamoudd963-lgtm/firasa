import streamlit as st
import google.generativeai as genai
import json

# --- 1. إعدادات الهوية البصرية (أبيض وأسود فخم) ---
st.set_page_config(page_title="فِراسة | Firasah", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"] { 
        font-family: 'Noto Sans Arabic', sans-serif; 
        text-align: right; 
        direction: rtl; 
    }
    .main { background-color: #ffffff; }
    h1, h2, h3, p, span, label { color: #000000 !important; }
    
    /* تصميم الأزرار */
    .stButton>button {
        background-color: #000000;
        color: #ffffff;
        border-radius: 8px;
        border: 2px solid #000000;
        width: 100%;
        height: 3.5em;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    /* تصميم صندوق النص */
    .stTextArea>div>div>textarea {
        background-color: #ffffff;
        color: #000000;
        border: 2px solid #000000;
        border-radius: 10px;
        font-size: 1.2rem;
    }

    /* صندوق التقرير */
    .report-box {
        border: 3px solid #000000;
        padding: 30px;
        border-radius: 15px;
        background-color: #ffffff;
        margin-top: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الربط الآمن مع "الخزنة" (Secrets) ---
# ملاحظة: عند تشغيل الكود على جهازك، سيطلب منك streamlit إنشاء ملف secrets.toml
# عند رفعه على الموقع، تضع المفتاح في إعدادات التطبيق (Advanced Settings)
try:
    API_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.warning("⚠️ نظام الحماية مفعل: يرجى إضافة GEMINI_KEY في إعدادات Secrets.")
    st.stop()

# --- 3. واجهة التطبيق الرئيسية ---
st.title("👁️ فِراسة")
st.write("أداة كشف النوايا وتحليل المشاعر العميقة | النسخة المحمية")

user_input = st.text_area("", placeholder="ألصق المحادثة هنا لنحلل ما وراء الكلمات...", height=150)

if st.button("تحليل الفِراسة"):
    if user_input:
        with st.spinner("جاري استحضار الفِراسة..."):
            try:
                # البرومبت الاحترافي لتحليل اللهجات
                prompt = f"""
                أنت خبير في علم الفراسة وتحليل سياق الكلام العربي واللهجات المحلية.
                حلل النص التالي بذكاء واستخرج المشاعر المبطنة:
                "{user_input}"
                
                يجب أن يكون الرد بتنسيق JSON فقط:
                {{
                  "seriousness": 0,
                  "tension": 0,
                  "friendliness": 0,
                  "evasion": 0,
                  "insight": "تحليل النية (بلهجة قوية وذكية)",
                  "recommendation": "الرد المقترح"
                }}
                النسب من 0 لـ 100.
                """
                
                response = model.generate_content(prompt)
                clean_response = response.text.strip().replace('```json', '').replace('```', '')
                data = json.loads(clean_response)
                
                # --- عرض النتائج ---
                st.markdown('<div class="report-box">', unsafe_allow_html=True)
                st.markdown("### 📊 نتائج تحليل فِراسة")
                
                cols = st.columns(4)
                cols[0].metric("الجدية", f"{data['seriousness']}%")
                cols[1].metric("التوتر", f"{data['tension']}%")
                cols[2].metric("الود", f"{data['friendliness']}%")
                cols[3].metric("التهرب", f"{data['evasion']}%")
                
                st.divider()
                st.subheader("🧠 تحليل النية")
                st.info(data['insight'])
                
                st.subheader("💡 نصيحة فِراسة للرد")
                st.success(data['recommendation'])
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error("حدث خطأ في الاتصال بالمحرك. تأكد من إعدادات الخزنة.")
    else:
        st.warning("أدخل نصاً أولاً.")

st.caption("تطبيق فِراسة - القوة في الفهم © 2026")
