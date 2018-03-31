from helperFunctions import roundHalfUp,distance,matrixMult,testMatrixMult,createText,loadImage,make2dBoard,clickInButton
# ======= constants =======
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
DBI = "button-blue.png" # default button image
TURN_LEFT = [[0,-1],[1,0]] # inner list is a row
TURN_RIGHT =[[0,1],[-1,0]]
# one robot only has one position on a board
# a robot has a default direction
class Robot(object):
    def __init__(self,curr_row,curr_col,mapBoard,direction=(0,1)):
        self.init_row = curr_row
        self.init_col = curr_col 
        self.init_dir = direction # these 3 values never change
        self.curr_row = curr_row
        self.curr_col = curr_col
        self.map = mapBoard
        board = make2dBoard(self.map.dim)
        board[curr_row][curr_col] = 1
        self.board = board
        self.dir = direction # a tuple

    def resetBot(self):
        self.curr_row = self.init_row
        self.curr_col = self.init_col
        self.dir = self.init_dir
        board = make2dBoard(self.map.dim)
        board[self.init_row][self.init_col] = 1
        self.board = board

    def isLegalMove(self,map,drow,dcol):
        newRow, newCol = self.curr_row+drow,self.curr_col+dcol
        # off the board
        if (newRow<0 or newRow>=map.dim or newCol<0 or newCol>=map.dim):
            return False
        # no path
        if map.board[newRow][newCol] == 0: return False
        return True

    def turnLeft(self):
        newDir = matrixMult(TURN_LEFT,self.dir)
        self.dir = tuple(newDir)

    def turnRight(self):
        newDir = matrixMult(TURN_RIGHT,self.dir)
        self.dir = tuple(newDir)

    def moveForward(self,step,data):
        # move forward
        drow = self.dir[0]*step
        dcol = self.dir[1]*step
        prev = (self.curr_row,self.curr_col) # memorize pos before change
        self.updatePos(drow,dcol)
        new = (self.curr_row,self.curr_col)
        if data.board.board[new[0]][new[1]]==2:
                    data.board.board[new[0]][new[1]] = 3

    def updatePos(self,drow,dcol):
        if self.isLegalMove(self.map,drow,dcol):
            self.board[self.curr_row][self.curr_col] = 0 # delete curr pos
            # update curr pos
            self.curr_row,self.curr_col=self.curr_row+drow,self.curr_col+dcol 
            self.board[self.curr_row][self.curr_col] = 1 # change new pos

    def drawRobot(self,screen): # for now, robot is a red circle
        ul = self.map.getCellBound(self.curr_row,self.curr_col)[0]
        loadImage(screen,"bb8.png",ul[0]-30,ul[1]-50)