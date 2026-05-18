import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title = "Sales Dashboard",
    page_icon = "📊",
    layout = "wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv('data/storedata/superstore_cleaned.csv', encoding='latin=1')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

df = load_data()

st.sidebar.header("Filters")

years = sorted(df['Year'].unique())
selected_years = st.sidebar.multiselect("Select Year", years, default=years)

regions = sorted(df['Region'].unique())
selected_regions = st.sidebar.multiselect("Select Region", regions, default=regions)

categories = sorted(df['Category'].unique())
selected_categories = st.sidebar.multiselect("Select Category", categories, default=categories)

df_filtered = df[
    (df['Year'].isin(selected_years)) &
    (df['Region'].isin(selected_regions)) &
    (df['Category'].isin(selected_categories))
]

st.title("📊 Sales Performance Dashboard")
st.markdown(f"Showing **{len(df_filtered):,}** orders based on selected filters")

st.subheader("Key Performance Indicators")

col1,col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Revenue ", f"${df_filtered['Sales'].sum():,.0f}")

with col2:
    st.metric("Total Profit", f"${df_filtered['Profit'].sum():,.0f}")

with col3:
    st.metric("Avg Profit Margin", f"{df_filtered['Profit Margin %'].mean():.1f}%")

with col4:
    st.metric("Total Orders", f"{df_filtered['Order ID'].nunique():,}")

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric("Total Customers", f"{df_filtered['Customer Name'].nunique():,}")

with col6:
    st.metric("Loss-making Orders", f"{df_filtered['Is Loss'].sum():,}")

with col7:
    loss_rate = df_filtered['Is Loss'].mean() * 100
    st.metric("Loss Order Rate", f"{loss_rate:.1f}%")

with col8:
    st.metric("Avg Ship Duration", f"{df_filtered['Ship Duration'].mean():.1f} days")

st.subheader("Sales and Profit Overview")

col1, col2 = st.columns(2)

with col1:
    region_data = df_filtered.groupby('Region').agg(
        Total_Sales = ('Sales', 'sum'),
        Total_Profit = ('Profit', 'sum')
    ).reset_index()

    fig_region = px.bar(
        region_data,
        x='Region',
        y=['Total_Sales', 'Total_Profit'],
        title = 'Sales and Profit by Region',
        barmode='group',
        color_discrete_map={'Total_Sales': '#636EFA', 'Total_Profit': '#00CC96'}
    )
    st.plotly_chart(fig_region, use_container_width=True)

with col2:
    yearly_data = df_filtered.groupby('Year').agg(
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum')
    ).reset_index()

    fig_yearly = px.line(
        yearly_data,
        x='Year',
        y=['Total_Sales', 'Total_Profit'],
        title='Yearly Sales & Profit Trend',
        markers=True,
        color_discrete_map={'Total_Sales': '#636EFA', 'Total_Profit': '#00CC96'}
    )
    st.plotly_chart(fig_yearly, use_container_width=True)

st.subheader("Category and Discount Analysis")

col1, col2 =st.columns(2)

with col1:
    subcat_data = df_filtered.groupby('Sub-Category').agg(
        Total_Profit=('Profit', 'sum')
    ).reset_index().sort_values('Total_Profit')

    fig_subcat = px.bar(
        subcat_data,
        x='Total_Profit',
        y='Sub-Category',
        orientation='h',
        title='Profit by Sub-Category',
        color='Total_Profit',
        color_continuous_scale=['red', 'yellow', 'green']
    )
    st.plotly_chart(fig_subcat, use_container_width=True)

