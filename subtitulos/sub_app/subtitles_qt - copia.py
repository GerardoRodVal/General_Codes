import sys
import random
from PySide6 import *
from functools import partial
from datetime import datetime, timedelta

import googletrans
from langdetect import detect
from deep_translator import GoogleTranslator

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QIcon
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMainWindow,
                               QSpacerItem, QSizePolicy, QFileDialog, QMessageBox, QBoxLayout, QProgressDialog,
                               QStackedLayout)

import ffmpeg
from opensubtitlescom import OpenSubtitles
import json
import sys

import subprocess
import tempfile
import os


def widget_format():
    return(
    """
    QWidget {
        background-color: #000000;
        font-size: 12px;
    }
    
    QPushButton{
        background-color: #20018F;
        font-size: 12px;
        color: white;
        border-radius: 10px;
        padding: 5px;
        width: 10px;
        height: 15px;}
    QPushButton:hover {background-color: #0e0140;}
    QPushButton:pressed {background-color: white;}
    
    QPushButton#trans_btn {
        width: 20px;      
        height: 15px;         
        }
        
    QPushButton:disabled {
        background-color: #a0a0a0;  /* Color de fondo cuando está desactivado */
        color: #d3d3d3;             /* Color del texto cuando está desactivado */
        }
    """)

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.dict_subs = {}
        self.setWindowTitle('Subtitles Editor')
        #self.setFixedSize(1200,700)

        # ------------------------ widgets
        self.widget_variables()

        # ------------------------ layouts
        self.widget_layout()

        # ------------------------ actions
        self.widget_actions()

        # ------------------------ format
        #self.set_widget_objs()

    def widget_variables(self):
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
        self.forwardButton.setEnabled(False)
        self.reloadButton = QPushButton()
        self.reloadButton.setIcon(QIcon('./icons/reboot.png'))
        self.reloadButton.setEnabled(False)

        self.btn_use_subs = QPushButton('Use')
        self.btn_use_subs.setEnabled(False)
        self.curr_subs = QtWidgets.QListWidget()
        self.curr_subs.setFixedSize(100, 200)

        self.curr_title = QtWidgets.QLabel("Current Subtitles", alignment=QtCore.Qt.AlignCenter)
        self.txt_search = QtWidgets.QLineEdit()
        self.txt_search.setPlaceholderText("Find by keywords: names, years, format, etc...")
        self.txt_search.setFixedSize(300, 30)
        self.btn_search = QtWidgets.QPushButton("Search")
        self.lst_subs = QtWidgets.QListWidget()
        self.lst_subs.setFixedSize(400, 200)
        self.empty_mssg = QLabel("The list is currently empty", self)
        self.btn_down_subs = QtWidgets.QPushButton("Download")
        self.btn_down_subs.setEnabled(False)

        self.btn_subs = QtWidgets.QPushButton("Load Subtitles")
        self.btn_subs.setFixedSize(150, 30)
        self.encode_list = QtWidgets.QComboBox()
        self.encode_list.setFixedSize(100, 30)
        self.separator1 = QtWidgets.QLabel("-" * 50, alignment=QtCore.Qt.AlignCenter)

        self.example_id = QtWidgets.QSpinBox()
        self.example_id.setFixedSize(70, 30)
        self.example_i = QtWidgets.QLabel("Original Format Subtitle", alignment=QtCore.Qt.AlignCenter)
        self.example_i.setFixedSize(200, 100)
        self.example_f = QtWidgets.QLabel("Edited Format Subtitle", alignment=QtCore.Qt.AlignCenter)
        self.example_f.setFixedSize(200, 100)

        self.lang_orig = QtWidgets.QComboBox()
        self.lang_orig.setFixedSize(100, 30)
        self.orig__ = QtWidgets.QLabel("--->")
        self.trans_btn = QtWidgets.QPushButton("Translate")
        self.trans_btn.setEnabled(False)
        self.trans_btn.setFixedSize(100, 25)
        self.lang_dest = QtWidgets.QComboBox()
        self.lang_dest.setFixedSize(100, 30)
        self.dest__ = QtWidgets.QLabel("<---")
        self.separator2 = QtWidgets.QLabel("-" * 50, alignment=QtCore.Qt.AlignCenter)

        self.title_time = QtWidgets.QLabel("Change time")
        self.time_values = QtWidgets.QDoubleSpinBox()
        self.time_values.setFixedSize(100, 30)
        self.separator3 = QtWidgets.QLabel("-" * 50, alignment=QtCore.Qt.AlignCenter)
        self.btn_save_subs = QtWidgets.QPushButton("Save Subs")
        self.btn_save_subs.setEnabled(False)
        self.btn_save_subs.setFixedSize(150, 30)

        self.title_sub = QtWidgets.QLineEdit()
        self.title_sub.setPlaceholderText("Title Name")
        self.title_sub.setFixedSize(200, 30)

        self.btn_add_subs = QtWidgets.QPushButton("Add Subs")
        self.btn_add_subs.setEnabled(False)
        self.btn_add_subs.setFixedSize(150, 30)

        self.btn_save_video = QtWidgets.QPushButton("Save Video")
        self.btn_save_video.setEnabled(False)
        self.btn_save_video.setFixedSize(150, 30)

    def widget_layout(self):
        self.layout = QtWidgets.QGridLayout(self)

        # ------------------------------------------------------------------------------ Layout for video player
        lyt_video_v = QVBoxLayout()
        lyt_video_v.addWidget(self.btn_load_video, alignment=QtCore.Qt.AlignCenter)
        lyt_video_v.addWidget(self.videoWidget, alignment=QtCore.Qt.AlignCenter)
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
        lyt_manual.addWidget(self.btn_down_subs)
        lyt_manual.addWidget(self.btn_subs)
        lyt_subs_s.addLayout(lyt_manual)
        # -
        lyt_opensub = QVBoxLayout()
        #-
        lyt_search = QHBoxLayout()
        lyt_search.addWidget(self.txt_search)
        lyt_search.addWidget(self.btn_search)
        lyt_opensub.addLayout(lyt_search)
        # -
        lyt_subs_mssg = QStackedLayout()
        lyt_subs_mssg.addWidget(self.lst_subs)
        lyt_subs_mssg.addWidget(self.empty_mssg)
        lyt_opensub.addLayout(lyt_subs_mssg)
        # -
        lyt_subs_s.addLayout(lyt_opensub)


        self.layout.addLayout(lyt_subs_s, 0, 2, 2, 1)

        # ------------------------------------------------------------------------------ layout examples edition
        lyt_subs_e = QHBoxLayout()
        # -
        lyt_subs_e.addWidget(self.example_i)
        # -
        layout_middle = QVBoxLayout()
        layout_middle.addWidget(self.separator1)
        layout_middle.addWidget(self.example_id, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.lang_orig, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.orig__, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.trans_btn, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.lang_dest, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.dest__, alignment=QtCore.Qt.AlignCenter)
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

        self.title_sub = QtWidgets.QLineEdit()
        self.title_sub.setPlaceholderText("Title Name")
        self.title_sub.setFixedSize(200, 30)

        self.btn_add_subs = QtWidgets.QPushButton("Add Subs")
        self.btn_add_subs.setEnabled(False)
        self.btn_add_subs.setFixedSize(150, 30)
        # -
        self.layout.addLayout(lyt_subs_e, 2,2, 2,3)

    def widget_actions(self):
        self.btn_load_video.clicked.connect(self.LoadVideo)
        self.playButton.clicked.connect(self.play_video)
        self.pauseButton.clicked.connect(self.pause_video)
        self.backButton.clicked.connect(self.rewind_10s)
        self.forwardButton.clicked.connect(self.forward_10s)
        self.reloadButton.clicked.connect(self.reload_video)

        self.btn_subs.clicked.connect(self.load_subs)
        self.btn_search.clicked.connect(self.search_subs)
        self.btn_down_subs.clicked.connect(self.download_subs)

        self.encode_list.currentIndexChanged.connect(self.enconde_subs)

        self.example_id.valueChanged.connect(self.update_example)
        self.time_values.valueChanged.connect(self.update_time)
        self.btn_save_subs.clicked.connect(self.save_srt)
        self.trans_btn.clicked.connect(self.translate_text)

        self.btn_use_subs.clicked.connect(self.use_localsub)
        self.btn_save_video.clicked.connect(self.save_video)
        self.btn_add_subs.clicked.connect(self.add_subs_function)

    @QtCore.Slot()
    def LoadVideo(self):

        self.curr_subs.clear()
        videoFile, _ = QFileDialog.getOpenFileName(self, "Abrir Video", "", "Videos (*.mp4 *.avi *.mkv)")
        self.file_path = QUrl.fromLocalFile(videoFile)
        if videoFile:
            self.wait_message('Loading Video...')
            self.mediaPlayer.setSource(self.file_path)
            self.playButton.setEnabled(True)
            self.pauseButton.setEnabled(True)
            self.forwardButton.setEnabled(True)
            self.backButton.setEnabled(True)
            self.reloadButton.setEnabled(True)
            self.btn_use_subs.setEnabled(True)
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
        print('finished')
        self.dict_subs = dict_subs
        self.progress_dialog.close()
        #self.wait_msg.destroy()

    @QtCore.Slot()
    def play_video(self):
        self.mediaPlayer.play()

    @QtCore.Slot()
    def pause_video(self):
        self.mediaPlayer.pause()

    @QtCore.Slot()
    def rewind_10s(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 10000)

    @QtCore.Slot()
    def forward_10s(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 10000)

    @QtCore.Slot()
    def reload_video(self):
        current_media = self.mediaPlayer.media()
        self.mediaPlayer.setMedia(current_media)
        self.mediaPlayer.play()

    @QtCore.Slot()
    def wait_message(self, message):
        self.progress_dialog = QProgressDialog("Please wait, process is running...", None, 0, 0, self)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.show()
        self.progress_dialog.setValue(0)

        """
        self.wait_msg = QMessageBox(self)
        self.wait_msg.setWindowTitle("Wait...")
        self.wait_msg.setIcon(QMessageBox.Information)
        self.wait_msg.setText(message)
        #self.wait_msg.setStyleSheet("QLabel{min-width: 150px; min-height: 50px;}")
        #self.wait_msg.setStandardButtons(QMessageBox.NoButton)
        self.wait_msg.setModal(True)
        #self.wait_msg.show()
        self.wait_msg.exec_()
        """

    def widget_layout_1(self):
        self.layout = QtWidgets.QGridLayout(self)

        # Layout for video player
        lyt_video = QHBoxLayout()
        lyt_video_v = QVBoxLayout()
        lyt_video_v.addWidget(self.btn_load_video, alignment=QtCore.Qt.AlignCenter)
        lyt_video_v.addWidget(self.videoWidget, alignment=QtCore.Qt.AlignCenter)
        lyt_video_b = QHBoxLayout()
        lyt_video_b.addWidget(self.playButton, alignment=QtCore.Qt.AlignCenter)
        lyt_video_b.addWidget(self.pauseButton, alignment=QtCore.Qt.AlignCenter)
        lyt_video_b.addWidget(self.backButton, alignment=QtCore.Qt.AlignCenter)
        lyt_video_b.addWidget(self.forwardButton, alignment=QtCore.Qt.AlignCenter)
        lyt_video_b.addWidget(self.reloadButton, alignment=QtCore.Qt.AlignCenter)
        lyt_video_v.addLayout(lyt_video_b)
        lyt_video.addLayout(lyt_video_v)
        lyt_video_s = QVBoxLayout()
        lyt_video_s.addWidget(self.btn_use_subs)
        lyt_video_s.addWidget(self.curr_subs)
        lyt_video.addLayout(lyt_video_s)
        self.layout.addLayout(lyt_video, 0, 0)

        # Layout for subtitles search
        lyt_subs = QVBoxLayout()
        lyt_subs_s = QHBoxLayout()
        lyt_subs_s.addWidget(self.txt_search, alignment=QtCore.Qt.AlignCenter)
        lyt_subs_s.addWidget(self.btn_search, alignment=QtCore.Qt.AlignCenter)
        lyt_subs.addLayout(lyt_subs_s)
        lyt_subs.addWidget(self.lst_subs, alignment=QtCore.Qt.AlignCenter)
        lyt_subs.addWidget(self.btn_down_subs, alignment=QtCore.Qt.AlignCenter)
        self.layout.addLayout(lyt_subs, 0, 1)

        # Layout for loading subtitles and encoding
        layout_linea_1 = QHBoxLayout()
        layout_linea_1.addWidget(self.btn_subs)
        layout_linea_1.addWidget(self.encode_list)
        self.layout.addLayout(layout_linea_1, 1, 0, 1, 2)

        # Additional settings and actions
        layout_middle = QVBoxLayout()
        layout_middle.addWidget(self.separator1)
        layout_middle.addWidget(self.example_id, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.lang_orig, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.orig__, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.trans_btn, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.lang_dest, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.dest__, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.separator2)
        layout_middle.addWidget(self.title_time, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.time_values, alignment=QtCore.Qt.AlignCenter)
        layout_middle.addWidget(self.separator3)
        layout_middle.addWidget(self.btn_save_subs, alignment=QtCore.Qt.AlignCenter)

        self.layout.addLayout(layout_middle, 2, 0, 5, 1)

        # Display widgets for example IDs
        self.layout.addWidget(self.example_i, 2, 1, 2, 1)
        self.layout.addWidget(self.example_f, 4, 1, 2, 1)
        self.layout.addWidget(self.title_sub, 6, 1, 1, 1, alignment=QtCore.Qt.AlignRight)
        self.layout.addWidget(self.btn_add_subs, 6, 1, 1, 1, alignment=QtCore.Qt.AlignCenter)

        self.layout.addWidget(self.btn_save_video, 7, 1,2,1)

    @QtCore.Slot()
    def add_subs_function(self):
        curr_name = self.title_sub.text()
        self.curr_subs.addItems([curr_name])

        curr_paragraph = self.new_paragraphs
        n = len(self.dict_subs)
        self.dict_subs[n] = curr_paragraph

        self.btn_save_video.setEnabled(True)

    def search_subs(self):
        self.subtitles = OpenSubtitles("MyApp v1.0.0", "SDI6uXyLXr80HhFIuYoIrNFXph1Or6cl")
        self.subtitles.login('_galighieri_', 'Visorak1!')

        val_search = self.txt_search.text()
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

    def use_localsub(self):
        curr_id = self.curr_subs.currentRow()
        paragraphs = self.dict_subs[curr_id]
        self.paragraphs = paragraphs
        self.new_paragraphs = paragraphs
        self.update_example()
        self.update_languajes()

    @QtCore.Slot()
    def download_subs(self):
        dict_id = self.subs_id
        curr_val = self.lst_subs.currentItem()
        curr_val = curr_val.text()
        print(curr_val)
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

        print(paragraphs)
        self.example_i.setText(paragraphs[self.example_id.value()-1])
        self.paragraphs = paragraphs
        self.new_paragraphs = paragraphs
        self.example_id.setRange(1, len(paragraphs))
        self.update_languajes()
        self.update_example()

        # ['1\n00:00:02,000 --> 00:00:07,000\nDownloaded from\nYTS.MX\n\n', '2\n00:00:08,000 --> 00:00:13,000\nOfficial YIFY movies site:\nYTS.MX\n\n', '3\n00:03:58,405 --> 00:04:00,449\nYou want it?\n\n',
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

    def set_widget_objs(self):
        self.btn_search.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn_search.setFixedSize(100, 35)

        self.btn_load_video.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn_load_video.setFixedSize(100, 35)

        self.btn_down_subs.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn_down_subs.setFixedSize(100, 35)

        self.lst_subs.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.lst_subs.setMinimumSize(550, 250)

        self.btn_subs.setObjectName("btn_subs")
        self.encode_list.setObjectName("encode_list")
        self.trans_btn.setObjectName("trans_btn")
        self.btn_save_subs.setObjectName("btn_save_subs")
        self.btn_search.setObjectName("btn_search")

    def update_time(self):
        def add_time(time, extra_time):
            row_time = datetime.strptime(time, "%H:%M:%S,%f")
            new_time = row_time + timedelta(seconds=float(extra_time))
            row = str(new_time.time())[:-3]
            row = row.replace('.',',')
            return row
        self.time_values.setRange(0.0, 1000.0)
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
        curr_land_id = detect(self.example_i.text())

        curr_lang = curr_land_id+' - ' +langs_dict[curr_land_id]
        try:    curr_idx = langs.index(curr_lang)
        except: curr_idx = 0
        spanish_id = 198

        self.lang_orig.addItems(langs)
        self.lang_orig.setCurrentIndex(curr_idx)
        self.lang_dest.addItems(langs)
        self.lang_dest.setCurrentIndex(spanish_id)
        self.trans_btn.setEnabled(True)

    @QtCore.Slot()
    def update_example(self):
        self.encode_list.addItems(['utf-8', 'latin1'])

        clean_pg = [i for i in self.paragraphs if i != '\n']
        id_ex = clean_pg[self.example_id.value()-1]
        self.example_i.setText(id_ex)

        clean_pg = [i for i in self.new_paragraphs if i != '\n']
        id_ex = clean_pg[self.example_id.value()-1]
        self.example_f.setText(id_ex)

        self.btn_save_subs.setEnabled(True)
        self.btn_add_subs.setEnabled(True)

    @QtCore.Slot()
    def load_subs(self):
        curr_ncode = self.encode_list.currentText()

        file_dialog = QtWidgets.QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self,
                                                   "Abrir Archivo de Texto","",
                                                   "Todos los Archivos (*)")

        file = open(file_path, encoding=curr_ncode)
        content = file.read()
        paragraphs = []
        pg_i = ''
        for p in content.split('\n'):
            pg_i += (p+'\n')
            if p == '':
                paragraphs.append(pg_i)
                pg_i = ''

        self.example_i.setText(paragraphs[self.example_id.value()-1])
        self.paragraphs = paragraphs
        self.new_paragraphs = paragraphs
        self.update_languajes()
        self.update_example()

    @QtCore.Slot()
    def save_srt(self):
        plain_format = '\n'.join(self.new_paragraphs)
        options      = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Guardar archivo de texto", '', "Text Files (*.srt);;All Files (*)", options=options)
        curr_ncode = self.encode_list.currentText()
        if file_name:
            with open(file_name, 'w', encoding=curr_ncode) as file: file.write(plain_format)

    @QtCore.Slot()
    def translate_text(self):

        self.wait_message('Transcribing subtitles...')

        dest = self.lang_dest.currentText()
        dest = dest.split(' ')[0]
        orig = self.lang_orig.currentText()
        orig = orig.split(' ')[0]
        trans_paragraphs = []

        for id, pr_i in enumerate(self.paragraphs):
            translated = GoogleTranslator(source=orig, target=dest).translate(pr_i)
            trans_paragraphs.append(translated)

        self.new_paragraphs = trans_paragraphs
        self.progress_dialog.close()
        self.update_example()

    def save_video_v1(self):
        options = QtWidgets.QFileDialog.Options()
        output_file, _ = QFileDialog.getSaveFileName(self, "Seleccionar archivos", "",
                                                     "Todos los archivos (*);;Archivos de texto (*.txt)",
                                                     options=options)

        subs_ = [self.dict_subs[i] for i in self.dict_subs.keys()]
        print('subs_', subs_)
        subs_ = [''.join(j) for j in subs_]
        tmp_subs = []
        path_subs = '/'.join(output_file.split('/')[:-1])
        ncode = self.encode_list.currentText()
        for id, sub_i in enumerate(subs_):
            sub_name = f'/sub_tmp_{id}.srt'
            path_srt = path_subs + sub_name
            file_i = open(path_srt, 'w+', encoding=ncode)
            file_i.write(sub_i)
            os.system(f"attrib +h {sub_name}")                  # hidden windows element
            file_i.close()
            tmp_subs.append(path_srt)
        tmp_subs = [path_i.replace('/','\\') for path_i in tmp_subs]

        subs_streams = [ffmpeg.input(subs_path) for subs_path in tmp_subs]
        output_file = output_file.replace('/', '\\')

        video_path = self.file_path.toLocalFile()
        video_path = video_path.replace('/', '\\')
        video_stream = ffmpeg.input(video_path)
        subs_labels = [self.curr_subs.item(i).text() for i in range(self.curr_subs.count())]

        output_cmd = ffmpeg.output(
            video_stream, *subs_streams, output_file,
            vcodec='copy',
            acodec='copy',
            scodec='srt',   # just for mp4
            **{f'metadata:s:s:{i}': f'title={subs_labels[i]}' for i in range(len(subs_labels))}
        )

        global_args = ['-map', '0']
        for i in range(len(subs_labels)):
            global_args += ['-map', str(i + 1)]

        cmd = output_cmd.compile()
        print('Comando ffmpeg:', ' '.join(cmd))

        output_cmd.global_args(*global_args).run()

        [os.remove(path_i) for path_i in tmp_subs]

    @QtCore.Slot()
    def save_video(self):
        print('flag final')
        options = QtWidgets.QFileDialog.Options()
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
            sub_name = f'/sub_tmp_{id}.srt'
            path_srt = path_subs + sub_name
            file_i = open(path_srt, 'w+', encoding=ncode)
            file_i.write(sub_i)
            os.system(f"attrib +h {path_srt}")  # hidden windows element
            file_i.close()
            tmp_subs.append(path_srt)
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
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print('result', result.stdout)
        except subprocess.CalledProcessError as e: print('Error de ffmpeg:', e.stderr)
        [os.remove(path_i) for path_i in tmp_subs]

if __name__ == "__main__":

    app = QtWidgets.QApplication([])
    #app.setStyleSheet(widget_format())

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())
