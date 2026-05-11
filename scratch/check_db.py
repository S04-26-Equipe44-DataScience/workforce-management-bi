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

def check_db():
    try:
        engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}")
        with engine.connect() as conn:
            result = conn.execute(text("SHOW DATABASES;"))
            databases = [row[0] for row in result]
            print(f"Databases: {databases}")
            
            if DB_NAME in databases:
                print(f"Database '{DB_NAME}' exists.")
                conn.execute(text(f"USE {DB_NAME};"))
                result = conn.execute(text("SHOW TABLES;"))
                tables = [row[0] for row in result]
                print(f"Tables in {DB_NAME}: {tables}")
                
                for table in tables:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    print(f"Table {table}: {count} rows")
            else:
                print(f"Database '{DB_NAME}' DOES NOT exist.")
    except Exception as e:
        print(f"Error connecting to database: {e}")

if __name__ == "__main__":
    check_db()