with col2:
    df_filtered['Discount Band'] = pd.cut(
        df_filtered['Discount'],
        bins=[-0.1, 0, 0.2, 0.4, 0.6, 0.9],
        labels=['No Discount', '1-20%', '21-40%', '41-60%', '61-90%']
    )

    discount_data = df_filtered.groupby('Discount Band', observed=True).agg(
        Avg_Profit_Margin=('Profit Margin %', 'mean')
    ).reset_index()

    fig_discount = px.bar(
        discount_data,
        x='Discount Band',
        y='Avg_Profit_Margin',
        title='Avg Profit Margin by Discount Band',
        color='Avg_Profit_Margin',
        color_continuous_scale=['red', 'yellow', 'green']
    )
    st.plotly_chart(fig_discount, use_container_width=True)

from prophet import Prophet

st.subheader("AI Sales Forecasting")

forecast_data = df_filtered.groupby('Order Date').agg(
    y=('Sales', 'sum')
).reset_index().rename(columns={'Order Date': 'ds'})

model = Prophet(yearly_seasonality=True, weekly_seasonality=False)
model.fit(forecast_data)

periods = st.slider("Forecast how many days into the future?", 30, 90, 365)

future = model.make_future_dataframe(periods=periods)
forecast = model.predict(future)

fig_forecast = go.Figure()

fig_forecast.add_trace(go.Scatter(
    x=forecast_data['ds'], y=forecast_data['y'],
    name='Actual Sales', line=dict(color='#636EFA')
))

fig_forecast.add_trace(go.Scatter(
    x=forecast['ds'], y=forecast['yhat'],
    name='Forecasted Sales', line=dict(color='#00CC96', dash='dash')
))

fig_forecast.add_trace(go.Scatter(
    x=forecast['ds'].tolist() + forecast['ds'].tolist()[::-1],
    y=forecast['yhat_upper'].tolist() + forecast['yhat_lower'].tolist()[::-1],
    fill='toself',
    fillcolor='rgba(0,204,150,0.1)',
    line=dict(color='rgba(255,255,255,0)'),
    name='Confidence Interval'
))

fig_forecast.update_layout(title='Sales Forecast', xaxis_title='Date', yaxis_title='Sales')
st.plotly_chart(fig_forecast, use_container_width=True)

st.markdown("**Forecast Summary**")
future_only = forecast[forecast['ds'] > forecast_data['ds'].max()]
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Forecasted Total Sales", f"${future_only['yhat'].sum():,.0f}")
with col2:
    st.metric("Avg Daily Sales", f"${future_only['yhat'].mean():,.0f}")
with col3:
    st.metric("Forecast Period", f"{periods} days")

st.subheader("Loss-Making Orders Analysis")

col1, col2 = st.columns(2)

with col1:
    loss_by_region = df_filtered[df_filtered['Is Loss']].groupby('Region').agg(
        Loss_Orders=('Is Loss', 'sum'),
        Total_Loss=('Profit', 'sum')
    ).reset_index().sort_values('Total_Loss')

    fig_loss_region = px.bar(
        loss_by_region,
        x='Region',
        y='Total_Loss',
        title='Total Loss by Region',
        color='Total_Loss',
        color_continuous_scale=['red', 'orange']
    )
    st.plotly_chart(fig_loss_region, use_container_width=True)

with col2:
    loss_by_cat = df_filtered[df_filtered['Is Loss']].groupby('Category').agg(
        Loss_Orders=('Is Loss', 'sum'),
        Total_Loss=('Profit', 'sum')
    ).reset_index().sort_values('Total_Loss')

    fig_loss_cat = px.bar(
        loss_by_cat,
        x='Category',
        y='Total_Loss',
        title='Total Loss by Category',
        color='Total_Loss',
        color_continuous_scale=['red', 'orange']
    )
    st.plotly_chart(fig_loss_cat, use_container_width=True)

# Loss orders table
st.markdown("**Top 20 Worst Performing Orders**")
loss_table = df_filtered[df_filtered['Is Loss']][
    ['Order ID', 'Customer Name', 'Region', 'Category', 'Sub-Category', 'Sales', 'Profit', 'Discount', 'Profit Margin %']
].sort_values('Profit').head(20).round(2)

st.dataframe(loss_table, use_container_width=True)