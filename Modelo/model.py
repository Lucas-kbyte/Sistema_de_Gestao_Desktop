import sqlite3

def conectar():
    return sqlite3.connect("produto.db")

def cria_tabela():
    """Cria todas as tabelas necessárias no banco de dados se elas não existirem."""
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

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                senha TEXT NOT NULL 
            )
        """)

        conexao.commit()
        print("Banco de dados inicializado: Tabelas de produtos e usuários verificadas/criadas!")
        
    except sqlite3.Error as erro:
        print(f"Ocorreu um erro ao inicializar o banco de dados: {erro}")
    finally:
        if conexao:
            conexao.close()

def listar_produtos():
    """Busca e retorna a lista de todos os produtos cadastrados."""
    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT nome_produto, quantidade, preco FROM banco")
        produtos = cursor.fetchall()
        return produtos
    except sqlite3.Error as erro:
        print(f"Erro ao listar produtos: {erro}")
        return []
    finally:
        if conexao:
            conexao.close()

if __name__ == "__main__":
    cria_tabela()