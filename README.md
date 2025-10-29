# Fraude Pipeline – Detecção Inteligente de Transações Fraudulentas

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?logo=scikitlearn)

Projeto completo de **engenharia de dados e machine learning** para **detecção de fraudes** em transações financeiras.  
Inclui pipeline de **ETL**, **modelagem com Random Forest**, **API com FastAPI** e visualização interativa via **Streamlit Dashboard**.


## Sumário

- [Visão Geral](#-visão-geral)
- [Arquitetura do Projeto](#-arquitetura-do-projeto)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Funcionalidades](#-funcionalidades)
- [Pipeline de Execução](#-pipeline-de-execução)
- [Demonstração do Dashboard](#-demonstração-do-dashboard)
- [Como Executar Localmente](#-como-executar-localmente)
- [Estrutura de Pastas](#-estrutura-de-pastas)
- [Aprendizados e Desafios](#-aprendizados-e-desafios)

---

## Visão Geral

O **Fraude Pipeline** demonstra um fluxo completo de **dados + IA aplicada à detecção de fraudes**.  
Desde o tratamento do dataset bruto até a análise de alertas em tempo real, o projeto cobre:

- Coleta e transformação de dados (`ETL`)
- Engenharia de atributos (`Feature Engineering`)
- Treinamento e avaliação de modelos (`Machine Learning`)
- API para predição (`FastAPI`)
- Dashboard para monitoramento (`Streamlit`)

---

##  Arquitetura do Projeto

```bash
 fraude-pipeline
 ┣ 📂 etl/                # Pipeline de extração e transformação
 ┣ 📂 features/           # Criação das variáveis derivadas
 ┣ 📂 model/              # Treinamento e avaliação do modelo
 ┣ 📂 api/                # API FastAPI para servir predições
 ┣ 📂 dashboard/          # Dashboard Streamlit interativo
 ┣ 📂 data/               # Dados brutos e processados
 ┣ 📂 db/                 # Scripts SQL e Docker Compose
 ┣ 📜 requirements.txt    # Dependências do projeto
 ┣ 📜 README.md           # Este arquivo
 ┗ 📜 .env.example        # Exemplo de configuração de ambiente
```

| Categoria            | Ferramentas                    |
| -------------------- | ------------------------------ |
| **Linguagem**        | Python 3.10                    |
| **ETL / Banco**      | Pandas, SQLAlchemy, PostgreSQL |
| **Machine Learning** | scikit-learn, joblib           |
| **API**              | FastAPI, Uvicorn               |
| **Dashboard**        | Streamlit                      |
| **Ambiente**         | Docker e Virtualenv (.venv)    |
| **Versionamento**    | Git e GitHub                   |


Funcionalidades

✅ ETL completo: extração, limpeza e carga dos dados
✅ Feature engineering com janelas móveis e z-score
✅ Treinamento e avaliação com RandomForestClassifier
✅ Métricas avançadas: AUC-ROC, AUC-PR, F1-score
✅ API de predição via FastAPI
✅ Dashboard Streamlit com:
Filtros dinâmicos (data, país, canal, valor)
Distribuição dos scores
Importância das features
Tabela de alertas de fraude

 Pipeline de Execução

1️⃣ ETL
Extrai dados CSV e insere em raw_transactions (PostgreSQL).

2️⃣ Feature Engineering
Cria atributos como:
hour
is_high_amount
rolling_1h_tx
amount_zscore
country_risk

3️⃣ Treinamento de Modelo
Treina o modelo RandomForestClassifier e calcula métricas como:
AUC-ROC
AUC-PR
F1-Score
Matriz de confusão

4️⃣ API com FastAPI
Endpoint /predict recebe transações e retorna a probabilidade de fraude.

5️⃣ Dashboard Streamlit
Visualização em tempo real de alertas e indicadores de desempenho do modelo.


## Como Executar Localmente

1️⃣ Clonar o repositório
```
git clone https://github.com/pablomigueldias/fraude-pipeline.git
cd fraude-pipeline
```
2️⃣ Criar e ativar ambiente virtual
```
python -m venv .venv
.venv\Scripts\activate
```
3️⃣ Instalar dependências
```
pip install -r requirements.txt
```

4️⃣ Rodar ETL e Treinamento
```
python -m etl.load_data
python -m features.make_feature
python -m model.train_model
```

5️⃣ Iniciar API e Dashboard
```
uvicorn api.main:app --reload --port 8000
streamlit run dashboard/app_dashboard.py
```










