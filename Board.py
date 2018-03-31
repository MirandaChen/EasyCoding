import math,random,copy,pygame
from helperFunctions import roundHalfUp,distance,matrixMult,testMatrixMult,createText,loadImage,make2dBoard,clickInButton
# ======= constants =======
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
DBI = "button-blue.png" # default button image
TURN_LEFT = [[0,-1],[1,0]] # inner list is a row
TURN_RIGHT =[[0,1],[-1,0]]

class Board(object):
    def __init__(self,board):
        # in the board(2d list): 0-no path, 1-path, 2-goals,3-reached goals
        self.init_board = copy.deepcopy(board)
        self.board = copy.deepcopy(board)
        self.dim = len(board)
        self.angle = 45 * math.pi / 180
        self.grid_tx = 150
        self.grid_ty = 200
        self.cell_x = 60
        self.cell_y = 30

    def __repr__(self):
        return str(self.board)
    def drawTiltedBoard(self,screen):
        for row in range(self.dim):
            for col in range(self.dim):
                if self.board[row][col]!=0:
                    # if width is zero then the polygon will be filled
                    width = 1 if self.board[row][col] == 1 else 0
                    color = YELLOW if self.board[row][col] == 3 else BLACK
                    pointlist = self.getCellBound(row,col)
                    pygame.draw.polygon(screen, color, pointlist,width)

    def resetBoard(self):
        self.board = copy.deepcopy(self.init_board)

    def getCellBound(self,row,col):
        y1 = self.grid_ty + row*self.cell_y
        y2 = y1 + self.cell_y
        x1 = roundHalfUp(self.grid_tx + col*self.cell_x- self.cell_y*row/math.tan(self.angle))
        x2 = x1 + self.cell_x
        x3 = roundHalfUp(x1 - self.cell_y/math.tan(self.angle))
        x4 = x3 + self.cell_x
        return [(x1,y1),(x2,y1),(x4,y2),(x3,y2)]