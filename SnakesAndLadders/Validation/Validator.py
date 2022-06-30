import json
import traceback

class Validator:
  
  def __init__(self) -> None:
    with open("./Validation/ogls.json", "r") as file:
      data: dict = json.load(file)
    self.__OglPassPhrase = data.get("passphrase")
    self.__Houses: dict = data.get("Houses")
      
    with open("./Validation/gameMasters.json", "r") as file:
      data: dict = json.load(file)
    self.__GMPassPhrase = data.get("passphrase")
    self.__Games: dict = data.get("Games")
  
  def regOGL(self, passphrase: str, uid: str, uname: str, house: str, og: int, ) -> bool:
    if passphrase != self.__OglPassPhrase or house not in self.__Houses or og < 0 or og > self.__Houses.get(house):
      return False
    
    try:
      with open("./Validation/ogls.json", 'r') as file:
        data: dict = json.load(file)
      
      if not data.get("OGLs") or data.get("OGLs").get(uid):
        return False
      
      data["OGLs"][uid] = [uname, house, og]
      with open("./Validation/ogls.json", 'w') as file:
        json.dump(data, file, indent=2)
      return True
    
    except OSError:
      traceback.print_exception
      return False
      
    
  def regGM(self, passphrase: str, uid:str, uname:str, station: int) -> bool:
    if passphrase != self.__GMPassPhrase or ("Game " + str(station)) not in self.__Games:
      return False
    
    try:
      with open("./Validation/gameMasters.json", 'r') as file:
        data: dict = json.load(file)
        
      if not data.get("GMs") or data.get("GMs").get(uid):
        return False
        
      data["GMs"][uid] = [uname, station]
      with open("./Validation/gameMasters.json", 'w') as file:
        json.dump(data, file, indent=2)
      return True
    
    except OSError:
      traceback.print_exception()
      return False
    
  def getOGL(self, uid: str) -> tuple:
    try:
      with open("./Validation/ogls.json", 'r') as file:
        data: dict = json.load(file)
        
      if ogl := data.get("OGLs").get(uid):
        return ogl[1], ogl[2]
        
    except OSError:
      traceback.print_exception()
    return None
  
  
  def getGM(self, uid: str) -> int:
    try:
      with open("./Validation/gameMasters.json", 'r') as file:
        data: dict = json.load(file)
      
      if gm := data.get("GMs").get(uid):
        return gm[1]
        
    except OSError:
      traceback.print_exception()
    return None
  
  
    
    