from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from db import criar_banco, registrar_pedido, verificar_status
import os

# Seu token aqui
TOKEN = "7291432204:AAHJlvJ9uQiPVwbXIxU9soA4TEpYJsR7GFQ"
WEBHOOK_URL = "https://m1000bot.onrender.com"

# Função para criar o banco de dados no início
criar_banco()

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = [["🛒 Comprar", "📦 Meus pedidos"], ["📞 Suporte", "❓ FAQ"]]
    reply_markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True)
    
    await update.message.reply_text(
        "🤖 Bem-vindo ao bot de vendas anônimas!\nEscolha uma opção:",
        reply_markup=reply_markup
    )

# Respostas do menu
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem = update.message.text
    user_id = update.effective_user.id

    if mensagem == "🛒 Comprar":
        with open("produto.jpg", "rb") as imagem:
            await update.message.reply_photo(
                photo=imagem,
                caption="🎬 O melhor da mídia - R$ 14,99\n💲 Só aceitamos PIX."
            )
        await update.message.reply_text(
            "Clique no link abaixo para realizar o pagamento e receber o produto:\n"
            "👉 [Link para pagamento Perfect Pay](https://checkout.perfectpay.com.br/pay/PPU38CPO4D1)"
        )

        registrar_pedido(user_id, update.effective_user.first_name, "pendente")

    elif mensagem == "📞 Suporte":
        await update.message.reply_text("📬 Suporte: @M1000rlk")

    elif mensagem == "📦 Meus pedidos":
        if verificar_status(user_id) == "pago":
            await update.message.reply_text("📝 Seu pedido foi confirmado. Você pode acessar o link do produto.")
            await update.message.reply_text("Clique para acessar o grupo: https://t.me/+9FTzWYZE2R02MmRh")
        else:
            await update.message.reply_text("❌ Você precisa realizar a compra para acessar seus pedidos.")

    elif mensagem == "❓ FAQ":
        keyboard = [[InlineKeyboardButton("❓ Ver FAQ", callback_data="faq")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Clique abaixo para ver as dúvidas frequentes:", reply_markup=reply_markup)

    else:
        await update.message.reply_text("❓ Opção inválida. Use o menu.")

# Resposta ao botão FAQ
async def resposta_faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    texto = (
        "📌 *FAQ - Perguntas Frequentes*\n\n"
        "1️⃣ _Como funciona a entrega?_\n"
        "→ A entrega é feita via Telegram após confirmação de pagamento.\n\n"
        "2️⃣ _Quais formas de pagamento são aceitas?_\n"
        "→ Perfect Pay com Pix, cartão de crédito e boleto.\n\n"
        "3️⃣ _É seguro comprar por aqui?_\n"
        "→ Sim! Pagamentos via Perfect Pay são seguros e rápidos.\n\n"
    )
    await query.edit_message_text(text=texto, parse_mode="Markdown")

# Inicializando o bot com Webhook
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, responder))
app.add_handler(CallbackQueryHandler(resposta_faq, pattern="faq"))

# Configurações do Webhook
PORT = int(os.environ.get("PORT", "10000"))
app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path="/webhook",
    webhook_url=WEBHOOK_URL
)

