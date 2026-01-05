import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Sportsman's Warehouse - Home Gym Products",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .product-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 100%;
    }
    .product-title {
        font-size: 14px;
        font-weight: bold;
        color: #333;
        margin-bottom: 10px;
        height: 40px;
        overflow: hidden;
    }
    .product-price {
        font-size: 18px;
        font-weight: bold;
        color: #28a745;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 20px;
        color: white;
    }
    .stMetric {
        background-color: #111 !important;
        color: #fff !important;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #222;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('sportsmans_warehouse_products.csv')
    # Clean price and create numeric column
    df['price_numeric'] = df['price'].str.replace('R', '').str.replace(' ', '').astype(float)
    # Extract brand (first word of product name)
    df['brand'] = df['product_name'].str.split().str[0]
    return df

df = load_data()

# Header
st.title("🏋️ Sportsman's Warehouse - Home Gym Products Dashboard")
st.markdown("---")

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Brand filter
brands = ['All'] + sorted(df['brand'].unique().tolist())
selected_brand = st.sidebar.selectbox("Select Brand", brands)

# Price range filter
min_price = float(df['price_numeric'].min())
max_price = float(df['price_numeric'].max())
price_range = st.sidebar.slider(
    "Price Range (R)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price),
    format="R %.0f"
)

# Page filter
pages = ['All'] + sorted(df['page'].unique().tolist())
selected_page = st.sidebar.selectbox("Select Page", pages)

# Apply filters
filtered_df = df.copy()
if selected_brand != 'All':
    filtered_df = filtered_df[filtered_df['brand'] == selected_brand]
filtered_df = filtered_df[(filtered_df['price_numeric'] >= price_range[0]) & 
                          (filtered_df['price_numeric'] <= price_range[1])]
if selected_page != 'All':
    filtered_df = filtered_df[filtered_df['page'] == selected_page]

# Key Metrics Row
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Products", len(filtered_df), delta=f"{len(filtered_df) - len(df)} from total" if selected_brand != 'All' or price_range != (min_price, max_price) else None)

with col2:
    avg_price = filtered_df['price_numeric'].mean()
    st.metric("Average Price", f"R {avg_price:,.2f}")

with col3:
    st.metric("Min Price", f"R {filtered_df['price_numeric'].min():,.2f}")

with col4:
    st.metric("Max Price", f"R {filtered_df['price_numeric'].max():,.2f}")

st.markdown("---")

# Charts Section
st.subheader("📈 Analytics & Visualizations")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Price Distribution", "🏷️ Brand Analysis", "📉 Price Trends", "🥧 Market Share"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Price histogram
        fig_hist = px.histogram(
            filtered_df, 
            x='price_numeric', 
            nbins=20,
            title='Price Distribution',
            labels={'price_numeric': 'Price (R)', 'count': 'Number of Products'},
            color_discrete_sequence=['#667eea']
        )
        fig_hist.update_layout(showlegend=False)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # Box plot by brand
        brand_counts = filtered_df['brand'].value_counts()
        top_brands = brand_counts[brand_counts >= 2].index.tolist()
        brand_data = filtered_df[filtered_df['brand'].isin(top_brands)]
        
        fig_box = px.box(
            brand_data, 
            x='brand', 
            y='price_numeric',
            title='Price Distribution by Brand (2+ products)',
            labels={'price_numeric': 'Price (R)', 'brand': 'Brand'},
            color='brand'
        )
        fig_box.update_layout(showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Brand count bar chart
        brand_counts = filtered_df['brand'].value_counts().head(15)
        fig_brand = px.bar(
            x=brand_counts.index, 
            y=brand_counts.values,
            title='Top 15 Brands by Product Count',
            labels={'x': 'Brand', 'y': 'Number of Products'},
            color=brand_counts.values,
            color_continuous_scale='Viridis'
        )
        fig_brand.update_layout(showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_brand, use_container_width=True)
    
    with col2:
        # Average price by brand
        avg_by_brand = filtered_df.groupby('brand')['price_numeric'].mean().sort_values(ascending=False).head(15)
        fig_avg = px.bar(
            x=avg_by_brand.index, 
            y=avg_by_brand.values,
            title='Top 15 Brands by Average Price',
            labels={'x': 'Brand', 'y': 'Average Price (R)'},
            color=avg_by_brand.values,
            color_continuous_scale='Reds'
        )
        fig_avg.update_layout(showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_avg, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        # Price categories
        def categorize_price(price):
            if price < 500:
                return 'Budget (< R500)'
            elif price < 1000:
                return 'Economy (R500-R1000)'
            elif price < 5000:
                return 'Mid-Range (R1000-R5000)'
            elif price < 10000:
                return 'Premium (R5000-R10000)'
            else:
                return 'Luxury (> R10000)'
        
        filtered_df['price_category'] = filtered_df['price_numeric'].apply(categorize_price)
        category_counts = filtered_df['price_category'].value_counts()
        
        fig_cat = px.bar(
            x=category_counts.index, 
            y=category_counts.values,
            title='Products by Price Category',
            labels={'x': 'Price Category', 'y': 'Number of Products'},
            color=category_counts.index,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_cat, use_container_width=True)
    
    with col2:
        # Scatter plot: Price vs Product (sorted)
        sorted_df = filtered_df.sort_values('price_numeric').reset_index(drop=True)
        sorted_df['rank'] = range(1, len(sorted_df) + 1)
        
        fig_scatter = px.scatter(
            sorted_df, 
            x='rank', 
            y='price_numeric',
            title='Price Distribution (Sorted Low to High)',
            labels={'rank': 'Product Rank', 'price_numeric': 'Price (R)'},
            hover_data=['product_name', 'brand'],
            color='brand'
        )
        fig_scatter.update_layout(showlegend=False)
        st.plotly_chart(fig_scatter, use_container_width=True)

with tab4:
    col1, col2 = st.columns(2)
    
    with col1:
        # Brand market share pie chart
        brand_counts = filtered_df['brand'].value_counts().head(10)
        fig_pie = px.pie(
            values=brand_counts.values, 
            names=brand_counts.index,
            title='Top 10 Brands Market Share (by product count)',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Revenue potential by brand (count * avg price)
        brand_revenue = filtered_df.groupby('brand').agg({
            'price_numeric': ['sum', 'count', 'mean']
        }).round(2)
        brand_revenue.columns = ['Total Value', 'Count', 'Avg Price']
        brand_revenue = brand_revenue.sort_values('Total Value', ascending=False).head(10)
        
        fig_revenue = px.bar(
            x=brand_revenue.index, 
            y=brand_revenue['Total Value'],
            title='Top 10 Brands by Total Inventory Value',
            labels={'x': 'Brand', 'y': 'Total Value (R)'},
            color=brand_revenue['Total Value'],
            color_continuous_scale='Blues'
        )
        fig_revenue.update_layout(showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_revenue, use_container_width=True)

st.markdown("---")

# Products Display Section
st.subheader(f"🛒 Products ({len(filtered_df)} items)")

# Sort options
sort_option = st.selectbox(
    "Sort by:",
    ["Price: Low to High", "Price: High to Low", "Name: A-Z", "Name: Z-A"]
)

if sort_option == "Price: Low to High":
    filtered_df = filtered_df.sort_values('price_numeric')
elif sort_option == "Price: High to Low":
    filtered_df = filtered_df.sort_values('price_numeric', ascending=False)
elif sort_option == "Name: A-Z":
    filtered_df = filtered_df.sort_values('product_name')
else:
    filtered_df = filtered_df.sort_values('product_name', ascending=False)

# Display products in grid
cols_per_row = 4
rows = [filtered_df.iloc[i:i+cols_per_row] for i in range(0, len(filtered_df), cols_per_row)]

for row_data in rows:
    cols = st.columns(cols_per_row)
    for idx, (_, product) in enumerate(row_data.iterrows()):
        with cols[idx]:
            with st.container():
                st.markdown(f"""
                <div class="product-card">
                    <div class="product-title">{product['product_name'][:50]}{'...' if len(product['product_name']) > 50 else ''}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Display image
                try:
                    st.image(product['image_url'], use_container_width=True)
                except:
                    st.image("https://via.placeholder.com/150?text=No+Image", use_container_width=True)
                
                st.markdown(f"**{product['price']}**")
                st.caption(f"Brand: {product['brand']}")

st.markdown("---")

# Data Table Section
with st.expander("📋 View Raw Data Table"):
    st.dataframe(
        filtered_df[['product_name', 'brand', 'price', 'price_numeric', 'image_url']],
        use_container_width=True,
        hide_index=True
    )
    
    # Download buttons
    col1, col2 = st.columns(2)
    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="filtered_products.csv",
            mime="text/csv"
        )
    with col2:
        json_data = filtered_df.to_json(orient='records', indent=2)
        st.download_button(
            label="📥 Download as JSON",
            data=json_data,
            file_name="filtered_products.json",
            mime="application/json"
        )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🏋️ Sportsman's Warehouse Product Dashboard | Data scraped from sportsmanswarehouse.co.za</p>
</div>
""", unsafe_allow_html=True)
