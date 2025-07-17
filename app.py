import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("lookup_d1_2025.csv")

df = load_data()

st.title("🎯 Tra cứu thứ hạng điểm thi 2025 - Khối D1")
st.markdown("Nhập điểm bạn đạt được để biết mình đang ở đâu trong bảng xếp hạng toàn quốc.")

diem_input = st.number_input("Nhập tổng điểm khối D1 (từ 0 đến 30)", min_value=0.0, max_value=30.0, step=0.05)

if st.button("Tra cứu"):
    df_sorted = df.sort_values(by="diem_moc", ascending=True)
    matched_rows = df_sorted[df_sorted["diem_moc"] <= diem_input]

    if matched_rows.empty:
        st.warning("Không tìm thấy dữ liệu phù hợp. Có thể điểm quá thấp.")
    else:
        row = matched_rows.iloc[-1]
        st.success(f"✅ Bạn đạt {diem_input} điểm")
        st.markdown(f"""
        - 📊 **Top {row['top_percent']:.2f}% cao nhất toàn quốc**
        - 🏆 **Vượt qua {row['higher_than_count']:,} thí sinh**
        - 👥 **Còn lại {row['count_greater_equal']:,} thí sinh bằng hoặc cao hơn bạn**
        """)

