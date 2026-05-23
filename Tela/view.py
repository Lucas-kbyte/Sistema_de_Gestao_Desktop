import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import cv2
from Controlador.control import inserir_produto, inserir_usuario, atualizar_preco, buscar_produto, deletar_produto, verificar_login

# terceiro teste disso
# AAAAAAAAAAAAAAAAAAAAAA DEUS SOCORROOOO!!!!

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def tela_principal():
    janela = ctk.CTk()
    janela.geometry("950x700")
    janela.title("Sistema de Gestão 3.0")
    janela.minsize(850, 600)

    global cap, tela_atual
    cap = None
    tela_atual = None  

    def carregar_video_por_tema():
        global cap
        if cap is not None:
            cap.release()

        tema_atual = ctk.get_appearance_mode()
        if tema_atual == "Dark":
            cap = cv2.VideoCapture("radar.webm")
        else:
            cap = cv2.VideoCapture("cigs.webm")

    def alternar_tema():
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            btn_tema.configure(text="Modo Preto")
        else:
            ctk.set_appearance_mode("Dark")
            btn_tema.configure(text="Modo Branco")

        carregar_video_por_tema()
        if tela_atual and hasattr(tela_atual, 'identificador') and tela_atual.identificador == "dash":
            mostrar_tela("dashboard")

    carregar_video_por_tema()

    def atualizar_frame():
        global cap
        if cap is None or not cap.isOpened():
            lbl_video.after(20, atualizar_frame)
            return

        ret, frame = cap.read()
        if ret:
            largura_janela = janela.winfo_width()
            altura_janela = janela.winfo_height()

            if largura_janela > 1 and altura_janela > 1:
                frame = cv2.resize(frame, (largura_janela, altura_janela))

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            lbl_video.configure(image=img)
            lbl_video.image = img

            lbl_video.after(20, atualizar_frame)
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            lbl_video.after(20, atualizar_frame)

    cor_do_texto = ("blue", "red")

    lbl_video = ctk.CTkLabel(janela, text="")
    lbl_video.place(x=0, y=0, relwidth=1, relheight=1)

    caixa_menu = ctk.CTkFrame(janela, corner_radius=15, fg_color=("#f0f0f0", "#161616"), border_width=1, border_color="#333333")
    caixa_menu.pack_propagate(False)

    lbl_menu = ctk.CTkLabel(caixa_menu, text="Opções", font=("Arial", 20, "bold"), text_color=cor_do_texto)
    lbl_menu.pack(pady=(30, 20), padx=15)

    btn_opcao1 = ctk.CTkButton(caixa_menu, text="Dashboard", width=130, command=lambda: mostrar_tela("dashboard"))
    btn_opcao1.pack(pady=10, padx=10)
    
    btn_ir_login = ctk.CTkButton(caixa_menu, text="Sair / Logoff", width=130, fg_color="transparent", border_width=1, command=lambda: mostrar_tela("login"))
    btn_ir_login.pack(pady=10, padx=10)

    btn_tema = ctk.CTkButton(caixa_menu, text="Modo Branco", fg_color="gray", hover_color="darkgray", command=alternar_tema, width=130)
    btn_tema.pack(side="bottom", pady=20, padx=10)

    def mostrar_tela(nome_tela):
        global tela_atual
        if tela_atual is not None:
            tela_atual.destroy()
            
        if nome_tela == "login":
            caixa_menu.place_forget()
            construir_login()
        elif nome_tela == "dashboard":
            caixa_menu.place(relx=0.02, rely=0.03, relwidth=0.18, relheight=0.94)
            construir_dashboard()

    def construir_login():
        global tela_atual
        
        caixa_login = ctk.CTkFrame(janela, width=380, height=520, corner_radius=15, fg_color=("#ffffff", "#1e1e1e"), border_width=1, border_color="#444444")
        caixa_login.place(relx=0.5, rely=0.5, anchor="center") 
        caixa_login.pack_propagate(False)
        tela_atual = caixa_login

        texto2 = ctk.CTkLabel(caixa_login, text="Sistema de Gestão 3.0", font=("Arial", 22, "bold"), text_color=cor_do_texto)
        texto2.pack(pady=(25, 10))

        def mudar_modo_auth(modo):
            lbl_mensagem.configure(text="")
            if modo == "Login":
                escreva3.pack_forget()
                btn_acao.configure(text="Entrar", command=executar_login)
            else:
                lbl_mensagem.pack_forget()
                btn_acao.pack_forget()
                
                escreva3.pack(pady=10)
                lbl_mensagem.pack(pady=10)
                btn_acao.pack(side="bottom", pady=(0, 35))
                btn_acao.configure(text="Registrar", command=executar_cadastro)

        seletor_auth = ctk.CTkSegmentedButton(caixa_login, values=["Login", "Cadastro"], command=mudar_modo_auth)
        seletor_auth.pack(pady=(0, 20))
        seletor_auth.set("Login")

        escreva = ctk.CTkEntry(caixa_login, placeholder_text="Usuário", width=260, height=35)
        escreva.pack(pady=10) 

        escreva2 = ctk.CTkEntry(caixa_login, placeholder_text="Senha", width=260, height=35, show="*")
        escreva2.pack(pady=10)

        escreva3 = ctk.CTkEntry(caixa_login, placeholder_text="Confirme a Senha", width=260, height=35, show="*")

        lbl_mensagem = ctk.CTkLabel(caixa_login, text="", font=("Arial", 12, "bold"))
        lbl_mensagem.pack(pady=10)

        def executar_login():
            if verificar_login(escreva, escreva2, lbl_mensagem):
                mostrar_tela("dashboard")

        def executar_cadastro():
            inserir_usuario(escreva, escreva2, escreva3, lbl_mensagem)

        btn_acao = ctk.CTkButton(caixa_login, text="Entrar", width=260, height=40, font=("Arial", 14, "bold"), fg_color="#003cff", command=executar_login)
        btn_acao.pack(side="bottom", pady=(0, 35))

    def construir_dashboard():
        global tela_atual
        
        caixa_dash = ctk.CTkFrame(janela, corner_radius=15, fg_color=("#f5f5f5", "#141414"), border_width=1, border_color="#333333")
        caixa_dash.place(relx=0.22, rely=0.03, relwidth=0.76, relheight=0.94)
        caixa_dash.pack_propagate(False)
        caixa_dash.identificador = "dash"
        tela_atual = caixa_dash

        frame_topo = ctk.CTkFrame(caixa_dash, fg_color="transparent")
        frame_topo.pack(fill="x", padx=20, pady=(20, 10))

        lbl_dash_titulo = ctk.CTkLabel(frame_topo, text="Painel de Produtos", font=("Arial", 24, "bold"), text_color=cor_do_texto)
        lbl_dash_titulo.pack(side="left", padx=(0, 15))

        def alternar_visao_interna(valores):
            for widget in frame_dinamico_dash.winfo_children():
                widget.destroy()
            if valores == "Gráfico":
                exibir_sub_grafico(frame_dinamico_dash, dados)
            elif valores == "Tabela":
                exibir_sub_tabela(frame_dinamico_dash, dados)

        seletor_visao = ctk.CTkSegmentedButton(frame_topo, values=["Gráfico", "Tabela"], command=alternar_visao_interna)
        seletor_visao.pack(side="right")
        seletor_visao.set("Tabela")

        frame_formulario = ctk.CTkFrame(caixa_dash, fg_color=("#e9e9e9", "#1e1e1e"), corner_radius=10)
        frame_formulario.pack(fill="x", padx=20, pady=10)

        escreva_nome = ctk.CTkEntry(frame_formulario, placeholder_text="Nome do Produto", width=180)
        escreva_nome.grid(row=0, column=0, padx=10, pady=15)

        escreva_qtd = ctk.CTkEntry(frame_formulario, placeholder_text="Qtd", width=80)
        escreva_qtd.grid(row=0, column=1, padx=10, pady=15)

        escreva_preco = ctk.CTkEntry(frame_formulario, placeholder_text="Preço (Ex: 10.50)", width=120)
        escreva_preco.grid(row=0, column=2, padx=10, pady=15)

        lbl_msg_dash = ctk.CTkLabel(frame_formulario, text="", font=("Arial", 12, "bold"))
        lbl_msg_dash.grid(row=0, column=3, padx=15, pady=15)

        def recarregar_dados_dashboard():
            nonlocal dados
            dados_brutos = buscar_produto()
            dados = dados_brutos if dados_brutos is not None else []
            alternar_visao_interna(seletor_visao.get())

        def funcao_criar_produto():
            inserir_produto(escreva_nome, escreva_qtd, escreva_preco, lbl_msg_dash)
            recarregar_dados_dashboard()

        def funcao_atualizar_produto():
            atualizar_preco(escreva_nome, escreva_preco, lbl_msg_dash)
            recarregar_dados_dashboard()

        def funcao_excluir_produto():
            deletar_produto(escreva_nome, lbl_msg_dash)
            recarregar_dados_dashboard()

        frame_botoes = ctk.CTkFrame(caixa_dash, fg_color="transparent")
        frame_botoes.pack(fill="x", padx=20, pady=5)

        btn_criar = ctk.CTkButton(frame_botoes, text="+ Criar Produto", width=140, height=35, fg_color="green", hover_color="darkgreen", font=("Arial", 12, "bold"), command=funcao_criar_produto)
        btn_criar.pack(side="left", padx=5)

        btn_atualizar = ctk.CTkButton(frame_botoes, text="✎ Atualizar Preço", width=140, height=35, fg_color="#e67e22", hover_color="#d35400", font=("Arial", 12, "bold"), command=funcao_atualizar_produto)
        btn_atualizar.pack(side="left", padx=5)

        btn_excluir = ctk.CTkButton(frame_botoes, text="🗑 Excluir Produto", width=140, height=35, fg_color="red", hover_color="darkred", font=("Arial", 12, "bold"), command=funcao_excluir_produto)
        btn_excluir.pack(side="left", padx=5)

        frame_dinamico_dash = ctk.CTkFrame(caixa_dash, fg_color="transparent")
        frame_dinamico_dash.pack(expand=True, fill="both", padx=20, pady=(10, 20))

        dados = []
        recarregar_dados_dashboard()

    def exibir_sub_grafico(parent_frame, dados):
        if not dados:
            ctk.CTkLabel(parent_frame, text="Nenhum dado cadastrado.", font=("Arial", 14, "italic")).pack(expand=True)
            return

        total = sum(int(item[1]) for item in dados if str(item[1]).isdigit())
        if total == 0: total = 1

        canvas_grafico = ctk.CTkCanvas(parent_frame, bg="#1f1f1f", highlightthickness=0)
        canvas_grafico.pack(side="left", expand=True, fill="both", padx=(0, 20))

        frame_legendas = ctk.CTkFrame(parent_frame, fg_color="transparent")
        frame_legendas.pack(side="right", fill="y", padx=10, pady=20)
        
        ctk.CTkLabel(frame_legendas, text="Legenda:", font=("Arial", 16, "bold"), text_color=cor_do_texto).pack(anchor="w", pady=(0, 15))

        cores_padrao = ["#3498db", "#2ecc71", "#9b59b6", "#e74c3c", "#f1c40f", "#1abc9c"]

        def desenhar_pizza(event=None):
            canvas_grafico.delete("all")
            largura = canvas_grafico.winfo_width()
            altura = canvas_grafico.winfo_height()
            tamanho_raio = min(largura, altura) * 0.7
            
            x0 = (largura - tamanho_raio) / 2
            y0 = (altura - tamanho_raio) / 2
            x1 = x0 + tamanho_raio
            y1 = y0 + tamanho_raio
            
            angulo_inicial = 0
            for idx, item in enumerate(dados):
                nome = item[0]
                valor = int(item[1]) if str(item[1]).isdigit() else 0
                cor = item[2] if len(item) > 2 else cores_padrao[idx % len(cores_padrao)]
                
                proporcao = valor / total
                angulo_fatia = proporcao * 360
                canvas_grafico.create_arc(x0, y0, x1, y1, start=angulo_inicial, extent=angulo_fatia, fill=cor, outline="#ffffff", width=1.5)
                angulo_inicial += angulo_fatia

        canvas_grafico.bind("<Configure>", desenhar_pizza)

        for idx, item in enumerate(dados):
            nome = item[0]
            valor = int(item[1]) if str(item[1]).isdigit() else 0
            cor = item[2] if len(item) > 2 else cores_padrao[idx % len(cores_padrao)]
            
            porcentagem = (valor / total) * 100
            linha_legendas = ctk.CTkFrame(frame_legendas, fg_color="transparent")
            linha_legendas.pack(anchor="w", pady=8)
            
            quadradinho = ctk.CTkFrame(linha_legendas, width=15, height=15, fg_color=cor, corner_radius=3)
            quadradinho.pack(side="left", padx=(0, 10))
            quadradinho.pack_propagate(False)
            
            lbl_texto_legenda = ctk.CTkLabel(linha_legendas, text=f"{nome}: {porcentagem:.1f}%", text_color=cor_do_texto)
            lbl_texto_legenda.pack(side="left")

    def exibir_sub_tabela(parent_frame, dados):
        tabela_scroll = ctk.CTkScrollableFrame(parent_frame, corner_radius=10)
        tabela_scroll.pack(expand=True, fill="both", pady=10)

        tabela_scroll.grid_columnconfigure(0, weight=2)
        tabela_scroll.grid_columnconfigure(1, weight=1)
        tabela_scroll.grid_columnconfigure(2, weight=2)

        headers = ["Produto / Categoria", "Quantidade", "Preço"]
        for col_idx, texto_header in enumerate(headers):
            lbl_header = ctk.CTkLabel(tabela_scroll, text=texto_header, font=("Arial", 14, "bold"), fg_color=("#c0c0c0", "#1f1f1f"), height=35, corner_radius=4)
            lbl_header.grid(row=0, column=col_idx, sticky="nsew", padx=2, pady=5)

        for row_idx, item in enumerate(dados, start=1):
            nome = item[0]
            valor = item[1]
            preco = item[3] if len(item) > 3 else (item[2] if len(item) > 2 else "R$ 0.00")
            cor_indicador = item[2] if (len(item) > 2 and "#" in str(item[2])) else "#3498db"

            cor_linha = ("#f2f2f2", "#2d2d2d") if row_idx % 2 == 0 else ("#e6e6e6", "#242424")

            lbl_cat = ctk.CTkLabel(tabela_scroll, text=f"  ●  {nome}", font=("Arial", 13), anchor="w", text_color=cor_indicador, fg_color=cor_linha, height=40)
            lbl_cat.grid(row=row_idx, column=0, sticky="nsew", padx=2, pady=2)

            lbl_val = ctk.CTkLabel(tabela_scroll, text=str(valor), font=("Arial", 13), fg_color=cor_linha)
            lbl_val.grid(row=row_idx, column=1, sticky="nsew", padx=2, pady=2)

            lbl_preco = ctk.CTkLabel(tabela_scroll, text=str(preco), font=("Arial", 13), anchor="center", fg_color=cor_linha, padx=10)
            lbl_preco.grid(row=row_idx, column=2, sticky="nsew", padx=2, pady=2)

    mostrar_tela("login")
    atualizar_frame()
    janela.mainloop()

    if cap is not None:
        cap.release()

if __name__ == "__main__":
    tela_principal()