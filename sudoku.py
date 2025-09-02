import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

def jogar():
    st.set_page_config(page_title="Sudoku", page_icon="🔢")
    st.title("🔢 Sudoku Aleatório")

    if "tabuleiro" not in st.session_state:
        st.session_state.tabuleiro = None
        st.session_state.solucao = None

    tamanho = 9  # Sudoku padrão 9x9

    # --- Funções internas ---
    def gerar_tabuleiro_completo():
        """Gera um tabuleiro completo de Sudoku"""
        base = 3
        side = base*base
        def pattern(r,c): return (base*(r%base)+r//base+c)%side
        def shuffle(s): return random.sample(s,len(s))

        rBase = range(base)
        rows  = [g*base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols  = [g*base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums  = shuffle(range(1,side+1))

        board = [[nums[pattern(r,c)] for c in cols] for r in rows]
        return board

    def criar_puzzle(board, n_holes=40):
        """Remove números para criar puzzle"""
        puzzle = [row.copy() for row in board]
        for _ in range(n_holes):
            i,j = random.randint(0,8), random.randint(0,8)
            puzzle[i][j] = 0
        return puzzle

    def desenhar_tabuleiro(tabuleiro):
        fig, ax = plt.subplots(figsize=(6,6))
        ax.set_xlim(-0.5,8.5)
        ax.set_ylim(-0.5,8.5)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.invert_yaxis()

        # Desenhar números
        for i in range(9):
            for j in range(9):
                num = tabuleiro[i][j]
                ax.text(j, i, str(num) if num != 0 else "", ha='center', va='center', fontsize=16)

        # Linhas grossas para separar blocos 3x3
        for i in range(10):
            lw = 2 if i%3==0 else 1
            ax.plot([-0.5,8.5],[i-0.5,i-0.5], color='black', linewidth=lw)
            ax.plot([i-0.5,i-0.5],[-0.5,8.5], color='black', linewidth=lw)
        return fig

    # --- Botões ---
    if st.button("Gerar Sudoku"):
        tabuleiro_completo = gerar_tabuleiro_completo()
        puzzle = criar_puzzle(tabuleiro_completo, n_holes=40)
        st.session_state.tabuleiro = puzzle
        st.session_state.solucao = tabuleiro_completo

        st.subheader("Sudoku (Puzzle)")
        fig = desenhar_tabuleiro(st.session_state.tabuleiro)
        st.pyplot(fig)

    if st.session_state.tabuleiro is not None:
        if st.button("Mostrar Gabarito"):
            st.subheader("Sudoku (Puzzle)")
            fig1 = desenhar_tabuleiro(st.session_state.tabuleiro)
            st.pyplot(fig1)

            st.subheader("Sudoku (Gabarito)")
            fig2 = desenhar_tabuleiro(st.session_state.solucao)
            st.pyplot(fig2)
