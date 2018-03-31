import pygame

# ======= constants =======
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
DBI = "button-blue.png" # default button image
TURN_LEFT = [[0,-1],[1,0]] # inner list is a row
TURN_RIGHT =[[0,1],[-1,0]]
# ============ helper functions===========
import decimal
def roundHalfUp(d): # cite from 15-112 course notes
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def distance(x1,y1,x2,y2):
    return (abs(x1-x2)**2 + abs(y1-y2)**2)**0.5

# this helper function multiply matrix M(rxc) and N(cx1), return a 1d list(rx1)
# M is a 2d list, N is a 1d list or tuple
def matrixMult(M,N):
    result = []
    for row in range(len(M)):
        rowSum = 0
        for col in range(len(M[0])):
            rowSum += M[row][col] * N[col] # inner product
        result.append(rowSum)
    return result

def testMatrixMult():
    print("texting matrixMult...",end="")
    assert(matrixMult(TURN_LEFT,(0,1))==[-1,0])
    assert(matrixMult(TURN_LEFT,(1,0))==[0,1])
    assert(matrixMult(TURN_RIGHT,(0,1))==[1,0])
    assert(matrixMult(TURN_RIGHT,(1,0))==[0,-1])
    print("passed!")

# create text in pygame takes in surface, text, topleft corner, color, font
def createText(screen,x,y,text,size=40,color=BLACK,font=None):
    # create a Font object from the system fonts
    Font = pygame.font.SysFont(None,size) # name, size, bold=False, italic=False
    label = Font.render(text,1,color) # create a new surface
    screen.blit(label,(x,y)) # combine the surfaces

def loadImage(screen,fileName,x,y,desireWid=None,desireHt=None,scale=None):
    image = pygame.image.load(fileName)
    image = image.convert_alpha()
    (image_x,image_y) = image.get_size()
    if scale != None:
        desireWid,desireHt = int(image_x*scale),int(image_y*scale)
    if desireWid!=None and desireHt!=None:
        image = pygame.transform.scale(image,(desireWid,desireHt))
    screen.blit(image,(x,y))

def make2dBoard(dim=5,default=0):
    return [[default]*dim for i in range(dim)]

def clickInButton(mouse_x,mouse_y,button):
    return ((button.x<=mouse_x<=button.x+button.w) 
                and (button.y<=mouse_y<=button.y+button.h))