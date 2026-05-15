cols = st.columns(2)
                    for i, (label, val) in enumerate(traits):
                        with cols[i % 2]:
                            st.markdown(f"""
                            <div class="bar-container">
                                <div class="bar-label">{label.strip()} ({val}%)</div>
                                <div class="bar-bg"><div class="bar-fill" style="width: {val}%"></div></div>
                            </div>
                            """, unsafe_allow_html=True)

                st.write("---")
                
                # عرض التحليل والردود
                st.subheader("👁️ النتائج العميقة")
                st.markdown(f'<div class="result-card">{res_text}</div>', unsafe_allow_html=True)
        else:
            st.warning("يرجى إدخال نص أولاً.")

st.markdown("<br><center style='color:#333'>فِراسة AI © 2026</center>", unsafe_allow_html=True)
