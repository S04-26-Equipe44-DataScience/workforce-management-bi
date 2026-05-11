import os
import sqlalchemy
from sqlalchemy import create_engine, text
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_USER     = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = os.getenv("DB_PORT", "3306")
DB_NAME     = os.getenv("DB_NAME", "workforce_bi")

def add_indexes():
    try:
        engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        with engine.connect() as conn:
            print("--- Adicionando índices para melhorar performance (3.1M registros)...")
            
            queries = [
                "CREATE INDEX idx_date_id ON fato_workforce(date_id)",
                "CREATE INDEX idx_region_id ON fato_workforce(region_id)",
                "CREATE INDEX idx_assignment_id ON fato_workforce(assignment_id)",
                "CREATE INDEX idx_employee_id ON fato_workforce(employee_id)"
            ]
            
            for query in queries:
                start = time.time()
                print(f"Executando: {query}...")
                conn.execute(text(query))
                conn.commit()
                end = time.time()
                print(f"Concluído em {round(end-start, 2)}s.")
                
            print("\n--- Índices criados com sucesso!")
            
    except Exception as e:
        print(f"Erro ao criar índices: {e}")

if __name__ == "__main__":
    add_indexes()
