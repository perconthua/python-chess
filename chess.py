#! -*- coding: utf-8 -*-
from operator import xor
import random
class piece(object):
    row=0
    column=0
    def __init__(self,board,player,row,column):
        self.player=player
        self.row=row
        self.column=column
        self.board=board
    def getIcon(self):
        if self.__class__.__name__ is 'empty':
            return " "
        icons={}
        icons['B']={}
        icons['B']['pawn']=u"\u2659"
        icons['B']['castle']=u"\u2656"
        icons['B']['knight']=u"\u2658"
        icons['B']['bishop']=u"\u2657"
        icons['B']['king']=u"\u2654"
        icons['B']['queen']=u"\u2655"

        icons['W']={}
        icons['W']['castle']=u"\u265C"
        icons['W']['knight']=u"\u265E"
        icons['W']['bishop']=u"\u265D"
        icons['W']['king']=u"\u265A"
        icons['W']['queen']=u"\u265B"
        icons['W']['pawn']=u"\u265F"
        return icons[self.player][self.__class__.__name__]
    def getShortMoves(self):
        piece=self.__class__.__name__
        row=self.row
        column=self.column
        return [self.getPosition((row+moves[0],column+moves[1])) for moves in self.listmoves if self.inBoard(row+moves[0],column+moves[1]) and self.player!=self.board[row+moves[0]][column+moves[1]].player]
    def getLongMoves(self):
        piece=self.__class__.__name__
        row=self.row
        column=self.column
        data=[]
        for moves in self.listmoves:
            i=1
            while self.inBoard(row+moves[0]*i,column+moves[1]*i) and self.board[row+moves[0]*i][column+moves[1]*i].player==" ":
                data.append(self.getPosition((row+moves[0]*i,column+moves[1]*i)))
                i+=1
            if self.inBoard(row+moves[0]*i,column+moves[1]*i) and self.board[row+moves[0]*i][column+moves[1]*i].player not in (self.player," "):
                data.append(self.getPosition((row+moves[0]*i,column+moves[1]*i)))
        return data
    
    def inBoard(self,row,column):
        return row in range(8) and column in range(8)
    def getPosition(self,l):
        return chr(ord("A")+l[1])+str(l[0]+1)


class king(piece):
    def __init__(self,board,player,row,column):
        super(king,self).__init__(board,player,row,column)
        self.listmoves=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]
    def getMoves(self):
        return super(king,self).getShortMoves()

class queen(piece):
    def __init__(self,board,player,row,column):
        super(queen,self).__init__(board,player,row,column)
        self.listmoves=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]
    def getMoves(self):
        return super(queen,self).getLongMoves()

class bishop(piece):
    def __init__(self,board,player,row,column):
        super(bishop,self).__init__(board,player,row,column)
        self.listmoves=[(1,1),(-1,-1),(1,-1),(-1,1)]
    def getMoves(self):
        return super(bishop,self).getLongMoves()

