"""電商資料 Streamlit 互動式儀表板"""
import streamlit as st
from data_loader import EcommerceDataLoader
from business_metrics import BusinessMetricsCalculator, MetricsVisualizer

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")
st.title("E-Commerce Analytics Dashboard")

# --- 側邊欄篩選器 ---
loader = EcommerceDataLoader('ecommerce_data/orders.csv')
df = loader.load()
available_years = sorted(df['year'].unique())

with st.sidebar:
    st.header("Filters")
    selected_year = st.selectbox("Analysis Year", available_years, index=len(available_years) - 1)
    compare_year = st.selectbox("Comparison Year", available_years, index=0)

df_analysis = loader.filter_by_year(selected_year)
calc = BusinessMetricsCalculator(df_analysis)
viz = MetricsVisualizer()

# --- KPI 指標卡片 ---
rev = calc.revenue_metrics()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${rev['total_revenue']:,.0f}")
col2.metric("Monthly Growth", f"{rev['latest_growth']:.1f}%")
col3.metric("Avg Order Value", f"${rev['avg_order_value']:,.0f}")
col4.metric("Total Orders", f"{rev['total_orders']:,}")

st.divider()

# --- 圖表區 2x2 ---
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.plotly_chart(viz.revenue_trend(rev['monthly_revenue']), width="stretch")
    st.plotly_chart(viz.state_revenue(calc.geo_metrics()), width="stretch")

with chart_col2:
    st.plotly_chart(viz.category_performance(calc.product_metrics()), width="stretch")
    st.plotly_chart(viz.satisfaction_distribution(df_analysis), width="stretch")

st.divider()

# --- 配送指標 ---
st.subheader("Delivery Metrics")
delivery = calc.delivery_metrics()
d_col1, d_col2, d_col3 = st.columns(3)
d_col1.metric("Avg Delivery Days", f"{delivery['avg_days']:.1f}")
d_col2.metric("Median Delivery Days", f"{delivery['median_days']:.0f}")
d_col3.metric("Over 7 Days", f"{delivery['over_7_days_pct']:.1f}%")

st.plotly_chart(viz.delivery_vs_satisfaction(delivery['by_satisfaction']), width="stretch")

# --- 年度比較 ---
st.divider()
st.subheader(f"{compare_year} vs {selected_year} Comparison")

comp_cols = st.columns(2)
for i, year in enumerate([compare_year, selected_year]):
    df_yr = loader.filter_by_year(year)
    c = BusinessMetricsCalculator(df_yr)
    r = c.revenue_metrics()
    s = c.satisfaction_metrics()
    with comp_cols[i]:
        st.markdown(f"### {year}")
        st.write(f"Orders: **{r['total_orders']:,}**")
        st.write(f"Revenue: **${r['total_revenue']:,.0f}**")
        st.write(f"Avg Order: **${r['avg_order_value']:,.0f}**")
        st.write(f"Satisfaction: **{s['mean']:.2f}**")
