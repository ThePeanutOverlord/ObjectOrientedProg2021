"""                   
 Author:           Paige Champagne
 Email:            paigechamp@gmail.com
 Label:            Final Project
 Title:            Pandemic Simulation
 Course:           CMPS 2143
 Semester:         Spring 2020

 Description:
          this is a simulation of a pandemic using pygame

 Usage:
       Customize config.json to change simulation variables

 Files:             simulation.py
                    config.json
                    images and fonts folders
                    readme.md
                
"""

#!/usr/bin/env python3

# Import and initialize the pygame library
import pygame
import random
import math
import sys,os
import json

# list of colors
colors = ["blue", "red", "yellow", "orange", "green"]
states = ["susceptible", "infected", "recovered"]


#cheacks if config.json is available
if os.path.isfile("config.json"):
       
        # open config for reading
        f = open("config.json")

        # read the file into a "data" variable
        data = f.read()

        # convert json into a python dictionary
        config = json.loads(data)

        # print the data out to the screen
        for key in config:
            print(key, config[key])
'''         
Class: population

Description: holds the people for the simulation

Methods:    __init__()
            add_people()

Usage: holds people
'''
class population(object):
    # constructor
    def __init__(self):
        self.list = []
        self.count = 0
    '''         
    Public: add_people(self, state, **kwargs)

    Description: adds people, both infected and not, into each community

    Params:     self,
                state: state of the person
                **kwargs: allows for varying data to be passed in

    returns:    p: the person created
    '''
    def add_people(self, state, **kwargs):
        color = kwargs.get("color", random.choice(colors))
        width = kwargs.get("width", config["sprite"]["width"])
        height = kwargs.get("height", config["sprite"]["height"])
        speed = kwargs.get("speed", config["sprite"]["speed"])
        community = kwargs.get("community", 1)

        x = random.randint(0, config["game"]["width"])
        y = random.randint(0, config["game"]["height"])
        coord = kwargs.get("coord", [x, y])
        if state == 1:
            p = Person(screen, coord=coord, state= "infected", community = community)
        elif state == 0:
            p = Person(screen, coord=coord, state="susceptible", community = community)
        
        # self.list.append(p)
        # self.count += 1
        return p

'''         
Class: Simulation

Description: runs the entire simulation and handles most sim variables

Methods:    __init__()
            get_infected()
            get_recovered()
            get_susceptible()
            populatesim()
            makeCommunities()
            simRun()
            calcR()

Usage: performs most major functions of the sim, responsible for running sim
'''
class Simulation:
    #constructor
    def __init__(self, **kwargs):
        self.pop = [] #list holding all the people
        self.game_width = config["game"]["width"] #screen width
        self.game_height = config["game"]["height"] #screen height
        self.screen = kwargs.get("screen", None) #screen? idk it's a pygame thing
        self.communities = [] #array holding all the communities
        self.sprite_group = pygame.sprite.Group() #group of sprites to draw
        self.infection_radius = config["sim"]["infection_radius"] #infection radius
        self.infection_rate = config["sim"]["infection_rate"]   #infection rate
        self.population_count = config["sim"]["population_count"] #number of population
        self.init_infected = config["sim"]["initial_infected"] #initial infected people
        self.init_susceptible = config["sim"]["initial_susceptible"] #initial susceptible people
        self.cnumber = config["sim"]["communities"] #number of communities
        self.R = 0  #R, the average number of people each infected person infects

        if self.screen == None:
            print(
                "Error: Simulation needs an instance of a pygame surface / screen!"
            )
            sys.exit()
    '''         
    Public: get_infected(self)

    Description: searches through people and gets amount of infected people

    Params:     self,

    returns:    x: the number of infected people
    '''
    def get_infected(self):
        x = 0
        for i in self.pop:
            if i.state == "infected":
              x +=1

        return x
    '''         
    Public: get_recovered(self)

    Description: searches through people and gets amount of recovered people

    Params:     self,

    returns:    x: the number of recovered people
    '''
    def get_recovered(self):
        x = 0
        for i in self.pop:
            if i.state == "recovered":
              x +=1

        return x
    '''         
    Public: get_susceptible(self)

    Description: searches through people and gets amount of susceptible people

    Params:     self,

    returns:    x: the number of susceptible people
    '''
    def get_susceptible(self):
        x = 0
        for i in self.pop:
            if i.state == "susceptible":
              x +=1

        return x
    '''         
    Public: populateSim(self, population)

    Description: calls other functions from communities to populate the sim

    Params:     self,
                population: the population made for the sim

    returns:    none
    '''
    def populateSim(self, population):
      for i in (self.communities):
          i.fill(self.population_count, population, self.init_infected, self.init_susceptible, self.sprite_group, self.cnumber, self.pop)
    '''         
    Public: simRun(self)

    Description: runs all major functions of sim like printing sprites and moving them

    Params:     self,

    returns:    none
    '''
    def simRun(self):
        # loop through each person and call a move method
        for i in range(len(self.pop)):
           # print(self.pop[i])
            self.pop[i].move()
      
        self.calcR()

        self.sprite_group.draw(self.screen)
    '''         
    Public: calcR(self)

    Description: calculates R

    Params:     self

    returns:    self.R
    '''
    def calcR(self):
      p = self.get_infected()
      sum = 0;
      for i in (self.pop):
          sum += i.encounters
      self.R = sum / p
      return self.R


