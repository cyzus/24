from tkinter import *
import random
import time


class TwentyFour(object):
    def __init__(self,numbers):
        self.numbers=numbers
    
    def initOrd(self,array,length):
        list=[] #all possible array list
        if length==4:
            for i in array:
                for j in array:
                    for k in array:
                        for l in array:
                            list.append([str(i),str(j),str(k),str(l)])
        if length==3:
            for i in array:
                for j in array:
                    for k in array:
                        list.append([str(i),str(j),str(k)])
        return list
    
    def screen(self,array): #screen out invalid order
        list=[]
        temp=sorted(self.numbers)
        
        for ord in array:
            if sorted(ord)==temp:
                list.append(ord)
                
        return list

def almostEqual(a,b): 
    if abs(a-b)<10**-8:
        return True
    else:
        return False



def check(exp):
    try:
        return almostEqual(eval(exp),24) #check eval(expression) is 24  
        #return eval(exp)== 24
       
    except:
        return False
    


#coolest part down here
def solve24(numbers):
    result=[]
    question=TwentyFour(numbers)
    measures=["+","-","*","/"]
    exps = ('((%s %s %s) %s %s) %s %s',
    
            '(%s %s %s) %s (%s %s %s)', 
    
            '(%s %s (%s %s %s)) %s %s',
    
    
            '%s %s ((%s %s %s) %s %s)',
    
            '%s %s (%s %s (%s %s %s))')
    allOrds=question.screen(question.initOrd(numbers,4))
    allMeasures=question.initOrd(measures,3)
    t=[exp %(num[0],mea[0],num[1],mea[1],num[2],mea[2],num[3]) 
        for num in allOrds for mea in allMeasures for exp in exps 
        if check(exp %(num[0],mea[0],num[1],mea[1],num[2],mea[2],num[3]))]
    if t:
        result.extend(t)
    return list(set(result))
    
    


def randomCard(): #random generate four cards from a shuffle deck
    solution=False
    while not solution:
        deck=[]
        for i in range(4):
            for j in range(1,14):
                if i == 0:
                    color="spade"
                elif i ==1:
                    color="club"
                elif i==2:
                    color="heart"
                else:
                    color="diamond"
                deck.append((str(j),color))
        random.shuffle(deck)
        cards=[deck[0],deck[1],deck[2],deck[3]]
        solution = solve24([num for (num,color) in cards])
    return cards



# Initialize the data which will be used to draw on the screen.
def init(data):
    initOptions(data)
    print("created by:\n Selina & Cyzus & Frances ")
    #initCalculate(data)

def switch(data,nextMode): #switch mode
    data.mode="switch"
    data.nextMode=nextMode
    data.dots=[]
    data.predots=[]

    for i in range(500):
        for j in range(500):
            data.predots.append((i,j))


def initOptions(data):
    data.mode="options"
    data.logox=data.width/2
    data.logoy=data.height/2
    data.optionsPicker=0
    margin=60
    length=80
    spacing=10
    horizMargin=100
    data.model1left=data.logox-length-spacing
    data.model1top=data.logoy+margin
    data.model2left=data.logox+spacing
    data.model2top=data.logoy+margin

def initCalculate(data):
    data.mode="calculate"
    horizMargin=50
    vertMargin=20
    data.squares=[]
    data.squareSize=80
    
    data.userInput=[]
    data.next=True
    for i in range(4):
        spacing=(data.width-horizMargin*2-data.squareSize*4)/3
        left=horizMargin+(data.squareSize+spacing)*i
        up=vertMargin+(data.height-vertMargin*2)/2
        data.squares.append((left,up))

    
    
    
def initArcade(data):
    data.mode="arcade"
    cx=data.width/2
    cy=data.height/2
    data.cards=[]
    data.cardsGenerated=randomCard()
    for i in range(2):
        for j in range(2):
            horiz=80
            vert=90
            if i>0:
                horiz=-horiz
            if j>0:
                vert=-vert
                
            data.cards.append((cx+horiz,cy+vert))

   
    

def initAnswer(data,array): 
    
    data.mode="answer"
    horizMargin=1/5*data.width
    data.answerBoxLeft=horizMargin
    data.answerBoxTop=1/2*data.height
    data.load  =True
    data.loadBar=data.answerBoxLeft
    
    try:
        data.answer=solve24(array)[0]
        
    except:
        data.answer="No Solution"



# These are the CONTROLLERs.
def mousePressed(event, data):
    pass
