import streamlit as st
from labirinto import jogar as jogar_labirinto
from cacapalavras import jogar as jogar_cacapalavras

st.title("🎮 Hub de Jogos")

jogo = st.selectbox("Escolha o jogo:", ["Selecione","Labirinto","Caça-Palavras"])

if jogo == "Labirinto":
    jogar_labirinto()
elif jogo == "Caça-Palavras":
    jogar_cacapalavras()