'''         
Class: FontHelper

Description: Does font stuff

Methods:    __init__()
            printLocation()
            print()

Usage: I'll be honest I don't really know how to work this
'''
class FontHelper:
    #constructor
    def __init__(self,**kwargs):
        self.screen = kwargs.get("screen", None)

        if not isinstance(self.screen, pygame.Surface):
            print("Error, FontHelper needs a 'pygame.Surface' to be passed in when constructed! Aborting.") 
            sys.exit()
        
        self.font_size = kwargs.get("font_size", 20)
        self.font_path = kwargs.get("font_path", './fonts/Roboto-Black.ttf')

        self.color = kwargs.get("color", (255,255,255))
        self.background = kwargs.get("background", (0,0,0))
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)

        self.font = pygame.font.Font(self.font_path, self.font_size)

        self.location = None

    '''         
    Public: printLocation(self,location)

    Description: uhh changes the location maybe?

    Params:     self,
                location: location to print the stuff

    returns:    none
    '''
    def printLocation(self,location):
        '''
        location can be a list with: [top,bottom,left,right]
            top,bottom,left,right = print at respective location in the center (top center, left center, etc.)
            top,right = print at top right corner
            bottom,left = print at bottem left corner
        location can be a tuple with: (x,y)
            gives exact location to print
        '''
        if isinstance(location, list):
            self.location = location
            self.x = -1
            self.y = -1
        
        if isinstance(location, tuple):
            self.x = location[0]
            self.y = location[1]
            self.location = None
    '''         
    Public: print(self,text)

    Description: prints the stuff but don't ask me how idk

    Params:     self,
                text: text to print

    returns:    none
    '''
    def print(self,text):
       
        if isinstance(text, list):
            text = ', '.join(map(str, text))
        elif not isinstance(text,str):
            text = str(text)

        # text to print, antialias, foregroundcolor, backgroundcolor (30, 255, 30), (30, 30, 255)
        text = self.font.render(text, True, self.color, self.background) 
        textRect = text.get_rect()

       # print(self.x,self.y)
        if self.x >= 0 and self.y >= 0:
            textRect.x = self.x
            textRect.y = self.y
        else:
            textRect.x = config["game"]["width"] // 2
            textRect.y = config["game"]["height"] // 2
            if "top" in self.location:
                textRect.top = 0
            if "bottom" in self.location:
                textRect.bottom = config["game"]["height"]
            if "left" in self.location:
                textRect.left = 0           
            if "right" in self.location:
                textRect.right = config["game"]["width"]

        self.screen.blit(text, textRect) 
        #self.screen.blit(t, textRect) 
        
