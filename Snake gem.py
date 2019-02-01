import time
import random
from tkinter import *

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
SIZE = 20
SPEED = SIZE
closePressed = False
master = Tk()
canvas = Canvas(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="black")
fruitBlock = 0
blocks = []
isGameOver = False
isGameOverScreen = False
xy = [1, 0]
score = 0
scoreTxt = 0
HighScore = 0
FPS = 0.1
cur_FPS = FPS

def closeClicked(event = None):
    global closePressed
    global canvas
    global master

    closePressed = True
    canvas = None
    master.destroy()
    master = None
def close():
    global closePressed
    global canvas
    global master

    closePressed = True
    canvas = None
    master.destroy()
    master = None
def closed():
    global master
    global closePressed
    try:
        master.update()
        return closePressed
    except:
        return True

def keyPressed(event):
    global xy, isGameOver
    key = event.keysym
    if key == 'Up' and xy[1] != 1:
        xy = [0, -1]
    if key == 'Down' and xy[1] != -1:
        xy = [0, 1]
    if key == 'Right' and xy[0] != -1:
        xy = [1, 0]
    if key == 'Left' and xy[0] != 1:
        xy = [-1, 0]
    if isGameOverScreen:
        Replay()

#   Class for every square:
class BlockTemp:
    # position of each square
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.block = canvas.create_rectangle(self.xPos, self.yPos, self.xPos + SIZE, self.yPos + SIZE)
    def fruitSpawn(self):
        canvas.itemconfig(self.block, fill="red")
        canvas.lower(self.block)
        return self.block
    def regularSpawn(self):
        canvas.itemconfig(self.block, fill="white")
        return self.block

def fruit():
    global fruitBlock
    xPos = random.randint(0, CANVAS_WIDTH / SIZE - 1) * SIZE
    yPos = random.randint(0, CANVAS_HEIGHT / SIZE - 1) * SIZE
    fruitBlock = BlockTemp(xPos, yPos).fruitSpawn()

def SnakeBegin():
    global blocks
    blocks = [BlockTemp(400-x*SIZE, 300).regularSpawn() for x in range(3)]

def fruitEat(headBlock):
    global score, fruitBlock, blocks, scoreTxt, cur_FPS
    if canvas.coords(headBlock) == canvas.coords(fruitBlock):
        score += 1
        lastBlock = canvas.coords(blocks[-1])
        canvas.delete(fruitBlock)
        fruit()
        blocks.append(BlockTemp(lastBlock[0], lastBlock[1]).regularSpawn())
        canvas.itemconfig(scoreTxt, text=score)
        if score % 10 == 0:
            cur_FPS *= 2/3

def borderCheck(headblock):
    global isGameOver
    headCoord = canvas.coords(headblock)
    xAVG = (headCoord[0]+headCoord[2])/2
    yAVG = (headCoord[1]+headCoord[3])/2
    if xAVG > CANVAS_WIDTH or xAVG < 0 or yAVG > CANVAS_HEIGHT or yAVG < 0:
        isGameOver = True

def Game():
    global isGameOver, scoreTxt
    scoreTxt = canvas.create_text(5, 10, text=score, anchor="w", fill="white", font="Arial")
    fruit()
    SnakeBegin()
    while not isGameOver:
        global xy
        headBlock = blocks[0]
        fruitEat(headBlock)
        for i in range(len(blocks)-1, 0, -1):
            if canvas.coords(blocks[i]) == canvas.coords(headBlock):
                isGameOver = True
            prevBlock = canvas.coords(blocks[i-1])
            canvas.coords(blocks[i], prevBlock)
        canvas.move(headBlock, xy[0]*SPEED, xy[1]*SPEED)
        borderCheck(headBlock)
        canvas.update()
        time.sleep(cur_FPS)
    if isGameOver:
        GameOver()

def Replay():
    global isGameOver, isGameOverScreen, xy, cur_FPS
    canvas.delete(ALL)
    cur_FPS = FPS
    isGameOver = False
    isGameOverScreen = False
    xy = [1, 0]
    Game()


def GameOver():
    global score, HighScore, isGameOverScreen
    canvas.delete(ALL)
    isGameOverScreen = True
    if score > HighScore:
        HighScore = score
    canvas.create_text(5, 10, text="Your score: %d" % score, anchor="w", fill="white", font="Arial")
    canvas.create_text(5, 30, text="High score: %d" % HighScore, anchor="w", fill="white", font="Arial")
    canvas.create_text(5, 50, text="Press any button to play again", anchor="w", fill="white", font="Arial")
    score = 0

def main():
    master.protocol("WM_DELETE_WINDOW", closeClicked)
    canvas.pack()
    master.bind("<Key>", keyPressed)
    master.bind("<Escape>", closeClicked)
    Game()
    mainloop()

main()
