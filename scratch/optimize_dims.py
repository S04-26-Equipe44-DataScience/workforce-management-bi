import os
import sqlalchemy
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_USER     = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = os.getenv("DB_PORT", "3306")
DB_NAME     = os.getenv("DB_NAME", "workforce_bi")

def optimize_dims():
    try:
        engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        with engine.connect() as conn:
            print("--- Otimizando tabelas de dimensão...")
            
            # Matar queries lentas primeiro
            result = conn.execute(text("SHOW PROCESSLIST"))
            for row in result:
                if row[4] == 'Query' and row[5] > 10:
                    print(f"Matando query {row[0]} (rodando há {row[5]}s)...")
                    conn.execute(text(f"KILL {row[0]}"))
            
            # Adicionar Primary Keys / Indexes nas Dims
            # Usamos IGNORE ou checamos antes se existe, mas aqui vou tentar direto ou via ALTER
            tables_configs = {
                "dim_data": "date_id",
                "dim_regiao": "region_id",
                "dim_cliente": "assignment_id",
                "dim_colaborador": "employee_id"
            }
            
            for table, col in tables_configs.items():
                try:
                    print(f"Adicionando índice em {table}({col})...")
                    conn.execute(text(f"ALTER TABLE {table} ADD PRIMARY KEY ({col})"))
                except Exception as e:
                    print(f"Aviso em {table}: {e}")
            
            conn.commit()
            print("--- Otimização concluída!")
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    optimize_dims()
