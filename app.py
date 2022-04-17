import sys
import os
import platform
import os.path
import time
import random
import watchdog.events
import watchdog.observers
import filecmp
import shutil
import glob
import xlsxwriter
import array as array
import subprocess


from datetime import date, datetime, timedelta
from PyQt5.QtCore import Qt,QSize,QSettings, QThread, pyqtSignal, pyqtSlot, QAbstractAnimation, QVariantAnimation, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap, QFont, QColor
from PyQt5.QtWidgets import *


APP_PATH = os.getcwd()
CONFIG = QSettings("config.ini", QSettings.IniFormat)
SITE = CONFIG.value('Site/name', "") 
DTS_FEED = CONFIG.value('Directory/dtsfeed', "")
PROG_INPUT = CONFIG.value('Directory/progin', "")
PROG_OUTPUT = CONFIG.value('Directory/progout', "")
RTTR_PROGRAM = CONFIG.value('Directory/rttrprog', "")
RTTR_OUT = CONFIG.value('Directory/rttrout', "")

PROG_DAT = CONFIG.value('Directory/progdat', "")

POINTA_NAME = CONFIG.value('PointName/PointA', "Point A")
POINTB_NAME = CONFIG.value('PointName/PointB', "Point B")
POINTC_NAME = CONFIG.value('PointName/PointC', "Point C")
POINTD_NAME = CONFIG.value('PointName/PointD', "Point D")

RTTR_OUTPUT = CONFIG.value('Directory/rttrout', "")
POINTA_FROM = CONFIG.value('PointA/from', "")
POINTA_TO = CONFIG.value('PointA/to', "")
POINTA_CHANNALA_ALERTT = float(CONFIG.value('PointA/aalertt', ""))
POINTA_CHANNALA_ALERTS = float(CONFIG.value('PointA/aalerts', ""))
POINTA_CHANNALA_ALERTC = float(CONFIG.value('PointA/aalertc', ""))
POINTA_CHANNALB_ALERTT = float(CONFIG.value('PointA/balertt', ""))
POINTA_CHANNALB_ALERTS = float(CONFIG.value('PointA/balerts', ""))
POINTA_CHANNALB_ALERTC = float(CONFIG.value('PointA/balertc', ""))
POINTA_CHANNALC_ALERTT = float(CONFIG.value('PointA/calertt', ""))
POINTA_CHANNALC_ALERTS = float(CONFIG.value('PointA/calerts', ""))
POINTA_CHANNALC_ALERTC = float(CONFIG.value('PointA/calertc', ""))

POINTB_FROM = CONFIG.value('PointB/from', "")
POINTB_TO = CONFIG.value('PointB/to', "")
POINTB_CHANNALA_ALERTT = CONFIG.value('PointB/aalertt', "")
POINTB_CHANNALA_ALERTS = CONFIG.value('PointB/aalerts', "")
POINTB_CHANNALA_ALERTC = CONFIG.value('PointB/aalertc', "")
POINTB_CHANNALB_ALERTT = CONFIG.value('PointB/balertt', "")
POINTB_CHANNALB_ALERTS = CONFIG.value('PointB/balerts', "")
POINTB_CHANNALB_ALERTC = CONFIG.value('PointB/balertc', "")
POINTB_CHANNALC_ALERTT = CONFIG.value('PointB/calertt', "")
POINTB_CHANNALC_ALERTS = CONFIG.value('PointB/calerts', "")
POINTB_CHANNALC_ALERTC = CONFIG.value('PointB/calertc', "")
POINTC_FROM = CONFIG.value('PointC/from', "")
POINTC_TO = CONFIG.value('PointC/to', "")
POINTC_CHANNALA_ALERTT = CONFIG.value('PointC/aalertt', "")
POINTC_CHANNALA_ALERTS = CONFIG.value('PointC/aalerts', "")
POINTC_CHANNALA_ALERTC = CONFIG.value('PointC/aalertc', "")
POINTC_CHANNALB_ALERTT = CONFIG.value('PointC/balertt', "")
POINTC_CHANNALB_ALERTS = CONFIG.value('PointC/balerts', "")
POINTC_CHANNALB_ALERTC = CONFIG.value('PointC/balertc', "")
POINTC_CHANNALC_ALERTT = CONFIG.value('PointC/calertt', "")
POINTC_CHANNALC_ALERTS = CONFIG.value('PointC/calerts', "")
POINTC_CHANNALC_ALERTC = CONFIG.value('PointC/calertc', "")
POINTD_FROM = CONFIG.value('PointD/from', "")
POINTD_TO = CONFIG.value('PointD/to', "")
POINTD_CHANNALA_ALERTT = CONFIG.value('PointD/aalertt', "")
POINTD_CHANNALA_ALERTS = CONFIG.value('PointD/aalerts', "")
POINTD_CHANNALA_ALERTC = CONFIG.value('PointD/aalertc', "")
POINTD_CHANNALB_ALERTT = CONFIG.value('PointD/balertt', "")
POINTD_CHANNALB_ALERTS = CONFIG.value('PointD/balerts', "")
POINTD_CHANNALB_ALERTC = CONFIG.value('PointD/balertc', "")
POINTD_CHANNALC_ALERTT = CONFIG.value('PointD/calertt', "")
POINTD_CHANNALC_ALERTS = CONFIG.value('PointD/calerts', "")
POINTD_CHANNALC_ALERTC = CONFIG.value('PointD/calertc', "")

POINTA_TIME = ""
POINTB_TIME = ""
POINTC_TIME = ""
POINTD_TIME = ""

BASELINE_CHANNALA = CONFIG.value('BaseLine/channel0', "")
BASELINE_CHANNALB = CONFIG.value('BaseLine/channel1', "")
BASELINE_CHANNALC = CONFIG.value('BaseLine/channel2', "")
BASELINE_CHANNALD = CONFIG.value('BaseLine/channel3', "")

BASELINE_FILES = [BASELINE_CHANNALA, BASELINE_CHANNALB, BASELINE_CHANNALC, BASELINE_CHANNALD]
BASELINE_VALUE = [[],[],[],[]]
BASELINE_TEMP = []

TODAY = date.today()

TODAY_YYYYMMDD = TODAY.strftime("%d%m%Y")
TODAY_DDMMYYYY = TODAY.strftime("%Y%m%d")
TODAY_YYYYMMDD2 = TODAY.strftime("%d/%m/%Y")
TODAY_DDMMYYYY2 = TODAY.strftime("%Y/%m/%d")
TODAY_DDMMMYYYY = TODAY.strftime("%d %b %Y")

RESULT_RTTR_A13 = 0.0000

APP_PATH
print("APP_PATH:", APP_PATH)
print("ccccccccccccc", BASELINE_FILES)

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

RTTROUT_PATHDATE = TODAY_DDMMYYYY


