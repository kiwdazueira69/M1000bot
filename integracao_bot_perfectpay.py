from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import sqlite3

# Seu token aqui
TOKEN = "7291432204:AAHJlvJ9uQiPVwbXIxU9soA4TEpYJsR7GFQ"
GRUPO_ID = -1002644150937 # Coloque o ID do seu grupo

# Caminho para o banco de dados
DB_PATH = 'banco.db'

# Função para verificar se o usuário pagou
def usuario_pagou(user_id):
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    cursor.execute("SELECT status FROM pedidos WHERE user_id = ?", (user_id,))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado is not None and resultado[0] == 'pago'

# Comando para pedir entrada no grupo
async def pedir_entrada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if usuario_pagou(user_id):
        await update.message.reply_text("✅ Pagamento confirmado! Você será adicionado ao grupo em instantes.")
        await context.bot.approve_chat_join_request(chat_id=GRUPO_ID, user_id=user_id)
    else:
        await update.message.reply_text("❌ Pagamento não identificado. Por favor, finalize a compra para acessar o grupo.")

# Executar o bot
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("entrar", pedir_entrada))

print("🤖 Bot rodando... Pressione Ctrl+C para parar.")
app.run_polling()
