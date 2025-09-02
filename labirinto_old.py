import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
from collections import deque

# --- Função para gerar labirinto ---
def gerar_labirinto(n=15, m=15):
    maze = np.ones((n, m))
    stack = [(1,1)]
    maze[1,1] = 0

    while stack:
        x, y = stack[-1]
        vizinhos = []
        for dx, dy in [(2,0), (-2,0), (0,2), (0,-2)]:
            nx, ny = x+dx, y+dy
            if 1 <= nx < n-1 and 1 <= ny < m-1 and maze[nx, ny] == 1:
                vizinhos.append((nx, ny, dx, dy))
        if vizinhos:
            nx, ny, dx, dy = random.choice(vizinhos)
            maze[nx-dx//2, ny-dy//2] = 0
            maze[nx, ny] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    # Entrada e saída
    maze[1,0] = 0
    maze[n-2,m-1] = 0
    return maze

# --- Função para resolver ---
def resolver_labirinto(maze):
    start = (1,0)
    end = (len(maze)-2, len(maze[0])-1)
    fila = deque([(start, [start])])
    visitados = set()

    while fila:
        (x,y), caminho = fila.popleft()
        if (x,y) == end:
            return caminho
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x+dx, y+dy
            if (
                0 <= nx < len(maze)
                and 0 <= ny < len(maze[0])
                and maze[nx, ny] == 0
                and (nx, ny) not in visitados
            ):
                fila.append(((nx,ny), caminho+[(nx,ny)]))
                visitados.add((nx,ny))
    return None

# ------------------------------
# INTERFACE STREAMLIT
# ------------------------------
st.set_page_config(page_title="Gerador de Labirintos", page_icon="🌀")

st.title("🌀 Gerador de Labirintos")
st.write("Escolha o tamanho e clique nos botões para gerar ou resolver o labirinto.")

# Entrada do usuário
n = st.slider("Altura do labirinto (ímpar)", 11, 51, 21, step=2)
m = st.slider("Largura do labirinto (ímpar)", 11, 51, 21, step=2)

# Inicializar variáveis na sessão
if "maze" not in st.session_state:
    st.session_state.maze = None
if "solucao" not in st.session_state:
    st.session_state.solucao = None

# Botão para gerar labirinto
if st.button("Gerar Labirinto"):
    st.session_state.maze = gerar_labirinto(n, m)
    st.session_state.solucao = None  # resetar solução

    st.subheader("Labirinto (atividade)")
    fig, ax = plt.subplots(figsize=(5,5))
    ax.imshow(st.session_state.maze, cmap="binary")
    ax.axis("off")
    st.pyplot(fig)

# Mostrar botão do gabarito só se já existir um labirinto
if st.session_state.maze is not None:
    if st.button("Mostrar Gabarito"):
        if st.session_state.solucao is None:
            st.session_state.solucao = resolver_labirinto(st.session_state.maze)

        # Mostrar labirinto (atividade)
        st.subheader("Labirinto (atividade)")
        fig, ax = plt.subplots(figsize=(5,5))
        ax.imshow(st.session_state.maze, cmap="binary")
        ax.axis("off")
        st.pyplot(fig)

        # Mostrar labirinto (gabarito)
        st.subheader("Labirinto (gabarito)")
        fig, ax = plt.subplots(figsize=(5,5))
        ax.imshow(st.session_state.maze, cmap="binary")
        if st.session_state.solucao:
            y_coords = [p[1] for p in st.session_state.solucao]
            x_coords = [p[0] for p in st.session_state.solucao]
            ax.plot(y_coords, x_coords, color="red", linewidth=1.5)
        ax.axis("off")
        st.pyplot(fig)
