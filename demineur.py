# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 12:24:53 2024

@author: arthu
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
from functools import partial


# GRID CLASS
class Grid:
    def __init__(self, cells, column, row):
        self.cells = cells
        self.column = column
        self.row = row
        
    # return un index de cells en int
    def positionCells(self, c, r):
        index = c * self.column + r
        return index
    
    def isPositionValid(self, c, r):
        if c > self.column -1 or r > self.row -1 or c < 0 or r < 0:
            return False
        else:
            return True
        
    def getCell(self, c, r):
        if self.isPositionValid(c, r):
            return self.cells[self.positionCells(c, r)]
        return None
        
        
    
    
    #fonction qui calcul quelles sont les cases adjacentes
    def touchingCells(self, c, r):
        
        touchingCells = []
        for colonne in range(c-1, c+2):
            for ligne in range(r-1, r+2):
                if colonne == c and ligne == r:
                    continue
                if self.isPositionValid(colonne, ligne):
                    touchingCells.append(self.getCell(colonne, ligne)) 
        return touchingCells
    
    def NumberOfBomb(self, Array):
        i = 0
        for bombe in Array:
            if bombe.bombeOrNot():
                i += 1
        return i
    
    
        
    
    # print function
    def __str__ (self):
        return f'{self.cells}'
    def __repr__ (self):
        return f'{self.cells}'
    
# CELL CLASS        
class Cell:
    def __init__(self, state):
        self.state = state
        self.isRevealed = False
        self.button = None 
        
    def bombeOrNot(self):
        return self.state == 1
        
            
    # print function
    def __str__ (self):
        return f'{self.state}'
    def __repr__ (self):
        return f'{self.state}'


def generateGrid(c, r, mine):
    allCells = []
    safeCells = (c*r)-mine
    
    while(len(allCells) != safeCells):
        allCells.append(Cell(0))
    for i in range(mine):
        allCells.append(Cell(1))
    np.random.shuffle(allCells)
    grid = Grid(allCells, c, r)         
    return grid


        
# generate grid function
class GrapGrid:
    def __init__(self, grille):
        self.grille = grille
        self.root = tk.Tk()
        self.root.title('D E M I N E U R')
        
        cellSize = 30
        
        window_width = (self.grille.column)*cellSize
        window_height = (self.grille.row) *cellSize
        self.root.geometry(f"{window_width}x{window_height}")
        self.buttons = []  # buttons
        
        for colonne in range(grille.row):
            row_buttons = []  
            for ligne in range(grille.column):
                
                button = tk.Button(
                    self.root,
                    text="",
                    width= 5,
                    height= 3,
                    borderwidth=2,
                    command=partial(self.onClickButton, colonne, ligne))

                button.grid(row=colonne, column=ligne, sticky="nsew")
                row_buttons.append(button)
                self.grille.getCell(colonne, ligne).button = button
                
            self.buttons.append(row_buttons)
            
        for i in range(grille.column):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(grille.row):
            self.root.grid_rowconfigure(i, weight=1)
            
        self.root.mainloop()
        
    """def updateTextSize(self):
            font_size = (self.grille.column + self.grille.row) / 3
            style = ttk.Style()
            style.configure("TLabel", font=('Helvetica', font_size))"""

    
    def recursivZeroCells(self, c, r):
        for colonne in range(c-1, c+2):
            for ligne in range(r-1, r+2):
                if colonne == c and ligne == r:
                    continue
                self.onClickButton(colonne, ligne)
                    


    def onClickButton(self, x, y):
        buttonCell = self.grille.getCell(x, y)
        if not self.grille.isPositionValid(x, y) or buttonCell.isRevealed == True:
            return 
            
        buttonCell.isRevealed = True
        bombes = None

        if buttonCell.bombeOrNot():
            for x in range(self.grille.column):
                for y in range(self.grille.row):
                    cell = self.grille.getCell(x, y)
                    if cell.bombeOrNot():
                        label = ttk.Label(self.root, text="💣", font="Helvatica")
                        label.configure(anchor="center")
                        self.buttons[x][y].grid_remove()
                        label.grid(row=x, column=y, sticky="nsew")
                       
                        
            YoN = tk.messagebox.askyesno(title=None, message="You lost, do you wish to restart the game ?")
            if YoN:
                self.root.destroy()
                main()
            else:
                self.root.destroy()
        else:
            bombes = self.grille.NumberOfBomb(self.grille.touchingCells(x, y))
            if bombes == 0:
                self.recursivZeroCells(x, y)
                bombes = " "
            label = ttk.Label(self.root, text=str(bombes), font="Helvatica", borderwidth=2, relief="solid")
            label.configure(background="grey", anchor="center")
            self.grille.getCell(x, y).button.grid_remove()
            label.grid(row=x, column=y, sticky="nsew")
            





# main        
def main() :
    grid = generateGrid(15, 15, 20)
    graf = GrapGrid(grid)
    

if __name__ == '__main__':
    main()








