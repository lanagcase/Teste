import pandas as pd  
import streamlit as st 
import plotly.express as px 
##from streamlit_extras.metric_cards import style_metric_cards 

@st.cache_data
def carregar_dados():
    
    df = pd.read_excel("Vendas.xlsx")

    return df

def main():

    st.set_page_config(layout="wide")

    st.title("Dashboard de Vendas 📊")

    df = carregar_dados()

    ano_filtrado = st.sidebar.selectbox("Filtrar por Ano:", ["Todos", *df["Ano"].unique()])

    # Aplicar filtro apenas se não for todos
    if ano_filtrado != "Todos":
        df_filtrado = df[df["Ano"] == ano_filtrado]
    else:
        df_filtrado = df

    total_custo = (df_filtrado["Custo"].sum()).astype(str)
    total_custo = total_custo.replace(".",",")
    total_custo = "R$" + total_custo[:2] + "." + total_custo[2:5] + "." + total_custo[5:]

    total_lucro = (df_filtrado["Lucro"].sum()).astype(str)
    total_lucro = total_lucro.replace(".",",")
    total_lucro = "R$" + total_lucro[:2] +"." + total_lucro[2:5] + "." + total_lucro[5:]

    total_clientes = df_filtrado["ID Cliente"].nunique()


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Custo", total_custo)
        ##style_metric_cards(border_left_color="#3e4095")

    with col2:
        st.metric("Total Lucro", total_lucro)
        
    
    
    with col3:
        st.metric("Total Clientes", total_clientes)
        

    st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 18px;
        color: rgba(0,0,0,0,)
    }
    </style>
    """,
    unsafe_allow_html=True,
    )

    produtos_vendidos_marca = df_filtrado.groupby("Marca")["Quantidade"].sum().sort_values(ascending=True).reset_index()

    lucro_categoria = df_filtrado.groupby("Categoria")["Lucro"].sum().reset_index()
    lucro_mes_categoria = df_filtrado.groupby(["mes_ano", "Categoria"])["Lucro"].sum().reset_index()

    col1, col2 = st.columns(2)

    fig = px.bar(produtos_vendidos_marca, x='Quantidade', y='Marca', orientation="h", 
             title="Total Produtos Vendidos por Marca", color_discrete_sequence=["#3e4095"], width=380, height=350, text="Quantidade")
    fig.update_layout(title_x= 0.2)
    fig.update_yaxes(automargin=True)
    col1.plotly_chart(fig, use_container_width=True)

    fig1 = px.pie(lucro_categoria, values='Lucro', names='Categoria', 
                  title='Lucro por Categoria', hole=0.6, width=380, height=350,
                  color_discrete_sequence=["#3e4095", "#EC610C"])
    fig1.update_layout(title_x= 0.4)

    col2.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(lucro_mes_categoria, x="mes_ano", y="Lucro", title='Lucro x Mês x Categoria', color="Categoria", markers=True)
    st.plotly_chart(fig2)






if __name__ == "__main__":
    main()