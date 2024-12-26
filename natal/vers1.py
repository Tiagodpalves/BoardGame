import streamlit as st
import random

# Configuração da página
st.set_page_config(layout="centered", page_title="Jogo de Tabuleiro")

# Estilo personalizado para aumentar a largura central
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1300px;  /* Altere esse valor para ajustar a largura */
        padding: 2rem;  /* Espaçamento interno */
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Configuração inicial
if "jogadores" not in st.session_state:
    st.session_state.jogadores = []
    st.session_state.emojis = []
    st.session_state.posicoes = []
    st.session_state.turno = 0
    st.session_state.jogo_iniciado = False

# Emojis disponíveis para escolha
emojis_disponiveis = ["😀", "😎", "🥳", "🎅", "🎄", "🤶"]

# Ordem das casas em espiral
ordem_casas = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
    19, 29, 39, 49, 59, 69, 79, 89, 99, 
    98, 97, 96, 95, 94, 93, 92, 91, 
    90, 80, 70, 60, 50, 40, 30, 20, 
    21, 22, 23, 24, 25, 26, 27, 
    37, 47, 57, 67, 77, 
    76, 75, 74, 73, 72,
    62,52,42,43,44,45,55,54
]

# Configuração do tabuleiro inicial
if "tabuleiro" not in st.session_state:
    num_casas = len(ordem_casas)
    st.session_state.tabuleiro = ["Início"] + [f"Desafio {i}" for i in range(1, num_casas - 1)] + ["Fim"]

# Função para exibir o tabuleiro visual
def mostrar_tabuleiro_visual():
    st.write("### Tabuleiro:")
    grid_size = 10
    tabuleiro_grid = [[""] * grid_size for _ in range(grid_size)]

    # Preenche o tabuleiro no grid 10x10 em formato espiral
    for idx, pos in enumerate(ordem_casas):
        row = pos // grid_size
        col = pos % grid_size
        tabuleiro_grid[row][col] = idx

    for row in tabuleiro_grid:
        cols = st.columns(grid_size)
        for col_idx, cell in enumerate(row):
            if cell == "":
                bg_color = "#235E6F"  # Espaços vazios
                texto = ""
            else:
                texto = st.session_state.tabuleiro[cell]
                bg_color = (
                    "#CC231E" if texto == "Início" or texto == "Fim" else "#34A65F"
                )
                jogadores_na_casa = [
                    emoji
                    for emoji, pos in zip(st.session_state.emojis, st.session_state.posicoes)
                    if pos == cell
                ]
                texto += "\n" + " ".join(jogadores_na_casa)

            with cols[col_idx]:
                st.markdown(
                    f"<div style='background-color:{bg_color};margin:3px; "
                    f"padding:10px; text-align:center; height:120px; width:120px;'>"
                    f"<b>{texto}</b></div>",
                    unsafe_allow_html=True,
                )

# Estilo personalizado com CSS para fundo
st.markdown(
    """
    <style>
    body {
        background-color: #235E6F;
    }
    .stButton>button {
        background-color: #ff4b4b;
      
    .stButton>button:hover {
        background-color: #ff6666;
    }
    .block-container {
        background-color: #235E6F;
        padding: 2rem;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Configuração dos jogadores
if not st.session_state.jogo_iniciado:
    st.write("## Configuração do Jogo 🎄")
    num_jogadores = st.number_input("Número de jogadores", min_value=2, max_value=4, step=1, key="num_jogadores")

    st.write("### Insira os nomes e escolha os emojis:")
    configuracao_completa = True
    for i in range(num_jogadores):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input(f"Nome do jogador {i + 1}", key=f"jogador_{i}")
        with col2:
            emoji = st.selectbox(f"Emoji do jogador {i + 1}", options=emojis_disponiveis, key=f"emoji_{i}")

        if not nome or not emoji:
            configuracao_completa = False
        else:
            if i >= len(st.session_state.jogadores):
                st.session_state.jogadores.append(nome)
                st.session_state.emojis.append(emoji)

    if st.button("Iniciar jogo 🎅", key="iniciar_jogo"):
        if configuracao_completa:
            st.session_state.posicoes = [0] * num_jogadores
            random.shuffle(st.session_state.jogadores)
            st.session_state.jogo_iniciado = True
        else:
            st.error("Por favor, preencha todos os nomes e emojis antes de começar!")
else:
    mostrar_tabuleiro_visual()

    # Controles do jogo
    st.write("### Controle do Jogo:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Jogar Dados 🎲"):
            jogador_atual = st.session_state.turno % len(st.session_state.jogadores)
            movimento = random.randint(1, 6)
            posicao_atual = st.session_state.posicoes[jogador_atual]
            nova_posicao = posicao_atual + movimento
            if nova_posicao >= len(ordem_casas) - 1:
                nova_posicao = len(ordem_casas) - 1
                st.success(f"{st.session_state.jogadores[jogador_atual]} chegou ao fim do jogo!")
            else:
                st.info(
                    f"{st.session_state.jogadores[jogador_atual]} avançou {movimento} casas para a posição {nova_posicao}!"
                )
            st.session_state.posicoes[jogador_atual] = nova_posicao
            st.session_state.turno += 1
    with col2:
        if st.button("Reiniciar Jogo 🔄"):
            st.session_state.jogo_iniciado = False
            st.session_state.posicoes = []
            st.session_state.jogadores = []
            st.session_state.emojis = []
            st.session_state.turno = 0
            st.experimental_rerun()