'''         
Class: Person(pygame.sprite.Sprite)

Description: Person in the simulation

Methods:    __init__()
            setDxDy()
            getDxDy()
            changeDirection()
            move()
            checkWalls()
            cdperson()
            collidePerson()
            beinfected()

Usage: Represents each individual person
'''
class Person(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, screen, **kwargs):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.width=config["sprite"]["width"] #initialized by config.json
        self.height=config["sprite"]["height"]
        self.speed=config["sprite"]["speed"]
        self.state = kwargs.get("state", "susceptible") #possibly passed in by creation of a person
        self.community = kwargs.get("community", 1)
        #sets up the colors each thing should be based on the state
        if self.state == "infected":
            self.color = "red"
        elif self.state == "susceptible":
            self.color = "yellow"
        elif self.state == "recovered":
            self.color = "green"
        else:
            self.color = "blue"
        #another screen thing
        self.screen = screen
        self.daysinfected = 0   #keeps track of how long so that they can get better
        self.fh = FontHelper(screen=screen)

        self.collisions = 0
        self.id = config["sim"]["pid"]
        config["sim"]["pid"] += 1
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0 
        self.y2 = 0

        self.encounters = 0 #used to calculate R
        #spawns them in the right quadrant for their community
        if self.community == 0:
            self.x1 = 0
            self.y1 = 0
            self.x2 = config["game"]["width"] // 2
            self.y2 = config["game"]["height"] // 2
        elif self.community == 1:
            self.x1 = config["game"]["width"] // 2
            self.y1 = 0
            self.x2 = config["game"]["width"] 
            self.y2 = config["game"]["height"] // 2
        elif self.community == 2:
            self.x1 = 0
            self.y1 = config["game"]["height"] // 2
            self.x2 = config["game"]["width"] // 2
            self.y2 = config["game"]["height"]
        elif self.community == 3:
            self.x1 = config["game"]["width"] // 2
            self.y1 = config["game"]["height"] // 2
            self.x2 = config["game"]["width"]
            self.y2 = config["game"]["height"]
        
        self.sidescontacted = "side"

        # choose sprite direction
        self.dx = 0
        self.dy = 0
        while self.dx + self.dy == 0:
            self.dx = random.choice([1, -1, 0])
            self.dy = random.choice([1, -1, 0])

        #get the image and customize it to fit sprite
        self.image = pygame.image.load(config["images"][self.color])
        self.image = pygame.transform.scale(self.image,
                                            (self.width, self.height))

        # generate random location
        self.x = random.randint(self.x1,self.x2)
        self.y = random.randint(self.y1,self.y2)
        #rectangle stuff
        self.rect = self.image.get_rect(center=(self.x, self.y))

        if self.rect.top < self.y1:
            self.rect.top = self.y1
        if self.rect.bottom > self.y2:
            self.rect.bottom = self.y2
        if self.rect.left < self.x1:
            self.rect.left = self.x1
        if self.rect.right > self.x2:
            self.rect.right = self.x2

    '''         
    Public: changeDirection(self, sides_contacted)

    Description: changes direction of the sprite based on what side was contacted

    Params:     self,
                sides_contacted: dictionary of sides and if they were contacted

    returns:    none
    '''
    def changeDirection(self, sides_contacted):
        
        if self.sides_contacted["top"] == True:
            self.dy = 1
        if self.sides_contacted["bottom"] == True:
            self.dy = -1
        if self.sides_contacted["left"] == True:
            self.dx = 1
        if self.sides_contacted["right"] == True:
            self.dx = -1
    '''         
    Public: move(self)

    Description: moves sprite in random directions, checks if colliding

    Params:     self,

    returns:    none
    '''
    def move(self):

        self.sides_contacted = self.checkWalls() #checks for walls

        self.changeDirection(self.sides_contacted) #changes direction
        if self.dx < 0:
            self.dx = -1
            self.rect.x -= self.speed
        elif self.dx > 0:
            self.dx = 1
            self.rect.x += self.speed

        if self.dy < 0:
            self.dy = -1
            self.rect.y -= self.speed
        elif self.dy > 0:
            self.dy = 1
            self.rect.y += self.speed

    '''         
    Public: checkWalls(self)

    Description: checks if colliding with a wall

    Params:     self

    returns:    sides: dictionary of walls hit
    '''   
    def checkWalls(self):
        sides = {"top": False, "bottom": False, "left": False, "right": False}

        if self.rect.top <= self.y1:
            sides["top"] = True
            return sides
        if self.rect.left <= self.x1:
            sides["left"] = True
            return sides
        if self.rect.right >= self.x2:
            sides["right"] = True
            return sides
        if self.rect.bottom >= self.y2:
            sides["bottom"] = True
            return sides

        return sides
    '''         
    Public: cdperson(self, other)

    Description: checks which way there are people in cases of social distancing

    Params:     self,
                other: other Person

    returns:    none
    '''
    def cdperson(self, other):
        sides = {"top": False, "bottom": False, "left": False, "right": False}

        if self.rect.top < other.rect.bottom or self.rect.top < other.rect.top:
            sides["top"] = True
        if self.rect.bottom > other.rect.top or self.rect.bottom > other.rect.bottom:
            sides["bottom"] = True
        if self.rect.right < other.rect.left or self.rect.right < other.rect.right:
            sides["right"] = True
        if self.rect.left > other.rect.right or self.rect.left > other.rect.left:
            sides["left"] = True

        self.changeDirection(sides)
    '''         
    Public: collidePerson(self, si, other, c)

    Description: checks if colliding and getting infected by others while moving

    Params:     self,
                si: infection rate
                other: other Person
                c: community to check if they're social distancing

    returns:    none
    '''
    def collidePerson(self, si, other, c):    

        # getting x,y for both sprites
        x1, y1 = self.rect.center
        x2, y2 = other.rect.center
        # distance
        d = math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
        if c.sd == True: #if social distancing in community
            if d <= c.sdd:  #if the distance is <= social distance
               self.cdperson(other)     #move away

        # if distance is less than some threshold , then do something
        if d <= config["sim"]["infection_radius"]*1 and random.random() < si:
            if self.state == "infected" and other.state == "susceptible": #if infecting others
                self.encounters += 1
            if self.state == "susceptible" and other.state == "infected": #if being infected
                self.image = pygame.image.load(config["images"]["red"])
                self.image = pygame.transform.scale(self.image,
                                                (self.width, self.height))
                self.state = "infected"
            
    '''         
    Public: beinfected(self, s, d)

    Description: updates infection and sets state to recovered if it's time

    Params:     self,
                s: time it takes to recover
                d: days just to verify

    returns:    none
    '''
    def beinfected(self, s, d):  
        if self.state == "infected": #update counter
            self.daysinfected += 1
        else:
            return
        
        if self.daysinfected == s:
            self.state = "recovered" #recovery (or death but we're not talking about that)
            self.image = pygame.image.load(config["images"]["green"])
            self.image = pygame.transform.scale(self.image,
                                                (self.width, self.height))        

