# imports
from maze import *
from sys import *

import lib.utils as utils
from lib.utils import *

try:
	import pygame
except :
  logger.logIt (fromModule = "import MAIN" , tag = "ERROR", content = "Can't import pygame... check your installation if you want to use visualisation module")
	
from math import floor



WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
INVO = (210,103,40)

class MazeView:
  """
    Provide some functions to visualise the result of the maze generator
  """
  #-------------------------------------------------------------------------------------#
  #              function definitions for drawing the maze with pygame                  #
  #-------------------------------------------------------------------------------------#
  def __init__(self, cell = 102 , wall = 10, directory = "datas/generated/defaultMuseum", writeMap = False):
    self.cellSize = cell
    self.wallSize = wall
    self.writeDirectory = directory
    self.writeMap = writeMap


  # generates a window with maze with all cells isolated from each other
  def base_window(self, m):
    winwidth = m.cols*self.cellSize+(m.cols+1)*self.wallSize
    winheight = m.rows*self.cellSize+(m.rows+1)*self.wallSize
    w = pygame.display.set_mode((winwidth,winheight))
    pygame.display.set_caption("Museum map")
    w.fill(BLACK)

    for i in range(m.rows):
      for j in range(m.cols):
        pygame.draw.rect(w,WHITE,(self.wallSize+(j*self.cellSize+j*self.wallSize),self.wallSize+(i*self.cellSize+
        i*self.wallSize),self.cellSize,self.cellSize))

    return w

  #--------------------------------------------------------------------------------------

  # knocks down walls from base_window to create the path
  def maze_window(self, m):
    w = self.base_window(m)

    for i in range(m.rows):
      for j in range(m.cols):
        if not m.maze[i][j][BOTTOMWALL]:
          pygame.draw.rect(w,WHITE,(j*self.cellSize+(j+1)*self.wallSize,(i+1)*self.cellSize+(i+1)
          *self.wallSize,self.cellSize,self.wallSize))
        if not m.maze[i][j][RIGHTWALL]:
          pygame.draw.rect(w,WHITE,((j+1)*self.cellSize+(j+1)*self.wallSize,i*self.cellSize+(i+1)
          *self.wallSize,self.wallSize,self.cellSize))

    pygame.display.update()
    return w
    
  #--------------------------------------------------------------------------------------

  # paints the solution path in the maze window
  def maze_path_window(self, m,w):
    path = m.solutionpath

    # print every cell within the solution path
    for index in range(len(path)-1):
      actrow = path[index][0]
      actcol = path[index][1]
      nextrow = path[index+1][0]
      nextcol = path[index+1][1]
      pygame.draw.rect(w,RED,(actcol*self.cellSize+(actcol+1)*self.wallSize,actrow*self.cellSize+(actrow+
      1)*self.wallSize,self.cellSize,self.cellSize))

      # also paint the white spaces between the cells
      if actrow == nextrow:
        if actcol < nextcol:
          pygame.draw.rect(w,RED,((actcol+1)*self.cellSize+(actcol+1)*self.wallSize,actrow*self.cellSize+
          (actrow+1)*self.wallSize,self.wallSize,self.cellSize))
        else:
          pygame.draw.rect(w,RED,(actcol*self.cellSize+actcol*self.wallSize,actrow*self.cellSize+(actrow+
          1)*self.wallSize,self.wallSize,self.cellSize))
      elif actcol == nextcol:
        if actrow < nextrow:
          pygame.draw.rect(w,RED,(actcol*self.cellSize+(actcol+1)*self.wallSize,(actrow+1)*self.cellSize+
          (actrow+1)*self.wallSize,self.cellSize,self.wallSize))
        else:
          pygame.draw.rect(w,RED,(actcol*self.cellSize+(actcol+1)*self.wallSize,actrow*self.cellSize+
          actrow*self.wallSize,self.cellSize,self.wallSize))

    # add a different color for start and end cells
    startrow = path[0][0]
    startcol = path[0][1]
    endrow = path[-1][0]
    endcol = path[-1][1]

    pygame.draw.rect(w,BLUE,(startcol*self.cellSize+(startcol+1)*self.wallSize,startrow*self.cellSize+(
    startrow+1)*self.wallSize,self.cellSize,self.cellSize))
    pygame.draw.rect(w,GREEN,(endcol*self.cellSize+(endcol+1)*self.wallSize,endrow*self.cellSize+(endrow+
    1)*self.wallSize,self.cellSize,self.cellSize))
    pygame.display.update()

    if self.writeMap:
      filename = self.writeDirectory + "map.bmp"
      pygame.image.save(w, filename) 
      logger.logIt (fromModule = "mazeView" , tag = "INFO", content = "Full map successfully saved to " + filename )

      for index in range(0,len(path)):
        surface = w.copy()

        actrow = path[index][0]
        actcol = path[index][1]

        pygame.draw.rect(surface,INVO,(actcol*self.cellSize+(actcol+1)*self.wallSize,actrow*self.cellSize+(
      actrow+1)*self.wallSize,self.cellSize,self.cellSize))


        filename = self.writeDirectory + "map"+str(index)+".bmp"
        pygame.image.save(surface, filename) 
        logger.logIt (fromModule = "mazeView" , tag = "INFO", content = "Partial map successfully saved to" + filename )

    
   
def visualize(mazeValue, dirFile = "datas/generated/defaultMuseum"):
  
  #mazeValue.solve_maze()
  #print maze
  #print maze.solutionpath

  # show the maze with the solution path
  mazeView = MazeView (108,12,dirFile, True)
  pygame.init()
  window = mazeView.maze_window(mazeValue)
  mazeView.maze_path_window(mazeValue,window)

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()

#================================================================================#
#                                Main Program                                    #
#================================================================================#
def main_function(rows, cols , recursive = False, cell = 102 , wall = 10):
  # sizes and colors

  maze = []
  # generate random maze, solve it
  if recursive : 
    minSize = floor((rows * cols) * 0.7)
    result = maze_search(rows, cols, minSize)
    maze = result[0]
  else :
    maze = Maze(rows,cols)
    maze.solve_maze()
  print maze

  #print maze
  #print maze.solutionpath

  # show the maze with the solution path
  mazeView = MazeView (cell,wall)
  pygame.init()
  window = mazeView.maze_window(maze)
  mazeView.maze_path_window(maze,window)

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()

if __name__ == "__main__":
  if argv[1] == "-h":
    print "Usage : numbersRows numbersCols sizeCell sizeWall \n ex : python mazeView.py 100 100 10 2"
    exit(0)

  # get the maze size from program arguments
  rows = int(argv[1])
  cols = int(argv[2])
  sizeCell = int(argv[3])
  sizeWall = int(argv[4])

  main_function(rows, cols, False,sizeCell ,sizeWall )
  # if ( argv[5] == 'T'):
  #   main_function(rows, cols, False,sizeCell ,sizeWall )
  # else :
  #   main_function(rows, cols, True, sizeCell ,sizeWall)