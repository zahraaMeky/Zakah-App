#!C:\Users\evdev\PycharmProjects\zakah\venv\Scripts python.exe

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from time import sleep
from threading import Thread

class Window(QMainWindow):

    def __init__(self):
        super(Window,self).__init__()
        self.browser = QWebEngineView()
        #self.pbar = QProgressBar(self)
        self.browser.setUrl(QUrl('http://127.0.0.1:8000/'))
        self.setCentralWidget(self.browser)
        self.showMaximized()
        #self.timer = QTimer()
        #self.timer.timeout.connect(self.ShowProgress)
        #self.timer(15000)


    def ShowProgress(self):
        for i in range(101):
            sleep(0.15)
            self.pbar.setValue(i)

        self.browser.setUrl(QUrl('http://127.0.0.1:8000/'))
        self.setCentralWidget(self.browser)
        self.showMaximized()
        self.timer.stop()

    def loadUrl(self):
        url = self.searchBar.text()
        self.browser.setUrl(QUrl(url))

def start_app():
    os.system('cd D:\\zakah\\zakahDeviceDjango\\ && D:\\zakah\\venv\Scripts\\python.exe manage.py runserver')

def run_printer_app():
    os.system('C:\\BIXOLON\\Web_Print_SDK\\Web_Print_SDK.exe')

Thread(target=start_app, args=()).start()
Thread(target=run_printer_app, args=()).start()
sleep(15)
MyApp = QApplication(sys.argv)
QApplication.setApplicationName('Donate App')
window = Window()
window.showFullScreen()
MyApp.exec_()