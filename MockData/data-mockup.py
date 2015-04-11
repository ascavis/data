import random
import math
import json

def randfloat(Min, Max, excludeMax=False):
  return(random.random()*(Max-Min)+Min)

def Orbitals():
  return({
    "periodYEARS" : randfloat(0.1, 10),
    "semimajoraxisAU" : randfloat(2, 5),
    "perihelionDATE" : randfloat(0, 10*365*24*3600),
    "argumentOfPerihelion" : randfloat(0, 2*math.pi),
    "longitudeOfTheAscendingNode" : randfloat(0, 2*math.pi, True),
    "inclination" : randfloat(0, math.pi),
    "eccentricity" : randfloat(0, 1, True),
    "meanAnomaly" : randfloat(0, math.pi, True)})


orbitTypes = ["smelly", "stinky", "whiny", "sad", "angry", "mad", "tiny", "stupid", "evil", "arrogant"]
spectralTypes = ["A", "B", "C"]

def Classification():
  Type = {}
  for sType in spectralTypes:
    Type.update({sType : randfloat(0,1)})
  return({
    "orbitType" : random.choice(orbitTypes),
    "diameterKM" : randfloat(0.01, 100),
    "albedo" : randfloat(0, 1),
    "spinPeriodH" : randfloat(0, 1.0*10**300), #maxfloat ~ 1.8e+308
    "type" : Type})
    

class Asteroid(object):
  def __init__(self):
    self.name = ''.join([random.choice('abcdefg1234567890') for _ in range(10)])
    self.orbitals = Orbitals()
    self.details = {}
    for i in range(random.randint(0,20)):
      self.details.update({''.join([random.choice('abcdefg1234567890') for _ in range(10)]): randfloat(1,100)})
    self.classification = Classification()

  def __json__(self):
    return({
      "Asteroid": {
        "name" : self.name,
        "orbitals": self.orbitals,
        "details": self.details,
        "classification" : self.classification}})

def printNJsonAsteroids(n):
  print(json.dumps([Asteroid().__json__() for i in range(n)]))

if(__name__=="__main__"):
  printNJsonAsteroids(1000)
