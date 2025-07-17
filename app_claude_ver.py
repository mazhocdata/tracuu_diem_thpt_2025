import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# Page config
st.set_page_config(
    page_title="🎯 Tra cứu điểm thi 2025",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
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
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        font-size: 1.1rem;
        font-weight: 300;
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
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f0f0f0;
    }
    
    .region-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    .region-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #333;
        margin: 0;
    }
    
    /* Sidebar Styles */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Input Styles */
    .stSelectbox > div > div > div {
        background: white;
        border-radius: 10px;
    }
    
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e9ecef;
        transition: border-color 0.3s ease;
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
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Tab Styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px 10px 0 0;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
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
    
    /* Hide settings menu */
    [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] [data-testid="stElementContainer"]:last-child {
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

def create_comparison_chart(df, khoi_input, diem_input):
    """Tạo biểu đồ so sánh giữa các vùng miền"""
    regions = ['Cả nước', 'Miền Bắc', 'Miền Nam']
    colors = ['#667eea', '#f093fb', '#4facfe']
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=regions,
        specs=[[{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}]]
    )
    
    for i, region in enumerate(regions):
        df_region = df[(df['khoi'] == khoi_input) & (df['view'] == region)].copy()
        df_region = df_region.sort_values('diem_moc')
        
        # Histogram
        fig.add_trace(
            go.Bar(
                x=df_region['diem_moc'],
                y=df_region['count_exact'],
                name=region,
                marker_color=colors[i],
                opacity=0.7,
                showlegend=False
            ),
            row=1, col=i+1
        )
        
        # User point
        user_data = df_region[df_region['diem_moc'] == diem_input]
        if not user_data.empty:
            fig.add_trace(
                go.Scatter(
                    x=[diem_input],
                    y=[user_data['count_exact'].values[0]],
                    mode='markers',
                    marker=dict(size=15, color='red', symbol='star'),
                    name=f'Điểm của bạn ({region})',
                    showlegend=False
                ),
                row=1, col=i+1
            )
    
    fig.update_layout(
        title="📊 So sánh phổ điểm giữa các vùng miền",
        height=400,
        showlegend=False,
        font=dict(family="Inter", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_xaxes(title_text="Điểm", gridcolor='lightgray')
    fig.update_yaxes(title_text="Số thí sinh", gridcolor='lightgray')
    
    return fig

def create_percentile_chart(df, khoi_input):
    """Tạo biểu đồ phân vị"""
    regions = ['Cả nước', 'Miền Bắc', 'Miền Nam']
    
    fig = go.Figure()
    
    for region in regions:
        df_region = df[(df['khoi'] == khoi_input) & (df['view'] == region)].copy()
        df_region = df_region.sort_values('diem_moc')
        
        fig.add_trace(
            go.Scatter(
                x=df_region['diem_moc'],
                y=df_region['percentile'],
                mode='lines+markers',
                name=region,
                line=dict(width=3),
                marker=dict(size=6)
            )
        )
    
    fig.update_layout(
        title="📈 Đường phân vị theo điểm",
        xaxis_title="Điểm",
        yaxis_title="Phân vị (%)",
        height=400,
        font=dict(family="Inter", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig.update_xaxes(gridcolor='lightgray')
    fig.update_yaxes(gridcolor='lightgray')
    
    return fig

def create_top_students_chart(df, khoi_input):
    """Biểu đồ top thí sinh theo vùng miền"""
    regions = ['Cả nước', 'Miền Bắc', 'Miền Nam']
    top_scores = []
    
    for region in regions:
        df_region = df[(df['khoi'] == khoi_input) & (df['view'] == region)]
        if len(df_region) > 0:
            # Lấy top 1% thí sinh
            total_students = df_region['count_exact'].sum()
            top_1_percent = max(1, int(total_students * 0.01))  # Ít nhất 1 thí sinh
            
            df_sorted = df_region.sort_values('diem_moc', ascending=False)
            cumsum = 0
            min_score = df_sorted['diem_moc'].max()  # Default to max score
            
            for _, row in df_sorted.iterrows():
                cumsum += row['count_exact']
                if cumsum >= top_1_percent:
                    min_score = row['diem_moc']
                    break
            
            top_scores.append({
                'region': region, 
                'min_score': float(min_score), 
                'students': top_1_percent
            })
    
    if not top_scores:
        return go.Figure()
    
    df_top = pd.DataFrame(top_scores)
    
    fig = go.Figure(data=[
        go.Bar(
            x=df_top['region'],
            y=df_top['min_score'],
            marker_color=['#667eea', '#f093fb', '#4facfe'],
            text=[f"{score:.1f}" for score in df_top['min_score']],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="🏆 Điểm chuẩn Top 1% theo vùng miền",
        xaxis_title="Vùng miền",
        yaxis_title="Điểm tối thiểu",
        height=300,
        font=dict(family="Inter", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# Load data
df = load_data()

# Header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🎯 Tra cứu thứ hạng điểm thi 2025</h1>
    <p class="main-subtitle">Khám phá vị trí của bạn trong bảng xếp hạng toàn quốc với giao diện hiện đại</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Thiết lập tra cứu")
    
    # Dark mode toggle (placeholder)
    dark_mode = st.checkbox("🌙 Chế độ tối", value=False)
    
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
        value=20.0,
        step=0.05,
        help="Nhập tổng điểm của bạn (0-30)"
    )
    
    st.markdown("---")
    
    # Quick stats
    df_khoi = df[df['khoi'] == khoi_input]
    total_students = df_khoi['count_exact'].sum()
    
    # Fix weighted average calculation
    scores = df_khoi['diem_moc'].values
    weights = df_khoi['count_exact'].values
    if len(scores) > 0 and len(weights) > 0:
        avg_score = np.average(scores, weights=weights)
    else:
        avg_score = 0
    
    st.markdown("### 📊 Thống kê nhanh")
    st.metric("Tổng thí sinh", f"{total_students:,}")
    st.metric("Điểm trung bình", f"{avg_score:.2f}")
    
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
    
    # Results tabs
    tab1, tab2, tab3 = st.tabs(["📊 Kết quả chi tiết", "📈 Biểu đồ phân tích", "🏆 Thống kê nâng cao"])
    
    with tab1:
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        
        # Quick overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        regions = ['Cả nước', 'Miền Bắc', 'Miền Nam']
        region_icons = ['🌍', '🏔️', '🏖️']
        
        results = {}
        for region in regions:
            results[region] = format_region_result(df, diem_input, region)
        
        # Display metrics
        for i, (region, icon) in enumerate(zip(regions, region_icons)):
            result = results[region]
            if result:
                with [col1, col2, col3][i]:
                    st.markdown(create_animated_metric_card(
                        f"Top % - {region}",
                        f"{result['top_percent']:.1f}%",
                        icon=icon
                    ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_animated_metric_card(
                "Điểm của bạn",
                f"{diem_input:.2f}",
                icon="🎯"
            ), unsafe_allow_html=True)
        
        # Detailed results for each region
        for region, icon in zip(regions, region_icons):
            result = results[region]
            if result:
                st.markdown(f"""
                <div class="results-container fade-in">
                    <div class="region-header">
                        <span class="region-icon">{icon}</span>
                        <h2 class="region-title">{region}</h2>
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "🥇 Xếp hạng top",
                        f"{result['top_percent']:.2f}%",
                        delta=f"Cao hơn {result['higher_than_count']:,} thí sinh"
                    )
                
                with col2:
                    st.metric(
                        "📊 Thứ hạng",
                        f"{result['rank']:,}",
                        delta=f"Trên tổng {result['total']:,} thí sinh"
                    )
                
                with col3:
                    st.metric(
                        "📈 Phân vị",
                        f"{result['percentile']:.1f}",
                        delta="percentile"
                    )
                
                st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        
        # Comparison chart
        fig_comparison = create_comparison_chart(df, khoi_input, diem_input)
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Percentile chart
            fig_percentile = create_percentile_chart(df, khoi_input)
            st.plotly_chart(fig_percentile, use_container_width=True)
        
        with col2:
            # Top students chart
            fig_top = create_top_students_chart(df, khoi_input)
            st.plotly_chart(fig_top, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Phân tích điểm của bạn")
            
            # Score analysis
            all_scores = []
            for region in regions:
                result = results[region]
                if result:
                    all_scores.append({
                        'Vùng miền': region,
                        'Top %': f"{result['top_percent']:.2f}%",
                        'Xếp hạng': f"{result['rank']:,}",
                        'Tổng TS': f"{result['total']:,}"
                    })
            
            if all_scores:
                df_analysis = pd.DataFrame(all_scores)
                st.dataframe(df_analysis, use_container_width=True)
            else:
                st.info("Không có dữ liệu để hiển thị.")
            
            # Improvement suggestions
            st.markdown("### 💡 Gợi ý cải thiện")
            
            valid_results = {k: v for k, v in results.items() if v is not None}
            if valid_results:
                best_region = min(valid_results.keys(), key=lambda x: valid_results[x]['top_percent'])
                worst_region = max(valid_results.keys(), key=lambda x: valid_results[x]['top_percent'])
                
                st.info(f"🏆 Bạn có thứ hạng tốt nhất ở **{best_region}** với top {valid_results[best_region]['top_percent']:.2f}%")
                
                if valid_results[worst_region]['top_percent'] < 50:
                    st.warning(f"📈 Cần cải thiện ở **{worst_region}** - hiện tại top {valid_results[worst_region]['top_percent']:.2f}%")
            else:
                st.info("💡 Không tìm thấy dữ liệu phù hợp để đưa ra gợi ý.")
        
        with col2:
            st.markdown("### 📊 Thống kê khối thi")
            
            # Subject block statistics
            khoi_stats_data = []
            for region in ['Cả nước', 'Miền Bắc', 'Miền Nam']:
                df_region = df[(df['khoi'] == khoi_input) & (df['view'] == region)]
                if len(df_region) > 0:
                    total_students = df_region['count_exact'].sum()
                    scores = df_region['diem_moc'].values
                    weights = df_region['count_exact'].values
                    if len(scores) > 0 and len(weights) > 0:
                        avg_score = np.average(scores, weights=weights)
                    else:
                        avg_score = 0
                    
                    khoi_stats_data.append({
                        'Vùng miền': region,
                        'Tổng thí sinh': f"{int(total_students):,}",
                        'Điểm TB': f"{avg_score:.2f}"
                    })
            
            if khoi_stats_data:
                khoi_stats_df = pd.DataFrame(khoi_stats_data)
                st.dataframe(khoi_stats_df, use_container_width=True)
            
            # Score distribution
            st.markdown("### 🎲 Phân bố điểm số")
            
            score_ranges = ['0-10', '10-15', '15-20', '20-25', '25-30']
            range_counts = []
            
            df_khoi = df[df['khoi'] == khoi_input]
            for range_name in score_ranges:
                if range_name == '0-10':
                    count = df_khoi[df_khoi['diem_moc'] < 10]['count_exact'].sum()
                elif range_name == '10-15':
                    count = df_khoi[(df_khoi['diem_moc'] >= 10) & (df_khoi['diem_moc'] < 15)]['count_exact'].sum()
                elif range_name == '15-20':
                    count = df_khoi[(df_khoi['diem_moc'] >= 15) & (df_khoi['diem_moc'] < 20)]['count_exact'].sum()
                elif range_name == '20-25':
                    count = df_khoi[(df_khoi['diem_moc'] >= 20) & (df_khoi['diem_moc'] < 25)]['count_exact'].sum()
                else:  # 25-30
                    count = df_khoi[df_khoi['diem_moc'] >= 25]['count_exact'].sum()
                
                range_counts.append(int(count))
            
            if range_counts and sum(range_counts) > 0:
                fig_pie = px.pie(
                    values=range_counts,
                    names=score_ranges,
                    title="Phân bố theo khoảng điểm",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_pie.update_layout(height=300, font=dict(family="Inter"))
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("Không có dữ liệu để hiển thị biểu đồ phân bố.")
        
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
                <p>Xem thứ hạng và phân vị của bạn</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 3rem;">📈</div>
                <h4>Biểu đồ trực quan</h4>
                <p>So sánh với các vùng miền</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 3rem;">🏆</div>
                <h4>Thống kê nâng cao</h4>
                <p>Phân tích sâu và gợi ý</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🎯 <strong>Tra cứu điểm thi 2025</strong> | Được xây dựng với ❤️ bằng Streamlit</p>
    <p style="font-size: 0.9rem;">💡 Dữ liệu được cập nhật từ kết quả thi chính thức</p>
</div>
""", unsafe_allow_html=True)
