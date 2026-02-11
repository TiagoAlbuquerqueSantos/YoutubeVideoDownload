
import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_default_color_theme('green')

        self.geometry("600x600")

        self.radio = ctk.CTkRadioButton(self, text="MP4")
        self.radio.pack(anchor="w", padx=5, pady=5)

if __name__ == '__main__':
    app = App()
    app.mainloop()