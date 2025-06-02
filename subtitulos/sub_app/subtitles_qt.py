from opensubtitlescom import OpenSubtitles
import subprocess
import tempfile
import ffmpeg
import json
import sys
import os
import re

from datetime import datetime, timedelta
from functools import partial
from PySide6 import *
import random

from deep_translator import GoogleTranslator
from langdetect import detect
import googletrans

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import QUrl, QTime
from PySide6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMainWindow,
                               QSpacerItem, QSizePolicy, QFileDialog, QMessageBox, QBoxLayout, QProgressDialog,
                               QCheckBox, QStackedLayout, QListWidget, QLineEdit, QComboBox, QDoubleSpinBox, QGridLayout, QSpinBox)

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.dict_subs = {}
        self.setWindowTitle('Subtitles Editor')
        self.setWindowIcon(QtGui.QIcon('./icons/cc.ico'))
        self.setFixedSize(1500,700)


        # ------------------------ widgets
        self.widget_variables()

        # ------------------------ layouts
        self.widget_layout()

        # ------------------------ actions
        self.widget_actions()

        # ------------------------ format
        self.format_widgets_gui()

    def widget_variables(self):
        self.video_counter = QLabel("00:00")
        self.btn_load_video = QPushButton("Load Video")
        self.audioOutput = QAudioOutput(self)
        self.mediaPlayer = QMediaPlayer(self)
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        self.videoWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.videoWidget.setFixedSize(500, 300)
        self.playButton = QPushButton()
        self.playButton.setIcon(QIcon('./icons/play.png'))
        self.playButton.setEnabled(False)
        self.pauseButton = QPushButton()
        self.pauseButton.setIcon(QIcon('./icons/pause.png'))
        self.pauseButton.setEnabled(False)
        self.backButton = QPushButton()
        self.backButton.setIcon(QIcon('./icons/back.png'))
        self.backButton.setEnabled(False)
        self.forwardButton = QPushButton()
        self.forwardButton.setIcon(QIcon('./icons/next.png'))
        self.forwardButton.setEnabled(True)
        self.reloadButton = QPushButton()
        self.reloadButton.setIcon(QIcon('./icons/reboot.png'))
        self.reloadButton.setEnabled(False)

        self.curr_title = QLabel("Current Subtitles", alignment=QtCore.Qt.AlignCenter)
        self.curr_subs = QListWidget()

        self.btn_use_subs = QPushButton('Use')
        self.btn_use_subs.setEnabled(False)
        self.btn_del_subs = QPushButton("Delete")
        self.btn_del_subs.setEnabled(False)
        self.btn_load_subs = QPushButton("Load Subtitles")
        self.btn_down_subs = QPushButton("Download")
        self.btn_down_subs.setEnabled(False)

        self.txt_search = QLineEdit()
        self.txt_search.setEnabled(False)
        self.lang_lst = QComboBox()
        self.save_cred = QCheckBox('save credentials')
        self.btn_search = QPushButton("Search")
        self.btn_search.setEnabled(False)
        self.lst_subs = QListWidget()
        self.lst_subs.setMaximumHeight(0)
        message_ = ('Create an '
                    '<a href="https://kb.synology.com/en-ca/DSM/tutorial/How_to_apply_for_API_key_from_OpenSubtitles">'
                    'OpenSubtitles.com</a> account <br> to use the online subtitle search <br>')
        self.opensub_message = QLabel(message_, alignment=QtCore.Qt.AlignCenter)
        self.opensub_message.setOpenExternalLinks(True)

        self.txt_username = QLineEdit(alignment=QtCore.Qt.AlignCenter)
        self.txt_username.setPlaceholderText("username")
        self.txt_username.setFixedSize(150, 30)
        self.txt_password = QLineEdit(alignment=QtCore.Qt.AlignCenter)
        self.txt_password.setPlaceholderText("password")
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setFixedSize(150, 30)
        self.txt_token = QLineEdit(alignment=QtCore.Qt.AlignCenter)
        self.txt_token.setPlaceholderText("token")
        self.txt_token.setEchoMode(QLineEdit.Password)
        self.txt_token.setFixedSize(150, 30)
        self.btn_login = QPushButton('Log-In')
        self.btn_login.setFixedSize(150, 50)
        try:
            with open('./cred.json', 'r') as f:
                creds = json.load(f)
                self.txt_username.setText(creds['username'])
                self.txt_password.setText(creds['password'])
                self.txt_token.setText(creds['token'])
            f.close()
        except: pass

        self.encode_list = QComboBox()
        self.encode_list.addItems(['utf-8', 'latin1'])
        self.separator1 = QLabel("-" * 50, alignment=QtCore.Qt.AlignCenter)

        self.example_id = QSpinBox()
        self.example_i = QLabel("Original Format Subtitle", alignment=QtCore.Qt.AlignCenter)
        self.example_i.setFixedSize(200, 100)
        self.example_f = QLabel("Edited Format Subtitle", alignment=QtCore.Qt.AlignCenter)
        self.example_f.setFixedSize(200, 100)

        self.lang_orig = QComboBox()
        self.orig__ = QLabel("--->")
        self.btn_translate = QPushButton("Translate")
        self.btn_translate.setEnabled(False)
        self.lang_dest = QComboBox()
        self.dest__ = QLabel("<---")
        self.separator2 = QLabel("-" * 50, alignment=QtCore.Qt.AlignCenter)

        self.title_time = QLabel("Change time")
        self.time_values = QDoubleSpinBox()
        self.separator3 = QLabel("-" * 50, alignment=QtCore.Qt.AlignCenter)
        self.btn_save_subs = QPushButton("Save Subs")
        self.btn_save_subs.setEnabled(False)

        self.title_sub = QLineEdit()
        self.title_sub.setPlaceholderText("Title Name")
        self.title_sub.setEnabled(False)

        self.btn_add_subs = QPushButton("Add Subs")
        self.btn_add_subs.setEnabled(False)

        self.btn_save_video = QPushButton("Save Video")
        self.btn_save_video.setEnabled(False)

    def widget_layout(self):
        self.layout = QGridLayout(self)

        # ------------------------------------------------------------------------------ Layout for video player
        lyt_video_v = QVBoxLayout()
        lyt_video_v.addWidget(self.btn_load_video, alignment=QtCore.Qt.AlignCenter)
        lyt_video_v.addWidget(self.videoWidget, alignment=QtCore.Qt.AlignCenter)
        lyt_video_v.addWidget(self.video_counter, alignment=QtCore.Qt.AlignCenter)
        self.layout.addLayout(lyt_video_v, 1, 0, 2, 1)
        # -
        lyt_video_b = QHBoxLayout()
        lyt_video_b.addWidget(self.playButton, alignment=QtCore.Qt.AlignTop)
        lyt_video_b.addWidget(self.pauseButton, alignment=QtCore.Qt.AlignTop)
        lyt_video_b.addWidget(self.backButton, alignment=QtCore.Qt.AlignTop)
        lyt_video_b.addWidget(self.forwardButton, alignment=QtCore.Qt.AlignTop)
        lyt_video_b.addWidget(self.reloadButton, alignment=QtCore.Qt.AlignTop)
        #-
        self.layout.addLayout(lyt_video_b, 3, 0, 1, 1)
        self.layout.addWidget(self.btn_save_video, 3,0, alignment=QtCore.Qt.AlignCenter)
        # ------------------------------------------------------------------------------ layout subtitles selection

        lyt_subs_s = QHBoxLayout()
        # -
        lyt_currsubs = QVBoxLayout()
        lyt_currsubs.addWidget(self.curr_title)
        lyt_currsubs.addWidget(self.curr_subs)
        lyt_subs_s.addLayout(lyt_currsubs)
        # -
        lyt_manual = QVBoxLayout()
        lyt_manual.addWidget(self.btn_use_subs)
        lyt_manual.addWidget(self.btn_del_subs)
        lyt_manual.addWidget(self.btn_down_subs)
        lyt_manual.addWidget(self.btn_load_subs)
        lyt_subs_s.addLayout(lyt_manual)
        # -
        lyt_opensub = QVBoxLayout()
        #-
        lyt_search = QHBoxLayout()
        lyt_search.addWidget(self.txt_search)
        lyt_search.addWidget(self.lang_lst)
        lyt_search.addWidget(self.btn_search)
        lyt_opensub.addLayout(lyt_search)
        # -
        lyt_subs_mssg = QVBoxLayout()
        lyt_subs_mssg.addWidget(self.lst_subs)
        lyt_subs_mssg.addWidget(self.opensub_message)
        lyt_subs_mssg.addWidget(self.txt_username, alignment=QtCore.Qt.AlignCenter)
        lyt_subs_mssg.addWidget(self.txt_password, alignment=QtCore.Qt.AlignCenter)
        lyt_subs_mssg.addWidget(self.txt_token, alignment=QtCore.Qt.AlignCenter)
        lyt_opensub.addLayout(lyt_subs_mssg)
        lyt_btn_li = QHBoxLayout()
        lyt_btn_li.addWidget(self.btn_login, alignment=QtCore.Qt.AlignRight)
        lyt_btn_li.addWidget(self.save_cred, alignment=QtCore.Qt.AlignCenter)
        lyt_opensub.addLayout(lyt_btn_li)
        # -
        lyt_subs_s.addLayout(lyt_opensub)
        #-
        self.layout.addLayout(lyt_subs_s, 0, 2, 2, 1)

        # ------------------------------------------------------------------------------ layout examples edition
        lyt_subs_e = QHBoxLayout()
        # -
        lyt_subs_e.addWidget(self.example_i)
        # -
        layout_middle = QVBoxLayout()
        layout_middle.addWidget(self.separator1)
        layout_middle.addWidget(self.encode_list, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.example_id, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.lang_orig, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.orig__, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.btn_translate, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.dest__, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.lang_dest, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.separator2)
        layout_middle.addWidget(self.title_time, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.time_values, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.separator3)
        lyt_subs_e.addLayout(layout_middle)
        #-
        lyt_btns = QHBoxLayout()
        lyt_btns.addWidget(self.btn_save_subs, alignment=QtCore.Qt.AlignRight)
        lyt_btns.addWidget(self.title_sub, alignment=QtCore.Qt.AlignRight)
        lyt_btns.addWidget(self.btn_add_subs, alignment=QtCore.Qt.AlignRight)
        layout_middle.addLayout(lyt_btns)
        # -
        lyt_subs_e.addWidget(self.example_f)
        # -
        self.layout.addLayout(lyt_subs_e, 2,2, 2,3)

    def widget_actions(self):

        self.mediaPlayer.positionChanged.connect(self.update_timeCounter)

        self.btn_load_video.clicked.connect(self.LoadVideo)
        self.playButton.clicked.connect(self.play_video)
        self.pauseButton.clicked.connect(self.pause_video)
        self.backButton.clicked.connect(self.rewind_10s)
        self.forwardButton.clicked.connect(self.forward_10s)
        self.reloadButton.clicked.connect(self.reload_video)

        self.btn_use_subs.clicked.connect(self.use_subs_btn)
        self.btn_down_subs.clicked.connect(self.download_subs_btn)
        self.btn_del_subs.clicked.connect(self.delete_subs_btn)
        self.btn_load_subs.clicked.connect(self.load_subs_btn)

        self.btn_search.clicked.connect(self.search_subs)
        self.btn_login.clicked.connect(self.login_account)

        self.encode_list.currentIndexChanged.connect(self.enconde_subs)

        self.example_id.valueChanged.connect(self.update_example)
        self.time_values.valueChanged.connect(self.update_time)
        self.btn_save_subs.clicked.connect(self.save_srt)
        self.btn_translate.clicked.connect(self.translate_text)

        self.btn_save_video.clicked.connect(self.save_video)
        self.btn_add_subs.clicked.connect(self.add_subs_function)

    def format_widgets_gui(self):

        self.btn_load_video.setStyleSheet("""
            QPushButton {
                background-color: #001f9c;  
                color: white;                
                border-radius: 10px;         
                font-size: 16px;            
                padding: 5px;
                width: 400px;
            }

            QPushButton:hover {
                background-color: #00135c;
                color:            white;
                border: 2px solid black;
            }

            QPushButton:pressed {
                background-color: white;
                color:            black;
                border: 2px solid black;
            }
        """)

        self.btn_save_video.setStyleSheet("""
            QPushButton {
                background-color: #001f9c;  
                color: white;                
                border-radius: 10px;         
                font-size: 16px;            
                padding: 5px;
                width: 400px;
            }

            QPushButton:hover {
                background-color: #00135c;
                color:            white;
                border: 2px solid black;
            }

            QPushButton:pressed {
                background-color: white;
                color:            black;
                border: 2px solid black;
            }
            
            QPushButton:disabled {
                background-color: #cccccc;
                color: gray;
                border: 2px solid black;
            }
        """)

        self.btn_down_subs.setStyleSheet("""
            QPushButton {
                background-color: #001f9c;  
                color: white;                
                border-radius: 10px;         
                font-size: 16px;            
                padding: 5px;
                width: 400px;
            }

            QPushButton:hover {
                background-color: #00135c;
                color:            white;
                border: 2px solid black;
            }

            QPushButton:pressed {
                background-color: white;
                color:            black;
                border: 2px solid black;
            }
            
            QPushButton:disabled {
                background-color: #cccccc;
                color: gray;
                border: 2px solid black;
            }
        """)

        self.curr_subs.setStyleSheet("""
            QListWidget {
                color: white;              
                font-size: 14px;
                padding: 5px;
            }

            QListWidget::item {
                background-color: #002fa7;     /* Color base */
                border-radius:    5px;         /* Bordes redondeados */
                padding:          8px;
                margin:           5px;         /* Espaciado entre elementos */
                border: 1px solid transparent; /* Borde inicial */
            }

            QListWidget::item:hover {
                background-color: #ffcc80; /* Color al pasar el mouse */
                color:            black;
                border: 1px solid #ff9800; /* Borde resaltado */
            }

            QListWidget::item:selected {
                background-color: #ff9800; /* Fondo de selección */
                color:            black;
                font-weight:      bold;
                border: 2px solid #ff5722; /* Borde de selección */
            }

            QListWidget::item:selected:!active {
                background-color: #ffa726;
                color:            black;
            }
        """)

        self.btn_use_subs.setStyleSheet("""
            QPushButton {
                background-color: #10194f;  
                color: white;              
                border-radius: 10px;       
                font-size: 16px;            
                weight: 10px;
                padding: 7px;

            }

            QPushButton:hover {
                background-color: black;
                color:            white;
                border:           2px solid white;
            }

            QPushButton:pressed {
                background-color: black;
                color:            white;
                border: 2px solid white;
            }
            
            QPushButton:disabled {
                background-color: #cccccc;
                color: gray;
                border: 2px solid black;
            }
        """)

        self.btn_del_subs.setStyleSheet("""
            QPushButton {
                background-color: #10194f;  
                color:            white;    
                border-radius:    10px;     
                font-size:        16px;    
                weight:           10px;
                padding: 7px;

            }

            QPushButton:hover {
                background-color: black;
                color:            white;
                border:           2px solid white;
            }

            QPushButton:pressed {
                background-color: black;
                color:            white;
                border: 2px solid white;
            }
            
            QPushButton:disabled {
                background-color: #cccccc;
                color: gray;
                border: 2px solid black;
            }
        """)

        self.btn_down_subs.setStyleSheet("""
            QPushButton {
                background-color: #44104f;  
                color:            white;  
                border-radius:    10px;    
                font-size:        16px;     
                weight:           10px;
                padding: 7px;

            }

            QPushButton:hover {
                background-color: black;
                color:            white;
                border:           2px solid white;
            }

            QPushButton:pressed {
                background-color: black;
                color:            white;
                border: 2px solid white;
            }

            QPushButton:disabled {
                background-color: #cccccc;
                color: gray;
                border: 2px solid black;
            }
        """)

        self.btn_load_subs.setStyleSheet("""
            QPushButton {
                background-color: #001f9c;  
                color: white;                
                border-radius: 10px;         
                font-size: 16px;            
                padding: 7px;
            }

            QPushButton:hover {
                background-color: black;
                color:            white;
                border: 2px solid white;
            }

            QPushButton:pressed {
                background-color: white;
                color:            black;
                border: 2px solid black;
            }
        """)

        self.btn_search.setStyleSheet("""
            QPushButton {
                background-color: #44104f;  
                color: white;                
                border-radius: 10px;         
                font-size: 16px;            
                padding: 7px;
            }

            QPushButton:hover {
                background-color: black;
                color:            white;
                border: 2px solid white;
            }

            QPushButton:pressed {
                background-color: white;
                color:            black;
                border: 2px solid black;
            }
            
            QPushButton:disabled {
                background-color: #cccccc;
                color: gray;
                border: 2px solid black;
            }
        """)

        self.lst_subs.setStyleSheet("""
            QListWidget {
                color: white;              
                font-size: 14px;
                padding: 2px;
            }

            QListWidget::item {
                border-radius:    5px;         /* Bordes redondeados */
                padding:          8px;
                margin:           2px;         /* Espaciado entre elementos */
                border: 1px solid transparent; /* Borde inicial */
            }

            QListWidget::item:hover {
                background-color: #ffcc80; /* Color al pasar el mouse */
                color:            black;
                border: 1px solid #ff9800; /* Borde resaltado */
            }

            QListWidget::item:selected {
                background-color: #ff9800; /* Fondo de selección */
                color:            black;
                font-weight:      bold;
                border: 2px solid #ff5722; /* Borde de selección */
            }

            QListWidget::item:selected:!active {
                background-color: #ffa726;
                color:            black;
            }
        """)

        self.lang_lst.setStyleSheet("""
            QComboBox {
                width: 20px;
            }
        """)

        self.btn_translate.setStyleSheet("""
            QPushButton {
                background-color: #4f4f00;  
                color: white;                
                border-radius: 10px;         
                font-size: 16px;            
                padding: 10px;
                width: 100px;
            }

            QPushButton:hover {
                background-color: #3e3e03;
                color:            white;
                border: 2px solid white;
            }

            QPushButton:pressed {
                background-color: white;
                color:            black;
                border: 2px solid black;
            }
            
            QPushButton:disabled {
                background-color: #cccccc;
                color: gray;
                border: 2px solid black;
            }
        """)

        self.btn_save_subs.setStyleSheet("""
            QPushButton {
                background-color: #4f4f00;  
                color: white;                
                border-radius: 10px;         
                font-size: 16px;            
                padding: 10;
                width: 100px;

            }

            QPushButton:hover {
                background-color: #3e3e03;
                color:            white;
                border: 2px solid white;
            }

            QPushButton:pressed {
                background-color: white;
                color:            black;
                border: 2px solid black;
            }
            
            QPushButton:disabled {
                background-color: #cccccc;
                color: gray;
                border: 2px solid black;
            }
        """)

        self.btn_add_subs.setStyleSheet("""
            QPushButton {
                background-color: #4f4f00;  
                color: white;                
                border-radius: 10px;         
                font-size: 16px;            
                padding: 10px;
                width: 100px;

            }

            QPushButton:hover {
                background-color: #3e3e03;
                color:            white;
                border: 2px solid white;
            }

            QPushButton:pressed {
                background-color: white;
                color:            black;
                border: 2px solid black;
            }
                    
            QPushButton:disabled {
                background-color: #cccccc;
                color: gray;
                border: 2px solid black;
            }
                """)

        self.title_sub.setStyleSheet("""
            QLineEdit {
                width: 150px;
            }
        """)

        self.lang_orig.setStyleSheet("""
            QComboBox {
                width: 100px;
            }
        """)

        self.lang_dest.setStyleSheet("""
            QComboBox {
                width: 100px;
            }
        """)

        self.txt_username.setStyleSheet("""
            QLineEdit {
                width: 200px;
            }
        """)

        self.txt_password.setStyleSheet("""
            QLineEdit {
                width: 20px;
            }
        """)

        self.txt_token.setStyleSheet("""
            QLineEdit {
                width: 50px;
            }
        """)

        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #44104f;  
                color: white;          
                border-radius: 15px;         
                padding: 2px;
                width: 20px;
            }

            QPushButton:hover {
                background-color: black;
                color:            white;
                border: 2px solid white;
            }

            QPushButton:pressed {
                background-color: white;
                color:            black;
                border: 2px solid black;
            }

        """)

    def clear_widgets(self):

        self.curr_subs.clear()

        return

    @QtCore.Slot()
    def login_account(self):
        username = self.txt_username.text()
        password = self.txt_password.text()
        token = self.txt_token.text()

        try:
            self.subtitles = OpenSubtitles("MyApp v1.0.0", token)
            self.subtitles.login(username, password)
            self.notifications('LogIn','Successfull Log-In')
        except:
            self.notifications('LogIn Error','Verify Credentials')
            return

        if self.save_cred.isChecked():
            json_f = './cred.json'
            if os.path.exists(json_f): os.remove(json_f)
            data = {'username': username, 'password': password, 'token': token}
            with open(json_f, 'w+') as f: json.dump(data, f)
            subprocess.run(['attrib', '+h', json_f], shell=True)

        self.txt_search.setPlaceholderText("Find by keywords: titles, years, format, etc...")
        self.btn_search.setEnabled(True)
        self.txt_search.setEnabled(True)

        langs = sorted([i for i in googletrans.LANGUAGES])
        id_es = langs.index('es')
        self.lang_lst.addItems(langs)
        self.lang_lst.setCurrentIndex(id_es)
        self.opensub_message.hide()
        self.txt_username.hide()
        self.txt_password.hide()
        self.txt_token.hide()
        self.btn_login.hide()
        self.save_cred.hide()

        self.lst_subs.setMaximumHeight(200)
        self.lst_subs.setMaximumWidth(500)

    @QtCore.Slot()
    def LoadVideo(self):

        self.videoFile, _ = QFileDialog.getOpenFileName(self, "Abrir Video", "", "Videos (*.mp4 *.avi *.mkv)")

        if self.videoFile:
            self.clear_widgets()
            self.wait_message('Loading Video...')
            self.file_path = QUrl.fromLocalFile(self.videoFile)
            self.mediaPlayer.setSource(self.file_path)
            self.playButton.setEnabled(True)
            self.pauseButton.setEnabled(True)
            self.forwardButton.setEnabled(True)
            self.backButton.setEnabled(True)
            self.reloadButton.setEnabled(True)
            self.btn_use_subs.setEnabled(True)
            self.btn_del_subs.setEnabled(True)
        else:
            return

        dict_subs = self.dict_subs
        full_path = self.file_path.toLocalFile()
        local_path = full_path.split('/')[:-1]
        file_name = full_path.split('/')[-1]
        file_extn = file_name.split('.')[-1]

        res = ffmpeg.probe(full_path, v='error', select_streams='s', show_entries='stream=index,codec_name')
        for i, row in enumerate(res['streams']):
            sub_i = row['tags']
            try:
                self.curr_subs.addItems([sub_i['title']])
                paragraph = self.get_internal_subs(i)
                dict_subs[i] = paragraph
            except:
                continue
        self.dict_subs = dict_subs
        self.progress_dialog.close()

    @QtCore.Slot()
    def update_timeCounter(self, position):
        time = QTime(0, 0).addMSecs(position)
        self.video_counter.setText(time.toString("hh:mm:ss.zzz"))

    @QtCore.Slot()
    def play_video(self):
        self.mediaPlayer.play()

    @QtCore.Slot()
    def pause_video(self):
        self.mediaPlayer.pause()

    @QtCore.Slot()
    def rewind_10s(self):

        curr_id = self.example_id.value()
        new_val = int(curr_id)-1
        self.example_id.setValue(new_val)
        clean_pg = [i for i in self.new_paragraphs if i != '\n']
        id_ex = clean_pg[new_val-1]

        time_ = re.search('\d+\:\d+\:\d+\,\d+', id_ex)
        time_ = time_[0]
        all_time = time_.split(':')
        hours = int(all_time[0])
        minutes = int(all_time[1])
        seconds = int(all_time[2].split(',')[0])
        milisds = int(all_time[2].split(',')[1])
        curr_pos = ((hours * 3600) + (minutes * 60) + seconds) * 1000
        curr_pos += milisds
        self.mediaPlayer.setPosition(curr_pos)

    @QtCore.Slot()
    def forward_10s(self):

        curr_id = self.example_id.value()
        new_val = int(curr_id)+1
        self.example_id.setValue(new_val)

        clean_pg = [i for i in self.new_paragraphs if i != '\n']
        id_ex = clean_pg[self.example_id.value()-1]

        time_ = re.search('\d+\:\d+\:\d+\,\d+', id_ex)
        time_ = time_[0]
        all_time = time_.split(':')
        hours   = int(all_time[0])
        minutes = int(all_time[1])
        seconds = int(all_time[2].split(',')[0])
        milisds = int(all_time[2].split(',')[1])
        curr_pos = ((hours * 3600) + (minutes * 60) + seconds) * 1000
        curr_pos += milisds
        self.mediaPlayer.setPosition(curr_pos)

    @QtCore.Slot()
    def reload_video(self):
        self.mediaPlayer.setPosition(0)

    @QtCore.Slot()
    def wait_message(self, message):
        self.progress_dialog = QProgressDialog("Please wait, process is running...", None, 0, 0, self)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.show()
        self.progress_dialog.setValue(0)

    def notifications(self, title, message):
        self.wait_msg = QMessageBox(self)
        self.wait_msg.setWindowTitle(title)
        self.wait_msg.setIcon(QMessageBox.Information)
        self.wait_msg.setText(message)

        self.wait_msg.setStandardButtons(QMessageBox.Ok)

        #self.wait_msg.setStyleSheet("QLabel{min-width: 150px; min-height: 50px;}")
        #self.wait_msg.setStandardButtons(QMessageBox.NoButton)
        self.wait_msg.setModal(True)
        #self.wait_msg.show()
        self.wait_msg.exec_()

    def confirmation_message(self):
        response = QMessageBox.question(self,
                                        "Confirmation",
                                        "Continue with this action?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                        )
        if response == QMessageBox.StandardButton.Yes: return 1
        else:                                          return 0

    @QtCore.Slot()
    def add_subs_function(self):
        curr_name = self.title_sub.text()
        self.curr_subs.addItems([curr_name])

        curr_paragraph = self.new_paragraphs
        n = len(self.dict_subs)
        self.dict_subs[n] = curr_paragraph

        self.btn_save_video.setEnabled(True)

    def search_subs(self):
        val_search = self.txt_search.text()
        if val_search == '': return
        response = self.subtitles.search(query=val_search, languages="es")

        r_json = response.to_json()
        json_str = r_json.rstrip(',')
        list_json = json.loads(json_str)

        self.lst_subs.clear()
        self.subs_id = {}
        self.response = response
        for id, movie_i in enumerate(list_json['data']):
            name = movie_i['file_name']
            self.subs_id[name] = id
            self.lst_subs.addItems([name])

        self.btn_down_subs.setEnabled(True)

    def timedelta_format(self, td):
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        milliseconds = td.microseconds // 1000
        return f'{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}'

    def get_internal_subs(self, id):
        local_path = self.file_path.toLocalFile()
        ffmpeg_command = ['ffmpeg', '-i', local_path, '-map', f'0:s:{id}', '-f', 'srt', '-']
        result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        subtitles_text = result.stdout
        paragraphs = []
        pg_i = ''
        for p in subtitles_text.split('\n'):
            pg_i += (p + '\n')
            if p == '':
                paragraphs.append(pg_i)
                pg_i = ''
        return paragraphs

    @QtCore.Slot()
    def use_subs_btn(self):
        curr_id = self.curr_subs.currentRow()
        paragraphs = self.dict_subs[curr_id]
        self.paragraphs = paragraphs
        self.new_paragraphs = paragraphs
        self.update_example()
    @QtCore.Slot()
    def delete_subs_btn(self):
        selected_items = self.curr_subs.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            row = self.curr_subs.row(item)
            self.curr_subs.takeItem(row)
    @QtCore.Slot()
    def download_subs_btn(self):
        dict_id = self.subs_id
        curr_val = self.lst_subs.currentItem()
        curr_val = curr_val.text()
        curr_id = dict_id[curr_val]
        subtitles = self.subtitles.download_and_parse(self.response.data[curr_id])
        paragraphs = []
        for sub_i in subtitles:
            row_i = ''
            start_time = self.timedelta_format(sub_i.start)
            end_time = self.timedelta_format(sub_i.end)
            row_i += f"{sub_i.index}\n"
            row_i += f"{start_time} --> {end_time}\n"
            row_i += f"{sub_i.content}\n\n"
            paragraphs.append(row_i)

        self.example_i.setText(paragraphs[self.example_id.value()-1])
        self.paragraphs = paragraphs
        self.new_paragraphs = paragraphs
        self.example_id.setRange(1, len(paragraphs))
        self.example_id.setValue(1)
        self.update_example()
    @QtCore.Slot()
    def load_subs_btn(self):
        curr_ncode = self.encode_list.currentText()

        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self,
                                                   "Abrir Archivo de Texto","",
                                                   "Todos los Archivos (*)")
        if not file_path: return

        file = open(file_path, encoding=curr_ncode)
        content = file.read()
        paragraphs = []
        pg_i = ''
        for p in content.split('\n'):
            pg_i += (p+'\n')
            if p == '':
                paragraphs.append(pg_i)
                pg_i = ''

        self.example_i.setText(paragraphs[0])
        self.paragraphs = paragraphs
        self.new_paragraphs = paragraphs
        self.example_id.setRange(1, len(paragraphs))
        self.example_id.setValue(1)
        self.update_example()

    @QtCore.Slot()
    def enconde_subs(self):
        paragraph = self.paragraphs
        ncode = self.encode_list.currentText()

        all_ncoded = []
        for p_i in paragraph:
            p_i_ncoded = p_i.encode(ncode, errors='replace').decode(ncode)
            all_ncoded.append(p_i_ncoded)
        self.paragraphs = paragraph
        self.new_paragraphs = paragraph

    def update_time(self):
        def add_time(time, extra_time):
            row_time = datetime.strptime(time, "%H:%M:%S,%f")
            new_time = row_time + timedelta(seconds=float(extra_time))
            row = str(new_time.time())[:-3]
            row = row.replace('.',',')
            return row
        self.time_values.setRange(-1000.0, 1000.0)
        self.time_values.setDecimals(3)
        self.time_values.setSingleStep(1)

        new_paragraphs = []
        extra_time = self.time_values.value()
        for pg_i in self.paragraphs:
            npg_i = []
            pg_i = pg_i.split('\n')
            for val_pg in pg_i:
                if '-->' in val_pg:
                    times_vals = val_pg
                    init, fin = times_vals.split(' --> ')
                    try:
                        init = add_time(init, extra_time)
                        fin = add_time(fin, extra_time)
                    except: continue
                    times_vals = init + ' --> ' + fin
                    npg_i.append(times_vals)
                else:
                    npg_i.append(val_pg)
            new_paragraphs.append('\n'.join(npg_i))

        self.new_paragraphs = new_paragraphs
        self.update_example()

    @QtCore.Slot()
    def update_languajes(self):
        langs_dict = googletrans.LANGUAGES
        langs = [ i+' - '+langs_dict[i] for i in langs_dict]

        # --------------------------------------------- get only text without spec charac
        patron = r"\b[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+\b"
        new_txt = re.findall(patron, self.example_i.text())
        new_txt = ''.join(new_txt).lower()
        # ---------------------------------------------

        curr_lang = detect(new_txt)
        curr_lang = curr_lang+' - ' +langs_dict[curr_lang]
        try:    curr_idx = langs.index(curr_lang)
        except: curr_idx = 0
        spanish_id = 198

        self.lang_orig.addItems(langs)
        self.lang_orig.setCurrentIndex(curr_idx)
        self.lang_dest.addItems(langs)
        self.lang_dest.setCurrentIndex(spanish_id)
        self.btn_translate.setEnabled(True)

    @QtCore.Slot()
    def update_example(self):
        clean_pg = [i for i in self.paragraphs if i != '\n']
        id_ex = clean_pg[self.example_id.value()-1]
        self.example_i.setText(id_ex)

        clean_pg = [i for i in self.new_paragraphs if i != '\n']
        id_ex = clean_pg[self.example_id.value()-1]
        self.example_f.setText(id_ex)
        self.btn_save_subs.setEnabled(True)
        self.update_languajes()
        if self.videoFile:
            self.btn_add_subs.setEnabled(True)
            self.title_sub.setEnabled(True)

    @QtCore.Slot()
    def save_srt(self):
        plain_format = '\n'.join(self.new_paragraphs)
        options      = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar archivo de texto", '', "Text Files (*.srt);;All Files (*)", options=options)
        curr_ncode = self.encode_list.currentText()
        if file_name:
            with open(file_name, 'w', encoding=curr_ncode) as file: file.write(plain_format)

    @QtCore.Slot()
    def translate_text(self):

        r = self.confirmation_message()
        if r == 0: return

        self.wait_message('Transcribing subtitles...')

        dest = self.lang_dest.currentText()
        dest = dest.split(' ')[0]
        orig = self.lang_orig.currentText()
        orig = orig.split(' ')[0]
        trans_paragraphs = []

        for id, pr_i in enumerate(self.paragraphs):
            translated = GoogleTranslator(source=orig, target=dest).translate(pr_i)
            trans_paragraphs.append(translated)

        format_trans = []
        for row in trans_paragraphs:
            row = row.replace(': ', ':')
            row = row.replace('->', '-->')
            row += '\n\n'
            format_trans.append(row)
        self.new_paragraphs = format_trans
        self.progress_dialog.close()
        self.update_example()

    @QtCore.Slot()
    def save_video(self):
        self.wait_message('Saving Video...')

        options = QFileDialog.Options()
        output_file, _ = QFileDialog.getSaveFileName(self, "Seleccionar archivos", "",
                                                     "Todos los archivos (*);;Archivos de texto (*.txt)",
                                                     options=options)
        if not output_file: return

        subs_ = [self.dict_subs[i] for i in self.dict_subs.keys()]
        subs_ = [''.join(j) for j in subs_]

        tmp_subs = []
        path_subs = '/'.join(output_file.split('/')[:-1])
        ncode = self.encode_list.currentText()
        for id, sub_i in enumerate(subs_):
            sub_name = f'sub_tmp_{id}.srt'
            path_srt = os.path.join(path_subs, sub_name)
            file_i = open(path_srt, 'w+', encoding=ncode)
            file_i.write(sub_i)
            file_i.close()
            tmp_subs.append(path_srt)
            subprocess.run(['attrib', '+h', path_srt], shell=True)

        tmp_subs = [path_i.replace('/', '\\') for path_i in tmp_subs]

        subs_streams = [ffmpeg.input(subs_path) for subs_path in tmp_subs]
        output_file = output_file.replace('/', '\\')

        video_path = self.file_path.toLocalFile()
        video_path = video_path.replace('/', '\\')
        video_stream = ffmpeg.input(video_path)
        subs_labels = [self.curr_subs.item(i).text() for i in range(self.curr_subs.count())]


        cmd = [
            "ffmpeg",
            "-i", video_path
        ]

        for subs_path in tmp_subs: cmd += ["-i", subs_path]

        cmd += [
            "-map", "0:v",
            "-map", "0:a"]

        for i in range(len(tmp_subs)):cmd += ["-map", str(i + 1)]

        cmd += [
            "-f", "matroska",
            "-acodec", "copy",
            "-vcodec", "copy",
            "-scodec", "srt"]

        for i, label in enumerate(subs_labels): cmd += ["-metadata:s:s:" + str(i), "title=" + label]
        cmd.append(output_file)
        print('Comando ffmpeg:', ' '.join(cmd))
        try:   subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e: print('Error de ffmpeg:', e.stderr)
        [os.remove(path_i) for path_i in tmp_subs]
        self.progress_dialog.close()

if __name__ == "__main__":

    app = QApplication([])
    #app.setStyleSheet(widget_format())

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())
