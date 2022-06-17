import json
from Board import Board
from Player import Player

class Game:
  __PLAYERS = {}
  __OLDBLOCKS = ["Manis", "Strix", "Aonyx", "Orcaella", "Rusa"]
  __NEWBLOCKS = ["Chelonia", "Panthera"]
  __BOARD = None
  __INITIALPOINTS = 0
  __ROLLCOST = 2
  __MOVECOST = 3
  __MOVESTEPS = 3
  __SABOCOST = 3
  __SABOSTEPS = -3
  __OLDBLKOFFSET = 15
  
  
  def __init__(self) -> None:    
    file = open('gameRules.json')
    data = json.load(file)
    
    if ("oldBlocks" in data):
      __OLDBLOCKS = data["newBlocks"]
      
    if ("newBlocks" in data):
      __NEWBLOCKS = data["newBlocks"]
    
    if ("initialPoints" in data):
      self.__INITIALPOINTS = data["initialPoints"]
    
    if ("rollCost" in data):
      self.__ROLLCOST = data["rollCost"]
      
    if ("moveCost" in data):
      self.__MOVECOST = data["moveCost"]
      
    if ("moveSteps" in data):
      self.__MOVESTEPS = data["moveSteps"]
      
    if ("saboCost" in data):
      self.__SABOCOST = data["saboCost"]
      
    if ("saboSteps" in data):
      self.__SABOSTEPS = data["saboSteps"]
      
    if ("oldBlockOffset" in data):
      self.__OLDBLKOFFSET = data["oldBlockOffset"]
      
    self.__BOARD = Board(data["boardHeight"], data["boardWidth"])
    
    for oldBlock in self.__OLDBLOCKS:
      self.__PLAYERS[oldBlock] = Player(oldBlock, 0 + self.__OLDBLKOFFSET, self.__INITIALPOINTS, self.__BOARD)
      
    for newBlock in self.__NEWBLOCKS:
      self.__PLAYERS[newBlock] = Player(newBlock, 0, self.__INITIALPOINTS, self.__BOARD)
    
    file.close()
  
    
  def incrementPoints(self, house, amount) -> bool:
    player = self.__PLAYERS[house]
    
    if (player == None):
      return False
    
    return player.incrementPoints(amount)

  
  def getPoints(self, house) -> int:
    player = self.__PLAYERS[house]
    
    if (player == None):
      return False
    
    return player.getPoints()
  
  
  def currPosition(self, house) -> int:
    player = self.__PLAYERS[house]
    
    if (player == None):
      return False
    
    return player.currPosition()
  
  
  def roll(self, house, steps) -> bool:
    player = self.__PLAYERS[house]
    
    if (player == None):
      return False
    
    # if (steps < 1 or steps > 6):
    #   return False
    
    return player.move(steps, - self.__ROLLCOST)
  
  
  def move(self, house) -> bool:
    player = self.__PLAYERS[house]
    
    if (player == None):
      return False
    
    return player.move(self.__MOVESTEPS, - self.__MOVECOST)
    
    
  def sabo(self, house, other) -> bool:
    player = self.__PLAYERS[house]
    target = self.__PLAYERS[other]
    
    if (player == None or target == None):
      return False
    
    if (not player.incrementPoints(- self.__SABOCOST)):
      return False
    
    if (not target.move(self.__SABOSTEPS, 0)):
      player.incrementPoints(self.__SABOCOST)
      return False
    
    return True
    
    
if __name__ == '__main__':
  game = Game()
  
  print("Strix Starting Points: " + str(game.getPoints("Strix")))
  print("Strix Starting Location: " + str(game.currPosition("Strix") + 1) + "\n")
  
  print("Strix Adding 2 Points: " + str(game.incrementPoints("Strix", 2)))
  print("Strix Try Move Without Enough Points: " + str(game.move("Strix")))
  
  print("Strix After Failed Move Points: " + str(game.getPoints("Strix")))
  print("Strix After Failed Move Location: " + str(game.currPosition("Strix") + 1) + "\n")
  
  print("Strix Try Roll: " + str(game.roll("Strix", 3)))
  
  print("Strix After Roll Points: " + str(game.getPoints("Strix")))
  print("Strix After Roll Location: " + str(game.currPosition("Strix") + 1) + "\n")
  
  print("Orcaella Starting Location: " + str(game.currPosition("Orcaella") + 1))
  print("Strix Try Sabo Orcaella Without Enough Points: " + str(game.sabo("Strix", "Orcaella")))
  print("Strix Points: " + str(game.getPoints("Strix")))
  print("Orcaella After Failed Sabotage Location: " + str(game.currPosition("Orcaella") + 1) + "\n")
  
  print("Strix Adding 3 Points: " + str(game.incrementPoints("Strix", 3)))
  print("Strix Points: " + str(game.getPoints("Strix")) + "\n")
  
  print("Chelonia Starting Location: " + str(game.currPosition("Chelonia") + 1))
  print("Strix Try Sabo Chelonia At Start: " + str(game.sabo("Strix", "Chelonia")))
  print("Strix Points: " + str(game.getPoints("Strix")))
  print("Chelonia After Failed Sabotage Location: " + str(game.currPosition("Chelonia") + 1) + "\n")
  
  print("Orcaella Starting Location: " + str(game.currPosition("Orcaella") + 1))
  print("Strix Try Sabo Orcaella: " + str(game.sabo("Strix", "Orcaella")))
  print("Strix Points: " + str(game.getPoints("Strix")))
  print("Orcaella After Sabotage Location: " + str(game.currPosition("Orcaella") + 1) + "\n")
  
  print("Strix Adding 2 Points: " + str(game.incrementPoints("Strix", 2)))
  print("Strix Points: " + str(game.getPoints("Strix")))
  print("Strix Roll to End: " + str(game.roll("Strix", 42)))
  print("Strix End Location: " + str(game.currPosition("Strix") + 1) + "\n")
  
  print("Strix Adding 2 Points: " + str(game.incrementPoints("Strix", 2)))
  print("Strix Roll Beyond End: " + str(game.roll("Strix", 1)))
  print("Strix End Location: " + str(game.currPosition("Strix") + 1) + "\n")