import PySimpleGUI as sg
from sources.ytdownl_config import *


class Interface:
    def __init__(self):
        self.local_arquivo = ler_arquivo('./sources/path_file')

        sg.theme('DarkBlue13')

        frame_layout_0 = [
            [sg.Input(key='url', size=(53, 0))]
        ]

        frame_layout_1 = [
            [sg.Radio('Mp4', 'arquivo', key='mp4file', size=(12, 0))],
            [sg.Radio('Mp3', 'arquivo', key='mp3file', size=(12, 0))]
        ]

        frame_layout_2 = [
            [sg.Radio('720p', 'resolucao', key='video720p', size=(11, 0))],
            [sg.Radio('360p', 'resolucao', key='video360p', size=(11, 0))]
        ]

        frame_layout_3 = [
            [sg.Radio('128kbps', 'audio', key='128audio')],
            [sg.Radio('144kbps', 'audio', key='144audio')]
        ]

        layout = [
            [sg.Frame('Digite a URL do YouTube', frame_layout_0)],
            [sg.Output(size=(53, 3))],
            [sg.Frame('Formato do Arquivo', frame_layout_1), sg.Frame('Resolução do Vídeo', frame_layout_2), sg.Frame('Config de Audio', frame_layout_3)],
            [sg.Button('Baixar'), sg.Button('Alterar local da Pasta', key='savepath')]
        ]

        self.janela = sg.Window('Baixador de Vídeos do YouTube.').layout(layout)

    def iniciar(self):
        while True:
            eventos, valores = self.janela.read()

            if eventos == sg.WIN_CLOSED:
                break
            elif eventos == 'Baixar':
                url_video = valores['url']
                if url_video == '':
                    print('Cole o link do vídeo acima e marque ás opções de audio e vídeo abaixo.')

                if valores['mp4file'] == True and valores['video720p'] == True:
                    download_video(url_video, '720p', 'mp4', self.local_arquivo)
                elif valores['mp4file'] == True and valores['video360p'] == True:
                    download_video(url_video, '360p', 'mp4', self.local_arquivo)
                elif valores['mp3file'] == True and valores['128audio'] == True:
                    download_video(url_video, '128kbps', 'mp3', self.local_arquivo)
                elif valores['mp3file'] == True and valores['144audio'] == True:
                    download_video(url_video, '144kbps', 'mp3', self.local_arquivo)

            elif eventos == 'savepath':
                local_salvamento =  sg.popup_get_folder('Cole o local da pasta')
                gravar_arquivo('./sources/path_file', local_salvamento)
                print('Após selecionar o local de salvamento do arquivo é nesessário reniciar o programa para aplicar'
                      ' ás seguintes alterações.')

if __name__ == '__main__':
    Interface().iniciar()
