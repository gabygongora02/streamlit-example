import pandas as pd
import plotly.express as px
import streamlit as st

# Function to load data
@st.cache_data
def load_data(file_path):
    df = pd.read_excel(file_path)
    return df

# Function to get top products by sales
def get_top_products_by_sales(df, n=5):
    product_sales = df.groupby('Product Name')[['Sales', 'Quantity']].sum().reset_index()
    top_products = product_sales.sort_values(by='Sales', ascending=False).head(n)
    return top_products

# Function to get top products by profit
def get_top_products_by_profit(df, n=5):
    product_sales_profit = df.groupby('Product Name')[['Sales', 'Profit']].sum().reset_index()
    top_profit_products = product_sales_profit.sort_values(by='Profit', ascending=False).head(n)
    return top_profit_products

# Function to create bar chart for sales
def create_sales_bar_chart(df_top_products):
    fig = px.bar(df_top_products, x='Product Name', y='Sales', title='Top 5 Products by Sales', text_auto=True)
    fig.update_layout(xaxis=dict(tickangle=-45, automargin=True, tickfont=dict(size=10)), yaxis=dict(title='Sales'), xaxis_title='Product Name')
    return fig

# Function to create bar chart for profit
def create_profit_bar_chart(df_top_profit_products):
    fig = px.bar(df_top_profit_products, x='Product Name', y='Profit', title='Top 5 Products by Profit')
    fig.update_layout(xaxis=dict(tickangle=-45, automargin=True, tickfont=dict(size=10)), yaxis=dict(title='Profit'), xaxis_title='Product Name')
    return fig

# Streamlit App
def main():
    st.title("Análisis de Ventas y Ganancias de Productos")

    file_path = "SalidaVentas.xlsx"
    df = load_data(file_path)

    st.write("Datos cargados exitosamente:")
    st.dataframe(df.head())

    st.header("Top 5 Productos por Ventas")
    top_sales_products = get_top_products_by_sales(df)
    sales_fig = create_sales_bar_chart(top_sales_products)
    st.plotly_chart(sales_fig)

    st.header("Top 5 Productos por Ganancia")
    top_profit_products = get_top_products_by_profit(df)
    profit_fig = create_profit_bar_chart(top_profit_products)
    st.plotly_chart(profit_fig)

if __name__ == "__main__":
    main()
