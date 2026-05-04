# 🏢 GlobalForce · Workforce Management | BI

> **Vertical:** Business Intelligence &nbsp;|&nbsp; **Setor:** HR / Business Intelligence / Data Analytics  
> **Duração:** 5 semanas (S0 → S4) &nbsp;|&nbsp; **Impacto:** Eficiência Operacional

---

## 📋 Visão Geral do Projeto

### Problema
Os clientes corporativos da GlobalForce precisam de relatórios executivos mensais sobre o status de sua força de trabalho — turnover, custos por região, utilização de capacidade e atingimento de metas. Atualmente, esses relatórios são gerados manualmente no Excel, um processo que leva **três dias por cliente**.

### Objetivo
Automatizar a geração de relatórios executivos conectando as fontes de dados internas da GlobalForce a dashboards interativos e relatórios exportáveis, **reduzindo o tempo de preparação de três dias para menos de uma hora**.

---

## 👥 Usuários

| Perfil | Necessidade |
|---|---|
| **Analista GlobalForce** | Carrega dados do período e gera o relatório com um clique |
| **Gerente de Conta** | Consulta o relatório executivo final para envio ao cliente |

---

## 🔄 Fluxo do Sistema

```
Carga de dados (assignments, hours, headcount)
        ↓
Pipeline ETL — processamento e atualização do modelo
        ↓
Dashboard atualizado com novos KPIs
        ↓
Analista revisa os indicadores
        ↓
Geração do PDF com um clique
        ↓
Envio ao cliente
```

---

## 📊 KPIs do Dashboard

| Indicador | Descrição |
|---|---|
| **Turnover** | Taxa de rotatividade de colaboradores por período |
| **Custo por Região** | Distribuição de custos de workforce por região (USD) |
| **Utilização de Capacidade** | % de ocupação da força de trabalho disponível |
| **Atingimento de Metas** | Performance vs. metas estabelecidas por cliente |

---

## 🛠️ Stack Tecnológica

| Etapa | Ferramenta |
|---|---|
| Extração e Tratamento (ETL) | Python (Pandas + SQLAlchemy) |
| Banco de Dados | MySQL Community Edition |
| Modelagem de Dados | SQL — modelo estrela (fato + dimensões) |
| Dashboard & Visualização | Metabase |
| Exportação PDF | Metabase (exportação nativa) |
| Versionamento de Dados | Git LFS (Large File Storage) |
| Documentação | Markdown |

---

## 📅 Cronograma

### S0 — Planejamento ✅ *concluída*
- [x] Mapear fontes de dados disponíveis (assignments, hours, headcount)
- [x] Definir e validar KPIs com stakeholders
- [x] Esboçar o modelo de dados (tabelas e relacionamentos)
- [x] Documentar o fluxo completo ponta a ponta
- [x] Definir stack tecnológica final (Python + MySQL + Metabase)

### S1 — Modelagem de Dados ✅ *concluída*
- [x] Criar modelo de dados unificado (fato + dimensões)
- [x] Gerar mock data sintético (CSV — 3,1M registros / 36 meses)
- [x] Documentar dicionário de dados
- [x] Popular tabelas no MySQL (`etl/pipeline.py`)
- [x] Construir pipeline ETL em Python conectando os CSVs ao MySQL
- [x] Validar integridade e qualidade dos dados

### S2 — Dashboard ✅ *concluída*
- [x] Desenvolver dashboard interativo com KPIs executivos
- [x] Implementar filtros por período, região e cliente
- [x] Criar visualizações claras e adequadas para nível executivo
- [x] Validar dados com cenários reais

### S3 — Automação e Relatório PDF 🔄 *em andamento*
- [ ] Configurar geração automática do PDF com um clique
- [/] Automatizar atualização do pipeline de dados (`etl/pipeline.py`)
- [/] Testar fluxo completo ponta a ponta
- [ ] Ajustes e correções com base nos testes

### S4 — Entregáveis Finais
- [ ] Manual do usuário (analista e gerente de conta)
- [ ] Análise de mercado documentada
- [ ] Proposta conceitual finalizada
- [ ] Demo funcional gravada
- [ ] Protótipo apresentável para stakeholders

---

## 📦 Entregáveis

| Entregável | Status |
|---|---|
| Proposta Conceitual | 🔲 Pendente |
| Demo funcional | 🔄 Em andamento |
| Documentação técnica | ✅ Concluída |
| Análise de Mercado | 🔲 Pendente |
| Protótipo | ✅ Concluído |

---

## 📁 Estrutura do Repositório

```
workforce-management-bi/
│
├── data/
│   ├── raw/              # Dados brutos das fontes internas
│   └── processed/        # Dados tratados após ETL
│
├── etl/
│   └── pipeline.py       # Script oficial — geração de dados e carga no MySQL
│
├── notebooks/                 # Exploração e prototipagem (não usar em produção)
│   └── Geração de Dados Sintéticos_ GlobalForce USA (2023-2025).ipynb
│
├── dashboard/
│   └── metabase_setup.md      # Configuração e queries do Metabase
│
├── docs/
│   ├── 01_data_sources_mapping.md # Mapeamento de fontes
│   ├── 02_kpi_definition.md       # Definição de KPIs
│   ├── 03_data_model.md           # Modelo de dados
│   ├── 04_data_dictionary.md      # Dicionário de dados
│   └── 05_end_to_end_flow.md      # Fluxo ponta a ponta
│
├── reports/
│   └── templates/             # Templates de relatório PDF
│
├── globalforce_usa_3years_2023_2025.csv  # Dataset sintético (3,1M registros)
└── README.md
```

---

## 📦 Dependências Python

| Biblioteca | Versão | Descrição |
|---|---|---|
| **pandas** | 2.x | Manipulação e tratamento de dados no pipeline ETL |
| **numpy** | 1.x | Operações vetorizadas para geração dos dados sintéticos |
| **sqlalchemy** | 2.x | Gerencia a conexão entre Python e MySQL |
| **pymysql** | 1.x | Conector específico Python → MySQL (usado pelo SQLAlchemy) |
| **faker** | latest | Geração de dados fictícios realistas para mock data |

### Instalação

```bash
# 1. Instalar Git LFS (necessário para baixar o dataset de 269MB)
git lfs install
git lfs pull

# 2. Instalar dependências Python
pip install pandas numpy sqlalchemy pymysql faker
```

### Fluxo das dependências

```
faker → gera dados fictícios
    ↓
pandas → organiza em tabelas
    ↓
sqlalchemy + pymysql → envia ao MySQL
    ↓
Metabase → visualiza os dados
```

---

## ⚠️ Observações

- A equipe tem liberdade para definir funcionalidades e soluções criativas onde os detalhes não forem especificados
- Dados sensíveis de clientes devem ser anonimizados nos ambientes de desenvolvimento e teste
- A base de dados sintética de 3.1M de registros serve como base para validação de performance do pipeline

---

## 👤 Autor

**André Luiz Ribeiro**  
[linkedin.com/in/andreluizr](https://www.linkedin.com/in/andreluizr)  
Data Analytics | Business Intelligence | Metabase | SQL | Python
