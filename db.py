import sqlite3

# Função para criar o banco de dados e a tabela
def criar_banco():
    conn = sqlite3.connect('pedidos.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pedidos (
        user_id INTEGER PRIMARY KEY,
        produto TEXT,
        status TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Função para inserir um novo pedido
def registrar_pedido(user_id, produto, status):
    conn = sqlite3.connect('pedidos.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pedidos (user_id, produto, status) VALUES (?, ?, ?)", (user_id, produto, status))
    conn.commit()
    conn.close()

# Função para verificar o status do pedido
def verificar_status(user_id):
    conn = sqlite3.connect('pedidos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM pedidos WHERE user_id = ?", (user_id,))
    status = cursor.fetchone()
    conn.close()
    return status[0] if status else None
