
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Desarrollador: Cristian M. Veliz Cano
Nombre del Soft: "Editor de Video"
Verción del Soft-Ware:  v_09
Distribución:  Gratuita

# moviepy: Editar vídeo con Python
# Seguramente alguna vez habrás editado un vídeo usando una aplicación como Vegas,
# After Effects o Premiere, pero ¿y si te digo que también se puede editar vídeo con
# Python?. La librería moviepy nos permite cortar, unir, rotar y mucho más. Se trata
# de un paquete open source para Python, y que por supuesto es compatible con Linux,
# macOS y Windows. A continuación te enseño sus posibilidades, a manera de Ejemplo.
# Lo primero de todo, deberás instalar el paquete. Si ya tienes pip
# instalado, llama el siguiente comando en el terminal.
# pip install moviepy
# Vale, ya tenemos el paquete instalado, empecemos a usarlo. La mayoría de funcionalidades
# de moviepy, giran en torno a la clase VideoFileClip y AudioFileClip. La primera permite
# trabajar con vídeo y la segunda con audio.
# Importa el paquete.

# from moviepy.editor import *
# #Abre un video que tengas
# video = VideoFileClip("video_ejemplo.mp4")
# Una vez hemos abierto el vídeo, ya lo tenemos en video almacenado y podemos
# empezar a hacer cosas con el. A continuación te enseño.
# Rotar vídeo:
# Si llamamos al método rotate() y le pasamos un número como entrada con los grados
# que queremos rotar el vídeo, nos devolverá un VideoFileClip rotado. Si queremos
# guardar el vídeo tan solo hay que llamar a write_videofile() y decirle el nombre que queremos,
# Super Simple, Verdad?...

