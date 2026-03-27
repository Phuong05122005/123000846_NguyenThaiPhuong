# app.py
import streamlit as st
from underthesea import word_tokenize, pos_tag

st.set_page_config(page_title="Demo POS Tagging Tiếng Việt", layout="wide")

st.title("Demo POS Tagging Tiếng Việt với Streamlit")
st.write("Nhập một câu tiếng Việt, ứng dụng sẽ tách từ và gán nhãn từ loại.")

# Input
text = st.text_area(
    "Nhập câu tiếng Việt ở đây:",
    "Hệ thống phân loại bình luận tiếng Việt rất chính xác.",
    height=100
)

analyze_clicked = st.button("🔍 Phân tích", type="primary", width="stretch")

col1, col2 = st.columns(2)

import pandas as pd
import base64
import io

# Bảng giải thích nhãn từ loại
POS_TAGS_EXPLANATION = {
    "N": "Danh từ",
    "Np": "Danh từ riêng",
    "Nc": "Danh từ chỉ loại",
    "Nu": "Danh từ đơn vị",
    "V": "Động từ",
    "A": "Tính từ",
    "P": "Đại từ",
    "R": "Phó từ",
    "L": "Định từ",
    "M": "Số từ",
    "E": "Giới từ",
    "C": "Liên từ",
    "I": "Thán từ",
    "T": "Trợ từ, tiểu từ",
    "B": "Từ gốc Hán-Việt",
    "Y": "Từ viết tắt",
    "S": "Từ ngoại lai",
    "X": "Từ không phân loại",
    "CH": "Dấu câu",
}

# Màu cho từng loại từ loại (điều chỉnh để tương phản tốt hơn)
POS_COLORS = {
    "N": "#E74C3C",   # Đỏ đậm
    "Np": "#C0392B",  # Đỏ tối
    "Nc": "#EC7063",  # Đỏ nhạt
    "Nu": "#F1948A",  # Hồng đỏ
    "V": "#27AE60",   # Xanh lá đậm
    "A": "#F1C40F",   # Vàng
    "P": "#16A085",   # Xanh ngọc
    "R": "#1ABC9C",   # Xanh ngọc nhạt
    "L": "#9B59B6",   # Tím
    "M": "#3498DB",   # Xanh dương
    "E": "#E67E22",   # Cam
    "C": "#2ECC71",   # Xanh lá nhạt
    "I": "#F39C12",   # Cam vàng
    "T": "#8E44AD",   # Tím đậm
    "B": "#D35400",   # Cam đậm
    "Y": "#5DADE2",   # Xanh dương nhạt
    "S": "#EC7063",   # Đỏ hồng
    "X": "#95A5A6",   # Xám
    "CH": "#BDC3C7",  # Xám nhạt
}

# TODO: Thêm xử lý tokenize và hiển thị kết quả ở col1
# TODO: Thêm xử lý POS tagging và hiển thị kết quả ở col2
# TODO: Thêm bảng giải thích các nhãn từ loại (POS tags)
# TODO: Thêm xử lý lỗi khi input rỗng
# TODO: Thêm tính năng export kết quả ra file CSV
# TODO: Thêm highlight màu cho từng loại từ loại khác nhau

# Lưu kết quả vào session_state để không mất khi rerun
if analyze_clicked:
    if not text.strip():
        st.error("⚠️ Vui lòng nhập nội dung!")
        st.session_state.pop("pos_result", None)
    else:
        st.session_state["pos_text"] = text
        st.session_state["pos_tokens"] = word_tokenize(text)
        st.session_state["pos_result"] = pos_tag(text)
        
if "pos_result" in st.session_state:
    pos_result = st.session_state["pos_result"]
    tokens = st.session_state["pos_tokens"]
    
    with col1:
        st.subheader("🔤 Tách từ (Tokenize)")
        st.write("Các từ được tách từ câu:")
        st.code(" | ".join(tokens), language="text")
    
    with col2:
        st.subheader("🏷️ Gán nhãn từ loại (POS Tagging)")
        st.write("Mỗi từ được gán nhãn từ loại với màu tương ứng:")
        
        # Tạo HTML để highlight màu
        highlighted_text = ""
        for word, tag in pos_result:
            color = POS_COLORS.get(tag, "#000000")  # Mặc định đen nếu không có màu
            highlighted_text += f'<span style="background-color: {color}; padding: 2px 4px; margin: 1px; border-radius: 3px; color: white; font-weight: bold;">{word} ({tag})</span> '
        
        st.markdown(highlighted_text, unsafe_allow_html=True)
    
    # Bảng giải thích nhãn từ loại
    st.subheader("📖 Bảng giải thích nhãn từ loại")
    pos_df = pd.DataFrame(list(POS_TAGS_EXPLANATION.items()), columns=["Nhãn", "Giải thích"])
    st.dataframe(pos_df, use_container_width=True)
    
    # Tính năng export kết quả ra file CSV
    st.subheader("⬇️ Xuất kết quả ra CSV")
    
    # Tạo DataFrame từ pos_result
    df_export = pd.DataFrame(pos_result, columns=["Từ", "Nhãn từ loại"])
    df_export["Giải thích nhãn"] = df_export["Nhãn từ loại"].map(POS_TAGS_EXPLANATION)
    
    # Xuất CSV với encoding UTF-8 BOM để hỗ trợ tiếng Việt trong Excel
    csv_data = df_export.to_csv(index=False, encoding="utf-8-sig")
    
    st.download_button(
        label="⬇️ Tải về kết quả POS Tagging (CSV)",
        data=csv_data,
        file_name="pos_tagging_result.csv",
        mime="text/csv",
        help="Mở bằng Excel: File → Import → chọn UTF-8 hoặc mở trực tiếp"
    )