
# ♟️ Chess Master Rating

**Chess Master Rating** é um aplicativo interativo desenvolvido com [Streamlit](https://streamlit.io/) que permite o gerenciamento, análise e visualização dos dados de desempenho de enxadristas com base em torneios e confrontos diretos. Ideal para clubes, escolas e competições de xadrez.

---

## 🚀 Funcionalidades

- Cadastro de enxadristas com desempenho individual
- Cálculo de **rating** com base em confrontos e pontuação (sistema inspirado no Elo)
- Registro de confrontos com atualização automática dos ratings
- Geração de **relatórios Excel**
- Visualização gráfica com **distribuição de ratings**
- Remoção de registros duplicados
- Alternância entre temas **claro** e **escuro**
- Interface web responsiva via **Streamlit**
- Integração com banco de dados **MongoDB Atlas**
- Estrutura para futuro **emparceiramento suíço**

---

## 🧠 Tecnologias Utilizadas

- [Python 3.10+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [PyMongo](https://pymongo.readthedocs.io/)

---

## ⚙️ Como Executar Localmente

1. **Clone o repositório:**

```bash
git clone https://github.com/wagnersantan/programa-chess-master-rating.git
cd programa-chess-master-rating


### ✅ Crie e ative um ambiente virtual (opcional, mas recomendado)

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar no Windows
venv\Scripts\activate

# Ativar no Linux ou MacOS
source venv/bin/activate
```
### ⚙️ Configure as variáveis de ambiente

Crie um arquivo `.env` ou configure no sistema as variáveis:

```env
MONGODB_USERNAME=seu_usuario
MONGODB_PASSWORD=sua_senha
```

---

### ▶️ Execute o aplicativo

```bash
streamlit run main.py
```

---

### 🧪 Funcionalidades em Desenvolvimento

- Sistema de emparceiramento suíço automatizado
- Tela de classificação geral por torneio
- Exportação de confrontos por rodada
- Autenticação de usuários

---

### 👥 Contribuidores

- @maasj1
- @wagnersantan

---

### 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

### 💡 Inspiração

Este projeto nasceu para facilitar a organização de torneios de xadrez estudantis, promovendo o aprendizado prático de programação, análise de dados e lógica matemática através do esporte.

