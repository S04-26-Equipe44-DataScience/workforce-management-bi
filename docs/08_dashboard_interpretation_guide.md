# 📊 Guia de Interpretação do Dashboard
**Projeto:** GlobalForce · Workforce Management | BI  
**Data:** 2026-05-11  
**Status:** ✅ Concluído

Este guia explica como ler e interpretar cada elemento do dashboard executivo. Destinado à equipe de gestão e aos stakeholders do projeto.

---

## 🔢 KPI Cards (Linha Superior)

Os quatro cards do topo mostram um resumo consolidado de todo o período e todas as regiões/clientes selecionados nos filtros.

| Card | O que representa | Como interpretar |
|---|---|---|
| **Turnover Médio** | % de colaboradores desligados em relação ao total | Quanto menor, melhor. Valores acima de 5% por mês indicam alta rotatividade e custo elevado de reposição |
| **Utilização de Capacidade** | % das horas planejadas que foram efetivamente trabalhadas | Próximo de 100% é ideal. Abaixo de 80% indica ociosidade; acima de 100% indica sobrecarga |
| **Custo Médio (USD)** | Custo médio mensal por colaborador | Serve como baseline de custo. Variações grandes entre períodos ou regiões merecem investigação |
| **Meta Média** | % médio de atingimento de metas entre todos os clientes | Acima de 80% é considerado saudável. Abaixo disso, algum cliente ou região pode estar com problemas |

---

## 📈 Gráfico 1 — KPI: Turnover Mensal (%)

**Tipo:** Linha | **Eixo X:** Período | **Eixo Y:** Turnover (%)

**O que mostra:** A evolução da taxa de desligamento de colaboradores mês a mês ao longo de 3 anos.

**Como interpretar:**
- Uma **linha estável e baixa** (abaixo de 5%) indica retenção saudável
- **Picos pontuais** podem refletir reestruturações, sazonalidade ou encerramento de contratos com clientes
- Uma **tendência de alta** ao longo do tempo é um sinal de alerta — pode indicar insatisfação ou problemas de gestão
- Compare os picos com os períodos de troca de cliente ou de região para identificar causas

**Pergunta que responde:** *"A empresa está conseguindo reter seus colaboradores ao longo do tempo?"*

---

## ⏱️ Gráfico 2 — KPI: Utilização de Capacidade (%)

**Tipo:** Gauge (velocímetro) | **Escala:** 0 a 100%

**O que mostra:** O percentual atual de aproveitamento da capacidade produtiva dos colaboradores (horas trabalhadas vs. horas planejadas).

**Como interpretar:**
- 🟢 **90–100%** (verde): operação eficiente, horas sendo bem aproveitadas
- 🟡 **70–90%** (amarelo): atenção — pode haver ociosidade ou ineficiência no planejamento
- 🔴 **0–70%** (vermelho): situação crítica — grande parte da capacidade contratada não está sendo utilizada

**Pergunta que responde:** *"Estamos aproveitando bem a capacidade da nossa equipe?"*

---

## 📋 Gráfico 3 — KPI: Custo Médio por Colaborador por Região (USD)

**Tipo:** Tabela | **Colunas:** Região, Colaboradores, Custo Médio (USD), Variação vs Média (%)

**O que mostra:** O custo médio mensal por colaborador em cada região, comparado com a média geral da empresa.

**Como interpretar:**
- A coluna **"Variação vs Média (%)"** é a mais importante: valores **positivos** indicam que aquela região custa mais que a média; valores **negativos** indicam que custa menos
- Regiões com custo acima da média merecem análise — podem ter cargos mais seniores, maior custo de vida local ou horas extras elevadas
- A coluna **"Colaboradores"** ajuda a entender o peso de cada região no total

**Pergunta que responde:** *"Qual região tem o maior custo operacional e por quê?"*

---

## 📊 Gráfico 4 — KPI: Atingimento de Metas por Cliente (%)

**Tipo:** Barra vertical | **Eixo X:** Cliente | **Eixo Y:** Meta Atingida (%)

**O que mostra:** O percentual médio de atingimento de metas para cada cliente, com uma linha de referência marcando a meta de 80%.

**Como interpretar:**
- Barras **acima da linha pontilhada (80%)** → cliente sendo atendido dentro do esperado ✅
- Barras **abaixo da linha pontilhada (80%)** → cliente com desempenho abaixo do contratado ⚠️
- Comparar clientes lado a lado ajuda a priorizar ações: o cliente com menor barra precisa de atenção imediata
- Se todos os clientes estiverem próximos do mesmo valor, pode indicar que as metas não estão diferenciadas o suficiente

**Pergunta que responde:** *"Quais clientes estão sendo bem atendidos e quais precisam de ação corretiva?"*

---

## 📉 Gráfico 5 — Evolução do Custo Médio por Região ao Longo do Tempo

**Tipo:** Linhas múltiplas | **Eixo X:** Período | **Eixo Y:** Custo Médio (USD) | **Séries:** Região

**O que mostra:** Como o custo médio por colaborador evoluiu em cada região ao longo dos 3 anos, com uma linha de cor diferente por região.

**Como interpretar:**
- Linhas que **sobem consistentemente** indicam aumento de custo naquela região — pode ser reflexo de reajustes salariais, horas extras ou mudança no perfil dos colaboradores
- Linhas que **cruzam** indicam que uma região inverteu sua posição de custo em relação a outra — isso merece investigação
- Grandes **variações pontuais** (picos ou quedas bruscas) podem refletir sazonalidade, mudança de contratos ou eventos extraordinários
- Uma região com custo **consistentemente acima das demais** merece análise de composição (cargos, senioridade, horas extras)

**Pergunta que responde:** *"Como o custo operacional de cada região evoluiu ao longo do tempo e quais regiões estão ficando mais caras?"*

---

## 🎛️ Filtros do Dashboard

Os três filtros no topo (**Região**, **Cliente**, **Data**) se aplicam a todos os gráficos simultaneamente.

| Filtro | Uso recomendado |
|---|---|
| **Região** | Isolar o desempenho de uma região específica para análise detalhada |
| **Cliente** | Focar em um cliente específico em reuniões de acompanhamento |
| **Data** | Recortar um período específico (ex: apenas 2025, ou último trimestre) |
