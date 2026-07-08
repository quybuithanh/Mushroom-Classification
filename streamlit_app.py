import io
import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="Mushroom Classification Demo",
    page_icon="🍄",
    layout="wide",
)


if "api_base_url" not in st.session_state:
    st.session_state.api_base_url = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")


def call_api(method: str, path: str, json_body: dict | None = None, timeout: int = 15):
    url = st.session_state.api_base_url.rstrip("/") + path
    try:
        response = requests.request(method, url, json=json_body, timeout=timeout)
        if response.status_code >= 400:
            return False, f"Lỗi {response.status_code}: {response.text}"
        return True, response.json()
    except requests.exceptions.ConnectionError:
        return False, f"Không kết nối được tới API tại {url}. Kiểm tra lại server FastAPI đã chạy chưa."
    except requests.exceptions.Timeout:
        return False, "API phản hồi quá lâu (timeout)."
    except Exception as e:
        return False, f"Lỗi không xác định: {e}"

FIELD_OPTIONS = {
    "cap_shape": [("b", "Hình chuông"), ("c", "Hình nón"), ("f", "Phẳng"), ("k", "Có núm"), ("s", "Lõm"), ("x", "Lồi")],
    "cap_surface": [("f", "Dạng xơ"), ("g", "Có rãnh"), ("s", "Nhẵn"), ("y", "Có vảy")],
    "cap_color": [("b", "Vàng da bò"), ("c", "Quế"), ("e", "Đỏ"), ("g", "Xám"), ("n", "Nâu"), ("p", "Hồng"), ("r", "Xanh lá"), ("u", "Tím"), ("w", "Trắng"), ("y", "Vàng")],
    "bruises": [("f", "Không bầm"), ("t", "Có bầm")],
    "odor": [("a", "Hạnh nhân"), ("c", "Creosote"), ("f", "Hôi thối"), ("l", "Hồi"), ("m", "Mốc"), ("n", "Không mùi"), ("p", "Hăng"), ("s", "Cay"), ("y", "Tanh cá")],
    "gill_attachment": [("a", "Dính"), ("f", "Tự do")],
    "gill_spacing": [("c", "Khít"), ("w", "Dày đặc")],
    "gill_size": [("b", "Rộng"), ("n", "Hẹp")],
    "gill_color": [("b", "Vàng da bò"), ("e", "Đỏ"), ("g", "Xám"), ("h", "Nâu sô-cô-la"), ("k", "Đen"), ("n", "Nâu"), ("o", "Cam"), ("p", "Hồng"), ("r", "Xanh lá"), ("u", "Tím"), ("w", "Trắng"), ("y", "Vàng")],
    "stalk_shape": [("e", "Phình to"), ("t", "Thon nhỏ dần")],
    "stalk_root": [("b", "Phình củ"), ("c", "Hình chùy"), ("e", "Đều"), ("r", "Có rễ")],
    "stalk_surface_above_ring": [("f", "Dạng xơ"), ("k", "Mượt"), ("s", "Nhẵn"), ("y", "Có vảy")],
    "stalk_surface_below_ring": [("f", "Dạng xơ"), ("k", "Mượt"), ("s", "Nhẵn"), ("y", "Có vảy")],
    "stalk_color_above_ring": [("b", "Vàng da bò"), ("c", "Quế"), ("e", "Đỏ"), ("g", "Xám"), ("n", "Nâu"), ("o", "Cam"), ("p", "Hồng"), ("w", "Trắng"), ("y", "Vàng")],
    "stalk_color_below_ring": [("b", "Vàng da bò"), ("c", "Quế"), ("e", "Đỏ"), ("g", "Xám"), ("n", "Nâu"), ("o", "Cam"), ("p", "Hồng"), ("w", "Trắng"), ("y", "Vàng")],
    "veil_type": [("p", "Bán phần")],
    "veil_color": [("n", "Nâu"), ("o", "Cam"), ("w", "Trắng"), ("y", "Vàng")],
    "ring_number": [("n", "Không có"), ("o", "1 vòng"), ("t", "2 vòng")],
    "ring_type": [("e", "Dễ biến mất"), ("f", "Loe"), ("l", "To"), ("n", "Không có"), ("p", "Rủ xuống")],
    "spore_print_color": [("b", "Vàng da bò"), ("h", "Nâu sô-cô-la"), ("k", "Đen"), ("n", "Nâu"), ("o", "Cam"), ("r", "Xanh lá"), ("u", "Tím"), ("w", "Trắng"), ("y", "Vàng")],
    "population": [("a", "Rất nhiều"), ("c", "Mọc cụm"), ("n", "Nhiều"), ("s", "Rải rác"), ("v", "Vài"), ("y", "Đơn lẻ")],
    "habitat": [("d", "Rừng"), ("g", "Đồng cỏ"), ("l", "Lá cây"), ("m", "Đồng cỏ (meadow)"), ("p", "Đường mòn"), ("u", "Đô thị"), ("w", "Đất hoang")],
}

