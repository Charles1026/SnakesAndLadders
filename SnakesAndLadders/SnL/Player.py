from SnL.Board import Board

class Player:
  
  def __init__(self, name: str, startPos: int, initialPoints: int, OGs: int, board: Board) -> None:
    self.__NAME = name
    self.__position = startPos
    self.__OGPoints = [initialPoints] * OGs
    self.__BOARD = board
    

  def getName(self) -> str:
    return self.__NAME

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
    
    
  def gameWon(self) -> bool:
    return self.__BOARD.gameWon(self.__position)
  
    
  def move(self, og: int, steps: int, cost: int) -> bool:
    if ((not self.incrementPoints(og, cost)) or self.gameWon() or self.__position < 0):
      return False
    
    self.__position = max(min(self.__position + steps, self.__BOARD.getEndpoint()), 0)
    return True


  def adminView(self) -> tuple:
    info = [self.__position]
    info.append(self.__OGPoints)
    return tuple(info)


  def adminSetPoints(self, og: int, amount: int) -> bool:
    if og < 0 or amount < 0:
      return False
    
    try:      
      self.__OGPoints[og] = amount
      return True
    
    except KeyError:
      return False


  def adminSetPos(self, position: int) -> bool:
    if position < 0 or position > self.__BOARD.getEndpoint():
      return False

    self.__position = position
    return True
  
  def adminAllSet(self, points: int) -> bool:
    for i in range(len(self.__OGPoints)):
      self.__OGPoints[i] = points
    return True