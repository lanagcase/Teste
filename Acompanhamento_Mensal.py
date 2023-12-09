import pandas as pd  
import streamlit as st 

@st.cache_data
def carregar_dados():
    
    df = pd.read_excel("Vendas.xlsx")

    return df

def main():


    st.set_page_config(layout="wide", page_icon="📊")
    
    df = carregar_dados()

    MoM = df.groupby(["mes_ano"])["Lucro"].sum().reset_index()
    MoM["LM"] = MoM["Lucro"].shift(1)
    MoM["Variação"] = MoM["Lucro"] - MoM["LM"]
    MoM["Variação%"] = MoM["Variação"] / MoM["LM"] * 100
    MoM["Variação%"] = MoM["Variação%"].map('{:.2f}%'.format)

    st.write(MoM)




if __name__ == "__main__":
    main()