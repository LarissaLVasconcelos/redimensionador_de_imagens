import customtkinter as ctk


from tkinter import filedialog, messagebox


from PIL import Image, ImageTk


from PIL import ImageGrab


from io import BytesIO



ctk.set_appearance_mode("System")


ctk.set_default_color_theme("blue")



original_image = None  # Variável para armazenar a imagem original


resize_button = None  # Variável para o botão de redimensionar


save_button = None  # Variável para o botão de salvar


revert_button = None  # Variável para o botão de reverter


def selecionar_imagem():


    global original_image  # Precisamos modificar a variável global


    file_path = filedialog.askopenfilename(


        title="Selecionar Imagem",


        filetypes=[("JPEG files", "*.jpg"),

                   ("PNG files", "*.png"), ("All files", "*.*")]
    )


    if file_path:


        image_path_entry.delete(0, ctk.END)


        image_path_entry.insert(0, file_path)


        original_image = Image.open(file_path)
        carregar_imagem(original_image)


def carregar_imagem(pil_image):


    try:


        global resize_button, save_button, revert_button


        pil_image.thumbnail((300, 300))


        img = ImageTk.PhotoImage(pil_image)


        image_display_label.configure(image=img)


        image_display_label.image = img


        # Mover a imagem para a esquerda

        image_display_label.place(x=300, y=100)


        # Reposicionar a seção de redimensionamento


        resize_frame.place(x=20, y=400)  # Posicionar abaixo da imagem


        # Adicionar botões de redimensionar, salvar, reverter se ainda não existirem


        if not resize_button:


            create_resize_button()


        if not save_button:

            create_save_button()


        if not revert_button:

            create_revert_button()


    except Exception as e:


        messagebox.showerror(

            "Erro", f"Não foi possível carregar a imagem: {e}")



def create_resize_button():


    global resize_button


    resize_button = ctk.CTkButton(

        resize_frame, text="Redimensionar", command=resize_image)


    resize_button.pack(side="left", padx=10, pady=10)



def create_save_button():

    global save_button


    save_button = ctk.CTkButton(

        resize_frame, text="Salvar", command=save_image)


    save_button.pack(side="left", padx=10, pady=10)



def create_revert_button():

    global revert_button


    revert_button = ctk.CTkButton(

        path_frame, text="Reverter", command=revert_image)


    revert_button.grid(row=0, column=2, padx=10, pady=10)



def destroy_resize_button():


    global resize_button


    if resize_button:


        resize_button.destroy()


        resize_button = None



def destroy_save_button():

    global save_button


    if save_button:


        save_button.destroy()


        save_button = None



def destroy_revert_button():

    global revert_button


    if revert_button:


        revert_button.destroy()


        revert_button = None



def revert_image():
    global original_image


    if original_image:
        carregar_imagem(original_image)


    else:


        messagebox.showerror("Erro", "Nenhuma imagem original carregada.")



def resize_image():


    file_path = image_path_entry.get()


    if not file_path:


        messagebox.showerror(

            "Erro", "Por favor, selecione ou insira o caminho de uma imagem.")
        return


    try:


        new_width = int(width_entry.get())


        new_height = int(height_entry.get())


        pil_image = Image.open(file_path)


        new_image = pil_image.resize((new_width, new_height))

        carregar_imagem(new_image)


    except ValueError:


        messagebox.showerror(

            "Erro", "Por favor, insira valores válidos para largura e altura.")


    except Exception as e:


        messagebox.showerror("Erro", f"Falha ao redimensionar a imagem: {e}")



def save_image():


    file_path = image_path_entry.get()


    if not file_path:


        messagebox.showerror(

            "Erro", "Por favor, selecione ou insira o caminho de uma imagem.")
        return


    try:


        save_path = filedialog.asksaveasfilename(


            defaultextension=".jpg",


            filetypes=[("JPEG files", "*.jpg"),

                       ("PNG files", "*.png"), ("All files", "*.*")]
        )


        if save_path:


            # Obter a região da tela onde o Label está localizado


            x = image_display_label.winfo_rootx()


            y = image_display_label.winfo_rooty()


            w = image_display_label.winfo_width()


            h = image_display_label.winfo_height()


            # Capturar a imagem da tela


            img = ImageGrab.grab(bbox=(x, y, x + w, y + h))


            # Salvar a imagem

            img.save(save_path)


            messagebox.showinfo("Sucesso", f"Imagem salva em: {save_path}")


    except Exception as e:


        messagebox.showerror("Erro", f"Falha ao salvar a imagem: {e}")



root = ctk.CTk()


root.title("Redimensionador de Imagens")


root.geometry("800x500")



frame = ctk.CTkFrame(root)


frame.pack(pady=20, padx=20, fill="both", expand=True)



# Seção de seleção e exibição de imagem


path_frame = ctk.CTkFrame(frame)


path_frame.pack(pady=10)



image_path_entry = ctk.CTkEntry(path_frame, width=400)


image_path_entry.grid(row=0, column=0, padx=10, pady=10)



select_button = ctk.CTkButton(

    path_frame, text="Selecionar Imagem", command=selecionar_imagem)


select_button.grid(row=0, column=1, padx=10, pady=10)



# Adicionando o botão Reverter no mesmo frame


revert_button = ctk.CTkButton(

    path_frame, text="Reverter", command=revert_image)


revert_button.grid(row=0, column=2, padx=10, pady=10)



# Removendo o texto do rótulo CTkLabel


image_display_label = ctk.CTkLabel(frame, text="")


image_display_label.pack(pady=20)



# Seção de redimensionamento


resize_frame = ctk.CTkFrame(frame)



width_label = ctk.CTkLabel(resize_frame, text="Largura:")


width_label.pack(side="left", padx=5, pady=5)



width_entry = ctk.CTkEntry(resize_frame, width=100)


width_entry.pack(side="left", padx=5, pady=5)



height_label = ctk.CTkLabel(resize_frame, text="Altura:")


height_label.pack(side="left", padx=5, pady=5)



height_entry = ctk.CTkEntry(resize_frame, width=100)


height_entry.pack(side="left", padx=5, pady=5)

root.mainloop()