class MyHandler(FileSystemEventHandler):

    def on_created(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')
        


        head, tail = os.path.split(event.src_path)
        print("tail -> ",tail)
        filename = tail.split("_")
        print("tail -> ",filename[1][5:6])
        print("tail -> ",filename[2][5:6])

        Point = filename[1][5:6]
        Phase = filename[2][5:6]

        file1 = open(event.src_path, "r")
        count = 0
        for line in file1:
            count += 1
            if(count == 1):
                datax = line.strip().split(",")
                temp_con = datax[1]
                current = datax[2]
                print("temp_con",temp_con)
            print("Line{}: {}".format(count, line.strip()))
        file1.close()


        if(Point == "A"):
            if(Phase == "A"):
                oMainwindow.threadMain.threadSignalMain.emit(0, 'A', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)

        if(Point == "A"):
            if(Phase == "B"):
                oMainwindow.threadMain.threadSignalMain.emit(0, 'B', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)

        if(Point == "A"):
            if(Phase == "C"):
                oMainwindow.threadMain.threadSignalMain.emit(0, 'C', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)


        if(Point == "B"):
            if(Phase == "A"):
                oMainwindow.threadMain.threadSignalMain.emit(1, 'A', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)

        if(Point == "B"):
            if(Phase == "B"):
                oMainwindow.threadMain.threadSignalMain.emit(1, 'B', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)

        if(Point == "B"):
            if(Phase == "C"):
                oMainwindow.threadMain.threadSignalMain.emit(1, 'C', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)

        if(Point == "C"):
            if(Phase == "A"):
                oMainwindow.threadMain.threadSignalMain.emit(2, 'A', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)

        if(Point == "C"):
            if(Phase == "B"):
                oMainwindow.threadMain.threadSignalMain.emit(2, 'B', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)

        if(Point == "C"):
            if(Phase == "C"):
                oMainwindow.threadMain.threadSignalMain.emit(2, 'C', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)


class HeaderLabel(QLabel):
    
    def __init__(self, text):
        super().__init__(text)

        palette = self.palette()
        palette.setColor(self.foregroundRole(), QColor(205,44,203))

        myFont=QFont()
        myFont.setBold(True)
        myFont.setPixelSize(10)
        self.setFont(myFont)

        # font = QFont('Arial')
        # font.setStyleHint(QFont.TypeWriter)
        # font.setPixelSize(15)
        self.setPalette(palette)


    def _set_color(self, col):        
        # self.setAttribute(Qt.WA_StyledBackground, True)
        # self.setStyleSheet('background-color: red')
        # self.backgroundRole(QColor('red'))
        palette = self.palette()
        palette.setColor(self.foregroundRole(), col)
        self.setPalette(palette)

    color = pyqtProperty(QColor, fset=_set_color)


class DigitLabel(QLabel):
    
    def __init__(self, text):
        super().__init__(text)

        palette = self.palette()
        palette.setColor(self.foregroundRole(), QColor(235,192,222))

        myFont=QFont()
        myFont.setBold(True)
        myFont.setPixelSize(10)
        self.setFont(myFont)

        # font = QFont('Arial')
        # font.setStyleHint(QFont.TypeWriter)
        # font.setPixelSize(15)
        self.setPalette(palette)


    def _set_color(self, col):        
        # self.setAttribute(Qt.WA_StyledBackground, True)
        # self.setStyleSheet('background-color: red')
        # self.backgroundRole(QColor('red'))
        palette = self.palette()
        palette.setColor(self.foregroundRole(), col)
        self.setPalette(palette)

    color = pyqtProperty(QColor, fset=_set_color)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        self.mainwidth = 1280
        self.mainheight = 720
        self.cardwidth = 350
        self.cardheight = 165
        self.labelwidth = 60
        self.labelheight = 18

        self.setObjectName("MainWindow")


        self.setWindowTitle('RTTR Monitoring System')
        self.setMinimumSize(self.mainwidth, self.mainheight)
        self.setGeometry(0,0,self.mainwidth,self.mainheight)
        self.setting_window = SettingWindow()
        self.reporting_window = ReportingWindow()

        # Tray
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        show_action = QAction("Show", self)
        hide_action = QAction("Hide", self)
        setting_action = QAction("Setting", self)
        reporting_action = QAction("Report", self)
        self.testfeed_action = QAction("Stop Feed", self)
        quit_action = QAction("Exit", self)

        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        setting_action.triggered.connect(self.show_setting_window)
        reporting_action.triggered.connect(self.show_reporting_window)

        self.testfeed_action.triggered.connect(self.start_stop_feed)

        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        # tray_menu.addAction(show_action)
        # tray_menu.addAction(hide_action)
        tray_menu.addAction(setting_action)
        tray_menu.addAction(reporting_action)

        tray_menu.addAction(self.testfeed_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
  
        self.initUI()
        self.threadMain = None  
        self.start_stop_feed()

        for f in glob.glob(PROG_INPUT+"/Temp_*.*"):
            os.remove(f)

        self.setMouseTracking(True)

        self.watchdog()


    def watchdog(self):

        pathx = RTTR_OUT
        self.event_handler = MyHandler()
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path=pathx, recursive=False)
        self.observer.start()
        

    def initUI(self):

        self.HeaderFont=QFont()
        self.HeaderFont.setBold(True)
        self.HeaderFont.setPixelSize(15)        
        BoxFont=QFont()
        BoxFont.setPixelSize(18)

        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.9)
        self.label_font = QFont('Arial')
        self.label_color = "color: #31906E;background:;font-size:18px;"
        self.label_default = "0.0"

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.samuiUI()


        for point in ['A','B','C','D']:
            for row in range (1,4):
                for col in range (1,5):
                    label = getattr(self, 'label{}{}{}'.format(point,row,col))
                    label.setText(self.label_default)
                    # label.setText("-"+"19000")
                    label.setFont(BoxFont)
                    label.setAlignment(Qt.AlignRight)

        for point in ['A','B','C','D']:
            for row in range (1,4):
                for col in range (1,5):
                    anim = getattr(self, 'anim{}{}{}'.format(point,row,col))
                    anim.setDuration(1000)
                    anim.setLoopCount(-1)
                    anim.setStartValue(QColor(255,0,0))
                    anim.setEndValue(QColor("white"))

        self.calculateBaseLine()
        self.calculateTempBaseLine()

    def show_setting_window(self):
        # self.(Qt.WindowActive)
        self.setting_window.hide()
        self.setting_window.show()

    def show_reporting_window(self):
        # self.(Qt.WindowActive)
        self.reporting_window.hide()
        self.reporting_window.show()

    def samuiUI(self):

        if(SITE == "Kanom"):
            background_pixmap = QPixmap('img_kanom.jpg')
        if(SITE == "Samui"):    
            background_pixmap = QPixmap('img_samui.jpg')

        
        self.image = QLabel()
        self.image.setPixmap(background_pixmap)
        self.image.setScaledContents(True)

        layout_box = QHBoxLayout(self.main_widget)
        layout_box.setContentsMargins(0, 0, 0, 0)
        layout_box.addWidget(self.image)

        point_pixmap = QPixmap('img_point.png')
        self.background_point1 = QLabel(self.main_widget)
        self.background_point1.setPixmap(point_pixmap)
        self.background_point1.resize(1574, 580)
        self.background_point1.setScaledContents(True)

        self.background_point2 = QLabel(self.main_widget)
        self.background_point2.setPixmap(point_pixmap)
        self.background_point2.resize(1574, 580)
        self.background_point2.setScaledContents(True)

        self.background_point3 = QLabel(self.main_widget)
        self.background_point3.setPixmap(point_pixmap)
        self.background_point3.resize(1574, 580)
        self.background_point3.setScaledContents(True)

        self.background_point4 = QLabel(self.main_widget)
        self.background_point4.setPixmap(point_pixmap)
        self.background_point4.resize(1574, 580)
        self.background_point4.setScaledContents(True)

        self.pointA_name = HeaderLabel(self.main_widget)
        self.pointA_name.setText(POINTA_NAME) 
        self.pointA_name.setFont(self.HeaderFont)
        self.pointA_name.resize(145, 20)
        self.pointA_name.move(410, 505)

        self.pointB_name = HeaderLabel(self.main_widget)
        self.pointB_name.setText("Point B")
        self.pointB_name.setFont(self.HeaderFont)
        self.pointB_name.resize(145, 20)
        self.pointB_name.move(250, 330)

        self.pointC_name = HeaderLabel(self.main_widget)
        self.pointC_name.setText("Point C")
        self.pointC_name.setFont(self.HeaderFont)
        self.pointC_name.resize(145, 20)
        self.pointC_name.move(355, 155)

        self.pointD_name = HeaderLabel(self.main_widget)
        self.pointD_name.setText("Point D")
        self.pointD_name.setFont(self.HeaderFont)
        self.pointD_name.resize(145, 20)
        self.pointD_name.move(680, 25)

        self.labelA11 = DigitLabel(self.main_widget)
        self.animA11 = QPropertyAnimation(self.labelA11, b"color")

        self.labelA12 = DigitLabel(self.main_widget)
        self.animA12 = QPropertyAnimation(self.labelA12, b"color")

        self.labelA13 = DigitLabel(self.main_widget)
        self.animA13 = QPropertyAnimation(self.labelA13, b"color")

        self.labelA14 = DigitLabel(self.main_widget)
        self.animA14 = QPropertyAnimation(self.labelA14, b"color")

        self.labelA21 = DigitLabel(self.main_widget)
        self.animA21 = QPropertyAnimation(self.labelA21, b"color")

        self.labelA21 = DigitLabel(self.main_widget)
        self.animA21 = QPropertyAnimation(self.labelA21, b"color")

        self.labelA22 = DigitLabel(self.main_widget)
        self.animA22 = QPropertyAnimation(self.labelA22, b"color")

        self.labelA23 = DigitLabel(self.main_widget)
        self.animA23 = QPropertyAnimation(self.labelA23, b"color")

        self.labelA24 = DigitLabel(self.main_widget)
        self.animA24 = QPropertyAnimation(self.labelA24, b"color")

        self.labelA31 = DigitLabel(self.main_widget)
        self.animA31 = QPropertyAnimation(self.labelA31, b"color")

        self.labelA31 = DigitLabel(self.main_widget)
        self.animA31 = QPropertyAnimation(self.labelA31, b"color")

        self.labelA32 = DigitLabel(self.main_widget)
        self.animA32 = QPropertyAnimation(self.labelA32, b"color")

        self.labelA33 = DigitLabel(self.main_widget)
        self.animA33 = QPropertyAnimation(self.labelA33, b"color")

        self.labelA34 = DigitLabel(self.main_widget)
        self.animA34 = QPropertyAnimation(self.labelA34, b"color")

        self.labelB11 = DigitLabel(self.main_widget)
        self.animB11 = QPropertyAnimation(self.labelB11, b"color")

        self.labelB11 = DigitLabel(self.main_widget)
        self.animB11 = QPropertyAnimation(self.labelB11, b"color")

        self.labelB12 = DigitLabel(self.main_widget)
        self.animB12 = QPropertyAnimation(self.labelB12, b"color")

        self.labelB13 = DigitLabel(self.main_widget)
        self.animB13 = QPropertyAnimation(self.labelB13, b"color")

        self.labelB14 = DigitLabel(self.main_widget)
        self.animB14 = QPropertyAnimation(self.labelB14, b"color")

        self.labelB21 = DigitLabel(self.main_widget)
        self.animB21 = QPropertyAnimation(self.labelB21, b"color")

        self.labelB21 = DigitLabel(self.main_widget)
        self.animB21 = QPropertyAnimation(self.labelB21, b"color")

        self.labelB22 = DigitLabel(self.main_widget)
        self.animB22 = QPropertyAnimation(self.labelB22, b"color")

        self.labelB23 = DigitLabel(self.main_widget)
        self.animB23 = QPropertyAnimation(self.labelB23, b"color")

        self.labelB24 = DigitLabel(self.main_widget)
        self.animB24 = QPropertyAnimation(self.labelB24, b"color")

        self.labelB31 = DigitLabel(self.main_widget)
        self.animB31 = QPropertyAnimation(self.labelB31, b"color")
 
        self.labelB31 = DigitLabel(self.main_widget)
        self.animB31 = QPropertyAnimation(self.labelB31, b"color")

        self.labelB32 = DigitLabel(self.main_widget)
        self.animB32 = QPropertyAnimation(self.labelB32, b"color")

        self.labelB33 = DigitLabel(self.main_widget)
        self.animB33 = QPropertyAnimation(self.labelB33, b"color")

        self.labelB34 = DigitLabel(self.main_widget)
        self.animB34 = QPropertyAnimation(self.labelB34, b"color")

        self.labelC11 = DigitLabel(self.main_widget)
        self.animC11 = QPropertyAnimation(self.labelC11, b"color")

        self.labelC11 = DigitLabel(self.main_widget)
        self.animC11 = QPropertyAnimation(self.labelC11, b"color")

        self.labelC12 = DigitLabel(self.main_widget)
        self.animC12 = QPropertyAnimation(self.labelC12, b"color")

        self.labelC13 = DigitLabel(self.main_widget)
        self.animC13 = QPropertyAnimation(self.labelC13, b"color")

        self.labelC14 = DigitLabel(self.main_widget)
        self.animC14 = QPropertyAnimation(self.labelC14, b"color")

        self.labelC21 = DigitLabel(self.main_widget)
        self.animC21 = QPropertyAnimation(self.labelC21, b"color")

        self.labelC21 = DigitLabel(self.main_widget)
        self.animC21 = QPropertyAnimation(self.labelC21, b"color")

        self.labelC22 = DigitLabel(self.main_widget)
        self.animC22 = QPropertyAnimation(self.labelC22, b"color")

        self.labelC23 = DigitLabel(self.main_widget)
        self.animC23 = QPropertyAnimation(self.labelC23, b"color")

        self.labelC24 = DigitLabel(self.main_widget)
        self.animC24 = QPropertyAnimation(self.labelC24, b"color")

        self.labelC31 = DigitLabel(self.main_widget)
        self.animC31 = QPropertyAnimation(self.labelC31, b"color")

        self.labelC31 = DigitLabel(self.main_widget)
        self.animC31 = QPropertyAnimation(self.labelC31, b"color")

        self.labelC32 = DigitLabel(self.main_widget)
        self.animC32 = QPropertyAnimation(self.labelC32, b"color")

        self.labelC33 = DigitLabel(self.main_widget)
        self.animC33 = QPropertyAnimation(self.labelC33, b"color")

        self.labelC34 = DigitLabel(self.main_widget)
        self.animC34 = QPropertyAnimation(self.labelC34, b"color")

        self.labelD11 = DigitLabel(self.main_widget)
        self.animD11 = QPropertyAnimation(self.labelD11, b"color")

        self.labelD12 = DigitLabel(self.main_widget)
        self.animD12 = QPropertyAnimation(self.labelD12, b"color")

        self.labelD13 = DigitLabel(self.main_widget)
        self.animD13 = QPropertyAnimation(self.labelD13, b"color")

        self.labelD14 = DigitLabel(self.main_widget)
        self.animD14 = QPropertyAnimation(self.labelD14, b"color")

        self.labelD14 = DigitLabel(self.main_widget)
        self.animD14 = QPropertyAnimation(self.labelD14, b"color")

        self.labelD21 = DigitLabel(self.main_widget)
        self.animD21 = QPropertyAnimation(self.labelD21, b"color")

        self.labelD21 = DigitLabel(self.main_widget)
        self.animD21 = QPropertyAnimation(self.labelD21, b"color")

        self.labelD22 = DigitLabel(self.main_widget)
        self.animD22 = QPropertyAnimation(self.labelD22, b"color")

        self.labelD23 = DigitLabel(self.main_widget)
        self.animD23 = QPropertyAnimation(self.labelD23, b"color")

        self.labelD24 = DigitLabel(self.main_widget)
        self.animD24 = QPropertyAnimation(self.labelD24, b"color")

        self.labelD31 = DigitLabel(self.main_widget)
        self.animD31 = QPropertyAnimation(self.labelD31, b"color")

        self.labelD31 = DigitLabel(self.main_widget)
        self.animD31 = QPropertyAnimation(self.labelD31, b"color")

        self.labelD32 = DigitLabel(self.main_widget)
        self.animD32 = QPropertyAnimation(self.labelD32, b"color")

        self.labelD33 = DigitLabel(self.main_widget)
        self.animD33 = QPropertyAnimation(self.labelD33, b"color")

        self.labelD34 = DigitLabel(self.main_widget)
        self.animD34 = QPropertyAnimation(self.labelD34, b"color")


    def calculateTempBaseLine(self):

        for idx,filename in enumerate(BASELINE_FILES):
            base_filename = filename
            self.dstfile_input = open(base_filename, 'r')
            self.lines = self.dstfile_input.readlines()        
            for count,line in enumerate(self.lines, 1):

                if(count == 6):
                    base_channel_no = line.strip().split()[-1]

                if(count == 24):
                    if(int(base_channel_no) == 0):
                        base_channel_0 = line.strip().split()[-1]
                        BASELINE_TEMP.append(base_channel_0)
                    if(int(base_channel_no) == 1):
                        base_channel_1 = line.strip().split()[-1]
                        BASELINE_TEMP.append(base_channel_1)
                    if(int(base_channel_no) == 2):
                        base_channel_2 = line.strip().split()[-1]
                        BASELINE_TEMP.append(base_channel_2)
                    if(int(base_channel_no) == 3):
                        base_channel_3 = line.strip().split()[-1]
                        BASELINE_TEMP.append(base_channel_3)
            
        print("BASELINE_TEMP--------->",BASELINE_TEMP)    


    def calculateBaseLine(self):

        for idx,filename in enumerate(BASELINE_FILES):
            # print("xxxxxxxx->",idx,filename)
            # print("###########################################################################")        
            base_line_datetime = []
            base_feed_datetime = ""
            base_channel_no = 5
            base_poAch0_count = 0        
            base_poAch0_total = 0.00
            base_poAch0_avg = 0.00
            base_poBch0_count = 0        
            base_poBch0_total = 0.00
            base_poBch0_avg = 0.00
            base_poCch0_count = 0        
            base_poCch0_total = 0.00
            base_poCch0_avg = 0.00
            base_distance = 0.00
            base_filename = None

            base_filename = filename
            # if(channel_no == 1): base_filename = "/Users/superong/app_rttr/progin/Baseline_Sep291223_15(CH2 Land).bslr"
            # if(channel_no == 2): base_filename = "/Users/superong/app_rttr/progin/Baseline_Sep291225_16(CH3 Land).bslr"
            # if(channel_no == 3): base_filename = "/Users/superong/app_rttr/progin/Baseline_Sep291234_17(Forsubmarine 29-09-64)).bslr"

            self.dstfile_input = open(base_filename, 'r')
            self.lines = self.dstfile_input.readlines()        
            for count,line in enumerate(self.lines, 1):
                # print(count,line.strip())
                
                if(count == 6):
                    base_channel_no = line.strip().split()[-1]

                if(count >= 35):
                    base_distance = [float(n) for n in line.strip().split()][0]
                    base_distance_val = [float(n) for n in line.strip().split()][1]
                    # print("base_distance------>",base_distance,base_distance_val)
                    if(int(base_channel_no) == 0):
                        # Phase A 
                        # print("base_distance A------>",POINTA_FROM,POINTA_TO)
                        if(base_distance > float(POINTA_FROM) and base_distance < float(POINTA_TO)):
                            base_poAch0_count += 1
                            base_poAch0_total = base_poAch0_total + base_distance_val
                            base_poAch0_avg = base_poAch0_total/float(base_poAch0_count)
                        if(base_distance > float(POINTB_FROM) and base_distance < float(POINTB_TO)):
                            base_poBch0_count += 1
                            base_poBch0_total = base_poBch0_total + base_distance_val
                            base_poBch0_avg = base_poBch0_total/float(base_poBch0_count)
                        if(base_distance > float(POINTC_FROM) and base_distance < float(POINTC_TO)):
                            base_poCch0_count += 1
                            base_poCch0_total = base_poCch0_total + base_distance_val
                            base_poCch0_avg = base_poCch0_total/float(base_poCch0_count)

                    if(int(base_channel_no) == 1):
                        # Phase A 
                        if(base_distance > float(POINTA_FROM) and base_distance < float(POINTA_TO)):
                            base_poAch0_count += 1
                            base_poAch0_total = base_poAch0_total + base_distance_val
                            base_poAch0_avg = base_poAch0_total/float(base_poAch0_count)

                        if(base_distance > float(POINTB_FROM) and base_distance < float(POINTB_TO)):
                            base_poBch0_count += 1
                            base_poBch0_total = base_poBch0_total + base_distance_val
                            base_poBch0_avg = base_poBch0_total/float(base_poBch0_count)

                        if(base_distance > float(POINTC_FROM) and base_distance < float(POINTC_TO)):
                            base_poCch0_count += 1
                            base_poCch0_total = base_poCch0_total + base_distance_val
                            base_poCch0_avg = base_poCch0_total/float(base_poCch0_count)

                    if(int(base_channel_no) == 2):
                        # Phase A 
                        if(base_distance > float(POINTA_FROM) and base_distance < float(POINTA_TO)):
                            base_poAch0_count += 1
                            base_poAch0_total = base_poAch0_total + base_distance_val
                            base_poAch0_avg = base_poAch0_total/float(base_poAch0_count)
                        
                        if(base_distance > float(POINTB_FROM) and base_distance < float(POINTB_TO)):
                            base_poBch0_count += 1
                            base_poBch0_total = base_poBch0_total + base_distance_val
                            base_poBch0_avg = base_poBch0_total/float(base_poBch0_count)

                        if(base_distance > float(POINTC_FROM) and base_distance < float(POINTC_TO)):
                            base_poCch0_count += 1
                            base_poCch0_total = base_poCch0_total + base_distance_val
                            base_poCch0_avg = base_poCch0_total/float(base_poCch0_count)                        

                    if(int(base_channel_no) == 3):
                        # Phase A 
                        if(base_distance > float(POINTA_FROM) and base_distance < float(POINTA_TO)):
                            base_poAch0_count += 1
                            base_poAch0_total = base_poAch0_total + base_distance_val
                            base_poAch0_avg = base_poAch0_total/float(base_poAch0_count)
                        
                        if(base_distance > float(POINTB_FROM) and base_distance < float(POINTB_TO)):
                            base_poBch0_count += 1
                            base_poBch0_total = base_poBch0_total + base_distance_val
                            base_poBch0_avg = base_poBch0_total/float(base_poBch0_count)

                        if(base_distance > float(POINTC_FROM) and base_distance < float(POINTC_TO)):
                            base_poCch0_count += 1
                            base_poCch0_total = base_poCch0_total + base_distance_val
                            base_poCch0_avg = base_poCch0_total/float(base_poCch0_count)     


            BASELINE_VALUE[idx].append(base_poAch0_avg)
            BASELINE_VALUE[idx].append(base_poBch0_avg)
            BASELINE_VALUE[idx].append(base_poCch0_avg)


        print("ccccccc->",BASELINE_VALUE)        
        print("###########################################################################")


    def on_threadSignalMain(self, value, feed_type, feed_datetime, channal, strain_pointA, strain_pointB, strain_pointC, strain_pointD,
                            temp_pointA, temp_pointB, temp_pointC, temp_pointD):
        ''' Visualization of streaming data WorkThreadMain '''
        print(str(value), feed_type, str(feed_datetime), str(channal), str(strain_pointA), str(strain_pointB), str(strain_pointC), str(strain_pointD))
        # data = []

        # for point in ['A','B','C','D']:
        #     rows = []
        #     for row in range (1,4):
        #         cols = []
        #         for col in range (1,4):
        #             label = getattr(self, 'label{}{}{}'.format(point,row,col))
        #             # print(label.text())
        #             cols.append(float(label.text()))
        #         rows.append(cols)
        #     data.append(rows)
        # print(data)

        # print("xxxxxxxxxxxxxxx------------------->",self.labelA11.text())


        if(channal==0):

            self.pointA_name.setText(POINTA_NAME+" @ "+str(feed_datetime)) 
            self.pointB_name.setText(POINTB_NAME+" @ "+str(feed_datetime)) 
            self.pointC_name.setText(POINTC_NAME+" @ "+str(feed_datetime)) 
            self.pointD_name.setText(POINTD_NAME+" @ "+str(feed_datetime)) 

            self.labelA11.setText((str(("{:.1f}".format(round(temp_pointA, 1))))))
            self.labelB11.setText((str(("{:.1f}".format(round(temp_pointB, 1))))))
            self.labelC11.setText((str(("{:.1f}".format(round(temp_pointC, 1))))))

            if(float(temp_pointA) < float(POINTA_CHANNALA_ALERTT)):
                self.animA11.setStartValue(QColor("red"))
                self.animA11.setEndValue(QColor("white"))
                self.animA11.start()
            else:
                self.animA11.setStartValue(QColor("green"))
                self.animA11.setEndValue(QColor("green"))
                self.animA11.start()

            if(float(temp_pointB) < float(POINTB_CHANNALA_ALERTT)):
                self.animB11.setStartValue(QColor("red"))
                self.animB11.setEndValue(QColor("white"))
                self.animB11.start()
            else:
                self.animB11.setStartValue(QColor("green"))
                self.animB11.setEndValue(QColor("green"))
                self.animB11.start()

            if(float(temp_pointC) < float(POINTC_CHANNALA_ALERTT)):
                self.animC11.setStartValue(QColor("red"))
                self.animC11.setEndValue(QColor("white"))            
                self.animC11.start()
            else:
                self.animC11.setStartValue(QColor("green"))
                self.animC11.setEndValue(QColor("green"))
                self.animC11.start()

            self.labelA12.setText(str(int(strain_pointA)))
            self.labelB12.setText(str(int(strain_pointB)))
            self.labelC12.setText(str(int(strain_pointC)))

            if(float(strain_pointA) < float(POINTA_CHANNALA_ALERTT)):
                self.animA12.setStartValue(QColor("red"))
                self.animA12.setEndValue(QColor("white"))
                self.animA12.start()
            else:
                self.animA12.setStartValue(QColor("green"))
                self.animA12.setEndValue(QColor("green"))
                self.animA12.start()

            if(float(strain_pointB) < float(POINTB_CHANNALA_ALERTT)):
                self.animB12.setStartValue(QColor("red"))
                self.animB12.setEndValue(QColor("white"))
                self.animB12.start()
            else:
                self.animB12.setStartValue(QColor("green"))
                self.animB12.setEndValue(QColor("green"))
                self.animB12.start()

            if(float(strain_pointC) < float(POINTC_CHANNALA_ALERTT)):
                self.animC12.setStartValue(QColor("red"))
                self.animC12.setEndValue(QColor("white"))            
                self.animC12.start()
            else:
                self.animC12.setStartValue(QColor("green"))
                self.animC12.setEndValue(QColor("green"))
                self.animC12.start()


        if(channal==1):

            self.pointA_name.setText(POINTA_NAME+" @ "+str(feed_datetime)) 
            self.pointB_name.setText(POINTB_NAME+" @ "+str(feed_datetime)) 
            self.pointC_name.setText(POINTC_NAME+" @ "+str(feed_datetime)) 
            self.pointD_name.setText(POINTD_NAME+" @ "+str(feed_datetime)) 

            self.labelA21.setText((str(("{:.1f}".format(round(temp_pointA, 1))))))
            self.labelB21.setText((str(("{:.1f}".format(round(temp_pointB, 1))))))
            self.labelC21.setText((str(("{:.1f}".format(round(temp_pointC, 1))))))

            if(float(temp_pointA) < float(POINTA_CHANNALB_ALERTT)):
                self.animA21.setStartValue(QColor("red"))
                self.animA21.setEndValue(QColor("white"))
                self.animA21.start()
            else:
                self.animA21.setStartValue(QColor("green"))
                self.animA21.setEndValue(QColor("green"))
                self.animA21.start()

            if(float(temp_pointB) < float(POINTB_CHANNALB_ALERTT)):
                self.animB21.setStartValue(QColor("red"))
                self.animB21.setEndValue(QColor("white"))
                self.animB21.start()
            else:
                self.animB21.setStartValue(QColor("green"))
                self.animB21.setEndValue(QColor("green"))
                self.animB21.start()

            if(float(temp_pointC) < float(POINTC_CHANNALB_ALERTT)):
                self.animC21.setStartValue(QColor("red"))
                self.animC21.setEndValue(QColor("white"))            
                self.animC21.start()
            else:
                self.animC21.setStartValue(QColor("green"))
                self.animC21.setEndValue(QColor("green"))
                self.animC21.start()


            self.labelA22.setText(str(int(strain_pointA)))
            self.labelB22.setText(str(int(strain_pointB)))
            self.labelC22.setText(str(int(strain_pointC)))

            if(float(strain_pointA) < float(POINTA_CHANNALB_ALERTT)):
                self.animA22.setStartValue(QColor("red"))
                self.animA22.setEndValue(QColor("white"))
                self.animA22.start()
            else:
                self.animA22.setStartValue(QColor("green"))
                self.animA22.setEndValue(QColor("green"))
                self.animA22.start()

            if(float(strain_pointB) < float(POINTB_CHANNALB_ALERTT)):
                self.animB22.setStartValue(QColor("red"))
                self.animB22.setEndValue(QColor("white"))
                self.animB22.start()
            else:
                self.animB22.setStartValue(QColor("green"))
                self.animB22.setEndValue(QColor("green"))
                self.animB22.start()

            if(float(strain_pointC) < float(POINTC_CHANNALB_ALERTT)):
                self.animC22.setStartValue(QColor("red"))
                self.animC22.setEndValue(QColor("white"))            
                self.animC22.start()
            else:
                self.animC22.setStartValue(QColor("green"))
                self.animC22.setEndValue(QColor("green"))
                self.animC22.start()

        if(channal==2):

            self.pointA_name.setText(POINTA_NAME+" @ "+str(feed_datetime)) 
            self.pointB_name.setText(POINTB_NAME+" @ "+str(feed_datetime)) 
            self.pointC_name.setText(POINTC_NAME+" @ "+str(feed_datetime)) 
            self.pointD_name.setText(POINTD_NAME+" @ "+str(feed_datetime)) 


            self.labelA31.setText((str(("{:.1f}".format(round(temp_pointA, 1))))))
            self.labelB31.setText((str(("{:.1f}".format(round(temp_pointB, 1))))))
            self.labelC31.setText((str(("{:.1f}".format(round(temp_pointC, 1))))))

            if(float(temp_pointA) < float(POINTA_CHANNALC_ALERTT)):
                self.animA31.setStartValue(QColor("red"))
                self.animA31.setEndValue(QColor("white"))
                self.animA31.start()
            else:
                self.animA31.setStartValue(QColor("green"))
                self.animA31.setEndValue(QColor("green"))
                self.animA31.start()

            if(float(temp_pointB) < float(POINTB_CHANNALC_ALERTT)):
                self.animB31.setStartValue(QColor("red"))
                self.animB31.setEndValue(QColor("white"))
                self.animB31.start()
            else:
                self.animB31.setStartValue(QColor("green"))
                self.animB31.setEndValue(QColor("green"))
                self.animB31.start()

            if(float(temp_pointC) < float(POINTC_CHANNALC_ALERTT)):
                self.animC31.setStartValue(QColor("red"))
                self.animC31.setEndValue(QColor("white"))            
                self.animC31.start()
            else:
                self.animC31.setStartValue(QColor("green"))
                self.animC31.setEndValue(QColor("green"))
                self.animC31.start()

            self.labelA32.setText(str(int(strain_pointA)))
            self.labelB32.setText(str(int(strain_pointB)))
            self.labelC32.setText(str(int(strain_pointC)))

            if(float(strain_pointA) < float(POINTA_CHANNALC_ALERTT)):
                self.animA32.setStartValue(QColor("red"))
                self.animA32.setEndValue(QColor("white"))
                self.animA32.start()
            else:
                self.animA32.setStartValue(QColor("green"))
                self.animA32.setEndValue(QColor("green"))
                self.animA32.start()

            if(float(strain_pointB) < float(POINTB_CHANNALC_ALERTT)):
                self.animB32.setStartValue(QColor("red"))
                self.animB32.setEndValue(QColor("white"))
                self.animB32.start()
            else:
                self.animB32.setStartValue(QColor("green"))
                self.animB32.setEndValue(QColor("green"))
                self.animB32.start()

            if(float(strain_pointC) < float(POINTC_CHANNALC_ALERTT)):
                self.animC32.setStartValue(QColor("red"))
                self.animC32.setEndValue(QColor("white"))            
                self.animC32.start()
            else:
                self.animC32.setStartValue(QColor("green"))
                self.animC32.setEndValue(QColor("green"))
                self.animC32.start()

        if(channal==3):

            self.pointA_name.setText(POINTA_NAME+" @ "+str(feed_datetime)) 
            self.pointB_name.setText(POINTB_NAME+" @ "+str(feed_datetime)) 
            self.pointC_name.setText(POINTC_NAME+" @ "+str(feed_datetime)) 
            self.pointD_name.setText(POINTD_NAME+" @ "+str(feed_datetime)) 

            self.labelD11.setText((str(("{:.1f}".format(round(temp_pointD, 1))))))
            self.labelD21.setText((str(("{:.1f}".format(round(temp_pointD, 1))))))
            self.labelD31.setText((str(("{:.1f}".format(round(temp_pointD, 1))))))

            if(float(temp_pointD) < float(POINTD_CHANNALA_ALERTT)):
                self.animD11.setStartValue(QColor("red"))
                self.animD11.setEndValue(QColor("white"))
                self.animD11.start()

                self.animD21.setStartValue(QColor("red"))
                self.animD21.setEndValue(QColor("white"))
                self.animD21.start()

                self.animD31.setStartValue(QColor("red"))
                self.animD31.setEndValue(QColor("white"))
                self.animD31.start()

            else:
                self.animD11.setStartValue(QColor("green"))
                self.animD11.setEndValue(QColor("green"))
                self.animD11.start()

                self.animD21.setStartValue(QColor("green"))
                self.animD21.setEndValue(QColor("green"))
                self.animD21.start()

                self.animD31.setStartValue(QColor("green"))
                self.animD31.setEndValue(QColor("green"))
                self.animD31.start()


            self.labelD12.setText(str(int(strain_pointD)))
            self.labelD22.setText(str(int(strain_pointD)))
            self.labelD32.setText(str(int(strain_pointD)))

            if(float(strain_pointD) < float(POINTA_CHANNALC_ALERTT)):
                self.animD12.setStartValue(QColor("red"))
                self.animD12.setEndValue(QColor("white"))
                self.animD12.start()

                self.animD22.setStartValue(QColor("red"))
                self.animD22.setEndValue(QColor("white"))
                self.animD22.start()

                self.animD32.setStartValue(QColor("red"))
                self.animD32.setEndValue(QColor("white"))
                self.animD32.start()

            else:
                self.animD12.setStartValue(QColor("green"))
                self.animD12.setEndValue(QColor("green"))
                self.animD12.start()

                self.animD22.setStartValue(QColor("green"))
                self.animD22.setEndValue(QColor("green"))
                self.animD22.start()

                self.animD32.setStartValue(QColor("green"))
                self.animD32.setEndValue(QColor("green"))
                self.animD32.start()



        # if(Point == "A"):
        #     if(Phase == "A"):
        #         oMainwindow.threadMain.threadSignalMain.emit(0, 'A', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)


        # if(Point == "A"):
        #     if(Phase == "B"):
        #         oMainwindow.threadMain.threadSignalMain.emit(0, 'B', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)

    # def on_threadSignalMain(self, value, feed_type, feed_datetime, channal, strain_pointA, strain_pointB, strain_pointC, strain_pointD,
    #                         temp_pointA, temp_pointB, temp_pointC, temp_pointD):

        if(channal==99):
            if(value==0):
                if(feed_type=='A'):

                    self.labelA14.setText((str(("{:.1f}".format(round(strain_pointA, 1))))))
                    self.labelA13.setText((str(("{:.1f}".format(round(strain_pointB, 1))))))

                    if(float(strain_pointA) < float(POINTC_CHANNALC_ALERTT)):
                        self.animA14.setStartValue(QColor("red"))
                        self.animA14.setEndValue(QColor("white"))            
                        self.animA14.start()
                    else:
                        self.animA14.setStartValue(QColor("green"))
                        self.animA14.setEndValue(QColor("green"))
                        self.animA14.start()

                    if(float(strain_pointB) < float(POINTC_CHANNALC_ALERTT)):
                        self.animA13.setStartValue(QColor("red"))
                        self.animA13.setEndValue(QColor("white"))            
                        self.animA13.start()
                    else:
                        self.animA13.setStartValue(QColor("green"))
                        self.animA13.setEndValue(QColor("green"))
                        self.animA13.start()

                if(feed_type=='B'):
                    
                    self.labelA24.setText((str(("{:.1f}".format(round(strain_pointA, 1))))))
                    self.labelA23.setText((str(("{:.1f}".format(round(strain_pointB, 1))))))

                    if(float(strain_pointA) < float(POINTC_CHANNALC_ALERTT)):
                        self.animA24.setStartValue(QColor("red"))
                        self.animA24.setEndValue(QColor("white"))            
                        self.animA24.start()
                    else:
                        self.animA24.setStartValue(QColor("green"))
                        self.animA24.setEndValue(QColor("green"))
                        self.animA24.start()

                    if(float(strain_pointB) < float(POINTC_CHANNALC_ALERTT)):
                        self.animA23.setStartValue(QColor("red"))
                        self.animA23.setEndValue(QColor("white"))            
                        self.animA23.start()
                    else:
                        self.animA23.setStartValue(QColor("green"))
                        self.animA23.setEndValue(QColor("green"))
                        self.animA23.start()

                if(feed_type=='C'):
                    
                    self.labelA34.setText((str(("{:.1f}".format(round(strain_pointA, 1))))))
                    self.labelA33.setText((str(("{:.1f}".format(round(strain_pointB, 1))))))

                    if(float(strain_pointA) < float(POINTC_CHANNALC_ALERTT)):
                        self.animA34.setStartValue(QColor("red"))
                        self.animA34.setEndValue(QColor("white"))            
                        self.animA34.start()
                    else:
                        self.animA34.setStartValue(QColor("green"))
                        self.animA34.setEndValue(QColor("green"))
                        self.animA34.start()

                    if(float(strain_pointB) < float(POINTC_CHANNALC_ALERTT)):
                        self.animA33.setStartValue(QColor("red"))
                        self.animA33.setEndValue(QColor("white"))            
                        self.animA33.start()
                    else:
                        self.animA33.setStartValue(QColor("green"))
                        self.animA33.setEndValue(QColor("green"))
                        self.animA33.start()


            if(value==1):
                if(feed_type=='A'):

                    self.labelB14.setText((str(("{:.1f}".format(round(strain_pointA, 1))))))
                    self.labelB13.setText((str(("{:.1f}".format(round(strain_pointB, 1))))))

                    if(float(strain_pointA) < float(POINTC_CHANNALC_ALERTT)):
                        self.animB14.setStartValue(QColor("red"))
                        self.animB14.setEndValue(QColor("white"))            
                        self.animB14.start()
                    else:
                        self.animB14.setStartValue(QColor("green"))
                        self.animB14.setEndValue(QColor("green"))
                        self.animB14.start()

                    if(float(strain_pointB) < float(POINTC_CHANNALC_ALERTT)):
                        self.animB13.setStartValue(QColor("red"))
                        self.animB13.setEndValue(QColor("white"))            
                        self.animB13.start()
                    else:
                        self.animB13.setStartValue(QColor("green"))
                        self.animB13.setEndValue(QColor("green"))
                        self.animB13.start()

                if(feed_type=='B'):
                    
                    self.labelB24.setText((str(("{:.1f}".format(round(strain_pointA, 1))))))
                    self.labelB23.setText((str(("{:.1f}".format(round(strain_pointB, 1))))))

                    if(float(strain_pointA) < float(POINTC_CHANNALC_ALERTT)):
                        self.animB24.setStartValue(QColor("red"))
                        self.animB24.setEndValue(QColor("white"))            
                        self.animB24.start()
                    else:
                        self.animB24.setStartValue(QColor("green"))
                        self.animB24.setEndValue(QColor("green"))
                        self.animB24.start()

                    if(float(strain_pointB) < float(POINTC_CHANNALC_ALERTT)):
                        self.animB23.setStartValue(QColor("red"))
                        self.animB23.setEndValue(QColor("white"))            
                        self.animB23.start()
                    else:
                        self.animB23.setStartValue(QColor("green"))
                        self.animB23.setEndValue(QColor("green"))
                        self.animB23.start()

                if(feed_type=='C'):
                    
                    self.labelB34.setText((str(("{:.1f}".format(round(strain_pointA, 1))))))
                    self.labelB33.setText((str(("{:.1f}".format(round(strain_pointB, 1))))))

                    if(float(strain_pointA) < float(POINTC_CHANNALC_ALERTT)):
                        self.animB34.setStartValue(QColor("red"))
                        self.animB34.setEndValue(QColor("white"))            
                        self.animB34.start()
                    else:
                        self.animB34.setStartValue(QColor("green"))
                        self.animB34.setEndValue(QColor("green"))
                        self.animB34.start()

                    if(float(strain_pointB) < float(POINTC_CHANNALC_ALERTT)):
                        self.animB33.setStartValue(QColor("red"))
                        self.animB33.setEndValue(QColor("white"))            
                        self.animB33.start()
                    else:
                        self.animB33.setStartValue(QColor("green"))
                        self.animB33.setEndValue(QColor("green"))
                        self.animB33.start()

            if(value==2):
                if(feed_type=='A'):

                    self.labelC14.setText((str(("{:.1f}".format(round(strain_pointA, 1))))))
                    self.labelC13.setText((str(("{:.1f}".format(round(strain_pointB, 1))))))

                    if(float(strain_pointA) < float(POINTC_CHANNALC_ALERTT)):
                        self.animC14.setStartValue(QColor("red"))
                        self.animC14.setEndValue(QColor("white"))            
                        self.animC14.start()
                    else:
                        self.animC14.setStartValue(QColor("green"))
                        self.animC14.setEndValue(QColor("green"))
                        self.animC14.start()

                    if(float(strain_pointB) < float(POINTC_CHANNALC_ALERTT)):
                        self.animC13.setStartValue(QColor("red"))
                        self.animC13.setEndValue(QColor("white"))            
                        self.animC13.start()
                    else:
                        self.animC13.setStartValue(QColor("green"))
                        self.animC13.setEndValue(QColor("green"))
                        self.animC13.start()

                if(feed_type=='B'):
                    
                    self.labelC24.setText((str(("{:.1f}".format(round(strain_pointA, 1))))))
                    self.labelC23.setText((str(("{:.1f}".format(round(strain_pointB, 1))))))

                    if(float(strain_pointA) < float(POINTC_CHANNALC_ALERTT)):
                        self.animC24.setStartValue(QColor("red"))
                        self.animC24.setEndValue(QColor("white"))            
                        self.animC24.start()
                    else:
                        self.animC24.setStartValue(QColor("green"))
                        self.animC24.setEndValue(QColor("green"))
                        self.animC24.start()

                    if(float(strain_pointB) < float(POINTC_CHANNALC_ALERTT)):
                        self.animC23.setStartValue(QColor("red"))
                        self.animC23.setEndValue(QColor("white"))            
                        self.animC23.start()
                    else:
                        self.animC23.setStartValue(QColor("green"))
                        self.animC23.setEndValue(QColor("green"))
                        self.animC23.start()

                if(feed_type=='C'):
                    
                    self.labelC34.setText((str(("{:.1f}".format(round(strain_pointA, 1))))))
                    self.labelC33.setText((str(("{:.1f}".format(round(strain_pointB, 1))))))

                    if(float(strain_pointA) < float(POINTC_CHANNALC_ALERTT)):
                        self.animC34.setStartValue(QColor("red"))
                        self.animC34.setEndValue(QColor("white"))            
                        self.animC34.start()
                    else:
                        self.animC34.setStartValue(QColor("green"))
                        self.animC34.setEndValue(QColor("green"))
                        self.animC34.start()

                    if(float(strain_pointB) < float(POINTC_CHANNALC_ALERTT)):
                        self.animC33.setStartValue(QColor("red"))
                        self.animC33.setEndValue(QColor("white"))            
                        self.animC33.start()
                    else:
                        self.animC33.setStartValue(QColor("green"))
                        self.animC33.setEndValue(QColor("green"))
                        self.animC33.start()

            if(value==3):
                if(feed_type=='A'):

                    self.labelD14.setText((str(("{:.1f}".format(round(strain_pointA, 1))))))
                    self.labelD13.setText((str(("{:.1f}".format(round(strain_pointB, 1))))))

                    self.labelD24.setText((str(("{:.1f}".format(round(strain_pointA, 1))))))
                    self.labelD23.setText((str(("{:.1f}".format(round(strain_pointB, 1))))))

                    self.labelD34.setText((str(("{:.1f}".format(round(strain_pointA, 1))))))
                    self.labelD33.setText((str(("{:.1f}".format(round(strain_pointB, 1))))))

                    if(float(strain_pointA) < float(POINTC_CHANNALC_ALERTT)):
                        self.animD14.setStartValue(QColor("red"))
                        self.animD14.setEndValue(QColor("white"))            
                        self.animD14.start()

                        self.animD24.setStartValue(QColor("red"))
                        self.animD24.setEndValue(QColor("white"))            
                        self.animD24.start()

                        self.animD34.setStartValue(QColor("red"))
                        self.animD34.setEndValue(QColor("white"))            
                        self.animD34.start()

                    else:
                        self.animD14.setStartValue(QColor("green"))
                        self.animD14.setEndValue(QColor("green"))
                        self.animD14.start()

                        self.animD24.setStartValue(QColor("green"))
                        self.animD24.setEndValue(QColor("green"))
                        self.animD24.start()

                        self.animD34.setStartValue(QColor("green"))
                        self.animD34.setEndValue(QColor("green"))
                        self.animD34.start()

                    if(float(strain_pointB) < float(POINTC_CHANNALC_ALERTT)):
                        self.animD13.setStartValue(QColor("red"))
                        self.animD13.setEndValue(QColor("white"))            
                        self.animD13.start()

                        self.animD23.setStartValue(QColor("red"))
                        self.animD23.setEndValue(QColor("white"))            
                        self.animD23.start()

                        self.animD33.setStartValue(QColor("red"))
                        self.animD33.setEndValue(QColor("white"))            
                        self.animD33.start()

                    else:
                        self.animD13.setStartValue(QColor("green"))
                        self.animD13.setEndValue(QColor("green"))
                        self.animD13.start()

                        self.animD23.setStartValue(QColor("green"))
                        self.animD23.setEndValue(QColor("green"))
                        self.animD23.start()

                        self.animD33.setStartValue(QColor("green"))
                        self.animD33.setEndValue(QColor("green"))
                        self.animD33.start()


    def mouseMoveEvent(self, event):
        self.setWindowTitle('RTTR Monitoring System: [%d : %d]' % (event.x(), event.y()))
        super(MainWindow, self).mouseMoveEvent(event)
        # self.labelA12.setText(str(value))

    def resizeEvent(self, event):

        print("------------------------------------===============", SITE)

        if(SITE == 'Kanom'):
            x = self.size().width()
            y = self.size().height()
            scale_width = (x/1280)
            scale_height = (y/720)
            print("Scale->",scale_width,scale_height)

            self.pointA_name.resize(int(250*scale_width), int(20*scale_height))
            self.pointA_name.move(int(410*scale_width), int(505*scale_height))
            self.pointB_name.resize(int(250*scale_width), int(20*scale_height))
            self.pointB_name.move(int(250*scale_width), int(330*scale_height))
            self.pointC_name.resize(int(250*scale_width), int(20*scale_height))
            self.pointC_name.move(int(355*scale_width), int(155*scale_height))
            self.pointD_name.resize(int(250*scale_width), int(20*scale_height))
            self.pointD_name.move(int(770*scale_width), int(25*scale_height))

            # Point A
            self.background_point1.resize(int(self.cardwidth*scale_width), int(self.cardheight*scale_height))
            self.background_point1.move(int(400*scale_width), int(500*scale_height))

            self.labelA11.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA11.move(int(473*scale_width), int(563*scale_height))

            self.labelA12.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA12.move(int(540*scale_width), int(563*scale_height))

            self.labelA13.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA13.move(int(607*scale_width), int(563*scale_height))

            self.labelA14.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA14.move(int(674*scale_width), int(563*scale_height))

            self.labelA21.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA21.move(int(473*scale_width), int(598*scale_height))

            self.labelA22.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA22.move(int(540*scale_width), int(598*scale_height))

            self.labelA23.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA23.move(int(607*scale_width), int(598*scale_height))

            self.labelA24.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA24.move(int(674*scale_width), int(598*scale_height))

            self.labelA31.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA31.move(int(473*scale_width), int(633*scale_height))

            self.labelA32.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA32.move(int(540*scale_width), int(633*scale_height))

            self.labelA33.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA33.move(int(607*scale_width), int(633*scale_height))

            self.labelA34.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA34.move(int(674*scale_width), int(633*scale_height))

        # Point B
            self.background_point2.resize(int(self.cardwidth*scale_width), int(self.cardheight*scale_height))
            self.background_point2.move(int(240*scale_width), int(325*scale_height))

            self.labelB11.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB11.move(int(313*scale_width), int(388*scale_height))

            self.labelB12.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB12.move(int(380*scale_width), int(388*scale_height))

            self.labelB13.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB13.move(int(447*scale_width), int(388*scale_height))

            self.labelB14.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB14.move(int(514*scale_width), int(388*scale_height))


            self.labelB21.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB21.move(int(313*scale_width), int(423*scale_height))

            self.labelB22.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB22.move(int(380*scale_width), int(423*scale_height))

            self.labelB23.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB23.move(int(447*scale_width), int(423*scale_height))

            self.labelB24.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB24.move(int(514*scale_width), int(423*scale_height))


            self.labelB31.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB31.move(int(313*scale_width), int(458*scale_height))

            self.labelB32.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB32.move(int(380*scale_width), int(458*scale_height))

            self.labelB33.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB33.move(int(447*scale_width), int(458*scale_height))

            self.labelB34.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB34.move(int(514*scale_width), int(458*scale_height))

            # Point C
            self.background_point3.resize(int(self.cardwidth*scale_width), int(self.cardheight*scale_height))
            self.background_point3.move(int(345*scale_width), int(150*scale_height))

            self.labelC11.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC11.move(int(418*scale_width), int(213*scale_height))

            self.labelC12.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC12.move(int(485*scale_width), int(213*scale_height))

            self.labelC13.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC13.move(int(552*scale_width), int(213*scale_height))

            self.labelC14.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC14.move(int(619*scale_width), int(213*scale_height))

            self.labelC21.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC21.move(int(418*scale_width), int(248*scale_height))

            self.labelC22.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC22.move(int(485*scale_width), int(248*scale_height))

            self.labelC23.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC23.move(int(552*scale_width), int(248*scale_height))

            self.labelC24.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC24.move(int(619*scale_width), int(248*scale_height))

            self.labelC31.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC31.move(int(418*scale_width), int(283*scale_height))

            self.labelC32.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC32.move(int(485*scale_width), int(283*scale_height))

            self.labelC33.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC33.move(int(552*scale_width), int(283*scale_height))

            self.labelC34.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC34.move(int(619*scale_width), int(283*scale_height))

            # Point D
            self.background_point4.resize(int(self.cardwidth*scale_width), int(self.cardheight*scale_height))
            self.background_point4.move(int(760*scale_width), int(20*scale_height))

            self.labelD11.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD11.move(int(833*scale_width), int(83*scale_height)) 

            self.labelD12.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD12.move(int(900*scale_width), int(83*scale_height))

            self.labelD13.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD13.move(int(967*scale_width), int(83*scale_height))

            self.labelD14.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD14.move(int(1034*scale_width), int(83*scale_height))

            self.labelD21.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD21.move(int(833*scale_width), int(118*scale_height))

            self.labelD22.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD22.move(int(900*scale_width), int(118*scale_height))

            self.labelD23.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD23.move(int(967*scale_width), int(118*scale_height))

            self.labelD24.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD24.move(int(1034*scale_width), int(118*scale_height))

            self.labelD31.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD31.move(int(833*scale_width), int(153*scale_height))

            self.labelD32.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD32.move(int(900*scale_width), int(153*scale_height))

            self.labelD33.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD33.move(int(967*scale_width), int(153*scale_height))

            self.labelD34.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD34.move(int(1034*scale_width), int(153*scale_height))

        if(SITE == 'Samui'):

            x = self.size().width()
            y = self.size().height()
            scale_width = (x/1280)
            scale_height = (y/720)
            print("Scale->",scale_width,scale_height)

            plabelwidth = 250
            plabelheight = 20

            # Point A
            boxA_x = 220
            boxA_y = 530
            pointA_name_x = boxA_x+8
            pointA_name_y = boxA_y+4
    
            labelA11_x = boxA_x + 72
            labelA11_y = boxA_y + 62
            labelA12_x = boxA_x + 72 + 67
            labelA12_y = labelA11_y
            labelA13_x = boxA_x + 72 + 67 + 67
            labelA13_y = labelA11_y
            labelA14_x = boxA_x + 72 + 67 + 67 + 67
            labelA14_y = labelA11_y

            labelA21_x = boxA_x + 72
            labelA21_y = boxA_y + 97
            labelA22_x = boxA_x + 72 + 67
            labelA22_y = labelA21_y
            labelA23_x = boxA_x + 72 + 67 + 67
            labelA23_y = labelA21_y
            labelA24_x = boxA_x + 72 + 67 + 67 + 67
            labelA24_y = labelA21_y

            labelA31_x = boxA_x + 72
            labelA31_y = boxA_y + 132
            labelA32_x = boxA_x + 72 + 67
            labelA32_y = labelA31_y
            labelA33_x = boxA_x + 72 + 67 + 67
            labelA33_y = labelA31_y
            labelA34_x = boxA_x + 72 + 67 + 67 + 67
            labelA34_y = labelA31_y


            self.background_point1.resize(int(self.cardwidth*scale_width), int(self.cardheight*scale_height))
            self.background_point1.move(int(boxA_x*scale_width), int(boxA_y*scale_height))

            self.pointA_name.resize(int(250*scale_width), int(20*scale_height))
            self.pointA_name.move(int(pointA_name_x*scale_width), int(pointA_name_y*scale_height))

            self.labelA11.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA11.move(int(labelA11_x*scale_width), int(labelA11_y*scale_height))

            self.labelA12.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA12.move(int(labelA12_x*scale_width), int(labelA12_y*scale_height))

            self.labelA13.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA13.move(int(labelA13_x*scale_width), int(labelA13_y*scale_height))

            self.labelA14.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA14.move(int(labelA14_x*scale_width), int(labelA14_y*scale_height))

            self.labelA21.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA21.move(int(labelA21_x*scale_width), int(labelA21_y*scale_height))

            self.labelA22.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA22.move(int(labelA22_x*scale_width), int(labelA22_y*scale_height))

            self.labelA23.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA23.move(int(labelA23_x*scale_width), int(labelA23_y*scale_height))

            self.labelA24.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA24.move(int(labelA24_x*scale_width), int(labelA24_y*scale_height))

            self.labelA31.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA31.move(int(labelA31_x*scale_width), int(labelA31_y*scale_height))

            self.labelA32.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA32.move(int(labelA32_x*scale_width), int(labelA32_y*scale_height))

            self.labelA33.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA33.move(int(labelA33_x*scale_width), int(labelA33_y*scale_height))

            self.labelA34.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelA34.move(int(labelA34_x*scale_width), int(labelA34_y*scale_height))

        # Point B

            boxB_x = 920
            boxB_y = 225

            pointB_name_x = boxB_x+8
            pointB_name_y = boxB_y+4

            labelB11_x = boxB_x + 72
            labelB11_y = boxB_y + 62
            labelB12_x = boxB_x + 72 + 67
            labelB12_y = labelB11_y
            labelB13_x = boxB_x + 72 + 67 + 67
            labelB13_y = labelB11_y
            labelB14_x = boxB_x + 72 + 67 + 67 + 67
            labelB14_y = labelB11_y

            labelB21_x = boxB_x + 72
            labelB21_y = boxB_y + 97
            labelB22_x = boxB_x + 72 + 67
            labelB22_y = labelB21_y
            labelB23_x = boxB_x + 72 + 67 + 67
            labelB23_y = labelB21_y
            labelB24_x = boxB_x + 72 + 67 + 67 + 67
            labelB24_y = labelB21_y

            labelB31_x = boxB_x + 72
            labelB31_y = boxB_y + 132
            labelB32_x = boxB_x + 72 + 67
            labelB32_y = labelB31_y
            labelB33_x = boxB_x + 72 + 67 + 67
            labelB33_y = labelB31_y
            labelB34_x = boxB_x + 72 + 67 + 67 + 67
            labelB34_y = labelB31_y

            self.background_point2.resize(int(self.cardwidth*scale_width), int(self.cardheight*scale_height))
            self.background_point2.move(int(boxB_x*scale_width), int(boxB_y*scale_height))

            self.pointB_name.resize(int(250*scale_width), int(20*scale_height))
            self.pointB_name.move(int(pointB_name_x*scale_width), int(pointB_name_y*scale_height))

            self.labelB11.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB11.move(int(labelB11_x*scale_width), int(labelB11_y*scale_height))

            self.labelB12.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB12.move(int(labelB12_x*scale_width), int(labelB12_y*scale_height))

            self.labelB13.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB13.move(int(labelB13_x*scale_width), int(labelB13_y*scale_height))

            self.labelB14.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB14.move(int(labelB14_x*scale_width), int(labelB14_y*scale_height))

            self.labelB21.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB21.move(int(labelB21_x*scale_width), int(labelB21_y*scale_height))

            self.labelB22.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB22.move(int(labelB22_x*scale_width), int(labelB22_y*scale_height))

            self.labelB23.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB23.move(int(labelB23_x*scale_width), int(labelB23_y*scale_height))

            self.labelB24.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB24.move(int(labelB24_x*scale_width), int(labelB24_y*scale_height))

            self.labelB31.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB31.move(int(labelB31_x*scale_width), int(labelB31_y*scale_height))

            self.labelB32.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB32.move(int(labelB32_x*scale_width), int(labelB32_y*scale_height))

            self.labelB33.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB33.move(int(labelB33_x*scale_width), int(labelB32_y*scale_height))

            self.labelB34.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelB34.move(int(labelB34_x*scale_width), int(labelB32_y*scale_height))

            # Point C
            boxC_x = 770
            boxC_y = 20

            pointC_name_x = boxC_x+8
            pointC_name_y = boxC_y+4

            labelC11_x = boxC_x + 72
            labelC11_y = boxC_y + 62
            labelC12_x = boxC_x + 72 + 67
            labelC12_y = labelC11_y
            labelC13_x = boxC_x + 72 + 67 + 67
            labelC13_y = labelC11_y
            labelC14_x = boxC_x + 72 + 67 + 67 + 67
            labelC14_y = labelC11_y

            labelC21_x = boxC_x + 72
            labelC21_y = boxC_y + 97
            labelC22_x = boxC_x + 72 + 67
            labelC22_y = labelC21_y
            labelC23_x = boxC_x + 72 + 67 + 67
            labelC23_y = labelC21_y
            labelC24_x = boxC_x + 72 + 67 + 67 + 67
            labelC24_y = labelC21_y

            labelC31_x = boxC_x + 72
            labelC31_y = boxC_y + 132
            labelC32_x = boxC_x + 72 + 67
            labelC32_y = labelC31_y
            labelC33_x = boxC_x + 72 + 67 + 67
            labelC33_y = labelC31_y
            labelC34_x = boxC_x + 72 + 67 + 67 + 67
            labelC34_y = labelC31_y

            self.background_point3.resize(int(self.cardwidth*scale_width), int(self.cardheight*scale_height))
            self.background_point3.move(int(boxC_x*scale_width), int(boxC_y*scale_height))

            self.pointC_name.resize(int(250*scale_width), int(20*scale_height))
            self.pointC_name.move(int(pointC_name_x*scale_width), int(pointC_name_y*scale_height))

            self.labelC11.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC11.move(int(labelC11_x*scale_width), int(labelC11_y*scale_height))

            self.labelC12.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC12.move(int(labelC12_x*scale_width), int(labelC12_y*scale_height))

            self.labelC13.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC13.move(int(labelC13_x*scale_width), int(labelC13_y*scale_height))

            self.labelC14.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC14.move(int(labelC14_x*scale_width), int(labelC14_y*scale_height))

            self.labelC21.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC21.move(int(labelC21_x*scale_width), int(labelC21_y*scale_height))

            self.labelC22.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC22.move(int(labelC22_x*scale_width), int(labelC22_y*scale_height))

            self.labelC23.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC23.move(int(labelC23_x*scale_width), int(labelC23_y*scale_height))

            self.labelC24.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC24.move(int(labelC24_x*scale_width), int(labelC24_y*scale_height))

            self.labelC31.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC31.move(int(labelC31_x*scale_width), int(labelC31_y*scale_height))

            self.labelC32.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC32.move(int(labelC32_x*scale_width), int(labelC32_y*scale_height))

            self.labelC33.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC33.move(int(labelC33_x*scale_width), int(labelC33_y*scale_height))

            self.labelC34.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelC34.move(int(labelC34_x*scale_width), int(labelC34_y*scale_height))

            # Point D
            boxD_x = 355
            boxD_y = 200

            pointD_name_x = boxD_x+8
            pointD_name_y = boxD_y+4

            labelD11_x = boxD_x + 72
            labelD11_y = boxD_y + 62
            labelD12_x = boxD_x + 72 + 67
            labelD12_y = labelD11_y
            labelD13_x = boxD_x + 72 + 67 + 67
            labelD13_y = labelD11_y
            labelD14_x = boxD_x + 72 + 67 + 67 + 67
            labelD14_y = labelD11_y

            labelD21_x = boxD_x + 72
            labelD21_y = boxD_y + 97
            labelD22_x = boxD_x + 72 + 67
            labelD22_y = labelD21_y
            labelD23_x = boxD_x + 72 + 67 + 67
            labelD23_y = labelD21_y
            labelD24_x = boxD_x + 72 + 67 + 67 + 67
            labelD24_y = labelD21_y

            labelD31_x = boxD_x + 72
            labelD31_y = boxD_y + 132
            labelD32_x = boxD_x + 72 + 67
            labelD32_y = labelD31_y
            labelD33_x = boxD_x + 72 + 67 + 67
            labelD33_y = labelD31_y
            labelD34_x = boxD_x + 72 + 67 + 67 + 67
            labelD34_y = labelD31_y

            self.background_point4.resize(int(self.cardwidth*scale_width), int(self.cardheight*scale_height))
            self.background_point4.move(int(boxD_x*scale_width), int(boxD_y*scale_height))

            self.pointD_name.resize(int(250*scale_width), int(20*scale_height))
            self.pointD_name.move(int(pointD_name_x*scale_width), int(pointD_name_y*scale_height))

            self.labelD11.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD11.move(int(labelD11_x*scale_width), int(labelD11_y*scale_height)) 

            self.labelD12.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD12.move(int(labelD12_x*scale_width), int(labelD12_y*scale_height))

            self.labelD13.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD13.move(int(labelD13_x*scale_width), int(labelD13_y*scale_height))

            self.labelD14.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD14.move(int(labelD14_x*scale_width), int(labelD14_y*scale_height))

            self.labelD21.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD21.move(int(labelD21_x*scale_width), int(labelD21_y*scale_height))

            self.labelD22.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD22.move(int(labelD22_x*scale_width), int(labelD22_y*scale_height))

            self.labelD23.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD23.move(int(labelD23_x*scale_width), int(labelD23_y*scale_height))

            self.labelD24.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD24.move(int(labelD24_x*scale_width), int(labelD24_y*scale_height))

            self.labelD31.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD31.move(int(labelD31_x*scale_width), int(labelD31_y*scale_height))

            self.labelD32.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD32.move(int(labelD32_x*scale_width), int(labelD32_y*scale_height))

            self.labelD33.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD33.move(int(labelD33_x*scale_width), int(labelD33_y*scale_height))

            self.labelD34.resize(int(self.labelwidth*scale_width), int(self.labelheight*scale_height))
            self.labelD34.move(int(labelD34_x*scale_width), int(labelD34_y*scale_height))


    def start_stop_feed(self):
        cM = random.randrange(15, 20)
        if self.threadMain is None:
            self.threadMain = WorkThreadMain(cM)
            self.threadMain.threadSignalMain.connect(self.on_threadSignalMain)
            self.threadMain.start()
            self.testfeed_action.setText("Stop Feed")

        else:
            self.threadMain.terminate()         
            self.threadMain = None
            self.testfeed_action.setText("Start Feed")

    def on_any_event(self, event):
        print(event.src_path, event.event_type)
 

class ReportingWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowState(Qt.WindowActive)
        # self.setWindowFlags(Qt.Window)
        self.setWindowTitle('Reports')
        self.setMinimumSize(760, 640)
        self.setMaximumSize(700, 640)
        # self.move(20,20)
        if(os.path.isdir(PROG_INPUT)):
            print("DTS_INPUT--->",PROG_INPUT)

        self.xxxx()

    def xxxx(self):

        configSite = "Samui"
        keytagname = "Channel 0"
        day = datetime.now()
        report_date_display =  day.strftime("%d/%m/%Y") 
        #     current_datetime = datetime.now()
        excel_date = day.strftime("%Y%m%d")    

        self.dirDaily = APP_PATH +"/reports"


        # day = sdate + timedelta(days=i)

        # report_date = day.strftime("%Y-%m-%d")
        excel_date = day.strftime("%Y%m%d")        
        # report_date_display =  day.strftime("%d/%m/%Y")            
        # yesterday = (sdate - timedelta(1)).strftime('%Y-%m-%d')


        workbook = xlsxwriter.Workbook(self.dirDaily+"/"+excel_date+'_PEA_Daily_report_'+keytagname+'.xlsx')
        worksheet = workbook.add_worksheet()
        
        worksheet.set_paper(9)
        worksheet.fit_to_pages(1, 0)
        
        worksheet.insert_image('A1', 'pea.jpg', {'x_scale': 0.5, 'y_scale': 0.5})                
        worksheet.set_column('A:H', 12)
        worksheet.set_column('I:K', 14)
        worksheet.set_row(1, 40)        
        worksheet.set_row(2, 40)
        # worksheet.set_top(1)

        cell_format_header = workbook.add_format({'align': 'center',
                            'valign': 'vcenter',
                            'bold': True, 'font_size': 14})
                        
        worksheet.merge_range('C2:I2', "PEA. PROTECTION AND RELAY DIVISION.", cell_format_header)
        worksheet.merge_range('C3:I3', "200 Ngamwongwan Road, Chatuchak, Bangkok 10900 Thailand.", cell_format_header)
        worksheet.merge_range('A4:K4', "Distributed Temperature & Strain Sensing", cell_format_header)
        worksheet.merge_range('C5:I5', "Date: " + str(report_date_display), cell_format_header)         
        
        first_row = 0
        first_col = 0
        rows_count = 11
        cols_count = 11

        # top left corner
        worksheet.conditional_format(first_row, first_col,
                                    first_row, first_col,
                                    {'type': 'formula', 'criteria': 'True',
                                    'format': workbook.add_format({'top': 1, 'left': 1})})
        # top right corner
        worksheet.conditional_format(first_row, first_col + cols_count - 1,
                                    first_row, first_col + cols_count - 1,
                                    {'type': 'formula', 'criteria': 'True',
                                    'format': workbook.add_format({'top': 1, 'right': 1})})
        # bottom left corner
        worksheet.conditional_format(first_row + rows_count - 1, first_col,
                                    first_row + rows_count - 1, first_col,
                                    {'type': 'formula', 'criteria': 'True',
                                    'format': workbook.add_format({'bottom': 1, 'left': 1})})
        # bottom right corner
        worksheet.conditional_format(first_row + rows_count - 1, first_col + cols_count - 1,
                                    first_row + rows_count - 1, first_col + cols_count - 1,
                                    {'type': 'formula', 'criteria': 'True',
                                    'format': workbook.add_format({'bottom': 1, 'right': 1})})

        # top
        worksheet.conditional_format(first_row, first_col + 1,
                                    first_row, first_col + cols_count - 2,
                                    {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'top': 1})})
        # left
        worksheet.conditional_format(first_row + 1, first_col,
                                    first_row + rows_count - 2, first_col,
                                    {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'left': 1})})
        # bottom
        worksheet.conditional_format(first_row + rows_count - 1, first_col + 1,
                                    first_row + rows_count - 1, first_col + cols_count - 2,
                                    {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'bottom': 1})})
        # right
        worksheet.conditional_format(first_row + 1,              first_col + cols_count - 1,
                                    first_row + rows_count - 2, first_col + cols_count - 1,
                                    {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'right': 1})})



        # border_format=workbook.add_format({'border':1})
        # worksheet.conditional_format('A8:K56',{'type':'blanks','format' : border_format} )



        # cell_format_header_data = workbook.add_format({'align': 'center',
        #                     'valign': 'vcenter',
        #                     'bold': True, 'font_size': 12,'border':1})                    

        # worksheet.write('A8', 'Date', cell_format_header_data)
        # worksheet.write('B8', 'Time', cell_format_header_data)
        # worksheet.write('C8', 'kV(AB)', cell_format_header_data)
        # worksheet.write('D8', 'kV(BC)', cell_format_header_data)
        # worksheet.write('E8', 'kV(CA)', cell_format_header_data)
        # worksheet.write('F8', 'IA', cell_format_header_data)
        # worksheet.write('G8', 'IB', cell_format_header_data)
        # worksheet.write('H8', 'IC', cell_format_header_data)
        # worksheet.write('I8', 'MW', cell_format_header_data)
        # worksheet.write('J8', 'Mvar', cell_format_header_data)
        # worksheet.write('K8', '%PF', cell_format_header_data)

        workbook.close()


class SettingWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowState(Qt.WindowActive)
        # self.setWindowFlags(Qt.Window)
        self.setWindowTitle('Setting')
        self.setMinimumSize(760, 640)
        self.setMaximumSize(700, 640)
        # self.move(20,20)
        if(os.path.isdir(PROG_INPUT)):
            print("DTS_INPUT--->",PROG_INPUT)

        layout = QVBoxLayout()
        groupbox = QGroupBox("Configuration")    
        grid0 = QGridLayout()

        self.groupbox_pointa = QGroupBox("Point A")
        self.groupbox_pointb = QGroupBox("Point B")
        self.groupbox_pointc = QGroupBox("Point C")
        self.groupbox_pointd = QGroupBox("Point D")

        #Setting PointA
        self.grid_pointa = QGridLayout()
        self.pointa_distance_lable = QLabel("Distance  From:")
        self.pointa_to_lable = QLabel("To:")
        self.pointa_from_input = QLineEdit()
        self.pointa_to_input = QLineEdit()
        self.pointa_to_lable.setAlignment(Qt.AlignCenter)
        self.pointa_from_input.setText(POINTA_FROM)
        self.pointa_to_input.setText(POINTA_TO)

        self.grid_pointa.addWidget(self.pointa_distance_lable, 0, 0)
        self.grid_pointa.addWidget(self.pointa_from_input, 0, 1)
        self.grid_pointa.addWidget(self.pointa_to_lable, 0, 2)
        self.grid_pointa.addWidget(self.pointa_to_input, 0, 3)

        self.pointa_channala_alert_lable = QLabel("Phase A Alert >=")
        self.pointa_channalb_alert_lable = QLabel("Phase B Alert >=")
        self.pointa_channalc_alert_lable = QLabel("Phase C Alert >=")
        self.pointa_channala_alertt_input = QLineEdit()
        self.pointa_channalb_alertt_input = QLineEdit()
        self.pointa_channalc_alertt_input = QLineEdit()
        self.pointa_channala_alerts_input = QLineEdit()
        self.pointa_channalb_alerts_input = QLineEdit()
        self.pointa_channalc_alerts_input = QLineEdit()
        self.pointa_channala_alertc_input = QLineEdit()
        self.pointa_channalb_alertc_input = QLineEdit()
        self.pointa_channalc_alertc_input = QLineEdit()

        self.pointa_channala_alertt_input.setText(str(POINTA_CHANNALA_ALERTT))
        self.pointa_channala_alerts_input.setText(str(POINTA_CHANNALA_ALERTS))
        self.pointa_channala_alertc_input.setText(str(POINTA_CHANNALA_ALERTC))
        self.pointa_channalb_alertt_input.setText(str(POINTA_CHANNALB_ALERTT))
        self.pointa_channalb_alerts_input.setText(str(POINTA_CHANNALB_ALERTS))
        self.pointa_channalb_alertc_input.setText(str(POINTA_CHANNALB_ALERTC))
        self.pointa_channalc_alertt_input.setText(str(POINTA_CHANNALC_ALERTT))
        self.pointa_channalc_alerts_input.setText(str(POINTA_CHANNALC_ALERTS))
        self.pointa_channalc_alertc_input.setText(str(POINTA_CHANNALC_ALERTC))

        self.pointa_temp_lable = QLabel("Temp(°C)")
        self.pointa_strain_lable = QLabel("Strain")
        self.pointa_current_lable = QLabel("Current")
        self.pointa_temp_lable.setAlignment(Qt.AlignCenter)
        self.pointa_strain_lable.setAlignment(Qt.AlignCenter)
        self.pointa_current_lable.setAlignment(Qt.AlignCenter)

        self.grid_pointa.addWidget(self.pointa_temp_lable , 1, 1)
        self.grid_pointa.addWidget(self.pointa_strain_lable, 1, 2)
        self.grid_pointa.addWidget(self.pointa_current_lable, 1, 3)
        self.grid_pointa.addWidget(self.pointa_channala_alert_lable, 2, 0)
        self.grid_pointa.addWidget(self.pointa_channala_alertt_input, 2, 1)
        self.grid_pointa.addWidget(self.pointa_channala_alerts_input, 2, 2)
        self.grid_pointa.addWidget(self.pointa_channala_alertc_input, 2, 3)
        self.grid_pointa.addWidget(self.pointa_channalb_alert_lable, 3, 0)
        self.grid_pointa.addWidget(self.pointa_channalb_alertt_input, 3, 1)
        self.grid_pointa.addWidget(self.pointa_channalb_alerts_input, 3, 2)
        self.grid_pointa.addWidget(self.pointa_channalb_alertc_input, 3, 3)
        self.grid_pointa.addWidget(self.pointa_channalc_alert_lable, 4, 0)
        self.grid_pointa.addWidget(self.pointa_channalc_alertt_input, 4, 1)
        self.grid_pointa.addWidget(self.pointa_channalc_alerts_input, 4, 2)
        self.grid_pointa.addWidget(self.pointa_channalc_alertc_input, 4, 3)

        self.groupbox_pointa.setLayout(self.grid_pointa)
        grid0.addWidget(self.groupbox_pointa, 0, 0)

        #Setting PointB
        self.grid_pointb = QGridLayout()
        self.pointb_distance_lable = QLabel("Distance  From:")
        self.pointb_to_lable = QLabel("To:")
        self.pointb_from_input = QLineEdit()
        self.pointb_to_input = QLineEdit()
        self.pointb_to_lable.setAlignment(Qt.AlignCenter)
        self.pointb_from_input.setText(POINTB_FROM)
        self.pointb_to_input.setText(POINTB_TO)

        self.grid_pointb.addWidget(self.pointb_distance_lable, 0, 0)
        self.grid_pointb.addWidget(self.pointb_from_input, 0, 1)
        self.grid_pointb.addWidget(self.pointb_to_lable, 0, 2)
        self.grid_pointb.addWidget(self.pointb_to_input, 0, 3)

        self.pointb_channala_alert_lable = QLabel("Phase A Alert >=")
        self.pointb_channalb_alert_lable = QLabel("Phase B Alert >=")
        self.pointb_channalc_alert_lable = QLabel("Phase C Alert >=")
        self.pointb_channala_alertt_input = QLineEdit()
        self.pointb_channalb_alertt_input = QLineEdit()
        self.pointb_channalc_alertt_input = QLineEdit()
        self.pointb_channala_alerts_input = QLineEdit()
        self.pointb_channalb_alerts_input = QLineEdit()
        self.pointb_channalc_alerts_input = QLineEdit()
        self.pointb_channala_alertc_input = QLineEdit()
        self.pointb_channalb_alertc_input = QLineEdit()
        self.pointb_channalc_alertc_input = QLineEdit()

        self.pointb_channala_alertt_input.setText(POINTB_CHANNALA_ALERTT)
        self.pointb_channala_alerts_input.setText(POINTB_CHANNALA_ALERTS)
        self.pointb_channala_alertc_input.setText(POINTB_CHANNALA_ALERTC)
        self.pointb_channalb_alertt_input.setText(POINTB_CHANNALB_ALERTT)
        self.pointb_channalb_alerts_input.setText(POINTB_CHANNALB_ALERTS)
        self.pointb_channalb_alertc_input.setText(POINTB_CHANNALB_ALERTC)
        self.pointb_channalc_alertt_input.setText(POINTB_CHANNALC_ALERTT)
        self.pointb_channalc_alerts_input.setText(POINTB_CHANNALC_ALERTS)
        self.pointb_channalc_alertc_input.setText(POINTB_CHANNALC_ALERTC)

        self.pointb_temp_lable = QLabel("Temp(°C)")
        self.pointb_strain_lable = QLabel("Strain")
        self.pointb_current_lable = QLabel("Current")
        self.pointb_temp_lable.setAlignment(Qt.AlignCenter)
        self.pointb_strain_lable.setAlignment(Qt.AlignCenter)
        self.pointb_current_lable.setAlignment(Qt.AlignCenter)

        self.grid_pointb.addWidget(self.pointb_temp_lable , 1, 1)
        self.grid_pointb.addWidget(self.pointb_strain_lable, 1, 2)
        self.grid_pointb.addWidget(self.pointb_current_lable, 1, 3)
        self.grid_pointb.addWidget(self.pointb_channala_alert_lable, 2, 0)
        self.grid_pointb.addWidget(self.pointb_channala_alertt_input, 2, 1)
        self.grid_pointb.addWidget(self.pointb_channala_alerts_input, 2, 2)
        self.grid_pointb.addWidget(self.pointb_channala_alertc_input, 2, 3)
        self.grid_pointb.addWidget(self.pointb_channalb_alert_lable, 3, 0)
        self.grid_pointb.addWidget(self.pointb_channalb_alertt_input, 3, 1)
        self.grid_pointb.addWidget(self.pointb_channalb_alerts_input, 3, 2)
        self.grid_pointb.addWidget(self.pointb_channalb_alertc_input, 3, 3)
        self.grid_pointb.addWidget(self.pointb_channalc_alert_lable, 4, 0)
        self.grid_pointb.addWidget(self.pointb_channalc_alertt_input, 4, 1)
        self.grid_pointb.addWidget(self.pointb_channalc_alerts_input, 4, 2)
        self.grid_pointb.addWidget(self.pointb_channalc_alertc_input, 4, 3)

        self.groupbox_pointb.setLayout(self.grid_pointb)
        grid0.addWidget(self.groupbox_pointb, 0, 1)

        #Setting PointC
        self.grid_pointc = QGridLayout()
        self.pointc_distance_lable = QLabel("Distance  From:")
        self.pointc_to_lable = QLabel("To:")
        self.pointc_from_input = QLineEdit()
        self.pointc_to_input = QLineEdit()
        self.pointc_to_lable.setAlignment(Qt.AlignCenter)
        self.pointc_from_input.setText(POINTC_FROM)
        self.pointc_to_input.setText(POINTC_TO)

        self.grid_pointc.addWidget(self.pointc_distance_lable, 0, 0)
        self.grid_pointc.addWidget(self.pointc_from_input, 0, 1)
        self.grid_pointc.addWidget(self.pointc_to_lable, 0, 2)
        self.grid_pointc.addWidget(self.pointc_to_input, 0, 3)

        self.pointc_channala_alert_lable = QLabel("Phase A Alert >=")
        self.pointc_channalb_alert_lable = QLabel("Phase B Alert >=")
        self.pointc_channalc_alert_lable = QLabel("Phase C Alert >=")
        self.pointc_channala_alertt_input = QLineEdit()
        self.pointc_channalb_alertt_input = QLineEdit()
        self.pointc_channalc_alertt_input = QLineEdit()
        self.pointc_channala_alerts_input = QLineEdit()
        self.pointc_channalb_alerts_input = QLineEdit()
        self.pointc_channalc_alerts_input = QLineEdit()
        self.pointc_channala_alertc_input = QLineEdit()
        self.pointc_channalb_alertc_input = QLineEdit()
        self.pointc_channalc_alertc_input = QLineEdit()

        self.pointc_channala_alertt_input.setText(POINTC_CHANNALA_ALERTT)
        self.pointc_channala_alerts_input.setText(POINTC_CHANNALA_ALERTS)
        self.pointc_channala_alertc_input.setText(POINTC_CHANNALA_ALERTC)
        self.pointc_channalb_alertt_input.setText(POINTC_CHANNALB_ALERTT)
        self.pointc_channalb_alerts_input.setText(POINTC_CHANNALB_ALERTS)
        self.pointc_channalb_alertc_input.setText(POINTC_CHANNALB_ALERTC)
        self.pointc_channalc_alertt_input.setText(POINTC_CHANNALC_ALERTT)
        self.pointc_channalc_alerts_input.setText(POINTC_CHANNALC_ALERTS)
        self.pointc_channalc_alertc_input.setText(POINTC_CHANNALC_ALERTC)

        self.pointc_temp_lable = QLabel("Temp(°C)")
        self.pointc_strain_lable = QLabel("Strain")
        self.pointc_current_lable = QLabel("Current")
        self.pointc_temp_lable.setAlignment(Qt.AlignCenter)
        self.pointc_strain_lable.setAlignment(Qt.AlignCenter)
        self.pointc_current_lable.setAlignment(Qt.AlignCenter)

        self.grid_pointc.addWidget(self.pointc_temp_lable , 1, 1)
        self.grid_pointc.addWidget(self.pointc_strain_lable, 1, 2)
        self.grid_pointc.addWidget(self.pointc_current_lable, 1, 3)
        self.grid_pointc.addWidget(self.pointc_channala_alert_lable, 2, 0)
        self.grid_pointc.addWidget(self.pointc_channala_alertt_input, 2, 1)
        self.grid_pointc.addWidget(self.pointc_channala_alerts_input, 2, 2)
        self.grid_pointc.addWidget(self.pointc_channala_alertc_input, 2, 3)
        self.grid_pointc.addWidget(self.pointc_channalb_alert_lable, 3, 0)
        self.grid_pointc.addWidget(self.pointc_channalb_alertt_input, 3, 1)
        self.grid_pointc.addWidget(self.pointc_channalb_alerts_input, 3, 2)
        self.grid_pointc.addWidget(self.pointc_channalb_alertc_input, 3, 3)
        self.grid_pointc.addWidget(self.pointc_channalc_alert_lable, 4, 0)
        self.grid_pointc.addWidget(self.pointc_channalc_alertt_input, 4, 1)
        self.grid_pointc.addWidget(self.pointc_channalc_alerts_input, 4, 2)
        self.grid_pointc.addWidget(self.pointc_channalc_alertc_input, 4, 3)

        self.groupbox_pointc.setLayout(self.grid_pointc)
        grid0.addWidget(self.groupbox_pointc, 1, 0)

        #Input PointD
        self.grid_pointd = QGridLayout()
        self.pointd_distance_lable = QLabel("Distance  From:")
        self.pointd_to_lable = QLabel("To:")
        self.pointd_from_input = QLineEdit()
        self.pointd_to_input = QLineEdit()
        self.pointd_to_lable.setAlignment(Qt.AlignCenter)
        self.pointd_from_input.setText(POINTD_FROM)
        self.pointd_to_input.setText(POINTD_TO)

        self.grid_pointd.addWidget(self.pointd_distance_lable, 0, 0)
        self.grid_pointd.addWidget(self.pointd_from_input, 0, 1)
        self.grid_pointd.addWidget(self.pointd_to_lable, 0, 2)
        self.grid_pointd.addWidget(self.pointd_to_input, 0, 3)

        self.pointd_channala_alert_lable = QLabel("Phase A Alert >=")
        self.pointd_channalb_alert_lable = QLabel("Phase B Alert >=")
        self.pointd_channalc_alert_lable = QLabel("Phase C Alert >=")
        self.pointd_channala_alertt_input = QLineEdit()
        self.pointd_channalb_alertt_input = QLineEdit()
        self.pointd_channalc_alertt_input = QLineEdit()
        self.pointd_channala_alerts_input = QLineEdit()
        self.pointd_channalb_alerts_input = QLineEdit()
        self.pointd_channalc_alerts_input = QLineEdit()
        self.pointd_channala_alertc_input = QLineEdit()
        self.pointd_channalb_alertc_input = QLineEdit()
        self.pointd_channalc_alertc_input = QLineEdit()

        self.pointd_channala_alertt_input.setText(POINTD_CHANNALA_ALERTT)
        self.pointd_channala_alerts_input.setText(POINTD_CHANNALA_ALERTS)
        self.pointd_channala_alertc_input.setText(POINTD_CHANNALA_ALERTC)
        self.pointd_channalb_alertt_input.setText(POINTD_CHANNALB_ALERTT)
        self.pointd_channalb_alerts_input.setText(POINTD_CHANNALB_ALERTS)
        self.pointd_channalb_alertc_input.setText(POINTD_CHANNALB_ALERTC)
        self.pointd_channalc_alertt_input.setText(POINTD_CHANNALC_ALERTT)
        self.pointd_channalc_alerts_input.setText(POINTD_CHANNALC_ALERTS)
        self.pointd_channalc_alertc_input.setText(POINTD_CHANNALC_ALERTC)

        self.pointd_temp_lable = QLabel("Temp(°C)")
        self.pointd_strain_lable = QLabel("Strain")
        self.pointd_current_lable = QLabel("Current")
        self.pointd_temp_lable.setAlignment(Qt.AlignCenter)
        self.pointd_strain_lable.setAlignment(Qt.AlignCenter)
        self.pointd_current_lable.setAlignment(Qt.AlignCenter)

        self.grid_pointd.addWidget(self.pointd_temp_lable , 1, 1)
        self.grid_pointd.addWidget(self.pointd_strain_lable, 1, 2)
        self.grid_pointd.addWidget(self.pointd_current_lable, 1, 3)
        self.grid_pointd.addWidget(self.pointd_channala_alert_lable, 2, 0)
        self.grid_pointd.addWidget(self.pointd_channala_alertt_input, 2, 1)
        self.grid_pointd.addWidget(self.pointd_channala_alerts_input, 2, 2)
        self.grid_pointd.addWidget(self.pointd_channala_alertc_input, 2, 3)
        self.grid_pointd.addWidget(self.pointd_channalb_alert_lable, 3, 0)
        self.grid_pointd.addWidget(self.pointd_channalb_alertt_input, 3, 1)
        self.grid_pointd.addWidget(self.pointd_channalb_alerts_input, 3, 2)
        self.grid_pointd.addWidget(self.pointd_channalb_alertc_input, 3, 3)
        self.grid_pointd.addWidget(self.pointd_channalc_alert_lable, 4, 0)
        self.grid_pointd.addWidget(self.pointd_channalc_alertt_input, 4, 1)
        self.grid_pointd.addWidget(self.pointd_channalc_alerts_input, 4, 2)
        self.grid_pointd.addWidget(self.pointd_channalc_alertc_input, 4, 3)

        self.groupbox_pointd.setLayout(self.grid_pointd)
        grid0.addWidget(self.groupbox_pointd, 1, 1)

        groupbox.setLayout(grid0)
        groupbox2 = QGroupBox("Directory")
        
        grid = QGridLayout()
        self.dts_feed_label = QLabel("DTS Feed (.tepr):")
        self.prog_input_label = QLabel("Program Input:")
        self.prog_output_label = QLabel("Program Output:")
        self.rttr_app_label = QLabel("RTTR Program:")
        self.rttr_output_label = QLabel("RTTR Output:")

        self.dts_feed_edit = QLineEdit()
        self.dts_feed_edit.setText(DTS_FEED)
        defaultBrowseButton3 = QPushButton("Browse Directory")
        defaultBrowseButton3.clicked.connect(self.openDirectoryDTSFeedDialog)
        grid.addWidget(self.dts_feed_label, 0, 0)
        grid.addWidget(self.dts_feed_edit, 0,2)
        grid.addWidget(defaultBrowseButton3, 0, 3)    

        self.prog_input_edit = QLineEdit()
        self.prog_input_edit.setText(PROG_INPUT)
        defaultBrowseButton = QPushButton("Browse Directory")
        defaultBrowseButton.clicked.connect(self.openDirectoryDialog)
        grid.addWidget(self.prog_input_label, 1, 0)
        grid.addWidget(self.prog_input_edit, 1,2)
        grid.addWidget(defaultBrowseButton, 1, 3)               
        
        self.prog_output_edit = QLineEdit()
        self.prog_output_edit.setText(PROG_OUTPUT)
        defaultBrowseButton2 = QPushButton("Browse Directory")   
        defaultBrowseButton2.clicked.connect(self.openDirectoryDialog2)  
        grid.addWidget(self.prog_output_label, 2, 0)
        grid.addWidget(self.prog_output_edit, 2,2)
        grid.addWidget(defaultBrowseButton2, 2, 3)     

        self.rttr_program_edit = QLineEdit()
        self.rttr_program_edit.setText(RTTR_PROGRAM)
        defaultBrowseButton3 = QPushButton("Browse Program")   
        defaultBrowseButton3.clicked.connect(self.openFileNamesDialog)  
        grid.addWidget(self.rttr_app_label, 3, 0)
        grid.addWidget(self.rttr_program_edit, 3,2)
        grid.addWidget(defaultBrowseButton3, 3, 3)     

        self.rttr_output_edit = QLineEdit()
        self.rttr_output_edit.setText(RTTR_OUTPUT)
        defaultBrowseButton4 = QPushButton("Browse Directory")   
        defaultBrowseButton4.clicked.connect(self.openDirectoryDialog3)  
        grid.addWidget(self.rttr_output_label, 4, 0)
        grid.addWidget(self.rttr_output_edit, 4,2)
        grid.addWidget(defaultBrowseButton4, 4, 3)     

        groupbox2.setLayout(grid)

        okButton = QPushButton('OK')
        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(lambda:self.close())
        okButton.clicked.connect(self.saveConfig) 

        # okButton.setMinimumWidth(25)
        okButton.setMaximumWidth(80)
        cancelButton.setMaximumWidth(80)
        # okButton.width(25)
        # okButton.resize(100,32)

        groupbo3 = QGroupBox()
        hbox = QHBoxLayout(self)

        groupbo3.setLayout(hbox)

        groupbo3.setMaximumHeight(50)

        # hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)
        hbox.setAlignment(Qt.AlignCenter)
        # vbox = QVBoxLayout()
        # vbox.addStretch(1)
        # vbox.addLayout(hbox)

        layout.addWidget(groupbox)
        layout.addWidget(groupbox2)
        layout.addWidget(groupbo3)

        self.setLayout(layout)


    def saveConfig(self):           
        print("Save")

        CONFIG.setValue('Directory/dtsfeed', self.dts_feed_edit.text())
        CONFIG.setValue('Directory/progin', self.prog_input_edit.text())
        CONFIG.setValue('Directory/progout', self.prog_output_edit.text())
        CONFIG.setValue('Directory/rttrprog', self.rttr_program_edit.text())
        CONFIG.setValue('Directory/rttrout', self.rttr_output_edit.text())

        CONFIG.setValue('PointA/from', self.pointa_from_input.text())
        CONFIG.setValue('PointA/to', self.pointa_to_input.text())
        CONFIG.setValue('PointA/aalertt', self.pointa_channala_alertt_input.text())
        CONFIG.setValue('PointA/aalerts', self.pointa_channala_alerts_input.text())
        CONFIG.setValue('PointA/aalertc', self.pointa_channala_alertc_input.text())
        CONFIG.setValue('PointA/balertt', self.pointa_channalb_alertt_input.text())
        CONFIG.setValue('PointA/balerts', self.pointa_channalb_alerts_input.text())
        CONFIG.setValue('PointA/balertc', self.pointa_channalb_alertc_input.text())
        CONFIG.setValue('PointA/calertt', self.pointa_channalc_alertt_input.text())
        CONFIG.setValue('PointA/calerts', self.pointa_channalc_alerts_input.text())
        CONFIG.setValue('PointA/calertc', self.pointa_channalc_alertc_input.text())

        CONFIG.setValue('PointB/from', self.pointb_from_input.text())
        CONFIG.setValue('PointB/to', self.pointb_to_input.text())
        CONFIG.setValue('PointB/aalertt', self.pointb_channala_alertt_input.text())
        CONFIG.setValue('PointB/aalerts', self.pointb_channala_alerts_input.text())
        CONFIG.setValue('PointB/aalertc', self.pointb_channala_alertc_input.text())
        CONFIG.setValue('PointB/balertt', self.pointb_channalb_alertt_input.text())
        CONFIG.setValue('PointB/balerts', self.pointb_channalb_alerts_input.text())
        CONFIG.setValue('PointB/balertc', self.pointb_channalb_alertc_input.text())
        CONFIG.setValue('PointB/calertt', self.pointb_channalc_alertt_input.text())
        CONFIG.setValue('PointB/calerts', self.pointb_channalc_alerts_input.text())
        CONFIG.setValue('PointB/calertc', self.pointb_channalc_alertc_input.text())

        CONFIG.setValue('PointC/from', self.pointc_from_input.text())
        CONFIG.setValue('PointC/to', self.pointc_to_input.text())
        CONFIG.setValue('PointC/aalertt', self.pointc_channala_alertt_input.text())
        CONFIG.setValue('PointC/aalerts', self.pointc_channala_alerts_input.text())
        CONFIG.setValue('PointC/aalertc', self.pointc_channala_alertc_input.text())
        CONFIG.setValue('PointC/balertt', self.pointc_channalb_alertt_input.text())
        CONFIG.setValue('PointC/balerts', self.pointc_channalb_alerts_input.text())
        CONFIG.setValue('PointC/balertc', self.pointc_channalb_alertc_input.text())
        CONFIG.setValue('PointC/calertt', self.pointc_channalc_alertt_input.text())
        CONFIG.setValue('PointC/calerts', self.pointc_channalc_alerts_input.text())
        CONFIG.setValue('PointC/calertc', self.pointc_channalc_alertc_input.text())

        CONFIG.setValue('PointD/from', self.pointd_from_input.text())
        CONFIG.setValue('PointD/to', self.pointd_to_input.text())
        CONFIG.setValue('PointD/aalertt', self.pointd_channala_alertt_input.text())
        CONFIG.setValue('PointD/aalerts', self.pointd_channala_alerts_input.text())
        CONFIG.setValue('PointD/aalertc', self.pointd_channala_alertc_input.text())
        CONFIG.setValue('PointD/balertt', self.pointd_channalb_alertt_input.text())
        CONFIG.setValue('PointD/balerts', self.pointd_channalb_alerts_input.text())
        CONFIG.setValue('PointD/balertc', self.pointd_channalb_alertc_input.text())
        CONFIG.setValue('PointD/calertt', self.pointd_channalc_alertt_input.text())
        CONFIG.setValue('PointD/calerts', self.pointd_channalc_alerts_input.text())
        CONFIG.setValue('PointD/calertc', self.pointd_channalc_alertc_input.text())

        CONFIG.sync()
        # Update Param
        # DTS_FEED = self.dts_feed_edit.text()
        # PROG_INPUT = self.prog_input_edit.text()
        # PROG_OUTPUT = self.prog_output_edit.text()
        # RTTR_PROGRAM = self.rttr_program_edit.text()
        # RTTR_OUTPUT = self.rttr_output_edit.text()

        # POINTA_FROM = self.pointa_from_input.text()
        # POINTA_TO = self.pointa_to_input.text()
        # POINTA_CHANNALA_ALERTT = self.pointa_channala_alertt_input.text()
        # POINTA_CHANNALA_ALERTS = self.pointa_channala_alerts_input.text()
        # POINTA_CHANNALA_ALERTC = self.pointa_channala_alertc_input.text()
        # POINTA_CHANNALB_ALERTT = self.pointa_channalb_alertt_input.text()
        # POINTA_CHANNALB_ALERTS = self.pointa_channalb_alerts_input.text()
        # POINTA_CHANNALB_ALERTC = self.pointa_channalb_alertc_input.text()
        # POINTA_CHANNALC_ALERTT = self.pointa_channalc_alertt_input.text()
        # POINTA_CHANNALC_ALERTS = self.pointa_channalc_alerts_input.text()
        # POINTA_CHANNALC_ALERTC = self.pointa_channalc_alertc_input.text()

        # POINTB_FROM = self.pointb_from_input.text()
        # POINTB_TO = self.pointb_to_input.text()
        # POINTB_CHANNALA_ALERTT = self.pointb_channala_alertt_input.text()
        # POINTB_CHANNALA_ALERTS = self.pointb_channala_alerts_input.text()
        # POINTB_CHANNALA_ALERTC = self.pointb_channala_alertc_input.text()
        # POINTB_CHANNALB_ALERTT = self.pointb_channalb_alertt_input.text()
        # POINTB_CHANNALB_ALERTS = self.pointb_channalb_alerts_input.text()
        # POINTB_CHANNALB_ALERTC = self.pointb_channalb_alertc_input.text()
        # POINTB_CHANNALC_ALERTT = self.pointb_channalc_alertt_input.text()
        # POINTB_CHANNALC_ALERTS = self.pointb_channalc_alerts_input.text()
        # POINTB_CHANNALC_ALERTC = self.pointb_channalc_alertc_input.text()

        # POINTC_FROM = self.pointc_from_input.text()
        # POINTC_TO = self.pointc_to_input.text()
        # POINTC_CHANNALA_ALERTT = self.pointc_channala_alertt_input.text()
        # POINTC_CHANNALA_ALERTS = self.pointc_channala_alerts_input.text()
        # POINTC_CHANNALA_ALERTC = self.pointc_channala_alertc_input.text()
        # POINTC_CHANNALB_ALERTT = self.pointc_channalb_alertt_input.text()
        # POINTC_CHANNALB_ALERTS = self.pointc_channalb_alerts_input.text()
        # POINTC_CHANNALB_ALERTC = self.pointc_channalb_alertc_input.text()
        # POINTC_CHANNALC_ALERTT = self.pointc_channalc_alertt_input.text()
        # POINTC_CHANNALC_ALERTS = self.pointc_channalc_alerts_input.text()
        # POINTC_CHANNALC_ALERTC = self.pointc_channalc_alertc_input.text()

        # POINTD_FROM = self.pointd_from_input.text()
        # POINTD_TO = self.pointd_to_input.text()
        # POINTD_CHANNALA_ALERTT = self.pointd_channala_alertt_input.text()
        # POINTD_CHANNALA_ALERTS = self.pointd_channala_alerts_input.text()
        # POINTD_CHANNALA_ALERTC = self.pointd_channala_alertc_input.text()
        # POINTD_CHANNALB_ALERTT = self.pointd_channalb_alertt_input.text()
        # POINTD_CHANNALB_ALERTS = self.pointd_channalb_alerts_input.text()
        # POINTD_CHANNALB_ALERTC = self.pointd_channalb_alertc_input.text()
        # POINTD_CHANNALC_ALERTT = self.pointd_channalc_alertt_input.text()
        # POINTD_CHANNALC_ALERTS = self.pointd_channalc_alerts_input.text()
        # POINTD_CHANNALC_ALERTC = self.pointd_channalc_alertc_input.text()

        DTS_FEED = CONFIG.value('Directory/dtsfeed', "")
        PROG_INPUT = CONFIG.value('Directory/progin', "")
        PROG_OUTPUT = CONFIG.value('Directory/progout', "")
        RTTR_PROGRAM = CONFIG.value('Directory/rttrprog', "")

        POINTA_NAME = CONFIG.value('PointName/PointA', "Point A")
        POINTB_NAME = CONFIG.value('PointName/PointB', "Point B")
        POINTC_NAME = CONFIG.value('PointName/PointC', "Point C")
        POINTD_NAME = CONFIG.value('PointName/PointD', "Point D")

        RTTR_OUTPUT = CONFIG.value('Directory/rttrout', "")
        POINTA_FROM = CONFIG.value('PointA/from', "")
        POINTA_TO = CONFIG.value('PointA/to', "")
        POINTA_CHANNALA_ALERTT = float(CONFIG.value('PointA/aalertt', ""))
        POINTA_CHANNALA_ALERTS = float(CONFIG.value('PointA/aalerts', ""))
        POINTA_CHANNALA_ALERTC = float(CONFIG.value('PointA/aalertc', ""))
        POINTA_CHANNALB_ALERTT = float(CONFIG.value('PointA/balertt', ""))
        POINTA_CHANNALB_ALERTS = float(CONFIG.value('PointA/balerts', ""))
        POINTA_CHANNALB_ALERTC = float(CONFIG.value('PointA/balertc', ""))
        POINTA_CHANNALC_ALERTT = float(CONFIG.value('PointA/calertt', ""))
        POINTA_CHANNALC_ALERTS = float(CONFIG.value('PointA/calerts', ""))
        POINTA_CHANNALC_ALERTC = float(CONFIG.value('PointA/calertc', ""))
        POINTB_FROM = CONFIG.value('PointB/from', "")
        POINTB_TO = CONFIG.value('PointB/to', "")
        POINTB_CHANNALA_ALERTT = CONFIG.value('PointB/aalertt', "")
        POINTB_CHANNALA_ALERTS = CONFIG.value('PointB/aalerts', "")
        POINTB_CHANNALA_ALERTC = CONFIG.value('PointB/aalertc', "")
        POINTB_CHANNALB_ALERTT = CONFIG.value('PointB/balertt', "")
        POINTB_CHANNALB_ALERTS = CONFIG.value('PointB/balerts', "")
        POINTB_CHANNALB_ALERTC = CONFIG.value('PointB/balertc', "")
        POINTB_CHANNALC_ALERTT = CONFIG.value('PointB/calertt', "")
        POINTB_CHANNALC_ALERTS = CONFIG.value('PointB/calerts', "")
        POINTB_CHANNALC_ALERTC = CONFIG.value('PointB/calertc', "")
        POINTC_FROM = CONFIG.value('PointC/from', "")
        POINTC_TO = CONFIG.value('PointC/to', "")
        POINTC_CHANNALA_ALERTT = CONFIG.value('PointC/aalertt', "")
        POINTC_CHANNALA_ALERTS = CONFIG.value('PointC/aalerts', "")
        POINTC_CHANNALA_ALERTC = CONFIG.value('PointC/aalertc', "")
        POINTC_CHANNALB_ALERTT = CONFIG.value('PointC/balertt', "")
        POINTC_CHANNALB_ALERTS = CONFIG.value('PointC/balerts', "")
        POINTC_CHANNALB_ALERTC = CONFIG.value('PointC/balertc', "")
        POINTC_CHANNALC_ALERTT = CONFIG.value('PointC/calertt', "")
        POINTC_CHANNALC_ALERTS = CONFIG.value('PointC/calerts', "")
        POINTC_CHANNALC_ALERTC = CONFIG.value('PointC/calertc', "")
        POINTD_FROM = CONFIG.value('PointD/from', "")
        POINTD_TO = CONFIG.value('PointD/to', "")
        POINTD_CHANNALA_ALERTT = CONFIG.value('PointD/aalertt', "")
        POINTD_CHANNALA_ALERTS = CONFIG.value('PointD/aalerts', "")
        POINTD_CHANNALA_ALERTC = CONFIG.value('PointD/aalertc', "")
        POINTD_CHANNALB_ALERTT = CONFIG.value('PointD/balertt', "")
        POINTD_CHANNALB_ALERTS = CONFIG.value('PointD/balerts', "")
        POINTD_CHANNALB_ALERTC = CONFIG.value('PointD/balertc', "")
        POINTD_CHANNALC_ALERTT = CONFIG.value('PointD/calertt', "")
        POINTD_CHANNALC_ALERTS = CONFIG.value('PointD/calerts', "")
        POINTD_CHANNALC_ALERTC = CONFIG.value('PointD/calertc', "")

        self.close()

    def openDirectoryDTSFeedDialog(self):           
        flags = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        d = directory = QFileDialog.getExistingDirectory(self,"Open Directory",os.getcwd(),flags)        
        self.dts_feed_edit.setText(d)

    def openDirectoryDialog(self):           
        flags = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        d = directory = QFileDialog.getExistingDirectory(self,"Open Directory",os.getcwd(),flags)        
        self.prog_input_edit.setText(d)

    def openDirectoryDialog2(self):           
        flags = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        d = directory = QFileDialog.getExistingDirectory(self,"Open Directory",os.getcwd(),flags)        
        self.prog_output_edit.setText(d)

    def openDirectoryDialog3(self):           
        flags = QFileDialog.DontResolveSymlinks
        d = directory = QFileDialog.getExistingDirectory(self,"Browse Application",os.getcwd(),flags)        
        self.rttr_output_edit.setText(d)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.exe)", options=options)
        if files:
            self.rttr_output_edit.setText(files[0])
            print(files)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            self.rttr_program_edit.setText(files[0])
            print(files)


