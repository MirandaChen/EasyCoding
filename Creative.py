import math,random,copy,pygame
from helperFunctions import roundHalfUp,distance,matrixMult,testMatrixMult,createText,loadImage,make2dBoard,clickInButton
from Buttons import Button,AddButton,SwitchToHelper,SwitchToMain,BackButton,RunButton,LevelButton,MoveButton,FastButton,SlowButton
from Buttons import TurnLeftButton,TurnRightButton,IfElseButton,JumpButton,RepeatButton,HelperFunctionButton,GoButton
from Robot import Robot
from Board import Board
from Level import Level
# ======= constants =======
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
DBI = "button-blue.png" # default button image
TURN_LEFT = [[0,-1],[1,0]] # inner list is a row
TURN_RIGHT =[[0,1],[-1,0]]

class Creative(Level):
    def __init__(self,level,obj,tip,board,levelCBList,bot_x,bot_y,hasHelperFunction=True):
        super().__init__(level,obj,tip,board,levelCBList,bot_x,bot_y,hasHelperFunction)
        # self.hasHelperFunction = hasHelperFunction
        # self.codeMode = "main" # or "helper"
        # self.chosenButton = None # mouse event
        # self.addingRepeat = False
        # self.win = False

        # self.level = level # an int
        # self.levelText = "level%d" %self.level
        # self.obj = obj
        # self.tip = tip # string
        # self.init_board = copy.deepcopy(board) # for reset use
        # self.board = Board(board) # create the board
        # self.levelCBList = levelCBList
        # self.bot = Robot(bot_x,bot_y,self.board)
        # if self.level == 6: 
        #     self.hasBot2 = False
        #     self.bot2 = Robot(0,0,self.board)
        # # memorize where are the goals
        # self.goalList = []
        # for row in range(len(board)):
        #     for col in range(len(board[0])):
        #         if self.board.board[row][col] == 2: self.goalList.append((row,col)) 
        # self.userCBlist = [] # wait for user's input
        # self.helperList = []
        # self.runTimeList =[]
        # self.maxRecursion = 5
        self.mode = "code"
        self.goButton = GoButton(600,600-150)

    def __eq__(self,other):
        if isinstance(other,Level):
            return self.level == other.level
        elif isinstance(other,int): return self.level==other
        else: return False

    def __repr__(self): return self.levelText

    def resetLevel(self): # reset bot pos, board, do not change user list
        self.board.resetBoard()
        self.win = False
        self.bot.resetBot()
        self.runTimeList=[]
        if self.level==6:self.bot2.resetBot()

    # ===== events inside level =====
    def levelMousePressed(self,data,x,y):
        # if click "back", always come back to menu
        if clickInButton(x,y,data.backButton):
            self.mode = "home"
            return
        if clickInButton(x,y,data.fastButton):
            data.animateSpeed = 5
            data.fastButton.highLight = True
            data.slowButton.highLight = False
            return
        if clickInButton(x,y,data.slowButton):
            data.animateSpeed = 15
            data.fastButton.highLight = False
            data.slowButton.highLight = True
            return

        if self.mode == "code":
            # click "run"
            if clickInButton(x,y,data.runButton):
                print("start running")
                self.resetLevel()
                # interpret list here 
                self.makeRunTimeList(self.userCBlist)
                print("runtimelist",self.runTimeList)
                data.isAnimating = True
                return

            # swich codeMode
            if clickInButton(x,y,data.switchToMain) and self.codeMode=="helper":
                self.codeMode = "main"
                return
            elif self.hasHelperFunction and clickInButton(x,y,data.switchToHelper)and self.codeMode =="main":
                self.codeMode = "helper"
                return
            # elif self.level==6 and clickInButton(x,y,data.addButton):
            #     self.hasBot2 = not self.hasBot2
                return
            else: 
                # add new buttons
                for cb in self.levelCBList: # cb: command button
                    x0,y0 = 800,50
                    if clickInButton(x,y,cb):
                        if self.codeMode == "main" and not self.addingRepeat:
                            self.userCBlist.append(cb.createNewButton(0,0))
                        elif self.codeMode == "helper" and not self.addingRepeat:
                            self.helperList.append(cb.createNewButton(0,0))
                        elif self.addingRepeat:
                            self.chosenButton.repeatList.append(cb.createNewButton(0,0))
                        return 

                # click buttons is coding area

                def ModifyRemoveOrMoveTimes(l):
                    for cb in l:
                        if clickInButton(x,y,cb) and isinstance(cb,MoveButton):
                            if self.chosenButton==None:
                                self.chosenButton = cb
                                self.chosenButton.changing = True
                                cb.highLight = True

                            else: # chosenbutton!= None
                                if clickInButton(x,y,cb):
                                    self.chosenButton.highLight = False
                                    self.chosenButton.changing = False
                                    cb.highLight = not cb.highLight
                                    cb.changing = not cb.changing
                                    self.chosenButton = cb
                                    return

                        elif isinstance(cb,RepeatButton):
                            if clickInButton(x,y,cb):
                                if self.chosenButton==None:
                                    self.chosenButton = cb
                                    cb.changing = True
                                    cb.highLight = True
                                    self.addingRepeat = cb.changing

                                else: # chosenbutton!= None
                                    self.chosenButton.highLight = False
                                    self.chosenButton.changing = False 
                                    cb.highLight = not cb.highLight
                                    cb.changing = not cb.changing
                                    self.addingRepeat = cb.changing
                                    self.chosenButton = cb
                            else:
                                ModifyRemoveOrMoveTimes(cb.repeatList)
                    return

                for cb in self.userCBlist: 
                    ModifyRemoveOrMoveTimes(self.userCBlist)
                for cb in self.helperList:
                    ModifyRemoveOrMoveTimes(self.helperList)


    def levelMouseDrag(self,data,x,y): # add features: auto placement!!!!!!!!!!!!!!!!
        if data.studyMode == self.levelText:
            if self.mode == "code":
                def update(l):
                    for button in l:
                        if clickInButton(x,y,button): 
                            button.x = x - button.w//2
                            button.y = y - button.h//2
                            return
                        if isinstance(button,RepeatButton):
                            update(button.repeatList)
                update(self.userCBlist)
                update(self.helperList)
        else: return None

    def levelKeyPressed(self,data,keyCode, modifier):
        if self.mode == "code":
            # "d" remove button
            if keyCode == 100:
                if isinstance(self.chosenButton,RepeatButton)and self.chosenButton.repeatList!=[]:
                    self.chosenButton.repeatList.pop()
                elif self.codeMode=="main" and self.userCBlist!=[]:
                    self.userCBlist.pop()
                elif self.codeMode=="helper" and self.helperList!=[]:
                    self.helperList.pop()

            if keyCode == 13: # hit enter
                if self.chosenButton!=None:
                    self.chosenButton.highLight = False
                    self.chosenButton.changing = False
                    self.addingRepeat = False

            # for now, "r" to reset
            if keyCode == 114: self.resetLevel()

            # change movestep/repeattime
            if keyCode == 273: # up
                def up(l): 
                    for button in l:
                        if isinstance(button,MoveButton) and button.changing==True:
                            button.moveStep+=1
                        elif isinstance(button,RepeatButton):
                            if button.changing == True: button.repeatTimes +=1
                            else: up(button.repeatList)
                up(self.userCBlist)
                up(self.helperList)

            elif keyCode == 274: # down
                def down(l): 
                    for button in l:
                        if isinstance(button,MoveButton) and button.changing==True:
                            button.moveStep-=1
                        elif isinstance(button,RepeatButton):
                            if button.changing == True: button.repeatTimes -=1
                            else: down(button.repeatList)
                down(self.userCBlist)
                down(self.helperList)

    def makeRunTimeList(self,l,depth=0):
        if depth>self.maxRecursion: return 
        for cb in l:
            if isinstance(cb,MoveButton):
                cb.makeMoveList()
                self.runTimeList += cb.moveList
            elif isinstance(cb,RepeatButton):
                for counter in range(cb.repeatTimes):
                    self.makeRunTimeList(cb.repeatList,depth+1)
            elif isinstance(cb,HelperFunctionButton):
                self.makeRunTimeList(self.helperList,depth+1)
            else:
                self.runTimeList.append(cb)

    def checkForWin(self):
        for goal in self.goalList:
            (x,y) = goal
            if self.board.board[x][y] == 2: return False
        return True

    def drawLevel(self,data,screen): # data is EasyCoding's self
        if self.mode == "home":
            pass
        elif self.mode == "code":
            # draw buttons
            data.backButton.drawButton(screen) 
            data.runButton.drawButton(screen)
            data.fastButton.drawButton(screen)
            data.slowButton.drawButton(screen)
            data.switchToMain.drawButton(screen)
            # data.addButton.drawButton(screen)
            data.switchToHelper.drawButton(screen)
            # draw borders
            pygame.draw.lines(screen,BLACK,False,[(data.width*0.4,0),(data.width*0.4,data.height)],3)
            pygame.draw.lines(screen,BLACK,False,[(data.width*0.6,0),(data.width*0.6,data.height)],3)
            createText(screen,50,20,"Creative Mode",45)
            createText(screen,data.width//2-80,20,"Commands")
            createText(screen,data.width//1.25-100,20,"Your Code")
            # draw board
            self.board.drawTiltedBoard(screen)
            self.bot.drawRobot(screen)
            # if self.hasBot2: 
            #     self.bot2.drawRobot(screen)
            # draw command buttons
            for button in self.levelCBList:
                button.drawButton(screen)
            # draw constraints... ...
            # draw user's buttons
            spacing,indent = 30,50
            def drawWithIndent(l,depth=0):
                nonlocal x0,y0
                for cb in l: 
                    cb.x,cb.y = x0+indent*depth,y0
                    y0+=cb.h+spacing # update y0
                    cb.drawButton(screen)
                    if isinstance(cb,RepeatButton):
                        drawWithIndent(cb.repeatList,depth+1)

            if self.codeMode == "main":
                x0,y0 = 0.6*1200+10,50 # keep updating
                drawWithIndent(self.userCBlist)
            else: # helper codeMode
                x0,y0 = 0.6*1200+10,50
                drawWithIndent(self.helperList)

            # show win message
            if self.win == True:
                createText(screen,150,50,"YOU WIN!")
