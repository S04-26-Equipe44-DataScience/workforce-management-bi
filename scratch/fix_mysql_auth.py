import sqlalchemy
from sqlalchemy import create_engine, text

DB_USER     = "root"
DB_PASSWORD = "REDACTED_PASSWORD"  
DB_HOST     = "localhost"
DB_PORT     = "3306"

def fix_auth():
    try:
        # Connect to mysql database
        engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/mysql")
        with engine.connect() as conn:
            # Check current plugin
            result = conn.execute(text("SELECT user, plugin FROM user WHERE user='root'"))
            for row in result:
                print(f"User: {row[0]}, Plugin: {row[1]}")
            
            # Change to mysql_native_password
            print("Changing root authentication to mysql_native_password...")
            conn.execute(text(f"ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '{DB_PASSWORD}';"))
            conn.execute(text("FLUSH PRIVILEGES;"))
            print("Successfully changed authentication method.")
            
            # Check again
            result = conn.execute(text("SELECT user, plugin FROM user WHERE user='root'"))
            for row in result:
                print(f"User: {row[0]}, Plugin: {row[1]}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_auth()
