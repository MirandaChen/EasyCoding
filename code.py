# Term Project
# Miranda Chen; andrew id: yinglanc
# animation framework cite from pygamegame.py
# created by Lukas Peraza for 15-112 F15 Pygame Optional Lecture, 11/11/15
import math,random,copy,pygame
from helperFunctions import roundHalfUp,distance,matrixMult,testMatrixMult,createText,loadImage,make2dBoard,clickInButton
from Buttons import Button,AddButton,SwitchToHelper,SwitchToMain,BackButton,RunButton,LevelButton,MoveButton,FastButton,SlowButton
from Buttons import TurnLeftButton,TurnRightButton,IfElseButton,JumpButton,RepeatButton,HelperFunctionButton,GoButton,NextButton
from Robot import Robot
from Board import Board
from Level import Level
from Creative import Creative
# ======= constants =======
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
DBI = "button-blue.png" # default button image
TURN_LEFT = [[0,-1],[1,0]] # inner list is a row
TURN_RIGHT =[[0,1],[-1,0]]

# ================ main game =================== 

class EasyCoding(object):

    # ====== game-specific initialization ======
    def init(self):
        # modes set up
        self.mode = "splashScreen" # main mode: splashScreen,study,creative,help
        self.studyMode = None # inside study mode, there are level1-6

        self.backButton = BackButton(self.width-200,self.height-90)
        self.runButton = RunButton(200,self.height-70)
        self.fastButton = FastButton(100,self.height-55)
        self.slowButton = SlowButton(300,self.height-55)
        self.switchToMain = SwitchToMain(self.width-42,50)
        self.switchToHelper = SwitchToHelper(self.width-42,250)
        self.addButton = AddButton(self.width-42,250)
        self.splashScreenInit()
        self.createLevelButtons()
        self.levelInit()
        self.creativeInit()

        self.isAnimating = False
        self.animateSpeed = 15
        self.timeCounter = 0
        self.lineCounter = 0
        self.currLevel = None

    def splashScreenInit(self):# splashScreen buttons
        buttonWid, buttonHt = 250,50
        pos1 = ((self.width-buttonWid)//2,200,buttonWid, buttonHt) # x,y,wid,h
        self.studyButton = Button(*pos1,"Study Mode",40)
        pos2 = ((self.width-buttonWid)//2,280,buttonWid, buttonHt) # x,y,wid,h
        self.creativeButton = Button(*pos2,"Creative Mode",40)
        pos3 = ((self.width-buttonWid)//2,360,buttonWid, buttonHt) # x,y,wid,h
        self.helpButton = Button(*pos3,"Help",40)
        self.splashButtons={self.studyButton:"study",
                            self.creativeButton:"creative",
                            self.helpButton:"help"}

    def createLevelButtons(self):
        # create buttons representing levels
        self.levelButtons = {self.backButton:"splashScreen"}
        spacing = 150
        for i in range(1,4):
            pos = (300+spacing*(i),200,50,50)
            self.levelButtons[LevelButton(*pos,"%d"%i)] ="level%d" %i
        for i in range(4,7):
            pos = (300+spacing*(i-3),300,50,50)
            self.levelButtons[LevelButton(*pos,"%d"%i)]="level%d" %i

    def levelInit(self):
        x0,y0 = self.width*0.4+10,100
        # initialize levels
        levelObj1 = "Learning Objectives: Basic and Variables"
        tip1 = """Tips: Click on Move button\nuse up and down arrow to change the number of steps.
                  \nHit enter once you finish changing"""
        self.board1 = [[0,0,0,0,0],
                  [0,0,0,0,2],
                  [1,1,1,1,1],
                  [0,0,0,0,0],
                  [0,0,0,0,0]]
        level1CBList = [MoveButton(x0,y0),
                        TurnLeftButton(x0,y0+100),TurnRightButton(x0,y0+200)]
        self.level1 = Level(1,levelObj1,tip1,self.board1,level1CBList,2,0,constraints=3) # basic and variables

        levelObj2 = "Learning Objectives: Loops"
        tip2 = """Tips: Click on repeat button\nuse up and down arrow to change the number of repeat times.
                  \nHit 'enter' once you finish changing
                  \nYou can only modify one button at a time"""
        self.board2 = [[1,1,1,2,1],
                  [2,0,0,0,1],
                  [0,0,0,0,1],
                  [0,0,0,0,2],
                  [0,1,1,1,1]]
        level2CBList = [MoveButton(x0,y0),TurnLeftButton(x0,y0+100),
                        TurnRightButton(x0,y0+200),RepeatButton(x0,y0+300)]
        self.level2 = Level(2,levelObj2,tip2,self.board2,level2CBList,4,1,constraints=4)

        levelObj3 = "Learning Objectives:If-else Conditions  "
        tip3 = ""
        self.board3 = [[0,0,0,0,0],
                  [0,0,0,0,0],
                  [1,1,1,1,2],
                  [0,0,0,0,0],
                  [0,0,0,0,0]]
        # randomly generate a hole
        hole = random.randint(1,3)
        self.board3[2][hole] = 0
        level3CBList = [MoveButton(x0,y0),TurnLeftButton(x0,y0+80),
                        TurnRightButton(x0,y0+160),RepeatButton(x0,y0+240),
                        JumpButton(x0,y0+320),IfElseButton(x0,y0+400)]
        self.level3 = Level(3,levelObj3,tip3,self.board3,level3CBList,2,0,constraints=2)

        levelObj4 = "Learning Objectives: Helper Function"
        tip4 = """Tips: If you call Helper Function, BB8 will execute commands inside the Helper Function
                  Click on side buttons to switch between main and helperfunction!"""
        self.board4 = [[1,0,0,0,0],
                  [2,1,0,0,0],
                  [0,2,1,0,0],
                  [0,0,2,1,0],
                  [0,0,0,2,1]]
        level4CBList = [MoveButton(x0,y0),TurnLeftButton(x0,y0+100),
                        TurnRightButton(x0,y0+200),HelperFunctionButton(x0,y0+300),RepeatButton(x0,y0+400)]
        self.level4 = Level(4,levelObj4,tip4,self.board4,level4CBList,0,0,True,constraints=2)

        levelObj5 = "Learning Objectives: Recursion"
        tip5 = """Tips: You know what? You can call helper function itself inside the helper function!"""

        self.board5 = [[1,0,0,0,0],
                  [2,1,0,0,0],
                  [0,2,1,0,0],
                  [0,0,2,1,0],
                  [0,0,0,2,1]]
        level5CBList = [MoveButton(x0,y0),TurnLeftButton(x0,y0+100),
                        TurnRightButton(x0,y0+200),HelperFunctionButton(x0,y0+300)]
        self.level5 = Level(5,levelObj5,tip5,self.board5,level5CBList,0,0,True,constraints=1)

        levelObj6 = "Learning Objectives: Object"
        tip6 = """Tips: click Add to call BB8’s friends to help him!"""
        self.board6 = [[1,1,1,1,2],
                  [0,0,0,0,0],
                  [1,1,1,1,2],
                  [0,0,0,0,0],
                  [0,0,0,0,0]]
        level6CBList = [MoveButton(x0,y0)]
        self.level6 = Level(6,levelObj6,tip6,self.board6,level6CBList,2,0,constraints=1)

        self.levelList = [self.level1,self.level2,self.level3,self.level4,self.level5,self.level6]

    def creativeInit(self):
        x0,y0 = self.width*0.4+10,100
        board = make2dBoard(10,1)
        creativeCBList = [MoveButton(x0,y0),TurnLeftButton(x0,y0+60),
                          TurnRightButton(x0,y0+120),JumpButton(x0,y0+180),
                          RepeatButton(x0,y0+240),IfElseButton(x0,y0+300),HelperFunctionButton(x0,y0+360)]
        self.creative = Creative(0,"","",board,creativeCBList,5,5)
        self.creative.mode = "home"

    # ====== events ======
    def findCurrLevel(self):
        i = int(self.studyMode[-1])
        for level in self.levelList: 
            if level == i: return level
        return None

    def mousePressed(self, x, y):
        if self.mode == "splashScreen":
            # if click in button, for debugging, hardcode the value
            for button in self.splashButtons:
                if clickInButton(x,y,button):
                    self.mode = self.splashButtons[button]

        elif self.mode == "help":
            if clickInButton(x,y,self.backButton):
                self.mode = "splashScreen"

        elif self.mode == "creative":
            if self.creative.mode == "home":
                if clickInButton(x,y,self.backButton):
                    self.mode = "splashScreen"
                    return
                elif clickInButton(x,y,self.creative.goButton):
                    print("hit go button")
                    self.creative.mode = "code"

            elif self.creative.mode == "code":
                self.creative.levelMousePressed(self,x,y)

        elif self.mode == "study":
            if self.studyMode == None:
                # back to last level
                if clickInButton(x,y,self.backButton):
                    self.mode = self.levelButtons[self.backButton]
                    return
                # go to next level
                for button in self.levelButtons:
                    if clickInButton(x,y,button):
                        self.studyMode = self.levelButtons[button]
            else: 
                level = self.findCurrLevel()
                level.levelMousePressed(self,x,y)

    def mouseDrag(self, x, y):
        if self.mode =="study" and self.studyMode != None:
            level = self.findCurrLevel()
            level.levelMouseDrag(self,x,y)

    def keyPressed(self, keyCode, modifier):
        if self.mode == "study" and self.studyMode != None:
            level = self.findCurrLevel()
            level.levelKeyPressed(self,keyCode, modifier) # self is data
        if self.mode == "creative":
            self.creative.levelKeyPressed(self,keyCode, modifier)

    def timerFired(self, dt):
        if self.mode =="study":
            self.studyModeTimerFired(dt)
        elif self.mode == "creative":
            self.creativeModeTimerFired(dt)

    def studyModeTimerFired(self,dt):
        if self.studyMode!=None:
            level = self.findCurrLevel()

        if self.isAnimating==True:
            def animateButton(bot,cb):
                print("animate",cb,"button")
                if isinstance(cb,MoveButton): 
                    bot.moveForward(1,level) # step,data
                elif isinstance(cb,TurnLeftButton):
                    bot.turnLeft()
                elif isinstance(cb,TurnRightButton):
                    bot.turnRight()
                elif isinstance(cb,JumpButton):
                    bot.moveForward(2,level)
                elif isinstance(cb,IfElseButton):
                    if bot.isLegalMove(level.board,bot.dir[0],bot.dir[1]):bot.moveForward(1,level)
                    else: bot.moveForward(2,level)

            self.timeCounter +=1 
            if level.userCBlist!=[]: currButton = level.runTimeList[self.lineCounter] # find which button is animating

            if self.timeCounter % self.animateSpeed == 0: # execute every xx calls
                print("speed",self.animateSpeed)
                animateButton(level.bot,currButton)
                if level.level==6 and level.hasBot2: animateButton(level.bot2,currButton)
                self.lineCounter+=1

            # win
            if level.checkForWin(): 
                level.win = True

            # end of animation
            if self.lineCounter >= len(level.runTimeList):
                self.isAnimating = False
                self.lineCounter = 0
                self.timeCounter = 0
                print("end animation")

    def creativeModeTimerFired(self,dt):
        if self.creative.mode == "code" and self.isAnimating==True:
            def animateButton(bot,cb):
                print("animate",cb,"button")
                if isinstance(cb,MoveButton): 
                    bot.moveForward(1,self.creative) # step,data
                elif isinstance(cb,TurnLeftButton):
                    bot.turnLeft()
                elif isinstance(cb,TurnRightButton):
                    bot.turnRight()
                elif isinstance(cb,JumpButton):
                    bot.moveForward(2,self.creative)
                elif isinstance(cb,IfElseButton):pass
            self.timeCounter +=1 
            if self.creative.userCBlist !=[]:
                currButton = self.creative.runTimeList[self.lineCounter] # find which button is animating

            if self.timeCounter% self.animateSpeed == 0: # execute every 5 calls
                animateButton(self.creative.bot,currButton)
                self.lineCounter+=1

            # end of animation
            if self.lineCounter >= len(self.creative.runTimeList):
                self.isAnimating = False
                self.lineCounter = 0
                self.timeCounter = 0
                print("end animation")


    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    # ====== redrawAll ======
    def redrawAll(self, screen):
        if self.mode == "splashScreen":
            EasyCoding.drawSplashScreen(self,screen)
        elif self.mode == "help":
            EasyCoding.drawHelpMode(self,screen)
        elif self.mode == "creative":
            EasyCoding.drawCreativeMode(self,screen)
        elif self.mode == "study":
            EasyCoding.drawStudyMode(self,screen)

    def drawSplashScreen(self,screen):
        loadImage(screen,"Bluebot.png",-10,200)
        loadImage(screen,"pinkBot.png",900,100,scale=1.3)
        # draw title
        # createText(screen,self.width//2-100,50,"EasyCoding",40)
        loadImage(screen,"title.png",self.width//2-180,50)
        # draw buttons
        for button in self.splashButtons:
            button.drawButton(screen)

    def drawHelpMode(self,screen):
        loadImage(screen,"confusedRobot.png",50,300,scale=0.5)

        createText(screen,self.width//2-100,20,"Instructions",40)
        loadImage(screen,"instructions.png",200,75,scale=0.9)
        self.backButton.drawButton(screen)

    def drawCreativeMode(self,screen):
        if self.creative.mode == "home":
            text1 = "Inside Creative Mode, you have big enough grid and no constraints!" 
            text2 = "Try as many as commands as you want and see how they work out!"
            createText(screen,self.width//2-200,50,"Welcome to Creative Mode!",40)
            createText(screen,self.width//2-500,150,text1,40)
            createText(screen,self.width//2-500,220,text2,40)
            loadImage(screen,"freeBot.png",50,300)
            

            self.backButton.drawButton(screen) 
            self.creative.goButton.drawButton(screen)
        elif self.creative.mode == "code":
            self.creative.drawLevel(self,screen) # data,screen
    
    def drawStudyMode(self,screen):
        if self.studyMode == None: # menu
            # draw title
            loadImage(screen,"studymode.png",self.width//2-200,50)
            loadImage(screen,"baymax_waving.png",-10,300)
            # draw level buttons
            for button in self.levelButtons:
                button.drawButton(screen)
        else:
            level = self.findCurrLevel()
            level.drawLevel(self,screen) # self is data

    def __init__(self, width=1200, height=600, fps=50, title="Easy Coding by Miranda"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255,230,100)
        pygame.init()

    # ====== run ============
    def run(self):
        
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))

                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()

def main():
    testMatrixMult()
    game = EasyCoding()
    game.run()

if __name__ == '__main__':
    main()