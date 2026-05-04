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
| **Custo por Região** | Distribuição de custos de workforce por localidade |
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
| Documentação | Markdown |

---

## 📅 Cronograma

### S0 — Planejamento ✅ *concluída*
- [x] Mapear fontes de dados disponíveis (assignments, hours, headcount)
- [x] Definir e validar KPIs com stakeholders
- [x] Esboçar o modelo de dados (tabelas e relacionamentos)
- [x] Documentar o fluxo completo ponta a ponta
- [x] Definir stack tecnológica final (Python + MySQL + Metabase)

### S1 — Modelagem de Dados
- [x] Criar modelo de dados unificado (fato + dimensões)
- [ ] Criar mock data e popular as tabelas
- [ ] Documentar dicionário de dados
- [ ] Construir pipeline ETL em Python conectando os CSVs ao MySQL
- [ ] Validar integridade e qualidade dos dados

### S2 — Dashboard
- [ ] Desenvolver dashboard interativo com KPIs executivos
- [ ] Implementar filtros por período, região e cliente
- [ ] Criar visualizações claras e adequadas para nível executivo
- [ ] Validar dados com cenários reais

### S3 — Automação e Relatório PDF
- [ ] Configurar geração automática do PDF com um clique
- [ ] Automatizar atualização do pipeline de dados
- [ ] Testar fluxo completo ponta a ponta
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
| Demo funcional | 🔲 Pendente |
| Documentação técnica | 🔲 Pendente |
| Análise de Mercado | 🔲 Pendente |
| Protótipo | 🔲 Pendente |

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
│   └── pipeline.py       # Script de extração e transformação
│
├── dashboard/
│   └── metabase_setup.md # Configuração e queries do Metabase
│
├── docs/
│   ├── data_model.md     # Documentação do modelo de dados
│   ├── data_dictionary.md# Dicionário de dados
│   └── user_manual.md    # Manual do usuário
│
├── reports/
│   └── templates/        # Templates de relatório PDF
│
└── README.md
```

---

## 📦 Dependências Python

| Biblioteca | Versão | Descrição |
|---|---|---|
| **pandas** | 2.x | Manipulação e tratamento de dados no pipeline ETL |
| **sqlalchemy** | 2.x | Gerencia a conexão entre Python e MySQL |
| **pymysql** | 1.x | Conector específico Python → MySQL (usado pelo SQLAlchemy) |
| **faker** | latest | Geração de dados fictícios realistas para mock data |

### Instalação

```bash
pip install pandas sqlalchemy pymysql faker
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

- Este projeto não implica vínculo empregatício com a GlobalForce
- A equipe tem liberdade para definir funcionalidades e soluções criativas onde os detalhes não forem especificados
- Dados sensíveis de clientes devem ser anonimizados nos ambientes de desenvolvimento e teste

---

## 👤 Autor

**André Luiz Ribeiro**  
[linkedin.com/in/andreluizr](https://www.linkedin.com/in/andreluizr)  
Data Analytics | Business Intelligence | Metabase | SQL | Python
