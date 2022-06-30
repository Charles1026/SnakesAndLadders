from SnL.Board import Board

class Player:
  
  def __init__(self, name: str, startPos: int, initialPoints: int, OGs: int, board: Board) -> None:
    self.__NAME = name
    self.__position = startPos
    self.__OGPoints = [initialPoints] * OGs
    self.__BOARD = board
    
    
  def getPoints(self, og: int) -> int:
      try:
        return self.__OGPoints[og]

      except:
        return -1
  
    
  def incrementPoints(self, og: int, amount: int) -> bool:
    if og < 0:
      return False
    
    try:
      if (self.__OGPoints[og] + amount < 0):
        return False
      
      self.__OGPoints[og] += amount
      return True
    
    except KeyError:
      return False
    
    
  def currPosition(self) -> int:
    return self.__position
    
    
  def move(self, og: int, steps: int, cost: int) -> bool:
    if ((not self.incrementPoints(og, cost)) or (self.__BOARD.gameWon(self.__position))):
      return False

    if (self.__position + steps < 0):
      return False
    
    self.__position += steps
    return True