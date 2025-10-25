from telethon import TelegramClient, events
import asyncio
import requests

# --- Configurações Telegram API ---
api_id = 22506763                 # Substitua pelo seu api_id
api_hash = '6973c935a3f68e503b58996a0b004105'   # Substitua pelo seu api_hash

# --- Configurações do BOT ---
bot_token = '8270473832:AAGTLN6W_rsHfBiX8jP_gHG6arblgBYI1UM'  # Token do BotFather
chat_id = 1807794970  # Seu ID pessoal (do @userinfobot)

# --- Palavras que você quer monitorar ---
keywords = [
    # RTX 5060 Ti (variações que podem aparecer)
    "rtx5060ti", "rtx 5060 ti", "rtx-5060ti",
    "rtx-5060-ti", "geforce rtx 5060 ti", "5060ti", "5060-ti",
    "nvidia rtx 5060", "nvidia rtx 5060 ti", "rtx 5060ti", "5060ti", "5060-ti", "5060 ti",

    # RX 9060 XT (variações que podem aparecer)
    "rx9060xt", "rx 9060 xt", "rx-9060xt", "rx-9060-xt",
    "radeon rx 9060 xt", "amd rx 9060 xt", "9060xt", "9060-xt",
    "rx9060", "rx 9060", "radeon 9060 xt", "amd 9060 xt", "rx 9060xt", 
    "9060xt", "9060-xt", "9060 xt"

    # Teste com termos aleatórios
    # "oferta", "desconto", "promoção", "liquidação", "apenas", "placa", "por"
]

client = TelegramClient('monitor_gpus', api_id, api_hash)

def enviar_mensagem_telegram(texto):
    """Função para enviar mensagem para o seu Telegram via bot"""
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {"chat_id": chat_id, "text": texto}
    requests.post(url, data=data)

@client.on(events.NewMessage)
async def handler(event):
    msg = event.raw_text.lower()
    if any(keyword in msg for keyword in keywords):
        texto_alerta = f"🔥 Oferta encontrada!\n\n📩 Mensagem: {event.raw_text[:1000]}"
        print(texto_alerta)
        enviar_mensagem_telegram(texto_alerta)

async def main():
    print("👀 Monitorando grupos... Pressione Ctrl+C para parar.")
    await client.start()
    await client.run_until_disconnected()

asyncio.run(main())
