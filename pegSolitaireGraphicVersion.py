from tkinter import *

class memory:
    def __init__(self):
        self.currentPositions=[]

    def getCurrentPositions(self):
        return self.currentPositions
    def add(self,position):
        self.currentPositions.append(position)
    def reset(self):
        self.currentPositions=[]

class position:
    def __init__(self,memory,position,root):
        self.position=position
        self.status='Empty'
        self.c=Canvas(width=50,height=50)
        self.c.create_oval(2,2,48,48)
        self.c.bind('<Button-1>',lambda event:memory.add(self.position))
        self.c.grid(row=position[0]+2,column=position[1]+2)
    
    def placePeg(self):
        self.c.create_oval(2,2,48,48,fill='black')
        self.status='Peg'

    def removePeg(self):
        self.c.create_oval(2,2,48,48,fill='white')
        self.status='Empty'
        
    def getStatus(self):
        return self.status
    
    def getPosition(self):
        return self.position

class label:
    def __init__(self,message,position):
        self.label=Label(text=message)
        self.label.grid(row=position[0],column=position[1])
    def changeLabel(self,s):
        self.label['text']=s

class PegSolitaire:
    def __init__(self,X,Y):
        self.m=memory()
        self.positions=[]
        root=Tk()
        self.l=label('Welcome to the Peg Solitaire',(0,0))
        self.l2=label('place pegs by selecting pegs',(1,0))
        for row in range(X):
            self.positions.append([])
            for column in range(Y):
                p=position(self.m,(row,column),root)
                self.positions[row].append(p)
        resetButton=Button(text='Reset Selected Positions')
        resetButton.bind('<Button-1>',lambda event:self.m.reset())
        resetButton.grid(row=X+2,column=0)
        jumpButton=Button(text='Jump currently Selected Positions')
        jumpButton.bind('<Button-1>',lambda event:self.jumpPeg())
        jumpButton.grid(row=X+2,column=Y+2)
        pegButton=Button(text='Place Peg on selected positions')
        pegButton.grid(row=X+3,column=0)
        pegButton.bind('<Button-1>',lambda event:self.pegs())
        root.mainloop()


        
    
    def pegs(self):
        l=self.m.getCurrentPositions()
        for i in l:
            self.placePeg(i)
        self.l2.changeLabel('Select Pegs To jump')
    def placePeg(self,position):
        self.positions[position[0]][position[1]].placePeg()

    def removePeg(self,position):
        self.positions[position[0]][position[1]].removePeg()
    def canJump(self,p1,p2):
        
        if p1==p2:
            return False

        if self.positions[p1[0]][p1[1]].getStatus()!='Peg': #there's no peg at 1st location
            return False

        if self.positions[p2[0]][p2[1]].getStatus()!='Empty': #there's a peg at 2nd position
            return False

        if p1[0]-p2[0] != 0 and p1[1]-p2[1] != 0: #positions are diagonal
            return False

        if p1[0]-p2[0]==1 or p1[0]-p2[0]==-1 or p1[1]-p2[1]==1 or p1[1]-p2[1]==-1:
            #positions are right next to each other
            return False

        if -2 > p1[0]-p2[0] > 2 or -2 > p1[1]-p2[1] > 2:
            #positions have more than 1 position in between them
            return False
            
        if p1[0]==p2[0]:        #moving horizontal
            
            if p1[1]>p2[1]:     #p1 is greater than p2
    
                if self.positions[p1[0]][p1[1]-1].getStatus()=='Empty':   #there is no peg between the two positions
                    return False
            else:           #p2 is greater than p1
                if self.positions[p1[0]][p2[1]-1].getStatus()=='Empty':   #there is no peg between the two positions
                    return False

        if p1[1]==p2[1]:        #moving vertical
            
            if p1[0]>p2[0]:     #p1 is greater than p2
                if self.positions[p1[0]-1][p1[1]].getStatus()=='Empty':   #there is no peg between the two positions
                    return False
            else:           #p2 is greater than p1
                if self.positions[p2[0]-1][p2[1]].getStatus()=='Empty':   #there is no peg between the two positions
                    return False
        
        return True
    def jumpPeg(self):
        l=self.m.getCurrentPositions()
        if len(l)>2:
            self.l2.changeLabel('You selected more than 2 positions to Jump')
        else:
            p1=l[0]
            p2=l[1]
            if self.canJump(p1,p2):
                self.placePeg(p2)
                self.removePeg(p1)
                if p1[0]==p2[0]:        #moving vertical
                    if p1[1]>p2[1]:     #p1 is greater than p2
                        self.removePeg((p1[0],p1[1]-1))
                    
                    else:           #p2 is greater than p1
                        self.removePeg((p1[0],p2[1]-1))

                if p1[1]==p2[1]:        #moving horizontal
            
                    if p1[0]>p2[0]:     #p1 is greater than p2
                        self.removePeg((p1[0]-1,p1[1]))
                    
                    else:           #p2 is greater than p1
                        self.removePeg((p2[0]-1,p1[1]))
                self.l2.changeLabel('Nice Move. Jump Again')
            else:
                self.l2.changeLabel('Cannot jump')
        if self.isStuck():
            self.l2.changeLabel('Nice Game. No more Moves')
    def isStuck(self):
        for row in range(len(self.positions)):
            for column in range(len(self.positions[row])):
                p1=(row,column)
                for row2 in range(len(self.positions)):
                    for column2 in range(len(self.positions[row2])):
                        p2=(row2,column2)
                        if self.canJump(p1,p2):
                            return False
        return True



def main():
    rows=int(input("Number of rows: "))
    columns=int(input("Number of columns: "))
    p=PegSolitaire(rows,columns)
main() 
    
