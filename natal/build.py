import streamlit as st
import random

# Ordem das casas em espiral
ordem_casas = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 19, 29, 39, 49, 59, 69, 79, 89, 99, 98, 97, 96, 95, 94,
    93, 92, 91, 90, 80, 70, 60, 50, 40, 30, 20, 21, 22, 23, 24, 25, 26, 27, 37, 47, 57, 
    67, 77, 76, 75, 74, 73, 72, 62, 52, 42, 43, 44, 45, 55, 54
]

# Listas das frases
# Lista de benefícios
beneficios = {
    "Atalho encontrado": "Avance 3 casas e escolha um jogador para beber.",
    "Sorte grande": "Role o dado novamente e avance o número tirado. Todos os outros bebem.",
    "Imunidade": "Você ganhou um passe livre a um desafio. Brinde à sua sorte! (Bebe Porra)",
    "Troca de lugar": "Troque de lugar com o jogador à sua frente. Ele bebe por isso!",
    "Juiz da rodada": "Escolha 2 jogadores para beber!",
}


# Lista de penalidades
penalidades = {
    "Caminho errado": "Volte 3 casas e beba o número do dado.",
    "Confusão": "Você ficou confuso e perdeu a vez. Beba 2 shots e reflita sobre seus erros.",
    "Castigo numérico": "O número que você tirou no dado agora é seu castigo em shots.",
    "Sem avançar": "Todos jogam novamente, mas você não pode avançar!",
    "Brinde coletivo": "Você paga um brinde coletivo e assiste todos beberem!",
    "Vento contrário": "O avanço foi interrompido. Volte 2 casas e beba 2 shots.",
    "Estratégia falha": "Perde uma rodada enquanto bebe 2 shots para planejar melhor.",
    "Desequilíbrio": "Avance 1 casa, mas beba 5 shots para compensar. Ou, retorne 3.",
    "Tropeço": "Volte para a última casa de desafio.",
    "Pausa necessária": "Fique 1 rodada sem jogar e beba 2 shots enquanto observa.",
    "Travessia perigosa": "Avance 2 casas, mas distribua 5 shots para os outros jogadores.",
    "Encruzilhada": "Escolha: volte 3 casas ou beba 2 shots.",
    "Falta de sorte": "Passe sua próxima jogada e beba 1 shots.",
    "Cansaço": "Avance 1 casa e escolha alguém para beber 1 shots com você.",
    "Destino cruel": "Volte para a casa inicial do último benefício.",
    "Rota alternativa": "Fique parado e distribua 3 shots entre os jogadores.",
}


desafios = {
    "Quem é o mais bonito?": "Escolha o mais bonito para beber.",
    "Solterio Forçado": "Escolha o jogador que ja esteve Friendzone para beber.",
    "Ihaaiinnnn!": "Imite a Pablo por uma rodada se falhar beba.",
    "Bala de IceKiss": "Vejo o video e se errar um dos nomes da Diva beba!",
    "Alcoolismo": "Foi um ano dificil beba 3 shots e fale 3 arrpendimentos a cada gole.",
    "O último romântico": "Declare seu amor (falso ou verdadeiro) para alguém. Se ninguém acreditar, beba 2 shots.",
    "Verdades secretas": "Revele um segredo e 2 mentiras, quem quiser saber beba!",
    "Roleplay inusitado": "Finja ser um professor sexy por 30 segundos. Se não convencer, beba 2 shots.",
    "Golpe de Insta": "Fale quem foi a ultima pessoa que voce bloqueou, ou beba 3 shots.",
    "Fetiche ou Fanfic?": "Confesse um fetiche. Se não quiser, tome 2 shots.",
    "Karaokê da vergonha": "Cante um trecho de um hit sertanejo ou pague 2 shots.",
    "O emoji proibido": "Desenhe seu emoji favorito no ar. Se ninguém entender, beba 2 shots.",
    "Influencer de plantão": "Simule uma campanha de marketing estranha para algo na sala. Se rir durante, tome 2 shots.",
    "Curiosidade picante": "Pergunte algo constrangedor para o próximo jogador. Se ele não responder, ambos bebem 2 shots.",
    "Vai, Safadão!": "Recrie uma pose sexual famosa. Se for tímido, tome 2 shots.",
    "Modo filosófico": "Responda: 'O que é mais importante, amor ou cerveja?' Quem discordar, bebe 1 gole.",
    "Roleta sensual": "Distribua 3 shots sensualmente no colo da pessoa da sua escolha.",
    "Mesmo barco": "Todos devem entrar em uma rodadada de verdade ou desafio, mas com um alvo em comum",
    

    "Dublagem épica": "Duble uma cena famosa. Se ninguém adivinhar, beba 2 shots.",
    "Tinder real life": "De like ou deslike para todos jogadores, se recusar beba 2 shots",
    "Confissão ousada": "Conte algo que fez e nunca revelou para ninguém. Se não quiser, tome 3 shots.",
    "Segredo dos lábios": "Sussurre algo picante para o jogador ao lado. Se ele não corar, você bebe 2 shots.",
    "Papel invertido": "Finja ser o jogador à sua esquerda por uma rodada. Se não convencer, beba 2 shots.",
    "Cantada infalível": "Dê uma cantada em alguém no grupo. Se não arrancar risadas ou aplausos, tome 2 shots.",
    "Desafio da verdade": "Responda: 'Você já mandou mensagem para alguém bêbado?', beba 2 shots.",
    "Strip ou shot": "Escolha: tire uma peça de roupa ou faça um bodyshot.",
    "Brinquedinho": "Conte algo que ja comprou em um sex shop",
}



