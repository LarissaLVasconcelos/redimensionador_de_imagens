import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from PIL import ImageGrab
from io import BytesIO

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

imagem_original = None  # Variável para armazenar a imagem original
botao_redimensionar = None  # Variável para o botão de redimensionar
botao_salvar = None  # Variável para o botão de salvar
botao_reverter = None  # Variável para o botão de reverter

def selecionar_imagem():
    global imagem_original  # Precisamos modificar a variável global
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecionar Imagem",
        filetypes=[("Arquivos JPEG", "*.jpg"), ("Arquivos PNG", "*.png"), ("Todos os arquivos", "*.*")]
    )
    if caminho_arquivo:
        entrada_caminho_imagem.delete(0, ctk.END)
        entrada_caminho_imagem.insert(0, caminho_arquivo)
        imagem_original = Image.open(caminho_arquivo)
        exibir_imagem(imagem_original)

def exibir_imagem(pil_imagem):
    try:
        global botao_redimensionar, botao_salvar, botao_reverter
        pil_imagem.thumbnail((300, 300))
        img = ImageTk.PhotoImage(pil_imagem)
        rotulo_exibicao_imagem.configure(image=img)
        rotulo_exibicao_imagem.image = img
        rotulo_exibicao_imagem.place(x=300, y=100)  # Mover a imagem para a esquerda
        # Reposicionar a seção de redimensionamento
        quadro_redimensionamento.place(x=20, y=400)  # Posicionar abaixo da imagem
        
        # Adicionar botões de redimensionar, salvar, reverter se ainda não existirem
        if not botao_redimensionar:
            criar_botao_redimensionar()
        if not botao_salvar:
            criar_botao_salvar()
        if not botao_reverter:
            criar_botao_reverter()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível carregar a imagem: {e}")

def criar_botao_redimensionar():
    global botao_redimensionar
    botao_redimensionar = ctk.CTkButton(quadro_redimensionamento, text="Redimensionar", command=redimensionar_imagem)
    botao_redimensionar.pack(side="left", padx=10, pady=10)

def criar_botao_salvar():
    global botao_salvar
    botao_salvar = ctk.CTkButton(quadro_redimensionamento, text="Salvar", command=salvar_imagem)
    botao_salvar.pack(side="left", padx=10, pady=10)

def criar_botao_reverter():
    global botao_reverter
    botao_reverter = ctk.CTkButton(quadro_caminho, text="Reverter", command=reverter_imagem)
    botao_reverter.grid(row=0, column=2, padx=10, pady=10)

def destruir_botao_redimensionar():
    global botao_redimensionar
    if botao_redimensionar:
        botao_redimensionar.destroy()
        botao_redimensionar = None

def destruir_botao_salvar():
    global botao_salvar
    if botao_salvar:
        botao_salvar.destroy()
        botao_salvar = None

def destruir_botao_reverter():
    global botao_reverter
    if botao_reverter:
        botao_reverter.destroy()
        botao_reverter = None

def reverter_imagem():
    global imagem_original
    if imagem_original:
        exibir_imagem(imagem_original)
    else:
        messagebox.showerror("Erro", "Nenhuma imagem original carregada.")

def redimensionar_imagem():
    caminho_arquivo = entrada_caminho_imagem.get()
    if not caminho_arquivo:
        messagebox.showerror("Erro", "Por favor, selecione ou insira o caminho de uma imagem.")
        return

    try:
        nova_largura = int(entrada_largura.get())
        nova_altura = int(entrada_altura.get())
        pil_imagem = Image.open(caminho_arquivo)
        nova_imagem = pil_imagem.resize((nova_largura, nova_altura))
        exibir_imagem(nova_imagem)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos para largura e altura.")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao redimensionar a imagem: {e}")

def salvar_imagem():
    caminho_arquivo = entrada_caminho_imagem.get()
    if not caminho_arquivo:
        messagebox.showerror("Erro", "Por favor, selecione ou insira o caminho de uma imagem.")
        return

    try:
        caminho_salvar = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("Arquivos JPEG", "*.jpg"), ("Arquivos PNG", "*.png"), ("Todos os arquivos", "*.*")]
        )
        if caminho_salvar:
            # Obter a região da tela onde o Label está localizado
            x = rotulo_exibicao_imagem.winfo_rootx()
            y = rotulo_exibicao_imagem.winfo_rooty()
            w = rotulo_exibicao_imagem.winfo_width()
            h = rotulo_exibicao_imagem.winfo_height()
            # Capturar a imagem da tela
            img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            # Salvar a imagem
            img.save(caminho_salvar)
            messagebox.showinfo("Sucesso", f"Imagem salva em: {caminho_salvar}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao salvar a imagem: {e}")

root = ctk.CTk()
root.title("Redimensionador de Imagens")
root.geometry("800x500")

frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Seção de seleção e exibição de imagem
quadro_caminho = ctk.CTkFrame(frame)
quadro_caminho.pack(pady=10)

entrada_caminho_imagem = ctk.CTkEntry(quadro_caminho, width=400)
entrada_caminho_imagem.grid(row=0, column=0, padx=10, pady=10)

botao_selecionar = ctk.CTkButton(quadro_caminho, text="Selecionar Imagem", command=selecionar_imagem)
botao_selecionar.grid(row=0, column=1, padx=10, pady=10)

# Adicionando o botão Reverter no mesmo frame
botao_reverter = ctk.CTkButton(quadro_caminho, text="Reverter", command=reverter_imagem)
botao_reverter.grid(row=0, column=2, padx=10, pady=10)

# Removendo o texto do rótulo CTkLabel
rotulo_exibicao_imagem = ctk.CTkLabel(frame, text="")
rotulo_exibicao_imagem.pack(pady=20)

# Seção de redimensionamento
quadro_redimensionamento = ctk.CTkFrame(frame)

rotulo_largura = ctk.CTkLabel(quadro_redimensionamento, text="Largura:")
rotulo_largura.pack(side="left", padx=5, pady=5)

entrada_largura = ctk.CTkEntry(quadro_redimensionamento, width=100)
entrada_largura.pack(side="left", padx=5, pady=5)

rotulo_altura = ctk.CTkLabel(quadro_redimensionamento, text="Altura:")
rotulo_altura.pack(side="left", padx=5, pady=5)

entrada_altura = ctk.CTkEntry(quadro_redimensionamento, width=100)
entrada_altura.pack(side="left", padx=5, pady=5)

root.mainloop()

