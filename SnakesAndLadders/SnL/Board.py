import numpy as np
import json

class Board:
  
  __BOARD = None
  
  __ENDPOINT = None
  
  def __init__(self, height: int, width: int) -> None:
    self.__ENDPOINT = (height * width) - 1
    
    board = np.zeros(self.__ENDPOINT + 1)
    
    file = open('./SnL/gameRules.json')
    data = json.load(file)
    
    snakes = data["snakes"]
    snakeKeys = snakes.keys()
    
    for key in snakeKeys:
       board[int(key) - 1] = snakes.get(key) - 1
       
    ladders = data["ladders"]
    ladderKeys = ladders.keys()
    
    for key in ladderKeys:
       board[int(key) - 1] = ladders.get(key) - 1
       
    self.__BOARD = board
    
    file.close
    
    
  def getEndpoint(self) -> int:
    return self.__ENDPOINT

  def gameWon(self, currPos: int) -> bool:
    return currPos >= self.__ENDPOINT
  
    
  def snakeOrLadder(self, landingSpot: int) -> int:
    # Game Won no Movement
    if (landingSpot >= self.__ENDPOINT):
      return 0
    
    nextPos = self.__BOARD[landingSpot]
    
    # Snake / Ladder Found
    if (nextPos > 0):
      return nextPos - landingSpot
    
    # Normal Movement
    return 0
  
if __name__ == '__main__':
  board = Board(6, 10)
  print("Game Won at 60? " + str(board.gameWon(60)))
  print("Game Won at 59? " + str(board.gameWon(59)))
  print("Game Won at 58? " + str(board.gameWon(58)))
  print("Game Won at 0? " + str(board.gameWon(0)))
  print("S/L at 16? " + str(board.snakeOrLadder(16)))
  print("S/L at 15? " + str(board.snakeOrLadder(15)))
  print("S/L at 42? " + str(board.snakeOrLadder(42)))
  print("S/L at 2? " + str(board.snakeOrLadder(2)))