FIELD_LABELS_VI = {
    "cap_shape": "Hình dạng mũ", 
    "cap_surface": "Bề mặt mũ", 
    "cap_color": "Màu mũ",
    "bruises": "Vết bầm", 
    "odor": "Mùi", 
    "gill_attachment": "Cách gắn phiến",
    "gill_spacing": "Khoảng cách phiến", 
    "gill_size": "Kích thước phiến", 
    "gill_color": "Màu phiến",
    "stalk_shape": "Hình dạng cuống", 
    "stalk_root": "Gốc cuống",
    "stalk_surface_above_ring": "Bề mặt cuống (trên vòng)", 
    "stalk_surface_below_ring": "Bề mặt cuống (dưới vòng)",
    "stalk_color_above_ring": "Màu cuống (trên vòng)", 
    "stalk_color_below_ring": "Màu cuống (dưới vòng)",
    "veil_type": "Loại màng bao", 
    "veil_color": "Màu màng bao", 
    "ring_number": "Số vòng",
    "ring_type": "Loại vòng",
    "spore_print_color": "Màu bào tử in", 
    "population": "Mật độ mọc", 
    "habitat": "Môi trường sống",
}

FEATURES = list(FIELD_OPTIONS.keys())


def option_display(field, code):
    for c, label in FIELD_OPTIONS[field]:
        if c == code:
            return f"{c} - {label}"
    return code


def code_from_display(display_value: str) -> str:
    return display_value.split(" - ")[0]


DEFAULT_SAMPLE = {
    "cap_shape": "x",
    "cap_surface": "s", 
    "cap_color": "y", 
    "bruises": "t", 
    "odor": "a",
    "gill_attachment": "f", 
    "gill_spacing": "c", 
    "gill_size": "b", 
    "gill_color": "k",
    "stalk_shape": "e", 
    "stalk_root": "c", 
    "stalk_surface_above_ring": "s",
    "stalk_surface_below_ring": "s", 
    "stalk_color_above_ring": "w", 
    "stalk_color_below_ring": "w",
    "veil_type": "p", 
    "veil_color": "w", 
    "ring_number": "o", 
    "ring_type": "p",
    "spore_print_color": "n", 
    "population": "n", 
    "habitat": "g",
}

st.sidebar.title("Mushroom Demo")
st.session_state.api_base_url = st.sidebar.text_input(
    "Địa chỉ API", value=st.session_state.api_base_url,
    help="Địa chỉ FastAPI đang chạy, vd http://127.0.0.1:8000",
)

page = st.sidebar.radio(
    "Chọn màn hình",
    [
        "Trang chủ/Dashboard",
        "Dự đoán",
        "Thông tin model",
        "Lịch sử",
        "Dự đoán hàng loạt (Batch)",
    ],
)

