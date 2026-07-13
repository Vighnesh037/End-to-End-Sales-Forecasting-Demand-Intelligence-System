import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Sales Forecasting & Demand Intelligence", page_icon="📊", layout="wide")

st.markdown("""
<style>
.stApp {background: #f4f7fb;}
.block-container {padding-top: 2rem; max-width: 1500px;}

[data-testid="stSidebar"] {background: #0f172a;}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {color: #f8fafc !important;}

.title {font-size: 2.1rem; font-weight: 800; color: #0f172a;}
.subtitle {font-size: 1rem; color: #64748b; margin: 4px 0 30px;}
.page-title {font-size: 1.7rem; font-weight: 800; color: #0f172a; margin-bottom: 20px;}
.section-title {font-size: 1.2rem; font-weight: 700; color: #1e293b; margin: 24px 0 12px;}

.kpi {
    background: #ffffff;
    border: 1px solid #dbe3ee;
    border-radius: 14px;
    padding: 22px;
    min-height: 120px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}
.kpi-label {font-size: 0.82rem; font-weight: 600; color: #64748b;}
.kpi-value {font-size: 1.8rem; font-weight: 800; color: #0f172a; margin-top: 8px;}

.stSelectbox label, .stMultiSelect label, .stSlider label {
    color: #334155 !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)
    return df


@st.cache_data
def load_forecasts():
    df = pd.read_csv("forecast_results.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df


@st.cache_data
def load_anomalies():
    df = pd.read_csv("anomaly_dates.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df


@st.cache_data
def load_demand_segments():
    return pd.read_csv("demand_segments.csv")


def kpi(label, value):
    st.markdown(
        f'<div class="kpi"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div></div>',
        unsafe_allow_html=True
    )


def style_chart(fig, height=420):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=60, r=30, t=60, b=60),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family="Arial", size=13, color="#334155"),
        title_font=dict(size=17, color="#0f172a"),
        legend=dict(font=dict(color="#475569")),
        hoverlabel=dict(bgcolor="white", font_color="#0f172a")
    )
    fig.update_xaxes(showgrid=False, linecolor="#cbd5e1", tickfont=dict(color="#475569"))
    fig.update_yaxes(showgrid=True, gridcolor="#e2e8f0", zeroline=False, tickfont=dict(color="#475569"))
    return fig


sales_df = load_data()
forecast_df = load_forecasts()

st.sidebar.markdown("## 📊 Sales Intelligence")
st.sidebar.caption("Forecasting & Demand Analytics")

page = st.sidebar.radio(
    "Navigation",
    ["Sales Overview", "Forecast Explorer", "Anomaly Report", "Product Demand Segments"],
    label_visibility="collapsed"
)

st.markdown('<div class="title">Sales Forecasting & Demand Intelligence</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Sales performance, future demand forecasting and business intelligence</div>',
    unsafe_allow_html=True
)


if page == "Sales Overview":
    st.markdown('<div class="page-title">Sales Overview</div>', unsafe_allow_html=True)

    total_sales = sales_df["Sales"].sum()
    total_orders = sales_df["Order ID"].nunique()
    total_customers = sales_df["Customer ID"].nunique()
    avg_order_value = total_sales / total_orders

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi("TOTAL SALES", f"${total_sales:,.0f}")
    with c2:
        kpi("TOTAL ORDERS", f"{total_orders:,}")
    with c3:
        kpi("AVERAGE ORDER VALUE", f"${avg_order_value:,.2f}")
    with c4:
        kpi("TOTAL CUSTOMERS", f"{total_customers:,}")

    sales_df["Year"] = sales_df["Order Date"].dt.year
    yearly_sales = sales_df.groupby("Year", as_index=False)["Sales"].sum()
    monthly_sales = sales_df.set_index("Order Date").resample("ME")["Sales"].sum().reset_index()

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            yearly_sales, x="Year", y="Sales", title="Annual Sales Performance",
            labels={"Year": "Year", "Sales": "Total Sales ($)"}
        )
        fig.update_traces(marker_color="#2563eb")
        fig.update_xaxes(tickmode="linear", dtick=1)
        st.plotly_chart(style_chart(fig), use_container_width=True)

    with c2:
        fig = px.line(
            monthly_sales, x="Order Date", y="Sales", title="Monthly Sales Trend",
            labels={"Order Date": "Month", "Sales": "Monthly Sales ($)"}
        )
        fig.update_traces(line=dict(color="#0f766e", width=3))
        st.plotly_chart(style_chart(fig), use_container_width=True)

    st.markdown('<div class="section-title">Regional and Category Performance</div>', unsafe_allow_html=True)

    regions = sorted(sales_df["Region"].dropna().unique())
    categories = sorted(sales_df["Category"].dropna().unique())

    c1, c2 = st.columns(2)
    with c1:
        selected_regions = st.multiselect("Select Regions", regions, default=regions)
    with c2:
        selected_categories = st.multiselect("Select Categories", categories, default=categories)

    filtered_df = sales_df[
        sales_df["Region"].isin(selected_regions) &
        sales_df["Category"].isin(selected_categories)
    ]

    filtered_sales = filtered_df.groupby(["Region", "Category"], as_index=False)["Sales"].sum()

    fig = px.bar(
        filtered_sales, x="Region", y="Sales", color="Category", barmode="group",
        title="Sales by Region and Category",
        labels={"Sales": "Total Sales ($)", "Category": "Product Category"},
        color_discrete_sequence=["#2563eb", "#0f766e", "#f59e0b"]
    )
    st.plotly_chart(style_chart(fig, 470), use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        category_sales = sales_df.groupby("Category", as_index=False)["Sales"].sum()
        fig = px.pie(
            category_sales, names="Category", values="Sales", hole=0.5,
            title="Sales Distribution by Category",
            color_discrete_sequence=["#2563eb", "#0f766e", "#f59e0b"]
        )
        fig.update_traces(textposition="outside", textinfo="label+percent")
        st.plotly_chart(style_chart(fig), use_container_width=True)

    with c2:
        region_sales = sales_df.groupby("Region", as_index=False)["Sales"].sum().sort_values("Sales")
        fig = px.bar(
            region_sales, x="Sales", y="Region", orientation="h",
            title="Total Sales by Region",
            labels={"Sales": "Total Sales ($)", "Region": "Region"}
        )
        fig.update_traces(marker_color="#7c3aed")
        st.plotly_chart(style_chart(fig), use_container_width=True)


elif page == "Forecast Explorer":
    st.markdown('<div class="page-title">Forecast Explorer</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        forecast_type = st.selectbox("Forecast By", ["Category", "Region"])

    options = sorted(forecast_df[forecast_df["Type"] == forecast_type]["Segment"].unique())

    with c2:
        selected_segment = st.selectbox(f"Select {forecast_type}", options)
    with c3:
        forecast_horizon = st.slider("Forecast Horizon (Months)", 1, 3, 3)

    segment_monthly = (
        sales_df[sales_df[forecast_type] == selected_segment]
        .set_index("Order Date")
        .resample("ME")["Sales"]
        .sum()
        .reset_index()
    )

    selected_forecast = (
        forecast_df[
            (forecast_df["Type"] == forecast_type) &
            (forecast_df["Segment"] == selected_segment)
        ]
        .sort_values("Date")
        .head(forecast_horizon)
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=segment_monthly["Order Date"], y=segment_monthly["Sales"],
        mode="lines", name="Historical Sales",
        line=dict(color="#2563eb", width=3)
    ))

    fig.add_trace(go.Scatter(
        x=selected_forecast["Date"], y=selected_forecast["Forecast"],
        mode="lines+markers", name="Forecast",
        line=dict(color="#f59e0b", width=3, dash="dash"),
        marker=dict(size=9)
    ))

    fig.update_layout(
        title=f"Historical Sales and {forecast_horizon}-Month Forecast — {selected_segment}",
        xaxis_title="Month",
        yaxis_title="Sales ($)",
        hovermode="x unified"
    )

    st.plotly_chart(style_chart(fig, 520), use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        kpi("FORECAST PERIOD", f"{forecast_horizon} Months")
    with c2:
        kpi("MODEL MAE", "$14,558.21")
    with c3:
        kpi("MODEL RMSE", "$18,869.81")

    st.markdown('<div class="section-title">Forecast Results</div>', unsafe_allow_html=True)

    forecast_display = selected_forecast[["Date", "Forecast"]].copy()
    forecast_display["Date"] = forecast_display["Date"].dt.strftime("%B %Y")
    forecast_display["Forecast"] = forecast_display["Forecast"].map(lambda x: f"${x:,.2f}")

    st.dataframe(forecast_display, hide_index=True, use_container_width=True)


elif page == "Anomaly Report":
    st.markdown('<div class="page-title">Anomaly Report</div>', unsafe_allow_html=True)

    anomaly_dates = load_anomalies()

    c1, c2, c3 = st.columns(3)
    with c1:
        kpi("DETECTED ANOMALIES", len(anomaly_dates))
    with c2:
        kpi("ANALYSIS FREQUENCY", "Weekly")
    with c3:
        kpi("DETECTION STATUS", "Complete")

    st.markdown('<div class="section-title">Weekly Sales Anomaly Detection</div>', unsafe_allow_html=True)
    st.image("charts/5output.png", use_container_width=True)

    st.markdown('<div class="section-title">Detected Anomaly Dates</div>', unsafe_allow_html=True)
    st.dataframe(anomaly_dates, hide_index=True, use_container_width=True)


elif page == "Product Demand Segments":
    st.markdown('<div class="page-title">Product Demand Segments</div>', unsafe_allow_html=True)

    demand_segments = load_demand_segments()

    c1, c2, c3 = st.columns(3)
    with c1:
        kpi("SUB-CATEGORIES ANALYSED", len(demand_segments))
    with c2:
        kpi("SEGMENTATION METHOD", "K-Means")
    with c3:
        kpi("ANALYSIS STATUS", "Complete")

    st.markdown('<div class="section-title">K-Means Demand Clusters</div>', unsafe_allow_html=True)
    st.image("charts/6output.png", use_container_width=True)

    st.markdown('<div class="section-title">Sub-Category Demand Segments</div>', unsafe_allow_html=True)
    st.dataframe(demand_segments, hide_index=True, use_container_width=True)