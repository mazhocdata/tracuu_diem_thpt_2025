import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# Page config
st.set_page_config(
    page_title="Tra cứu điểm thi 2025",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI with League Spartan font
st.markdown("""
<style>
    /* Import Google Fonts - League Spartan */
    @import url('https://fonts.googleapis.com/css2?family=League+Spartan:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'League Spartan', sans-serif;
    }
    
    /* Info Header Styles */
    .info-header {
        padding: 0.8rem 0;
        margin-bottom: 1rem;
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .info-header a {
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.3s ease;
    }
    
    .info-header a:hover {
        color: #764ba2;
        text-decoration: underline;
    }
    
    .author-name {
        color: #667eea;
        font-weight: 700;
    }
    
    .company-name {
        color: #764ba2;
        font-weight: 700;
    }

    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        font-size: 1.1rem;
        font-weight: 400;
        margin-top: 0.5rem;
        opacity: 0.9;
    }
    
    /* Card Styles */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-title {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.5rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #333;
        margin: 0;
    }
    
    .metric-delta {
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Results Section */
    .results-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    .region-header {
        display: flex;
        flex-direction: column;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f0f0f0;
    }
    
    .region-title-row {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .region-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
        color: #333;
    }
    
    .region-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #333 !important;
        margin: 0;
    }
    
    .region-subtext {
        font-size: 0.9rem;
        color: #666;
        font-style: italic;
        margin-left: 2rem;
        opacity: 0.8;
    }
    
    /* Input Styles */
    .stSelectbox > div > div > div {
        background: white;
        border-radius: 10px;
        font-family: 'League Spartan', sans-serif;
        color: #333 !important;
    }
    
    .stSelectbox > div > div > div > div {
        color: #333 !important;
    }
    
    .stSelectbox label {
        color: #333 !important;
    }
    
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e9ecef;
        transition: border-color 0.3s ease;
        font-family: 'League Spartan', sans-serif;
        color: #333 !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stNumberInput label {
        color: #333 !important;
    }
    
    /* Hide number input +/- buttons */
    .stNumberInput > div > div > button {
        display: none !important;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        font-family: 'League Spartan', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Hide Streamlit elements */
    [data-testid="stToolbar"] {
        display: none !important;
    }
    
    .stAppDeployButton {
        display: none !important;
    }
    
    [data-testid="stDecoration"] {
        display: none !important;
    }
    
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    footer {
        display: none !important;
    }
    
    .viewerBadge_container__1QSob {
        display: none !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .metric-card {
            margin: 0.5rem 0;
            padding: 1rem;
        }
        
        .results-container {
            padding: 1rem;
        }
        
        .region-title {
            color: #333 !important;
            font-size: 1.3rem;
        }
        
        .region-header {
            background: rgba(0,0,0,0.05);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        
        .region-subtext {
            margin-left: 0;
            font-size: 0.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load data for calculations (metrics, rankings)"""
    return pd.read_csv("lookup_2025_18_7.csv")

@st.cache_data
def load_histogram_data():
    """Load data specifically for histogram visualization"""
    return pd.read_csv("lookup_2025_18_7_histogram.csv")

@st.cache_data
def load_top_2024_data():
    """Load data for 2024 top percentage thresholds"""
    return pd.read_csv("lookup_2025_18_7_top_2024.csv")

def create_animated_metric_card(title, value, delta=None, icon="📊"):
    delta_html = f'<div class="metric-delta" style="color: #28a745;">▲ {delta}</div>' if delta else ""
    
    return f"""
    <div class="metric-card fade-in">
        <div class="metric-title">{icon} {title}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """

def get_2024_top_percentage(df_2024, khoi_input, region, diem_input):
    """Tìm top % tương ứng với điểm user nếu thi năm 2024"""
    # Filter data cho view và khối
    df_region_2024 = df_2024[df_2024['View'] == region].copy()
    
    if khoi_input not in df_region_2024.columns:
        return None
    
    # Sắp xếp theo Top % tăng dần
    df_region_2024 = df_region_2024.sort_values('Top %')
    
    # Tìm top % mà user đạt được (điểm user >= điểm ngưỡng)
    eligible_rows = df_region_2024[df_region_2024[khoi_input] <= diem_input]
    
    if eligible_rows.empty:
        # Điểm quá thấp, không lọt top nào
        return {"top_percent": ">100", "threshold_score": None}
    
    # Lấy top % tốt nhất (nhỏ nhất) mà user đạt được
    best_top_percent = eligible_rows['Top %'].iloc[0]
    threshold_score = eligible_rows[khoi_input].iloc[0]
    
    return {
        "top_percent": f"{best_top_percent}%",
        "threshold_score": threshold_score
    }

def create_region_histogram(df_histogram, khoi_input, region, diem_input):
    """Tạo histogram cho từng vùng miền với highlight cho điểm >= user score"""
    df_region = df_histogram[(df_histogram['khoi'] == khoi_input) & (df_histogram['view'] == region)].copy()
    df_region = df_region.sort_values('diem_moc')
    
    # Color mapping for each region
    region_colors = {
        'Cả nước': '#667eea',
        'Miền Bắc': '#f093fb', 
        'Miền Nam': '#4facfe'
    }
    
    region_color = region_colors.get(region, '#667eea')
    
    # Create color array based on user score
    colors = []
    opacities = []
    
    for score in df_region['diem_moc']:
        if score >= diem_input:
            # Keep original region color for scores >= user score
            colors.append(region_color)
            opacities.append(0.8)
        else:
            # Light gray for scores < user score
            colors.append('#d6d8db')  # Very light gray for scores < user score
            opacities.append(0.4)
    
    fig = go.Figure()
    
    # Add histogram bars with conditional coloring
    fig.add_trace(
        go.Bar(
            x=df_region['diem_moc'],
            y=df_region['count_exact'],
            name=f'Số thí sinh đạt điểm này',
            marker=dict(
                color=colors,
                opacity=opacities,
                line=dict(width=0.5, color='white')
            ),
            hovertemplate=(
                '<b>Điểm:</b> %{x}<br>' +
                '<b>Số thí sinh:</b> %{y:,.0f}<br>' +
                f'<b>Vùng:</b> {region}<br>' +
                '<b>Trạng thái:</b> %{customdata}<br>' +
                '<extra></extra>'
            ),
            customdata=[
                'Cao hơn/bằng điểm của bạn' if score >= diem_input 
                else 'Thấp hơn điểm của bạn' 
                for score in df_region['diem_moc']
            ]
        )
    )
    
    # Add user point with enhanced styling
    user_data = df_region[df_region['diem_moc'] == diem_input]
    if not user_data.empty:
        fig.add_trace(
            go.Scatter(
                x=[diem_input],
                y=[user_data['count_exact'].values[0]],
                mode='markers+text',
                marker=dict(
                    size=20, 
                    color='#dc3545',  # Red for user point
                    symbol='star',
                    line=dict(width=3, color='white')
                ),
                text=['ĐIỂM CỦA BẠN'],
                textposition='top center',
                textfont=dict(
                    size=10,  # Smaller text for mobile
                    color='#dc3545',
                    family='League Spartan'
                ),
                name='Điểm của bạn',
                hovertemplate=(
                    '<b>🎯 Điểm của bạn:</b> %{x}<br>' +
                    '<b>👥 Số thí sinh cùng điểm:</b> %{y:,.0f}<br>' +
                    '<extra></extra>'
                )
            )
        )
    
    # Add vertical line at user score for better visibility
    fig.add_vline(
        x=diem_input,
        line_dash="dash",
        line_color="#dc3545",
        line_width=2,
        opacity=0.7,
        annotation_text=f"Điểm: {diem_input}",  # Shorter annotation for mobile
        annotation_position="top",
        annotation_font_size=10
    )
    
    # Mobile-optimized layout
    fig.update_layout(
        title=dict(
            text=f"Phổ điểm thi - Khối {khoi_input} ({region})",  # Removed subtitle
            font=dict(family="League Spartan", size=14)  # Smaller title for mobile
        ),
        xaxis_title="Tổng điểm",
        yaxis_title="Số thí sinh",
        height=350,  # Reduced height for mobile
        showlegend=False,  # Hide legend on mobile for cleaner look
        font=dict(family="League Spartan", size=10),  # Smaller font
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='closest',
        margin=dict(t=60, b=40, l=40, r=20),  # Optimized margins for mobile
        xaxis=dict(
            showspikes=True,
            spikecolor="red",
            spikethickness=1,
            spikedash="dot"
        )
    )
    
    fig.update_xaxes(
        gridcolor='rgba(128,128,128,0.2)',
        title_font=dict(family="League Spartan", size=12),
        showgrid=False,
        zeroline=False,
        dtick=5,
        tick0=0,
        tickmode='linear'
    )
    fig.update_yaxes(
        gridcolor='rgba(128,128,128,0.2)',
        title_font=dict(family="League Spartan", size=12),
        showgrid=False,
        zeroline=False
    )
    
    return fig

def create_score_breakdown_table(df, khoi_input, region):
    """Tạo bảng thống kê phân bổ điểm theo các mốc quan trọng"""
    df_region = df[(df['khoi'] == khoi_input) & (df['view'] == region)].copy()
    df_region = df_region.sort_values('diem_moc', ascending=False)
    total = df_region['count_exact'].sum()
    
    # Định nghĩa các mốc điểm chi tiết
    score_thresholds = [29.0, 28.0, 27.0, 26.0, 25.0, 24.0, 23.0, 22.0, 21.0, 20.0, 19.0, 18.0, 17.0]
    
    breakdown_data = []
    
    # Xử lý các mốc >= 17
    for threshold in score_thresholds:
        label = f"{int(threshold)}+"
        
        # Tìm row có điểm chính xác bằng threshold
        exact_row = df_region[df_region['diem_moc'] == threshold]
        
        if not exact_row.empty:
            # Sử dụng data có sẵn từ file
            student_count = exact_row['count_greater_equal'].values[0]
            percentage = exact_row['top_percent'].values[0]
        else:
            # Nếu không có điểm chính xác, tìm điểm gần nhất >= threshold
            filtered_df = df_region[df_region['diem_moc'] >= threshold]
            if not filtered_df.empty:
                closest_row = filtered_df.iloc[-1]  # Lấy điểm nhỏ nhất >= threshold
                student_count = closest_row['count_greater_equal']
                percentage = closest_row['top_percent']
            else:
                student_count = 0
                percentage = 0.0
        
        breakdown_data.append({
            'Tổng điểm': label,
            'Số thí sinh': f"{student_count:,}",
            'Thứ hạng theo %': f"{percentage:.1f}%"
        })
    
    # Xử lý mốc <17
    filtered_df_below_17 = df_region[df_region['diem_moc'] < 17.0]
    student_count_below_17 = filtered_df_below_17['count_exact'].sum()
    percentage_below_17 = (student_count_below_17 / total * 100) if total > 0 else 0
    
    breakdown_data.append({
        'Tổng điểm': '<17',
        'Số thí sinh': f"{student_count_below_17:,}",
        'Thứ hạng theo %': f"{percentage_below_17:.1f}%"
    })
    
    # Thêm dòng Total
    breakdown_data.append({
        'Tổng điểm': 'Total',
        'Số thí sinh': f"{total:,}",
        'Thứ hạng theo %': '100.0%'
    })
    
    return pd.DataFrame(breakdown_data)

def display_score_breakdown_section(df, khoi_input, region, diem_input, user_result):
    """Hiển thị section thống kê phân bổ điểm"""
    
    st.markdown("""
    <div style="margin-top: 2rem;">
        <h4 style="color: #333; margin-bottom: 1rem;">📊 Bảng so sánh chi tiết các mốc điểm:</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Chỉ hiển thị note cho vùng "Cả nước" với data thực tế của user
    if region == "Cả nước" and user_result:
        # Tính toán dynamic values
        user_score = diem_input
        user_rank = user_result['rank']
        
        # Lấy số thí sinh ở mốc điểm của user
        df_region = df[(df['khoi'] == khoi_input) & (df['view'] == region)].copy()
        user_score_int = int(user_score) if user_score == int(user_score) else user_score
        
        # Tìm mốc điểm tương ứng trong bảng
        exact_row = df_region[df_region['diem_moc'] == user_score]
        if not exact_row.empty:
            students_at_threshold = exact_row['count_greater_equal'].values[0]
        else:
            # Tìm mốc gần nhất
            threshold = int(user_score) if user_score >= int(user_score) else int(user_score) + 1
            threshold_row = df_region[df_region['diem_moc'] == threshold]
            students_at_threshold = threshold_row['count_greater_equal'].values[0] if not threshold_row.empty else 0
        
        # Tính số thí sinh cùng điểm
        students_same_score = students_at_threshold - user_rank + 1
        
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #17a2b8; margin-bottom: 1rem;">
            <p style="color: #666; font-size: 0.9rem; margin: 0;">
                <strong>💡 Lưu ý:</strong><br>
                • <strong>Thứ hạng trên metrics</strong>: Vị trí cụ thể của bạn trong danh sách xếp hạng<br>
                • <strong>Số thí sinh trong bảng</strong>: Tổng số thí sinh đạt mốc điểm đó trở lên (≥)<br>
                • <strong>Ví dụ với điểm của bạn</strong>: Bạn có thứ hạng {user_rank:,} và mốc {user_score_int}+ có {students_at_threshold:,} thí sinh, 
                nghĩa là có {students_same_score:,} thí sinh cùng điểm {user_score} với bạn
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tạo bảng breakdown
    breakdown_df = create_score_breakdown_table(df, khoi_input, region)
    
    # Custom styling cho bảng với dòng Total được highlight
    def highlight_total_row(row):
        if row['Tổng điểm'] == 'Total':
            return ['background-color: #667eea; color: white; font-weight: bold; border: 1px solid #5a6fd8; padding: 10px; text-align: center; font-family: League Spartan;'] * len(row)
        else:
            return ['background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 8px; text-align: center; font-family: League Spartan;'] * len(row)
    
    styled_df = breakdown_df.style.apply(highlight_total_row, axis=1).set_table_styles([
        {
            'selector': 'thead th',
            'props': [
                ('background-color', '#667eea'),
                ('color', 'white'),
                ('font-weight', 'bold'),
                ('text-align', 'center'),
                ('padding', '12px'),
                ('font-family', 'League Spartan'),
                ('border', '1px solid #5a6fd8')
            ]
        },
        {
            'selector': 'table',
            'props': [
                ('border-collapse', 'collapse'),
                ('margin', '0 auto'),
                ('border-radius', '8px'),
                ('overflow', 'hidden'),
                ('box-shadow', '0 4px 6px rgba(0, 0, 0, 0.1)'),
                ('width', '100%')
            ]
        }
    ]).hide(axis="index")
    
    # Hiển thị bảng
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Tổng điểm": st.column_config.TextColumn(
                "Tổng điểm",
                width="medium",
            ),
            "Số thí sinh": st.column_config.TextColumn(
                "Số thí sinh",
                width="medium",
            ),
            "Thứ hạng theo %": st.column_config.TextColumn(
                "Thứ hạng theo %",
                width="medium",
            )
        }
    )
    
    # Chỉ hiển thị note cuối cho vùng "Cả nước" với điểm thực tế của user
    if region == "Cả nước":
        user_score_int = int(diem_input) if diem_input == int(diem_input) else int(diem_input)
        st.markdown(f"""
        <div style="margin-top: 1rem; padding: 0.8rem; background: #e8f4f8; border-radius: 6px; border-left: 3px solid #17a2b8;">
            <p style="color: #31708f; font-size: 0.85rem; margin: 0; font-style: italic;">
                <strong>🔍 Cách đọc bảng:</strong> Mốc "{user_score_int}+" có nghĩa là số thí sinh đạt từ {user_score_int}.0 điểm trở lên. 
                Nếu bạn có {diem_input} điểm, bạn sẽ nằm trong nhóm này cùng với những người có điểm cao hơn.
            </p>
        </div>
        """, unsafe_allow_html=True)

def get_region_subtext(region):
    """Get descriptive subtext for each region"""
    subtexts = {
        'Cả nước': 'Toàn bộ các tỉnh thành trên cả nước',
        'Miền Bắc': 'Các tỉnh thành từ Huế trở ra Bắc', 
        'Miền Nam': 'Các tỉnh thành từ Đà Nẵng trở vô Nam'
    }
    return subtexts.get(region, '')

# Load data
df = load_data()  # For calculations
df_histogram = load_histogram_data()  # For histogram visualization
df_2024 = load_top_2024_data()  # For 2024 comparison

# Mobile sidebar solution using session state
if 'sidebar_open' not in st.session_state:
    st.session_state.sidebar_open = True

# Add custom mobile sidebar toggle
col_toggle, col_spacer = st.columns([1, 10])
with col_toggle:
    if st.button("☰", key="mobile_toggle", help="Mở/đóng menu"):
        st.session_state.sidebar_open = not st.session_state.sidebar_open

# Info Header
st.markdown("""
<div class="info-header">
    📊 Data được xử lý và phân tích bởi <span class="author-name">Hieu Nguyen</span> - Founder of 
    <a href="https://madzynguyen.com/product/master-analytical-thinking-data-analysis-with-power-bi/?utm_source=web&utm_medium=maz&utm_campaign=web_diemthi_link&utm_id=web_diemthi&utm_content=web_diemthi" target="_blank" class="company-name">MazHocData</a> | 
    <a href="https://www.linkedin.com/in/ntrunghieu/" target="_blank">💼 LinkedIn</a>
</div>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🎯 Tra cứu thứ hạng điểm thi 2025</h1>
    <p class="main-subtitle">Khám phá vị trí của bạn trong bảng xếp hạng toàn quốc với giao diện hiện đại</p>
</div>
""", unsafe_allow_html=True)

# Sidebar (conditional display for mobile)
if st.session_state.sidebar_open or st.session_state.get('force_sidebar', False):
    with st.sidebar:
        st.markdown("### 📚 Thiết lập tra cứu")
        
        st.markdown("---")
        
        # Inputs
        khoi_input = st.selectbox(
            "📚 Chọn khối thi",
            sorted(df['khoi'].unique()),
            help="Chọn khối thi bạn muốn tra cứu"
        )
        
        diem_input = st.number_input(
            "🎯 Nhập tổng điểm",
            min_value=0.0,
            max_value=30.0,
            value=21.0,
            step=0.05,
            help="Nhập tổng điểm của bạn (0-30)"
        )
        
        lookup_button = st.button("🔍 Tra cứu ngay", use_container_width=True)
        
        # Thông tin bổ sung
        st.markdown("---")
        
        # Tips section
        st.markdown("### 💡 Gợi ý")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                    padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
            <p style="margin: 0; font-size: 0.85rem; color: #495057;">
                <strong>🎯 Điểm cao:</strong> ≥ 24 điểm<br>
                <strong>📈 Điểm khá:</strong> 18-24 điểm<br>
                <strong>⚖️ Điểm trung bình:</strong> < 18 điểm
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Help section
        st.markdown("### ❓ Trợ giúp")
        with st.expander("📖 Cách sử dụng"):
            st.markdown("""
            1. **Chọn khối thi** của bạn
            2. **Nhập điểm tổng** (3 môn cộng lại)
            3. **Nhấn tra cứu** để xem kết quả
            4. **Xem biểu đồ** và bảng thống kê chi tiết
            """)
        
        with st.expander("🤔 Câu hỏi thường gặp"):
            st.markdown("""
            **Q: Điểm tôi nhập có chính xác không?**  
            A: Đảm bảo cộng đúng tổng 3 môn thi
            
            **Q: Thứ hạng có ý nghĩa gì?**  
            A: Vị trí của bạn so với tất cả thí sinh cùng khối
            
            **Q: Dữ liệu từ nguồn nào?**  
            A: Từ kết quả thi chính thức năm 2025
            """)
        
        # Contact info
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem;">
            <p style="margin: 0; font-size: 0.8rem; color: #6c757d;">
                💬 Cần hỗ trợ? Liên hệ qua<br>
                <a href="https://www.facebook.com/madzyandlucas" target="_blank" 
                   style="color: #667eea; text-decoration: none;">
                   Facebook
                </a> 
                hoặc 
                <a href="https://madzynguyen.com" target="_blank" 
                   style="color: #667eea; text-decoration: none;">
                   Website
                </a>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # DON'T close sidebar after search - keep it open for multiple searches
        # This fixes the bug where users can't change inputs after first search
else:
    # Create hidden inputs to maintain state
    khoi_input = st.session_state.get('khoi_input', sorted(df['khoi'].unique())[0])
    diem_input = st.session_state.get('diem_input', 21.0)
    lookup_button = st.session_state.get('lookup_button', False)

# Store input values in session state
st.session_state.khoi_input = khoi_input
st.session_state.diem_input = diem_input

# Main content
if lookup_button:
    
    def format_region_result(df, diem_input, region):
        df_region = df[(df['khoi'] == khoi_input) & (df['view'] == region)].copy()
        df_region = df_region.sort_values('diem_moc')
        df_region['cumsum'] = df_region['count_exact'].cumsum()
        total = df_region['count_exact'].sum()

        user_row = df_region[df_region['diem_moc'] == diem_input]
        if user_row.empty:
            return None

        surpassed = int(user_row['cumsum'].values[0])
        percentile = 100 * surpassed / total
        rank = int(total - surpassed + 1)

        return {
            'top_percent': 100 - percentile,
            'higher_than_count': surpassed,
            'rank': rank,
            'total': int(total),
            'percentile': percentile
        }
    
    # Only one tab now - Kết quả chi tiết
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    # Quick overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    regions = ['Cả nước', 'Miền Bắc', 'Miền Nam']
    region_icons = ['🌍', '⛰️', '🏖️']
    
    results = {}
    for region in regions:
        results[region] = format_region_result(df, diem_input, region)
    
    # Display metrics
    for i, (region, icon) in enumerate(zip(regions, region_icons)):
        result = results[region]
        if result:
            # Get total students for this region
            df_region = df[(df['khoi'] == khoi_input) & (df['view'] == region)]
            total_students = df_region['count_exact'].sum()
            
            with [col1, col2, col3][i]:
                st.markdown(create_animated_metric_card(
                    f"Top % - {region}",
                    f"{result['top_percent']:.1f}%",
                    delta=f"Tổng: {total_students:,} thí sinh",
                    icon=icon
                ), unsafe_allow_html=True)
    
    with col4:
        # Get ranking compared to entire country
        country_result = results['Cả nước']
        ranking_info = f"#{country_result['rank']:,} / {country_result['total']:,}" if country_result else "N/A"
        
        st.markdown(create_animated_metric_card(
            "Điểm của bạn",
            f"{diem_input:.2f}",
            delta=f"Xếp hạng: {ranking_info}",
            icon="🎯"
        ), unsafe_allow_html=True)
    
    # 2024 Comparison Section
    st.markdown("### 📅 So sánh với năm 2024")
    st.markdown("""
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #ffc107;">
        <p style="margin: 0; color: #856404; font-size: 0.9rem;">
            <strong>💡 Thông tin:</strong> Nếu điểm số này thi vào năm 2024, bạn sẽ đạt top % như sau:
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1_2024, col2_2024, col3_2024 = st.columns(3)
    
    for i, (region, icon) in enumerate(zip(regions, region_icons)):
        comparison_2024 = get_2024_top_percentage(df_2024, khoi_input, region, diem_input)
        
        with [col1_2024, col2_2024, col3_2024][i]:
            if comparison_2024:
                if comparison_2024["top_percent"] == ">100":
                    st.markdown(create_animated_metric_card(
                        f"2024 - {region}",
                        "Ngoài top 100%",
                        delta="Điểm chưa đủ",
                        icon="📉"
                    ), unsafe_allow_html=True)
                else:
                    # So sánh với kết quả 2025
                    current_result = results[region]
                    if current_result:
                        current_top = current_result['top_percent']
                        comparison_2024_num = float(comparison_2024["top_percent"].replace('%', ''))
                        
                        if comparison_2024_num < current_top:
                            trend = f"Tốt hơn {current_top - comparison_2024_num:.1f}%"
                            trend_color = "#28a745"
                        elif comparison_2024_num > current_top:
                            trend = f"Kém hơn {comparison_2024_num - current_top:.1f}%"
                            trend_color = "#dc3545"
                        else:
                            trend = "Tương đương"
                            trend_color = "#ffc107"
                    else:
                        trend = ""
                        trend_color = "#666"
                    
                    st.markdown(f"""
                    <div class="metric-card fade-in">
                        <div class="metric-title">{icon} 2024 - {region}</div>
                        <div class="metric-value">Top {comparison_2024["top_percent"]}</div>
                        <div class="metric-delta" style="color: {trend_color};">
                            {trend}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Detailed results for each region with histogram
    for region, icon in zip(regions, region_icons):
        result = results[region]
        if result:
            st.markdown(f"""
            <div class="results-container fade-in">
                <div class="region-header">
                    <div class="region-title-row">
                        <span class="region-icon">{icon}</span>
                        <h2 class="region-title">{region}</h2>
                    </div>
                    <div class="region-subtext">{get_region_subtext(region)}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Desktop: side by side layout
            col_metrics, col_chart = st.columns([1, 2])
            
            with col_metrics:
                st.metric(
                    "🏆 Xếp hạng top",
                    f"{result['top_percent']:.2f}%",
                    delta=f"Cao hơn {result['higher_than_count']:,} thí sinh"
                )
                
                st.metric(
                    "📊 Thứ hạng",
                    f"{result['rank']:,}",
                    delta=f"Trên tổng {result['total']:,} thí sinh"
                )
                
                st.metric(
                    "📈 Phân vị", 
                    f"{result['percentile']:.1f}",
                    delta="percentile"
                )
            
            with col_chart:
                fig_histogram = create_region_histogram(df_histogram, khoi_input, region, diem_input)
                st.plotly_chart(fig_histogram, use_container_width=True)
            
            # Thêm bảng thống kê phân bổ điểm với parameters đầy đủ
            display_score_breakdown_section(df, khoi_input, region, diem_input, result)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Welcome screen
    st.markdown("""
    <div class="results-container fade-in" style="text-align: center; padding: 3rem;">
        <h2>🚀 Chào mừng đến với hệ thống tra cứu điểm thi hiện đại!</h2>
        <p style="font-size: 1.1rem; color: #666; margin: 2rem 0;">
            Nhập thông tin của bạn ở sidebar bên trái và nhấn nút <strong>"Tra cứu ngay"</strong> 
            để khám phá vị trí của mình trong bảng xếp hạng toàn quốc.
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 2rem;">
            <div style="text-align: center;">
                <div style="font-size: 3rem;">📊</div>
                <h4>Phân tích chi tiết</h4>
                <p>Xem thứ hạng và phân vị của bạn với biểu đồ tương tác</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🎯 <strong>Tra cứu điểm thi 2025</strong> | Được xây dựng với ❤️ HieuNguyen</p>
    <p style="font-size: 0.9rem;">💡 Dữ liệu được cập nhật từ kết quả thi chính thức</p>
</div>
""", unsafe_allow_html=True)
