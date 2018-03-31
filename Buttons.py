import math,random,copy,pygame
from helperFunctions import roundHalfUp,distance,matrixMult,testMatrixMult,createText,loadImage,make2dBoard,clickInButton

# ======================= classes ===========================
# ======= constants =======
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
DBI = "button-blue.png" # default button image
TURN_LEFT = [[0,-1],[1,0]] # inner list is a row
TURN_RIGHT =[[0,1],[-1,0]]
# Button:takes in top-left corner,width,height,image,displaytext and textsize
class Button(object):
    def __init__(self,x,y,w,h,text=None,textSize=40,fileName=DBI):
        self.x = x 
        self.y = y
        self.w = w
        self.h = h
        self.cx = x + w//2 # center point
        self.cy = y + h//2
        self.text = text
        self.textSize = textSize
        self.fileName = fileName

    def drawButton(self,screen):
        # draw bkgd
        if self.fileName != None:
            loadImage(screen,self.fileName,self.x,self.y,self.w,self.h)
        # draw text
        if self.text != None: 
            createText(screen,self.x+10,self.y+10,self.text,self.textSize)

    def __repr__(self):
        return self.text

    def __hash__(self): # to put in dictionary
        return hash(self.text)

class AddButton(Button):
    def __init__(self,x,y,w=56,h=128,text="Add",textSize=40,fileName="sidebutton-yellow.png"):
        super().__init__(x,y,w,h,text,textSize,fileName)

    def drawButton(self,screen):
        loadImage(screen,self.fileName,self.x,self.y,self.w,self.h)  

class SwitchToHelper(Button):
    def __init__(self,x,y,w=56,h=128,text="Helper",textSize=40,fileName="sidebutton-blue.png"):
        super().__init__(x,y,w,h,text,textSize,fileName)

    def drawButton(self,screen):
        loadImage(screen,self.fileName,self.x,self.y,self.w,self.h)

class SwitchToMain(Button):
    def __init__(self,x,y,w=56,h=128,text="",textSize=40,fileName="sidebutton-green.png"):
        super().__init__(x,y,w,h,text,textSize,fileName)

    def drawButton(self,screen):
        loadImage(screen,self.fileName,self.x,self.y,self.w,self.h)

class BackButton(Button):
    def __init__(self,x,y,w=120,h=60,text="Back",textSize=40,fileName="button-back.png"):
        super().__init__(x,y,w,h,text,textSize,fileName)

    def drawButton(self,screen):
        loadImage(screen,self.fileName,self.x,self.y,self.w,self.h)

class RunButton(Button):
    def __init__(self,x,y,w=70,h=70,text="Run",textSize=None,fileName="button-run.png"):
        super().__init__(x,y,w,h,text,textSize,fileName)

    def drawButton(self,screen):
        loadImage(screen,self.fileName,self.x,self.y,self.w,self.h)

class LevelButton(Button):
    def __init__(self,x,y,w,h,text,textSize=40,fileName="button-stamp.png"):
        super().__init__(x,y,w,h,text,textSize,fileName)

# command buttons
class MoveButton(Button):
    def __init__(self,x=0,y=0,w=200,h=50,text=None,textSize=40,fileName=DBI,moveStep=1):
        super().__init__(x,y,w,h,text,textSize,fileName)
        self.text = "Move"
        self.moveStep = moveStep # int
        self.highLight = False
        self.moveList = []
        self.changing = False

    def makeMoveList(self):
        self.moveList=[]
        for i in range(self.moveStep):
            self.moveList.append(MoveButton(0,0))

    def createNewButton(self,x,y): # given new x,y pos
        return MoveButton(x,y,self.w,self.h,self.text,self.textSize,DBI)

    def drawButton(self,screen):
        loadImage(screen,self.fileName,self.x,self.y,self.w,self.h)
        text = self.text + " %d step" %self.moveStep
        createText(screen,self.x+10,self.y+10,text,self.textSize)
        if self.highLight == True:
            pygame.draw.rect(screen,RED,(self.x,self.y,self.w,self.h),5)

class TurnRightButton(Button):
    def __init__(self,x=None,y=None,w=150,h=50,text=None,textSize=40,fileName=DBI):
        super().__init__(x,y,w,h,text,textSize,fileName)
        self.text = "Turn Right"

    def createNewButton(self,x,y): # given new x,y pos
        return TurnRightButton(x,y,self.w,self.h,self.text,self.textSize)

class TurnLeftButton(Button):
    def __init__(self,x=None,y=None,w=150,h=50,text=None,textSize=40,fileName=DBI):
        super().__init__(x,y,w,h,text,textSize,fileName)
        self.text = "Turn Left"

    def createNewButton(self,x,y): # given new x,y pos
        return TurnLeftButton(x,y,self.w,self.h,self.text,self.textSize)

