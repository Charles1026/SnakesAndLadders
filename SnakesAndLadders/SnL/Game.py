import json
import sys
sys.path.append('../Renderer')
from SnL.Board import Board
from SnL.Player import Player
from Renderer.renderer import Renderer

class Game:
  __PLAYERS = {}
  __OLDBLOCKS = ["manis", "strix", "aonyx", "orcaella", "rusa"]
  __NEWBLOCKS = ["chelonia", "panthera"]
  __OLDOGS = 3
  __NEWOGS = 4
  __BOARD = None
  __INITIALPOINTS = 0
  __ROLLCOST = 2
  __MOVECOST = 3
  __MOVESTEPS = 3
  __SABOCOST = 3
  __SABOSTEPS = -3
  __OLDBLKOFFSET = 14
  __SNAKES = {
      "16": 7,
      "28": 11,
      "39": 24,
      "53": 50
  }
  __LADDERS = {
      "14": 26,
      "18": 22,
      "34": 48,
      "43": 56
  }
  __MAXPOINTADDITION = 2
  
  
  def __init__(self) -> None:    
    file = open('./SnL/gameRules.json')
    data = json.load(file)
    
    if ("oldBlocks" in data):
      self.__OLDBLOCKS = data["oldBlocks"]
      
    if ("newBlocks" in data):
      self.__NEWBLOCKS = data["newBlocks"]
      
    if ("oldOGs" in data):
      self.__OLDOGS = data["oldOGs"]
      
    if ("newOGs" in data):
      self.__NEWOGS = data["newOGs"]
    
    if ("initialPoints" in data):
      self.__INITIALPOINTS = data["initialPoints"]
      
    if ("maxPoints" in data):
      self.__MAXPOINTS = data["maxPoints"]
    
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
      
    if ("snakes" in data):
      self.__SNAKES = data["snakes"]
      
    if ("ladders" in data):
      self.__LADDERS = data["ladders"]
      
    if ("maxPointAddition" in data):
      self.__MAXPOINTADDITION = data["maxPointAddition"]
      
    self.__BOARD = Board(data["boardHeight"], data["boardWidth"])
    
    for oldBlock in self.__OLDBLOCKS:
      self.__PLAYERS[oldBlock] = Player(oldBlock, 0 + self.__OLDBLKOFFSET, self.__INITIALPOINTS, self.__OLDOGS, self.__BOARD)
      
    for newBlock in self.__NEWBLOCKS:
      self.__PLAYERS[newBlock] = Player(newBlock, 0, self.__INITIALPOINTS, self.__NEWOGS, self.__BOARD)
    
    file.close()
    
    self.__renderer : Renderer = Renderer()
    
    for newBlock in self.__NEWBLOCKS:
      self.__renderer.addHouse(newBlock, 0)
    
    for oldBlock in self.__OLDBLOCKS:
      self.__renderer.addHouse(oldBlock, self.__OLDBLKOFFSET)
      
    self.__renderer.draw()
  
    
  def incrementPoints(self, house: str, og: int, amount: int) -> bool:
    if amount < 0 or amount > self.__MAXPOINTADDITION or self.maxPoints(house, og):
      return False
    
    try:
      player: Player = self.__PLAYERS[house]
    except KeyError:
      return False
    
    currPoints = self.getPoints(house, og)
    finalAmount = min(amount, self.__MAXPOINTS - currPoints)
    
    return player.incrementPoints(og, finalAmount)

  
  def getPoints(self, house: str, og: int) -> int:
    try:
      player: Player = self.__PLAYERS[house]
    except KeyError:
      return -1
    
    return player.getPoints(og)
  
  
  def maxPoints(self, house: str, og: int) -> int:
    points = self.getPoints(house, og)
    if points == -1:
      return -1
    if points >= self.__MAXPOINTS:
      return 1
    return 0
  
  def maxAddition(self, points: int) -> bool:
    return points > self.__MAXPOINTADDITION
    
  
  def currPosition(self, house: str) -> int:
    try:
      player: Player = self.__PLAYERS[house]
    except KeyError:
      return False
    
    return player.currPosition()
  
  def gameWon(self, house: str) -> bool:
    try:
      player: Player = self.__PLAYERS[house]
    except KeyError:
      return False
    
    return player.gameWon()
  
  
  def roll(self, house: str, og: int, steps: int) -> bool:
    try:
      player: Player = self.__PLAYERS[house]
    except KeyError:
      return False
    
    if (steps < 1 or steps > 6):
      return False
    
    currPos = player.currPosition()
    
    if player.move(og, steps, - self.__ROLLCOST):
      newPos = player.currPosition() + self.specialTileHandler(house, og)
      self.__renderer.moveHouse(house, currPos, newPos)
      self.__renderer.draw()
      return True
    
    return False
  
  
  def move(self, house: str, og: int) -> bool:
    try:
      player: Player = self.__PLAYERS[house]
    except KeyError:
      return False
    
    currPos = player.currPosition()
    
    if player.move(og, self.__MOVESTEPS, - self.__MOVECOST):
      newPos = player.currPosition() + self.specialTileHandler(house, og)
      self.__renderer.moveHouse(house, currPos, newPos)
      self.__renderer.draw()
      return True
    
    return False
    
    
  def sabo(self, house: str, other: str, og: int) -> bool:
    try:
      player: Player = self.__PLAYERS[house]
      target: Player = self.__PLAYERS[other]
    except KeyError:
      return False
    
    if (not player.incrementPoints(og, - self.__SABOCOST)):
      return False
    
    currPos = target.currPosition()
    
    if (not target.move(0, self.__SABOSTEPS, 0)):
      player.incrementPoints(og, self.__SABOCOST)
      return False
    
    newPos = target.currPosition() + self.specialTileHandler(other, og)
    self.__renderer.moveHouse(other, currPos, newPos)
    self.__renderer.draw()
    return True
  
  
  def specialTileHandler(self, house: str, og: int) -> int:
    try:
      player: Player = self.__PLAYERS[house]
    except KeyError:
      return False
    
    currPos = player.currPosition()
    
    if(snakePos:=self.__SNAKES.get(str(currPos))):
      steps = snakePos - currPos
      player.move(og, steps, 0)
      return steps
      
    elif(ladderPos:=self.__LADDERS.get(str(currPos))):
      steps = ladderPos - currPos
      player.move(og, steps, 0)
      return steps
    
    return 0
    

  def adminView(self, house: str) -> tuple:
    try:
      player: Player = self.__PLAYERS[house]
    except KeyError:
      return None

    return player.adminView()


  def adminSetPoints(self, house: str, og: int, amount: int) -> bool:
    try:
      player: Player = self.__PLAYERS[house]
    except KeyError:
      return False

    return player.adminSetPoints(og, amount)


  def adminSetPos(self, house: str, position: int) -> bool:
    try:
      player: Player = self.__PLAYERS[house]
    except KeyError:
      return False

    currPos = player.currPosition()
    if player.adminSetPos(position):
      newPos = position + self.specialTileHandler(house, 0)
      self.__renderer.moveHouse(house, currPos, newPos)
      self.__renderer.draw()
      return True
    return False


  def adminAllSet(self, points: int) -> bool:
    for player in self.__PLAYERS:
      if not self.__PLAYERS[player].adminAllSet(points):
        return False
    return True
  
  def recordGameState(self) -> bool:
    houseData = {}
    for player in self.__PLAYERS:
      houseData[player] = self.__PLAYERS[player].adminView()
    with open("./logs/gameState.json", 'w') as file:
      json.dump(houseData, file, indent=2)

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
  
  print("Orcaella Adding 2 Points: " + str(game.incrementPoints("Orcaella", 2)))
  print("Orcaella Roll To Snake: " + str(game.roll("Orcaella", 4)))
  print("Orcaella End Location: " + str(game.currPosition("Orcaella") + 1) + "\n")