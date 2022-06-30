from Renderer.cell import Cell

class Board:
  
  __boardImg = "../assets/board.jpg"
  __boardWidth = 1280
  __boardHeight = 905
  __boardRows = 6
  __boardColumns = 10
  
  __cellWidth = 115
  __cellHeight = 122
  __firstCellX = 65
  __firstCellY = 82
  
  def __init__(self) -> None:
    cellID = 1
    currY = self.__firstCellY + (self.__boardRows - 1) * self.__cellHeight
    self.__board = []
    
    for row in range(self.__boardRows):
      if (row % 2 == 0):
        currX = self.__firstCellX
        for column in range(self.__boardColumns):
          self.__board.append(Cell(cellID, currX, currY))
          currX += self.__cellWidth
          cellID += 1
                
      else:
        currX = self.__firstCellX + (self.__boardColumns - 1) * self.__cellWidth
        for column in range(self.__boardColumns):
          self.__board.append(Cell(cellID, currX, currY))
          currX -= self.__cellWidth
          cellID += 1

      currY -= self.__cellHeight
  
  def getCellWidth(self) -> int:
    return self.__cellWidth  
      
  def getCellHeight(self) -> int:
    return self.__cellHeight  
  
  def getBoard(self) -> list:
    return self.__board
  
  def addHouse(self, house, cell) -> bool:
    curr = self.__board[cell]

    if curr.inCell(house):
      return False
    
    curr.addHouse(house)
    return True
  
  def moveHouse(self, house, currCell, newCell) -> bool:
    curr = self.__board[currCell]
    new = self.__board[newCell]
    
    if curr.inCell(house) and not new.inCell(house):
      curr.delHouse(house)
      new.addHouse(house)
      return True
    
    return False
  