from Modelo.model import conectar, cria_tabela, listar_produtos
from tkinter import messagebox
import tkinter as tk
from tkinter import messagebox

def inserir_produto(nome, quantidade, preco, lbl_mensagem):
    n_dig = nome.get().strip()
    q_dig = quantidade.get().strip()
    p_dig = preco.get().strip()

    if n_dig == "" or q_dig == "" or p_dig == "":
        lbl_mensagem.configure(text="Preencha todos os campos! :P", text_color="red")
        return

    try:
        quantidade_num = int(q_dig)
        preco_num = float(p_dig.replace(",", "."))
        
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT id FROM banco WHERE nome_produto = ?", (n_dig,))
        produto_existente = cursor.fetchone()

        if produto_existente:
            conexao.close()
            lbl_mensagem.configure(text=f"Erro: '{n_dig}' já está cadastrado!", text_color="red")
            return

        sql = "INSERT INTO banco (nome_produto, quantidade, preco) VALUES (?, ?, ?)"
        cursor.execute(sql, (n_dig, quantidade_num, preco_num))

        conexao.commit()
        conexao.close()

        lbl_mensagem.configure(text=f"Produto '{n_dig}' salvo com sucesso! :3", text_color="green")

        nome.delete(0, 'end')
        quantidade.delete(0, 'end')
        preco.delete(0, 'end')
        
    except ValueError:
        lbl_mensagem.configure(text="Quantidade e preço válidos, por favor!", text_color="red")
    except Exception as e:
        lbl_mensagem.configure(text=f"Erro ao salvar: {e}", text_color="red")
        
    except ValueError:
        lbl_mensagem.configure(text="Quantidade e preço devem ser números válidos!", text_color="red")
    except Exception as e:
        lbl_mensagem.configure(text=f"Erro ao salvar: {e}", text_color="red")


def buscar_produto():
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        sql = "SELECT nome_produto, quantidade, preco FROM banco"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        
        conexao.close()
        return resultados
    except Exception as e:
        print(f"Erro ao buscar produtos: {e}")
        return []

def atualizar_preco(nome, novo_preco, lbl_mensagem):
    n_dig = nome.get().strip()
    p_dig = novo_preco.get().strip()

    if n_dig == "" or p_dig == "":
        lbl_mensagem.configure(text="Preencha o nome e o novo preço! :P", text_color="red")
        return

    try:
        preco_num = float(p_dig.replace(",", "."))
        
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT id FROM banco WHERE nome_produto = ?", (n_dig,))
        produto_existente = cursor.fetchone()

        if not produto_existente:
            conexao.close()
            lbl_mensagem.configure(text=f"Erro: '{n_dig}' não foi encontrado!", text_color="red")
            return

        sql = "UPDATE banco SET preco = ? WHERE nome_produto = ?"
        cursor.execute(sql, (preco_num, n_dig))

        conexao.commit()
        conexao.close()

        lbl_mensagem.configure(text=f"Preço de '{n_dig}' atualizado para R$ {preco_num:.2f}!", text_color="green")

        nome.delete(0, 'end')
        novo_preco.delete(0, 'end')
        
    except ValueError:
        lbl_mensagem.configure(text="O preço deve ser um número válido!", text_color="red")
    except Exception as e:
        lbl_mensagem.configure(text=f"Erro ao atualizar: {e}", text_color="red")


def deletar_produto(nome, lbl_mensagem): 
    n_dig = nome.get().strip()

    if n_dig == "":
        lbl_mensagem.configure(text="Digite o nome do produto para deletar! :P", text_color="red")
        return

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT id FROM banco WHERE nome_produto = ?", (n_dig,))
        produto_existente = cursor.fetchone()

        if not produto_existente:
            conexao.close()
            lbl_mensagem.configure(text=f"Erro: '{n_dig}' não foi encontrado!", text_color="red")
            return

        certeza = messagebox.askyesno(
            title="Confirmar Exclusão", 
            message=f"Você realmente quer deletar o produto '{n_dig}'?\nEssa ação não pode ser desfeita!"
        )

        if not certeza:
            conexao.close()
            lbl_mensagem.configure(text="Exclusão cancelada!", text_color="orange")
            return

        sql = "DELETE FROM banco WHERE nome_produto = ?"
        cursor.execute(sql, (n_dig,))

        conexao.commit()
        conexao.close()

        lbl_mensagem.configure(text=f"Produto '{n_dig}' excluído com sucesso!", text_color="green")

        nome.delete(0, 'end')
        
    except Exception as e:
        lbl_mensagem.configure(text=f"Erro ao deletar: {e}", text_color="red")


def inserir_usuario(nome, senha, confirma_senha, lbl_mensagem):
    n_dig = nome.get().strip()
    s_dig = senha.get().strip()
    c_dig = confirma_senha.get().strip()

    if n_dig == "" or s_dig == "" or c_dig == "":
        lbl_mensagem.configure(text="Preencha todos os campos! :P", text_color="red")
        return

    if s_dig != c_dig:
        lbl_mensagem.configure(text="As senhas não coincidem! ❌", text_color="red")
        return

    try:

        int(s_dig) 
        
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT id FROM usuario WHERE nome = ?", (n_dig,))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            conexao.close()
            lbl_mensagem.configure(text=f"Erro: O usuário '{n_dig}' já existe!", text_color="red")
            return

        sql = "INSERT INTO usuario (nome, senha) VALUES (?, ?)"
        cursor.execute(sql, (n_dig, s_dig))

        conexao.commit()
        conexao.close()

        lbl_mensagem.configure(text=f"Usuário '{n_dig}' criado com sucesso! :3", text_color="green")

        nome.delete(0, 'end')
        senha.delete(0, 'end')
        confirma_senha.delete(0, 'end')
        
    except ValueError:
        lbl_mensagem.configure(text="A senha deve conter apenas números!", text_color="red")
    except Exception as e:
        lbl_mensagem.configure(text=f"Erro ao salvar: {e}", text_color="red")


def verificar_login(nome, senha, lbl_mensagem):
    n_dig = nome.get().strip()
    s_dig = senha.get().strip()

    if n_dig == "" or s_dig == "":
        lbl_mensagem.configure(text="Por favor, preencha todos os campos! :P", text_color="red")
        return False

    try:
        int(s_dig)
        
        conexao = conectar()
        cursor = conexao.cursor()

        sql = "SELECT id FROM usuario WHERE nome = ? AND senha = ?"
        cursor.execute(sql, (n_dig, s_dig))
        usuario_encontrado = cursor.fetchone()

        conexao.close()

        if usuario_encontrado:
            lbl_mensagem.configure(text="Login realizado com sucesso! Simbora! :3", text_color="green")
            return True
        else:
            lbl_mensagem.configure(text="Usuário ou senha incorretos! ❌", text_color="red")
            return False
            
    except ValueError:
        lbl_mensagem.configure(text="Usuário ou senha incorretos! ❌", text_color="red")
        return False
    except Exception as e:
        lbl_mensagem.configure(text=f"Erro no sistema: {e}", text_color="red")
        return False