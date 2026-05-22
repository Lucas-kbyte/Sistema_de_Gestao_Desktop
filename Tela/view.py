import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import cv2

# segundo teste disso
# AAAAAAAAAAAAAAAAAAAAAA DEUS SOCORROOOO!!!!

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def tela_principal():
    janela = ctk.CTk()
    janela.geometry("850x650") 
    janela.title("Sistema de Gestão 2.0")
    janela.minsize(800, 600)

    global cap
    cap = None

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
        if container_principal.winfo_children():
            for widget in container_principal.winfo_children():
                if hasattr(widget, 'identificador') and widget.identificador == "dash":
                    construir_dashboard()

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

    container_principal = ctk.CTkFrame(janela, fg_color="transparent")
    container_principal.place(relx=0.02, rely=0.03, relwidth=0.74, relheight=0.94)

    caixa_menu = ctk.CTkFrame(janela, corner_radius=10)
    caixa_menu.place(relx=0.78, rely=0.03, relwidth=0.20, relheight=0.94)
    caixa_menu.pack_propagate(False)

    lbl_menu = ctk.CTkLabel(
        caixa_menu, text="Opções", font=("Serif", 20, "bold"), text_color=cor_do_texto
    )
    lbl_menu.pack(pady=(30, 10), padx=15)

    btn_opcao1 = ctk.CTkButton(caixa_menu, text="Dashboard", width=140, command=lambda: mostrar_tela("dashboard"))
    btn_opcao1.pack(pady=10, padx=10)
    
    btn_ir_login = ctk.CTkButton(caixa_menu, text="Login", width=140, fg_color="transparent", border_width=1, command=lambda: mostrar_tela("login"))
    btn_ir_login.pack(pady=10, padx=10)

    btn_tema = ctk.CTkButton(
        caixa_menu, text="Modo Branco", fg_color="gray", hover_color="darkgray", command=alternar_tema, width=140
    )
    btn_tema.pack(side="bottom", pady=20, padx=10)

    def mostrar_tela(nome_tela):
        for widget in container_principal.winfo_children():
            widget.destroy()
            
        if nome_tela == "login":
            construir_login()
        elif nome_tela == "dashboard":
            construir_dashboard()

    def construir_login():
        caixa_login = ctk.CTkFrame(container_principal, width=460, height=580, corner_radius=10, fg_color="transparent")
        caixa_login.place(relx=0.5, rely=0.5, anchor="center")
        caixa_login.pack_propagate(False)

        caixa_login_bonito = ctk.CTkFrame(caixa_login, height=150)
        caixa_login_bonito.place(relx=0, rely=0, relwidth=1)
        caixa_login_bonito.pack_propagate(False)

        caixa_login_bonito_to = ctk.CTkFrame(caixa_login_bonito, height=35, fg_color="#5f5f5f")
        caixa_login_bonito_to.place(relx=0, rely=0.8, relwidth=1)
        caixa_login_bonito_to.pack_propagate(False)
        
        texto2 = ctk.CTkLabel(
            caixa_login_bonito, text="Sistema de Gestão 2.0", font=("Serif", 24, "bold"), text_color=cor_do_texto
        )
        texto2.pack(pady=(30, 10))

        texto = ctk.CTkLabel(
            caixa_login_bonito, text="Por favor, digite sua senha aqui", font=("Serif", 16), text_color=cor_do_texto
        )
        texto.pack(pady=0, padx=50)

        escreva = ctk.CTkEntry(caixa_login, placeholder_text="Usuário", width=240, text_color=cor_do_texto)
        escreva.pack(pady=(180, 15)) 

        escreva2 = ctk.CTkEntry(caixa_login, placeholder_text="Senha", width=240, show="*", text_color=cor_do_texto)
        escreva2.pack(pady=15, padx=10)

        escreva3 = ctk.CTkEntry(caixa_login, placeholder_text="Confirme a Senha", width=240, show="*", text_color=cor_do_texto)
        escreva3.pack(pady=15)

        btn_entrar = ctk.CTkButton(
            caixa_login, text="Entrar", width=240, fg_color="#003cff", command=lambda: mostrar_tela("dashboard")
        )
        btn_entrar.pack(pady=30)

    def construir_dashboard():
        caixa_dash = ctk.CTkFrame(container_principal, corner_radius=10, fg_color="transparent")
        caixa_dash.place(relx=0, rely=0, relwidth=1, relheight=1)
        caixa_dash.pack_propagate(False)
        caixa_dash.identificador = "dash"

        frame_topo = ctk.CTkFrame(caixa_dash, fg_color="transparent")
        frame_topo.pack(fill="x", padx=20, pady=(20, 10))

        lbl_dash_titulo = ctk.CTkLabel(
            frame_topo, text="Painel de Vendas", font=("Serif", 26, "bold"), text_color=cor_do_texto
        )
        lbl_dash_titulo.pack(side="left")

        def alternar_visao_interna(valores):
            for widget in frame_dinamico_dash.winfo_children():
                widget.destroy()
            if valores == "Gráfico":
                exibir_sub_grafico(frame_dinamico_dash, dados)
            elif valores == "Tabela":
                exibir_sub_tabela(frame_dinamico_dash, dados)

        seletor_visao = ctk.CTkSegmentedButton(
            frame_topo, values=["Gráfico", "Tabela"], command=alternar_visao_interna
        )
        seletor_visao.pack(side="right")
        seletor_visao.set("Tabela")

        dados = [] 

        frame_dinamico_dash = ctk.CTkFrame(caixa_dash, fg_color="transparent")
        frame_dinamico_dash.pack(expand=True, fill="both", padx=20, pady=(0, 20))

        exibir_sub_tabela(frame_dinamico_dash, dados)


    def exibir_sub_grafico(parent_frame, dados):
        if not dados:
            ctk.CTkLabel(parent_frame, text="Nenhum dado cadastrado para gerar o gráfico.", font=("Arial", 14, "italic")).pack(expand=True)
            return

        total = sum(item[1] for item in dados)
        canvas_grafico = ctk.CTkCanvas(parent_frame, bg="#1f1f1f", highlightthickness=0)
        canvas_grafico.pack(side="left", expand=True, fill="both", padx=(0, 20))

        frame_legendas = ctk.CTkFrame(parent_frame, fg_color="transparent")
        frame_legendas.pack(side="right", fill="y", padx=10, pady=20)
        
        ctk.CTkLabel(frame_legendas, text="Legenda:", font=("Arial", 16, "bold")).pack(anchor="w", pady=(0, 15))

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
            for nome, valor, cor, desc in dados:
                proporcao = valor / total if total > 0 else 0
                angulo_fatia = proporcao * 360
                canvas_grafico.create_arc(
                    x0, y0, x1, y1, start=angulo_inicial, extent=angulo_fatia, 
                    fill=cor, outline="#ffffff", width=1.5
                )
                angulo_inicial += angulo_fatia

        canvas_grafico.bind("<Configure>", desenhar_pizza)

        for nome, valor, cor, desc in dados:
            porcentagem = (valor / total) * 100 if total > 0 else 0
            linha_legenda = ctk.CTkFrame(frame_legendas, fg_color="transparent")
            linha_legenda.pack(anchor="w", pady=8)
            
            quadradinho = ctk.CTkFrame(linha_legenda, width=15, height=15, fg_color=cor, corner_radius=3)
            quadradinho.pack(side="left", padx=(0, 10))
            quadradinho.pack_propagate(False)
            
            lbl_texto_legenda = ctk.CTkLabel(linha_legenda, text=f"{nome}: {porcentagem:.1f}% (R$ {valor})")
            lbl_texto_legenda.pack(side="left")


    def exibir_sub_tabela(parent_frame, dados):
        if not dados:
            ctk.CTkLabel(parent_frame, text="A tabela está vazia. Insira dados para visualizar.", font=("Arial", 16, "italic"), text_color="gray").pack(expand=True)
            return

        tabela_scroll = ctk.CTkScrollableFrame(parent_frame, corner_radius=10)
        tabela_scroll.pack(expand=True, fill="both", pady=10)

        tabela_scroll.grid_columnconfigure(0, weight=2)
        tabela_scroll.grid_columnconfigure(1, weight=1)
        tabela_scroll.grid_columnconfigure(2, weight=3)

        headers = ["Categoria", "Faturamento", "Status / Observação"]
        for col_idx, texto_header in enumerate(headers):
            lbl_header = ctk.CTkLabel(
                tabela_scroll, text=texto_header, font=("Arial", 14, "bold"), 
                fg_color=("#c0c0c0", "#1f1f1f"), height=35, corner_radius=4
            )
            lbl_header.grid(row=0, column=col_idx, sticky="nsew", padx=2, pady=5)

        for row_idx, (nome, valor, cor, desc) in enumerate(dados, start=1):
            cor_linha = ("#f2f2f2", "#2d2d2d") if row_idx % 2 == 0 else ("#e6e6e6", "#242424")

            lbl_cat = ctk.CTkLabel(
                tabela_scroll, text=f"  ●  {nome}", font=("Arial", 13), 
                anchor="w", text_color=cor, fg_color=cor_linha, height=40
            )
            lbl_cat.grid(row=row_idx, column=0, sticky="nsew", padx=2, pady=2)

            lbl_val = ctk.CTkLabel(
                tabela_scroll, text=f"R$ {valor},00", font=("Arial", 13), anchor="center", fg_color=cor_linha
            )
            lbl_val.grid(row=row_idx, column=1, sticky="nsew", padx=2, pady=2)

            lbl_desc = ctk.CTkLabel(
                tabela_scroll, text=desc, font=("Arial", 13), anchor="w", fg_color=cor_linha, padx=10
            )
            lbl_desc.grid(row=row_idx, column=2, sticky="nsew", padx=2, pady=2)

    mostrar_tela("login")

    atualizar_frame()
    janela.mainloop()

    if cap is not None:
        cap.release()

if __name__ == "__main__":
    tela_principal()