# class Handler(watchdog.events.PatternMatchingEventHandler):
# 	def __init__(self):
# 		# Set the patterns for PatternMatchingEventHandler
# 		watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.tepr','*.txt'],
# 															ignore_directories=True, case_sensitive=False)
# 	def on_created(self, event):
# 		print("Watchdog received created event - % s." % event.src_path)

# 	def on_modified(self, event):
# 		print("Watchdog received modified event - % s." % event.src_path)


class WorkThreadMain(QThread):
    ''' Streaming Main task '''
    threadSignalMain = pyqtSignal(int,str,str,int,float,float,float,float,float,float,float,float)
    # threadSignalMain = pyqtSignal(int,str,str,int,float,float,float,float)
                        # self.threadSignalMain.emit(c,"Strain",str(strain_feed_datetime),int(strain_channel_no),strain_poAch0_avg,strain_poBch0_avg,strain_poCch0_avg,0.0)

    def __init__(self, startParm):
        super().__init__()
        self.startParm = startParm

    def run(self, *args, **kwargs):

        c = self.startParm

        for file_name in os.listdir(DTS_FEED):
            if file_name.startswith('Baseline') or file_name.startswith('Strain'):
                print(file_name)
                shutil.copy(DTS_FEED+'/'+file_name, PROG_INPUT+'/')

        while True:
            c += 1
            temp_line_datetime = []
            temp_feed_datetime = ""
            temp_channel_no = 5
            temp_poAch0_count = 0        
            temp_poAch0_total = 0.00
            temp_poAch0_avg = -0.00000001
            temp_poBch0_count = 0        
            temp_poBch0_total = 0.00
            temp_poBch0_avg = -0.00000001
            temp_poCch0_count = 0        
            temp_poCch0_total = 0.00
            temp_poCch0_avg = -0.00000001
            temp_poDch0_count = 0        
            temp_poDch0_total = 0.00
            temp_poDch0_avg = 0.00

            temp_distance = 0.00

            if(os.path.isdir(DTS_FEED) and os.path.isdir(PROG_INPUT)):
                self.dc = filecmp.dircmp(DTS_FEED, PROG_INPUT, ignore=['LOG']).left_only
                if len(self.dc) > 0:

                    if self.dc[0].startswith('Temp_') and self.dc[0].endswith('.freqr'):

                        # print("vvvvvvvvvvvvv---->",self.dc[0])
                        shutil.copy(DTS_FEED+'/'+self.dc[0], PROG_INPUT+'/')
                        extract_filename_dot = self.dc[0].split('.')[0]
                        extract_filename = extract_filename_dot.split('_')
                        # print("mmmmmmmmmmm->",extract_filename)
                        temp_filename = extract_filename[0] + "_" + extract_filename[2] + "_" + extract_filename[3] + ".tepr"
                        print("temp_filename----->", temp_filename)

                        # ////////////////
                        shutil.copy(DTS_FEED+'/'+temp_filename, PROG_INPUT+'/')

                        self.dstfile_input = open(DTS_FEED+'/'+temp_filename, 'r')
                        self.lines = self.dstfile_input.readlines()        
                        for count,line in enumerate(self.lines, 1):
                            # print(count,line.strip())

                            if(count == 4):
                                temp_line_datetime = line.strip().split()
                                temp_feed_datetime = str(temp_line_datetime[2])+ " " + str(temp_line_datetime[3]) + " " + str(temp_line_datetime[4])
                                print("temp_feed_datetime------>",temp_feed_datetime)
                        
                            if(count == 6):
                                temp_channel_no = line.strip().split("=")[1]
                                # print("temp_channel_no------>",temp_channel_no)

                            if(count == 32):
                                temp_total_records = line.strip().split()[0]
                                # print("temp_total_records------>",temp_total_records)

                            if(count >= 34):
                                temp_distance = [float(n) for n in line.strip().split()][0]
                                temp_distance_val = [float(n) for n in line.strip().split()][1]

                                # print("temp_distance------>",temp_distance,temp_distance_val)

                                if(int(temp_channel_no) == 0):
                                    # Phase A 
                                    # print("temp_distance A------>",POINTA_FROM,POINTA_TO)
                                    # self.calculateBaseLine(0)

                                    if(temp_distance > float(POINTA_FROM) and temp_distance < float(POINTA_TO)):
                                        temp_poAch0_count += 1
                                        temp_poAch0_total = temp_poAch0_total + temp_distance_val
                                        temp_poAch0_avg = temp_poAch0_total/float(temp_poAch0_count)

                                    if(temp_distance > float(POINTB_FROM) and temp_distance < float(POINTB_TO)):
                                        temp_poBch0_count += 1
                                        temp_poBch0_total = temp_poBch0_total + temp_distance_val
                                        temp_poBch0_avg = temp_poBch0_total/float(temp_poBch0_count)

                                    if(temp_distance > float(POINTC_FROM) and temp_distance < float(POINTC_TO)):
                                        temp_poCch0_count += 1
                                        temp_poCch0_total = temp_poCch0_total + temp_distance_val
                                        temp_poCch0_avg = temp_poCch0_total/float(temp_poCch0_count)


                                if(int(temp_channel_no) == 1):
                                    # self.calculateBaseLine(1)
                                    # Phase A 
                                    if(temp_distance > float(POINTA_FROM) and temp_distance < float(POINTA_TO)):
                                        temp_poAch0_count += 1
                                        temp_poAch0_total = temp_poAch0_total + temp_distance_val
                                        temp_poAch0_avg = temp_poAch0_total/float(temp_poAch0_count)

                                    if(temp_distance > float(POINTB_FROM) and temp_distance < float(POINTB_TO)):
                                        temp_poBch0_count += 1
                                        temp_poBch0_total = temp_poBch0_total + temp_distance_val
                                        temp_poBch0_avg = temp_poBch0_total/float(temp_poBch0_count)

                                    if(temp_distance > float(POINTC_FROM) and temp_distance < float(POINTC_TO)):
                                        temp_poCch0_count += 1
                                        temp_poCch0_total = temp_poCch0_total + temp_distance_val
                                        temp_poCch0_avg = temp_poCch0_total/float(temp_poCch0_count)

                                if(int(temp_channel_no) == 2):
                                    # self.calculateBaseLine(2)
                                    # Phase A 
                                    if(temp_distance > float(POINTA_FROM) and temp_distance < float(POINTA_TO)):
                                        temp_poAch0_count += 1
                                        temp_poAch0_total = temp_poAch0_total + temp_distance_val
                                        temp_poAch0_avg = temp_poAch0_total/float(temp_poAch0_count)
                                    
                                    if(temp_distance > float(POINTB_FROM) and temp_distance < float(POINTB_TO)):
                                        temp_poBch0_count += 1
                                        temp_poBch0_total = temp_poBch0_total + temp_distance_val
                                        temp_poBch0_avg = temp_poBch0_total/float(temp_poBch0_count)

                                    if(temp_distance > float(POINTC_FROM) and temp_distance < float(POINTC_TO)):
                                        temp_poCch0_count += 1
                                        temp_poCch0_total = temp_poCch0_total + temp_distance_val
                                        temp_poCch0_avg = temp_poCch0_total/float(temp_poCch0_count)                        
                                        
                                if(int(temp_channel_no) == 3):
                                    # self.calculateBaseLine(2)
                                    # Phase A 
                                    if(temp_distance > float(POINTD_FROM) and temp_distance < float(POINTD_TO)):
                                        temp_poDch0_count += 1
                                        temp_poDch0_total = temp_poDch0_total + temp_distance_val
                                        temp_poDch0_avg = temp_poDch0_total/float(temp_poDch0_count)


                        if(int(temp_channel_no) == 0):
                            if(temp_poAch0_avg != None):
                                self.writeDataFilebyChannel("PointA","PhaseA", str(temp_line_datetime[2]), str(temp_line_datetime[3]), str(temp_line_datetime[4]), temp_poAch0_avg + float(BASELINE_TEMP[0]))
                            if(temp_poBch0_avg != None):
                                self.writeDataFilebyChannel("PointB","PhaseA", str(temp_line_datetime[2]), str(temp_line_datetime[3]), str(temp_line_datetime[4]), temp_poBch0_avg + float(BASELINE_TEMP[0]))
                            if(temp_poCch0_avg != None):
                                self.writeDataFilebyChannel("PointC","PhaseA", str(temp_line_datetime[2]), str(temp_line_datetime[3]), str(temp_line_datetime[4]), temp_poCch0_avg + float(BASELINE_TEMP[0]))
                        
                        if(int(temp_channel_no) == 1):
                            if(temp_poAch0_avg != None):
                                self.writeDataFilebyChannel("PointA","PhaseB", str(temp_line_datetime[2]), str(temp_line_datetime[3]), str(temp_line_datetime[4]), temp_poAch0_avg + float(BASELINE_TEMP[1]))
                            if(temp_poBch0_avg != None):
                                self.writeDataFilebyChannel("PointB","PhaseB", str(temp_line_datetime[2]), str(temp_line_datetime[3]), str(temp_line_datetime[4]), temp_poBch0_avg + float(BASELINE_TEMP[1]))
                            if(temp_poCch0_avg != None):
                                self.writeDataFilebyChannel("PointC","PhaseB", str(temp_line_datetime[2]), str(temp_line_datetime[3]), str(temp_line_datetime[4]), temp_poCch0_avg + float(BASELINE_TEMP[1]))
                        
                        if(int(temp_channel_no) == 2):
                            if(temp_poAch0_avg != None):
                                self.writeDataFilebyChannel("PointA","PhaseC", str(temp_line_datetime[2]), str(temp_line_datetime[3]), str(temp_line_datetime[4]),temp_poAch0_avg + float(BASELINE_TEMP[2]))
                            if(temp_poBch0_avg != None):
                                self.writeDataFilebyChannel("PointB","PhaseC", str(temp_line_datetime[2]), str(temp_line_datetime[3]), str(temp_line_datetime[4]),temp_poBch0_avg + float(BASELINE_TEMP[2]))
                            if(temp_poCch0_avg != None):
                                self.writeDataFilebyChannel("PointC","PhaseC", str(temp_line_datetime[2]), str(temp_line_datetime[3]), str(temp_line_datetime[4]),temp_poCch0_avg + float(BASELINE_TEMP[2]))

                        if(int(temp_channel_no) == 3):
                            if(temp_poDch0_avg != None):
                                self.writeDataFilebyChannel("PointD","PhaseA", str(temp_line_datetime[2]), str(temp_line_datetime[3]), str(temp_line_datetime[4]),temp_poDch0_avg + float(BASELINE_TEMP[3]))



                        # self.threadSignalMain.emit(c,"Temp",str(temp_feed_datetime),int(temp_channel_no),temp_poAch0_avg,temp_poBch0_avg,temp_poCch0_avg,0.0)
                        # ////////////////
                        # mmmmmmmmmmm-> ['Temp', 'Freq', 'Oct221158', '11']
                        # ccc
                        # for filename in self.dc.left_only:
                        #     print("xxxxx->",filename)
                        strain_line_datetime = []
                        strain_feed_datetime = ""
                        strain_channel_no = 5
                        strain_poAch0_count = 0        
                        strain_poAch0_total = 0.00
                        strain_poAch0_avg = 0.00
                        strain_poBch0_count = 0        
                        strain_poBch0_total = 0.00
                        strain_poBch0_avg = 0.00
                        strain_poCch0_count = 0        
                        strain_poCch0_total = 0.00
                        strain_poCch0_avg = 0.00

                        strain_poDch0_count = 0        
                        strain_poDch0_total = 0.00
                        strain_poDch0_avg = 0.00

                        strain_distance = 0.00
                        strain_total_records = 0
                        strain_coefficient = 0
                        epsilon = 0

                        self.dstfile_input = open(DTS_FEED+'/'+self.dc[0], 'r')
                        self.lines = self.dstfile_input.readlines()        
                        for count,line in enumerate(self.lines, 1):
                            # print(count,line.strip())

                            if(count == 4):
                                strain_line_datetime = line.strip().split()
                                strain_feed_datetime = str(strain_line_datetime[2])+ " " + str(strain_line_datetime[3]) + " " + str(strain_line_datetime[4])
                                # print("strain_feed_datetime------>",strain_feed_datetime)
                        
                            if(count == 6):
                                strain_channel_no = line.strip().split("=")[1]
                                # print("strain_channel_no------>",strain_channel_no)

                            if(count == 24):
                                temp_t0 = line.strip().split()[-1]
                                print(temp_t0)

                            if(count == 26):
                                strain_coefficient_ce = line.strip().split()[-1]
                                print(strain_coefficient_ce)

                            if(count == 27):
                                temp_coefficient_ct = line.strip().split()[-1]
                                print(temp_coefficient_ct)
                                # print("strain_total_records------>",strain_total_records)

                            if(count == 32):
                                strain_total_records = line.strip().split()[0]
                                # print("strain_total_records------>",strain_total_records)

                            if(count >= 34):
                                strain_distance = [float(n) for n in line.strip().split()][0]
                                strain_distance_val = [float(n) for n in line.strip().split()][1]

                                # print("strain_distance------>",strain_distance,strain_distance_val)

                                if(int(strain_channel_no) == 0):
                                    # Phase A 
                                    ################ print("strain_distance A------>",POINTA_FROM,POINTA_TO)
                                    if(strain_distance > float(POINTA_FROM) and strain_distance < float(POINTA_TO)):
                                        strain_poAch0_count += 1
                                        strain_poAch0_total = strain_poAch0_total + strain_distance_val
                                        strain_poAch0_avg = strain_poAch0_total/float(strain_poAch0_count)
                                    
                                    if(strain_distance > float(POINTB_FROM) and strain_distance < float(POINTB_TO)):
                                        strain_poBch0_count += 1
                                        strain_poBch0_total = strain_poBch0_total + strain_distance_val
                                        strain_poBch0_avg = strain_poBch0_total/float(strain_poBch0_count)
                                    
                                    if(strain_distance > float(POINTC_FROM) and strain_distance < float(POINTC_TO)):
                                        strain_poCch0_count += 1
                                        strain_poCch0_total = strain_poCch0_total + strain_distance_val
                                        strain_poCch0_avg = strain_poCch0_total/float(strain_poCch0_count)

                                    #Read BaseLine

                                if(int(strain_channel_no) == 1):
                                    # Phase A 
                                    if(strain_distance > float(POINTA_FROM) and strain_distance < float(POINTA_TO)):
                                        strain_poAch0_count += 1
                                        strain_poAch0_total = strain_poAch0_total + strain_distance_val
                                        strain_poAch0_avg = strain_poAch0_total/float(strain_poAch0_count)

                                    if(strain_distance > float(POINTB_FROM) and strain_distance < float(POINTB_TO)):
                                        strain_poBch0_count += 1
                                        strain_poBch0_total = strain_poBch0_total + strain_distance_val
                                        strain_poBch0_avg = strain_poBch0_total/float(strain_poBch0_count)

                                    if(strain_distance > float(POINTC_FROM) and strain_distance < float(POINTC_TO)):
                                        strain_poCch0_count += 1
                                        strain_poCch0_total = strain_poCch0_total + strain_distance_val
                                        strain_poCch0_avg = strain_poCch0_total/float(strain_poCch0_count)

                                if(int(strain_channel_no) == 2):
                                    # Phase A 
                                    if(strain_distance > float(POINTA_FROM) and strain_distance < float(POINTA_TO)):
                                        strain_poAch0_count += 1
                                        strain_poAch0_total = strain_poAch0_total + strain_distance_val
                                        strain_poAch0_avg = strain_poAch0_total/float(strain_poAch0_count)
                                    
                                    if(strain_distance > float(POINTB_FROM) and strain_distance < float(POINTB_TO)):
                                        strain_poBch0_count += 1
                                        strain_poBch0_total = strain_poBch0_total + strain_distance_val
                                        strain_poBch0_avg = strain_poBch0_total/float(strain_poBch0_count)

                                    if(strain_distance > float(POINTC_FROM) and strain_distance < float(POINTC_TO)):
                                        strain_poCch0_count += 1
                                        strain_poCch0_total = strain_poCch0_total + strain_distance_val
                                        strain_poCch0_avg = strain_poCch0_total/float(strain_poCch0_count)


                                if(int(strain_channel_no) == 3):
                                    # Phase A 
                                    if(strain_distance > float(POINTD_FROM) and strain_distance < float(POINTD_TO)):
                                        strain_poDch0_count += 1
                                        strain_poDch0_total = strain_poDch0_total + strain_distance_val
                                        strain_poDch0_avg = strain_poDch0_total/float(strain_poDch0_count)

                        # cal
                        # strain_poAch0_calculate = (strain_poCch0_avg -
                        print("BASELINE_VALUE --->",BASELINE_VALUE)
                        print("data-->",strain_channel_no,temp_poAch0_avg ,strain_poAch0_avg, BASELINE_VALUE[int(strain_channel_no)])

                        self.threadSignalMain.emit(c,"Strain", str(strain_feed_datetime), int(strain_channel_no),
                                    strain_poAch0_avg, strain_poBch0_avg, strain_poCch0_avg, strain_poDch0_avg,
                                    temp_poAch0_avg + float(BASELINE_TEMP[0]) , temp_poBch0_avg + float(BASELINE_TEMP[1]), 
                                    temp_poCch0_avg + float(BASELINE_TEMP[2]), temp_poDch0_avg + + float(BASELINE_TEMP[3]))


                    else:
                        print("other---->",self.dc[0])
                        shutil.copy(DTS_FEED+'/'+self.dc[0], PROG_INPUT+'/')
                        pass


            QThread.msleep(10000)


    def writeDataFilebyChannel(self , PointName, Channel, Month, Date, Time, Temp):

        # print("Current working directory: {0}".format(APP_PATH))
        # print("Month: ",self.month_converter(Month))
        # print("Date: ", Date)
        Time_x = Time.replace(":", "")        
        print("--------------------------------------****************",Time, Time_x)

        year = datetime.now().year
        datapath = APP_PATH+"/progdat/"+str(year)+str(self.month_converter(Month))+str(Date)
        outpath = APP_PATH+"/progout/"+str(year)+str(self.month_converter(Month))+str(Date)
        rttroutpath = APP_PATH+"/rttrout/"+str(year)+str(self.month_converter(Month))+str(Date)


        if not os.path.exists(datapath):
            os.makedirs(datapath)
        
        if not os.path.exists(outpath):
            os.makedirs(outpath)

        if not os.path.exists(rttroutpath):
            os.makedirs(rttroutpath)


        datafilename = datapath +'/'+PointName+'_'+Channel+'.txt'

        self.dstfile_output = open(datafilename, "a+")
        self.dstfile_output.write(Time+" "+str(Temp)+ "\n")
        self.dstfile_output.close()

        src = APP_PATH + "/progdat/header/kanom/PointA.txt"
        des = datapath +'/'+str(year)+str(self.month_converter(Month))+str(Date)+"_"+PointName+'_'+Channel+'.ci'
        shutil.copyfile(src, des)

        filename_avg = datapath + "/" +PointName+'_'+Channel+'.txt'

        print("read data from ->>>>>>>>", filename_avg)
        file = open(filename_avg)
        # get the first line of the file
        line1 = file.readlines()
        # print(line1)
        file.close()
        mylist = list(dict.fromkeys(line1))
        print(mylist)

        ci_hour = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        for data in mylist:
            # print("Thank you--->", data.strip())
            check_hour = data.split()
            # print(filename_avg,"--->", check_hour[0], check_hour[1])
            data_hour = check_hour[0].split(":")[0]
            # print("data_hour", data_hour)

            if(str(data_hour) == '00'): ci_hour[0].append(float(check_hour[1])) 
            if(str(data_hour) == '01'): ci_hour[1].append(float(check_hour[1]))
            if(str(data_hour) == '02'): ci_hour[2].append(float(check_hour[1]))
            if(str(data_hour) == '03'): ci_hour[3].append(float(check_hour[1]))
            if(str(data_hour) == '04'): ci_hour[4].append(float(check_hour[1]))
            if(str(data_hour) == '05'): ci_hour[5].append(float(check_hour[1]))
            if(str(data_hour) == '06'): ci_hour[6].append(float(check_hour[1]))
            if(str(data_hour) == '07'): ci_hour[7].append(float(check_hour[1]))
            if(str(data_hour) == '08'): ci_hour[8].append(float(check_hour[1]))
            if(str(data_hour) == '09'): ci_hour[9].append(float(check_hour[1]))
            if(str(data_hour) == '10'): ci_hour[10].append(float(check_hour[1]))
            if(str(data_hour) == '11'): ci_hour[11].append(float(check_hour[1]))
            if(str(data_hour) == '12'): ci_hour[12].append(float(check_hour[1]))
            if(str(data_hour) == '13'): ci_hour[13].append(float(check_hour[1]))
            if(str(data_hour) == '14'): ci_hour[14].append(float(check_hour[1]))
            if(str(data_hour) == '15'): ci_hour[15].append(float(check_hour[1]))
            if(str(data_hour) == '16'): ci_hour[16].append(float(check_hour[1]))
            if(str(data_hour) == '17'): ci_hour[17].append(float(check_hour[1]))
            if(str(data_hour) == '18'): ci_hour[18].append(float(check_hour[1]))
            if(str(data_hour) == '19'): ci_hour[19].append(float(check_hour[1]))
            if(str(data_hour) == '20'): ci_hour[20].append(float(check_hour[1]))
            if(str(data_hour) == '21'): ci_hour[21].append(float(check_hour[1]))
            if(str(data_hour) == '22'): ci_hour[22].append(float(check_hour[1]))
            if(str(data_hour) == '23'): ci_hour[23].append(float(check_hour[1]))

        # print("Avg raws to grouping ci hour -->", ci_hour)

        cii = 0

        # print("Write to Files ->>>>>>>>", filename_avg)

        file2 = open(src)
        content = file2.readlines()
        file.close()

        # print("-------------------------------------------------------------------------------------")
        # print(content)
        # print("-------------------------------------------------------------------------------------")

        sections = ['[CABLE1]\nCIRCUITNAME=CIRCUIT_1\n','\n[CABLE2]\nCIRCUITNAME=CIRCUIT_2\n','\n[AMBIENT]\n']

        cifile = APP_PATH + '/progout/'+str(year)+str(self.month_converter(Month))+str(Date)+Time_x+"_"+PointName+'_'+Channel+'.ci'
        file3 = open(cifile,"w")

        for _line in content:
            file3.write(_line)

        for section in sections:
            file3.write(section)
            for hour in ci_hour:
                # print("Hour", cii)
                cii += 1
                if(section.find("CIRCUIT_1") > 0):
                    file3.write(f"{cii:02}"+"."+"00"+" "+f"{self.month_converter(Month):02}"+"/"+str(Date)+" "+"419.000000"+" ")
                if(cii == 24): cii = 0
                # print("================")
                avg_val = 0
                total_val = 0
                for val in hour:
                    if(len(hour)):
                        total_val = (total_val + val)/len(hour)
                    else:
                        total_val = 0.0000000

                    # print("Lenght:", len(hour))
                    # print("Val:", val)

                if(section.find("CIRCUIT_1") > 0):                
                    file3.write(f"{total_val:.6f}"+"\n")

                if(section.find("CIRCUIT_2") > 0):
                    file3.write(f"{cii:02}"+"."+"00"+" "+f"{self.month_converter(Month):02}"+"/"+str(Date)+" "+"0.000000"+" ")
                if(cii == 24): cii = 0
                # print("================")
                avg_val = 0
                total_val = 0
                for val in hour:
                    total_val = 0.0000000
                    # print("Lenght:", len(hour))
                    # print("Val:", val)
                if(section.find("CIRCUIT_2") > 0):                
                    file3.write(f"{total_val:.6f}"+"\n")

            
            if(section.find("AMBIENT") > 0):
                file3.write("06.38 11/16 17.0"+"\n")
                file3.write("06.46 11/16 17.0"+"\n")
                file3.write("06.54 11/16 17.0"+"\n")
                file3.write("07.02 11/16 17.0"+"\n")
                file3.write("07.09 11/16 17.0"+"\n")
                file3.write("09.43 11/16 17.0"+"\n")
                file3.write("09.44 11/16 17.0"+"\n")
                file3.write("09.52 11/16 17.0"+"\n")
                file3.write("09.59 11/16 17.0"+"\n")
                file3.write("10.07 11/16 17.0"+"\n")
                file3.write("10.15 11/16 17.0"+"\n")
                file3.write("10.27 11/16 17.0"+"\n")
                file3.write("10.36 11/16 17.0"+"\n")
                file3.write("10.43 11/16 17.0"+"\n")
                file3.write("10.51 11/16 17.0"+"\n")
                file3.write("10.59 11/16 17.0"+"\n")
                file3.write("11.14 11/16 17.0"+"\n")
                file3.write("11.14 11/16 17.0"+"\n")
                file3.write("11.27 11/16 17.0"+"\n")
                file3.write("11.27 11/16 17.0"+"\n")
                file3.write("11.35 11/16 17.0"+"\n")
                file3.write("11.43 11/16 17.0"+"\n")
                file3.write("11.50 11/16 17.0"+"\n")
                file3.write("11.50 11/16 17.0"+"\n")


        file3.close()


        check_platform = platform.system()

        if(check_platform == 'Darwin'):
            print("I'm MacOS")

        if(check_platform == 'Windows'):

            print("I'm Windows")
            result_ci = APP_PATH + '\\rttrout\\'+str(year)+str(self.month_converter(Month))+str(Date)+Time_x+"_"+PointName+'_'+Channel+'.txt'

            command1 = "\"C:\\Program Files (x86)\\CYME\\CYMCAPRTTR\\CymcapRTR.exe\" "+cifile+" "+result_ci+" D:\\RTTR_Thermal_Sections_and_MDB\\1-CableTrenchTypeA_star\\E.txt D:\\RTTR_Thermal_Sections_and_MDB\\1-CableTrenchTypeA_star\\P.txt -hide_pg"
            returned_value1 = subprocess.call(command1, shell=True)  

            # print("\nresult_ci File:", result_ci)

            # result_ci = "C:\\app\\rttrout\\20211127112810_PointA_PhaseA.txt"
            result_ci = "C:\\app\\rttrout\\20211022113423_PointD_PhaseA.txt"


            if(os.path.exists(result_ci)):

                head, tail = os.path.split(result_ci)
                print("tail -> ",tail)
                filename = tail.split("_")
                print("tail -> ",filename[1][5:6])
                print("tail -> ",filename[2][5:6])

                Point = filename[1][5:6]
                Phase = filename[2][5:6]

                file1 = open(result_ci, "r")
                count = 0
                for line in file1:
                    count += 1
                    if(count == 1):
                        datax = line.strip().split(",")
                        temp_con = datax[1]
                        current = datax[2]
                        print("temp_con",temp_con)
                    print("Line{}: {}".format(count, line.strip()))
                file1.close()


                if(Point == "A"):
                    if(Phase == "A"):
                        self.threadSignalMain.emit(0, 'A', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)

                if(Point == "A"):
                    if(Phase == "B"):
                        self.threadSignalMain.emit(0, 'B', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)

                if(Point == "A"):
                    if(Phase == "C"):
                        self.threadSignalMain.emit(0, 'C', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)


                if(Point == "B"):
                    if(Phase == "A"):
                        self.threadSignalMain.emit(1, 'A', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)

                if(Point == "B"):
                    if(Phase == "B"):
                        self.threadSignalMain.emit(1, 'B', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)

                if(Point == "B"):
                    if(Phase == "C"):
                        self.threadSignalMain.emit(1, 'C', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)

                if(Point == "C"):
                    if(Phase == "A"):
                        self.threadSignalMain.emit(2, 'A', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)

                if(Point == "C"):
                    if(Phase == "B"):
                        self.threadSignalMain.emit(2, 'B', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)

                if(Point == "C"):
                    if(Phase == "C"):
                        self.threadSignalMain.emit(2, 'C', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)

                if(Point == "D"):
                    if(Phase == "A"):
                        self.threadSignalMain.emit(3, 'A', "22222222222", 99, float(temp_con), float(current), -99.00, 0.00, 0.00, 0.00, 0.00, 0.00)



        # Excute RTTR here
        print("\n\n\nExcute RTTR File:", cifile)
        print("\n\n\n")


    def month_converter(self ,month):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        return months.index(month) + 1


    def stop(self, *args, **kwargs):
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    oMainwindow = MainWindow()
    oMainwindow.show()
    sys.exit(app.exec_())
