import streamlit as st
import math

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Ứng dụng tính lãi tiền gửi tiết kiệm")
st.write("Nhập thông tin tiền gửi để tính tiền lãi và tổng số tiền nhận được.")

# =========================
# NHẬP DỮ LIỆU
# =========================

st.subheader("📌 Thông tin tiền gửi")

# Số tiền gửi
tien_gui = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

# Kỳ hạn
ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=1200,
    value=12,
    step=1
)

# Lãi suất
lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1
)

# Hình thức nhận lãi
hinh_thuc_nhan_lai = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)

# Loại lãi
loai_lai = st.radio(
    "Phương pháp tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ],
    horizontal=True
)

# =========================
# TÍNH TOÁN
# =========================

if st.button("🧮 Tính lãi", use_container_width=True):

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    # Chuyển đổi
    lai_suat_nam = lai_suat / 100
    so_thang = ky_han

    # =========================
    # LÃI ĐƠN
    # =========================
    if loai_lai == "Lãi đơn":

        # Tổng lãi trong toàn bộ kỳ hạn
        tong_lai = tien_gui * lai_suat_nam * (so_thang / 12)

        # Số kỳ nhận lãi
        if hinh_thuc_nhan_lai == "Cuối kỳ":
            so_ky = 1
        elif hinh_thuc_nhan_lai == "Hàng tháng":
            so_ky = so_thang
        else:
            so_ky = math.ceil(so_thang / 3)

        # Lãi mỗi kỳ
        lai_dinh_ky = tong_lai / so_ky

        # Tổng tiền cuối cùng
        tong_tien = tien_gui + tong_lai

    # =========================
    # LÃI KÉP
    # =========================
    else:

        if hinh_thuc_nhan_lai == "Cuối kỳ":
            # Toàn bộ tiền lãi nhập gốc vào cuối kỳ
            so_ky = 1
            lai_dinh_ky = tien_gui * (
                (1 + lai_suat_nam) ** (so_thang / 12) - 1
            )
            tong_lai = lai_dinh_ky
            tong_tien = tien_gui + tong_lai

        elif hinh_thuc_nhan_lai == "Hàng tháng":
            # Lãi suất theo tháng
            lai_suat_thang = lai_suat_nam / 12

            so_ky = so_thang

            tong_tien = tien_gui * (
                (1 + lai_suat_thang) ** so_thang
            )

            tong_lai = tong_tien - tien_gui

            # Lãi của kỳ đầu tiên
            lai_dinh_ky = tien_gui * lai_suat_thang

        else:
            # Lãi kép hàng quý
            lai_suat_quy = lai_suat_nam / 4

            so_quy = so_thang // 3
            thang_le = so_thang % 3

            # Phần kỳ hạn đủ quý
            tong_tien = tien_gui * (
                (1 + lai_suat_quy) ** so_quy
            )

            # Nếu còn tháng lẻ thì tính thêm phần lãi theo tháng
            if thang_le > 0:
                tong_tien *= (
                    1 + lai_suat_nam * thang_le / 12
                )

            tong_lai = tong_tien - tien_gui

            so_ky = math.ceil(so_thang / 3)

            # Lãi quý đầu tiên
            lai_dinh_ky = tien_gui * lai_suat_quy

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================

    st.divider()
    st.subheader("📊 Kết quả")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            f"{lai_dinh_ky:,.0f} VNĐ"
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            f"{tong_lai:,.0f} VNĐ"
        )

    st.metric(
        "💰 Tổng tiền gốc + lãi",
        f"{tong_tien:,.0f} VNĐ"
    )

    # =========================
    # CHI TIẾT
    # =========================

    st.divider()
    st.subheader("📋 Chi tiết khoản gửi")

    st.write(f"**Số tiền gửi:** {tien_gui:,.0f} VNĐ")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc_nhan_lai}")
    st.write(f"**Phương pháp:** {loai_lai}")

    if hinh_thuc_nhan_lai == "Hàng tháng":
        st.info(
            f"Bạn nhận khoảng **{lai_dinh_ky:,.0f} VNĐ tiền lãi mỗi tháng** "
            f"theo cách tính đã chọn."
        )

    elif hinh_thuc_nhan_lai == "Hàng quý":
        st.info(
            f"Bạn nhận khoảng **{lai_dinh_ky:,.0f} VNĐ tiền lãi mỗi quý** "
            f"theo cách tính đã chọn."
        )

    else:
        st.info(
            f"Đến cuối kỳ, bạn nhận tổng cộng "
            f"**{tong_tien:,.0f} VNĐ**."
        )

# =========================
# GHI CHÚ
# =========================

st.divider()

with st.expander("ℹ️ Lưu ý về cách tính"):
    st.write(
        """
        - **Lãi đơn:** tiền lãi được tính dựa trên số tiền gốc ban đầu.
        - **Lãi kép:** tiền lãi được cộng vào vốn để tiếp tục tính lãi cho các kỳ sau.
        - Lãi suất được nhập theo **%/năm**.
        - Kỳ hạn được nhập theo **tháng**.
        - Đây là công cụ tính toán tham khảo; cách tính thực tế của ngân hàng
          có thể khác do quy định về số ngày thực gửi, ngày trả lãi và phương thức
          nhập lãi vào gốc.
        """
    )
