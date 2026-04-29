# 🔄 Fluxo Completo Ponta a Ponta
**Projeto:** GlobalForce · Workforce Management | BI  
**Etapa:** S0 — Planejamento  
**Status:** ✅ Concluído

---

## 1. Visão Geral do Fluxo

```
┌─────────────────────────────────────────────────────────────────┐
│                        FONTES DE DADOS                          │
│         assignments.csv  │  hours.csv  │  headcount.csv         │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                        ETL (Python)                             │
│   Extração → Limpeza → Transformação → Carga no banco           │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                   BANCO DE DADOS (PostgreSQL)                   │
│   fato_workforce │ dim_colaborador │ dim_data │ dim_regiao       │
│                  │                             │ dim_cliente     │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                        METABASE                                 │
│   Questions (queries) → Dashboard → Filtros interativos         │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                     RELATÓRIO EXECUTIVO                         │
│         Exportação PDF com 1 clique → Envio ao cliente          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Detalhamento de Cada Etapa

### Etapa 1 — Carga de Dados
**Responsável:** Analista GlobalForce  
**Frequência:** Mensal

| Ação | Detalhe |
|---|---|
| Receber os arquivos | `assignments.csv`, `hours.csv`, `headcount.csv` do período |
| Validar os arquivos | Verificar se os arquivos estão completos e no formato esperado |
| Depositar na pasta | Copiar para `/data/raw/YYYY-MM/` no repositório |

---

### Etapa 2 — Pipeline ETL (Python)
**Script:** `etl/pipeline.py`  
**Trigger:** Manual ou agendado (cron job mensal)

| Passo | Descrição | Biblioteca |
|---|---|---|
| Extração | Leitura dos CSVs da pasta `/data/raw/` | Pandas |
| Limpeza | Remoção de duplicatas, tratamento de nulos, padronização de datas | Pandas |
| Validação | Checagem de integridade referencial entre as tabelas | Pandas |
| Transformação | Criação das tabelas fato e dimensão no modelo estrela | Pandas |
| Carga | Inserção/atualização dos dados no PostgreSQL | SQLAlchemy |
| Log | Registro do resultado da execução (linhas inseridas, erros) | logging |

---

### Etapa 3 — Banco de Dados (PostgreSQL)
**Ambiente:** Local (SQLite para dev) / Servidor (PostgreSQL para produção)

| Ação | Detalhe |
|---|---|
| Modelo estrela | Tabelas criadas conforme `docs/data_model.md` |
| Atualização | ETL faz upsert (insert or update) para não duplicar dados |
| Backup | Dump mensal antes de cada nova carga |

---

### Etapa 4 — Metabase (Dashboard)
**Acesso:** http://localhost:3000 (dev) / URL do servidor (produção)

| Ação | Detalhe |
|---|---|
| Conexão | Metabase conectado ao PostgreSQL via configuração de banco |
| Questions | Queries SQL salvas para cada KPI (Turnover, Custo, Utilização, Metas) |
| Dashboard | Painel executivo com filtros de Período, Região e Cliente |
| Atualização | Metabase re-executa as queries automaticamente ao abrir o dashboard |

---

### Etapa 5 — Revisão e Exportação
**Responsável:** Analista GlobalForce / Gerente de Conta

| Ação | Detalhe |
|---|---|
| Revisão | Analista verifica os KPIs no dashboard após a carga |
| Filtros | Seleciona o cliente e o período desejado |
| Exportação | Clica em "Download PDF" no Metabase para gerar o relatório |
| Envio | Gerente de Conta envia o PDF ao cliente por e-mail |

---

## 3. Diagrama de Responsabilidades

| Etapa | Analista GlobalForce | Gerente de Conta | Sistema (Automático) |
|---|---|---|---|
| Receber arquivos CSV | ✅ | | |
| Executar pipeline ETL | ✅ | | |
| Atualizar banco de dados | | | ✅ |
| Atualizar dashboard | | | ✅ |
| Revisar KPIs | ✅ | | |
| Exportar PDF | ✅ | | |
| Enviar ao cliente | | ✅ | |

---

## 4. Tratamento de Erros

| Cenário | Ação |
|---|---|
| Arquivo CSV ausente ou corrompido | Pipeline aborta e gera log de erro |
| Dados fora do formato esperado | Pipeline registra linhas com problema e continua |
| Falha na conexão com o banco | Pipeline tenta reconectar 3x antes de abortar |
| Dashboard sem dados novos | Metabase exibe aviso de "última atualização em XX/XX" |

---

## 5. Checklist de Execução Mensal

```
[ ] Receber os 3 arquivos CSV do período
[ ] Validar formato e completude dos arquivos
[ ] Executar: python etl/pipeline.py
[ ] Verificar log de execução (sem erros críticos)
[ ] Acessar o Metabase e confirmar atualização dos KPIs
[ ] Aplicar filtros do cliente desejado
[ ] Exportar PDF do relatório executivo
[ ] Enviar ao cliente
```

---

## 6. Ambiente de Desenvolvimento

| Componente | Versão recomendada |
|---|---|
| Python | 3.11+ |
| Pandas | 2.x |
| SQLAlchemy | 2.x |
| PostgreSQL | 15+ (produção) |
| SQLite | 3.x (desenvolvimento) |
| Metabase | Open Source — latest |
| Docker | Para subir Metabase + PostgreSQL localmente |

### Subindo o ambiente local com Docker

```bash
# Clonar o repositório
git clone https://github.com/andreluizr/workforce-management-bi
cd workforce-management-bi

# Subir Metabase + PostgreSQL
docker-compose up -d

# Instalar dependências Python
pip install -r requirements.txt

# Executar o pipeline ETL
python etl/pipeline.py
```

---

## 7. Resumo da S0 — Entregáveis Concluídos

| Entregável | Arquivo | Status |
|---|---|---|
| Mapeamento de fontes | `docs/data_sources_mapping.md` | ✅ |
| Definição de KPIs | `docs/kpi_definition.md` | ✅ |
| Modelo de dados | `docs/data_model.md` | ✅ |
| Fluxo ponta a ponta | `docs/end_to_end_flow.md` | ✅ |
| Stack tecnológica | Definida (Python + PostgreSQL + Metabase) | ✅ |

**S0 concluída. Próxima etapa: S1 — Modelagem de Dados.**
