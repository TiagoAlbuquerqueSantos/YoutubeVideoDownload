
import customtkinter as ctk


class DownloadVideo(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry('400x200')
        self.resizable(False, False)

        ctk.CTkLabel(
            self,
            text='Baixando Vídeo...',
            width=150,
            height=30,
        ).place(relx=0.5, rely=0.2, anchor='center')

        self.barra_progresso = ctk.CTkProgressBar(
            self,
            orientation='horizontal',
            indeterminate_speed=0.5,
            mode='indeterminate',
            width=300,
        )
        self.barra_progresso.place(relx=0.5, rely=0.5, anchor='center')
        self.barra_progresso.start()

        self.btn_concluir = ctk.CTkButton(
            self,
            text='Concluir',
            width=140,
            height=30,
            border_width=1,
            command=self.fechar_janela,
            state='disabled'
        )
        self.btn_concluir.place(relx=0.47, rely=0.87, anchor='se')

        self.btn_cancelar = ctk.CTkButton(
            self,
            text='Cancelar',
            width=140,
            height=30,
            border_width=1,
            command=self.fechar_janela,
        )
        self.btn_cancelar.place(relx=0.53, rely=0.87, anchor='sw')

    def fechar_janela(self):
        self.destroy()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.segunda_janela = None

        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('themes/Cobalt.json')

        self.geometry('540x350')
        self.grid_columnconfigure([0], weight=1)
        self.grid_rowconfigure([0], weight=1)
        self.title('Baixador de vídeos do Youtube')
        self.resizable(False, False)

        self.conteudo = ctk.CTkFrame(self, border_width=1)

        self.frame_layout_1 = ctk.CTkFrame(self.conteudo, border_width=1)
        self.frame_layout_2 = ctk.CTkFrame(self.conteudo, border_width=1)
        self.frame_layout_3 = ctk.CTkFrame(self.conteudo, border_width=1)

        self.conteudo.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame_layout_1.grid_columnconfigure(0, weight=1)
        self.frame_layout_2.grid_columnconfigure(0, weight=1)
        self.frame_layout_3.grid_columnconfigure(0, weight=1)

        self.conteudo.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.frame_layout_1.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.frame_layout_2.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.frame_layout_3.grid(row=2, column=2, padx=10, pady=10, sticky='w')

        self.entrada_usr = ctk.CTkEntry(
            self.conteudo,
            placeholder_text='Digite a URL do Youtube',
            border_width=1,
            height=30
        )
        self.entrada_usr.grid(row=0, column=0, padx=10, pady=10, sticky='ew', columnspan=3)

        ctk.CTkLabel(
            self.frame_layout_1,
            text='Formato do Arquivo',
            corner_radius=6,
            fg_color='gray30',
        ).grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        ctk.CTkLabel(
            self.frame_layout_2,
            text='Resolução do Vídeo',
            corner_radius=6,
            fg_color='gray30',
        ).grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        ctk.CTkLabel(
            self.frame_layout_3,
            text='Config. de Áudio',
            corner_radius=6,
            fg_color='gray30',
        ).grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.formato_arquivo = ctk.CTkOptionMenu(
            self.frame_layout_1,
            values=['mp4', 'mp3'],
            width=150,
            height=30,
            command=self.esconder_menu_res_video,
        )
        self.formato_arquivo.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.res_video = ctk.CTkOptionMenu(
            self.frame_layout_2,
            values=['720p', '360p'],
            width=150,
            height=30,
        )
        self.res_video.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.config_audio = ctk.CTkOptionMenu(
            self.frame_layout_3,
            values=['128kbps', '144kbps'],
            width=150,
            height=30,
            state='disabled',
        )
        self.config_audio.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.btn = ctk.CTkButton(
            self.conteudo,
            text='Baixar',
            width=160,
            height=30,
            border_width=1,
            command=self.abrir_segunda_janela,
        )
        self.btn.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        # ctk.CTkOptionMenu(
        #     self.conteudo,
        #     values=['dark', 'light', 'system'],
        #     width=150,
        #     height=30,
        #     command=self.change_theme,
        # ).grid(row=3, column=1, padx=10, pady=10, sticky='w')

    def change_theme(self, new_theme):
        ctk.set_appearance_mode(new_theme)

    def esconder_menu_res_video(self, valor):
        if valor == 'mp3':
            self.res_video.configure(state='disabled')
        else:
            self.res_video.configure(state='normal')

        if valor == 'mp4':
            self.config_audio.configure(state='disabled')
        else:
            self.config_audio.configure(state='normal')

    def abrir_segunda_janela(self):
        if self.segunda_janela is None or not self.segunda_janela.winfo_exists():
            self.segunda_janela = DownloadVideo()
        else:
            self.segunda_janela.focus()


if __name__ == '__main__':
    app = App()
    app.mainloop()