# Lista de normais
normais = {
    "Todos bebem": "Todos os jogadores devem beber.",
    "Meninas bebem": "Apenas as meninas devem beber.",
    "Meninos bebem": "Apenas os meninos devem beber.",
    "Hora do Hulk": "O jogador mais forte deve beber.",
    "Quem vê de cima?": "O jogador mais alto deve beber.",
    "O pequeno gigante": "O jogador mais baixo deve beber.",
    "Quem paga o próximo drink?": "O jogador mais rico deve beber.",
    "Fugiu de desafios?": "Se você evitou 1 desafio, hora de beber.",
    "Quem está na frente?": "O jogador imediatamente à sua frente deve beber.",
    "Direita!": "Passe a bebida para o jogador à sua direita.",
    "Esquerda!": "Passe a bebida para o jogador à sua esquerda.",
    "Facista!": "Passe a bebida para o segundo jogador à sua direita.",
    "Comunista!": "Passe a bebida para o segundo jogador à sua esquerda.",
    "Brinde a alguém!": "Escolha um jogador para beber e brinde a ele.",
    "Quem está ganhando?": "O jogador na liderança deve beber.",
    "Mais distante do fim": "O jogador mais longe do final deve beber.",
    "Brinde coletivo": "Quem esta na mesma casa brinda e bebe junto.",
    "Invente uma regra": "Crie uma regra para a rodada. Quem desobedecer, bebe.",
    "Vermelho": "Se você está usando algo vermelho, beba.",
    "Post nas redes": "Se você postou algo nas redes sociais hoje, beba.",
    "Mais desafios concluídos": "O jogador com mais desafios concluídos escolhe quem bebe.",
    "Número par no dado": "Jogue o dado se tirar par beba.",
    "Atrás de você": "Todos os jogadores atrás de você no tabuleiro bebem.",
    "Bebeu água?": "Quem bebeu água antes do jogo agora bebe o dobro.",
    "Penalidade": "Se você já caiu em uma casa de penalidade, beba 1 shots.",
    "Nome mais curto": "O jogador com o nome mais curto bebe.",
    "Nome com vogal": "Jogadores cujo nome começa com vogal devem beber.",
    "Segurando o copo": "Quem estiver segurando o copo deve beber.",
    "Usou o celular": "Se você usou o celular durante o jogo, beba 1 shots.",
    "Sem óculos": "Todos que não estão usando óculos bebem.",
    "Mais próximo": "O jogador mais próximo de você no tabuleiro bebe.",
    "Não fez ninguém beber": "Se você ainda não fez ninguém beber, beba 2 shots.",
}

