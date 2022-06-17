class Player:
  
  __NAME = "House"
  
  __position = 0
  
  __points = 0
  
  __BOARD = None

  
  def __init__(self, name, startPos, initialPoints, board) -> None:
    self.__NAME = name
    self.__position = startPos
    self.__points = initialPoints
    self.__BOARD = board
    
    
  def getPoints(self) -> int:
    return self.__points
  
    
  def incrementPoints(self, amount) -> bool:
    if (self.__points + amount < 0):
      return False
    
    self.__points += amount
    return True
    
    
  def currPosition(self) -> int:
    return self.__position
    
    
  def move(self, steps, cost) -> bool:
    if ((not self.incrementPoints(cost)) or (self.__BOARD.gameWon(self.__position))):
      return False

    if (self.__position + steps < 0):
      return False
    
    self.__position += steps
    return True