'''

##=========================================================================================================
##=========================================================================================================

from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QSizePolicy, \
QFileDialog, QMessageBox, QHBoxLayout, QSlider, QProgressBar, QMenu, QAction, QDialog, QShortcut, \
QTextEdit
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent, QMultimedia, QMediaMetaData
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QTime, QThread, pyqtSignal, QEvent, QTranslator, QLocale, QLibraryInfo
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette, QCursor, QKeySequence

##=========================================================================================================
##=========================================================================================================

from tkinter import *
import cv2
import shutil
import imutils
from PIL import Image as im_app
import numpy as np
import tempfile
import subprocess
import os, sys, time
from typing import Tuple

##===============================================================
##===============================================================
import moviepy

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips, vfx, clips_array
from moviepy.video.fx.all import resize

##=========================================================================================================

global file_path_end, trimmed_clip, clip, final_clip, file_name, output_format, file_path_open, file_path_open_audio, file_path_open_image

file_path_end = ""
file_name = ""
output_format = ""
file_path_open = ""
file_path_open_audio = ""
file_path_open_image = ""
working = ""
file_path_video = ""

trimmed_clip = None
clip = None
final_clip = None
##=========================================================================================================
##=========================================================================================================

## Get absolute path to resource, works for dev and for pyinstaller
class Path():
    
    def resource_path(relative_path):
        """Get absolute path to resource, works for dev and for pyinstaller"""
        try:
            #PyInstaller Create a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

##=========================================================================================================        
##=========================================================================================================

## Clase Principal [Editor de Video -v9]
class VideoPlayer(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()

##=========================================================================================================
##=========================================================================================================

    def initUI(self):

        self.setWindowTitle('Editor de Video -v9')

##=========================================================================================================
##=========================================================================================================

        self.raiz = Tk()
        ##Ajustando Geometry de App
        self.app_width = 725
        self.app_height = 525

        self.screen_width = self.raiz.winfo_screenwidth()
        self.screen_height = self.raiz.winfo_screenheight()

        self.pos_x = (self.screen_width / 2) - (self.app_width / 2)
        self.pos_y = (self.screen_height / 2) - (self.app_height / 2) -50
        
        self.setGeometry(int(self.pos_x),int(self.pos_y),int(self.app_width),int(self.app_height))   ##Forma Modificada Tkinter

##=========================================================================================================
##=========================================================================================================

        self.Ico_app = Path.resource_path('Ico\\1.png')
        self.setWindowIcon(QIcon(self.Ico_app))

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.font = QtGui.QFont()
        self.font.setPointSize(12)
        self.font.setBold(True)
        self.font.setWeight(50)

        self.file_path = ""
        self.output_name = ""
        self.Texto_Files = ""
        self.converted_current_time_1 = 0

        self.playlist = QMediaPlaylist()

        self.video_widget = QVideoWidget()
        self.video_widget.setStyleSheet("background-color:black;")
        self.video_widget.setGeometry(self.pos().x(), self.pos().y(), self.width(), self.height())

        self.player = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.player.setVideoOutput(self.video_widget)

        self.open_button = QPushButton('Abrir Video', self)
        self.open_button.clicked.connect(lambda: Open_All_Files.openFile(self))

        self.play_button = QPushButton('Play', self)
        self.play_button.clicked.connect(lambda: Play_All_Videos.playVideo(self))

        self.Union_Video = QPushButton('Unir Videos', self)
        self.Union_Video.clicked.connect(lambda: Acctions_App.merge_videos(self))

        self.time_vid_2 = QLabel(self)
        self.time_vid_2.setFont(self.font)
        self.time_vid_2.setStyleSheet('background-color:black; color: #ffffff')
        self.time_vid_2.setText(' Sts.')
        self.time_vid_2.setFixedWidth(85)
        self.time_vid_2.setFixedHeight(25)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.slider.setStyleSheet("QSlider::groove:horizontal {\n"
"    border: 1px solid #ffff00;\n"
"    height: 4px; \n"
"    background: #ffff00;\n"
" \n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background:   rgb(128, 0, 255);\n"
"    \n"
"    width: 9px;\n"
"    height:7px;\n"
"\n"
"left: 11px;\n"
"right: 11px;\n"
"\n"
"\n"
"    margin: -12px; \n"
"    border-radius:14px;\n"
"}\n"
"\n"
"\n"
"QSlider::add-page:horizontal{\n"
"background-color:white;\n"
"border: 1px solid white;\n"
"}\n"
"")
        self.slider.sliderMoved.connect(lambda position: Play_All_Videos.setSliderPosition(self, position))

        self.time_vid = QLabel(self)
        self.time_vid.setFont(self.font)
        self.time_vid.setStyleSheet('background-color:black; color: #ffffff')
        self.time_vid.setText('  00:00:00 | Vol ')
        self.time_vid.setFixedWidth(125)
        self.time_vid.setFixedHeight(30)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet('background-color:black; color: #ffffff')
        self.progress_bar.setMaximum(1000)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setFocusPolicy(Qt.NoFocus)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(self.player.volume())
        self.volume_slider.setSizePolicy(50, 50)
        self.volume_slider.setStyleSheet("QSlider::groove:horizontal {\n"
"    border: 1px solid #ffff00;\n"
"    height: 4px; \n"
"    background: #ffff00;\n"
" \n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background:   rgb(128, 0, 255);\n"
"    \n"
"    width: 9px;\n"
"    height:7px;\n"
"\n"
"left: 11px;\n"
"right: 11px;\n"
"\n"
"\n"
"    margin: -12px; \n"
"    border-radius:14px;\n"
"}\n"
"\n"
"\n"
"QSlider::add-page:horizontal{\n"
"background-color:white;\n"
"border: 1px solid white;\n"
"}\n"
"")
        self.volume_slider.sliderMoved.connect(self.player.setVolume)
        self.volume_slider.sliderMoved.connect(lambda e: Vol_App_Vid.Colocando_pos_vol(self, e))
        self.volume_slider.valueChanged.connect(self.player.setVolume)
        self.volume_slider.valueChanged.connect(lambda e: Vol_App_Vid.Colocando_pos_vol(self, e))
        #self.volume_slider.hide()

        self.trim_start_button = QPushButton('Recortar Inicio', self)
        self.trim_start_button.clicked.connect(lambda: Acctions_App.trimStart(self))

        self.trim_end_button = QPushButton('Recortar Final', self)
        self.trim_end_button.clicked.connect(lambda: Acctions_App.trimEnd(self))

        self.Converted_To_MP4_btn = QPushButton('Converted To MP3||WAV', self)
        self.Converted_To_MP4_btn.clicked.connect(lambda: Acctions_App.Conver_To_MP3_WAP(self))

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.video_widget)
        
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.open_button)

        t_layout = QHBoxLayout()
        t_layout.setContentsMargins(0, 0, 0, 0)
        t_layout.addWidget(self.time_vid_2)
        t_layout.addWidget(self.slider)
        t_layout.addWidget(self.time_vid)
        t_layout.addWidget(self.volume_slider)
        self.layout.addLayout(t_layout)

        trim_layout = QHBoxLayout()
        trim_layout.addWidget(self.play_button)
        trim_layout.addWidget(self.trim_start_button)
        trim_layout.addWidget(self.trim_end_button)
        trim_layout.addWidget(self.Union_Video)
        trim_layout.addWidget(self.Converted_To_MP4_btn)
        self.layout.addLayout(trim_layout)

        self.setLayout(self.layout)

        self.video_widget.installEventFilter(self)
        self.player.positionChanged.connect(lambda position: Play_All_Videos.position_changed(self, position))
        self.player.durationChanged.connect(lambda: Play_All_Videos.updateSlider(self))
        self.player.metaDataChanged.connect(lambda: VideoPlayer.meta_data(self, self.player))

        # Conecte a las funciones de visualización del menú
        self.video_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.video_widget.customContextMenuRequested.connect(lambda: Menu_Clic.Menu_RightClic(self))

        # Conecte a las funciones de visualización del menú
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(lambda: Menu_Clic.create_rightmenu(self))

        self.volume_slider.setValue(50)
        self.player.setVolume(50)

        self.set_aspect_ratio_mode(Qt.IgnoreAspectRatio)

        print("\n============================================")
        print("➜ Inniciando Labores en: <-|-> 🔥 Editor de Video -v9 <-|-> ✔️ Muchas Gracias...")
        print("============================================")

        Message_Box.Ms_Info(self)
        self.variables_utiles()
        
        # Atajo Ctrl + I para mostrar información del software
        info_software = QShortcut(QKeySequence('F1'), self)
        info_software.activated.connect(self.show_app_info)

        self.show()

##=========================================================================================================
##=========================================================================================================    
    # =========================
    ## Metodo Mostrar la Info, del Soft, en una Ventanita Emergente, enforma de Dialogo
    # =========================
    def show_app_info(self):
        dialog = app_info(self)
        dialog.exec_()

##=========================================================================================================
##=========================================================================================================

    def variables_utiles(self):

        self.Texto_N1, self.Texto_N2, self.Texto_N3 = "", "", ""
        self.Texto_N4, self.Texto_N5, self.Texto_N6 = "", "", ""

##=========================================================================================================
##=========================================================================================================

    def set_aspect_ratio_mode(self, mode):
        
        self.video_widget.setAspectRatioMode(mode)

##=========================================================================================================
##=========================================================================================================

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:        ## Key Board (Teclado - Tecla Escape (ESC))
            sys.exit()                          ## Exit (Clouse App) Cerrar la Aplicación

        elif event.key() == 73:                 ## I
            Message_Box.Ms_Info(self)           ## Informatión App

##=========================================================================================================
##=========================================================================================================

    def wheelEvent(self, event):

        #self.volume_slider.hide()
        num = event.angleDelta().y()

        if num == 120:

            self.Vol_Muted = False

            e = self.volume_slider.value() + 1

            if e == 101:
                pass

            else:

                Vol_App_Vid.Colocando_pos_vol(self, e)

        else:

            self.Vol_Muted = False

            e = self.volume_slider.value() - 1

            if e <= -1:
                pass

            else:

                Vol_App_Vid.Colocando_pos_vol(self, e)

    def eventFilter(self, obj, event):

        if event.type() == QEvent.MouseButtonPress:
            Play_All_Videos.playVideo(self)

        return False

##=========================================================================================================
##=========================================================================================================
    
    # Shorten text that may be too long
    def _truncate(self, text, length=25):

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ...."

    def meta_data(self, player):

        if player.isMetaDataAvailable():

            if player.metaData(QMediaMetaData.AlbumArtist):
                self.Texto_N1 = str('Artista:  ' + player.metaData(QMediaMetaData.AlbumArtist)) + '\n'
            
            if player.metaData(QMediaMetaData.AlbumTitle):
                self.Texto_N2 = str('Nombre del Albun:  ' + self._truncate(player.metaData(QMediaMetaData.AlbumTitle))) + '\n'    
            
            if player.metaData(QMediaMetaData.Title):
                self.Texto_N3 = str('Nombre del Medio:  ' + self._truncate(player.metaData(QMediaMetaData.Title))) + '\n'
            
            if player.metaData(QMediaMetaData.Year):
                self.Texto_N4 = str('Año de Producción:  ' + f'{player.metaData(QMediaMetaData.Year)}') + '\n'
            
            if player.metaData(QMediaMetaData.Genre):
                self.Texto_N5 = str('Genero:  ' + str(player.metaData(QMediaMetaData.Genre)[0])) + '\n'
            
            if player.metaData(QMediaMetaData.Title):
                self.Texto_N6 = str('Nombre del Track:  ' + f'{self._truncate(player.metaData(QMediaMetaData.Title),20)}') + '\n'

            self.Texto_Files = str(self.Texto_N1 + self.Texto_N2 + self.Texto_N3 + self.Texto_N4 + self.Texto_N5 + self.Texto_N6)

            return self.Texto_Files

##=========================================================================================================
##=========================================================================================================

## Control de Volumen en Video
class Vol_App_Vid(VideoPlayer):

    def __init__(self):
        super().__init__()

    def Colocando_pos_vol(self, e):

        self.player.setVolume(e)
        self.volume_slider.setValue(e)

##=========================================================================================================
##=========================================================================================================

## Controla los Mensajes Emitidos, en la App
class Message_Box(VideoPlayer):

    def __init__(self):
        super().__init__()

    def Ms_Info(self):
        print("\n============================================")
        print("➜ Innico: Mensaje de Bienvenida...")
        print("============================================")

        QMessageBox.information(self, 'Información', 'Este Soft esta Desarrollado, muy Minimalista,\
            \nPero, esta enfocado a Editar Videos con las Extenciónes de Archivos:\
            \n("*.mp4") y ("*.avi").- \
            \n\nDesarrollado por:  Cristian M. Velilz Cano\
            \nNombre del Soft-Ware:  \"Editor de Video\"\
            \nVerción del Soft-Ware: v_09.\
            \n\nCon este pequeño Soft-Ware, podremos, Quitar de Forma eficiente, el\
            \nInnicio, sea el tiempo que estimemos, como tambien Quitar de Forma\
            \nEficiente, el final del mismo, con el tiempo que estimemos, asi como\
            \nTambien, podremos, Unir Varios Videos a la Vez, es decir que podremos\
            \nUnir 1 o 2 o etc. de Videos a su mismo Tiempo.-\
            \n\nDistribución:  \"Gratuita\"\
            \n\nCon la Tecla ESC [Escape], Cerraremos el Soft.-\
            \nPara Mas Información Pulsa la Tecla F1 (Help)')

    def Ms_Info_star(self):
        global working, file_path_video

        QMessageBox.information(self, 'Información', 'Fabor, dar Tiempo hasta que este concluya con sus\
        \nsus labores, reproduciendo, en el Visor de Videos, el Video Trabajado.\
        \n\nMuchas Gracias, por su tiempo...')

        working = str("Procesando Solicitud...")
        title_video.Actualizando_Title(self, file_path_video)

    def dialog_critical(self, e):

        print("\n============================================")
        print('Error: ' + ' Se ha cometido un \"Error\", El Error Es: \n{}'.format(e))
        print("============================================")

        s = 'Error: ' + ' Se ha cometido un \"Error\", El Error Es:\
        \n{}'.format(e)
        dlg = QMessageBox(self)
        dlg.setText(str(s))
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

##=========================================================================================================
##=========================================================================================================

## En está Classe, Controlaremos, la Malloria, de los Distitons Metodos, para los Distintos, que
## Haceres en la App
class Acctions_App(VideoPlayer):

    def __init__(self):
        super().__init__()

    def concluidas_las_tareas(self):
        global working

        print("\n============================================")
        print("En cuanto sea Concluida la Solicitud, Se le Dara Aviso...")
        print("============================================")

        working = str("Concluida la Solicitud...")
        return None

    ## Recortar Inicio
    def trimStart(self):
        global file_path_end, trimmed_clip, clip
        print("\n============================================")
        print("➜ Innicio: Recortar Innicio de Video...")
        print("============================================")

        Play_All_Videos.playVideo(self)
        
        if self.player.state() == QMediaPlayer.PlayingState:

            Play_All_Videos.playVideo(self)

            QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

            file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ## (self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

            if file_path == [] or file_path == "":
                    
                QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                Acctions_App.concluidas_las_tareas(self)

            else:

                try:

                    file_path_end = file_path

                    current_position = self.player.position()
                    current_position = current_position

                    clip = Acctions_App.createVideoClip(self)
                    clip = clip
                
                    trimmed_clip = clip.subclip(current_position / 1000, clip.end)
                    trimmed_clip = trimmed_clip

                except Exception as e:
                    print(e)

                    Message_Box.dialog_critical(self, str(f'{e}'))
                    Acctions_App.concluidas_las_tareas(self)

                    return 

                Message_Box.Ms_Info_star(self)

                self.progress_bar.setValue(0)
                self.thread_1 = MergeThread2(file_path_end, self.player, index=2)
                self.thread_1.innicio_1.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                self.thread_1.any_signal_1.connect(lambda counter: Acctions_App.my_function(self, counter))
                self.thread_1.video_merged_1.connect(lambda: Play_All_Videos.display_video(self, file_path_end))
                self.thread_1.any_error_1.connect(lambda error: Acctions_App.my_function_error(self, error))
                self.thread_1.concluyo_1.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                self.thread_1.start()

                Acctions_App.concluidas_las_tareas(self)

        elif self.player.state() == 2:

            QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

            file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ## (self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

            if file_path == [] or file_path == "":
                    
                QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                Acctions_App.concluidas_las_tareas(self)

            else:

                file_path_end = file_path

                current_position = self.player.position()
                current_position = current_position

                clip = Acctions_App.createVideoClip(self)
                clip = clip
                
                trimmed_clip = clip.subclip(current_position / 1000, clip.end)
                trimmed_clip = trimmed_clip

                Message_Box.Ms_Info_star(self)

                self.progress_bar.setValue(0)
                self.thread_1 = MergeThread2(file_path_end, self.player, index=2)
                self.thread_1.innicio_1.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                self.thread_1.any_signal_1.connect(lambda counter: Acctions_App.my_function(self, counter))
                self.thread_1.video_merged_1.connect(lambda: Play_All_Videos.display_video(self, file_path_end))
                self.thread_1.any_error_1.connect(lambda error: Acctions_App.my_function_error(self, error))
                self.thread_1.concluyo_1.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                self.thread_1.start()

                Acctions_App.concluidas_las_tareas(self)

    ## Recortar Final
    def trimEnd(self):
        global file_path_end, trimmed_clip, clip
        print("\n============================================")
        print("➜ Innicio: Recortar Final...")
        print("============================================")

        Play_All_Videos.playVideo(self)

        if self.player.state() == QMediaPlayer.PlayingState:
            Play_All_Videos.playVideo(self)

            QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

            file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ##(self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

            if file_path == [] or file_path == "":
                    
                QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                Acctions_App.concluidas_las_tareas(self)

            else:

                try:

                    file_path_end = file_path

                    current_position = self.player.position()
                    clip = Acctions_App.createVideoClip(self)
                    
                    trimmed_clip = clip.subclip(0, current_position / 1000)
                    trimmed_clip = trimmed_clip

                except Exception as e:
                    print(e)

                    Message_Box.dialog_critical(self, str(f'{e}'))
                    Acctions_App.concluidas_las_tareas(self)

                    return

                Message_Box.Ms_Info_star(self)

                self.progress_bar.setValue(0)
                self.thread_2 = MergeThread3(self.player, file_path_end, index=2)
                self.thread_2.innicio_2.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                self.thread_2.any_signal_2.connect(lambda counter: Acctions_App.my_function(self, counter))
                self.thread_2.video_merged_2.connect(lambda: Play_All_Videos.display_video(self, file_path_end))
                self.thread_2.any_error_2.connect(lambda error: Acctions_App.my_function_error(self, error))
                self.thread_2.concluyo_2.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                self.thread_2.start()

                Acctions_App.concluidas_las_tareas(self)

        elif self.player.state() == 2:

            QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

            file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ##(self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

            if file_path == [] or file_path == "":
                    
                QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                Acctions_App.concluidas_las_tareas(self)

            else:

                file_path_end = file_path

                current_position = self.player.position()
                clip = Acctions_App.createVideoClip(self)
                
                trimmed_clip = clip.subclip(0, current_position / 1000)
                trimmed_clip = trimmed_clip

                Message_Box.Ms_Info_star(self)

                self.progress_bar.setValue(0)
                self.thread_2 = MergeThread3(self.player, file_path_end, index=2)
                self.thread_2.innicio_2.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                self.thread_2.any_signal_2.connect(lambda counter: Acctions_App.my_function(self, counter))
                self.thread_2.video_merged_2.connect(lambda: Play_All_Videos.display_video(self, file_path_end))
                self.thread_2.any_error_2.connect(lambda error: Acctions_App.my_function_error(self, error))
                self.thread_2.concluyo_2.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                self.thread_2.start()

                Acctions_App.concluidas_las_tareas(self)

    ## Converted To MP4
    def convert_video(self):
        global file_name, output_format, file_path_open
        print("\n============================================")
        print("➜ Innicio: Converted To...")
        print("============================================")

        file_name = file_path_open
        
        if file_path_open == "":
            pass

        else:

            Play_All_Videos.playVideo(self)

            QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')
            
            output_format = QFileDialog.getSaveFileName(self, "Guardar Video Convertido", filter="MP4: (*.mp4) ;; AVI: (*.avi) ;; MOV: (*.mov) ;; WMV: (*.wmv)  ;; OGV: (*.ogv) ;; WEBM: (*.webm) ")[0] ##(self, 'Guardar video recortado', '', 'Video Files (*.mp4 *.avi)')

            if output_format == [] or output_format == "":
                    
                QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                Acctions_App.concluidas_las_tareas(self)

            else:

                output_file, output_extension = os.path.splitext(output_format)
                output_extension = output_extension[1:].lower()

                file_path_end = output_format

                if output_extension == 'mp4':

                    Acctions_App.Extencion_Vid(self, output_extension, file_path_end)

                elif output_extension == 'avi':

                    Acctions_App.Extencion_Vid(self, output_extension, file_path_end)

                elif output_extension == 'mov':

                    Acctions_App.Extencion_Vid(self, output_extension, file_path_end)

                elif output_extension == 'wmv':

                    Acctions_App.Extencion_Vid(self, output_extension, file_path_end)

                elif output_extension == 'ogv':

                    Acctions_App.Extencion_Vid(self, output_extension, file_path_end)

                elif output_extension == 'webm':

                    Acctions_App.Extencion_Vid(self, output_extension, file_path_end)

                else:
                    print("\n============================================")
                    print('Formato de salida no válido. Por favor, seleccione MP4 o AVI.')
                    print("============================================")

    def Extencion_Vid(self, ext, file_path_end):

        Message_Box.Ms_Info_star(self)        
        self.progress_bar.setValue(0)

        self.thread_3 = MergeThread4(self.player, file_path_end, ext, index=3)
        self.thread_3.innicio_3.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
        self.thread_3.any_signal_3.connect(lambda counter: Acctions_App.my_function(self, counter))
        self.thread_3.video_merged_3.connect(lambda: Play_All_Videos.display_video(self, file_path_end))
        self.thread_3.any_error_3.connect(lambda error: Acctions_App.my_function_error(self, error))
        self.thread_3.concluyo_3.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
        self.thread_3.start()

        Acctions_App.concluidas_las_tareas(self)

    ## Unir Videos
    def merge_videos(self):
        global final_clip
        print("\n============================================")
        print("➜ Innicio: Uniendo Video...")
        print("============================================")
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        
        file_names, _ = QFileDialog.getOpenFileNames(self, 'Seleccionar Videos', '', 'Videos (*.mp4 *.avi);;All Files (*)', options=options)
        if file_names:
            clips = []

            try:
                for file_name in file_names:
                    clip = VideoFileClip(file_name)
                    clips.append(clip)

            except Exception as e:
                print(e)

                Message_Box.dialog_critical(self, str(f'{e}'))
                Acctions_App.concluidas_las_tareas(self)

                return
                
            final_clip = concatenate_videoclips(clips)

            QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

            file_path = QFileDialog.getSaveFileName(self, "Guardar Unión de videos como", filter="MP4(*.mp4)")[0] ##(self, 'Guardar video recortado', '', 'Video Files (*.mp4 *.avi)')

            if file_path == [] or file_path == "":
                    
                QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                Acctions_App.concluidas_las_tareas(self)

            else:

                Message_Box.Ms_Info_star(self)

                try:
            
                    self.file_path = file_path
                    self.progress_bar.setValue(0)
                    self.thread = MergeThread(self.player, file_names, file_path, index=1)
                    self.thread.innicio.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                    self.thread.any_signal.connect(lambda counter: Acctions_App.my_function(self, counter))
                    self.thread.video_merged.connect(lambda: Play_All_Videos.display_video(self, self.file_path))
                    self.thread.any_error.connect(lambda error: Acctions_App.my_function_error(self, error))
                    self.thread.concluyo.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                    self.thread.start()

                finally:
                    Acctions_App.concluidas_las_tareas(self)

    ## Utilizado en: --> Recortar Inicio |-| Recortar Final
    def createVideoClip(self):

        file_path = self.player.currentMedia().canonicalUrl().toLocalFile()
        return VideoFileClip(file_path)

    ## Quitar Sonido
    def quitar_audio_video(self):
        global file_path_end, file_path_open
        print("\n============================================")
        print("➜ Innicio: Quitar Sonido...")
        print("============================================")

        if file_path_open == "":

            e = str('Cancelaste la Busqueda de Medios (MP4),\nO no la Innciaste.')
            Message_Box.dialog_critical(self, e)
            Acctions_App.concluidas_las_tareas(self)

        else:

            Play_All_Videos.playVideo(self)

            if self.player.state() == QMediaPlayer.PlayingState:
                Play_All_Videos.playVideo(self)

                QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
    \nMuchas Gracias...')

                file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ##(self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

                if file_path == [] or file_path == "":
                        
                    QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                    Acctions_App.concluidas_las_tareas(self)

                else:

                    file_path_end = file_path
                    Message_Box.Ms_Info_star(self)

                    try:

                        self.progress_bar.setValue(0)
                        self.thread_5 = MergeThread5(self.player, file_path_end, index=5)
                        self.thread_5.innicio_5.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                        self.thread_5.any_signal_5.connect(lambda counter: Acctions_App.my_function(self, counter))
                        self.thread_5.video_merged_5.connect(lambda: Play_All_Videos.display_video(self, file_path_end))
                        self.thread_5.any_error_5.connect(lambda error: Acctions_App.my_function_error(self, error))
                        self.thread_5.concluyo_5.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                        self.thread_5.start()

                    except Exception as e:
                        print(e)

                        Message_Box.dialog_critical(self, str(f'{e}'))
                        Acctions_App.concluidas_las_tareas(self)

                    finally:
                        Acctions_App.concluidas_las_tareas(self)

            elif self.player.state() == 2:

                QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

                file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ##(self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

                if file_path == [] or file_path == "":
                        
                    QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                    Acctions_App.concluidas_las_tareas(self)

                else:

                    file_path_end = file_path
                    Message_Box.Ms_Info_star(self)

                    try:

                        self.progress_bar.setValue(0)
                        self.thread_5 = MergeThread5(self.player, file_path_end, index=5)
                        self.thread_5.innicio_5.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                        self.thread_5.any_signal_5.connect(lambda counter: Acctions_App.my_function(self, counter))
                        self.thread_5.video_merged_5.connect(lambda: Play_All_Videos.display_video(self, file_path_end))
                        self.thread_5.any_error_5.connect(lambda error: Acctions_App.my_function_error(self, error))
                        self.thread_5.concluyo_5.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                        self.thread_5.start()

                    except Exception as e:
                        print(e)

                        Message_Box.dialog_critical(self, str(f'{e}'))
                        Acctions_App.concluidas_las_tareas(self)

                    finally:
                        Acctions_App.concluidas_las_tareas(self)

    ## Agregar Sonido
    def agregar_audio_video(self):
        global file_path_open, file_path_open_audio, file_path_end
        print("\n============================================")
        print("➜ Innicio: Agregar Sonido...")
        print("============================================")

        if file_path_open == "":

            e = str('Cancelaste la Busqueda de Medios (MP4),\nO no la Innciaste.')
            Message_Box.dialog_critical(self, e)
            Acctions_App.concluidas_las_tareas(self)

        else:

            Play_All_Videos.playVideo(self)

            if self.player.state() == QMediaPlayer.PlayingState:
                Play_All_Videos.playVideo(self)

                QMessageBox.information(self, 'Aviso', 'Fabor de Agregar un Audio para Fucionar con el Video.\
\nMuchas Gracias...')

                file_path_open_audio = Open_All_Files.openFile_audio(self)
                file_path_open_audio = file_path_open_audio

                QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

                file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ##(self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))
                file_path_end = file_path
                if file_path == [] or file_path == "":
                        
                    QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                    Acctions_App.concluidas_las_tareas(self)

                else:

                    file_path_end = file_path
                    Message_Box.Ms_Info_star(self)

                    try:

                        self.progress_bar.setValue(0)
                        self.thread_6 = MergeThread6(self.player, file_path_end, index=6)
                        self.thread_6.innicio_6.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                        self.thread_6.any_signal_6.connect(lambda counter: Acctions_App.my_function(self, counter))
                        self.thread_6.video_merged_6.connect(lambda: Play_All_Videos.display_video(self, file_path_end))
                        self.thread_6.any_error_6.connect(lambda error: Acctions_App.my_function_error(self, error))
                        self.thread_6.concluyo_6.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                        self.thread_6.start()

                    except Exception as e:
                        print(e)

                        Message_Box.dialog_critical(self, str(f'{e}'))
                        Acctions_App.concluidas_las_tareas(self)

                    finally:
                        Acctions_App.concluidas_las_tareas(self)

            elif self.player.state() == 2:

                QMessageBox.information(self, 'Aviso', 'Fabor de Agregar un Audio para Fucionar con el Video.\
\nMuchas Gracias...')

                file_path_open_audio = Open_All_Files.openFile_audio(self)
                file_path_open_audio = file_path_open_audio

                QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

                file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ##(self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))
                file_path_end = file_path
                if file_path == [] or file_path == "":
                        
                    QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                    Acctions_App.concluidas_las_tareas(self)

                else:

                    file_path_end = file_path
                    Message_Box.Ms_Info_star(self)

                    try:

                        self.progress_bar.setValue(0)
                        self.thread_6 = MergeThread6(self.player, file_path_end, index=6)
                        self.thread_6.innicio_6.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                        self.thread_6.any_signal_6.connect(lambda counter: Acctions_App.my_function(self, counter))
                        self.thread_6.video_merged_6.connect(lambda: Play_All_Videos.display_video(self, file_path_end))
                        self.thread_6.any_error_6.connect(lambda error: Acctions_App.my_function_error(self, error))
                        self.thread_6.concluyo_6.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                        self.thread_6.start()

                    except Exception as e:
                        print(e)

                        Message_Box.dialog_critical(self, str(f'{e}'))
                        Acctions_App.concluidas_las_tareas(self)

                    finally:
                        Acctions_App.concluidas_las_tareas(self)

    ## Ajustar Video Poco
    def ajustar_video_poco(self):
        Acctions_App.ajustar_video(self, 1, 1, 1)       ## Rojo - Verde - Azul

    ## Ajustar Video Medio
    def ajustar_video_medio(self):
        Acctions_App.ajustar_video(self, 2, 2, 2)        ## Rojo - Verde - Azul

    ## Ajustar Video Alto
    def ajustar_video_alto(self):
        Acctions_App.ajustar_video(self, 3, 3, 3)        ## Rojo - Verde - Azul

    def ajustar_video(self, brillo, contraste, saturacion):
        global file_path_end, file_path_open        
        print("\n============================================")
        print("➜ Innicio: Ajuste de Video en Brillo...")
        print("============================================")

        if file_path_open == "":

            e = str('Cancelaste la Busqueda de Medios (MP4),\nO no la Innciaste.')
            Message_Box.dialog_critical(self, e)
            Acctions_App.concluidas_las_tareas(self)

        else:

            Play_All_Videos.playVideo(self)

            if self.player.state() == QMediaPlayer.PlayingState:
                Play_All_Videos.playVideo(self)

                QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

                file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ##(self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

                if file_path == [] or file_path == "":
                        
                    QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                    Acctions_App.concluidas_las_tareas(self)

                else:

                    file_path_end = file_path
                    Message_Box.Ms_Info_star(self)

                    try:

                        self.progress_bar.setValue(0)
                        self.thread_7 = MergeThread7(self.player, file_path_end, brillo, contraste, saturacion, index=7)
                        self.thread_7.innicio_7.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                        self.thread_7.any_signal_7.connect(lambda counter: Acctions_App.my_function(self, counter))
                        self.thread_7.video_merged_7.connect(lambda: Play_All_Videos.display_video(self, file_path_end))
                        self.thread_7.any_error_7.connect(lambda error: Acctions_App.my_function_error(self, error))
                        self.thread_7.concluyo_7.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                        self.thread_7.start()

                    except Exception as e:
                        print(e)

                        Message_Box.dialog_critical(self, str(f'{e}'))
                        Acctions_App.concluidas_las_tareas(self)

                    finally:
                        Acctions_App.concluidas_las_tareas(self)

            elif self.player.state() == 2:

                QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

                file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ##(self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

                if file_path == [] or file_path == "":
                        
                    QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                    Acctions_App.concluidas_las_tareas(self)

                else:

                    file_path_end = file_path
                    Message_Box.Ms_Info_star(self)

                    try:

                        self.progress_bar.setValue(0)
                        self.thread_7 = MergeThread7(self.player, file_path_end, brillo, contraste, saturacion, index=7)
                        self.thread_7.innicio_7.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                        self.thread_7.any_signal_7.connect(lambda counter: Acctions_App.my_function(self, counter))
                        self.thread_7.video_merged_7.connect(lambda: Play_All_Videos.display_video(self, file_path_end))
                        self.thread_7.any_error_7.connect(lambda error: Acctions_App.my_function_error(self, error))
                        self.thread_7.concluyo_7.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                        self.thread_7.start()

                    except Exception as e:
                        print(e)

                        Message_Box.dialog_critical(self, str(f'{e}'))
                        Acctions_App.concluidas_las_tareas(self)

                    finally:
                        Acctions_App.concluidas_las_tareas(self)

##============================================================================================
##============================================================================================
    
    ## Efecto Blanco y Negro
    def Efecto_blanco_negro(self):

        efecto = "blanco_negro"
        r, v, a = 0, 0, 0
        colores = (r, v, a)
        Acctions_App.ajustar_efecto_video(self, efecto, colores)
    
    ## Efecto Blanco y Sepia
    def Efecto_Sepia(self):

        efecto = "sepia"
        r, v, a = 166, 125, 2
        colores = (r, v, a)
        Acctions_App.ajustar_efecto_video(self, efecto, colores)
    
    ## Efecto Blanco y Azul
    def Efecto_Azul(self):

        efecto = "azul"
        r, v, a = 0, 0, -1
        colores = (r, v, a)
        Acctions_App.ajustar_efecto_video(self, efecto, colores)
    
    ## Efecto Blanco y Rojo
    def Efecto_Rojo(self):

        efecto = "rojo"
        r, v, a = -1, 0, 0
        colores = (r, v, a)
        Acctions_App.ajustar_efecto_video(self, efecto, colores)
    
    ## Efecto Blanco y Verde
    def Efecto_Verde(self):

        efecto = "verde"
        r, v, a = 0, -1, 0
        colores = (r, v, a)
        Acctions_App.ajustar_efecto_video(self, efecto, colores)
    
    ## Efecto Blanco y Amarillo
    def Efecto_Amarillo(self):

        efecto = "amarillo"
        r, v, a = 202, 202, -1
        colores = (r, v, a)
        Acctions_App.ajustar_efecto_video(self, efecto, colores)

    def ajustar_efecto_video(self, efecto, colores):
        global file_path_end, file_path_open
        print("\n============================================")
        print("➜ Innicio de: Efecto En Color de Video...")
        print("============================================")

        if file_path_open == "":

            e = str('Cancelaste la Busqueda de Medios (MP4),\nO no la Innciaste.')
            Message_Box.dialog_critical(self, e)
            Acctions_App.concluidas_las_tareas(self)

        else:

            Play_All_Videos.playVideo(self)

            if self.player.state() == QMediaPlayer.PlayingState:
                Play_All_Videos.playVideo(self)

                QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

                file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ##(self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

                if file_path == [] or file_path == "":
                        
                    QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                    Acctions_App.concluidas_las_tareas(self)

                else:

                    file_path_end = file_path
                    Message_Box.Ms_Info_star(self)

                    try:

                        self.progress_bar.setValue(0)
                        self.thread_8 = MergeThread8(self.player, file_path_end, efecto, colores, index=8)
                        self.thread_8.innicio_8.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                        self.thread_8.any_signal_8.connect(lambda counter: Acctions_App.my_function(self, counter))
                        self.thread_8.video_merged_8.connect(lambda: Play_All_Videos.display_video(self, file_path_end))
                        self.thread_8.any_error_8.connect(lambda error: Acctions_App.my_function_error(self, error))
                        self.thread_8.concluyo_8.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                        self.thread_8.start()

                    except Exception as e:
                        print(e)

                        Message_Box.dialog_critical(self, str(f'{e}'))
                        Acctions_App.concluidas_las_tareas(self)

                    finally:
                        Acctions_App.concluidas_las_tareas(self)

            elif self.player.state() == 2:

                QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

                file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ##(self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

                if file_path == [] or file_path == "":
                        
                    QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                    Acctions_App.concluidas_las_tareas(self)

                else:

                    file_path_end = file_path
                    Message_Box.Ms_Info_star(self)

                    try:

                        self.progress_bar.setValue(0)
                        self.thread_8 = MergeThread8(self.player, file_path_end, efecto, colores, index=8)
                        self.thread_8.innicio_8.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                        self.thread_8.any_signal_8.connect(lambda counter: Acctions_App.my_function(self, counter))
                        self.thread_8.video_merged_8.connect(lambda: Play_All_Videos.display_video(self, file_path_end))
                        self.thread_8.any_error_8.connect(lambda error: Acctions_App.my_function_error(self, error))
                        self.thread_8.concluyo_8.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                        self.thread_8.start()

                    except Exception as e:
                        print(e)

                        Message_Box.dialog_critical(self, str(f'{e}'))
                        Acctions_App.concluidas_las_tareas(self)

                    finally:
                        Acctions_App.concluidas_las_tareas(self)

    ## Marca de Agua Arriba Izquierda
    def agregar_marca_de_agua_Arr_Iz(self):

        # pos = {'center': ['center', 'center'],
        #        'left': ['left', 'center'],
        #        'right': ['right', 'center'],
        #        'top': ['center', 'top'],
        #        'bottom': ['center', 'bottom']}[pos]

        poss1="left"
        poss2="top"
        Acctions_App.agregar_marca_de_agua(self, poss1=poss1, poss2=poss2)

    ## Marca de Agua Arriba Centrada
    def marca_de_agua_Arr_Centrada(self):

        poss1="center"
        poss2="top"
        Acctions_App.agregar_marca_de_agua(self, poss1=poss1, poss2=poss2)

    ## Marca de Agua Arriba Derecha
    def agregar_marca_de_agua_Arr_De(self):

        poss1="right"
        poss2="top"
        Acctions_App.agregar_marca_de_agua(self, poss1=poss1, poss2=poss2)

    ## Marca de Agua Centrada Izquierda
    def agregar_marca_de_agua_Cent_Iz(self):

        poss1="left"
        poss2="center"
        Acctions_App.agregar_marca_de_agua(self, poss1=poss1, poss2=poss2)

    ## Marca de Agua Centrada Centrada
    def agregar_marca_de_agua_Cent_Centrada(self):

        poss1="center"
        poss2="center"
        Acctions_App.agregar_marca_de_agua(self, poss1=poss1, poss2=poss2)

    ## Marca de Agua Centrada Derecha
    def agregar_marca_de_agua_Cent_De(self):

        poss1="right"
        poss2="center"
        Acctions_App.agregar_marca_de_agua(self, poss1=poss1, poss2=poss2)

    ## Marca de Agua Abajo Izquierda
    def agregar_marca_de_agua_Aba_Iz(self):

        poss1="left"
        poss2="bottom"
        Acctions_App.agregar_marca_de_agua(self, poss1=poss1, poss2=poss2)

    ## Marca de Agua Abajo Centrada
    def agregar_marca_de_agua_Aba_Centrada(self):

        poss1="center"
        poss2="bottom"
        Acctions_App.agregar_marca_de_agua(self, poss1=poss1, poss2=poss2)

    ## Marca de Agua Abajo Derecha
    def agregar_marca_de_agua_Aba_De(self):

        poss1="right"
        poss2="bottom"
        Acctions_App.agregar_marca_de_agua(self, poss1=poss1, poss2=poss2)

    def agregar_marca_de_agua(self, poss1="", poss2=""):
        global file_path_end, file_path_open, file_path_open_image
        print("\n============================================")
        print("➜ Innicio de: Agregando Marca de Agua...")
        print("============================================")

        if file_path_open == "":

            e = str('Cancelaste la Busqueda de Medios (MP4),\nO no la Innciaste.')
            Message_Box.dialog_critical(self, e)
            Acctions_App.concluidas_las_tareas(self)

        else:

            Play_All_Videos.playVideo(self)

            poss1 = str(poss1)
            poss2 = str(poss2)

            if self.player.state() == QMediaPlayer.PlayingState:
                Play_All_Videos.playVideo(self)
                QMessageBox.information(self, 'Aviso', 'Fabor de Agregar una Imagen, para la Marca de Agua.\
\nMuchas Gracias...')

                file_path_open_image = Open_All_Files.openFile_image(self)
                file_path_open_image = file_path_open_image

                file_path_open_image = Path.resource_path(file_path_open_image)

                QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

                file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ##(self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

                if file_path == [] or file_path == "":
                        
                    QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                    Acctions_App.concluidas_las_tareas(self)

                else:

                    file_path_end = file_path
                    Message_Box.Ms_Info_star(self)

                    try:

                        self.progress_bar.setValue(0)
                        self.thread_9 = MergeThread9(self.player, file_path_end, file_path_open_image, poss1=poss1, poss2=poss2, index=9)
                        self.thread_9.innicio_9.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                        self.thread_9.any_signal_9.connect(lambda counter: Acctions_App.my_function(self, counter))
                        self.thread_9.video_merged_9.connect(lambda: Play_All_Videos.display_video(self, file_path_end))
                        self.thread_9.any_error_9.connect(lambda error: Acctions_App.my_function_error(self, error))
                        self.thread_9.concluyo_9.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                        self.thread_9.start()

                    except Exception as e:
                        print(e)

                        Message_Box.dialog_critical(self, str(f'{e}'))
                        Acctions_App.concluidas_las_tareas(self)

                    finally:
                        Acctions_App.concluidas_las_tareas(self)

            elif self.player.state() == 2:
                QMessageBox.information(self, 'Aviso', 'Fabor de Agregar una Imagen, para la Marca de Agua.\
\nMuchas Gracias...')

                file_path_open_image = Open_All_Files.openFile_image(self)
                file_path_open_image = file_path_open_image

                file_path_open_image = Path.resource_path(file_path_open_image)

                QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

                file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ##(self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

                if file_path == [] or file_path == "":
                        
                    QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                    Acctions_App.concluidas_las_tareas(self)

                else:

                    file_path_end = file_path
                    Message_Box.Ms_Info_star(self)

                    try:

                        self.progress_bar.setValue(0)
                        self.thread_9 = MergeThread9(self.player, file_path_end, file_path_open_image, poss1=poss1, poss2=poss2, index=9)
                        self.thread_9.innicio_9.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                        self.thread_9.any_signal_9.connect(lambda counter: Acctions_App.my_function(self, counter))
                        self.thread_9.video_merged_9.connect(lambda: Play_All_Videos.display_video(self, file_path_end))
                        self.thread_9.any_error_9.connect(lambda error: Acctions_App.my_function_error(self, error))
                        self.thread_9.concluyo_9.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                        self.thread_9.start()

                    except Exception as e:
                        print(e)

                        Message_Box.dialog_critical(self, str(f'{e}'))
                        Acctions_App.concluidas_las_tareas(self)

                    finally:
                        Acctions_App.concluidas_las_tareas(self)

    ## Converted To MP3||WAV
    def Conver_To_MP3_WAP(self):
        global file_path_open, output_format
        print("\n============================================")
        print("➜ Innicio: Converted To MP3||WAV...")
        print("============================================")

        if file_path_open == "":

            e = str('Cancelaste la Busqueda de Medios (MP4),\nO no la Innciaste.')
            Message_Box.dialog_critical(self, e)
            Acctions_App.concluidas_las_tareas(self)

        else:

            try:

                if self.player.state() == QMediaPlayer.PlayingState:
                    Play_All_Videos.playVideo(self)

                QMessageBox.information(self, 'Info', 'Procede a Buscar una Ubicación donde Alojar los Archivos MP3...\nMuchas Gracias.')

                self.output_name = QFileDialog.getSaveFileName(self, "Guardar Video Convertido", filter="MP3: (*.mp3) ;; WAV: (*.wav) ")[0]
                # dialog = QFileDialog()
                # self.output_name = dialog.getExistingDirectory(self, 'Slecciona el Dir. de Salida')

                output_name = self.output_name

                if self.output_name == "":

                    e = str('Cancelaste la Ubicación de Salida para el Archivo (MP3) o (WAV).')
                    Message_Box.dialog_critical(self, e)
                    Acctions_App.concluidas_las_tareas(self)
                    pass

                else:

                    Message_Box.Ms_Info_star(self)
                    QMessageBox.information(self, 'Info', 'Comensare a Trabajar\nFabor Dar Tiempo\nMuchas Gracias...')

                    try:

                        self.progress_bar.setValue(0)
                        self.thread_10 = MergeThread10(self.player, file_path_open, output_name, index=10)
                        self.thread_10.innicio_10.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                        self.thread_10.any_signal_10.connect(lambda counter: Acctions_App.my_function(self, counter))
                        self.thread_10.video_merged_10.connect(lambda: Play_All_Videos.display_video(self, output_name))
                        self.thread_10.any_error_10.connect(lambda error: Acctions_App.my_function_error(self, error))
                        self.thread_10.concluyo_10.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                        self.thread_10.start()

                    except Exception as e:
                        print(e)

                        Message_Box.dialog_critical(self, str(f'{e}'))
                        Acctions_App.concluidas_las_tareas(self)

                    finally:
                        Acctions_App.concluidas_las_tareas(self)

            except Exception as e:
                print(e)

                Message_Box.dialog_critical(self, str(f'{e}'))
                Acctions_App.concluidas_las_tareas(self)

            finally:
                Acctions_App.concluidas_las_tareas(self)

##==================================================================================================
##==================================================================================================
    
    ## Filtro de Corrección de Color
    def color_filter(self):
        global file_path_end, file_path_open
        print("\n============================================")
        print("➜ Innicio de: Filtro de Corrección de Color...")
        print("============================================")

        if file_path_open == "":

            e = str('Cancelaste la Busqueda de Medios (MP4),\nO no la Innciaste.')
            Message_Box.dialog_critical(self, e)
            Acctions_App.concluidas_las_tareas(self)

        else:

            Play_All_Videos.playVideo(self)

            if self.player.state() == QMediaPlayer.PlayingState:
                Play_All_Videos.playVideo(self)

                QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

                file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ##(self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

                if file_path == [] or file_path == "":
                        
                    QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                    Acctions_App.concluidas_las_tareas(self)

                else:

                    output_path = file_path
                    video_path = file_path_open
                    Message_Box.Ms_Info_star(self)

                    try:

                        self.progress_bar.setValue(0)
                        self.thread_11 = MergeThread11(self.player, video_path, output_path, index=11)
                        self.thread_11.innicio_11.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                        self.thread_11.any_signal_11.connect(lambda counter: Acctions_App.my_function(self, counter))
                        self.thread_11.video_merged_11.connect(lambda: Play_All_Videos.display_video(self, output_path))
                        self.thread_11.any_error_11.connect(lambda error: Acctions_App.my_function_error(self, error))
                        self.thread_11.concluyo_11.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                        self.thread_11.start()

                    except Exception as e:
                        print(e)

                        Message_Box.dialog_critical(self, str(f'{e}'))
                        Acctions_App.concluidas_las_tareas(self)

                    finally:
                        Acctions_App.concluidas_las_tareas(self)

            elif self.player.state() == 2:

                QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

                file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ##(self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

                if file_path == [] or file_path == "":
                        
                    QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                    Acctions_App.concluidas_las_tareas(self)

                else:

                    output_path = file_path
                    video_path = file_path_open
                    Message_Box.Ms_Info_star(self)

                    try:

                        self.progress_bar.setValue(0)
                        self.thread_11 = MergeThread11(self.player, video_path, output_path, index=11)
                        self.thread_11.innicio_11.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                        self.thread_11.any_signal_11.connect(lambda counter: Acctions_App.my_function(self, counter))
                        self.thread_11.video_merged_11.connect(lambda: Play_All_Videos.display_video(self, output_path))
                        self.thread_11.any_error_11.connect(lambda error: Acctions_App.my_function_error(self, error))
                        self.thread_11.concluyo_11.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                        self.thread_11.start()

                    except Exception as e:
                        print(e)

                        Message_Box.dialog_critical(self, str(f'{e}'))
                        Acctions_App.concluidas_las_tareas(self)

                    finally:
                        Acctions_App.concluidas_las_tareas(self)
                
##==================================================================================================
##==================================================================================================

# Resoluciones Para Video:

# Alta:
# 4320p (8K): 7680x4320
# 2160p (4K): 3840x2161
# 1440p (2K): 2560x1440

# Media Alta  .-. Recomendado -.-
# 1080p (HD): 1920x1080  .-. Recomendado -.-

# Media:
# 720p (HD): 1280x720

# Baja:
# 480p (SD): 854x480
# 360p (SD): 640x360
# 240p (SD): 426x240
    
    ## Resolucione: 4320p (8K): 7680x4320
    def resize_resolutin_4320p(self):

        # 4320p (8K): 7680x4320
        size1 = int(7680)
        size2 = int(4320)
        new_size = (size1, size2)

        Acctions_App.resize_video_resolotion(self, new_size)

    ## Resolucione: 2160p (4K): 3840x2161
    def resize_resolutin_2160p(self):

        # 2160p (4K): 3840x2161
        size1 = int(3840)
        size2 = int(2161)
        new_size = (size1, size2)

        Acctions_App.resize_video_resolotion(self, new_size)

    ## Resolucione: 1440p (2K): 2560x1440
    def resize_resolutin_1440p(self):

        # 1440p (2K): 2560x1440
        size1 = int(2560)
        size2 = int(1440)
        new_size = (size1, size2)

        Acctions_App.resize_video_resolotion(self, new_size)
##===============================================
##===============================================
    ## Resolucione: 1080p (HD): 1920x1080
    def resize_resolutin_1080p(self):

        # 1080p (HD): 1920x1080  .-. Recomendado -.-
        size1 = int(1920)
        size2 = int(1080)
        new_size = (size1, size2)

        Acctions_App.resize_video_resolotion(self, new_size)
##===============================================
##===============================================
    ## Resolucione: 720p (HD): 1280x720
    def resize_resolutin_720p(self):

        # 720p (HD): 1280x720
        size1 = int(1280)
        size2 = int(720)
        new_size = (size1, size2)

        Acctions_App.resize_video_resolotion(self, new_size)
##===============================================
##===============================================
    ## Resolucione: 480p (SD): 854x480
    def resize_resolutin_480p(self):

        # 480p (SD): 854x480
        size1 = int(854)
        size2 = int(480)
        new_size = (size1, size2)

        Acctions_App.resize_video_resolotion(self, new_size)

    ## Resolucione: 360p (SD): 640x360
    def resize_resolutin_360p(self):

        # 360p (SD): 640x360
        size1 = int(640)
        size2 = int(360)
        new_size = (size1, size2)

        Acctions_App.resize_video_resolotion(self, new_size)

    ## Resolucione: 240p (SD): 426x240
    def resize_resolutin_240p(self):

        # 240p (SD): 426x240
        size1 = int(426)
        size2 = int(240)
        new_size = (size1, size2)

        Acctions_App.resize_video_resolotion(self, new_size)

##===============================================
##===============================================

    def resize_video_resolotion(self, new_size):
        global file_path_end, file_path_open
        print("\n============================================")
        print("➜ Innicio de: Resoluciones Para Video...")
        print("============================================")

        if file_path_open == "":

            e = str('Cancelaste la Busqueda de Medios (MP4),\nO no la Innciaste.')
            Message_Box.dialog_critical(self, e)
            Acctions_App.concluidas_las_tareas(self)

        else:

            Play_All_Videos.playVideo(self)

            if self.player.state() == QMediaPlayer.PlayingState:
                Play_All_Videos.playVideo(self)

                QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

                file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ##(self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

                if file_path == [] or file_path == "":
                        
                    QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')

                else:

                    output_path = file_path
                    video_path = file_path_open
                    Message_Box.Ms_Info_star(self)

                    try:

                        self.progress_bar.setValue(0)
                        self.thread_12 = MergeThread12(self.player, video_path, output_path, new_size, index=12)
                        self.thread_12.innicio_12.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                        self.thread_12.any_signal_12.connect(lambda counter: Acctions_App.my_function(self, counter))
                        self.thread_12.video_merged_12.connect(lambda: Play_All_Videos.display_video(self, output_path))
                        self.thread_12.any_error_12.connect(lambda error: Acctions_App.my_function_error(self, error))
                        self.thread_12.concluyo_12.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                        self.thread_12.start()

                    except Exception as e:
                        print(e)

                        Message_Box.dialog_critical(self, str(f'{e}'))
                        Acctions_App.concluidas_las_tareas(self)

                    finally:
                        Acctions_App.concluidas_las_tareas(self)

            elif self.player.state() == 2:

                QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

                file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ##(self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

                if file_path == [] or file_path == "":
                        
                    QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                    Acctions_App.concluidas_las_tareas(self)

                else:

                    output_path = file_path
                    video_path = file_path_open
                    Message_Box.Ms_Info_star(self)

                    try:

                        self.progress_bar.setValue(0)
                        self.thread_12 = MergeThread12(self.player, video_path, output_path, new_size, index=12)
                        self.thread_12.innicio_12.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                        self.thread_12.any_signal_12.connect(lambda counter: Acctions_App.my_function(self, counter))
                        self.thread_12.video_merged_12.connect(lambda: Play_All_Videos.display_video(self, output_path))
                        self.thread_12.any_error_12.connect(lambda error: Acctions_App.my_function_error(self, error))
                        self.thread_12.concluyo_12.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                        self.thread_12.start()

                    except Exception as e:
                        print(e)

                        Message_Box.dialog_critical(self, str(f'{e}'))
                        Acctions_App.concluidas_las_tareas(self)

                    finally:
                        Acctions_App.concluidas_las_tareas(self)
                
##==================================================================================================
##==================================================================================================
    
    ## Rotar Video (-) 90g
    def rotate_vid_90(self):

        rotate_v = int(90)
        Acctions_App.rotate_vid_file(self, rotate_v)

    ## Rotar Video (-) 180g
    def rotate_vid_180(self):

        rotate_v = int(180)
        Acctions_App.rotate_vid_file(self, rotate_v)

    ## Rotar Video (+) 90g
    def rotate_vid_270(self):

        rotate_v = int(270)
        Acctions_App.rotate_vid_file(self, rotate_v)

##===============================================
##===============================================

    def rotate_vid_file(self, rotate_v):
        global file_path_end, file_path_open
        print("\n============================================")
        print("➜ Innicio de: Menú Ratación de Video...")
        print("============================================")

        if file_path_open == "":

            e = str('Cancelaste la Busqueda de Medios (MP4),\nO no la Innciaste.')
            Message_Box.dialog_critical(self, e)
            Acctions_App.concluidas_las_tareas(self)

        else:

            Play_All_Videos.playVideo(self)

            if self.player.state() == QMediaPlayer.PlayingState:
                Play_All_Videos.playVideo(self)

                QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

                file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ##(self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

                if file_path == [] or file_path == "":
                        
                    QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                    Acctions_App.concluidas_las_tareas(self)

                else:

                    output_path = file_path
                    video_path = file_path_open
                    Message_Box.Ms_Info_star(self)

                    try:

                        self.progress_bar.setValue(0)
                        self.thread_13 = MergeThread13(self.player, video_path, output_path, rotate_v, index=13)
                        self.thread_13.innicio_13.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                        self.thread_13.any_signal_13.connect(lambda counter: Acctions_App.my_function(self, counter))
                        self.thread_13.video_merged_13.connect(lambda: Play_All_Videos.display_video(self, output_path))
                        self.thread_13.any_error_13.connect(lambda error: Acctions_App.my_function_error(self, error))
                        self.thread_13.concluyo_13.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                        self.thread_13.start()

                    except Exception as e:
                        print(e)

                        Message_Box.dialog_critical(self, str(f'{e}'))
                        Acctions_App.concluidas_las_tareas(self)

                    finally:
                        Acctions_App.concluidas_las_tareas(self)

            elif self.player.state() == 2:

                QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')

                file_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ##(self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

                if file_path == [] or file_path == "":
                        
                    QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                    Acctions_App.concluidas_las_tareas(self)

                else:

                    output_path = file_path
                    video_path = file_path_open
                    Message_Box.Ms_Info_star(self)

                    try:

                        self.progress_bar.setValue(0)
                        self.thread_13 = MergeThread13(self.player, video_path, output_path, rotate_v, index=13)
                        self.thread_13.innicio_13.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                        self.thread_13.any_signal_13.connect(lambda counter: Acctions_App.my_function(self, counter))
                        self.thread_13.video_merged_13.connect(lambda: Play_All_Videos.display_video(self, output_path))
                        self.thread_13.any_error_13.connect(lambda error: Acctions_App.my_function_error(self, error))
                        self.thread_13.concluyo_13.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                        self.thread_13.start()

                    except Exception as e:
                        print(e)

                        Message_Box.dialog_critical(self, str(f'{e}'))
                        Acctions_App.concluidas_las_tareas(self)

                    finally:
                        Acctions_App.concluidas_las_tareas(self)
                
##==================================================================================================
##==================================================================================================
    
    ## Crear Video de Imagenes
    def Create_Video_From_IMGs(self):
        global accion, file_path_open, working, file_path_video
        print("\n============================================")
        print("➜ Innicio para: Crear Video de Imagenes...")
        print("============================================")

        working = ""
        file_path_open = ""
        file_path_video = str("Generando Video...")
        title_video.Actualizando_Title(self, file_path_video)

        Message_Box.Ms_Info_star(self)

        QMessageBox.information(self, 'Aviso', 'Fabor de Elegir Que Imagenes se Utilizaran Para, Crear el Video')
        archivo, _ = QFileDialog.getOpenFileNames(self, "Open file", "", "Image files: ((*.png ; *.jpg ; *.jpeg))")

        if archivo:

            QMessageBox.information(self, 'Aviso', 'Elegir un Directorio para Poder Almacenar las Imagenes Temporalmente.')
            dialog = QFileDialog()
            images_temp = dialog.getExistingDirectory(self, 'Slecciona el Dir. Imagenes Temporales')

            if images_temp == "":

                e = str('Cancelaste la Ubicación de Salida para Poder Almacenar las Imagenes Temporalmente...')
                Message_Box.dialog_critical(self, e)
                Acctions_App.concluidas_las_tareas(self)
                pass

            else:

                QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.')
                output_path = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;MP4V(*.mp4v);;AVI(*.avi);;WMV(*.wmv)")[0]

                if output_path == [] or output_path == "":
                    QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')
                    Acctions_App.concluidas_las_tareas(self)

                else:

                    file_path_open = output_path

                    try:

                        self.progress_bar.setValue(0)
                        self.thread_14 = MergeThread14(self.player, archivo, images_temp, output_path, index=14)
                        self.thread_14.innicio_14.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                        self.thread_14.any_signal_14.connect(lambda counter: Acctions_App.my_function(self, counter))
                        self.thread_14.video_merged_14.connect(lambda: Play_All_Videos.display_video(self, output_path))
                        self.thread_14.any_error_14.connect(lambda error: Acctions_App.my_function_error(self, error))
                        self.thread_14.concluyo_14.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                        self.thread_14.start()

                    except Exception as e:
                        print(e)

                        Message_Box.dialog_critical(self, str(f'{e}'))
                        Acctions_App.concluidas_las_tareas(self)

                    finally:
                        Acctions_App.concluidas_las_tareas(self)

##==================================================================================================
##==================================================================================================
    
    ## Controla el Tiempo en la Barra de Progreso al Innicio y al Final el los MergeThread´s
    def my_function(self, counter):
        
        cnt = counter
        index = self.sender().index
        
        if index == 1:
            self.progress_bar.setValue(cnt)

        elif index == 2:
            self.progress_bar.setValue(cnt)

        elif index == 3:
            self.progress_bar.setValue(cnt)

        elif index == 5:
            self.progress_bar.setValue(cnt)

        elif index == 6:
            self.progress_bar.setValue(cnt)

        elif index == 7:
            self.progress_bar.setValue(cnt)

        elif index == 8:
            self.progress_bar.setValue(cnt)

        elif index == 9:
            self.progress_bar.setValue(cnt)

        elif index == 10:
            self.progress_bar.setValue(cnt)

        elif index == 11:
            self.progress_bar.setValue(cnt)

        elif index == 12:
            self.progress_bar.setValue(cnt)

        elif index == 13:
            self.progress_bar.setValue(cnt)

        elif index == 14:
            self.progress_bar.setValue(cnt)

        elif index == 15:
            self.progress_bar.setValue(cnt)

        elif index == 16:
            self.progress_bar.setValue(cnt)

    ## Controla el Flujo de los Errores el los MergeThread´s
    def my_function_error(self, e):

        Message_Box.dialog_critical(self, str(f'{e}'))
        Acctions_App.concluidas_las_tareas(self)

    def my_function_innicio(self, msn):
        QMessageBox.information(self, 'Aviso:', str(f'{msn}'))

    def my_function_concluyo(self, msn):
        QMessageBox.information(self, 'Aviso:', str(f'{msn}'))

##=========================================================================================================
##=========================================================================================================

## Controla la Reproducción, en los Videos, al Innico y al Final en los MergeThread´s
class Play_All_Videos(VideoPlayer):

    def __init__(self):
        super().__init__()

    def position_changed(self, position):
        
        duration = self.player.duration()
        if duration > 0:
            self.slider.setMaximum(duration)
            self.slider.setValue(self.player.position())

        Play_All_Videos.Decrese_Time_Vid(self, position)

    def playVideo(self):
        global file_path_open
        print("\n============================================")
        print("➜ Innico de: Reproducción, en los Videos...")
        print("============================================")

        if file_path_open == "":

            e = str('Cancelaste la Busqueda de Medios (MP4),\nO no la Innciaste.')
            Message_Box.dialog_critical(self, e)
            Acctions_App.concluidas_las_tareas(self)

        else:

            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.pause()
                self.play_button.setText('Play')
                Play_All_Videos.Play_Time_Vid(self)

            else:

                self.player.play()
                self.play_button.setText('Pause')
                Play_All_Videos.Play_Time_Vid(self)

    def setSliderPosition(self, position):

        self.player.setPosition(position)

    def updateSlider(self):

        Play_All_Videos.Play_Time_Vid(self)

    def Play_Time_Vid(self):

        try:
            
            next_frame_time = QtMultimedia.QMediaPlayer.duration(self.player)

            t = next_frame_time * 1e-3 # to seconds
            if t > 0:
                self.converted_current_time_1 = time.strftime('  %H:%M:%S  ', time.gmtime(int(t)))
                self.time_vid.setText(self.converted_current_time_1+'| Vol ')

        except Exception as e:
            print(e)

            Message_Box.dialog_critical(self, str(f'{e}'))
            Acctions_App.concluidas_las_tareas(self)

    def Decrese_Time_Vid(self, position):

        try:
                
            d = position
            t = d * 1e-3 # to seconds

            if t > 0:
                self.converted_current_time_3 = time.strftime('  %H:%M:%S  ', time.gmtime(int(t)))
                self.time_vid_2.setText(self.converted_current_time_3)

                if self.converted_current_time_3 == self.converted_current_time_1:

                    self.time_vid.setText('  00:00:00  Vol.')
                    self.time_vid_2.setText(' Sts.')

                else:
                    pass

        except Exception as e:
            print(e)

            Message_Box.dialog_critical(self, str(f'{e}'))
            Acctions_App.concluidas_las_tareas(self)

    def display_video(self, file_path):
        global file_path_video

        self.playlist.clear()
        file_path_video = file_path

        try:

            # Control de reproducción de video de Qt.
            self.palylist = QMediaPlaylist()
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(file_path)))

            self.player.setPlaylist(self.playlist)
            self.player.playlist().setCurrentIndex(0)

            title_video.Actualizando_Title(self, file_path)

            self.player.play()

        except Exception as e:
            print(e)

            Message_Box.dialog_critical(self, str(f'{e}'))
            Acctions_App.concluidas_las_tareas(self)

##=========================================================================================================
##=========================================================================================================

## Controla la Busqueda de los Medios a Ser Tratados en los MergeThread´s
class Open_All_Files(VideoPlayer):

    def __init__(self):
        super().__init__()

    def openFile(self):
        global file_path_open, working
        print("\n============================================")
        print('Innicio de: Busqueda de los Medios a Ser Tratados...')
        print("============================================")

        working = ""
        file_path_open = "-"
        title_video.Actualizando_Title(self, file_path_open)

        file_path, _ = QFileDialog.getOpenFileName(self, "Open file Video", "", "Video files: *.mp4 ; *.avi ; *.mp3 ; *.wav ; *.mkv ; *.wmv ; *.webm")
        if file_path:

            file_path_open = file_path
            title_video.Actualizando_Title(self, file_path)
            Play_All_Videos.display_video(self, file_path)

        else:

            file_path_video = ""
            QMessageBox.information(self, 'Aviso', 'Cancelaste, la Busqueda...')

    def openFile_audio(self):
        global file_path_open_audio

        file_path, _ = QFileDialog.getOpenFileName(self, "Open file Audio (MP3)", "", "Video files MP3: *.mp3")
        if file_path:

            file_path_open_audio = file_path
            return file_path_open_audio

    def openFile_image(self):
        global file_path_open_image

        file_path, _ = QFileDialog.getOpenFileName(self, "Open file Image", "", "Image: *.png ;; JPG(*.jpg) ;; JPEG(*.jpeg)")
        if file_path:

            image = cv2.imread(file_path)
            imagen1 = imutils.resize(image, height=80)
            file_path_open_image = tempfile.mktemp(".png")
            cv2.imwrite(file_path_open_image, imagen1)

            return file_path_open_image

##=========================================================================================================
##=========================================================================================================

## Controla donde se Alojaran los Videos despues de Ser tratados en los MergeThread´s
class Save_All_Videos(VideoPlayer):

    def __init__(self):
        super().__init__()

    def saveVideo(self):
        global file_path_end, trimmed_clip, clip

        trimmed_clip.write_videofile(file_path_end, codec="libx264")

    def saveVideo2(self):
        global file_path_end, file_path_open

        # Carga el video
        video_clip = VideoFileClip(file_path_open)
        
        # Elimina el audio del video
        video_clip = video_clip.without_audio()
        
        # Guarda el video sin audio
        video_clip.write_videofile(file_path_end, codec="libx264", audio_codec="aac")

    def saveVideo3(self):
        global file_path_open, file_path_open_audio, file_path_end

        if file_path_open == "":

            e = str('Cancelaste la Busqueda de Medios (MP4),\nO no la Innciaste.')
            Message_Box.dialog_critical(self, e)
            Acctions_App.concluidas_las_tareas(self)

        else:

            # Carga el video
            video_clip = VideoFileClip(file_path_open)

            # Carga el audio
            audio_clip = AudioFileClip(file_path_open_audio)

            # Si el video no tiene audio, agrega el audio al principio
            if not video_clip.audio:

                video_clip = video_clip.set_audio(audio_clip)

            else:

                # Si el video ya tiene audio, concatena el video con el audio
                video_clip = concatenate_videoclips([video_clip.set_audio(None), audio_clip.set_duration(video_clip.duration)])

            # Guarda el video con el audio agregado
            video_clip.write_videofile(file_path_end, codec="libx264", audio_codec="aac")

    def saveVideo4(self, video_path, output_path, brillo=0, contraste=0, saturacion=0):

        video_clip = VideoFileClip(video_path)
        col = (int(brillo), int(contraste), int(saturacion))
        video_clip = vfx.colorx(video_clip, col)
        video_clip.write_videofile(output_path)

    def saveVideo5(self, efecto, colores):
        global file_path_open, file_path_end

        if file_path_open == "":

            e = str('Cancelaste la Busqueda de Medios (MP4),\nO no la Innciaste.')
            Message_Box.dialog_critical(self, e)
            Acctions_App.concluidas_las_tareas(self)

        else:

            video_clip = VideoFileClip(file_path_open)

            if efecto == "blanco_negro":

                video_clip = vfx.blackwhite(video_clip)

            elif efecto == "sepia":

                r = colores[0]
                v = colores[1]
                a = colores[2]

                colores = (int(r), int(v), int(a))
                video_clip = vfx.colorx(video_clip, colores)

            elif efecto == "azul":

                r = colores[0]
                v = colores[1]
                a = colores[2]

                colores = (int(r), int(v), int(a))
                video_clip = vfx.colorx(video_clip, colores)

            elif efecto == "rojo":

                r = colores[0]
                v = colores[1]
                a = colores[2]

                colores = (int(r), int(v), int(a))
                video_clip = vfx.colorx(video_clip, colores)

            elif efecto == "verde":

                r = colores[0]
                v = colores[1]
                a = colores[2]

                colores = (int(r), int(v), int(a))
                video_clip = vfx.colorx(video_clip, colores)

            elif efecto == "amarillo":

                r = colores[0]
                v = colores[1]
                a = colores[2]

                colores = (int(r), int(v), int(a))
                video_clip = vfx.colorx(video_clip, colores)

            # Agrega más opciones de efectos según lo necesites
            video_clip.write_videofile(file_path_end)

    def set_logo_size(videoclip: VideoFileClip, size: Tuple[int, int] = None, factor_width=None, factor_height=None):
        if factor_width:
            return {'width': int(videoclip.size[0] * factor_width)}

        if factor_height:
            return {'height': int(videoclip.size[1] * factor_height)}

        raise ValueError("Use percent_width or percent height or a size tuple pair")

    def saveVideo6(self, video_path, output_path, marca_de_agua_path, poss1='right', poss2='bottom'):

        position = (f'{poss1}', f'{poss2}')

        video_clip = VideoFileClip(video_path)
        marca_de_agua = ImageClip(marca_de_agua_path).resize(**Save_All_Videos.set_logo_size(video_clip, factor_width=0.1)).set_pos(position).set_duration(video_clip.duration)
        video_con_marca_de_agua = CompositeVideoClip([video_clip, marca_de_agua], size=video_clip.size)
        video_con_marca_de_agua.write_videofile(output_path)

##=========================================================================================================
##=========================================================================================================

    def convert(self, mp4_name, output_name):

        try:

            path_1 = Path.resource_path(mp4_name)
            path_2 = Path.resource_path(output_name)

            videoclip = VideoFileClip(path_1)
            audioclip = videoclip.audio
            audioclip.write_audiofile(path_2)
            audioclip.close()
            videoclip.close()

        except Exception as e:
            print(e)

            Message_Box.dialog_critical(self, str(f'{e}'))
            Acctions_App.concluidas_las_tareas(self)

    def saveVideo7(self, file_path_open, output_name):

        if file_path_open == "":

            e = str('Cancelaste la Busqueda de Medios (MP4),\nO no la Innciaste.')
            Message_Box.dialog_critical(self, e)
            Acctions_App.concluidas_las_tareas(self)

        else:

            Save_All_Videos.convert(self, file_path_open, output_name)

    def saveVideo8(self, video_path, output_path):

        if video_path == "":

            e = str('Cancelaste la Busqueda de Medios (MP4),\nO no la Innciaste.')
            Message_Box.dialog_critical(self, e)
            Acctions_App.concluidas_las_tareas(self)

        else:

            video = VideoFileClip(video_path)
            filtered_video = video.fx(vfx.colorx, 1.5)
            filtered_video.write_videofile(output_path)
            #wb.open_new(output_path)

    def saveVideo9(self, video_path, output_path, new_size):
        global file_path_open

        if video_path == "":

            e = str('Cancelaste la Busqueda de Medios (MP4),\nO no la Innciaste.')
            Message_Box.dialog_critical(self, e)
            Acctions_App.concluidas_las_tareas(self)

        else:

            clip = VideoFileClip(video_path)
            video = resize(clip, newsize=new_size)
            video.write_videofile(output_path)
            #wb.open_new(output_path)

    def saveVideo10(self, video_path, output_path, rotate_v):

        if video_path == "":

            e = str('Cancelaste la Busqueda de Medios (MP4),\nO no la Innciaste.')
            Message_Box.dialog_critical(self, e)
            Acctions_App.concluidas_las_tareas(self)

        else:

            video = VideoFileClip(video_path)
            video_r = vfx.rotate(clip = video, angle = rotate_v)
            video_r.write_videofile(output_path)
            #wb.open_new(output_path)  , new_size

##=========================================================================================================
##=========================================================================================================

## Controla la Actualización, de el Titulo en los Videos, antes y Despues de Ser Tratados en los MergeThread´s
class title_video(VideoPlayer):

## Metodo para Acortar el Titulo si este fuera muy Largo (Alternativo)
    def acortando_title(self, text, length=60):

        name, ext = os.path.splitext(text)

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ....{ext}"

## Metodo para Colocar en el Titulo Lo Que Deseemos que Hira, en este Caso el Titulo del Video
    def Actualizando_Title(self, file_path=None):
        global working, accion

        if file_path == "":
            pass

        else:

            fpath, fname = os.path.split(file_path)

            txt_title4 = title_video.acortando_title(self, fname)

            if working == "":
                self.setWindowTitle(f"Editor de Video -v9 || {txt_title4} || {working}")

            else:
                self.setWindowTitle(f"Editor de Video -v9 || {txt_title4} || {working}")

##=========================================================================================================
##=========================================================================================================

## Controla Todo en Segundo Plano para que la App, no se Cuelgue, todo al CPU, 2do Hilo
## (Unir Videos)
class MergeThread(QThread):

    innicio = pyqtSignal(str)
    any_signal = pyqtSignal(int)
    video_merged = pyqtSignal(str)
    any_error = pyqtSignal(str)
    concluyo = pyqtSignal(str)

    def __init__(self, player, file_names, file_path, index=0):
        super().__init__()

        self.player = player
        self.index = index
        self.file_names = file_names
        self.file_path = file_path
        self.cont = True

    def run(self):
        global final_clip

        VideoPlayer.variables_utiles(self)

        msn = "Se Innicia, con la Tarea Asignada"
        self.innicio.emit(str(f"{msn}"))

        clips = []
        for file_name in self.file_names:
            clip = VideoFileClip(file_name)
            clips.append(clip)

        cnt=0
        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal.emit(cnt)

        self.cont = True

        try:

            final_clip = concatenate_videoclips(clips)

            if self.file_path:
                final_clip.write_videofile(self.file_path)
                    
                # Liberar recursos
                for clip in clips:
                        clip.close()

                final_clip.close()

        except Exception as e:
            self.any_error.emit(str(f'{e}'))

        meta = VideoPlayer.meta_data(self, self.player)
        msn = f"Se Concluye, con la Tarea Asignada\n{meta}\nEl Video se Almaceno en:\n{self.file_path}"
        self.concluyo.emit(str(f"{msn}"))

        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal.emit(cnt)

        self.video_merged.emit(self.file_path)
    
    # Shorten text that may be too long
    def _truncate(self, text, length=25):

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ...."

##=========================================================================================================
##=========================================================================================================

## Controla Todo en Segundo Plano para que la App, no se Cuelgue, todo al CPU, 2do Hilo 
## (Recortar Inicio)
class MergeThread2(QThread):

    innicio_1 = pyqtSignal(str)
    any_signal_1 = pyqtSignal(int)
    video_merged_1 = pyqtSignal(str)
    any_error_1 = pyqtSignal(str)
    concluyo_1 = pyqtSignal(str)

    def __init__(self, file_path_end, player, index=0):
        super().__init__()

        self.player = player
        self.index = index
        self.cont = True
        self.file_path_end = file_path_end

    def run(self):
        global file_path_end

        VideoPlayer.variables_utiles(self)

        msn = "Se Innicia, con la Tarea Asignada"
        self.innicio_1.emit(str(f"{msn}"))

        cnt=0
        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_1.emit(cnt)
        
        self.cont = True

        try:

            Save_All_Videos.saveVideo(self)

        except Exception as e:
            self.any_error_1.emit(str(f'{e}'))

        meta = VideoPlayer.meta_data(self, self.player)
        msn = f"Se Concluye, con la Tarea Asignada\n{meta}\nEl Video se Almaceno en:\n{self.file_path_end}"
        self.concluyo_1.emit(str(f"{msn}"))

        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_1.emit(cnt)

        self.video_merged_1.emit(file_path_end)

    
    # Shorten text that may be too long
    def _truncate(self, text, length=25):

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ...."

##=========================================================================================================
##=========================================================================================================

## Controla Todo en Segundo Plano para que la App, no se Cuelgue, todo al CPU, 2do Hilo 
## (Recortar Final)
class MergeThread3(QThread):

    innicio_2 = pyqtSignal(str)
    any_signal_2 = pyqtSignal(int)
    video_merged_2 = pyqtSignal(str)
    any_error_2 = pyqtSignal(str)
    concluyo_2 = pyqtSignal(str)

    def __init__(self, player, file_path_end, index=0):
        super().__init__()

        self.player = player
        self.index = index
        self.cont = True
        self.file_path_end = file_path_end

    def run(self):
        global file_path_end

        VideoPlayer.variables_utiles(self)

        msn = "Se Innicia, con la Tarea Asignada"
        self.innicio_2.emit(str(f"{msn}"))

        cnt=0
        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_2.emit(cnt)
        
        self.cont = True

        try:

            Save_All_Videos.saveVideo(self)

        except Exception as e:
            self.any_error_2.emit(str(f'{e}'))

        meta = VideoPlayer.meta_data(self, self.player)
        msn = f"Se Concluye, con la Tarea Asignada\n{meta}\nEl Video se Almaceno en:\n{self.file_path_end}"
        self.concluyo_2.emit(str(f"{msn}"))

        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_2.emit(cnt)

        self.video_merged_2.emit(file_path_end)
    
    # Shorten text that may be too long
    def _truncate(self, text, length=25):

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ...."

##=========================================================================================================
##=========================================================================================================

## Controla Todo en Segundo Plano para que la App, no se Cuelgue, todo al CPU, 2do Hilo
## (Converted To MP4)
class MergeThread4(QThread):

    innicio_3 = pyqtSignal(str)
    any_signal_3 = pyqtSignal(int)
    video_merged_3 = pyqtSignal(str)
    any_error_3 = pyqtSignal(str)
    concluyo_3 = pyqtSignal(str)

    def __init__(self, player, file_path_end, ext, index=0):
        super().__init__()

        self.player = player
        self.index = index
        self.cont = True
        self.extencion = ext
        self.file_path_end = file_path_end

    def run(self):
        global file_name, output_format

        VideoPlayer.variables_utiles(self)

        msn = "Se Innicia, con la Tarea Asignada"
        self.innicio_3.emit(str(f"{msn}"))

        cnt=0
        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_3.emit(cnt)
        
        self.cont = True

        try:

            if self.extencion == 'mp4':
                subprocess.call(['ffmpeg', '-i', file_name, output_format])

            elif self.extencion == 'avi':

                video_clip = VideoFileClip(file_name)
                video_clip.write_videofile(output_format, codec='rawvideo')

            elif self.extencion == 'mov':

                video_clip = VideoFileClip(file_name)
                video_clip.write_videofile(output_format, codec='rawvideo')

            elif self.extencion == 'wmv':

                video_clip = VideoFileClip(file_name)
                video_clip.write_videofile(output_format, codec='libx264')

            elif self.extencion == 'ogv':

                video_clip = VideoFileClip(file_name)
                video_clip.write_videofile(output_format, codec='libtheora')

            elif self.extencion == 'webm':

                video_clip = VideoFileClip(file_name)
                video_clip.write_videofile(output_format, codec='libvpx')

        except Exception as e:
            self.any_error_3.emit(str(f'{e}'))

        meta = VideoPlayer.meta_data(self, self.player)
        msn = f"Se Concluye, con la Tarea Asignada\n{meta}\nEl Video se Almaceno en:\n{self.file_path_end}"
        self.concluyo_3.emit(str(f"{msn}"))

        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_3.emit(cnt)

        self.video_merged_3.emit(file_path_end)
    
    # Shorten text that may be too long
    def _truncate(self, text, length=25):

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ...."

##=========================================================================================================
##=========================================================================================================

## Controla Todo en Segundo Plano para que la App, no se Cuelgue, todo al CPU, 2do Hilo
## (Quitar Sonido)
class MergeThread5(QThread):

    innicio_5 = pyqtSignal(str)
    any_signal_5 = pyqtSignal(int)
    video_merged_5 = pyqtSignal(str)
    any_error_5 = pyqtSignal(str)
    concluyo_5 = pyqtSignal(str)

    def __init__(self, player, file_path_end, index=0):
        super().__init__()

        self.player = player
        self.index = index
        self.cont = True
        self.file_path_end = file_path_end

    def run(self):
        global file_path_end

        VideoPlayer.variables_utiles(self)

        msn = "Se Innicia, con la Tarea Asignada"
        self.innicio_5.emit(str(f"{msn}"))

        cnt=0
        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_5.emit(cnt)
        
        self.cont = True

        try:

            Save_All_Videos.saveVideo2(self)

        except Exception as e:
            self.any_error_5.emit(str(f'{e}'))

        meta = VideoPlayer.meta_data(self, self.player)
        msn = f"Se Concluye, con la Tarea Asignada\n{meta}\nEl Video se Almaceno en:\n{self.file_path_end}"
        self.concluyo_5.emit(str(f"{msn}"))

        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_5.emit(cnt)

        self.video_merged_5.emit(file_path_end)
    
    # Shorten text that may be too long
    def _truncate(self, text, length=25):

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ...."

##=========================================================================================================
##=========================================================================================================

## Controla Todo en Segundo Plano para que la App, no se Cuelgue, todo al CPU, 2do Hilo
## (Agregar Sonido)
class MergeThread6(QThread):

    innicio_6 = pyqtSignal(str)
    any_signal_6 = pyqtSignal(int)
    video_merged_6 = pyqtSignal(str)
    any_error_6 = pyqtSignal(str)
    concluyo_6 = pyqtSignal(str)

    def __init__(self, player, file_path_end, index=0):
        super().__init__()

        self.player = player
        self.index = index
        self.cont = True
        self.file_path_end = file_path_end

    def run(self):
        global file_path_open, file_path_open_audio, file_path_end

        VideoPlayer.variables_utiles(self)

        msn = "Se Innicia, con la Tarea Asignada"
        self.innicio_6.emit(str(f"{msn}"))

        cnt=0
        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_6.emit(cnt)
        
        self.cont = True

        try:

            Save_All_Videos.saveVideo3(self)

        except Exception as e:
            self.any_error_6.emit(str(f'{e}'))

        meta = VideoPlayer.meta_data(self, self.player)
        msn = f"Se Concluye, con la Tarea Asignada\n{meta}\nEl Video se Almaceno en:\n{self.file_path_end}"
        self.concluyo_6.emit(str(f"{msn}"))

        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_6.emit(cnt)

        self.video_merged_6.emit(file_path_end)
    
    # Shorten text that may be too long
    def _truncate(self, text, length=25):

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ...."

##=========================================================================================================
##=========================================================================================================

## Controla Todo en Segundo Plano para que la App, no se Cuelgue, todo al CPU, 2do Hilo
## (Ajustar Video Poco - Medio - Alto)
class MergeThread7(QThread):

    innicio_7 = pyqtSignal(str)
    any_signal_7 = pyqtSignal(int)
    video_merged_7 = pyqtSignal(str)
    any_error_7 = pyqtSignal(str)
    concluyo_7 = pyqtSignal(str)

    def __init__(self, player, file_path_end, brillo, contraste, saturacion, index=0):
        super().__init__()

        self.player = player
        self.index = index
        self.cont = True
        self.brillo, self.contraste, self.saturacion = int(brillo), int(contraste), int(saturacion)
        self.file_path_end = file_path_end

    def run(self):
        global file_path_open, file_path_end

        VideoPlayer.variables_utiles(self)

        msn = "Se Innicia, con la Tarea Asignada"
        self.innicio_7.emit(str(f"{msn}"))

        brillo, contraste, saturacion = self.brillo, self.contraste, self.saturacion

        cnt=0
        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_7.emit(cnt)
        
        self.cont = True

        try:

            Save_All_Videos.saveVideo4(self, file_path_open, file_path_end, brillo, contraste, saturacion)

        except Exception as e:
            self.any_error_7.emit(str(f'{e}'))

        meta = VideoPlayer.meta_data(self, self.player)
        msn = f"Se Concluye, con la Tarea Asignada\n{meta}\nEl Video se Almaceno en:\n{self.file_path_end}"
        self.concluyo_7.emit(str(f"{msn}"))

        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_7.emit(cnt)

        self.video_merged_7.emit(file_path_end)
    
    # Shorten text that may be too long
    def _truncate(self, text, length=25):

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ...."

##=========================================================================================================
##=========================================================================================================

## Controla Todo en Segundo Plano para que la App, no se Cuelgue, todo al CPU, 2do Hilo
## Ajustar Efecto de Color en Video [Rojo, Verde, Sepia, etc...]
class MergeThread8(QThread):

    innicio_8 = pyqtSignal(str)
    any_signal_8 = pyqtSignal(int)
    video_merged_8 = pyqtSignal(str)
    any_error_8 = pyqtSignal(str)
    concluyo_8 = pyqtSignal(str)

    def __init__(self, player, file_path_end, efecto, colores, index=8):
        super().__init__()

        self.player = player
        self.index = index
        self.cont = True

        self.efecto = efecto
        self.colores = colores
        self.file_path_end = file_path_end

    def run(self):
        global file_path_open, file_path_end

        VideoPlayer.variables_utiles(self)

        msn = "Se Innicia, con la Tarea Asignada"
        self.innicio_8.emit(str(f"{msn}"))

        efecto = self.efecto
        colores = self.colores

        cnt=0
        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_8.emit(cnt)
        
        self.cont = True

        try:

            Save_All_Videos.saveVideo5(self, efecto, colores)

        except Exception as e:
            self.any_error_8.emit(str(f'{e}'))

        meta = VideoPlayer.meta_data(self, self.player)
        msn = f"Se Concluye, con la Tarea Asignada\n{meta}\nEl Video se Almaceno en:\n{self.file_path_end}"
        self.concluyo_8.emit(str(f"{msn}"))

        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_8.emit(cnt)

        self.video_merged_8.emit(file_path_end)
    
    # Shorten text that may be too long
    def _truncate(self, text, length=25):

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ...."

##=========================================================================================================
##=========================================================================================================

## Controla Todo en Segundo Plano para que la App, no se Cuelgue, todo al CPU, 2do Hilo
## Agrega Marca de Agua, en Videos [Arriba, En Medio, Abajo, etc...]
class MergeThread9(QThread):

    innicio_9 = pyqtSignal(str)
    any_signal_9 = pyqtSignal(int)
    video_merged_9 = pyqtSignal(str)
    any_error_9 = pyqtSignal(str)
    concluyo_9 = pyqtSignal(str)

    def __init__(self, player, file_path_end, marca_de_agua_path, poss1="", poss2="", index=9):
        super().__init__()

        self.player = player
        self.index = index
        self.cont = True

        self.marca_de_agua_path = marca_de_agua_path
        self.poss1 = poss1
        self.poss2 = poss2
        self.file_path_end = file_path_end

    def run(self):
        global file_path_open, file_path_end, file_path_open_image

        VideoPlayer.variables_utiles(self)

        msn = "Se Innicia, con la Tarea Asignada"
        self.innicio_9.emit(str(f"{msn}"))

        file_path_open_image = self.marca_de_agua_path
        poss1 = self.poss1
        poss2 = self.poss2

        cnt=0
        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_9.emit(cnt)
        
        self.cont = True

        try:

            Save_All_Videos.saveVideo6(self, file_path_open, file_path_end, file_path_open_image, poss1=poss1, poss2=poss2)

        except Exception as e:
            self.any_error_9.emit(str(f'{e}'))

        meta = VideoPlayer.meta_data(self, self.player)
        msn = f"Se Concluye, con la Tarea Asignada\n{meta}\nEl Video se Almaceno en:\n{self.file_path_end}"
        self.concluyo_9.emit(str(f"{msn}"))

        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_9.emit(cnt)

        self.video_merged_9.emit(file_path_end)
    
    # Shorten text that may be too long
    def _truncate(self, text, length=25):

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ...."

##=========================================================================================================
##=========================================================================================================

## Controla Todo en Segundo Plano para que la App, no se Cuelgue, todo al CPU, 2do Hilo
## (Converted To MP3||WAV)
class MergeThread10(QThread):

    innicio_10 = pyqtSignal(str)
    any_signal_10 = pyqtSignal(int)
    video_merged_10 = pyqtSignal(str)
    any_error_10 = pyqtSignal(str)
    concluyo_10 = pyqtSignal(str)

    def __init__(self, player, file_path_open, output_name, index=10):
        super().__init__()

        self.player = player
        self.index = index
        self.cont = True

        self.file_path_open = file_path_open
        self.output_name = output_name
        self.file_path_end = file_path_end

    def run(self):

        VideoPlayer.variables_utiles(self)

        msn = "Se Innicia, con la Tarea Asignada"
        self.innicio_10.emit(str(f"{msn}"))

        file_path_open = self.file_path_open
        output_name = self.output_name

        cnt=0
        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_10.emit(cnt)
        
        self.cont = True

        try:

            Save_All_Videos.saveVideo7(self, file_path_open, output_name)

        except Exception as e:
            self.any_error_10.emit(str(f'{e}'))

        meta = VideoPlayer.meta_data(self, self.player)
        msn = f"Se Concluye, con la Tarea Asignada\n{meta}\nEl Audio [MP3] del Video se Almaceno en:\n{self.output_name}"
        self.concluyo_10.emit(str(f"{msn}"))

        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_10.emit(cnt)

        self.video_merged_10.emit(output_name)
    
    # Shorten text that may be too long
    def _truncate(self, text, length=25):

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ...."

##=========================================================================================================
##=========================================================================================================

## Controla Todo en Segundo Plano para que la App, no se Cuelgue, todo al CPU, 2do Hilo
## (Filtro de Corrección de Color)
class MergeThread11(QThread):

    innicio_11 = pyqtSignal(str)
    any_signal_11 = pyqtSignal(int)
    video_merged_11 = pyqtSignal(str)
    any_error_11 = pyqtSignal(str)
    concluyo_11 = pyqtSignal(str)

    def __init__(self, player, video_path, output_path, index=11):
        super().__init__()

        self.player = player
        self.index = index
        self.cont = True

        self.video_path = video_path
        self.output_path = output_path
        self.file_path_end = file_path_end

    def run(self):

        VideoPlayer.variables_utiles(self)

        msn = "Se Innicia, con la Tarea Asignada"
        self.innicio_11.emit(str(f"{msn}"))

        video_path = self.video_path
        output_path = self.output_path

        cnt=0
        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_11.emit(cnt)
        
        self.cont = True

        try:

            Save_All_Videos.saveVideo8(self, video_path, output_path)

        except Exception as e:
            self.any_error_11.emit(str(f'{e}'))

        meta = VideoPlayer.meta_data(self, self.player)
        msn = f"Se Concluye, con la Tarea Asignada\n{meta}\nEl Video se Almaceno en:\n{self.output_path}"
        self.concluyo_11.emit(str(f"{msn}"))

        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_11.emit(cnt)

        self.video_merged_11.emit(file_path_end)
    
    # Shorten text that may be too long
    def _truncate(self, text, length=25):

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ...."

##=========================================================================================================
##=========================================================================================================

## Controla Todo en Segundo Plano para que la App, no se Cuelgue, todo al CPU, 2do Hilo
## Resoluciones Para Video: [Alta, Media Alta, Media, Vaja]
class MergeThread12(QThread):

    innicio_12 = pyqtSignal(str)
    any_signal_12 = pyqtSignal(int)
    video_merged_12 = pyqtSignal(str)
    any_error_12 = pyqtSignal(str)
    concluyo_12 = pyqtSignal(str)

    def __init__(self, player, video_path, output_path, new_size, index=12):
        super().__init__()

        self.player = player
        self.index = index
        self.cont = True

        self.video_path = video_path
        self.output_path = output_path
        self.new_size = new_size
        self.file_path_end = file_path_end

    def run(self):

        VideoPlayer.variables_utiles(self)

        msn = "Se Innicia, con la Tarea Asignada"
        self.innicio_12.emit(str(f"{msn}"))

        video_path = self.video_path
        output_path = self.output_path
        new_size = self.new_size

        cnt=0
        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_12.emit(cnt)
        
        self.cont = True

        try:

            Save_All_Videos.saveVideo9(self, video_path, output_path, new_size)

        except Exception as e:
            self.any_error_12.emit(str(f'{e}'))

        meta = VideoPlayer.meta_data(self, self.player)
        msn = f"Se Concluye, con la Tarea Asignada\n{meta}\nEl Video se Almaceno en:\n{self.output_path}"
        self.concluyo_12.emit(str(f"{msn}"))

        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_12.emit(cnt)

        self.video_merged_12.emit(file_path_end)
    
    # Shorten text that may be too long
    def _truncate(self, text, length=25):

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ...."

##=========================================================================================================
##=========================================================================================================

## Controla Todo en Segundo Plano para que la App, no se Cuelgue, todo al CPU, 2do Hilo
## (Rotar Video)
class MergeThread13(QThread):

    innicio_13 = pyqtSignal(str)
    any_signal_13 = pyqtSignal(int)
    video_merged_13 = pyqtSignal(str)
    any_error_13 = pyqtSignal(str)
    concluyo_13 = pyqtSignal(str)

    def __init__(self, player, video_path, output_path, rotate_v, index=13):
        super().__init__()

        self.player = player
        self.index = index
        self.cont = True

        self.video_path = video_path
        self.output_path = output_path
        self.rotate_v = rotate_v
        self.file_path_end = file_path_end

    def run(self):

        VideoPlayer.variables_utiles(self)

        msn = "Se Innicia, con la Tarea Asignada"
        self.innicio_13.emit(str(f"{msn}"))

        video_path = self.video_path
        output_path = self.output_path
        rotate_v = self.rotate_v

        cnt=0
        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_13.emit(cnt)
        
        self.cont = True

        try:

            Save_All_Videos.saveVideo10(self, video_path, output_path, rotate_v)

        except Exception as e:
            self.any_error_13.emit(str(f'{e}'))

        meta = VideoPlayer.meta_data(self, self.player)
        msn = f"Se Concluye, con la Tarea Asignada\n{meta}\nEl Video se Almaceno en:\n{self.output_path}"
        self.concluyo_13.emit(str(f"{msn}"))

        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_13.emit(cnt)

        self.video_merged_13.emit(file_path_end)
    
    # Shorten text that may be too long
    def _truncate(self, text, length=25):

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ...."

##=========================================================================================================
##=========================================================================================================

## Ingreso y Selección de Imagenes para: [Crear Video de Imagenes - (class Create_Vid_F_Imgs)]
class Ingresando_Imagenes(VideoPlayer):

    def __init__(self):
        super().__init__()

##=================================================================================================
##=================================================================================================

    def name(entrada):

        entrada_im = ""
        entrada_im = entrada

        fpath, fname = os.path.split(entrada_im)
        name = fname.split('.')
        name = name[0] + '.png'

        return name

    def Open_Images(self, archivo, images_temp):

        path_im = []

        if archivo:

            if not os.path.exists(f'{images_temp}/img_temp'):
                os.mkdir(f'{images_temp}/img_temp')

            else:
                shutil.rmtree(f'{images_temp}/img_temp')
                os.mkdir(f'{images_temp}/img_temp')

            new_output = f'{images_temp}/img_temp'
            new_output1 = new_output

            for i in archivo:

                try:

                    path = Ingresando_Imagenes.name(i)

                    Ima_Menu_1 = Path.resource_path(i)
                    imagen_0 = im_app.open(Ima_Menu_1).resize((1920, 1200))
                    imagen_0.save(new_output+'/'+path, "PNG", optimize = True, quality = 150)

                    path_im.append(new_output1+'/'+path)
                    print(new_output1+'/'+path)

                except Exception as e:
                    print(e)

                    continue

            return path_im

##=========================================================================================================
##=========================================================================================================

## Crear Video de Imagenes  [Se Utiliza en: MergeThread14]
class Create_Vid_F_Imgs(VideoPlayer):

    def __init__(self):
        super().__init__()

    def Creando_Video(self, archivo, images_temp, output_path):
 
        #Leer imagenes
        cont = 0
        fra = 0.3

        dir_path = []
        path_imread = []

        archivo = Ingresando_Imagenes.Open_Images(self, archivo, images_temp)
        output_path = output_path

        if output_path == [] or output_path == "":

            QMessageBox.information(self, 'Aviso', 'No, se Guara ningun Video.')

        else:

            for i in archivo:

                try:

                    path = cv2.imread(str(i))
                    path_imread.append(path)

                except Exception as e:
                    print(e)

                    continue
             
            #Caracteristicas del video
            video = cv2.VideoWriter(output_path,cv2.VideoWriter_fourcc(*'mp4v'),fra,(1920, 1200))

            for path in path_imread:

                try:

                    # Poner cada frame en video
                    video.write(path)

                except Exception as e:
                    print(e)

                    continue
                 
            #liberar recursos
            video.release()

            # Procedemos a abrir el video:    Video_Salida
            fpath, fname = os.path.split(archivo[0])
            shutil.rmtree(fpath)

##=========================================================================================================
##=========================================================================================================
## Controla Todo en Segundo Plano para que la App, no se Cuelgue, todo al CPU, 2do Hilo
## Crear Video de Imagenes
class MergeThread14(QThread):

    innicio_14 = pyqtSignal(str)
    any_signal_14 = pyqtSignal(int)
    video_merged_14 = pyqtSignal(str)
    any_error_14 = pyqtSignal(str)
    concluyo_14 = pyqtSignal(str)

    def __init__(self, player, archivo, images_temp, output_path, index=14):
        super().__init__()

        self.player = player
        self.index = index
        self.cont = True

        self.archivo = archivo
        self.images_temp = images_temp
        self.output_path = output_path

    def run(self):

        VideoPlayer.variables_utiles(self)

        msn = "Se Innicia, con la Tarea Asignada"
        self.innicio_14.emit(str(f"{msn}"))

        archivo = self.archivo
        images_temp = self.images_temp
        output_path = self.output_path

        cnt=0
        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_14.emit(cnt)
        
        self.cont = True

        try:

            Create_Vid_F_Imgs.Creando_Video(self, archivo, images_temp, output_path)

        except Exception as e:
            self.any_error_14.emit(str(f'{e}'))

        meta = VideoPlayer.meta_data(self, self.player)
        msn = f"Se Concluye, con la Tarea Asignada\n{meta}\nEl Video se Almaceno en:\n{self.output_path}"
        self.concluyo_14.emit(str(f"{msn}"))

        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_14.emit(cnt)

        self.video_merged_14.emit(file_path_end)
    
    # Shorten text that may be too long
    def _truncate(self, text, length=25):

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ...."

##=========================================================================================================
##=========================================================================================================
## Controla Todo en Segundo Plano para que la App, no se Cuelgue, todo al CPU, 2do Hilo
## Multiplexar de 1 a 6 Videos, Forma #1
class MergeThread15(QThread):

    innicio_15 = pyqtSignal(str)
    any_signal_15 = pyqtSignal(int)
    video_merged_15 = pyqtSignal(str)
    any_error_15 = pyqtSignal(str)
    concluyo_15 = pyqtSignal(str)

    def __init__(self, player, in_video, output_path, file_path, index=15):
        super().__init__()

        self.player = player
        self.index = index
        self.cont = True
        self.in_video = in_video
        self.output_path = output_path
        self.file_path = file_path
        self.file_path_end = file_path_end

    def run(self):

        VideoPlayer.variables_utiles(self)

        msn = "Se Innicia, con la Tarea Asignada"
        self.innicio_15.emit(str(f"{msn}"))

        output_path = self.output_path
        in_video = self.in_video
        file_path = self.file_path

        cnt=0
        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_15.emit(cnt)
        
        self.cont = True

        try:

            Array_Clips.Mix_Clips(self, in_video, output_path, file_path)

        except Exception as e:
            self.any_error_15.emit(str(f'{e}'))

        meta = VideoPlayer.meta_data(self, self.player)
        msn = f"Se Concluye, con la Tarea Asignada\n{meta}\nEl Video se Almaceno en:\n{self.output_path}"
        self.concluyo_15.emit(str(f"{msn}"))

        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_15.emit(cnt)

        self.video_merged_15.emit(file_path_end)
    
    # Shorten text that may be too long
    def _truncate(self, text, length=25):

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ...."

##=========================================================================================================
##=========================================================================================================
## Controla Todo en Segundo Plano para que la App, no se Cuelgue, todo al CPU, 2do Hilo
## Multiplexar de 1 a 4 Videos, Forma #2
class MergeThread16(QThread):

    innicio_16 = pyqtSignal(str)
    any_signal_16 = pyqtSignal(int)
    video_merged_16 = pyqtSignal(str)
    any_error_16 = pyqtSignal(str)
    concluyo_16 = pyqtSignal(str)

    def __init__(self, player, in_video, output_path, file_path, index=16):
        super().__init__()

        self.player = player
        self.index = index
        self.cont = True
        self.in_video = in_video
        self.output_path = output_path
        self.file_path = file_path
        self.file_path_end = file_path_end

    def run(self):

        VideoPlayer.variables_utiles(self)

        msn = "Se Innicia, con la Tarea Asignada"
        self.innicio_16.emit(str(f"{msn}"))

        output_path = self.output_path
        in_video = self.in_video
        file_path = self.file_path

        cnt=0
        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_16.emit(cnt)
        
        self.cont = True

        try:

            Array_Clips.Mix_Clips_2(self, in_video, output_path, file_path)

        except Exception as e:
            self.any_error_16.emit(str(f'{e}'))

        meta = VideoPlayer.meta_data(self, self.player)
        msn = f"Se Concluye, con la Tarea Asignada\n{meta}\nEl Video se Almaceno en:\n{self.output_path}"
        self.concluyo_16.emit(str(f"{msn}"))

        while (self.cont):
            cnt+=1
            if cnt==1000:
                cnt=0
                self.cont = False

            time.sleep(0.01)
            self.any_signal_16.emit(cnt)

        self.video_merged_16.emit(file_path_end)
    
    # Shorten text that may be too long
    def _truncate(self, text, length=25):

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ...."

##=========================================================================================================
##=========================================================================================================

## Para Multiplexar Videos
class Array_Clips(VideoPlayer):

    def __init__(self):
        super().__init__()

    def Clip_Mix_Vids_1(self):
        global accion, file_path_open, working, file_path_video
        print("\n============================================")
        print("➜ Innicio para: Multiplexar de 1 a 6 Videos...")
        print("============================================")

        working = ""
        file_path_open = ""
        file_path_video = str("Multiplexeando Forma 1")
        title_video.Actualizando_Title(self, file_path_video)

        try:

            QMessageBox.information(self, 'Aviso', 'Fabor de Elegir Que Videos se Utilizaran Para, Crear el Nuevo Video')
            file_path = QFileDialog.getOpenFileNames(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ## (self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

            QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')
            Output_Vid = QFileDialog.getSaveFileName(self, "Guardar  video Multiplexado como?", filter="MP4(*.mp4);;AVI(*.avi)")[0] ## (self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

            if file_path == [] or file_path == "" or Output_Vid == "" or Output_Vid == []:
                pass

            else:
                Message_Box.Ms_Info_star(self)
                file_path_open = Output_Vid

                in_video_path = file_path[0]
                in_video = path_output_vid = Path.resource_path(in_video_path)

                output_path = Path.resource_path(f"{Output_Vid}")

                try:

                    self.progress_bar.setValue(0)
                    self.thread_15 = MergeThread15(self.player, in_video, output_path, file_path, index=15)
                    self.thread_15.innicio_15.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                    self.thread_15.any_signal_15.connect(lambda counter: Acctions_App.my_function(self, counter))
                    self.thread_15.video_merged_15.connect(lambda: Play_All_Videos.display_video(self, output_path))
                    self.thread_15.any_error_15.connect(lambda error: Acctions_App.my_function_error(self, error))
                    self.thread_15.concluyo_15.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                    self.thread_15.start()

                except Exception as e:
                    print(e)

                    Message_Box.dialog_critical(self, str(f'{e}'))
                    Acctions_App.concluidas_las_tareas(self)

                finally:
                    Acctions_App.concluidas_las_tareas(self)


        except Exception as e:
            print(e)

            Message_Box.dialog_critical(self, str(f'{e}'))
            Acctions_App.concluidas_las_tareas(self)

    def Clip_Mix_Vids_2(self):
        global accion, file_path_open, working, file_path_video
        print("\n============================================")
        print("➜ Innicio para: Multiplexar de 1 a 4 Videos...")
        print("============================================")

        working = ""
        file_path_open = ""
        file_path_video = str("Multiplexeando Forma 2")
        title_video.Actualizando_Title(self, file_path_video)

        try:

            QMessageBox.information(self, 'Aviso', 'Fabor de Elegir Que Imagenes se Utilizaran Para, Crear el Video')
            file_path = QFileDialog.getOpenFileNames(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ## (self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

            QMessageBox.information(self, 'Aviso', 'Fabor de darle un nombre y una Ubicación al Video, Tratado.\
\nMuchas Gracias...')
            Output_Vid = QFileDialog.getSaveFileName(self, "Guardar  video recortado como", filter="MP4(*.mp4);;AVI(*.avi)")[0] ## (self, "Guardar como", "",("MP4(* .mp4) ;; AVI(* .avi)) ;; All Files(*.*)"))

            if file_path == [] or file_path == "" or Output_Vid == "" or Output_Vid == []:
                pass

            else:

                Message_Box.Ms_Info_star(self)
                file_path_open = Output_Vid

                in_video_path = file_path[0]
                in_video = path_output_vid = Path.resource_path(in_video_path)

                output_path = Path.resource_path(f"{Output_Vid}")

                try:

                    self.progress_bar.setValue(0)
                    self.thread_16 = MergeThread16(self.player, in_video, output_path, file_path, index=16)
                    self.thread_16.innicio_16.connect(lambda innicio: Acctions_App.my_function_innicio(self, innicio))
                    self.thread_16.any_signal_16.connect(lambda counter: Acctions_App.my_function(self, counter))
                    self.thread_16.video_merged_16.connect(lambda: Play_All_Videos.display_video(self, output_path))
                    self.thread_16.any_error_16.connect(lambda error: Acctions_App.my_function_error(self, error))
                    self.thread_16.concluyo_16.connect(lambda concluyo: Acctions_App.my_function_concluyo(self, concluyo))
                    self.thread_16.start()

                except Exception as e:
                    print(e)

                    Message_Box.dialog_critical(self, str(f'{e}'))
                    Acctions_App.concluidas_las_tareas(self)

                finally:
                    Acctions_App.concluidas_las_tareas(self)

        except Exception as e:
            print(e)

            Message_Box.dialog_critical(self, str(f'{e}'))
            Acctions_App.concluidas_las_tareas(self)

    def Mix_Clips(self, in_video, output_path, file_path):

        width = 800
        height = 600
        mask = "MaskVideo\\myMaskVideo.mp4"

        try:

            cont_files = len(file_path)
            if cont_files == 1:

                # Cargar los videos
                video1 = VideoFileClip(f"{in_video}").resize(newsize = (width, height))
                video2 = VideoFileClip(f"{mask}").resize(newsize = (width, height))

                # Crear una cuadrícula con los videos
                final_clip = clips_array([[video1, video2]])

                # Guardar el video final
                final_clip.write_videofile(f"{output_path}", codec="libx264", fps=24)

            elif cont_files == 2:

                in_video2 = file_path[1]

                # Cargar los videos
                video1 = VideoFileClip(f"{in_video}").resize(newsize = (width, height))
                video2 = VideoFileClip(f"{in_video2}").resize(newsize = (width, height))

                # Crear una cuadrícula con los videos
                final_clip = clips_array([[video1, video2]])

                # Guardar el video final
                final_clip.write_videofile(f"{output_path}", codec="libx264", fps=24)

            elif cont_files == 3:

                in_video2 = file_path[1]
                in_video3 = file_path[2]

                # Cargar los videos
                video1 = VideoFileClip(f"{in_video}").resize(newsize = (width, height))
                video2 = VideoFileClip(f"{in_video2}").resize(newsize = (width, height))
                video3 = VideoFileClip(f"{in_video3}").resize(newsize = (width, height))
                video4 = VideoFileClip(f"{mask}").resize(newsize = (width, height))

                # Crear una cuadrícula con los videos
                final_clip = clips_array([[video1, video2], [video3, video4]])

                # Guardar el video final
                final_clip.write_videofile(f"{output_path}", codec="libx264", fps=24)

            elif cont_files == 4:

                in_video2 = file_path[1]
                in_video3 = file_path[2]
                in_video4 = file_path[3]

                # Cargar los videos
                video1 = VideoFileClip(f"{in_video}").resize(newsize = (width, height))
                video2 = VideoFileClip(f"{in_video2}").resize(newsize = (width, height))
                video3 = VideoFileClip(f"{in_video3}").resize(newsize = (width, height))
                video4 = VideoFileClip(f"{in_video4}").resize(newsize = (width, height))

                # Crear una cuadrícula con los videos
                final_clip = clips_array([[video1, video2], [video3, video4]])

                # Guardar el video final
                final_clip.write_videofile(f"{output_path}", codec="libx264", fps=24)

            elif cont_files == 5:

                in_video2 = file_path[1]
                in_video3 = file_path[2]
                in_video4 = file_path[3]
                in_video5 = file_path[4]

                # Cargar los videos
                video1 = VideoFileClip(f"{in_video}").resize(newsize = (width, height))
                video2 = VideoFileClip(f"{in_video2}").resize(newsize = (width, height))
                video3 = VideoFileClip(f"{in_video3}").resize(newsize = (width, height))
                video4 = VideoFileClip(f"{in_video4}").resize(newsize = (width, height))
                video5 = VideoFileClip(f"{in_video5}").resize(newsize = (width, height))
                video6 = VideoFileClip(f"{mask}").resize(newsize = (width, height))

                # Crear una cuadrícula con los videos
                final_clip = clips_array([[video1, video2, video3], [video4, video5, video6]])

                # Guardar el video final
                final_clip.write_videofile(f"{output_path}", codec="libx264", fps=24)

            elif cont_files >= 6:

                in_video2 = file_path[1]
                in_video3 = file_path[2]
                in_video4 = file_path[3]
                in_video5 = file_path[4]
                in_video6 = file_path[5]

                # Cargar los videos
                video1 = VideoFileClip(f"{in_video}").resize(newsize = (width, height))
                video2 = VideoFileClip(f"{in_video2}").resize(newsize = (width, height))
                video3 = VideoFileClip(f"{in_video3}").resize(newsize = (width, height))
                video4 = VideoFileClip(f"{in_video4}").resize(newsize = (width, height))
                video5 = VideoFileClip(f"{in_video5}").resize(newsize = (width, height))
                video6 = VideoFileClip(f"{in_video6}").resize(newsize = (width, height))

                # Crear una cuadrícula con los videos
                final_clip = clips_array([[video1, video2, video3], [video4, video5, video6]])

                # Guardar el video final
                final_clip.write_videofile(f"{output_path}", codec="libx264", fps=24)

        except Exception as e:
            print(e)

            Message_Box.dialog_critical(self, str(f'{e}'))
            Acctions_App.concluidas_las_tareas(self)

##================================================================================
##================================================================================

    def Mix_Clips_2(self, in_video, output_path, file_path):

        try:

            cont_files = len(file_path)
            if cont_files == 1:

                # Cargar los videos
                video1 = cv2.VideoCapture(f"{file_path[0]}")

                # Obtener propiedades
                fps = int(video1.get(cv2.CAP_PROP_FPS))
                width = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))

                # Definir tamaño de cada video en la composición
                new_width = width // 2
                new_height = height // 2

                # Crear un nuevo video para guardar el resultado
                out = cv2.VideoWriter(f"{output_path}", cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

                while True:

                    ret1, frame1 = video1.read()

                    if not ret1:
                        break

                    # Redimensionar los videos para que entren en la misma imagen
                    frame1 = cv2.resize(frame1, (new_width, new_height))

                    # Crear un fondo negro donde pondremos los videos
                    output_frame = np.zeros((height, width, 3), dtype=np.uint8)

                    # Colocar los videos en diferentes posiciones
                    output_frame[:new_height, :new_width] = frame1  # Arriba izquierda

                    # Escribir el frame en el video de salida
                    out.write(output_frame)

                # Liberar recursos
                video1.release()

                out.release()
                cv2.destroyAllWindows()

            elif cont_files == 2:

                # Cargar los videos
                video1 = cv2.VideoCapture(f"{file_path[0]}")
                video2 = cv2.VideoCapture(f"{file_path[1]}")

                # Obtener propiedades
                fps = int(video1.get(cv2.CAP_PROP_FPS))
                width = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))

                # Definir tamaño de cada video en la composición
                new_width = width // 2
                new_height = height // 2

                # Crear un nuevo video para guardar el resultado
                out = cv2.VideoWriter(f"{output_path}", cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

                while True:

                    ret1, frame1 = video1.read()
                    ret2, frame2 = video2.read()

                    if not ret1 or not ret2:
                        break

                    # Redimensionar los videos para que entren en la misma imagen
                    frame1 = cv2.resize(frame1, (new_width, new_height))
                    frame2 = cv2.resize(frame2, (new_width, new_height))

                    # Crear un fondo negro donde pondremos los videos
                    output_frame = np.zeros((height, width, 3), dtype=np.uint8)

                    # Colocar los videos en diferentes posiciones
                    output_frame[:new_height, :new_width] = frame1  # Arriba izquierda
                    output_frame[:new_height, new_width:] = frame2  # Arriba derecha

                    # Escribir el frame en el video de salida
                    out.write(output_frame)

                # Liberar recursos
                video1.release()
                video2.release()

                out.release()
                cv2.destroyAllWindows()

            elif cont_files == 3:

                # Cargar los videos
                video1 = cv2.VideoCapture(f"{file_path[0]}")
                video2 = cv2.VideoCapture(f"{file_path[1]}")
                video3 = cv2.VideoCapture(f"{file_path[2]}")

                # Obtener propiedades
                fps = int(video1.get(cv2.CAP_PROP_FPS))
                width = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))

                # Definir tamaño de cada video en la composición
                new_width = width // 2
                new_height = height // 2

                # Crear un nuevo video para guardar el resultado
                out = cv2.VideoWriter(f"{output_path}", cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

                while True:

                    ret1, frame1 = video1.read()
                    ret2, frame2 = video2.read()
                    ret3, frame3 = video3.read()

                    if not ret1 or not ret2 or not ret3:
                        break

                    # Redimensionar los videos para que entren en la misma imagen
                    frame1 = cv2.resize(frame1, (new_width, new_height))
                    frame2 = cv2.resize(frame2, (new_width, new_height))
                    frame3 = cv2.resize(frame3, (new_width, new_height))

                    # Crear un fondo negro donde pondremos los videos
                    output_frame = np.zeros((height, width, 3), dtype=np.uint8)

                    # Colocar los videos en diferentes posiciones
                    output_frame[:new_height, :new_width] = frame1  # Arriba izquierda
                    output_frame[:new_height, new_width:] = frame2  # Arriba derecha
                    output_frame[new_height:, :new_width] = frame3  # Abajo izquierda

                    # Escribir el frame en el video de salida
                    out.write(output_frame)

                # Liberar recursos
                video1.release()
                video2.release()
                video3.release()

                out.release()
                cv2.destroyAllWindows()

            elif cont_files >= 4:

                # Cargar los videos
                video1 = cv2.VideoCapture(f"{file_path[0]}")
                video2 = cv2.VideoCapture(f"{file_path[1]}")
                video3 = cv2.VideoCapture(f"{file_path[2]}")
                video4 = cv2.VideoCapture(f"{file_path[3]}")

                # Obtener propiedades
                fps = int(video1.get(cv2.CAP_PROP_FPS))
                width = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))

                # Definir tamaño de cada video en la composición
                new_width = width // 2
                new_height = height // 2

                # Crear un nuevo video para guardar el resultado
                out = cv2.VideoWriter(f"{output_path}", cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

                while True:

                    ret1, frame1 = video1.read()
                    ret2, frame2 = video2.read()
                    ret3, frame3 = video3.read()
                    ret4, frame4 = video4.read()

                    if not ret1 or not ret2 or not ret3 or not ret4:
                        break

                    # Redimensionar los videos para que entren en la misma imagen
                    frame1 = cv2.resize(frame1, (new_width, new_height))
                    frame2 = cv2.resize(frame2, (new_width, new_height))
                    frame3 = cv2.resize(frame3, (new_width, new_height))
                    frame4 = cv2.resize(frame4, (new_width, new_height))

                    # Crear un fondo negro donde pondremos los videos
                    output_frame = np.zeros((height, width, 3), dtype=np.uint8)

                    # Colocar los videos en diferentes posiciones
                    output_frame[:new_height, :new_width] = frame1  # Arriba izquierda
                    output_frame[:new_height, new_width:] = frame2  # Arriba derecha
                    output_frame[new_height:, :new_width] = frame3  # Abajo izquierda
                    output_frame[new_height:, new_width:] = frame4  # Abajo derecha

                    # Escribir el frame en el video de salida
                    out.write(output_frame)

                # Liberar recursos
                video1.release()
                video2.release()
                video3.release()            
                video4.release()

                out.release()
                cv2.destroyAllWindows()

        except Exception as e:
            print(e)

            Message_Box.dialog_critical(self, str(f'{e}'))
            Acctions_App.concluidas_las_tareas(self)

##=========================================================================================================
##final_clip = clips_array([[video1, video2], [video3, video4]]) mask
##=========================================================================================================

## Menú en Clic Derecho de el Mouse, o en Teclado con Tecla Menú
class Menu_Clic(VideoPlayer):

    def __init__(self):
        super().__init__()

    def Menu_RightClic(self):

        Play_All_Videos.playVideo(self)
        Menu_Clic.create_rightmenu(self)

    def create_rightmenu(self):

        # Objeto de menú
        self.groupBox_menu = QMenu(self)
        self.groupBox_menu.setFont(self.font)
        self.groupBox_menu.setStyleSheet('background-color: #b3ffb3; color: #400080; selection-background-color: #8080ff')

        ##================================================================================================================
        ##================================================================================================================

        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        self.Converted_To_MP4_1 = Path.resource_path('Ico\\tech.png')
        self.Converted_To_MP4 = QAction(QIcon(self.Converted_To_MP4_1), 'Converted To MP4', self)

        self.Converted_To_MP4.setStatusTip('Converted To MP4') 
        self.Converted_To_MP4.triggered.connect(lambda: Acctions_App.convert_video(self)) 
        self.groupBox_menu.addAction(self.Converted_To_MP4)

        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.edit_ico = Path.resource_path('Ico\\Ok-icon.png')
        self.edit = self.groupBox_menu.addMenu(QIcon(self.edit_ico), '&Menú Sonido')
        self.edit.setStyleSheet('background-color: #cc9999; color: blue, ; selection-background-color: #8a4848')

        self.edit.addSeparator()
        self.edit.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.edit.addSeparator()
        self.edit.addSeparator()

        self.Quitar_Sonido_1 = Path.resource_path('Ico\\tech.png')
        self.Quitar_Sonido = QAction(QIcon(self.Quitar_Sonido_1), '&Quitar Sonido', self)

        self.Quitar_Sonido.setStatusTip('Quitar Sonido') 
        self.Quitar_Sonido.triggered.connect(lambda: Acctions_App.quitar_audio_video(self)) 
        self.edit.addAction(self.Quitar_Sonido)

        self.edit.addSeparator()
        self.edit.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.edit.addSeparator()
        self.edit.addSeparator()

        self.Agregar_Sonido_1 = Path.resource_path('Ico\\tech.png')
        self.Agregar_Sonido = QAction(QIcon(self.Agregar_Sonido_1), '&Agregar Sonido', self)

        self.Agregar_Sonido.setStatusTip('Agregar Sonido') 
        self.Agregar_Sonido.triggered.connect(lambda: Acctions_App.agregar_audio_video(self)) 
        self.edit.addAction(self.Agregar_Sonido)

        self.edit.addSeparator()
        self.edit.addSeparator()

        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.edit_ico_1 = Path.resource_path('Ico\\Ok-icon.png')
        self.edit_2 = self.groupBox_menu.addMenu(QIcon(self.edit_ico_1), '&Menú Video Brillo')
        self.edit_2.setStyleSheet('background-color: #fe23bc; color: blue, ; selection-background-color: #b000b0')

        self.edit_2.addSeparator()
        self.edit_2.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.edit_2.addSeparator()
        self.edit_2.addSeparator()

        self.ajustar_video0 = Path.resource_path('Ico\\tech.png')
        self.ajustar_video_1 = QAction(QIcon(self.ajustar_video0), '&Ajustar Video Poco', self)

        self.ajustar_video_1.setStatusTip('Ajustar_Video_Poco') 
        self.ajustar_video_1.triggered.connect(lambda: Acctions_App.ajustar_video_poco(self)) 
        self.edit_2.addAction(self.ajustar_video_1)

        self.edit_2.addSeparator()
        self.edit_2.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.edit_2.addSeparator()
        self.edit_2.addSeparator()

        self.ajustar_video1 = Path.resource_path('Ico\\tech.png')
        self.ajustar_video_2 = QAction(QIcon(self.ajustar_video1), '&Ajustar Video Medio', self)

        self.ajustar_video_2.setStatusTip('Ajustar_Video_Medio') 
        self.ajustar_video_2.triggered.connect(lambda: Acctions_App.ajustar_video_medio(self)) 
        self.edit_2.addAction(self.ajustar_video_2)

        self.edit_2.addSeparator()
        self.edit_2.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.edit_2.addSeparator()
        self.edit_2.addSeparator()

        self.ajustar_video2 = Path.resource_path('Ico\\tech.png')
        self.ajustar_video_2 = QAction(QIcon(self.ajustar_video2), '&Ajustar Video Alto', self)

        self.ajustar_video_2.setStatusTip('Ajustar_Video_Alto') 
        self.ajustar_video_2.triggered.connect(lambda: Acctions_App.ajustar_video_alto(self)) 
        self.edit_2.addAction(self.ajustar_video_2)

        self.edit_2.addSeparator()
        self.edit_2.addSeparator()

        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.Efecto_1 = Path.resource_path('Ico\\Ok-icon.png')
        self.edit_efecto = self.groupBox_menu.addMenu(QIcon(self.Efecto_1), '&Menú Efectos Colores Video')
        self.edit_efecto.setStyleSheet('background-color: #3333ff; color: blue, ; selection-background-color: #0000a8')

        self.edit_efecto.addSeparator()
        self.edit_efecto.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.edit_efecto.addSeparator()
        self.edit_efecto.addSeparator()

        self.Efecto_blanco_negro0 = Path.resource_path('Ico\\tech.png')
        self.Efecto_blanco_negro1 = QAction(QIcon(self.Efecto_blanco_negro0), '&Efecto Blanco y Negro', self)

        self.Efecto_blanco_negro1.setStatusTip('Efecto_blanco_negro') 
        self.Efecto_blanco_negro1.triggered.connect(lambda: Acctions_App.Efecto_blanco_negro(self)) 
        self.edit_efecto.addAction(self.Efecto_blanco_negro1)

        ##================================================================================================================
        ##================================================================================================================

        self.edit_efecto.addSeparator()
        self.edit_efecto.addSeparator()

        self.Efecto_Sepia0 = Path.resource_path('Ico\\tech.png')
        self.Efecto_Sepia1 = QAction(QIcon(self.Efecto_Sepia0), '&Efecto Sepia', self)

        self.Efecto_Sepia1.setStatusTip('Efecto Sepia') 
        self.Efecto_Sepia1.triggered.connect(lambda: Acctions_App.Efecto_Sepia(self)) 
        self.edit_efecto.addAction(self.Efecto_Sepia1)

        ##================================================================================================================
        ##================================================================================================================

        self.edit_efecto.addSeparator()
        self.edit_efecto.addSeparator()

        self.Efecto_Azul0 = Path.resource_path('Ico\\tech.png')
        self.Efecto_Azul1 = QAction(QIcon(self.Efecto_Azul0), '&Efecto Azul', self)

        self.Efecto_Azul1.setStatusTip('Efecto Azul') 
        self.Efecto_Azul1.triggered.connect(lambda: Acctions_App.Efecto_Azul(self)) 
        self.edit_efecto.addAction(self.Efecto_Azul1)

        ##================================================================================================================
        ##================================================================================================================

        self.edit_efecto.addSeparator()
        self.edit_efecto.addSeparator()

        self.Efecto_Rojo0 = Path.resource_path('Ico\\tech.png')
        self.Efecto_Rojo1 = QAction(QIcon(self.Efecto_Rojo0), '&Efecto Rojo', self)

        self.Efecto_Rojo1.setStatusTip('Efecto Rojo') 
        self.Efecto_Rojo1.triggered.connect(lambda: Acctions_App.Efecto_Rojo(self)) 
        self.edit_efecto.addAction(self.Efecto_Rojo1)

        ##================================================================================================================
        ##================================================================================================================

        self.edit_efecto.addSeparator()
        self.edit_efecto.addSeparator()

        self.Efecto_Verde0 = Path.resource_path('Ico\\tech.png')
        self.Efecto_Verde1 = QAction(QIcon(self.Efecto_Verde0), '&Efecto Verde', self)

        self.Efecto_Verde1.setStatusTip('Efecto Verde') 
        self.Efecto_Verde1.triggered.connect(lambda: Acctions_App.Efecto_Verde(self)) 
        self.edit_efecto.addAction(self.Efecto_Verde1)

        ##================================================================================================================
        ##================================================================================================================

        self.edit_efecto.addSeparator()
        self.edit_efecto.addSeparator()

        self.Efecto_Amarillo0 = Path.resource_path('Ico\\tech.png')
        self.Efecto_Amarillo1 = QAction(QIcon(self.Efecto_Amarillo0), '&Efecto Amarillo', self)

        self.Efecto_Amarillo1.setStatusTip('Efecto Amarillo') 
        self.Efecto_Amarillo1.triggered.connect(lambda: Acctions_App.Efecto_Amarillo(self)) 
        self.edit_efecto.addAction(self.Efecto_Amarillo1)

        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Marca_de_Agua0 = Path.resource_path('Ico\\Ok-icon.png')
        self.Menú_Marca_de_Agua = self.groupBox_menu.addMenu(QIcon(self.Menú_Marca_de_Agua0), '&Menú Marca de Agua')
        self.Menú_Marca_de_Agua.setStyleSheet('background-color: #00eaea; color: blue, ; selection-background-color: #005959')

        self.Menú_Marca_de_Agua.addSeparator()
        self.Menú_Marca_de_Agua.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Marca_de_Agua_arrIz0 = Path.resource_path('Ico\\Ok-icon.png')
        self.Menú_Marca_de_Agua_arrIz = self.Menú_Marca_de_Agua.addMenu(QIcon(self.Menú_Marca_de_Agua_arrIz0), '&Menú Marca de Agua Arriba')
        self.Menú_Marca_de_Agua_arrIz.setStyleSheet('background-color: #cc9999; color: blue, ; selection-background-color: #8a4848')

        self.Menú_Marca_de_Agua_arrIz.addSeparator()
        self.Menú_Marca_de_Agua_arrIz.addSeparator()

        self.Menú_Marca_de_Agua.addSeparator()
        self.Menú_Marca_de_Agua.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Marca_de_Agua_arrIz.addSeparator()
        self.Menú_Marca_de_Agua_arrIz.addSeparator()

        self.marca_de_agua_Arr_Iz0 = Path.resource_path('Ico\\tech.png')
        self.marca_de_agua_Arr_Iz1 = QAction(QIcon(self.marca_de_agua_Arr_Iz0), '&Marca de Agua Arriba Izquierda', self)

        self.marca_de_agua_Arr_Iz1.setStatusTip('marca_de_agua_Arr_Iz') 
        self.marca_de_agua_Arr_Iz1.triggered.connect(lambda: Acctions_App.agregar_marca_de_agua_Arr_Iz(self)) 
        self.Menú_Marca_de_Agua_arrIz.addAction(self.marca_de_agua_Arr_Iz1)

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Marca_de_Agua_arrIz.addSeparator()
        self.Menú_Marca_de_Agua_arrIz.addSeparator()

        self.marca_de_agua_Arr_Centrada0 = Path.resource_path('Ico\\tech.png')
        self.marca_de_agua_Arr_Centrada1 = QAction(QIcon(self.marca_de_agua_Arr_Centrada0), '&Marca de Agua Arriba Centrada', self)

        self.marca_de_agua_Arr_Centrada1.setStatusTip('marca_de_agua_Arr_Centrada') 
        self.marca_de_agua_Arr_Centrada1.triggered.connect(lambda: Acctions_App.marca_de_agua_Arr_Centrada(self)) 
        self.Menú_Marca_de_Agua_arrIz.addAction(self.marca_de_agua_Arr_Centrada1)

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Marca_de_Agua_arrIz.addSeparator()
        self.Menú_Marca_de_Agua_arrIz.addSeparator()

        self.agregar_marca_de_agua_Aba_De0 = Path.resource_path('Ico\\tech.png')
        self.agregar_marca_de_agua_Aba_De1 = QAction(QIcon(self.agregar_marca_de_agua_Aba_De0), '&Marca de Agua Arriba Derecha', self)

        self.agregar_marca_de_agua_Aba_De1.setStatusTip('marca_de_agua_Arr_Derecha') 
        self.agregar_marca_de_agua_Aba_De1.triggered.connect(lambda: Acctions_App.agregar_marca_de_agua_Arr_De(self))
        self.Menú_Marca_de_Agua_arrIz.addAction(self.agregar_marca_de_agua_Aba_De1)

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Marca_de_Agua_Centrado0 = Path.resource_path('Ico\\Ok-icon.png')
        self.Menú_Marca_de_Agua_Centrado = self.Menú_Marca_de_Agua.addMenu(QIcon(self.Menú_Marca_de_Agua_Centrado0), '&Menú Marca de Agua Centrado')
        self.Menú_Marca_de_Agua_Centrado.setStyleSheet('background-color: #cc9999; color: blue, ; selection-background-color: #8a4848')

        self.Menú_Marca_de_Agua_Centrado.addSeparator()
        self.Menú_Marca_de_Agua_Centrado.addSeparator()

        self.Menú_Marca_de_Agua.addSeparator()
        self.Menú_Marca_de_Agua.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Marca_de_Agua_Centrado.addSeparator()
        self.Menú_Marca_de_Agua_Centrado.addSeparator()

        self.agregar_marca_de_agua_Cent_Iz0 = Path.resource_path('Ico\\tech.png')
        self.agregar_marca_de_agua_Cent_Iz1 = QAction(QIcon(self.agregar_marca_de_agua_Cent_Iz0), '&Marca de Agua Centrado, Izquierda', self)

        self.agregar_marca_de_agua_Cent_Iz1.setStatusTip('marca_de_agua_Cent_Centrada') 
        self.agregar_marca_de_agua_Cent_Iz1.triggered.connect(lambda: Acctions_App.agregar_marca_de_agua_Cent_Iz(self)) 
        self.Menú_Marca_de_Agua_Centrado.addAction(self.agregar_marca_de_agua_Cent_Iz1)

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Marca_de_Agua_Centrado.addSeparator()
        self.Menú_Marca_de_Agua_Centrado.addSeparator()

        self.agregar_marca_de_agua_Cent_Centrada0 = Path.resource_path('Ico\\tech.png')
        self.agregar_marca_de_agua_Cent_Centrada1 = QAction(QIcon(self.agregar_marca_de_agua_Cent_Centrada0), '&Marca de Agua Centrado, Centrada', self)

        self.agregar_marca_de_agua_Cent_Centrada1.setStatusTip('marca_de_agua_Cent_Centrada') 
        self.agregar_marca_de_agua_Cent_Centrada1.triggered.connect(lambda: Acctions_App.agregar_marca_de_agua_Cent_Centrada(self))
        self.Menú_Marca_de_Agua_Centrado.addAction(self.agregar_marca_de_agua_Cent_Centrada1)

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Marca_de_Agua_Centrado.addSeparator()
        self.Menú_Marca_de_Agua_Centrado.addSeparator()

        self.agregar_marca_de_agua_Cent_De0 = Path.resource_path('Ico\\tech.png')
        self.agregar_marca_de_agua_Cent_De1 = QAction(QIcon(self.agregar_marca_de_agua_Cent_De0), '&Marca de Agua Centrado, Derecha', self)

        self.agregar_marca_de_agua_Cent_De1.setStatusTip('marca_de_agua_Cent_Centrada') 
        self.agregar_marca_de_agua_Cent_De1.triggered.connect(lambda: Acctions_App.agregar_marca_de_agua_Cent_De(self)) 
        self.Menú_Marca_de_Agua_Centrado.addAction(self.agregar_marca_de_agua_Cent_De1)

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Marca_de_Agua_Abajo0 = Path.resource_path('Ico\\Ok-icon.png')
        self.Menú_Marca_de_Agua_Abajo = self.Menú_Marca_de_Agua.addMenu(QIcon(self.Menú_Marca_de_Agua_Abajo0), '&Menú Marca de Agua Abajo')
        self.Menú_Marca_de_Agua_Abajo.setStyleSheet('background-color: #cc9999; color: blue, ; selection-background-color: #8a4848')

        self.Menú_Marca_de_Agua_Abajo.addSeparator()
        self.Menú_Marca_de_Agua_Abajo.addSeparator()

        self.Menú_Marca_de_Agua.addSeparator()
        self.Menú_Marca_de_Agua.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Marca_de_Agua_Abajo.addSeparator()
        self.Menú_Marca_de_Agua_Abajo.addSeparator()

        self.agregar_marca_de_agua_Aba_Iz0 = Path.resource_path('Ico\\tech.png')
        self.agregar_marca_de_agua_Aba_Iz1 = QAction(QIcon(self.agregar_marca_de_agua_Aba_Iz0), '&Marca de Agua Abajo Izquierda', self)

        self.agregar_marca_de_agua_Aba_Iz1.setStatusTip('marca_de_agua_Aba_Centrada') 
        self.agregar_marca_de_agua_Aba_Iz1.triggered.connect(lambda: Acctions_App.agregar_marca_de_agua_Aba_Iz(self)) 
        self.Menú_Marca_de_Agua_Abajo.addAction(self.agregar_marca_de_agua_Aba_Iz1)

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Marca_de_Agua_Abajo.addSeparator()
        self.Menú_Marca_de_Agua_Abajo.addSeparator()

        self.agregar_marca_de_agua_Aba_Centrada0 = Path.resource_path('Ico\\tech.png')
        self.agregar_marca_de_agua_Aba_Centrada1 = QAction(QIcon(self.agregar_marca_de_agua_Aba_Centrada0), '&Marca de Agua Aabjo Centrada', self)

        self.agregar_marca_de_agua_Aba_Centrada1.setStatusTip('marca_de_agua_Aba_Centrada') 
        self.agregar_marca_de_agua_Aba_Centrada1.triggered.connect(lambda: Acctions_App.agregar_marca_de_agua_Aba_Centrada(self))
        self.Menú_Marca_de_Agua_Abajo.addAction(self.agregar_marca_de_agua_Aba_Centrada1)

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Marca_de_Agua_Abajo.addSeparator()
        self.Menú_Marca_de_Agua_Abajo.addSeparator()

        self.agregar_marca_de_agua_Arr_De0 = Path.resource_path('Ico\\tech.png')
        self.agregar_marca_de_agua_Arr_De1 = QAction(QIcon(self.agregar_marca_de_agua_Arr_De0), '&Marca de Agua Aabjo Derecha', self)

        self.agregar_marca_de_agua_Arr_De1.setStatusTip('marca_de_agua_Aba_Centrada') 
        self.agregar_marca_de_agua_Arr_De1.triggered.connect(lambda: Acctions_App.agregar_marca_de_agua_Aba_De(self)) 
        self.Menú_Marca_de_Agua_Abajo.addAction(self.agregar_marca_de_agua_Arr_De1)

        ##================================================================================================================
        ##================================================================================================================

        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        self.Menú_Corrección_Color0 = Path.resource_path('Ico\\Ok-icon.png')
        self.Menú_Corrección_Color = self.groupBox_menu.addMenu(QIcon(self.Menú_Corrección_Color0), '&Menú Corrección de Color')
        self.Menú_Corrección_Color.setStyleSheet('background-color: #c0c0c0; color: blue, ; selection-background-color: #400080')

        self.Menú_Corrección_Color.addSeparator()
        self.Menú_Corrección_Color.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Corrección_Color.addSeparator()
        self.Menú_Corrección_Color.addSeparator()

        self.Corrección_Color0 = Path.resource_path('Ico\\tech.png')
        self.Corrección_Color1 = QAction(QIcon(self.Corrección_Color0), '&Filtro de Corrección de Color', self)

        self.Corrección_Color1.setStatusTip('Corrección Color') 
        self.Corrección_Color1.triggered.connect(lambda: Acctions_App.color_filter(self)) 
        self.Menú_Corrección_Color.addAction(self.Corrección_Color1)

        ##================================================================================================================
        ##================================================================================================================

        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        self.Menú_Corrección_resize_video0 = Path.resource_path('Ico\\Ok-icon.png')
        self.Menú_Corrección_resize_video = self.groupBox_menu.addMenu(QIcon(self.Menú_Corrección_resize_video0), '&Menú Resolución en Video')
        self.Menú_Corrección_resize_video.setStyleSheet('background-color: #00eaea; color: blue, ; selection-background-color: #005959')

        self.Menú_Corrección_resize_video.addSeparator()
        self.Menú_Corrección_resize_video.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Resolución_Video_Alta0 = Path.resource_path('Ico\\Ok-icon.png')
        self.Menú_Resolución_Video_Alta = self.Menú_Corrección_resize_video.addMenu(QIcon(self.Menú_Resolución_Video_Alta0), '&Resolución en Video Alta:')
        self.Menú_Resolución_Video_Alta.setStyleSheet('background-color: #cc9999; color: blue, ; selection-background-color: #8a4848')

        self.Menú_Resolución_Video_Alta.addSeparator()
        self.Menú_Resolución_Video_Alta.addSeparator()

        self.Menú_Corrección_resize_video.addSeparator()
        self.Menú_Corrección_resize_video.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Resolución_Video_Alta.addSeparator()
        self.Menú_Resolución_Video_Alta.addSeparator()

        self.Corrección_4320p0 = Path.resource_path('Ico\\tech.png')
        self.Corrección_4320p1 = QAction(QIcon(self.Corrección_4320p0), '&Resolucione: 4320p (8K): 7680x4320', self)

        self.Corrección_4320p1.setStatusTip('Corrección Color') 
        self.Corrección_4320p1.triggered.connect(lambda: Acctions_App.resize_resolutin_4320p(self))
        self.Menú_Resolución_Video_Alta.addAction(self.Corrección_4320p1)

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Resolución_Video_Alta.addSeparator()
        self.Menú_Resolución_Video_Alta.addSeparator()

        self.Corrección_2160p0 = Path.resource_path('Ico\\tech.png')
        self.Corrección_2160p1 = QAction(QIcon(self.Corrección_2160p0), '&Resolucione: 2160p (4K): 3840x2161', self)

        self.Corrección_2160p1.setStatusTip('Corrección Color') 
        self.Corrección_2160p1.triggered.connect(lambda: Acctions_App.resize_resolutin_2160p(self))
        self.Menú_Resolución_Video_Alta.addAction(self.Corrección_2160p1)

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Resolución_Video_Alta.addSeparator()
        self.Menú_Resolución_Video_Alta.addSeparator()

        self.Corrección_1440p0 = Path.resource_path('Ico\\tech.png')
        self.Corrección_1440p1 = QAction(QIcon(self.Corrección_1440p0), '&Resolucione: 1440p (2K): 2560x1440', self)

        self.Corrección_1440p1.setStatusTip('Corrección Color')
        self.Corrección_1440p1.triggered.connect(lambda: Acctions_App.resize_resolutin_1440p(self))
        self.Menú_Resolución_Video_Alta.addAction(self.Corrección_1440p1)

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Resolución_Video_Media0 = Path.resource_path('Ico\\Ok-icon.png')
        self.Menú_Resolución_Video_Media = self.Menú_Corrección_resize_video.addMenu(QIcon(self.Menú_Resolución_Video_Media0), '&Resolución en Video Media:')
        self.Menú_Resolución_Video_Media.setStyleSheet('background-color: #cc9999; color: blue, ; selection-background-color: #8a4848')

        self.Menú_Resolución_Video_Media.addSeparator()
        self.Menú_Resolución_Video_Media.addSeparator()

        self.Menú_Corrección_resize_video.addSeparator()
        self.Menú_Corrección_resize_video.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Resolución_Video_Media.addSeparator()
        self.Menú_Resolución_Video_Media.addSeparator()

        self.Corrección_1080p0 = Path.resource_path('Ico\\tech.png')
        self.Corrección_1080p1 = QAction(QIcon(self.Corrección_1080p0), '&Resolucione: 1080p (HD): 1920x1080 -|- Recomendado', self)

        self.Corrección_1080p1.setStatusTip('Corrección Color') 
        self.Corrección_1080p1.triggered.connect(lambda: Acctions_App.resize_resolutin_1080p(self))
        self.Menú_Resolución_Video_Media.addAction(self.Corrección_1080p1)

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Resolución_Video_Media.addSeparator()
        self.Menú_Resolución_Video_Media.addSeparator()

        self.Corrección_720p0 = Path.resource_path('Ico\\tech.png')
        self.Corrección_720p1 = QAction(QIcon(self.Corrección_720p0), '&Resolucione: 720p (HD): 1280x720', self)

        self.Corrección_720p1.setStatusTip('Corrección Color') 
        self.Corrección_720p1.triggered.connect(lambda: Acctions_App.resize_resolutin_720p(self))
        self.Menú_Resolución_Video_Media.addAction(self.Corrección_720p1)

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Resolución_Video_Vaja0 = Path.resource_path('Ico\\Ok-icon.png')
        self.Menú_Resolución_Video_Vaja = self.Menú_Corrección_resize_video.addMenu(QIcon(self.Menú_Resolución_Video_Vaja0), '&Resolución en Video Vaja:')
        self.Menú_Resolución_Video_Vaja.setStyleSheet('background-color: #cc9999; color: blue, ; selection-background-color: #8a4848')

        self.Menú_Resolución_Video_Vaja.addSeparator()
        self.Menú_Resolución_Video_Vaja.addSeparator()

        self.Menú_Corrección_resize_video.addSeparator()
        self.Menú_Corrección_resize_video.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Resolución_Video_Vaja.addSeparator()
        self.Menú_Resolución_Video_Vaja.addSeparator()

        self.Corrección_480p0 = Path.resource_path('Ico\\tech.png')
        self.Corrección_480p1 = QAction(QIcon(self.Corrección_480p0), '&Resolucione: 480p (SD): 854x480', self)

        self.Corrección_480p1.setStatusTip('Corrección Color') 
        self.Corrección_480p1.triggered.connect(lambda: Acctions_App.resize_resolutin_480p(self))
        self.Menú_Resolución_Video_Vaja.addAction(self.Corrección_480p1)

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Resolución_Video_Vaja.addSeparator()
        self.Menú_Resolución_Video_Vaja.addSeparator()

        self.Corrección_360p0 = Path.resource_path('Ico\\tech.png')
        self.Corrección_360p1 = QAction(QIcon(self.Corrección_360p0), '&Resolucione: 360p (SD): 640x360', self)

        self.Corrección_360p1.setStatusTip('Corrección Color') 
        self.Corrección_360p1.triggered.connect(lambda: Acctions_App.resize_resolutin_360p(self))
        self.Menú_Resolución_Video_Vaja.addAction(self.Corrección_360p1)

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_Resolución_Video_Vaja.addSeparator()
        self.Menú_Resolución_Video_Vaja.addSeparator()

        self.Corrección_resize_video0 = Path.resource_path('Ico\\tech.png')
        self.Corrección_resize_video1 = QAction(QIcon(self.Corrección_resize_video0), '&Resolucione: 240p (SD): 426x240', self)

        self.Corrección_resize_video1.setStatusTip('Corrección Color') 
        self.Corrección_resize_video1.triggered.connect(lambda: Acctions_App.resize_resolutin_240p(self))
        self.Menú_Resolución_Video_Vaja.addAction(self.Corrección_resize_video1)

        ##================================================================================================================
        ##================================================================================================================

        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        self.Menú_rotate_vid0 = Path.resource_path('Ico\\Ok-icon.png')
        self.Menú_rotate_vid = self.groupBox_menu.addMenu(QIcon(self.Menú_rotate_vid0), '&Menú Ratación de Video')
        self.Menú_rotate_vid.setStyleSheet('background-color: #00eaea; color: blue, ; selection-background-color: #005959')

        self.Menú_rotate_vid.addSeparator()
        self.Menú_rotate_vid.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_rotate_vid.addSeparator()
        self.Menú_rotate_vid.addSeparator()

        self.rotate_vid_900 = Path.resource_path('Ico\\tech.png')
        self.rotate_vid_901 = QAction(QIcon(self.rotate_vid_900), '&Rotar Video (-) 90g', self)

        self.rotate_vid_901.setStatusTip('Corrección Color') 
        self.rotate_vid_901.triggered.connect(lambda: Acctions_App.rotate_vid_90(self))
        self.Menú_rotate_vid.addAction(self.rotate_vid_901)

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_rotate_vid.addSeparator()
        self.Menú_rotate_vid.addSeparator()

        self.rotate_vid_2700 = Path.resource_path('Ico\\tech.png')
        self.rotate_vid_2701 = QAction(QIcon(self.rotate_vid_2700), '&Rotar Video (+) 90g', self)

        self.rotate_vid_2701.setStatusTip('Corrección Color') 
        self.rotate_vid_2701.triggered.connect(lambda: Acctions_App.rotate_vid_270(self))
        self.Menú_rotate_vid.addAction(self.rotate_vid_2701)

        ##================================================================================================================
        ##================================================================================================================

        self.Menú_rotate_vid.addSeparator()
        self.Menú_rotate_vid.addSeparator()

        self.rotate_vid_1800 = Path.resource_path('Ico\\tech.png')
        self.rotate_vid_1801 = QAction(QIcon(self.rotate_vid_1800), '&Rotar Video 180g', self)

        self.rotate_vid_1801.setStatusTip('Corrección Color') 
        self.rotate_vid_1801.triggered.connect(lambda: Acctions_App.rotate_vid_180(self))
        self.Menú_rotate_vid.addAction(self.rotate_vid_1801)

        ##================================================================================================================
        ##================================================================================================================

        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        self.Exit_file = Path.resource_path('Ico\\tech.png')
        Create_vid_f_Imgs = QAction(QIcon(self.Exit_file), '&Crear Video de Imagenes', self)

        Create_vid_f_Imgs.setStatusTip("Create Vid From Imgs")
        Create_vid_f_Imgs.triggered.connect(lambda: Acctions_App.Create_Video_From_IMGs(self))
        self.groupBox_menu.addAction(Create_vid_f_Imgs) 
        
        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.Multiplexar_ico = Path.resource_path('Ico\\Ok-icon.png')
        self.Multiplexar = self.groupBox_menu.addMenu(QIcon(self.Multiplexar_ico), '&Menú Multiplexar')
        self.Multiplexar.setStyleSheet('background-color: #cc9999; color: blue, ; selection-background-color: #8a4848')

        self.Multiplexar.addSeparator()
        self.Multiplexar.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.Multiplexar.addSeparator()
        self.Multiplexar.addSeparator()

        self.Quitar_Sonido_1 = Path.resource_path('Ico\\mix.png')
        self.Quitar_Sonido = QAction(QIcon(self.Quitar_Sonido_1), '&Multiplexar de 1 a 6 Videos, Forma #1?', self)

        self.Quitar_Sonido.setStatusTip('Quitar Sonido') 
        self.Quitar_Sonido.triggered.connect(lambda: Array_Clips.Clip_Mix_Vids_1(self)) 
        self.Multiplexar.addAction(self.Quitar_Sonido)

        self.Multiplexar.addSeparator()
        self.Multiplexar.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.Multiplexar.addSeparator()
        self.Multiplexar.addSeparator()

        self.Agregar_Sonido_1 = Path.resource_path('Ico\\mix.png')
        self.Agregar_Sonido = QAction(QIcon(self.Agregar_Sonido_1), '&Multiplexar de 1 a 4 Videos, Forma #2?', self)

        self.Agregar_Sonido.setStatusTip('Agregar Sonido') 
        self.Agregar_Sonido.triggered.connect(lambda: Array_Clips.Clip_Mix_Vids_2(self)) 
        self.Multiplexar.addAction(self.Agregar_Sonido)

        self.Multiplexar.addSeparator()
        self.Multiplexar.addSeparator()

        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        self.Ms_Bienvenida0 = Path.resource_path('Ico\\OK.png')
        Ms_Bienvenida = QAction(QIcon(self.Ms_Bienvenida0), '&Mensaje de Bienvenida', self)
        Ms_Bienvenida.setShortcut('I')

        Ms_Bienvenida.setStatusTip("Ms_Bienvenida")
        Ms_Bienvenida.triggered.connect(lambda: Message_Box.Ms_Info(self))
        self.groupBox_menu.addAction(Ms_Bienvenida)
        
        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        self.Ms_Podremos_Realizar0 = Path.resource_path('Ico\\OK.png')
        Ms_Podremos_Realizar = QAction(QIcon(self.Ms_Podremos_Realizar0), '&Loque Podremos Realizar', self)
        Ms_Podremos_Realizar.setShortcut('F1')

        Ms_Podremos_Realizar.setStatusTip("Ms_Podremos_Realizar")
        Ms_Podremos_Realizar.triggered.connect(lambda: VideoPlayer.show_app_info(self)) 
        self.groupBox_menu.addAction(Ms_Podremos_Realizar) 
        
        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        self.Exit_file = Path.resource_path('Ico\\Salir.png')
        Exit_action = QAction(QIcon(self.Exit_file), '&Exit', self)
        Exit_action.setShortcut('Escape')

        Exit_action.setStatusTip("Exit App")
        Exit_action.triggered.connect(app.quit) 
        self.groupBox_menu.addAction(Exit_action) 
        
        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        self.groupBox_menu.popup(QCursor.pos())

##======================================================================================
##======================================================================================

class app_info(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        #-> Forma Uno (1)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        #-> Forma Dos (2)
        #self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)

        self.setWindowTitle("✨ Información del Software ✨")
        self.setFixedSize(520, 420)
        self.setModal(True)

        self.init_ui()

    def init_ui(self):

        print("\n============================================")
        print("➜ Innicio: Podremos Realizar en la App...")
        print("============================================")

        layout = QVBoxLayout(self)

        # --- Título ---
        title = QLabel("✨ Editor de Video -v9 ✨")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 16pt;
                font-weight: bold;
                color: #00A3FF;
            }
        """)
        layout.addWidget(title)

        # --- Texto informativo ---
        info_text = QTextEdit()
        info_text.setLineWrapMode(QTextEdit.NoWrap)
        info_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        info_text.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        info_text.setReadOnly(True)
        info_text.setText("""
📌 Este Soft esta Desarrollado, muy Minimalista, Pero, esta enfocado a Editar Videos, y con este Soft, podremos:\
\n\n01) ⭐ Ver en tiempo Real, el Video a ser tratado, como Ver como quedo ya Tradado.\
\n02) ⭐ En el Btn. Play, Podremos: -Darle Play y Puse.\
\n03) ⭐ En el Btn. Recortar Innicio, Podremos: -Recortarle el Innicio, el tiempo que deseemos por medio de la barrita de Trancición del tiempo del Video.\
\n04) ⭐ En el Btn. Recortar Final, Podremos: -Recortarle el Final, el tiempo que deseemos por medio de la barrita de Trancición del tiempo del Video.\
\n05) ⭐ En el Btn. Unir Videos, Podremos: -Unir Videos (Concatenar | Fusionar), la cantidad que deseemos.\
\n06) ⭐ En el Btn. de Converted To MP3||WAV, Podremos: -Comvertir de MP4 a MP3, WAV, u otros.\
\n07) ⭐ Con la Opción, en el Menú, Converted To MP4, Podremos: -Conver Videos de distintos Formatos a: -|- MP4, AVI, MOV, WMV, OGV,WEBM.\
\n08) ⭐ Con el Submenú Sonido, Podremos: -Agregar o Quitar Sonido a cualquier Video.\
\n09) ⭐ Con el Submenú Video Brillo, Podremos: -Ajustar el Vrillo en --Poco, Medio, Alto Brillo--\
\n10) ⭐ Con el Submenú Efecto Colores, Podremos: -Dar el efecto, de Vición Nocturna, Vición Calorifica Etc. Etc. Etc. (6-EFECTOS)\
\n11) ⭐ Con el Submenú Marca de Agua, Podremos: -Colocar cualquier Imagen como marca de Agua, en 9 pociciónes Distintas.\
\n12) ⭐ Con el Submenú Correccion de Color, Podremos: -Bien este Submenú, es solamente por si el Video esta Demaciado Obscuro, y lo queremos aclarar un poco.\
\n13) ⭐ Con el Submenú Resolucion de Video, Podremos: -Cambiar la Resolución del Video es decir, que si el Video es 360sd (La más pequeña), podremos Cambiarla hasta 8K\
\n14) ⭐ Con el Submenú de Rotación de Video, Podremos: -Rotar el Video a Nuestra Necesidad.\
\n15) ⭐ Con el Submenú de Crear Video de Imagenes, Podremos: -Bien como su nombre lo indica, podremmos crear un Video, a partir de Imagenes, no importando la Cantidad de Img´s.\
\n16) ⭐ Con el Submenú de Multiplexar Videos?, Podremos: -Multiplexar Varios Videos de 1n Video a 6 Videos y no más.\
\n17) ⭐ Con la Opción, en el Menú, Mensaje de Bienvenida, Veremos: -El Mensajito del Innicio.\
\n\n===================  TECLAS DE ATAJO  ===================\
\n18) ⭐ Con la Tecla (I), Veremos el Mensajito de Información.- \
\n19) ⭐ Con la Tecla (F1), Veremos este Cuadro de Alluda.- \
\n20) ⭐ Con la Tecla (ESC [Escape]), Cerraremos el Soft.- \
\n\nDesarrollado por:  Cristian M. Velilz Cano\
""")

        info_text.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #F1F1F1;
                border: 1px solid #5A5A5A;
                border-radius: 5px;
                padding: 8px;
                font-size: 10.5pt;
            }
        """)
        layout.addWidget(info_text)

        # --- Botón cerrar ---
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        close_button.setFixedHeight(32)
        layout.addWidget(close_button)

##=========================================================================================================
##=========================================================================================================

if __name__ == '__main__':

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    traductor = QTranslator(app)
    lugar = QLocale.system().name()
    path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    traductor.load("qtbase_%s" % lugar, path)
    app.installTranslator(traductor)

    
    player = VideoPlayer()
    sys.exit(app.exec_())

##=========================================================================================================
##=========================================================================================================

'''
EDICIÓN DE VIDEO CON PYTHON: CREACIÓN DE VIDEOS DE PANTALLA DIVIDIDA, CON ‘MOVIEPY’.
programacion python 80889555 algoritmos, computer vission, ffmpeg, funciones en python, imagen, 
programación en python, programacion, python, software, Como muchos ya sabréis, ‘moviepy‘ 
es una librería que nos permite la generación y edición de archivos de video, la cual podremos 
instalar en nuestro equipo utilizando el comando ‘pip install moviepy‘:
 