# Função para inicializar o tabuleiro
def inicializar_tabuleiro():
    num_casas = len(ordem_casas)
    
    # Garante que a ordem será aleatória a cada início de sessão
    casas_disponiveis = list(range(1, num_casas - 1))  # Exclui início e fim
    random.shuffle(casas_disponiveis)
    
    # Divide as casas por tipo
    casas_beneficios = casas_disponiveis[:5]
    casas_penalidades = casas_disponiveis[5:15]
    casas_desafios = casas_disponiveis[15:30]
    casas_normais = casas_disponiveis[30:]

    # Cria o tabuleiro com categorias
    tabuleiro = ["Início"] + [""] * (num_casas - 2) + ["Fim"]
    
    # Distribui as categorias
    for idx in casas_beneficios:
        tabuleiro[idx] = "Benefício"
    for idx in casas_penalidades:
        tabuleiro[idx] = "Penalidade"
    for idx in casas_desafios:
        tabuleiro[idx] = "Desafio"
    for idx in casas_normais:
        tabuleiro[idx] = "Normal"
    
    # Utiliza conjuntos para evitar frases repetidas
    beneficios_usados = set()
    penalidades_usadas = set()
    desafios_usados = set()
    normais_usados = set()
    
    # Função para escolher frase única
    def escolher_frase_unica(dicionario, usadas):
        while True:
            titulo, descricao = random.choice(list(dicionario.items()))  # Escolhe um par (chave, valor)
            if titulo not in usadas:  # Verifica se o título já foi usado
                usadas.add(titulo)
                return {"titulo": titulo, "descricao": descricao}  # Retorna um dicionário


    # Adiciona as frases com títulos e descrições
    st.session_state.tabuleiro = []
    for casa in tabuleiro:
        if casa == "Início":
            st.session_state.tabuleiro.append(
                {"tipo": "Início", "titulo": "Início", "descricao": ""}
            )
        elif casa == "Fim":
            st.session_state.tabuleiro.append(
                {"tipo": "Fim", "titulo": "Fim", "descricao": ""}
            )
        elif casa == "Benefício":
            st.session_state.tabuleiro.append(
                {"tipo": "Benefício", **escolher_frase_unica(beneficios, beneficios_usados)}
            )
        elif casa == "Penalidade":
            st.session_state.tabuleiro.append(
                {"tipo": "Penalidade", **escolher_frase_unica(penalidades, penalidades_usadas)}
            )
        elif casa == "Desafio":
            st.session_state.tabuleiro.append(
                {"tipo": "Desafio", **escolher_frase_unica(desafios, desafios_usados)}
            )
        elif casa == "Normal":
            st.session_state.tabuleiro.append(
                {"tipo": "Normal", **escolher_frase_unica(normais, normais_usados)}
            )
        else:
            st.session_state.tabuleiro.append(
                {"tipo": "", "titulo": "", "descricao": ""}
            )


# Exibe o tabuleiro
def mostrar_tabuleiro_visual():
    # Adicionando CSS para o efeito hover
    st.markdown(
        """
        <style>
            .hover-card {
                background-color: #235E6F;
                color: white;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
                height: 150px;
                width: 120px;
                margin: 3px;
                transition: transform 0.3s, height 0.3s, width 0.3s, z-index 0.3s;
                overflow: hidden;
            }
            .hover-card:hover {
                transform: scale(1.2);
                height: 250px;
                width: 200px;
                z-index: 10;
                position: absolute;
            }
            .hover-card .details {
                display: none;
            }
            .hover-card:hover .details {
                display: block;
            }
            .static-card {
                background-color: #235E6F;
                color: white;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
                height: 150px;
                width: 120px;
                margin: 3px;
                overflow: hidden;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🎄 **Tabuleiro do Jogo** 🎲")
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
                # Para casas fora da lista ordem_casas
                card_class = "static-card"
                bg_color = "#235E6F"
                titulo = ""
                descricao = ""
                jogadores_texto = ""
            else:
                # Para casas presentes na lista ordem_casas
                card_class = "hover-card"
                casa_info = st.session_state.tabuleiro[cell]
                titulo = casa_info["titulo"]
                descricao = casa_info["descricao"]
                if titulo == "Início" or titulo == "Fim":
                    bg_color = "#CC231E"
                elif casa_info["tipo"] == "Benefício":
                    bg_color = "#F4D03F"
                elif casa_info["tipo"] == "Penalidade":
                    bg_color = "#B22222"
                elif casa_info["tipo"] == "Desafio":
                    bg_color = "#4682B4"
                else:
                    bg_color = "#34A65F"  # Casas normais
                
                jogadores_na_casa = [
                    emoji for emoji, pos in zip(st.session_state.emojis, st.session_state.posicoes) if pos == cell
                ]
                jogadores_texto = " ".join(jogadores_na_casa)

            with cols[col_idx]:
                st.markdown(
                    f"""
                    <div class='{card_class}' style='background-color:{bg_color};'>
                        <b style='font-size: 18px; display: block; margin-bottom: 10px;'>{titulo}</b>
                        <p>{jogadores_texto}</p>
                        <div class='details'>
                            <p style='margin-top: 10px;'>{descricao}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


