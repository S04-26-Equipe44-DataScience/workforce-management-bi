import sqlalchemy
from sqlalchemy import create_engine, text

DB_USER     = "root"
DB_PASSWORD = "REDACTED_PASSWORD"  
DB_HOST     = "localhost"
DB_PORT     = "3306"
DB_NAME     = "workforce_bi"

def check_columns():
    try:
        engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        with engine.connect() as conn:
            for table in ['dim_cliente', 'dim_colaborador', 'dim_data', 'dim_regiao', 'fato_workforce']:
                print(f"\nColumns in {table}:")
                result = conn.execute(text(f"DESCRIBE {table};"))
                for row in result:
                    print(row)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_columns()
