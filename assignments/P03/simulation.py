#!/usr/bin/env python3

# Import and initialize the pygame library
import pygame
import random
import math
import sys,os

# list of colors
colors = ["blue", "light_blue", "yellow", "orange", "green"]

config = {
    "sprite": {
        "width": 8,
        "height": 20,
        "speed": 2,
    },
    "images": {
        "blue": "./images/person_blue_64x64.png",
        "light_blue": "./images/person_light_blue_64x64.png",
        "red": "./images/person_red_64x64.png",
        "white": "./images/person_white_64x64.png",
        "yellow": "./images/person_yellow_64x64.png",
        "orange": "./images/person_orange_64x64.png",
        "green": "./images/person_green_64x64.png",
        "black": "./images/person_black_64x64.png"
    },
    "game": {
        "width": 800,
        "height": 625,
        "day": 0,
        "fps": 40,
        "loop_count": 0
    },
    "sim": {
        "social_distancing": False,
        "social_distance": 20,
        "infection_radius": 10,
        "infection_rate": .75,
        "population_count": 300,
        "pid": 1,
        "communities": 4,
        "initial_infected": .05,
        "initial_susceptible": .95,
        "infection_duration": 10
    }
}
states = ["susceptible", "infected", "recovered"]


class population(object):
    
    def __init__(self):
        self.list = []
        self.count = 0
    
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
       
    
    def get_infected(self, Person):
        for i in self.list:
            self.list.count(Person.state == "infected")


class Simulation:
    def __init__(self, **kwargs):
        self.pop = []
        self.game_width = config["game"]["width"]
        self.game_height = config["game"]["height"]
        self.screen = kwargs.get("screen", None)
        self.communities = []
        self.sprite_group = pygame.sprite.Group()
        self.infection_radius = config["sim"]["infection_radius"]
        self.infection_rate = config["sim"]["infection_rate"]
        self.population_count = config["sim"]["population_count"]
        self.init_infected = config["sim"]["initial_infected"]
        self.init_susceptible = config["sim"]["initial_susceptible"]
        self.cnumber = config["sim"]["communities"]
        self.R = 0

        #print(self.screen)

        if self.screen == None:
            print(
                "Error: Simulation needs an instance of a pygame surface / screen!"
            )
            sys.exit()

   # def getR(self):

    def populateSim(self, population):
    #  print("in populate")

      for i in (self.communities):
          i.fill(self.population_count, population, self.init_infected, self.init_susceptible, self.sprite_group, self.cnumber, self.pop)

    def makeCommunities(self, community):
        print("in make comm")
        for i in range(self.cnumber):
            c = community
            print(c.cid)
            self.communities.append(c)
            c.cid += 1

    def simRun(self):
        # loop through each person and call a move method
        for i in range(len(self.pop)):
           # print(self.pop[i])
            self.pop[i].move()
            for j in range(len(self.pop)):
                if self.pop[i] != self.pop[j]:
                    collided = self.pop[i].checkCollide(
                        self.pop[j])
                    if collided:
                        dx, dy = self.pop[i].getDxDy()
                        self.pop[j].setDxDy(dx * -1, dy * -1)
                        

        self.sprite_group.draw(self.screen)

class FontHelper:
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
        

