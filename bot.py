from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from db import criar_banco, registrar_pedido, verificar_status

# Seu token aqui
TOKEN = "7291432204:AAHJlvJ9uQiPVwbXIxU9soA4TEpYJsR7GFQ"

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

        # Registrar o pedido do usuário no banco de dados
        registrar_pedido(user_id, update.effective_user.first_name)
        with open("pedidos.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"ID {user_id} solicitou compra.\n")

    elif mensagem == "📞 Suporte":
        await update.message.reply_text("📬 Suporte: @M1000rlk")

    elif mensagem == "📦 Meus pedidos":
        # Verificar se o usuário já comprou
        if verificar_status(user_id):
            await update.message.reply_text("📝 Seu pedido foi confirmado. Você pode acessar o link do produto.")
            # Enviar o link do grupo apenas para compradores
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
        "2️⃣ Quais formas de pagamento são aceitas?_\n"
        "→ Atualmente, aceitamos pagamentos via Perfect Pay, que oferece opções como Pix, cartão de crédito e boleto bancário.\n\n"
        "3️⃣ O que é a Perfect Pay?_\n"
        "→ A Perfect Pay é uma plataforma de pagamentos brasileira que permite transações seguras e rápidas, com suporte a diversas formas de pagamento.\n\n"
        "4️⃣ A Perfect Pay é confiável?_\n"
        "→ Sim. A Perfect Pay possui uma reputação considerada ótima no Reclame Aqui, com uma nota média de 8.6/10 nos últimos 6 meses.\n\n"
        "5️⃣ É seguro comprar por aqui?_ \n"
        "→ Sim! Utilizamos a Perfect Pay para garantir segurança e agilidade nas transações. Após a confirmação do pagamento, o produto é entregue diretamente no Telegram.\n\n"
        "Se tiver mais dúvidas, fale diretamente conosco pelo suporte."
    )
    await query.edit_message_text(text=texto, parse_mode="Markdown")

# Executar o bot
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, responder))
app.add_handler(CallbackQueryHandler(resposta_faq, pattern="faq"))

print("🤖 Bot rodando... Pressione Ctrl+C para parar.")
app.run_polling()
