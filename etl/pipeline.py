"""
=============================================================
GlobalForce · Workforce Management | BI
Script: pipeline.py
Etapa: S1 — Modelagem de Dados
Descrição: Processa o CSV de 3.1M de registros e popula o
           modelo estrela no MySQL (Normalização).

Cenário simulado (narrativa de portfólio):
  "Empresa com recuperação" — turnover alto em 2023,
  plano de retenção implementado em 2024, resultado
  controlado em 2025. Sazonalidade realista com picos
  em janeiro e julho (encerramento de contratos).

Correções aplicadas:
  - Bug 1: goal_achievement diferenciado por cliente,
           com tendência de melhora ao longo do tempo.
  - Bug 2: assignment_id fixo por colaborador
           (employee_id % 5), garantindo consistência
           entre execuções.
  - Bug 3: is_terminated = 1 apenas no mês exato do
           desligamento, simulado com distribuição
           ponderada por período (narrativa de recuperação).
  - Bug 4: worked_hours escalada por fator de utilização
           por período (melhora progressiva 2023→2025).
  - Bug 5: monthly_cost com reajuste anual de ~3%.
=============================================================
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import time
import os
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURAÇÕES DE CONEXÃO ---
DB_USER     = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = os.getenv("DB_PORT", "3306")
DB_NAME     = os.getenv("DB_NAME", "workforce_bi")
CSV_PATH    = "globalforce_usa_3years_2023_2025.csv"

# --- NARRATIVA: TURNOVER POR PERÍODO ---
# Taxa base mensal por período (YYYY-MM-DD → float).
# 2023: alto (~4.5%), sazonalidade em jan/jul.
# 2024: caindo (~2.5%), plano de retenção em curso.
# 2025: controlado (~1.5%), estabilização.
TURNOVER_RATE = {
    # 2023 — Problema identificado
    "2023-01-01": 0.060,  # jan: pico sazonal (encerramento de contratos)
    "2023-02-01": 0.042,
    "2023-03-01": 0.040,
    "2023-04-01": 0.038,
    "2023-05-01": 0.041,
    "2023-06-01": 0.044,
    "2023-07-01": 0.058,  # jul: pico sazonal
    "2023-08-01": 0.043,
    "2023-09-01": 0.040,
    "2023-10-01": 0.039,
    "2023-11-01": 0.037,
    "2023-12-01": 0.041,
    # 2024 — Plano de retenção implementado
    "2024-01-01": 0.038,  # jan: ainda sazonal, mas menor
    "2024-02-01": 0.032,
    "2024-03-01": 0.029,
    "2024-04-01": 0.027,
    "2024-05-01": 0.026,
    "2024-06-01": 0.025,
    "2024-07-01": 0.033,  # jul: pico reduzido
    "2024-08-01": 0.024,
    "2024-09-01": 0.022,
    "2024-10-01": 0.021,
    "2024-11-01": 0.020,
    "2024-12-01": 0.021,
    # 2025 — Resultado: turnover controlado
    "2025-01-01": 0.022,  # jan: pico quase eliminado
    "2025-02-01": 0.017,
    "2025-03-01": 0.016,
    "2025-04-01": 0.015,
    "2025-05-01": 0.015,
    "2025-06-01": 0.016,
    "2025-07-01": 0.019,  # jul: sazonal residual
    "2025-08-01": 0.015,
    "2025-09-01": 0.014,
    "2025-10-01": 0.013,
    "2025-11-01": 0.013,
    "2025-12-01": 0.014,
}

# --- NARRATIVA: UTILIZAÇÃO DE CAPACIDADE POR PERÍODO ---
# 2023: baixa (ociosidade), melhorando com o plano de retenção.
# 2025: eficiente e estável.
UTILIZATION_FACTOR = {
    "2023-01-01": 0.820, "2023-02-01": 0.825, "2023-03-01": 0.830,
    "2023-04-01": 0.835, "2023-05-01": 0.840, "2023-06-01": 0.845,
    "2023-07-01": 0.838, "2023-08-01": 0.850, "2023-09-01": 0.858,
    "2023-10-01": 0.865, "2023-11-01": 0.870, "2023-12-01": 0.868,
    "2024-01-01": 0.872, "2024-02-01": 0.878, "2024-03-01": 0.885,
    "2024-04-01": 0.890, "2024-05-01": 0.895, "2024-06-01": 0.900,
    "2024-07-01": 0.893, "2024-08-01": 0.905, "2024-09-01": 0.910,
    "2024-10-01": 0.915, "2024-11-01": 0.918, "2024-12-01": 0.916,
    "2025-01-01": 0.920, "2025-02-01": 0.925, "2025-03-01": 0.930,
    "2025-04-01": 0.935, "2025-05-01": 0.938, "2025-06-01": 0.940,
    "2025-07-01": 0.935, "2025-08-01": 0.942, "2025-09-01": 0.945,
    "2025-10-01": 0.948, "2025-11-01": 0.950, "2025-12-01": 0.948,
}

# --- METAS POR CLIENTE ---
# (mean_2023, mean_2025, std) — melhora progressiva ao longo do tempo.
# Clientes com problema em 2023 mostram recuperação até 2025.
CLIENT_GOAL_PARAMS = {
    1: (82, 91, 4),   # GlobalForce Internal: melhora consistente
    2: (90, 95, 3),   # Alpha Group: sempre bom, leve melhora
    3: (65, 78, 6),   # Beta Corp: abaixo da meta, recuperando
    4: (80, 88, 5),   # Delta Solutions: melhora estável
    5: (70, 82, 7),   # Epsilon Inc: problema em 2023, recuperação visível
}

# --- REAJUSTE ANUAL DE CUSTO (~3% ao ano) ---
COST_MULTIPLIER = {2023: 1.000, 2024: 1.030, 2025: 1.061}


def get_engine():
    return create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


def build_employee_client_map(csv_path: str) -> dict:
    """Mapeamento fixo employee_id → assignment_id (1-5)."""
    print("--- Construindo mapeamento fixo employee → cliente...")
    employees = pd.read_csv(csv_path, usecols=['employee_id'])['employee_id'].unique()
    return {int(emp): int((emp % 5) + 1) for emp in employees}


def build_termination_map(csv_path: str) -> dict:
    """
    Constrói o mapa de desligamentos com distribuição ponderada por período,
    simulando a narrativa de recuperação:
      - 2023: alta taxa (~4.5%), picos em jan/jul
      - 2024: taxa declinante (~2.5%)
      - 2025: taxa controlada (~1.5%)
    """
    print("--- Construindo mapa de desligamentos (narrativa de recuperação)...")
    df_ids      = pd.read_csv(csv_path, usecols=['employee_id', 'period'])
    all_periods = sorted(df_ids['period'].unique())
    all_employees = df_ids['employee_id'].unique()

    # Calcula headcount médio por período para estimar nº de desligamentos
    headcount_por_periodo = df_ids.groupby('period')['employee_id'].nunique()

    # Nº alvo de desligamentos por período
    desligamentos_alvo = {
        p: int(headcount_por_periodo.get(p, 88000) * TURNOVER_RATE.get(p, 0.025))
        for p in all_periods
    }
    total_alvo = sum(desligamentos_alvo.values())
    print(f"--- Total de desligamentos planejados: {total_alvo:,} "
          f"({total_alvo/len(all_periods):,.0f}/mês em média)")

    # Distribui colaboradores pelos períodos respeitando os pesos
    np.random.seed(42)
    weights = np.array([desligamentos_alvo.get(p, 1) for p in all_periods], dtype=float)
    weights /= weights.sum()

    # Usa apenas os colaboradores necessários (total_alvo)
    n_to_terminate = min(total_alvo, len(all_employees))
    chosen_employees = np.random.choice(all_employees, size=n_to_terminate, replace=False)
    assigned_periods = np.random.choice(all_periods, size=n_to_terminate,
                                        replace=True, p=weights)

    termination_map = {
        int(emp): str(period)
        for emp, period in zip(chosen_employees, assigned_periods)
    }
    print(f"--- {len(termination_map):,} colaboradores com desligamento mapeado.")
    return termination_map


def assign_goal_achievement(assignment_ids: pd.Series,
                             periods: pd.Series) -> np.ndarray:
    """
    goal_achievement diferenciado por cliente com tendência de melhora
    ao longo do tempo (narrativa de recuperação).
    Interpola linearmente entre mean_2023 e mean_2025.
    """
    years = pd.to_datetime(periods).dt.year
    goals = np.empty(len(assignment_ids), dtype=float)

    for client_id, (mean_2023, mean_2025, std) in CLIENT_GOAL_PARAMS.items():
        mask = assignment_ids == client_id
        n = mask.sum()
        if n == 0:
            continue
        # Progresso linear: 0.0 em 2023 → 1.0 em 2025
        progress = ((years[mask] - 2023) / 2).clip(0, 1)
        mean_t   = mean_2023 + (mean_2025 - mean_2023) * progress
        noise    = np.random.normal(0, std, size=n)
        goals[mask] = np.clip(mean_t + noise, 60, 105)

    return np.round(goals, 1)


def run_pipeline():
    start_time = time.time()
    engine     = get_engine()
    np.random.seed(42)

    print("--- Iniciando Pipeline ETL (Narrativa: Recuperação de Turnover)...")
    print(f"--- Lendo arquivo: {CSV_PATH}")

    df_full = pd.read_csv(CSV_PATH)

    with engine.begin() as conn:
        print("--- Limpando tabelas antigas...")
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        for table in ["fato_workforce", "dim_colaborador",
                      "dim_regiao", "dim_data", "dim_cliente"]:
            conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

        # --- DIM_REGIAO ---
        print("--- Criando dim_regiao...")
        dim_regiao = df_full[['region', 'state']].drop_duplicates().reset_index(drop=True)
        dim_regiao.columns = ['region_name', 'state']
        dim_regiao['region_id'] = dim_regiao.index + 1
        dim_regiao['country'] = 'USA'
        dim_regiao.to_sql("dim_regiao", conn, if_exists="replace", index=False)

        # --- DIM_DATA ---
        print("--- Criando dim_data...")
        periods  = pd.to_datetime(df_full['period'].unique())
        dim_data = pd.DataFrame({
            'period':           periods,
            'date_id':          range(1, len(periods) + 1),
            'month':            periods.month,
            'quarter':          (periods.month - 1) // 3 + 1,
            'year':             periods.year,
            'is_current_period': (periods == periods.max()),
        })
        dim_data.to_sql("dim_data", conn, if_exists="replace", index=False)

        # --- DIM_COLABORADOR ---
        print("--- Criando dim_colaborador...")
        dim_colab = df_full.sort_values('period').drop_duplicates('employee_id', keep='last')
        dim_colab = dim_colab[['employee_id', 'department', 'region', 'role', 'monthly_cost']]
        dim_colab.to_sql("dim_colaborador", conn, if_exists="replace", index=False)

        # --- DIM_CLIENTE ---
        print("--- Criando dim_cliente...")
        clientes = [
            (1, 1, "GlobalForce Internal", "Active"),
            (2, 2, "Alpha Group",          "Active"),
            (3, 3, "Beta Corp",            "Active"),
            (4, 4, "Delta Solutions",      "Active"),
            (5, 5, "Epsilon Inc",          "Active"),
        ]
        dim_cliente = pd.DataFrame(
            clientes, columns=['assignment_id', 'client_id', 'client_name', 'status']
        )
        dim_cliente.to_sql("dim_cliente", conn, if_exists="replace", index=False)

    # --- FATO_WORKFORCE ---
    print("--- Processando fato_workforce (3.1M registros)...")

    regiao_map = dim_regiao.set_index(['region_name', 'state'])['region_id'].to_dict()
    data_map   = dim_data.set_index(
        pd.to_datetime(dim_data['period']).dt.strftime('%Y-%m-%d')
    )['date_id'].to_dict()

    employee_client_map = build_employee_client_map(CSV_PATH)
    termination_map     = build_termination_map(CSV_PATH)

    chunk_size = 500_000
    total_rows = 0

    for chunk in pd.read_csv(CSV_PATH, chunksize=chunk_size):

        # Chaves FK
        chunk['region_id']     = chunk.set_index(['region', 'state']).index.map(regiao_map)
        chunk['date_id']       = chunk['period'].map(data_map)
        chunk['assignment_id'] = chunk['employee_id'].map(employee_client_map)

        # is_terminated com narrativa de recuperação
        chunk['term_period'] = chunk['employee_id'].map(termination_map).astype(str)
        chunk['is_terminated'] = (
            chunk['period'].astype(str) == chunk['term_period']
        ).astype(int)

        # goal_achievement com tendência de melhora por cliente
        chunk['goal_achievement'] = assign_goal_achievement(
            chunk['assignment_id'], chunk['period']
        )

        # worked_hours escalada para refletir melhora de utilização
        chunk['util_factor'] = chunk['period'].map(UTILIZATION_FACTOR).fillna(0.90)
        chunk['worked_hours'] = np.clip(
            chunk['planned_hours'] * chunk['util_factor'] *
            np.random.normal(1.0, 0.02, size=len(chunk)),
            0, chunk['planned_hours'] * 1.15   # máx 15% de hora extra
        ).round(1)
        chunk['overtime_hours'] = np.maximum(
            0, chunk['worked_hours'] - chunk['planned_hours']
        ).round(1)

        # monthly_cost com reajuste anual de ~3%
        chunk['year'] = pd.to_datetime(chunk['period']).dt.year
        chunk['cost_mult'] = chunk['year'].map(COST_MULTIPLIER).fillna(1.0)
        chunk['monthly_cost'] = (chunk['monthly_cost'] * chunk['cost_mult']).round(2)

        fato_chunk = chunk[[
            'assignment_id', 'employee_id', 'date_id', 'region_id',
            'worked_hours', 'planned_hours', 'overtime_hours',
            'monthly_cost', 'goal_achievement', 'is_terminated'
        ]]

        fato_chunk.to_sql("fato_workforce", engine, if_exists="append", index=False)
        total_rows += len(fato_chunk)
        print(f"--- {total_rows:,} registros processados...")

    # --- ÍNDICES DE PERFORMANCE ---
    print("--- Criando índices de performance...")
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE dim_data        ADD PRIMARY KEY (date_id)"))
        conn.execute(text("ALTER TABLE dim_regiao      ADD PRIMARY KEY (region_id)"))
        conn.execute(text("ALTER TABLE dim_cliente     ADD PRIMARY KEY (assignment_id)"))
        conn.execute(text("ALTER TABLE dim_colaborador ADD PRIMARY KEY (employee_id)"))
        conn.execute(text("CREATE INDEX idx_fato_date ON fato_workforce(date_id)"))
        conn.execute(text("CREATE INDEX idx_fato_reg  ON fato_workforce(region_id)"))
        conn.execute(text("CREATE INDEX idx_fato_cli  ON fato_workforce(assignment_id)"))

    end_time = time.time()
    print(f"\n--- ETL CONCLUÍDO COM SUCESSO!")
    print(f"--- Tempo total: {round((end_time - start_time) / 60, 2)} minutos")
    print(f"--- Total de linhas na Fato: {total_rows:,}")
    print(f"--- Banco '{DB_NAME}' pronto para o Metabase.")

if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        print(f"--- ERRO NO PIPELINE: {e}")
        raise
