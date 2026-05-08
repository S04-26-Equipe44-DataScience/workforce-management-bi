import sqlalchemy
from sqlalchemy import create_engine, text
import time

DB_USER     = "root"
DB_PASSWORD = "REDACTED_PASSWORD"  
DB_HOST     = "localhost"
DB_PORT     = "3306"
DB_NAME     = "workforce_bi"

def final_optimize():
    try:
        engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        with engine.connect() as conn:
            print("--- Iniciando Otimização Final de Performance ---")
            
            # 1. Equalizar tipos de dados (Crucial para a performance do JOIN)
            print("Equalizando tipos de dados (assignment_id)...")
            start = time.time()
            conn.execute(text("ALTER TABLE fato_workforce MODIFY COLUMN assignment_id BIGINT"))
            conn.commit()
            print(f"Concluído em {round(time.time()-start, 2)}s.")
            
            # 2. Verificar Buffer Pool
            result = conn.execute(text("SHOW VARIABLES LIKE 'innodb_buffer_pool_size'"))
            size_bytes = int(result.fetchone()[1])
            size_mb = size_bytes / (1024 * 1024)
            print(f"Tamanho do Buffer Pool: {size_mb:.2f} MB")
            
            if size_mb < 512:
                print("DICA: O Buffer Pool está baixo para 3M de linhas. Recomendado aumentar para pelo menos 1GB no my.ini.")
            
            print("\n--- Otimização concluída! O Dashboard deve estar mais rápido agora.")
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    final_optimize()
