#  Fraude Pipeline – Detecção Inteligente de Transações Fraudulentas

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?logo=scikitlearn)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

🚀 Projeto completo de **engenharia de dados e machine learning** para **detecção de fraudes** em transações financeiras.  
Inclui pipeline de ETL, modelagem com Random Forest, API com FastAPI e visualização via **Streamlit Dashboard**.

---

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
- [Contato](#-contato)

---

## Visão Geral

O **Fraude Pipeline** demonstra um fluxo completo de **dados + IA aplicada à detecção de fraudes**.  
Desde o tratamento do dataset bruto até a análise de alertas em tempo real, o projeto cobre:

- Coleta e transformação de dados (`ETL`)
- Engenharia de atributos (`Feature Engineering`)
- Treinamento e avaliação de modelos (`Machine Learning`)
- API para predição
- Dashboard para monitoramento

## Arquitetura do Projeto

```bash
📦 fraude-pipeline
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
