import streamlit as st
import random
import string
import matplotlib.pyplot as plt
import numpy as np

# --- Função para gerar grade ---
def gerar_grade(palavras, tamanho=15, max_tentativas=100):
    grid = [["" for _ in range(tamanho)] for _ in range(tamanho)]
    palavras_pos = []

    direcoes = [(0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]

    for palavra in palavras:
        palavra = palavra.upper()
        colocado = False
        tentativas = 0

        while not colocado and tentativas < max_tentativas:
            tentativas += 1
            dirx, diry = random.choice(direcoes)
            x = random.randint(0, tamanho-1)
            y = random.randint(0, tamanho-1)

            endx = x + dirx*(len(palavra)-1)
            endy = y + diry*(len(palavra)-1)
            if not (0 <= endx < tamanho and 0 <= endy < tamanho):
                continue

            valido = True
            for i in range(len(palavra)):
                nx, ny = x + dirx*i, y + diry*i
                if grid[nx][ny] not in ("", palavra[i]):
                    valido = False
                    break
            if not valido:
                continue

            for i in range(len(palavra)):
                nx, ny = x + dirx*i, y + diry*i
                grid[nx][ny] = palavra[i]

            palavras_pos.append((palavra, (x,y), (endx,endy)))
            colocado = True

    # Preenche espaços vazios
    for i in range(tamanho):
        for j in range(tamanho):
            if grid[i][j] == "":
                grid[i][j] = random.choice(string.ascii_uppercase)

    return grid, palavras_pos

# --- Função para desenhar grade ---
def desenhar_grade(grid, posicoes=None, destacar=False):
    tamanho = len(grid)
    fig, ax = plt.subplots(figsize=(tamanho/2, tamanho/2))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-0.5, tamanho-0.5)
    ax.set_ylim(-0.5, tamanho-0.5)
    ax.invert_yaxis()

    # desenhar letras
    for i in range(tamanho):
        for j in range(tamanho):
            ax.text(j, i, grid[i][j], ha='center', va='center', fontsize=12)

    # destacar palavras se necessário
    if destacar and posicoes:
        for _, (x1,y1), (x2,y2) in posicoes:
            ax.plot([y1,y2],[x1,x2], color='red', linewidth=2)

    return fig

# --- Lista de palavras disponíveis ---
lista_palavras = [
    "FLAMENGO","GATO","CASA","AMOR","SOL","LUZ",
    "FLORESTA","MAR","LIVRO","MUSICA","VIAGEM","SONHO",
    "PAZ","FAMILIA","ESTRELA","MAGIA","NATUREZA","RIO"
]

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Caça-Palavras", page_icon="🧩")
st.title("🧩 Caça-Palavras Aleatório")

# Tamanho da grade
tamanho = st.slider("Tamanho da grade", 8, 20, 15)

# Quantidade de palavras
max_palavras = len(lista_palavras)
qtd = st.slider("Quantidade de palavras", 1, max_palavras, min(8, max_palavras))

# Inicializar sessão
if "grid" not in st.session_state:
    st.session_state.grid = None
if "posicoes" not in st.session_state:
    st.session_state.posicoes = None
if "palavras" not in st.session_state:
    st.session_state.palavras = None

# Botão gerar caça-palavras
if st.button("Gerar Caça-Palavras"):
    palavras = random.sample(lista_palavras, qtd)
    grid, posicoes = gerar_grade(palavras, tamanho)
    st.session_state.grid = grid
    st.session_state.posicoes = posicoes
    st.session_state.palavras = palavras

    st.subheader("Palavras a encontrar:")
    st.write(", ".join([p.upper() for p in palavras]))

    st.subheader("Caça-Palavras")
    fig = desenhar_grade(grid)
    st.pyplot(fig)

# Botão mostrar gabarito somente se já gerou
if st.session_state.grid is not None:
    if st.button("Mostrar Gabarito"):
        st.subheader("Caça-Palavras")
        fig1 = desenhar_grade(st.session_state.grid)
        st.pyplot(fig1)

        st.subheader("Gabarito")
        fig2 = desenhar_grade(st.session_state.grid, st.session_state.posicoes, destacar=True)
        st.pyplot(fig2)