class IfElseButton(Button): 
    def __init__(self,x=None,y=None,w=150,h=50,text=None,textSize=40,fileName=DBI,extended=False):
        super().__init__(x,y,w,h,text,textSize,fileName)
        self.text = "If-Else"
        self.extended = extended
        self.mode = 1 # 2,3,4
        self.text1 = "If has Path: Move;Else: Jump"
        self.text2 = "If has Path: Jump;Else: Move"
        self.text3 = "If no Path: Jump;Else: Move"
        self.text4 = "If no Path: Move;Else: Jump"
        self.highLight = False
        self.changing = False

    def drawButton(self,screen):
        if self.extended == False:
            super().drawButton(screen)
        else:
            loadImage(screen,self.fileName,self.x,self.y,self.w+250,self.h)
            createText(screen,self.x+10,self.y+10,self.text1,self.textSize)
            if self.highLight == True:
                pygame.draw.rect(screen,RED,(self.x,self.y,self.w+250,self.h),5)


    def createNewButton(self,x,y): # given new x,y pos
        return IfElseButton(x,y,self.w,self.h,self.text,self.textSize,extended=True)

class JumpButton(Button):
    def __init__(self,x=None,y=None,w=150,h=50,text=None,textSize=40,fileName=DBI):
        super().__init__(x,y,w,h,text,textSize,fileName)
        self.text = "Jump"

    def createNewButton(self,x,y): # given new x,y pos
        return JumpButton(x,y,self.w,self.h,self.text,self.textSize)

class RepeatButton(Button):
    def __init__(self,x=None,y=None,w=200,h=50,text=None,textSize=40,fileName=DBI,repeatTimes=1):
        super().__init__(x,y,w,h,text,textSize,fileName)
        self.text = "Repeat"
        self.repeatTimes = repeatTimes
        self.highLight = False
        self.repeatList = []
        self.changing = False

    def createNewButton(self,x,y): # given new x,y pos
        return RepeatButton(x,y,self.w,self.h,self.text,self.textSize)

    def drawButton(self,screen):
        loadImage(screen,self.fileName,self.x,self.y,self.w,self.h)
        text = self.text + " %d time" %self.repeatTimes
        createText(screen,self.x+10,self.y+10,text,self.textSize)
        if self.highLight == True:
            pygame.draw.rect(screen,RED,(self.x,self.y,self.w,self.h),5)

class HelperFunctionButton(Button):
    def __init__(self,x=None,y=None,w=220,h=50,text=None,textSize=40,fileName=DBI):
        super().__init__(x,y,w,h,text,textSize,fileName)
        self.text = "Helper Function"

    def createNewButton(self,x,y): # given new x,y pos
        return HelperFunctionButton(x,y,self.w,self.h,self.text,self.textSize)

class GoButton(Button):
    def __init__(self,x,y,w=120,h=120,text="Go",textSize=40,fileName="go.png"):
        super().__init__(x,y,w,h,text,textSize,fileName)

    def drawButton(self,screen):
        loadImage(screen,self.fileName,self.x,self.y,self.w,self.h)

class FastButton(Button):
    def __init__(self,x,y,w=100,h=40,text="Fast",textSize=40,fileName=DBI):
        super().__init__(x,y,w,h,text,textSize,fileName)
        self.highLight = False

    def drawButton(self,screen):
        # draw text
        if self.text != None: 
            createText(screen,self.x+10,self.y+10,self.text,self.textSize)
        if self.highLight == True:
            pygame.draw.rect(screen,BLACK,(self.x,self.y,self.w,self.h),5)

class SlowButton(Button):
    def __init__(self,x,y,w=100,h=40,text="Slow",textSize=40,fileName=DBI):
        super().__init__(x,y,w,h,text,textSize,fileName)
        self.highLight = True

    def drawButton(self,screen):
        # draw text
        if self.text != None: 
            createText(screen,self.x+10,self.y+10,self.text,self.textSize)
        if self.highLight == True:
            pygame.draw.rect(screen,BLACK,(self.x,self.y,self.w,self.h),5)

class NextButton(Button):
    def __init__(self,x,y,w=50,h=50,text="Next",textSize=40,fileName="next2.png"):
        super().__init__(x,y,w,h,text,textSize,fileName)

    def drawButton(self,screen):
        loadImage(screen,self.fileName,self.x,self.y,self.w,self.h)

class HasPathButton(Button):
    pass

class NoPathButton(Button):
    pass