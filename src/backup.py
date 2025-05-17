import pandas as pd
from bson import ObjectId
import matplotlib.pyplot as plt
from pymongo import MongoClient
import io
import streamlit as st
from urllib.parse import quote_plus
import os

# Função para conectar ao MongoDB
def conectar_mongodb():
    username = os.getenv('MONGODB_USERNAME')  # Usando variáveis de ambiente
    password = os.getenv('MONGODB_PASSWORD')

    # Corrigido: convertendo para bytes antes de aplicar quote_plus
    username_encoded = quote_plus(username.encode('utf-8'))
    password_encoded = quote_plus(password.encode('utf-8'))

    connection_string = f"mongodb+srv://{username_encoded}:{password_encoded}@enxadristas.6qxskfv.mongodb.net/?retryWrites=true&w=majority&appName=enxadristas"
    return MongoClient(connection_string)

# Conectar ao MongoDB
client = conectar_mongodb()
db = client["enxadristas_db"]
collection = db["enxadristas"]

# Função para reiniciar a coleção
def reiniciar_colecao():
    if "enxadristas" in db.list_collection_names():
        db.drop_collection("enxadristas")
    db.create_collection("enxadristas")

# Chama a função para reiniciar a coleção no início do script (opcional)
# reiniciar_colecao()

# Definindo constantes
RATING_INICIAL = 1600
K = 32

# Funções de cálculo
def calcular_pontuacao(medalhas_ouro, medalhas_prata, medalhas_bronze):
    return (medalhas_ouro * 3) + (medalhas_prata * 2) + (medalhas_bronze * 1)

def atualizar_rating(rating_atual, resultado, expectativa):
    return round(rating_atual + K * (resultado - expectativa))

def expectativa_vitoria(rating_jogador, rating_oponente):
    return 1 / (1 + 10 ** ((rating_oponente - rating_jogador) / 400))

# Funções de manipulação de dados
def cadastrar_enxadrista(nome, ultimo_torneio, ouro, prata, bronze, partidas):
    pontuacao = calcular_pontuacao(ouro, prata, bronze)
    media_pontos = pontuacao / partidas if partidas > 0 else 0
    enxadrista = {
        'nome': nome,
        'rating': RATING_INICIAL,
        'ouro': ouro,
        'prata': prata,
        'bronze': bronze,
        'último_torneio': ultimo_torneio,
        "Pontuação": pontuacao,
        "Média de Pontos": media_pontos,
        "Partidas": partidas
    }
    collection.insert_one(enxadrista)
    return f"Enxadrista {nome} cadastrado com sucesso!"

def registrar_confronto(nome1, nome2, resultado):
    jogador1 = collection.find_one({'nome': nome1})
    jogador2 = collection.find_one({'nome': nome2})
    
    if jogador1 and jogador2:
        expectativa1 = expectativa_vitoria(jogador1['rating'], jogador2['rating'])
        expectativa2 = expectativa_vitoria(jogador2['rating'], jogador1['rating'])
        novo_rating1 = atualizar_rating(jogador1['rating'], resultado, expectativa1)
        novo_rating2 = atualizar_rating(jogador2['rating'], 1 - resultado, expectativa2)

        collection.update_one({'nome': nome1}, {'$set': {'rating': novo_rating1}})
        collection.update_one({'nome': nome2}, {'$set': {'rating': novo_rating2}})
        return "Confronto registrado com sucesso!"
    else:
        return "Jogador não encontrado!"

def gerar_relatorio():
    enxadristas = list(collection.find())
    df = pd.DataFrame(enxadristas)
    df.insert(0, 'Posição', range(1, len(df) + 1))
    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output

def gerar_grafico():
    enxadristas = list(collection.find())
    df = pd.DataFrame(enxadristas)
    
    if df.empty:
        return None
    
    plt.figure(figsize=(8, 6))
    wedges, texts, autotexts = plt.pie(
        df["rating"],
        labels=df["nome"],
        autopct="%1.1f%%",
        startangle=90,
        colors=plt.cm.viridis(range(len(df))),
        textprops={'fontsize': 12}
    )
    plt.title("Distribuição de Rating dos Enxadristas")
    return plt

def remover_duplicados():
    nomes = collection.distinct('nome')
    for nome in nomes:
        duplicados = list(collection.find({'nome': nome}))
        if len(duplicados) > 1:
            ids_para_excluir = [str(enxadrista['_id']) for enxadrista in duplicados[1:]]
            collection.delete_many({'_id': {'$in': [ObjectId(id) for id in ids_para_excluir]}})
    return "Duplicados removidos com sucesso!"

def remover_enxadrista(nome):
    resultado = collection.delete_one({'nome': nome})
    if resultado.deleted_count > 0:
        return f"Enxadrista {nome} removido com sucesso!"
    else:
        return f"Enxadrista {nome} não encontrado."

# Interface do Streamlit
st.set_page_config(
    page_title="Chess Master Rating",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicializa o tema na session state
if "tema" not in st.session_state:
    st.session_state.tema = "Escuro"

# Função para aplicar o tema
def aplicar_tema(tema):
    if tema == "Escuro":
        st.markdown(
            """
            <style>
            .reportview-container {
                background-color: #1E1E1E;
                color: white;
            }
            .sidebar .sidebar-content {
                background-color: #1E1E1E;
                color: white;
            }
            .stButton button {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            .reportview-container {
                background-color: white;
                color: black;
            }
            .sidebar .sidebar-content {
                background-color: white;
                color: black;
            }
            .stButton button {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

# Aplica o tema atual
aplicar_tema(st.session_state.tema)

# Título e Descrição
st.markdown(
    """
    <h1 style='text-align: center; color: #DAA520;'>
        Chess Master Rating 🏆
    </h1>
    <h3 style='text-align: center; color: #4CAF50;'>
        Acompanhe o desempenho dos enxadristas e seus ratings!
    </h3>
    """,
    unsafe_allow_html=True
)

# Sidebar Personalizada
with st.sidebar:
    st.header("ℹ️ Sobre o Projeto")
    st.markdown(
        """
        **Chess Master Rating** é um aplicativo para gerenciar e acompanhar o desempenho de enxadristas.
        
        - **Objetivo:** Facilitar o cálculo de ratings e a visualização de estatísticas.
        - **Tecnologias:** Streamlit, MongoDB, Python.
        """
    )

    st.markdown("---")

    st.header("🔗 Links do GitHub dos Devs")
    st.markdown("[Dev Marcelo](https://github.com/maasj1)")
    st.markdown("[Dev Wagner](https://github.com/wagnersantan)")

# Adicionando abas para melhor organização
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Cadastro e Registro", "Relatórios e Gráficos", "Manutenção de Dados", "Emparceiramento Suíço", "Resultados"])

# Inicializa a estrutura para armazenar resultados das rodadas
if "resultados_rodadas" not in st.session_state:
    st.session_state.resultados_rodadas = []

# Restante do código segue sem mudanças
