import streamlit as st
import random
from build import mostrar_tabuleiro_visual, inicializar_tabuleiro

# Definindo a configuração da página
st.set_page_config(
    page_title="Meu Jogo de Tabuleiro",
    page_icon="🎲",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Configuração do tema
st.markdown(
    """
    <style>
        .stApp {
            background-color: #f5624d;
        }
        .stSidebar {
            background-color: #34a65f;
        }
        .stMenu, .stHeader {
            background-color: #323f6f;  /* Opcional: ajuste outras partes, se necessário */
        }
    </style>
    """, unsafe_allow_html=True
)


# Estilo personalizado para fundo completo
st.markdown(
    """
    <style>
        body {
            background-color: #235E6F !important;
            margin: 0;
            padding: 0;
            overflow: hidden;
        }
        .block-container {
            background-color: #235E6F;
            padding: 2rem;
            border-radius: 10px;
            max-width: 1300px;
        }
        .stButton>button {
            background-color: #CC231E;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #FF4B4B;
        }
        .sidebar .stButton>button {
            background-color: #34A65F;
        }
        .sidebar .stButton>button:hover {
            background-color: #46B97A;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Estilização da Sidebar com cor verde

st.markdown("""
    <style>
        [data-testid="stSidebar"] {{
            background-color: #34A65F;
        }}
        [data-testid="stSidebar"] h1, h2, h3, h4, h5, h6 {{
            color: white;
        }}
        [data-testid="stSidebar"] label {{
            color: white;
        }}
    </style>
""" , 
unsafe_allow_html=True)

    # Função para exibir a notificação usando st.toast
def exibir_toast(jogador, movimento, casa_atual):
    st.toast(
        f"🎲 {jogador} rolou o dado! 🎲\n"
        f"Resultado: {movimento}\n"
        f"📍 Nova Casa: {casa_atual}",
        icon="🎉"
    )

def alterar_posicao_jogador():
    jogador_escolhido = st.session_state.jogador_selecionado
    alteracao = st.session_state.numero_casas

    # Atualiza a posição do jogador escolhido
    nova_posicao = st.session_state.posicoes[jogador_escolhido] + alteracao

    # Garante que o jogador não ultrapasse os limites do tabuleiro
    nova_posicao = max(0, min(nova_posicao, len(st.session_state.tabuleiro) - 1))

    # Atualiza a posição do jogador
    st.session_state.posicoes[jogador_escolhido] = nova_posicao

    # Exibe um feedback na barra lateral
    st.sidebar.info(
        f"🔄 {st.session_state.jogadores[jogador_escolhido]} foi movido para a casa {nova_posicao}."
    )

def _atualizar_tabuleiro():
    jogador_atual = st.session_state.turno % len(st.session_state.jogadores)
    movimento = random.randint(1, 6)  # Simular a rolagem do dado
    nova_posicao = st.session_state.posicoes[jogador_atual] + movimento
    # Verifica se o jogador alcançou ou ultrapassou a última casa
    if nova_posicao >= len(st.session_state.tabuleiro) - 1:
        st.session_state.posicoes[jogador_atual] = len(st.session_state.tabuleiro) - 1
        st.sidebar.success(f"🎉 {nome_jogador} chegou ao Fim e venceu o jogo! 🎉")
        st.stop()
    else:
        st.session_state.posicoes[jogador_atual] = nova_posicao

    # Exibe o toast com os resultados
    exibir_toast(nome_jogador, movimento, st.session_state.tabuleiro[nova_posicao])

    # Atualiza o histórico com os resultados 
    st.session_state.historico.append( f"{emoji_jogador} {nome_jogador} rolou {movimento} e foi para a casa {nova_posicao}." )

    # Avança para o próximo turno
    st.session_state.turno += 1


# Configuração inicial
if "jogadores" not in st.session_state:
    st.session_state.jogadores = []
    st.session_state.emojis = []
    st.session_state.posicoes = []
    st.session_state.historico = []
    st.session_state.turno = 0
    st.session_state.jogo_iniciado = False

# Emojis disponíveis
emojis_disponiveis = ["😀", "😎", "🥳", "🎅", "🎄", "🤶"]


# Tabuleiro inicial
if "tabuleiro" not in st.session_state:
    inicializar_tabuleiro()

# Layout inicial da tela de configuração dos jogadores
def player_screen_layout():
    col1, col2, col3 = st.columns(3)
    col1.write(' ')
    col2.image('natal/logo.png', width=350)
    col3.write(' ')
        
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">
            <h2 style="color:white; text-align:center;">🎅 Configure os Jogadores 🎅</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

jogadores_predefinidos = [
    ("Tiago", "🎅"),
    ("Amanda", "🦌"),
    ("Joao", "⛄"),
    ("Alisson", "🧝"),
    ("Lara", "⭐"),
    ("Clara", "🎁"),
    ("Igor", "🍪"),
    ("Camilla", "🎄"),
    ("Bebel", "🔔"),
    ("Lucas", "❄️"),
]

# Configuração dos jogadores
if not st.session_state.jogo_iniciado:
    player_screen_layout()
    st.sidebar.write("## Configuração 🎅")
    # Inicializa listas de jogadores e emojis se ainda não estiverem no estado
    if "jogadores" not in st.session_state:
        st.session_state.jogadores = []
        st.session_state.emojis = []
        st.session_state.posicoes = []
        st.session_state.turno = 0


    if st.sidebar.button("Usar Jogadores Predefinidos"):
        st.session_state.jogadores = []
        st.session_state.emojis = []
        st.session_state.posicoes = []
        st.session_state.turno = 0

        for jogador in jogadores_predefinidos:
            nome, emoji = jogador
            st.session_state.jogadores.append(nome)
            st.session_state.emojis.append(emoji)

        st.session_state.posicoes = [0] * 10  # Inicializa as posições dos jogadores
        random.shuffle(st.session_state.jogadores)  # Aleatoriza a ordem dos jogadores
        st.session_state.jogo_iniciado = True
    
    else:
        num_jogadores = st.sidebar.number_input("Número de jogadores", min_value=2, max_value=4, step=1, key="num_jogadores")

        for i in range(num_jogadores):
            nome = st.sidebar.text_input(f"Nome do jogador {i + 1}", key=f"jogador_{i}")
            # Usando st.radio para seleção do emoji
            emoji = st.sidebar.radio(f"Escolha o emoji do jogador {i + 1}", options=emojis_disponiveis, key=f"emoji_{i}")

            # Atualiza as listas de jogadores e emojis no estado
            if len(st.session_state.jogadores) > i:
                st.session_state.jogadores[i] = nome
                st.session_state.emojis[i] = emoji
            else:
                st.session_state.jogadores.append(nome)
                st.session_state.emojis.append(emoji)

        if st.sidebar.button("Iniciar Jogo 🎅"):
            if all(st.session_state.jogadores):  # Verifica se todos os jogadores preencheram os dados
                st.session_state.posicoes = [0] * num_jogadores  # Inicializa as posições dos jogadores
                random.shuffle(st.session_state.jogadores)  # Aleatoriza a ordem dos jogadores
                st.session_state.jogo_iniciado = True
            else:
                st.sidebar.error("Preencha todos os nomes e emojis antes de começar!")
else:
    mostrar_tabuleiro_visual()
    jogador_atual = st.session_state.turno % len(st.session_state.jogadores)
    nome_jogador = st.session_state.jogadores[jogador_atual]
    emoji_jogador = st.session_state.emojis[jogador_atual]

    # Sidebar
    st.sidebar.write(f"## 🎲 Turno de {nome_jogador} {emoji_jogador}")


    # Botão de "Jogar Dados" com callback
    if not st.session_state.get("jogo_vencido", False):
        st.sidebar.button("🎲 Jogar Dados", on_click=_atualizar_tabuleiro)
    else:
        st.sidebar.success(st.session_state.mensagem)

    # Interface na barra lateral
    st.sidebar.header("Alterar Posição de Jogadores")

    # Dropdown para selecionar o jogador
    jogadores_dropdown = {
        i: nome for i, nome in enumerate(st.session_state.jogadores)
    }
    st.sidebar.selectbox(
        "Selecione o jogador:",
        options=list(jogadores_dropdown.keys()),
        format_func=lambda x: jogadores_dropdown[x],
        key="jogador_selecionado",
    )

    # Input para o número de casas
    st.sidebar.number_input(
        "Número de casas (positivo para avançar, negativo para voltar):",
        min_value=-len(st.session_state.tabuleiro),
        max_value=len(st.session_state.tabuleiro),
        value=0,
        step=1,
        key="numero_casas",
    )

    # Botão para executar a ação
    if st.sidebar.button("Alterar Posição"):
        alterar_posicao_jogador()

# Exibição do tabuleiro
if st.session_state.jogo_iniciado:
    st.sidebar.markdown("---")
    # Exibe informações do turno atual
    st.sidebar.write("## 🚦 Status dos Jogadores")
    
    # Ordena os jogadores por proximidade ao final
    jogadores_ordenados = sorted(
        zip(st.session_state.jogadores, st.session_state.emojis, st.session_state.posicoes),
        key=lambda x: x[2],  # Ordena pela posição no tabuleiro
        reverse=True
    )
    
    for nome, emoji, posicao in jogadores_ordenados:
        casa_atual = st.session_state.tabuleiro[posicao]
        st.sidebar.write(f"{emoji} **{nome}**: {casa_atual}")

    # Espaçamento entre seções
    st.sidebar.markdown("---")

    # Histórico de jogadas estilizado
    st.sidebar.write("## 📜 Histórico de Jogadas")
    if "historico" not in st.session_state:
        st.session_state.historico = []  # Inicializa o histórico

    # HTML para estilizar o histórico
    historico_html = """
    <div style="background-color: #235E6F; color: white; padding: 10px; border-radius: 5px; height: 200px; overflow-y: scroll; font-size: 14px;">
    """
    for entrada in st.session_state.historico:
        historico_html += f"<p>{entrada}</p>"
    historico_html += "</div>"

    st.sidebar.markdown(historico_html, unsafe_allow_html=True)

    # Atualiza o histórico ao final de cada turno
    jogador_atual = st.session_state.turno % len(st.session_state.jogadores)
    nome_jogador = st.session_state.jogadores[jogador_atual]
    emoji_jogador = st.session_state.emojis[jogador_atual]

    if "nova_posicao" in st.session_state:
        movimento = st.session_state.nova_posicao - st.session_state.posicoes[jogador_atual] + movimento  # Calcula o movimento
        st.session_state.historico.append(
            f"{emoji_jogador} {nome_jogador} rolou {movimento} e foi para a casa {st.session_state.nova_posicao}."
        )
        
    st.sidebar.markdown("---")

    # Botão de reiniciar o jogo
    if st.sidebar.button("🔄 Reiniciar Jogo"):
        st.session_state.jogadores = []
        st.session_state.emojis = []
        st.session_state.posicoes = []
        st.session_state.turno = 0
        st.session_state.jogo_iniciado = False
        st.experimental_rerun()