from PIL import Image
from Renderer.board import Board

class Renderer:
  
  __pathToImages = "./assets/"
  __houseWidth = 594
  __houseHeight = 420
  
  def __init__(self) -> None:
    self.__board = Board()
    
  def addHouse(self, house, cell) -> bool:
    return self.__board.addHouse(house, cell)
  
  def moveHouse(self, house, currCell, newCell) -> bool:
    if self.__board.moveHouse(house, currCell, newCell):
      return True
    return False
    
  def draw(self) -> None:
    cells = self.__board.getBoard()
    boardImg = Image.open(self.__pathToImages + "board.png")
    
    for cell in cells:
      houses : set = cell.getHouses()
      size = len(houses)
      if size > 0:
        combined = Image.new('RGBA', (self.__houseWidth, self.__houseHeight * size))
        currY = 0
        for house in houses:
          housePic = Image.open(self.__pathToImages + house + ".png")
          combined.paste(housePic, (0, currY), housePic)
          currY += self.__houseHeight
          
        newWidth = round((combined.width / combined.height) * self.__board.getCellHeight())
        resized = combined.resize((newWidth, self.__board.getCellHeight()))
        boardImg.paste(resized, (cell.cellX, cell.cellY), resized)
    boardImg.save("./renderedImg.png")
    print("New Image Drawn")
      
      
if __name__ == "__main__":
  renderer : Renderer = Renderer()
  renderer.addHouse("Strix", 1)
  renderer.addHouse("Chelonia", 9)
  renderer.draw()
  renderer.moveHouse("Strix", 1, 10)
  renderer.draw()
  
    