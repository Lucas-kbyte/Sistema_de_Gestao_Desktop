import sqlite3

def conectar():
    return sqlite3.connect("produto.db")

def criar_tabela():
    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS banco(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_produto TEXT NOT NULL,
                    preco REAL NOT NULL, 
                    quantidade INTEGER
                )
            """)

        conexao.commit()
        print("iTEM verificado/criado com sucesso!") 
    except sqlite3.Error as erro:
        print(f"Ocorreu um erro: {erro}")
    finally:
        if conexao:
            conexao.close()

def criar_tabela_usuario():
    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS banco(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    senha INTEGER NOT NULL
                )
            """)

        conexao.commit()
        print("Usuário verificado/criado com sucesso!") 
    except sqlite3.Error as erro:
        print(f"Ocorreu um erro: {erro}")
    finally:
        if conexao:
            conexao.close()