En el Proximo, vamos a ver como podemos generar, de forma sencilla, un vídeo en el que, 
mediante la división de pantalla, muestre más de un vídeo a la vez. Para ello, empezaremos importando 
la propia librería ‘moviepy‘ junto a los módulos ‘VideoFileClip‘ y ‘clips_array‘:
 
Una vez importados los recursos con los que vamos a trabajar, podemos iniciar la creación de nuestro 
vídeo combinado usando el método «VideoFileClip()» al que pasaremos, para cada vídeo, el 
nombre del archivo en cuestión, especificando a su vez (usando el método «subclip«) el intervalo de 
tiempo en segundos que queremos seleccionar (en nuestro ejemplo, tomaremos los 4 primeros segundos de 
cada uno):
 
Una vez cargados los vídeos con los que vamos a trabajar (4 en este caso) utilizaremos «clips_array()» 
para especificar los videos que vamos a mostrar en el resultado, introduciendo estos en formato array 
tal y como se muestra a continuación:
 
Finalmente, una vez definido el contenido de nuestro futuro vídeo (que hemos almacenado en la 
variable «comb1»), pasaremos a crear nuestro vídeo, que mediante el método «write_videofile()»
(al que pasaremos el nombre del nuevo vídeo) iniciando un proceso cuya duración dependerá 
naturalmente del tamaño y duración de los videos seleccionados:
 
OUTPUT:
 
Como se ve, en este primer ensayo hemos tomado únicamente los dos primeros videos de los 4 que 
hemos cargado. No obstante, podemos utilizar «clips_array()» tanto para añadir más videos 
(lo que supondrá también que el tiempo de generación aumente) como para definir la estructura en la 
que estos se presentarán:
 
OUTPUT:
 
Al mismo tiempo ‘moviepy‘ nos permite establecer márgenes entre los videos compartidos, a la hora de cargar 
estos, usando el método ‘margin()‘ pasándole el grosor que queremos para dicho margen:
 
OUTPUT:
 
Se muestra la presencia de un margen para dividir los vídeos en el resultado final. A su vez, una vez 
que hayamos terminado, deberemos proceder a cerrar los videos abiertos:
 '''

##=========================================================================================================
##=========================================================================================================