'''         
Class: Community(population)

Description: a physical boundary and group of people

Methods:    __init__()
            move()
            fill()
            draw()

Usage: helps control people and keeps them together
'''
class Community(population):
    ''' boundaries , local stats
    '''
    def __init__(self, id, s):
                    #  x1 , y1  x2 , y2
        self.bounds = [100,100,300,300]
        self.cid = id
        self.p = population
        self.pop = s.pop
        
        self.sd = config["sim"]["social_distancing"]
        if self.sd == True:
            self.sdd = config["sim"]["social_distance"]
        
    '''         
    Public: move(self)

    Description: could be used to move people specifically in this community

    Params:     self

    returns:    none
    '''
    def move(self):
        for p in population.list:
            p.move(self.bounds)
    '''         
    Public: fill(self, pcount, population, initinfect, initsusc, sprtgrp, cnum, pop)

    Description: fills this community with people

    Params:     self,
                pcount: amount of people that are in the sim
                population: used for the population of community
                initinfect: initial amount of infected people
                initsusc: initial amount of susceptible people
                sprtgrp: group of sprites beloinging to simulation
                cnum: amount of communities
                pop: population

    returns:    none
    '''        
    def fill(self, pcount, population, initinfect, initsusc, sprtgrp, cnum, pop):
        w = (initinfect * pcount)/cnum #get amount of infected to start with
        x = (initsusc * pcount)/cnum #same with susceptible
        for _ in range(int(w)): #add infected people
           p = self.p.add_people(self.p, 1, community=self.cid)
           sprtgrp.add(p)
           pop.append(p)
        for _ in range(int(x)): #add susceptible people
            p = self.p.add_people(self.p, 0, community=self.cid)
            sprtgrp.add(p)
            pop.append(p)

    '''         
    Public: draw(self)

    Description: draws community boundaries

    Params:     self

    returns:    none
    '''   
    def draw(self):    
        rect_width = 2
        # upper left
        pygame.draw.rect(screen,(255,0,0),(0,0,config["game"]["width"]//2,config["game"]["height"]//2),rect_width)
        # upper right
        
        pygame.draw.rect(screen,(255,0,0),(config["game"]["width"]//2,0,config["game"]["width"]//2-rect_width//2,config["game"]["height"]//2),rect_width)
        #lower left
        pygame.draw.rect(screen,(255,0,0),(0,config["game"]["height"]//2,config["game"]["width"]//2,config["game"]["height"]//2),rect_width)
        #lower right
        pygame.draw.rect(screen,(255,0,0),(config["game"]["width"]//2,config["game"]["height"]//2,config["game"]["width"]//2,config["game"]["height"]//2),rect_width)



#__________________________________________________________________________
screen = pygame.display.set_mode( #that screen variable that we've passed into like everything
        [config["game"]["width"], config["game"]["height"]])

 #main function yay
if __name__ == '__main__':    
    pygame.init()
    pygame.display.set_caption('Corona Virus') 
    sprites_list = []
    # Set up the drawing window
    
    pop = population() #make a population
    
    sim = Simulation(screen=screen, #and a simulation
                     width=config["game"]["width"],
                     height=config["game"]["height"],
                     population_count=config["sim"]["population_count"])
    for i in range(config["sim"]["communities"]): #also some communities
        x = Community(i, sim)
        sim.communities.append(x)


    sim.populateSim(pop) #put some people in the sim

    # helps keep game loop running at
    # specific frames per second
    clock = pygame.time.Clock()

    # Run until the user asks to quit
    running = True
    #used in loop so the game loop doesn't travel at light speed
    y = 0
    days = 1

    
    #___ GAME LOOP ____________________________________________________________
    while running:
        r = "R=" #used to print R. why did I put it here? who knows?
        # Fill the background with blackish
        screen.fill((30, 30, 30))
        #the stuff that slows our roll and makes sure we don't go too fast
        y = y + 1
        if y == 20:
            days = days + 1
            y = 0
            print("day: ", days)
            print("R = ", sim.R)
            for i in sim.pop:
                i.beinfected(config["sim"]["infection_duration"], days)
        
        for c in sim.communities:
            c.draw() #draws communities
        
        sim.simRun()   #runs essential sim functions
        # pygame stuff?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for p in sim.pop: #moving and colliding
            p.move()
            for c in sim.communities:
                for sp in c.pop:
                   if not p == sp:  #and sp.state == 'infected':
                      p.collidePerson(config["sim"]["infection_rate"], sp, c)

        prnt = FontHelper(screen=screen) #this is probably necessary

        #prints days
        text = prnt.font.render(str(days), True,   (30, 255, 30), (30, 30, 255)) 
        # # bounding rectangle
        textRect = text.get_rect()

        # # set where to position the text
        textRect.right = config["game"]["width"]
        textRect.top = config["game"]["height"]

        # # prints text 
        screen.blit(text, textRect) 

        r += str(sim.R)
        prnt.print(str(r))

        #___END CONTROL SIMULATION_____________________________________________________________

        # This keeps game loop running at a constant FPS
        clock.tick(config["game"]["fps"])  # FPS = frames per second

        # Count number of loops game runs (careful, this number could get LARGE)
        config["game"]["loop_count"] += 1

        # Flip the display (refresh the screen)
        pygame.display.flip()

#___ END GAME LOOP ____________________________________________________________
# Done! Time to quit.
    pygame.quit()
    