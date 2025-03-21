<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gerenciador de Enxadristas</title>
</head>
<body>
    <h1>Gerenciador de Enxadristas</h1>

    <h2>Descrição</h2>
    <p>O Gerenciador de Enxadristas é uma aplicação desenvolvida em Python utilizando a biblioteca Tkinter para a interface gráfica, que permite o cadastro, gerenciamento e análise de dados de enxadristas. A aplicação armazena informações em um banco de dados MongoDB e possibilita calcular ratings Elo, gerar relatórios em formato Excel e visualizar dados através de gráficos.</p>

    <h2>Funcionalidades</h2>
    <ul>
        <li><strong>Cadastro de Enxadristas:</strong> Permite registrar novos enxadristas com informações como nome, medalhas e partidas jogadas.</li>
        <li><strong>Registro de Confrontos:</strong> Possibilita registrar confrontos entre jogadores, atualizando automaticamente o rating Elo de cada um com base no resultado.</li>
        <li><strong>Visualização de Dados:</strong> Mostra uma tabela com os dados dos enxadristas, incluindo posição, nome, rating e medalhas.</li>
        <li><strong>Geração de Relatórios:</strong> Exporta os dados dos enxadristas para um arquivo Excel.</li>
        <li><strong>Geração de Gráficos:</strong> Cria gráficos de pizza que ilustram a distribuição do rating dos enxadristas e os insere no arquivo Excel gerado.</li>
        <li><strong>Exclusão de Enxadristas:</strong> Permite remover enxadristas do banco de dados.</li>
    </ul>

    <h2>Requisitos</h2>
    <p>Para executar a aplicação, você precisará das seguintes bibliotecas Python:</p>
    <ul>
        <li>tkinter</li>
        <li>pandas</li>
        <li>matplotlib</li>
        <li>openpyxl</li>
        <li>xlsxwriter</li>
        <li>pymongo</li>
    </ul>
    <p>Você pode instalar as bibliotecas necessárias utilizando o pip:</p>
    <pre><code>pip install pandas matplotlib openpyxl xlsxwriter pymongo</code></pre>
    <p>Além disso, é necessário ter o MongoDB instalado e em execução em sua máquina. Certifique-se de que o MongoDB está acessível pelo endereço <code>mongodb://localhost:27017/</code>.</p>

    <h2>Como Usar</h2>
    <p>Clone o repositório para sua máquina local:</p>
    <pre><code>git clone https://github.com/seu_usuario/gerenciador-enxadristas.git</code></pre>
    <p>Navegue até o diretório do projeto:</p>
    <pre><code>cd gerenciador-enxadristas</code></pre>
    <p>Execute o script Python:</p>
    <pre><code>python nome_do_seu_script.py</code></pre>
    <p>Utilize a interface gráfica para cadastrar enxadristas, registrar confrontos, gerar relatórios e gráficos, e gerenciar os dados conforme necessário.</p>

    <h2>Estrutura do Código</h2>
    <h3>Funções Principais:</h3>
    <ul>
        <li><strong>calcular_pontuacao:</strong> Calcula a pontuação com base nas medalhas.</li>
        <li><strong>atualizar_rating:</strong> Atualiza o rating de um jogador após um confronto.</li>
        <li><strong>cadastrar_enxadrista:</strong> Cadastra um novo enxadrista no banco de dados.</li>
        <li><strong>registrar_confronto:</strong> Registra o resultado de um confronto entre dois enxadristas.</li>
        <li><strong>gerar_relatorio:</strong> Gera um arquivo Excel com os dados dos enxadristas.</li>
        <li><strong>gerar_grafico:</strong> Cria um gráfico de pizza com a distribuição do rating dos enxadristas.</li>
        <li><strong>excluir_enxadrista:</strong> Remove um enxadrista do banco de dados.</li>
    </ul>
    <p><strong>Interface Gráfica:</strong> Utiliza widgets do Tkinter para criar uma interface intuitiva e fácil de usar, permitindo interação com o usuário.</p>

    <h2>Contribuição</h2>
    <p>Sinta-se à vontade para contribuir com melhorias ou sugestões! Você pode abrir uma issue ou enviar um pull request.</p>

    <h2>Licença</h2>
    <p>Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.</p>

    <p>Desenvolva suas habilidades em gestão de dados de enxadristas com este gerenciador e aproveite para aprimorar seu conhecimento em Python e MongoDB!</p>
</body>
</html>
