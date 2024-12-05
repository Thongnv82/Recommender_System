import streamlit as st
import pandas as pd
import pickle

# Các Function:
def get_recommendations(df, ma_san_pham, cosine_sim, nums=5):
    # Get the index of the product that matches the ma_san_pham
    matching_indices = df.index[df['ma_san_pham'] == ma_san_pham].tolist()
    if not matching_indices:
        print(f"No product found with ID: {ma_san_pham}")
        return pd.DataFrame()  # Return an empty DataFrame if no match
    idx = matching_indices[0]

    # Get the pairwise similarity scores of all products with that product
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the products based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the nums most similar products (Ignoring the product itself)
    sim_scores = sim_scores[1:nums+1]

    # Get the product indices
    product_indices = [i[0] for i in sim_scores]

    # Return the top n most similar products as a DataFrame
    return df.iloc[product_indices]

# Hiển thị đề xuất ra bảng
def display_recommended_products(recommended_products, cols=5):
    for i in range(0, len(recommended_products), cols):
        cols = st.columns(cols)
        for j, col in enumerate(cols):
            if i + j < len(recommended_products):
                product = recommended_products.iloc[i + j]
                with col:   
                    st.write(product['ten_san_pham'])                    
                    expander = st.expander(f"Mô tả")
                    product_description = product['mo_ta']
                    truncated_description = ' '.join(product_description.split()[:100]) + '...'
                    expander.write(truncated_description)
                    expander.markdown("Nhấn vào mũi tên để đóng hộp text này.")           

# Đọc dữ liệu sản phẩm 1200 dòng
df_products = pd.read_csv('San_pham.csv')
# Lấy 10 sản phẩm
random_products = df_products.head(n=10)
# print(random_products)

# THIẾT KẾ SIDEBAR:

# Tạo menu
menu = ["Thông kê", "Đề xuất sản phẩm"]
# Hiển thị tiêu đề to hơn bằng Markdown
# st.sidebar.markdown("### <span style='font-size:20px;'>Lựa chọn</span>", unsafe_allow_html=True)

# Hiển thị selectbox
# choice = st.sidebar.selectbox("", menu)
# menu = ["Thông kê", "Đề xuất sản phẩm"]
choice = st.sidebar.selectbox("**Nguyễn Văn Thông**", menu)

# Giáo viên hướng dẫn:
st.sidebar.write("""#### Giảng viên hướng dẫn:
                    Khuất Thùy Phương""")
# st.sidebar.write("**Khuất Thùy Phương**")

# Ngày bảo vệ:
st.sidebar.write("""#### Thời gian bảo vệ: 
                 16/12/2024""")

# Hiển thị thông tin thành viên trong sidebar
st.sidebar.write("#### Thành viên thực hiện:")

# Thành viên 1: Nguyễn Văn Thông
st.sidebar.image("Thongnv.jpg", width=150)
st.sidebar.write("**Nguyễn Văn Thông**")

# Thành viên 2: Vũ Trần Ngọc Lan
st.sidebar.image("Lan.jpg", width=150)
st.sidebar.write("**Vũ Trần Ngọc Lan**")

###### Giao diện Streamlit ######
st.image('Hasaki_Pic.jpg', use_column_width=True)


# LỰA CHỌN PHÂN TÍCH:
if choice == 'Đề xuất sản phẩm':    
    st.subheader("PHÂN TÍCH & ĐỀ XUẤT SẢN PHẨM TƯƠNG TỰ")
    # LỤA CHỌN SẢN PHẨM:
    st.session_state.random_products = random_products

    # Open and read file to cosine_sim_new
    with open('Group_11_Sun_Cosine_Sim.pkl', 'rb') as f:
        cosine_sim_new = pickle.load(f)

    # Kiểm tra xem 'selected_ma_san_pham' đã có trong session_state hay chưa
    if 'selected_ma_san_pham' not in st.session_state:
        # Nếu chưa có, thiết lập giá trị mặc định là None hoặc ID sản phẩm đầu tiên
        st.session_state.selected_ma_san_pham = None

    # Theo cách cho người dùng chọn sản phẩm từ dropdown
    # Tạo một tuple cho mỗi sản phẩm, trong đó phần tử đầu là tên và phần tử thứ hai là ID
    product_options = [(row['ten_san_pham'], row['ma_san_pham']) for index, row in st.session_state.random_products.iterrows()]
    st.session_state.random_products
    # Tạo một dropdown với options là các tuple này
    selected_product = st.selectbox(
        "Chọn sản phẩm",
        options=product_options,
        format_func=lambda x: x[0]  # Hiển thị tên sản phẩm
    )
    # Display the selected product
    st.write("Bạn đã chọn:", selected_product)

    # Cập nhật session_state dựa trên lựa chọn hiện tại
    st.session_state.selected_ma_san_pham = selected_product[1]

    if st.session_state.selected_ma_san_pham:
        st.write("ma_san_pham: ", st.session_state.selected_ma_san_pham)
        # Hiển thị thông tin sản phẩm được chọn
        selected_product = df_products[df_products['ma_san_pham'] == st.session_state.selected_ma_san_pham]

        if not selected_product.empty:
            st.write('#### Bạn vừa chọn:')
            st.write('### ', selected_product['ten_san_pham'].values[0])

            product_description = selected_product['mo_ta'].values[0]
            truncated_description = ' '.join(product_description.split()[:100])
            st.write('##### Thông tin:')
            st.write(truncated_description, '...')

            st.write('##### Các sản phẩm liên quan:')
            recommendations = get_recommendations(df_products, st.session_state.selected_ma_san_pham, cosine_sim=cosine_sim_new, nums=3) 
            display_recommended_products(recommendations, cols=3)
        else:
            st.write(f"Không tìm thấy sản phẩm với ID: {st.session_state.selected_ma_san_pham}")

elif choice == 'Thông kê':
    st.subheader("NHỮNG THÔNG KÊ CƠ BẢN")
    # Sản phẩm bán theo năm:
    st.write("##### 1. Tổng sản phẩm bán theo năm")
    st.image("Sanpha_theo_nam.jpg", width=700)

    # Sản phẩm bán theo tháng:
    st.write("##### 2. Sản phẩm bán theo tháng")
    st.image("Sanpham_theo_thang.jpg", width=700)

    # Sản phẩm bán theo tháng:
    st.write("##### 3. Tổng số các sản phẩm khác nhau")
    st.image("Sanpham_Khacnhau.jpg", width=700)

    # Sản phẩm bán theo tháng:
    st.write("##### 4. Thông kê phần đánh giá của khách hàng")
    st.image("Khachhang_Danhgia.jpg", width=700)


# streamlit run content_based_app.py

