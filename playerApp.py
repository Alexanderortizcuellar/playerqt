from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from player import Ui_MainWindow
import sys

def duration(ms):
    minutes, seconds = divmod(ms,60000)
    seconds,_ = divmod(seconds,1000)
    return f"{minutes}:{seconds}"

def dur(ms,pos):
    ms = ms-pos
    minutes, seconds = divmod(ms,60000)
    seconds,_ = divmod(seconds,1000)
    pos+=pos
    return f"{minutes}:{seconds}"


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.player = QMediaPlayer()
        self.player.setVolume(self.volumeSlider.value())
        self.player.durationChanged.connect(self.updateDuration)
        self.player.positionChanged.connect(self.updatePosition)
        self.volumeSlider.valueChanged.connect(self.player.setVolume)
        self.durationslider.valueChanged.connect(self.player.setPosition)
        self.list = self.playerList
        self.list.addItem(r"C:\Users\ASUS\qt_programs\player\fur elise (Ludwig van Beethoven).3gpp")
        self.playbtn.clicked.connect(self.play_pause)
        self.stopbtn.clicked.connect(lambda x:self.player.setPosition(0))
        self.pushButton_5.clicked.connect(self.mute)
        self.actionOpen_File.triggered.connect(self.playSong)
        self.actionOpen_Folder.triggered.connect(self.openFolder)
        
    def updateDuration(self,d):
        self.durationslider.setRange(0,d)
    def updatePosition(self,v):
        self.durationslider.blockSignals(True)
        self.durationslider.setValue(v)
        self.durationslider.blockSignals(False)
        self.durationProgress.setText(duration(v))
        self.duration.setText(dur(self.player.duration(),v))
    def updateState(self,state):
        pass
    def playSong(self):
        f = QFileDialog.getOpenFileName(self,"Choose a file")
        file = QUrl.fromLocalFile(f[0])
        self.content = QMediaContent(file)
        self.player.setMedia(self.content)
        self.player.play()
        self.playbtn.setIcon(QIcon("pause.png"))
    def play_pause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.playbtn.setIcon(QIcon("play.png"))
        else:
            self.player.play()
            self.playbtn.setIcon(QIcon("pause.png"))
    def mute(self):
        if self.player.isMuted():
            self.player.setMuted(False)
            self.pushButton_5.setIcon(QIcon("speaker.png"))
        else:
            self.player.setMuted(True)
            self.pushButton_5.setIcon(QIcon("speaker-volume-control-mute"))
    def openFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "open Folder")
        fol = QDir(folder)
        files = QDirIterator(fol)
        while files.hasNext():
            self.list.addItem(files.next())

    def contextMenuEvent(self, event):
        menu = QMenu()
        togle = QAction("Stop") if self.player.state() == QMediaPlayer.PlayingState else QAction("Play")
        icon = togle.setIcon(QIcon("pause.png")) if self.player.state() == QMediaPlayer.PlayingState else togle.setIcon(QIcon("play.png"))
        menu.addAction(togle)
        speed = menu.addMenu("Speed")
        fast = speed.addAction("Fast")
        faster = speed.addAction("Faster")
        normal = speed.addAction("Normal")
        slow = speed.addAction("Slow")
        slower = speed.addAction("Slower")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        
    def closeEvent(self, event):
        msg = QMessageBox.question(self,"Quit", "Do you want to quit?")
        if msg == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


        
        


app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()