class knight(piece):
    def __init__(self,board,player,row,column):
        super(knight,self).__init__(board,player,row,column)
        self.listmoves=[(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]
    def getMoves(self):
        return super(knight,self).getShortMoves()

class castle(piece):
    def __init__(self,board,player,row,column):
        super(castle,self).__init__(board,player,row,column)
        self.listmoves=[(1,0),(-1,0),(0,1),(0,-1)]
    def getMoves(self):
        return super(castle,self).getLongMoves()

class pawn(piece):
    def __init__(self,board,player,row,column):
        super(pawn,self).__init__(board,player,row,column)
        if row<4:
            self.listmoves=[(1,0)]
        else:
            self.listmoves=[(-1,0)]
    def getMoves(self):
        row=self.row
        column=self.column
        data=[]
        updown=self.listmoves[0][0]
        if self.inBoard(row+updown,column):
            if self.board[row+updown][column].player==" ":
                data.append(self.getPosition((row+updown,column)))
        if row in (1,6) and (self.board[row+updown*2][column].player+self.board[row+updown][column].player)=="  ":
            data.append(self.getPosition((row+updown*2,column)))
        
        d1a,d1b=(row+updown,column+1)
        d2a,d2b=(row+updown,column-1)
        if self.inBoard(d1a,d1b) and self.board[d1a][d1b].player not in (self.player," "):
            data.append(self.getPosition((d1a,d1b)))
        if self.inBoard(d2a,d2b) and self.board[d2a][d2b].player not in (self.player," "):
            data.append(self.getPosition((d2a,d2b)))
        return data
        
class empty(piece):
    def __init__(self,board,player,row,column):
        super(empty,self).__init__(board,player,row,column)
        self.listmoves=[]

class chessBoard(object):
    def __init__(self):
        self.initBoard()
        self.play()
    def initBoard(self):
        self.message=""
        self.gameEnd=False
        self.winner=""
        self.board=range(8)
        players=['W','B']
        color1=random.choice(players)
        players.remove(color1)
        color2=players[0]

        for x in xrange(8):
            self.board[x]=range(8)
            for y in xrange(8):
                self.add(empty(self.board,' ',x,y))
        for x in range(8):
            self.add(pawn(self.board,color1,1,x))
            self.add(pawn(self.board,color2,6,x))

        self.add(castle(self.board,color1,0,0))
        self.add(castle(self.board,color1,0,7))
        self.add(knight(self.board,color1,0,1))
        self.add(knight(self.board,color1,0,6))
        self.add(bishop(self.board,color1,0,2))
        self.add(bishop(self.board,color1,0,5))
        self.add(  king(self.board,color1,0,4))
        self.add( queen(self.board,color1,0,3))
        self.add(castle(self.board,color2,7,0))
        self.add(castle(self.board,color2,7,7))
        self.add(knight(self.board,color2,7,1))
        self.add(knight(self.board,color2,7,6))
        self.add(bishop(self.board,color2,7,2))
        self.add(bishop(self.board,color2,7,5))
        self.add( queen(self.board,color2,7,4))
        self.add(  king(self.board,color2,7,3))
        
    def add(self,piece):
        self.board[piece.row][piece.column]=piece

    def draw(self):
        print "\n"*10
        print "Ajedrez en consola!!!"
        print "========================"
        print "\n ABCDEFGH"
        for k,x in enumerate(self.board):
            row=""
            for k2,obj in enumerate(x):
                if obj.getIcon()==" ":
                    if xor(k%2==0,k2%2==0):
                        row+=u"\u2591"
                    else:
                        row+=u"\u2593"
                else:
                    row+=obj.getIcon()

            print str(k+1)+row+str(k+1)
        print " ABCDEFGH"
        
        
    def drawHD(self):
        print "\n"*10
        print "Ajedrez en consola!!!"
        print "========================"
        print "   "+"   ".join(list("ABCDEFGH"))
        for k,x in enumerate(self.board):
            print " "+("+---")*len(self.board[0])+"+"
            row=""
            for obj in x:
                row+=obj.getIcon()
            print str(k+1)+"| "+" | ".join(row)+" |"+str(k+1)

        print " "+"+---"*len(self.board[0])+"+"
        print "   "+"   ".join(list("ABCDEFGH"))

    def getCordinates(self,cordinate):
        cordinate=list(cordinate.upper())
        cordinate[0]=int(ord(cordinate[0])-ord("A"))
        cordinate[1]=int(cordinate[1])-1
        return (cordinate[1],cordinate[0])

    def movePiece(self,move):
        start,end=move.split(" ")
        r1,c1=self.getCordinates(start)
        r2,c2=self.getCordinates(end)
        
        p1=self.board[r1][c1]
        p2=self.board[r2][c2]
        p1.row=r2
        p1.column=c2
        if p2.__class__.__name__=="king":
            self.gameEnd=True
            self.winner=p1.player
        self.add(empty(self.board,' ',r1,c1))
        self.add(p1)

    def isValidMove(self,move,player):
        move=move.upper().strip()
        if len(move)!=5 or move[2]!=" " \
            or move[0] not in "ABCDEFGH" \
            or move[3] not in "ABCDEFGH" \
            or move[1] not in "12345678" \
            or move[4] not in "12345678":
            self.message="Jugada inválida,use el formato: 'LD LD' : L=(A,B,C,D,E,F,G,H) D=(1,2,3,4,5,6,7,8)"
            return False
        start,end=move.split(" ")
        if start == end:
            self.message="El destino debe ser diferente al origen!"
            return False
        r1,c1=self.getCordinates(start)
        r2,c2=self.getCordinates(end)
        if self.board[r1][c1].player==" ":
            self.message="La posición %s esta vacía"%start
            return False
        if self.board[r1][c1].player!=player:
            self.message="La Ficha que intenta mover es del otro jugador"
            return False
        if end not in self.board[r1][c1].getMoves():
            self.message="No puede mover desde %s hacia %s"%(start,end)
            return False
        return True

    def play(self):
        icon={}
        name={}
        icon['W']=king(None,'W',0,0).getIcon()
        icon['B']=king(None,'B',0,0).getIcon()
        name['W']="Blanco"
        name['B']="Negro "
        history=""
        player=random.choice(['W','B'])
        print "\nAJEDREZ EN CONSOLA"
        print "=================="
        print "Elija un modo de visualización (se recomienda la fuente Deja Vu Sans Mono)"
        print "1) Modo Full HD (recommended)"
        print "2) Modo solicitado "
        print("opcion:"),
        if raw_input()=="2":
            draw=self.draw
        else:
            draw=self.drawHD
        draw()
        while not self.gameEnd:
            print ("\n%s %s>"%(name[player].strip(),icon[player])),
            move=raw_input()
            if move.strip()=="":
                draw()
                continue
            if self.isValidMove(move,player):
                self.movePiece(move)
                draw()
                player=('W','B')[player=='W']
                history+=name[player]+":"+move+"\n"
            else:
                draw()
                print self.message
        print "Historial de jugadas"
        print "===================="
        print history
        print "El ganador es el jugador %s %s :)"%(name[self.winner],icon[self.winner])

if __name__ == "__main__":
    chessBoard()