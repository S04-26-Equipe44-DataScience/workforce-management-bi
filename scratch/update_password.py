import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Carrega as variáveis atuais do .env
load_dotenv()

# DEFINA AQUI A NOVA SENHA
NOVA_SENHA = "123Global!"

def update_password():
    # Pega as credenciais atuais do .env para se conectar
    user = os.getenv("DB_USER", "root")
    old_password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")

    try:
        print(f"--- Iniciando atualização de senha para o usuário: {user}")
        
        # Cria a conexão com a senha antiga
        engine = create_engine(f"mysql+pymysql://{user}:{old_password}@{host}:{port}")
        
        with engine.connect() as conn:
            # Comando para alterar a senha usando o método padrão do servidor
            print(f"Alterando senha no banco de dados...")
            sql = text(f"ALTER USER '{user}'@'localhost' IDENTIFIED BY '{NOVA_SENHA}';")
            conn.execute(sql)
            
            # Aplica as mudanças
            conn.execute(text("FLUSH PRIVILEGES;"))
            conn.commit()
            
            print("✅ Senha atualizada no MySQL com sucesso!")
            print("\n" + "="*50)
            print("PRÓXIMO PASSO OBRIGATÓRIO:")
            print(f"Abra o arquivo .env e altere a linha:")
            print(f"DB_PASSWORD={NOVA_SENHA}")
            print("="*50)

    except Exception as e:
        print(f"❌ Erro ao atualizar senha: {e}")
        print("\nVerifique se a senha atual no seu arquivo .env está correta.")

if __name__ == "__main__":
    update_password()
