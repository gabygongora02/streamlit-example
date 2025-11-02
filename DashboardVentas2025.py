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
def create_sales_bar_chart(df_top_products, title):
    fig = px.bar(df_top_products, x='Product Name', y='Sales', title=title, text_auto=True)
    fig.update_layout(xaxis=dict(tickangle=-45, automargin=True, tickfont=dict(size=10)), yaxis=dict(title='Sales'), xaxis_title='Product Name')
    return fig

# Function to create bar chart for profit
def create_profit_bar_chart(df_top_profit_products, title):
    fig = px.bar(df_top_profit_products, x='Product Name', y='Profit', title=title)
    fig.update_layout(xaxis=dict(tickangle=-45, automargin=True, tickfont=dict(size=10)), yaxis=dict(title='Profit'), xaxis_title='Product Name')
    return fig

# Streamlit App
def main():
    st.title("Análisis de Ventas y Ganancias de Productos")

    file_path = "SalidaVentas.xlsx"
    df = load_data(file_path)

    st.sidebar.header("Filtros")

    region_options = ['Todas'] + list(df['Region'].unique())
    selected_region = st.sidebar.selectbox("Selecciona una Región", region_options)

    filtered_df = df

    if selected_region != 'Todas':
        filtered_df = df[df['Region'] == selected_region]
        state_options = ['Todos'] + list(filtered_df['State'].unique())
        selected_state = st.sidebar.selectbox(f"Selecciona un Estado en {selected_region}", state_options)

        if selected_state != 'Todos':
            filtered_df = filtered_df[filtered_df['State'] == selected_state]
            sales_title = f"Top 5 Productos por Ventas en {selected_state}, {selected_region}"
            profit_title = f"Top 5 Productos por Ganancia en {selected_state}, {selected_region}"
        else:
            sales_title = f"Top 5 Productos por Ventas en {selected_region}"
            profit_title = f"Top 5 Productos por Ganancia en {selected_region}"
    else:
        sales_title = "Top 5 Productos por Ventas en todas las Regiones"
        profit_title = "Top 5 Productos por Ganancia en todas las Regiones"

    st.sidebar.markdown("---")
    show_dataframe = st.sidebar.checkbox("Mostrar DataFrame Filtrado")

    if show_dataframe:
        st.write("Datos filtrados:")
        st.dataframe(filtered_df)

    st.header(sales_title)
    top_sales_products = get_top_products_by_sales(filtered_df)
    sales_fig = create_sales_bar_chart(top_sales_products, sales_title)
    st.plotly_chart(sales_fig)

    st.header(profit_title)
    top_profit_products = get_top_products_by_profit(filtered_df)
    profit_fig = create_profit_bar_chart(top_profit_products, profit_title)
    st.plotly_chart(profit_fig)

if __name__ == "__main__":
    main()
