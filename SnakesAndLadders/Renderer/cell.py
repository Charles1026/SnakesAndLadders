class Cell:
  
  def __init__(self, id: int, cellX: int, cellY: int) -> None:
    self.id = id
    self.cellX = cellX
    self.cellY = cellY
    self.__houses = set()
    
  def addHouse(self, house:str) -> None: 
    self.__houses.add(house)
    
  def delHouse(self, house:str) -> None:
    self.__houses.remove(house)
  
  def inCell(self, house) -> bool:
    return house in self.__houses
    
  def getHouses(self) -> set:
    return self.__houses