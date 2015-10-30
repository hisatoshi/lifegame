#coding:utf-8

from datetime import datetime as dt
from lifePy.LifeGame import Cells
from PyQt5.QtWidgets import (QApplication, QWidget)
from PyQt5.QtCore import (QSize, QLine, QPoint, QTimer, Qt)
from PyQt5.QtGui import (QPainter, QColor, QPen, QMouseEvent)

#coding:utf-8

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.__initCells__()
        self.__initUI__()
        self.__initTimer__()

    def __initCells__(self) :
        self.cY=300
        self.cX=300
        self.cSize=10
        self.Cells = Cells(self.cY,self.cX)
        #ランダムでセルを作る
        #self.Cells.randomBorn()
        #セルを指定して作る
        #self.Cells.setTrues([(404,x) for x in range(80)])
        #グライダー
        #self.Cells.setTrues([(24, 0),(22, 1),(24, 1),(12, 2),(13, 2),(20, 2),(21, 2),(34, 2),(35, 2),(11, 3),(15, 3),(20, 3),(21, 3),(34, 3),(35, 3),(0, 4),(1, 4),(10, 4),(16, 4),(20, 4),(21, 4),(0, 5),(1, 5),(10, 5),(14, 5),(16, 5),(17, 5),(22, 5),(24, 5),(10, 6),(16, 6),(24, 6),(11, 7),(15, 7),(12, 8),(13, 8)])
        self.Cells.setTrues([(0,0)])

    def __initUI__(self) :
        self.setGeometry(300,300,self.cX*self.cSize+1,self.cY*self.cSize+1)
        self.setStyleSheet("background-color : black")
        self.show()

    def __initTimer__(self) :
        self.interval = 100
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.nextScreen)
        self.timer.setInterval(self.interval)
        self.timer.start()

    def nextScreen(self) :
        self.Cells.nextGeneration()
        self.update()


    def mousePressEvent(self,event) :

        x,y = map(int,[event.x()/self.cSize, event.y()/self.cSize])
        if self.Cells.getAlive(y,x):
            self.Cells.setAlive(y,x,False)
        else :
            self.Cells.setAlive(y,x,True)
        self.update()

    def keyPressEvent(self,event) :

        #shiftKey
        if event.key() == 16777248 :
            self.timer.stop()
        #commandKey
        elif event.key() == 16777249 :
            self.timer.stop()
            self.Cells.randomBorn()
            self.timer.start()
        #sKey(save)
        elif event.key() == 83 :
            cells = self.Cells.getTupple()
            dtNow = dt.now()
            dStr = dtNow.strftime('%Y%m%d')
            f = open(dStr+".dat","w")
            for p in cells :
                f.write(",".join(map(str,list(p))))
                f.write("\n")
        #lKey(load)
        elif event.key() == 76 :
            #そのうち実装する
            pass
        else :
            print(event.key())

    def keyReleaseEvent(self,event) :

        #shiftKey
        if event.key() == 16777248 :
            self.timer.start()

    def paintEvent(self,event) :
        qp = QPainter()
        qp.begin(self)
        self.drawScreen(event,qp)
        qp.end()


    def drawScreen(self,event,qp) :
        self.drawLines(event,qp)
        self.drawCells(event,qp)

    def drawLines(self, event, qp):
        pen = QPen(QColor(0,255,0), 1, Qt.SolidLine)
        bpen = QPen(QColor(0,0,0),1, Qt.SolidLine)
        qp.setPen(pen)
        xs = [x*self.cSize for x in range(self.cX+1)]
        ys = [y*self.cSize for y in range(self.cY+1)]
        for x in xs :
            qp.drawLine(QPoint(x,0),QPoint(x,self.cY*self.cSize+1))
        for y in ys :
            qp.drawLine(QPoint(0,y),QPoint(self.cX*self.cSize+1,y))

    def drawCells(self,event,qp) :
        qp.setBrush(QColor(0, 255, 0))
        for (x,y) in self.Cells.getTupple():
            qp.drawRect(x*self.cSize, y*self.cSize, self.cSize, self.cSize)
