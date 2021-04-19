import pygame
import numpy as np
import sys
import time

# global config
class Config:
    colors = {}
    cnf = {}

    def __init__(self):
        self.colors = {
            "black"     : (0,   0,   0),
            "dark_grey" : (25,  25,  25),
            "grey"      : (128, 128, 128),
            "red"       : (255, 25,  25),
            "green"     : (25,  255, 25),
            "blue"      : (25,  25,  255),
            "white"     : (255, 255, 255)
        }
        self.cnf = {
            "synch_time": 0.1,
            "sc_width"  : 500,
            "sc_height" : 500,
            "background": self.colors["dark_grey"],
            "n_rows"    : 25,
            "n_cols"    : 25,
            "size_row"  : 0,
            "size_col"  : 0,
            "clr_dead"  : self.colors["grey"],
            "clr_alive" : self.colors["white"]
        }
        self.cnf.update({ "size_row" : (self.cnf["sc_width"]  / self.cnf["n_rows"]) } )
        self.cnf.update({ "size_col" : (self.cnf["sc_height"] / self.cnf["n_cols"]) } )

    def get_synchTime(self):
        return self.cnf["synch_time"]
    def get_width(self):
        return self.cnf["sc_width"]
    def get_height(self):
        return self.cnf["sc_height"]
    def get_background(self):
        return self.cnf["background"]
    def get_grid(self):
        return (self.cnf["n_rows"], self.cnf["n_cols"])
    def get_cellSize(self):
        return self.cnf["size_row"],self.cnf["size_col"]
    def get_colorAndWidth(self,alive=False):
        if alive:
            return self.cnf["clr_alive"],0
        else:
            return self.cnf["clr_dead"],1



def main():
    # Initialize config
    cfg = Config()
    # Initialize pygame
    pygame.init()
    # Create screen with its 
    screen = pygame.display.set_mode((cfg.get_width(), cfg.get_height()))
    pygame.display.set_caption("Game of Life")
    # Create game matrix
    gameState = np.zeros(cfg.get_grid())
    # Get number of rows and cols
    rows, cols = cfg.get_grid()[0], cfg.get_grid()[1]

    # Hold flag
    hold = True

    """
    MAIN GAME LOOP
    """
    while True:
        # Set background
        screen.fill(cfg.get_background())
        # Create a new gameState to simultaneously update the hole board
        newGameState = np.copy(gameState)

        # Get the cell size
        ly,lx = cfg.get_cellSize()
        # Iterate each row and column
        for y in range(rows):
            for x in range(cols):
                if not hold:
                    # Calculate new game state as a toroidal board
                    n_neigh =   gameState[(y-1)%rows, (x-1)%cols] + \
                                gameState[(y-1)%rows, (x)  %cols] + \
                                gameState[(y-1)%rows, (x+1)%cols] + \
                                gameState[(y+1)%rows, (x-1)%cols] + \
                                gameState[(y+1)%rows, (x)  %cols] + \
                                gameState[(y+1)%rows, (x+1)%cols] + \
                                gameState[(y)  %rows, (x-1)%cols] + \
                                gameState[(y)  %rows, (x+1)%cols]
                    
                    # RULE#1: dead cell with 3 neigbours alive, revives
                    if gameState[y,x] == 0 and n_neigh == 3:
                        newGameState[y,x] = 1
                    # RULE#2: alive cell with less than 2 or more than 3 alive neighbours, dies
                    elif gameState[y,x] == 1 and (n_neigh < 2 or n_neigh > 3):
                        newGameState[y,x] = 0

                # Create Cell polygon
                poly = [
                    ( (y)  *ly, (x)  *lx ),
                    ( (y)  *ly, (x+1)*lx ),
                    ( (y+1)*ly, (x+1)*lx ),
                    ( (y+1)*ly, (x)  *lx )
                ]
                # Get color and border flag for the game cell
                color,width = cfg.get_colorAndWidth(newGameState[y,x])
                # Draw polygon
                pygame.draw.polygon(screen,color,poly,width)

        gameState = np.copy(newGameState)

        # Track end of game, mouse and keyboard
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    hold = not hold
                    #print("space")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                xCell = int(mouseX/lx)
                yCell = int(mouseY/ly)
                #print("mouse: [{0},{1}] -> cell: [{2},{3}]".format(mouseX,mouseY,xCell,yCell))
                if 1 == gameState[xCell,yCell]:
                    gameState[xCell,yCell] = 0
                else:
                    gameState[xCell,yCell] = 1

        # Update display info
        pygame.display.flip()
        # Synch timer
        time.sleep(cfg.get_synchTime())

if __name__ == "__main__":
    main()