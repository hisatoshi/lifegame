#coding:utf-8
import random
import time

#セルのクラス
class Cell() :
    def __init__(self):
        self.alive=False

    def getAlive(self):
        return self.alive
    def setAlive(self,t) :
        self.alive = t

#セルをまとめておくクラス
class Cells() :
    def __init__(self,y,x) :
        #セルの上下左右に１つずつ余剰のセルを作ることで
        #端っこのセルでも自分を中央とした8つのセルをみて生存確認ができる
        self.y=y
        self.x=x
        self.Cells=[[Cell() for i in range(x+2)] for j in range(y+2)]
        self.nextCells=[[False for i in range(x)] for j in range(y)]


    def getAlive(self,y,x) :
        if self.Cells[y+1][x+1].getAlive() :
            return True
        else :
            return False

    def setAlive(self,y,x,t) :
        self.Cells[y+1][x+1].setAlive(t)

    def randomBorn(self):
        num = random.randint(0,self.x*self.y)
        self.setTrues([(random.randint(0,self.y-1), random.randint(0,self.x-1))for i in range(num)])

    def setTrues(self,yxTupples):
        for (y,x) in yxTupples :
            self.setAlive(y,x, True)


    def getTupple(self) :
        return [(x-1,y-1) for (y, vectorCell) in enumerate(self.Cells) for (x, Cell) in enumerate(vectorCell) if Cell.getAlive()]


    #あるセルの周りにいくつ生存しているセルが存在してるかの確認
    def _checkAroundAliveCellNum(self,int pY,int pX) :
        return sum([1 if self.getAlive(y,x) and (not (pX==x and pY==y)) else 0 for x in [pX-1, pX, pX+1] for y in [pY-1, pY, pY+1]])

    #セルの次の世代での生死を判別
    #ここをうまく高速化
    def _checkAlive(self) :
        cdef int pY, pX
        for (pY, pX) in [(y,x) for y in range(self.y) for x in range(self.x)] :
            num = self._checkAroundAliveCellNum(pY,pX)
            if(self.getAlive(pY,pX)) :
                if(2<=num<=3) :
                    self.nextCells[pY][pX]=True
                else :
                    self.nextCells[pY][pX]=False
            else :
                if(num==3) :
                    self.nextCells[pY][pX]=True
                else :
                    self.nextCells[pY][pX]=False



    #次の世代へ移行
    def _goNext(self) :
        for (vectorNext,vectorPresent) in zip(self.nextCells,self.Cells[1:-1]) :
            for (nextCell, PresentCell) in zip(vectorNext, vectorPresent[1:-1]) :
                if(nextCell) :
                    PresentCell.setAlive(True)
                else :
                    PresentCell.setAlive(False)


    #外部からはこれを呼ぶだけでおっけー
    def nextGeneration(self) :
        a=time.time()
        self._checkAlive()
        b=time.time()
        self._goNext()
        c=time.time()
        print("チェックにかかる時間 : "+str(b-a))
        print("次に行く時間 : "+str(c-b))
