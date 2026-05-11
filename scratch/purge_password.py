import os
import glob

def purge_password():
    # Extensões que podem conter a senha (arquivos de texto)
    extensions = ('.py', '.md', '.txt', '.csv', '.env', '.example', '.sql', '.json')
    
    # Busca recursiva por todos os arquivos
    for f in glob.glob('**/*', recursive=True):
        if os.path.isfile(f) and f.endswith(extensions):
            try:
                with open(f, 'rb') as file:
                    content = file.read()
                
                if b'Arib1979!' in content:
                    print(f"Limpando arquivo: {f}")
                    new_content = content.replace(b'Arib1979!', b'REDACTED_PASSWORD')
                    with open(f, 'wb') as file:
                        file.write(new_content)
            except Exception as e:
                pass

if __name__ == "__main__":
    purge_password()
