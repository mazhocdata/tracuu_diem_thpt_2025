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
    
    /* Sidebar Styles */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Input Styles */
    .stSelectbox > div > div > div {
        background: white;
        border-radius: 10px;
        font-family: 'League Spartan', sans-serif;
    }
    
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e9ecef;
        transition: border-color 0.3s ease;
        font-family: 'League Spartan', sans-serif;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
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
    
    /* Tab Styles - Increased width */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        min-width: 200px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px 15px 0 0;
        font-weight: 600;
        font-family: 'League Spartan', sans-serif;
        font-size: 1.1rem;
        padding: 0 2rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Icons */
    .icon {
        display: inline-block;
        width: 1.2em;
        height: 1.2em;
        margin-right: 0.5rem;
    }
    
    .icon-white {
        filter: brightness(0) invert(1);
    }
    
    .icon-dark {
        filter: brightness(0);
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Hide GitHub and menu buttons */
    [data-testid="stToolbar"] {
        display: none !important;
    }
    
    .stAppDeployButton {
        display: none !important;
    }
    
    [data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Hide hamburger menu */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Hide "Made with Streamlit" footer */
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
        
        .stTabs [data-baseweb="tab"] {
            min-width: 150px;
            font-size: 1rem;
            padding: 0 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("lookup_2025.csv")

def create_animated_metric_card(title, value, delta=None, icon="📊"):
    delta_html = f'<div class="metric-delta" style="color: #28a745;">▲ {delta}</div>' if delta else ""
    
    return f"""
    <div class="metric-card fade-in">
        <div class="metric-title">{icon} {title}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """

def create_region_histogram(df, khoi_input, region, diem_input):
    """Tạo histogram cho từng vùng miền với tooltip"""
    df_region = df[(df['khoi'] == khoi_input) & (df['view'] == region)].copy()
    df_region = df_region.sort_values('diem_moc')
    
    # Color mapping
    color_map = {
        'Cả nước': '#667eea',
        'Miền Bắc': '#f093fb', 
        'Miền Nam': '#4facfe'
    }
    
    fig = go.Figure()
    
    # Add histogram bars
    fig.add_trace(
        go.Bar(
            x=df_region['diem_moc'],
            y=df_region['count_exact'],
            name=f'Số thí sinh đạt điểm này',
            marker_color=color_map.get(region, '#667eea'),
            opacity=0.8,
            hovertemplate=(
                '<b>Điểm:</b> %{x}<br>' +
                '<b>Số thí sinh:</b> %{y:,.0f}<br>' +
                f'<b>Vùng:</b> {region}<br>' +
                '<extra></extra>'
            )
        )
    )
    
    # Add user point if exists
    user_data = df_region[df_region['diem_moc'] == diem_input]
    if not user_data.empty:
        fig.add_trace(
            go.Scatter(
                x=[diem_input],
                y=[user_data['count_exact'].values[0]],
                mode='markers',
                marker=dict(
                    size=15, 
                    color='red', 
                    symbol='star',
                    line=dict(width=2, color='white')
                ),
                name='Điểm của bạn',
                hovertemplate=(
                    '<b>Điểm của bạn:</b> %{x}<br>' +
                    '<b>Số thí sinh cùng điểm:</b> %{y:,.0f}<br>' +
                    '<extra></extra>'
                )
            )
        )
    
    fig.update_layout(
        title=f"Phổ điểm thi - Khối D1 ({region})",
        xaxis_title="Tổng điểm",
        yaxis_title="Số thí sinh",
        height=400,
        showlegend=True,
        font=dict(family="League Spartan", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='closest',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig.update_xaxes(
        gridcolor='lightgray',
        title_font=dict(family="League Spartan", size=14)
    )
    fig.update_yaxes(
        gridcolor='lightgray',
        title_font=dict(family="League Spartan", size=14)
    )
    
    return fig

def get_region_subtext(region):
    """Get descriptive subtext for each region"""
    subtexts = {
        'Cả nước': 'Toàn bộ các tỉnh thành trên cả nước',
        'Miền Bắc': 'Các tỉnh thành từ Huế trở ra Bắc', 
        'Miền Nam': 'Các tỉnh thành từ Đà Nẵng trở vô Nam'
    }
    return subtexts.get(region, '')
    icons = {
        "target": "🎯",
        "world": "🌍", 
        "mountain": "⛰️",
        "beach": "🏖️",
        "rank": "📊",
        "trophy": "🏆",
        "percentage": "📈",
        "book": "📚",
        "search": "🔍"
    }
    return icons.get(icon_type, "📊")

# Load data
df = load_data()

# Info Header
st.markdown("""
<div class="info-header">
    📊 Data được xử lý và phân tích bởi <span class="author-name">Hieu Nguyen</span> - Founder of 
    <a href="https://madzynguyen.com/product/master-analytical-thinking-data-analysis-with-power-bi/?utm_source=web&utm_medium=maz&utm_campaign=web_diemthi_link&utm_id=web_diemthi&utm_content=web_diemthi" target="_blank" class="company-name">MazHocData</a> | 
    <a href="https://www.linkedin.com/in/ntrunghieu/" target="_blank">💼 LinkedIn</a>
</div>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="main-header">
    <h1 class="main-title">🎯 Tra cứu thứ hạng điểm thi 2025</h1>
    <p class="main-subtitle">Khám phá vị trí của bạn trong bảng xếp hạng toàn quốc với giao diện hiện đại</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(f"### 📚 Thiết lập tra cứu")
    
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
            
            # Metrics and histogram side by side
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
                # Create and display histogram for this region
                fig_histogram = create_region_histogram(df, khoi_input, region, diem_input)
                st.plotly_chart(fig_histogram, use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Welcome screen
    st.markdown(f"""
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
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🎯 <strong>Tra cứu điểm thi 2025</strong> | Được xây dựng với ❤️ bằng Streamlit</p>
    <p style="font-size: 0.9rem;">💡 Dữ liệu được cập nhật từ kết quả thi chính thức</p>
</div>
""", unsafe_allow_html=True)
