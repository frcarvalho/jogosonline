import streamlit as st
from labirinto import jogar as jogar_labirinto
from cacapalavras import jogar as jogar_cacapalavras
from sudoku import jogar as jogar_sudoku

st.title("🎮 Hub de Jogos")

jogo = st.selectbox("Escolha o jogo:", ["Selecione","Labirinto","Caça-Palavras", "Sudoku"])

if jogo == "Labirinto":
    jogar_labirinto()
elif jogo == "Caça-Palavras":
    jogar_cacapalavras()
elif jogo == "Sudoku":
    jogar_sudoku()