def keyPressed_Calculate(event,data):
    
    try:
        
        if 0<=int(event.keysym)<=9:
            if data.next==True and int(event.keysym)!=0:
                data.userInput.append(event.keysym)
                data.next=False
            elif len(data.userInput)>0 and int(data.userInput[-1])//10<=0:
                data.userInput[-1]+=event.keysym
            
            
    except:
        pass
    if event.keysym=="Return":
        if len(data.userInput)>0 and 1<=int(data.userInput[-1])<=13:
            data.next=True
            if len(data.userInput)==4:
                data.nextMode="calculate"
                initAnswer(data,data.userInput)
        else:
            print("invalid input")
    elif event.keysym=="BackSpace" and len(data.userInput)>0:
        if int(data.userInput[-1])//10>0:
            data.userInput[-1]=str(int(data.userInput[-1])//10)
        else:
            data.userInput.pop()
            data.next=True
    elif event.keysym=="Escape":
        initOptions(data)

def keyPressed_Arcade(event,data):
    if event.keysym=="Escape":
        initOptions(data)
    elif event.keysym=="Return":
        data.flip+=1
        if data.flip>13:
            print("You take %d seconds to finish a deck. Cool!" %data.time)
            initOptions(data)
            return
        initArcade(data)
        
    elif event.keysym=="h":
        data.nextMode="arcade"
        initAnswer(data,[num for (num,color) in data.cardsGenerated])

def keyPressed_Options(event,data):
    if event.keysym=="Left":
        data.optionsPicker=0
    elif event.keysym=="Right":
        data.optionsPicker=1
    elif event.keysym=="Return":
        if data.optionsPicker==0:
            switch(data,"calculate")
            #initCalculate(data)
        elif data.optionsPicker==1:
            switch(data,"arcade")
            #initArcade(data)
def keyPressed(event, data):
    # use event.char and event.keysym (chase key)
    if data.mode=="options":
        keyPressed_Options(event,data)
    elif data.mode=="calculate":
        keyPressed_Calculate(event,data)
    elif data.mode=="answer":
        if event.keysym=="Escape":
            if data.nextMode=="calculate":
                initCalculate(data)
            elif data.nextMode=="arcade":
                initArcade(data)
    elif data.mode=="arcade":
        keyPressed_Arcade(event,data)
 
def loadAnswer(data):   
    maxload=data.answerBoxLeft+data.width-data.answerBoxLeft*2
    if data.load:
        if data.loadBar<maxload:
            data.loadBar+=random.randrange(0,15)
            if data.loadBar>maxload:
                data.loadBar=maxload
        else:
            data.load=False


    
            
def addDots(data): #add dots in loading splash
    maxNum=3000
    for i in range(random.randrange(50,200)):
        if len(data.dots)>=maxNum:
            break
        i=random.randrange(0,len(data.predots))
        (x,y)=data.predots.pop(i)
        data.dots.append((x,y))

    if len(data.dots)>=maxNum:
        if data.nextMode=="arcade":
            data.iniTime=round(time.time(),2)
            data.time=0
            data.flip=1
            initArcade(data)
        elif data.nextMode=="calculate":
            initCalculate(data)

def timerFired(data):
    if data.mode=="answer":
        if data.load:
            loadAnswer(data)
    elif data.mode=="switch":
        addDots(data)
    elif data.mode=="arcade":
        data.time=round(time.time()-data.iniTime,1)
    


# This is the VIEW
# IMPORTANT: VIEW does *not* modify data at all!
# It only draws on the canvas.
def drawBoard(canvas,data):
    canvas.create_rectangle(0,0,data.width,data.height,width=0,fill="white")


def drawSplash(canvas,data):
    cx=data.width//2
    cy=data.height//2
    text1="Awesome!"

def drawDots(canvas,data):
    for i in range(len(data.dots)):
        (x,y)=data.dots[i]
        size=30
        canvas.create_oval(x-0.5*size,y-0.5*size,x+0.5*size,y+0.5*size,
            width=0,fill="black")
    canvas.create_text(data.width/2,data.height/2,fill="white",
        text="Loading...",font="Times 80")

def drawCalculate(canvas,data):
    title="4 numbers(1~13), plz..."
    margin=40
    canvas.create_text(data.width/2,data.height/2-margin,
        text=title)
    canvas.create_text(data.width-margin,data.height-margin,anchor="e",
        text="[Esc]Back / [Enter]Confirm")
    for i in range(4):
        (left,up)=data.squares[i]
        size=data.squareSize
        
        canvas.create_rectangle(left,up,left+size,up+size)
        if len(data.userInput)-1>=i:
            
            num=data.userInput[i]
            cx=(left+left+size)/2
            cy=(up+up+size)/2
            canvas.create_text(cx,cy,text=num,font="Helvetica")
            
def drawAnswer(canvas,data):
    left=data.answerBoxLeft
    up=data.answerBoxTop
    width=data.width-left*2
    height=30
    margin=40
    canvas.create_rectangle(left,up,left+width,up+height)
    if data.load:
        canvas.create_rectangle(left,up,data.loadBar,up+height,fill="grey")
        canvas.create_text(data.width/2,data.height/2-margin,
            text="Loading...")
    else:
        canvas.create_text(left+width/2,up+height/2,text=data.answer)
        canvas.create_text(data.width-margin,data.height-margin,anchor="e",
            text="[Esc]Back")

def drawArcade(canvas,data):
    margin=50
    cardMargin=5
    canvas.create_text(data.width/2,margin,anchor="s",
        text="Can you get a 24?")
    canvas.create_text(data.width/2,margin,anchor="n",
        text=data.time)
    canvas.create_text(data.width-margin,data.height-margin,anchor="e",
        text="[H]Help / [Esc]Back / [Enter]Next")

    for i in range(4):
        cardHeight=160
        cardWidth=120
        (sx,sy)=data.cards[i]
        canvas.create_rectangle(sx-cardWidth/2,sy-cardHeight/2,
            sx+cardWidth/2,sy+cardHeight/2)
        (card,color)=data.cardsGenerated[i]
        if card=="1":
            card="A"
        elif card=="11":
            card="J"
        elif card=="12":
            card="Q"
        elif card=="13":
            card="K"
        
        canvas.create_text(sx-cardWidth/2+cardMargin,sy-cardHeight/2+cardMargin,
            text=card,anchor="nw")
        drawColor(canvas,color,(sx,sy))

    
def drawOptions(canvas,data):
    mode1Text="black"
    mode1Bar="white"
    mode2Text="black"
    mode2Bar="white"
    if data.optionsPicker==0:
        mode1Text="white"
        mode1Bar="black"
    elif data.optionsPicker==1:
        mode2Text="white"
        mode2Bar="black"
    
    mode1="Calculate"
    mode2="Arcade"
    textMargin=35
    
    canvas.create_text(data.logox,data.logoy,text="24",font="Times 100")
    
    length=80
    width=40
    
    canvas.create_rectangle(data.model1left,data.model1top,
        data.model1left+length,data.model1top+width,fill=mode1Bar)
    canvas.create_rectangle(data.model2left,data.model2top,
        data.model2left+length,data.model2top+width,fill=mode2Bar)
    canvas.create_text(data.model1left+length/2,data.model1top+width/2,
        text=mode1,font="Helvetica 12",fill=mode1Text)
    canvas.create_text(data.model2left+length/2,data.model2top+width/2,
        text=mode2,font="Helvetica 12",fill=mode2Text)
    

def drawColor(canvas,color,position):
    (x,y)=position
    if color == "diamond":
        width=10
        height=3**0.5*width
        canvas.create_polygon(x-width,y,x,y-height,x+width,y,x,y+height,
            fill="red")
    elif color == "heart":
        width=10
        r=width//2
        canvas.create_polygon(x-2*r,y,x+2*r,y,x,3**0.5*width+y,fill="red")
        canvas.create_oval(x-2*r,y-r,x,y+r,fill="red",width=0)
        canvas.create_oval(x,y-r,x+2*r,y+r,fill="red",width=0)
    elif color == "spade":
        width=10
        r=width//2
        canvas.create_polygon(x+2*r,y,x-2*r,y,x,-3**0.5*width+y,fill="black")
        canvas.create_oval(x-2*r,y-r,x,y+r,fill="black",width=0)
        canvas.create_oval(x,y-r,x+2*r,y+r,fill="black",width=0)
        canvas.create_polygon(x,y,x-r,y+2*r,x+r,y+2*r,fill="black")
    elif color == "club":
        width=10
        r=width//2
        
        canvas.create_oval(x-r,y-r*2.6,x+r,y-r*0.6,fill="black")
        canvas.create_oval(x-2*r,y-r,x,y+r,fill="black",width=0)
        canvas.create_oval(x,y-r,x+2*r,y+r,fill="black",width=0)
        canvas.create_polygon(x,y-0.6*r,x-r,y+2*r,x+r,y+2*r,fill="black")
    
def redrawAll(canvas, data):
    # draw in canvas
    drawBoard(canvas,data)
    if data.mode=="options":
        drawOptions(canvas,data)
    if data.mode=="calculate":
        drawCalculate(canvas,data)
    elif data.mode=="answer":
        drawAnswer(canvas,data)
    elif data.mode=="arcade":
        drawArcade(canvas,data)
    elif data.mode=="switch":
        drawDots(canvas,data)




def run():
    width=500
    height=500
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    root.title("24")
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("Byeee!")

run()