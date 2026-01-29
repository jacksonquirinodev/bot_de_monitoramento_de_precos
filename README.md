# Monitor de Preços com Playwright e Telegram

Aplicação desktop desenvolvida em Python que realiza o monitoramento automático de preços em um site de e-commerce, notificando o usuário via Telegram quando o preço alvo configurado é atingido.

O projeto possui interface gráfica simples e intuitiva, execução assíncrona da automação (sem travar a interface) e um sistema básico de licença para controle de acesso.

---

## 🚀 Funcionalidades

- Interface gráfica com CustomTkinter
- Monitoramento automático de preços com Playwright
- Envio de alertas via Telegram
- Execução em background (threading)
- Sistema simples de licença persistente
- Logs em tempo real exibidos na interface
- Uso de variáveis de ambiente para dados sensíveis

---

## 🧰 Tecnologias Utilizadas

- Python 3
- Playwright
- CustomTkinter
- Requests
- Telegram Bot API

---

## ⚙️ Pré-requisitos

- Python 3.10+
- Playwright instalado
- Bot do Telegram configurado

Instalação das dependências:
```bash
pip install customtkinter playwright requests
playwright install

🔐 Configuração do Telegram

Defina as seguintes variáveis de ambiente no sistema:

TOKEN_TELEGRAM → Token do bot

ID_CHAT → ID do chat ou grupo (pode ser negativo)

Exemplo (Windows):

setx TOKEN_TELEGRAM SEU_TOKEN_AQUI
setx ID_CHAT -123456789


Reinicie o terminal ou a IDE após definir as variáveis.

🧾 Licença de Acesso (Demonstração)

Na primeira execução, o programa solicita uma licença de acesso.

Para fins de demonstração, utilize a seguinte licença válida:

DEMO1234567


Após validada, a licença é salva localmente e não será solicitada novamente.

▶️ Como Executar
python app.py


Informe:

Nome do produto

Preço alvo

O sistema iniciará o monitoramento automaticamente e enviará um alerta via Telegram quando o preço desejado for atingido.

📌 Observações

O projeto foi desenvolvido com foco educacional e demonstrativo.

O site monitorado é um ambiente de testes.

Tokens e dados sensíveis não devem ser versionados.