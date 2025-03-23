import pandas as pd
from bson import ObjectId
import matplotlib.pyplot as plt
from pymongo import MongoClient
import io
import streamlit as st

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["enxadristas_db"]
collection = db["enxadristas"]

RATING_INICIAL = 1600
K = 32

# Funções para cálculo e manipulação de dados
def calcular_pontuacao(medalhas_ouro, medalhas_prata, medalhas_bronze):
    return (medalhas_ouro * 3) + (medalhas_prata * 2) + (medalhas_bronze * 1)

def atualizar_rating(rating_atual, resultado, expectativa):
    return round(rating_atual + K * (resultado - expectativa))

def expectativa_vitoria(rating_jogador, rating_oponente):
    return 1 / (1 + 10 ** ((rating_oponente - rating_jogador) / 400))

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
st.set_page_config(page_title="Chess Master Rating", layout="wide")

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


# Adicionando abas para melhor organização
tab1, tab2, tab3 = st.tabs(["Cadastro e Registro", "Relatórios e Gráficos", "Manutenção de Dados"])

with tab1:
    with st.expander("Cadastro de Enxadrista", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            with st.form("cadastro_form"):
                nome = st.text_input("Nome:")
                ultimo_torneio = st.text_input("Último Torneio:")
                ouro = st.number_input("🥇 Ouro:", min_value=0)
                prata = st.number_input("🥈 Prata:", min_value=0)
                bronze = st.number_input("🥉 Bronze:", min_value=0)
                partidas = st.number_input("Partidas:", min_value=0)
                submitted = st.form_submit_button("Cadastrar")
                if submitted:
                    result = cadastrar_enxadrista(nome, ultimo_torneio, ouro, prata, bronze, partidas)
                    st.success(result)

        with col2:
            with st.form("confronto_form"):
                nome1 = st.text_input("Jogador 1:")
                nome2 = st.text_input("Jogador 2:")
                resultado = st.number_input("Resultado (0 a 1):", min_value=0.0, max_value=1.0, step=0.1)
                submitted = st.form_submit_button("Registrar Confronto")
                if submitted:
                    result = registrar_confronto(nome1, nome2, resultado)
                    st.success(result)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Gerar Relatório"):
            relatorio = gerar_relatorio()
            st.download_button("Baixar Relatório", relatorio, "ranking_enxadristas.xlsx")

    with col2:
        if st.button("Gerar Gráfico"):
            fig = gerar_grafico()
            if fig:
                st.pyplot(fig)
            else:
                st.warning("Nenhum dado disponível para gerar gráfico.")

with tab3:
    if st.button("Remover Duplicados"):
        result = remover_duplicados()
        st.success(result)

    st.header("Remover Enxadrista")
    nome_remover = st.selectbox("Selecione o Enxadrista:", [enxadrista['nome'] for enxadrista in collection.find()])
    if st.button("Remover Enxadrista"):
        result = remover_enxadrista(nome_remover)
        st.success(result)

# Exibir tabela de enxadristas
st.header("Tabela de Enxadristas")
enxadristas = list(collection.find())
if enxadristas:
    df = pd.DataFrame(enxadristas)

    # Adiciona ícones às colunas de medalhas
    df["Ouro"] = "🥇 " + df["ouro"].astype(str)
    df["Prata"] = "🥈 " + df["prata"].astype(str)
    df["Bronze"] = "🥉 " + df["bronze"].astype(str)

    # Converter todas as colunas que contêm ObjectId para string
    for column in df.columns:
        if df[column].dtype == 'object':
            df[column] = df[column].apply(lambda x: str(x) if isinstance(x, ObjectId) else x)

    st.dataframe(df)
else:
    st.warning("Nenhum enxadrista cadastrado.")