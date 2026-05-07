"""
=============================================================
GlobalForce · Workforce Management | BI
Script: report_generator.py
Etapa: S3 — Automação e Relatório PDF
Descrição: Gera relatórios executivos em PDF a partir de 
           dashboards do Metabase usando Playwright.
=============================================================
"""

import os
import time
from playwright.sync_api import sync_playwright

# --- CONFIGURAÇÕES ---
# Substitua pela URL pública do seu dashboard no Metabase
METABASE_DASHBOARD_URL = "http://localhost:3000/public/dashboard/fdd35251-f505-420d-bc1c-636aa5b1cb14"
OUTPUT_DIR = "reports"

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"--- Pasta '{OUTPUT_DIR}' criada.")

def generate_report(client_name, region=None, period=None):
    """
    Gera um PDF para um cliente específico aplicando filtros via URL.
    """
    ensure_output_dir()
    
    with sync_playwright() as p:
        print(f"--- Iniciando navegador para: {client_name}...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 1600}
        )
        page = context.new_page()

        # Constrói a URL com filtros tratando espaços corretamente
        import urllib.parse
        params = {"client": client_name}
        if region: params["region"] = region
        if period: params["date"] = period
        
        url_with_filters = f"{METABASE_DASHBOARD_URL}?{urllib.parse.urlencode(params)}"
        
        print(f"--- Acessando: {url_with_filters}")
        
        try:
            # Acessa a página e aguarda o carregamento inicial
            page.goto(url_with_filters, wait_until="load")
            
            # Aguarda o tempo necessário para o Metabase processar os 3.1M de registros
            print("--- Aguardando processamento dos dados (20s)...")
            time.sleep(20) 
            
            # Caminho do arquivo final
            filename = f"Relatorio_Executivo_{client_name.replace(' ', '_')}_{time.strftime('%Y%m%d')}.pdf"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            # Gera o PDF (A4, modo retrato)
            page.pdf(
                path=filepath,
                format="A4",
                print_background=True,
                margin={"top": "20px", "bottom": "20px", "left": "20px", "right": "20px"}
            )
            
            print(f"--- ✅ Relatório gerado com sucesso: {filepath}")
            
        except Exception as e:
            print(f"--- ❌ ERRO ao gerar relatório para {client_name}: {e}")
        
        finally:
            browser.close()

if __name__ == "__main__":
    # Exemplo de geração em lote para os principais clientes
    clientes_teste = ["Alpha Group", "Beta Corp", "Delta Solutions"]
    
    print("--- 📊 Iniciando Geração de Relatórios Mensais...")
    
    for cliente in clientes_teste:
        generate_report(cliente)
    
    print("\n--- Processo concluído!")
