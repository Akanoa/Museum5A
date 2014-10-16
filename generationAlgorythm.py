import math
import random



# Orientation enum
class Orientation:
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3
 
# Cell data structure
class Cell:
    def __init__(self):
        self.visited = False
        self.walls = [None, None, None, None]

    def display(self):
        print "visited" +"\n"
        print self.walls
        for x in range(len(self.walls)):
            if self.walls[x] != None:
                self.walls[x].display()

 
# Wall data structure
class Wall:
    def __init__(self):
        self.firstCell = None
        self.lastCell = None
        self.broken = False
        self.typeDoor = None

    def display(self):
        print "First Cell" +"\n"
        if self.lastCell: 
            print "lastCell"  +"\n"
        if self.broken == True:  
            print "broken!"  +"\n"

class GenerationAlgorythm:
    def __init__(self, width, height):
        # Base params (size)
        self.mazeWidth = width
        self.mazeHeight = height
         
        # Startpoint (left)
        self.startPointX = int(0)
        self.startPointY = int(math.floor(self.mazeHeight/2)) 

        self.mazeGenerated = None

    def generate(self):
        # Create maze structure
        maze = [[Cell() for i in range(self.mazeHeight)] for j in range(self.mazeWidth)]

        maze = list(list(Cell() for i in range(self.mazeHeight)) for j in range(self.mazeWidth))

        # Connect walls
        for y in range(0, self.mazeHeight):
            for x in range(0, self.mazeWidth):
                if x-1 >= 0:
                    if maze[x-1][y].walls[Orientation.RIGHT] != None:
                        maze[x][y].walls[Orientation.LEFT] = maze[x-1][y].walls[Orientation.RIGHT]
                    else:
                        maze[x][y].walls[Orientation.LEFT] = Wall()
                        maze[x][y].walls[Orientation.LEFT].firstCell = maze[x][y]
                        maze[x][y].walls[Orientation.LEFT].lastCell = maze[x-1][y]
                if x+1 < self.mazeWidth:
                    if maze[x+1][y].walls[Orientation.LEFT] != None:
                        maze[x][y].walls[Orientation.RIGHT] = maze[x+1][y].walls[Orientation.LEFT]
                    else:
                        maze[x][y].walls[Orientation.RIGHT] = Wall()
                        maze[x][y].walls[Orientation.RIGHT].firstCell = maze[x][y]
                        maze[x][y].walls[Orientation.RIGHT].lastCell = maze[x+1][y]
                if y-1 >= 0:
                    if maze[x][y-1].walls[Orientation.BOTTOM] != None:
                        maze[x][y].walls[Orientation.TOP] = maze[x][y-1].walls[Orientation.BOTTOM]
                    else:
                        maze[x][y].walls[Orientation.TOP] = Wall()
                        maze[x][y].walls[Orientation.TOP].firstCell = maze[x][y]
                        maze[x][y].walls[Orientation.TOP].lastCell = maze[x][y-1]
                if y+1 < self.mazeHeight:
                    if maze[x][y+1].walls[Orientation.TOP] != None:
                        maze[x][y].walls[Orientation.BOTTOM] = maze[x][y+1].walls[Orientation.TOP]
                    else:
                        maze[x][y].walls[Orientation.BOTTOM] = Wall()
                        maze[x][y].walls[Orientation.BOTTOM].firstCell = maze[x][y]
                        maze[x][y].walls[Orientation.BOTTOM].lastCell = maze[x][y+1]

        # Start algorithm
        wallList = []
        currentCell = maze[self.startPointX][self.startPointY]
        currentCell.visited = True
        wallList.extend(currentCell.walls)

        # Iterate
        while len(wallList) != 0:
            # Pick a wall randomly in wall list
            currentWall = random.choice(wallList)
            currentCell = None
            
            if currentWall != None:
                # If cell on the opposite of the wall isn't in the maze
                if currentWall.firstCell != None and not(currentWall.firstCell.visited):
                    currentCell = currentWall.firstCell
                elif currentWall.lastCell != None and not(currentWall.lastCell.visited):
                    currentCell = currentWall.lastCell
                
                if currentCell != None:
                    # break the wall, and mark it as part of the maze
                    currentWall.broken = True
                    currentCell.visited = True
                    # Add the walls of the new cell to the wall list
                    wallList.extend(currentCell.walls)
                else:
                    # If all cells are already in the maze, remove the wall to wall list
                    wallList.remove(currentWall)
            else:
                # If there is no wall, skip it
                wallList.remove(currentWall)

        self.mazeGenerated = maze

    def display(self):
        for x in range(len(self.mazeGenerated)):
            for y in range(len(self.mazeGenerated[x])):
                self.mazeGenerated[x][y].display()

if __name__ == "__main__":
    algo = GenerationAlgorythm(4,4)
    algo.generate()
    algo.display()
    myMaze = algo.mazeGenerated