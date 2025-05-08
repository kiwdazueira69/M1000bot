import sqlite3
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configurações
BOT_TOKEN = "7291432204:AAHJlvJ9uQiPVwbXIxU9soA4TEpYJsR7GFQ"
GROUP_ID = "-1002644150937"  # Coloque o ID do seu grupo aqui
DATABASE = "database.db"


def criar_tabela():
    """
    Cria a tabela de usuários aprovados se não existir.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios_aprovados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def salvar_usuario(telegram_id, status):
    """
    Salva o usuário no banco de dados.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios_aprovados (telegram_id, status) VALUES (?, ?)", (telegram_id, status))
    conn.commit()
    conn.close()


def aprovar_usuario(user_id):
    """
    Aprova o usuário no grupo do Telegram.
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/approveChatJoinRequest"
    params = {
        "chat_id": GROUP_ID,
        "user_id": user_id
    }
    response = requests.post(url, params=params)
    
    if response.status_code == 200:
        print(f"✅ Usuário {user_id} aprovado no grupo!")
        salvar_usuario(user_id, "Aprovado")
    else:
        print(f"⚠️ Falha ao aprovar o usuário {user_id}: {response.text}")
        salvar_usuario(user_id, "Falha")


@app.route('/integracao_bot_perfectpay', methods=['POST'])
def pagamento_perfectpay():
    """
    Recebe notificações de pagamento da Perfect Pay.
    """
    data = request.json
    print(f"📥 Notificação recebida: {data}")

    # Validação de status de pagamento
    if data.get("status") == "aprovado":
        telegram_id = data.get("client_telegram_id")
        
        if telegram_id:
            aprovar_usuario(telegram_id)
            return jsonify({"message": "Usuário aprovado"}), 200
        else:
            return jsonify({"message": "ID do Telegram não encontrado"}), 400
    
    return jsonify({"message": "Pagamento não aprovado"}), 400


if __name__ == "__main__":
    criar_tabela()
    print("✅ API rodando na porta 5000")
    app.run(port=5000)
