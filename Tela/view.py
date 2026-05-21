import customtkinter as ctk

# primeiros testes disso
# modificações: 250 
# AAAAAAAAAAAAAAAAAAAAAA DEUS SOCORROOOO!!!!

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def tela_principal():
    janela = ctk.CTk()
    janela.geometry("700x650")
    janela.title("Sistema de Gestão 1.0")

    def alternar_tema():
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            btn_tema.configure(text="Modo Preto")
        else:
            ctk.set_appearance_mode("Light")
            ctk.set_appearance_mode("Dark")
            btn_tema.configure(text="Modo Branco")


    menu_lateral = ctk.CTkFrame(janela, width=180)
    menu_lateral.pack(side="left", fill="y", padx=10, pady=10)

    lbl_menu = ctk.CTkLabel(menu_lateral, text="Menu", font=("Serif", 20, "bold"))
    lbl_menu.pack(pady=20, padx=10)

    btn_opcao1 = ctk.CTkButton(menu_lateral, text="Dashboard")
    btn_opcao1.pack(pady=10, padx=10, fill="x")

    btn_tema = ctk.CTkButton(menu_lateral, text="Modo Branco", fg_color="gray", hover_color="darkgray", command=alternar_tema)
    btn_tema.pack(side="bottom", pady=20, padx=10, fill="x")


    conteudo_direita = ctk.CTkFrame(janela, fg_color="transparent")
    conteudo_direita.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    texto2 = ctk.CTkLabel(conteudo_direita, text="Sistema de Gestão 1.0", font=("Serif", 28, "bold"), text_color="#003cff")
    texto2.pack(side="top", anchor="n", pady=20)

    card_login = ctk.CTkFrame(conteudo_direita, width=300) 
    card_login.pack(expand=True)
    card_login.grid_columnconfigure(0, weight=1)

    texto = ctk.CTkLabel(card_login, text="Por favor, Digite sua senha aqui", font=("Serif", 20), text_color="#0333ce")
    texto.grid(row=0, column=0, pady=20, padx=20)

    escreva = ctk.CTkEntry(card_login, placeholder_text="Usuário", width=220)
    escreva.grid(row=1, column=0, pady=10, padx=20)

    escreva2 = ctk.CTkEntry(card_login, placeholder_text="Senha", width=220, show="*")
    escreva2.grid(row=2, column=0, pady=10, padx=20)

    escreva3 = ctk.CTkEntry(card_login, placeholder_text="Confirme a Senha", width=220, show="*")
    escreva3.grid(row=3, column=0, pady=10, padx=20)

    btn_entrar = ctk.CTkButton(card_login, text="Entrar", width=220, fg_color="#003cff")
    btn_entrar.grid(row=4, column=0, pady=20, padx=20)


    janela.mainloop()

if __name__ == "__main__":
    tela_principal()