ok_health, health_data = call_api("GET", "/health")
if ok_health:
    st.sidebar.success("API đang hoạt động")
else:
    st.sidebar.error("Không kết nối được API")
    st.sidebar.caption(str(health_data))

# Trang chủ / Dashboard

def render_home():
    st.title("Dashboard — Mushroom Classification")
    st.caption("Demo giao diện cho REST API phân loại nấm độc/ăn được.")

    ok, data = call_api("GET", "/history?limit=500")
    if not ok:
        st.warning(f"Chưa lấy được dữ liệu lịch sử: {data}")
        return

    if not data:
        st.info("Chưa có lần dự đoán nào được lưu. Hãy thử màn hình 'Dự đoán' trước.")
        return

    df = pd.DataFrame(data)
    total = len(df)
    n_edible = (df["prediction"] == "edible").sum()
    n_poison = (df["prediction"] == "poisonous").sum()
    avg_conf = df["confidence"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tổng số dự đoán", total)
    col2.metric("Ăn được (edible)", int(n_edible))
    col3.metric("Độc (poisonous)", int(n_poison))
    col4.metric("Độ tin cậy trung bình", f"{avg_conf * 100:.1f}%")

    st.subheader("Tỉ lệ edible / poisonous")
    dist = df["prediction"].value_counts()
    st.bar_chart(dist)

    st.subheader("5 lần dự đoán gần nhất")
    st.dataframe(df.head(5), use_container_width=True)

# Dự đoán

def render_predict():
    st.title("Dự đoán 1 mẫu nấm")

    with st.form("predict_form"):
        input_dict = {}
        cols = st.columns(3)
        for i, field in enumerate(FEATURES):
            col = cols[i % 3]
            options = [c for c, _ in FIELD_OPTIONS[field]]
            default_code = DEFAULT_SAMPLE[field]
            selected = col.selectbox(
                FIELD_LABELS_VI[field],
                options=options,
                index=options.index(default_code),
                format_func=lambda code, f=field: option_display(f, code),
                key=f"predict_{field}",
            )
            input_dict[field] = selected

        submitted = st.form_submit_button("Dự đoán", type="primary")

    if submitted:
        ok, result = call_api("POST", "/predict", input_dict)
        if not ok:
            st.error(result)
            return

        label = result["prediction"]
        confidence = result["confidence"]

        if label == "edible":
            st.success(f"Kết quả: ĂN ĐƯỢC (edible) — độ tin cậy {confidence * 100:.2f}%")
        else:
            st.error(f"Kết quả: ĐỘC (poisonous) — độ tin cậy {confidence * 100:.2f}%")

        prob_df = pd.DataFrame(
            {"Xác suất": result["probabilities"]}
        )
        st.bar_chart(prob_df)

# Thông tin model

def render_model_info():
    st.title("📊 Thông tin model")

    ok, info = call_api("GET", "/model-info")
    if not ok:
        st.error(info)
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Loại model", info["model_type"])
    col2.metric("Số cây (n_estimators)", info["n_estimators"])
    col3.metric("Số đặc trưng đầu vào", info["n_features"])

    col4, col5 = st.columns(2)
    col4.metric("Tiêu chí phân nhánh", info["criterion"])
    col5.metric("Random state", info["random_state"])

    st.write("**Các lớp phân loại:**", ", ".join(info["classes"]))

    st.subheader("Mức độ quan trọng của từng đặc trưng (feature importance)")
    fi = pd.Series(info["feature_importances"]).sort_values(ascending=False)
    st.bar_chart(fi.head(10))

    with st.expander("Xem toàn bộ 22 đặc trưng đầu vào"):
        st.write(info["features"])

# Lịch sử

def render_history():
    st.title("Lịch sử dự đoán")

    limit = st.slider("Số dòng muốn xem", min_value=5, max_value=200, value=20, step=5)
    filter_choice = st.selectbox("Lọc theo kết quả", ["Tất cả", "edible", "poisonous"])

    ok, data = call_api("GET", f"/history?limit={limit}")
    if not ok:
        st.error(data)
        return

    if not data:
        st.info("Chưa có lịch sử nào.")
        return

    df = pd.DataFrame(data)
    prob_df = pd.json_normalize(df["probabilities"]).add_prefix("prob_")
    df = pd.concat([df.drop(columns=["probabilities"]), prob_df], axis=1)

    if filter_choice != "Tất cả":
        df = df[df["prediction"] == filter_choice]

    st.dataframe(df, use_container_width=True)

    csv_bytes = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "⬇️ Xuất CSV",
        data=csv_bytes,
        file_name=f"history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )

# Dự đoán hàng loạt (batch) + xuất CSV

def render_batch():
    st.title("Dự đoán hàng loạt (Batch)")

    tab_manual, tab_csv = st.tabs(["Nhập tay", "Tải file CSV"])

    items = None

    with tab_manual:
        st.caption("Thêm/xóa dòng bằng nút + / - ở cuối bảng. Mỗi ô là 1 dropdown mã hợp lệ.")

        column_config = {}
        for field in FEATURES:
            display_options = [option_display(field, c) for c, _ in FIELD_OPTIONS[field]]
            column_config[field] = st.column_config.SelectboxColumn(
                FIELD_LABELS_VI[field], options=display_options, required=True,
            )

        default_row = {field: option_display(field, DEFAULT_SAMPLE[field]) for field in FEATURES}
        init_df = pd.DataFrame([default_row])

        edited_df = st.data_editor(
            init_df,
            column_config=column_config,
            num_rows="dynamic",
            use_container_width=True,
            key="batch_editor",
        )

        if st.button("Dự đoán hàng loạt (từ bảng nhập tay)", type="primary"):
            items = [
                {field: code_from_display(row[field]) for field in FEATURES}
                for _, row in edited_df.iterrows()
            ]

    with tab_csv:
        template_df = pd.DataFrame([DEFAULT_SAMPLE])
        st.download_button(
            "Tải file CSV mẫu",
            data=template_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="mushroom_batch_template.csv",
            mime="text/csv",
        )

        uploaded = st.file_uploader("Tải lên file CSV (đúng 22 cột mã, xem file mẫu ở trên)", type=["csv"])
        if uploaded is not None:
            csv_df = pd.read_csv(uploaded, dtype=str)
            missing = set(FEATURES) - set(csv_df.columns)
            if missing:
                st.error(f"File CSV thiếu các cột: {sorted(missing)}")
            else:
                st.dataframe(csv_df, use_container_width=True)
                if st.button("Dự đoán hàng loạt (từ file CSV)", type="primary"):
                    items = csv_df[FEATURES].to_dict(orient="records")

    if items:
        ok, result = call_api("POST", "/predict/batch", {"items": items})
        if not ok:
            st.error(result)
            return

        st.success(f"Đã dự đoán {result['count']} mẫu.")

        rows = []
        for r in result["results"]:
            row = dict(r["input"])
            row["prediction"] = r["prediction"]
            row["confidence"] = r["confidence"]
            row["prob_edible"] = r["probabilities"].get("edible")
            row["prob_poisonous"] = r["probabilities"].get("poisonous")
            rows.append(row)

        result_df = pd.DataFrame(rows)
        st.dataframe(result_df, use_container_width=True)

        csv_bytes = result_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "Xuất ra CSV",
            data=csv_bytes,
            file_name=f"batch_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )

# Điều hướng

if page =="Trang chủ/Dashboard":
    render_home()
elif page =="Dự đoán":
    render_predict()
elif page == "Thông tin model":
    render_model_info()
elif page == "Lịch sử":
    render_history()
elif page == "Dự đoán hàng loạt (Batch)":
    render_batch()