from telethon import TelegramClient, events
import asyncio
import requests
import os
import threading
from flask import Flask

# --- Configurações Telegram API ---
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# --- Configurações do BOT ---
bot_token = os.getenv("BOT_TOKEN")
chat_id = int(os.getenv("CHAT_ID"))

# --- Palavras que você quer monitorar ---
keywords = [
    # RTX 5060 Ti (variações)
    "rtx5060ti", "rtx 5060 ti", "rtx-5060ti",
    "rtx-5060-ti", "geforce rtx 5060 ti", "5060ti", "5060-ti",
    "nvidia rtx 5060", "nvidia rtx 5060 ti", "rtx 5060ti", "5060 ti",

    # RX 9060 XT (variações)
    "rx9060xt", "rx 9060 xt", "rx-9060xt", "rx-9060-xt",
    "radeon rx 9060 xt", "amd rx 9060 xt", "9060xt", "9060-xt",
    "rx9060", "rx 9060", "radeon 9060 xt", "amd 9060 xt", "rx 9060xt", 
    "9060 xt"
]

# --- Inicializa cliente Telethon ---
client = TelegramClient('monitor_gpus', api_id, api_hash)

# --- Função para enviar mensagem via bot ---
def enviar_mensagem_telegram(texto):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {"chat_id": chat_id, "text": texto}
    requests.post(url, data=data)

# --- Handler: quando chega nova mensagem em algum grupo ---
@client.on(events.NewMessage)
async def handler(event):
    msg = event.raw_text.lower()
    if any(keyword in msg for keyword in keywords):
        texto_alerta = f"🔥 Oferta encontrada!\n\n📩 Mensagem: {event.raw_text[:1000]}"
        print(texto_alerta)
        enviar_mensagem_telegram(texto_alerta)

# --- Flask para manter o Railway ativo ---
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot de ofertas de GPUs está ativo!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# --- Thread para rodar o Flask em paralelo ---
threading.Thread(target=run_flask).start()

# --- Loop principal do bot ---
async def main():
    print("👀 Monitorando grupos... Pressione Ctrl+C para parar.")
    await client.start()
    await client.run_until_disconnected()

# --- Executa ---
asyncio.run(main())