class Person(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, screen, **kwargs):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.width=config["sprite"]["width"]
        self.height=config["sprite"]["height"]
        self.speed=config["sprite"]["speed"]
        self.state = kwargs.get("state", "susceptible")
        self.community = kwargs.get("community", 1)

        if self.state == "infected":
            self.color = "red"
        elif self.state == "susceptible":
            self.color = "yellow"
        elif self.state == "recovered":
            self.color = "green"
        else:
            self.color = "blue"

        self.screen = screen
        self.daysinfected = 0
        self.fh = FontHelper(screen=screen)

        self.collisions = 0
        self.id = config["sim"]["pid"]
        config["sim"]["pid"] += 1
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0 
        self.y2 = 0

        self.socialdistance = 0
        
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
        
        self.fh.printLocation((self.x1,self.y1))

        self.speed = 5

        # choose sprite direction
        self.dx = 0
        self.dy = 0
        while self.dx + self.dy == 0:
            self.dx = random.choice([1, -1, 0])
            self.dy = random.choice([1, -1, 0])

        # random.random() returns a number between 0 and 1
        # random.randint(start,end)
        # random.choice(list_of_items) choose a random item

        self.image = pygame.image.load(config["images"][self.color])
        self.image = pygame.transform.scale(self.image,
                                            (self.width, self.height))

        # generate random location
        self.x = random.randint(self.x1,self.x2)
        self.y = random.randint(self.y1,self.y2)

        self.rect = self.image.get_rect(center=(self.x, self.y))

        if self.rect.top < self.y1:
            self.rect.top = self.y1
        if self.rect.bottom > self.y2:
            self.rect.bottom = self.y2
        if self.rect.left < self.x1:
            self.rect.left = self.x1
        if self.rect.right > self.x2:
            self.rect.right = self.x2


    def setDxDy(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def getDxDy(self):
        return (self.dx, self.dy)

    def changeDirection(self, sides_contacted):
        if sides_contacted == "top":
            self.dy = 1
        if sides_contacted == "bottom":
            self.dy = -1
        if sides_contacted == "left":
            self.dx = 1
        if sides_contacted == "right":
            self.dx = -1

    def move(self):

        sides_contacted = self.checkWalls()

        self.changeDirection(sides_contacted)
     
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

        location = f"x:{self.rect.x},y:{self.rect.y}"
        self.fh.print(location)
    
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

    def collidePerson(self, si, other, sd):
        """
        Public: collide(self, si, other, sd = 6)
        Description: checks if colliding with other person and if they get infected
        Params: self, si (variable for infection rt), other (other person), sd (social distance)
        Returns: none
        """
        # print("checking collide")
        if not other.state == "infected":
             return

        # getting x,y for both sprites
        x1, y1 = self.rect.center
        x2, y2 = other.rect.center
        # distance
        d = math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
        
        if d < sd:
            self.changeDirection(other)
            print(f"d:{d} collision:{self.width*1.2}")

        # if distance is less than some threshold , then do something
        if d < config["sim"]["infection_radius"] and random.randrange(1) < si:
            self.image = pygame.image.load(config["images"]["red"])
            self.image = pygame.transform.scale(self.image,
                                                (self.width, self.height))
            self.state = "infected"

    def checkCollide(self, other):
        sides_contacted = {
            "top": False,
            "bottom": False,
            "left": False,
            "right": False
        }

        if self.rect.colliderect(other.rect):
            
            if self.rect.top < other.rect.top:
                sides_contacted["bottom"] = True
                self.rect.y -= abs(self.rect.y - other.rect.y) // 8
            if self.rect.left < other.rect.left:
                sides_contacted["right"] = True
                self.rect.x -= abs(self.rect.x - other.rect.x) // 8
            if self.rect.right > other.rect.right:
                sides_contacted["left"] = True
                self.rect.x += abs(self.rect.x - other.rect.x) // 8
            if self.rect.bottom > other.rect.bottom:
                sides_contacted["top"] = True
                self.rect.y += abs(self.rect.y - other.rect.y) // 8

            self.changeDirection(sides_contacted)

            return True

        return False

    def beinfected(self, s, d):
        """
        Public: beinfected(self, s, d)
        Description: keeps track of days infected and controls recovery
        Params: self, s(the days before recovery), d(days passed in game loop)
        Returns: none
        """
        print("checking infection")
        if self.state == "infected":
            self.daysinfected += 1
        else:
            return
        
        if self.daysinfected == s:
            self.state = "recovered"
            self.image = pygame.image.load(config["images"]["green"])
            self.image = pygame.transform.scale(self.image,
                                                (self.width, self.height))        


def MyGamePrint(**kwargs):
        screen = kwargs.get("screen", None)
        font_path = kwargs.get("font_path","./fonts/LeagueSpartan-Bold.otf")
        text = kwargs.get("text",None)
        color = kwargs.get("color",(0,0,0))
        bgcolor = kwargs.get("bgcolor",(255,255,255))
        x = kwargs.get("x",0)
        y = kwargs.get("y",0)

        if not isinstance(screen, pygame.Surface):
            print("Error, FontHelper needs a 'pygame.Surface' to be passed in when constructed! Aborting.") 
            sys.exit()

        if not os.path.isfile(font_path):
            print("Error: Font path is invalid! ... Exiting...")
            sys.exit()

        #                            text          antialias   foreground     background
        text = font.render(text, True,   color, bgcolor) 

        # bounding rectangle
        textRect = text.get_rect()

        # set where to position the text
        textRect.left = x
        textRect.top = y

        # prints text 
        screen.blit(text, textRect) 


class Community(population):
    ''' boundaries , local stats
    '''
    def __init__(self, id):
                    #  x1 , y1  x2 , y2
        self.bounds = [100,100,300,300]
        self.cid = id
        self.p = population
        self.sd

    def travel(self):
        i = random.randint(0,len(self.people))
        p = self.people[i]
        del self.people[i]
        return p

    def move(self):
        for p in population.list:
            p.move(self.bounds)
        
    def fill(self, pcount, population, initinfect, initsusc, sprtgrp, cnum, pop):
        print(self.cid)
        w = (initinfect * pcount)/cnum
        x = (initsusc * pcount)/cnum
        print(w, x)
        for _ in range(int(w)):
           p = self.p.add_people(self.p, 1, community=self.cid)
           sprtgrp.add(p)
           pop.append(p)
        for _ in range(int(x)):
            p = self.p.add_people(self.p, 0, community=self.cid)
            sprtgrp.add(p)
            pop.append(p)

    def setsd(self, sim):
       if config["sim"]["social_distancing"] == True:
          for i in sim.pop:
              i.socialdistance = config["sim"]["social_distance"]


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
screen = pygame.display.set_mode(
        [config["game"]["width"], config["game"]["height"]])


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Corona Virus') 
    sprites_list = []
    # Set up the drawing window

    pop = population()
    
    sim = Simulation(screen=screen,
                     width=config["game"]["width"],
                     height=config["game"]["height"],
                     population_count=config["sim"]["population_count"])
    for i in range(config["sim"]["communities"]):
        x = Community(i)
        sim.communities.append(x)


    sim.populateSim(pop)

    # helps keep game loop running at
    # specific frames per second
    clock = pygame.time.Clock()

    # Run until the user asks to quit
    running = True
    y = 0
    days = 0
    #___ GAME LOOP ____________________________________________________________
    while running:
        # Fill the background with blackish
        # Do not do this after you draw sprites!
        screen.fill((30, 30, 30))
        y = y +1
        if x == 30:
            days = days + 1
            x = 0
            print("day: ", days)
            for i in sim.pop:
                i.beinfected(config["sim"]["infection_duration"], days)
        for c in sim.communities:
            c.draw()
        
        sim.simRun()   
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for p in sim.pop:
            p.move()
            for sp in sim.pop:
             #   if not p == sp:  #and sp.state == 'infected':
                p.collidePerson(config["sim"]["infection_rate"], sp, p.sd)

        # #                            text          antialias   foreground     background
        # #text = font.render(str(len(sim.population)), True,   (30, 255, 30), (30, 30, 255)) 
        # text = font.render(str(len(sim.population)), True,   (255, 0, 0), (255, 255, 255)) 

        # # bounding rectangle
        # textRect = text.get_rect()

        # # set where to position the text
        # textRect.right = config["game"]["width"]
        # textRect.bottom = config["game"]["height"]

        # # prints text 
        # screen.blit(text, textRect) 
        #MyGamePrint(screen=screen,text=str(len(sim.population)),color=(0,255,0),bgcolor=(0,0,255),x=config["game"]["width"]//2,y=config["game"]["height"]//2)
        # fh1.print(str(len(sim.population)))

        # fh2.print(str(len(sim.population)))

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