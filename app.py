
import customtkinter as ctk


class FormatArq(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self._border_width = 2

        self.texto = ctk.CTkLabel(
            self,
            text='Formato do Arquivo',
            corner_radius=6,
            fg_color='gray30',
        )
        self.texto.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.formato_arquivo = ctk.CTkOptionMenu(
            self,
            values=['mp4', 'mp3'],
            width=150,
            height=30,
        )
        self.formato_arquivo.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')


class ResVideo(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self._border_width = 2

        self.texto = ctk.CTkLabel(
            self,
            text='Resolução do Vídeo',
            corner_radius=6,
            fg_color='gray30',
        )
        self.texto.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.formato_arquivo = ctk.CTkOptionMenu(
            self,
            values=['720p', '360p'],
            width=150,
            height=30,
        )
        self.formato_arquivo.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')


class QualidadeAudio(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self._border_width = 2

        self.texto = ctk.CTkLabel(
            self,
            text='Resolução do Vídeo',
            corner_radius=6,
            fg_color='gray30',
        )
        self.texto.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.formato_arquivo = ctk.CTkOptionMenu(
            self,
            values=['128kbps', '144kbps'],
            width=150,
            height=30,
        )
        self.formato_arquivo.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')


class Content(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self._border_width = 2
        self.grid_columnconfigure((0, 1, 2), weight=1)
       # self.grid_rowconfigure(0, weight=1)

        self.entrada_usr = ctk.CTkEntry(
            self,
            placeholder_text='Digite a URL do Youtube',
            height=30
        )
        self.entrada_usr.grid(row=0, column=0, padx=10, pady=10, sticky='ew', columnspan=3)

        self.frame_layout_1 = FormatArq(self)
        self.frame_layout_1.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.frame_layout_2 = ResVideo(self)
        self.frame_layout_2.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        self.frame_layout_3 = QualidadeAudio(self)
        self.frame_layout_3.grid(row=2, column=2, padx=10, pady=10, sticky='w')

        self.btn = ctk.CTkButton(
            self,
            text='Baixar',
            width=150,
            height=30,
            border_color='white',
        )
        self.btn.grid(row=3, column=0, padx=10, pady=10, sticky='w')


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('dark')
      #  ctk.set_default_color_theme('themes/midnight.json')

        self.geometry('540x350')
        self.grid_columnconfigure([0], weight=1)
        self.grid_rowconfigure([0], weight=1)
        self.title('Baixador de vídeos do Youtube')
        self.resizable(False, False)

        self.content = Content(self)
        self.content.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')


if __name__ == '__main__':
    app = App()
    app.mainloop()
