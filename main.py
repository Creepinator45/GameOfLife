from weakref import WeakValueDictionary
from typing import Optional, Sequence
from time import sleep

class Cell:
    allCells: dict[tuple[int, int], "Cell"] = WeakValueDictionary()
    livingCells: dict[tuple[int, int], "Cell"] = {}
    adjacentOffsets: tuple[tuple[int, int]] = ((-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    doActiveDeletion:bool = True

    def __init__(self, position: tuple[int, int]):
        self.__numLiveNeighbors: int = 0
        self.__isAlive: bool = False
        self.__position: tuple[int, int] = position
        self.__neighbors: list[Optional[Cell]] = [None, None, None, None, None, None, None, None]
        self.__willLive: bool = False
        Cell.allCells[position] = self
    
    @property
    def numLiveNeighbors(self):
        return self.__numLiveNeighbors
    @numLiveNeighbors.setter
    def numLiveNeighbors(self, value: int):
        self.__numLiveNeighbors = value
    
    @property
    def position(self):
        return self.__position
    
    @property
    def isAlive(self):
        return self.__isAlive

    def birth(self):
        if self.__isAlive:
            raise ValueError("attempted to birth living cell")
        
        self.__isAlive = True
        Cell.livingCells[self.position] = self
        for i, offset in enumerate(Cell.adjacentOffsets):
            #get references to neighboring cells, creating them if they don't yet exist
            neighborPos = (self.position[0] + offset[0], self.position[1] + offset[1])

            #self.__neighbors[i] = Cell.allCells.setdefault(neighborPos, Cell(neighborPos)) I have no idea why this line wasn't working, the following is my replacement for it
            if neighborPos in Cell.allCells:
                self.__neighbors[i] = Cell.allCells[neighborPos]
            else:
                self.__neighbors[i] = Cell(neighborPos)
                Cell.allCells[neighborPos] = self.__neighbors[i]

            #update neighbor counts
            self.__neighbors[i].numLiveNeighbors += 1
    
    def kill(self):
        if not self.__isAlive:
            raise ValueError("attempted to kill dead cell")

        self.__isAlive = False
        del Cell.livingCells[self.position]
        #reset neighbors
        for neighbor in self.__neighbors:
            neighbor.numLiveNeighbors -= 1
            neighbor = None
    
    def planUpdate(self):
        match self.numLiveNeighbors:
            case 0 if Cell.doActiveDeletion and not self.isAlive:
                del Cell.allCells[self.position]
            case 0|1:
                self.__willLive = False
            case 2:
                self.__willLive = self.isAlive
            case 3:
                self.__willLive = True
            case 4|5|6|7|8:
                self.__willLive = False
    
    def update(self):
        if self.__willLive == self.isAlive:
            return
        if self.__willLive:
            self.birth()
        else:
            self.kill()

    def __repr__(self) -> str:
        return f"Cell(living: {self.isAlive}, position: {self.position}, living neighbors: {self.numLiveNeighbors})"
    
    @staticmethod
    def planGrid():
        cellsToPlan = list(Cell.allCells.values())
        for cell in cellsToPlan:
            cell.planUpdate()
    
    @staticmethod
    def updateGrid():
        cellsToUpdate = list(Cell.allCells.values())
        for cell in cellsToUpdate:
            cell.update()
    
    @staticmethod
    def birthCells(cellCoordinates: Sequence[tuple[int, int]]):
        for coordinate in cellCoordinates:
            if coordinate in Cell.allCells:
                cell = Cell.allCells[coordinate]
            else:
                cell = Cell(coordinate)
            cell.birth()

    @staticmethod
    def reprGrid() -> str:
        #find bounds for grid
        maxX = 0
        minX = 0
        maxY = 0
        minY = 0
        for cell in Cell.livingCells:
            if cell[0] > maxX:
                maxX = cell[0]
            if cell[0] < minX:
                minX = cell[0]
            if cell[1] > maxY:
                maxY = cell[1]
            if cell[1] < minY:
                minY = cell[1]
        #assemble grid
        outputStr = ""
        for x in range(minX-1, maxX+2):
            for y in range(minY-1, maxY+2):
                match Cell.allCells.get((x,y), None):
                    case None:
                        outputStr += "  "
                    case cell if cell.isAlive:
                        outputStr += " x"
                    case cell if not cell.isAlive:
                        outputStr += " -"
            outputStr += "\n"
        
        return outputStr

def main():
    startingCells = [(0,0), (0,1), (0,-1), (-1,0), (1, -1)]
    Cell.birthCells(startingCells)
    Cell.doActiveDeletion = True

    while True:
        print("----------------------------------------------")
        print(Cell.reprGrid())
        Cell.planGrid()
        Cell.updateGrid()
        sleep(1)

if __name__ == '__main__':
    main()