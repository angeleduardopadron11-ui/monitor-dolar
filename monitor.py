import logging
import requests
from bs4 import BeautifulSoup
import urllib3
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
TOKEN_TELEGRAM = '8626589946:AAF238iqR8XySubIJ3Sc2izJw4pVqlwIZ50'


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def obtener_tasa_bcv():
    try:
        url = "https://www.bcv.org.ve/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(r.content, 'html.parser')
        tasa_str = soup.find("div", {"id": "dolar"}).find("strong").text.strip()
        return tasa_str.replace(',', '.')
    except Exception as e:
        print(f"Error extrayendo BCV: {e}")
        return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"👋 ¡Hola {user}! Soy tu Monitor P2P personal.\n\n"
        "Comandos disponibles:\n"
        "📈 /precio - Ver tasa oficial BCV\n"
        "🧮 /calcular [monto] - Saber cuántos Bs son tus USDT"
    )

async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasa = obtener_tasa_bcv()
    if tasa:
        await update.message.reply_text(f"🏛️ *Tasa Oficial BCV:* {tasa} Bs.", parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ No pude conectar con el BCV en este momento.")

async def calcular(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        monto = float(context.args[0])
        tasa = float(obtener_tasa_bcv())
        resultado = monto * tasa
        await update.message.reply_text(f"💰 {monto} USDT equivalen a:\n🔥 *{resultado:.2f} Bs.* (Tasa: {tasa})", parse_mode='Markdown')
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Uso correcto: /calcular 100")


if __name__ == '__main__':
    print("--- 🛰️ MONITOR Y BOT ACTIVADOS ---")
    tasa_inicial = obtener_tasa_bcv()
    print(f"✅ Tasa actual detectada: {tasa_inicial} Bs.")
    print("🚀 El Bot está esperando mensajes en Telegram...")
    
    
    application = ApplicationBuilder().token(TOKEN_TELEGRAM).build()
    
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('precio', precio))
    application.add_handler(CommandHandler('calcular', calcular))
    
    
    application.run_polling()