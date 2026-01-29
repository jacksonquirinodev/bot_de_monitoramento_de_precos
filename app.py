import customtkinter as ctk
from tkinter import messagebox
import threading
import os
import time
import requests
from playwright.sync_api import sync_playwright

# CONFIGURAÇÕES
LICENCA_VALIDA = "DEMO1234567"
ARQUIVO_LICENCA = "licenca.dat"

TOKEN = os.getenv("TOKEN_TELEGRAM")
CHAT_ID = os.getenv("ID_CHAT")

# FUNÇÕES AUXILIARES
def extrair_preco(texto):
    return float(
        texto.replace("R$", "")
             .replace("\xa0", "")
             .replace(".", "")
             .replace(",", ".")
             .strip()
    )

def enviar_telegram(produto, preco, url):
    texto = f"🚨 Alerta!\n{produto} caiu para R$ {preco:.2f}\n🔗 {url}"
    url_api = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url_api, data={
        "chat_id": CHAT_ID,
        "text": texto
    })

def salvar_licenca(licenca):
    with open(ARQUIVO_LICENCA, "w") as f:
        f.write(licenca)

def licenca_existe():
    if not os.path.exists(ARQUIVO_LICENCA):
        return False
    with open(ARQUIVO_LICENCA, "r") as f:
        return f.read().strip() == LICENCA_VALIDA

# INTERFACE
class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Monitor de Preços")
        self.geometry("720x520")
        self.minsize(720,520)
        self.maxsize(720,520)
        ctk.set_appearance_mode("dark")

        self.criar_widgets()

        if not licenca_existe():
            self.solicitar_licenca()

    def criar_widgets(self):
        self.label_titulo = ctk.CTkLabel(self, text="Monitoramento de Preços", font=("Arial", 20))
        self.label_titulo.pack(pady=10)

        self.entry_produto = ctk.CTkEntry(self, placeholder_text="Nome do produto")
        self.entry_produto.pack(pady=10, fill="x", padx=40)

        self.entry_preco = ctk.CTkEntry(self, placeholder_text="Preço alvo (ex: 399.90)")
        self.entry_preco.pack(pady=10, fill="x", padx=40)

        self.botao_iniciar = ctk.CTkButton(self, text="Iniciar Monitoramento", command=self.iniciar)
        self.botao_iniciar.pack(pady=15)

        self.log = ctk.CTkTextbox(self, height=150)
        self.log.pack(padx=20, pady=10, fill="both", expand=True)
        self.log.configure(state="disabled")

    def escrever_log(self, mensagem):
        self.log.configure(state="normal")
        self.log.insert("end", f"{mensagem}\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def bloquear_interface(self):
        self.botao_iniciar.configure(state="disabled")
        self.entry_produto.configure(state="disabled")
        self.entry_preco.configure(state="disabled")

    def solicitar_licenca(self):
        licenca = ctk.CTkInputDialog(
            text="Informe sua licença:",
            title="Licença"
        ).get_input()

        if licenca != LICENCA_VALIDA:
            messagebox.showerror("Licença inválida", "Favor fornecer uma licença válida")
            self.destroy()
        else:
            salvar_licenca(licenca)
            messagebox.showinfo("Licença aceita", "Licença validada com sucesso!")

    def iniciar(self):
        produto = self.entry_produto.get().strip()
        preco_alvo = self.entry_preco.get().strip()

        if not produto or not preco_alvo:
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos")
            return

        try:
            preco_alvo = float(preco_alvo.replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Preço inválido")
            return

        self.bloquear_interface()
        threading.Thread(
            target=self.executar_automacao,
            args=(produto, preco_alvo),
            daemon=True
        ).start()

    # AUTOMAÇÃO
    def executar_automacao(self, produto, preco_alvo):
        self.escrever_log("🚀 Iniciando monitoramento...")
        time.sleep(1)

        with sync_playwright() as p:
            self.escrever_log("🌐 Abrindo navegador")
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(locale="pt-BR")
            page = context.new_page()

            while True:
                self.escrever_log("🔎 Acessando site")
                page.goto("https://nikeclone-devaprender.netlify.app/", wait_until="domcontentloaded")

                self.escrever_log(f"📦 Procurando produto: {produto}")
                page.get_by_role("heading", level=3, name=produto).click()

                preco_texto = page.locator("#detail-price").inner_text()
                preco_atual = extrair_preco(preco_texto)

                self.escrever_log(f"💰 Preço atual: R$ {preco_atual:.2f}")

                if preco_atual <= preco_alvo:
                    self.escrever_log("✅ Preço alvo atingido! Enviando alerta...")
                    enviar_telegram(produto, preco_atual, page.url)
                    break
                else:
                    self.escrever_log("⏳ Preço ainda não atingido. Nova verificação em 1 minuto")
                    time.sleep(60)

            browser.close()
            self.escrever_log("🛑 Monitoramento finalizado")

# EXECUÇÃO
if __name__ == "__main__":
    app = App()
    app.mainloop()
