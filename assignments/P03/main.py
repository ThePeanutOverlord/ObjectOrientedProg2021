"""                   
 Author:           Paige Champagne
 Email:            paigechamp@gmail.com
 Label:            program 3 (2 if you want to be technical)
 Title:            Pandemic Simulation
 Course:           CMPS 2143
 Semester:         Spring 2020

 Description:
          this is a simulation of a pandemic using pygame

 Usage:
       Used to visualize a pandemic situation. parameters are able to be adjusted

 Files:           main.py
                    /images/pac_red_30x30.png
                    /images/pac_yellow_30x30.png
                    /images/pac_green_30x30.png

"""


#!/usr/bin/env python3

# Import and initialize the pygame library
import pygame
import random
import math

class Config:
    """
    Class: Config
    Description: Some data used
    no methods
    used to load parts of the program originally.
    """
    #no constructor
    width = 1024
    height = 768
    sprite_images = {
        "blue" : "./images/pac_blue_30x30.png",
        "light_blue" : "./images/pac_light_blue_30x30.png",
        "red" : "./images/pac_red_30x30.png",
        "white" : "./images/pac_white_30x30.png",
        "yellow" : "./images/pac_yellow_30x30.png",
        "orange" : "./images/pac_orange_30x30.png",
        "green" : "./images/pac_green_30x30.png"
    }
    social_distancing = False
    infection_radius = 10
    infection_rate = .2
    population_count = 10
    sprite_width = 15
    sprite_height = 15
    sprite_speed = 2

Config.width = 400
Config.height = 400
Config.pid = 1
Config.myClock = 1

states = ["susceptible", "infected", "recovered"]


class population(object):
    """
    Class: population
    Description: holds the people for the simulation
    Methods: __init__()
            add_people()
            get_infected()
    Usage: puts all the people in a list and calculates stats
    """
    def __init__(self):
        self.list = []
        self.count = 0
    
    def add_people(self, Person):
        self.list.append(Person)
        sprites_list.add(self.list[-1])
        self.count += 1
    
    def get_infected(self, Person):
        for i in self.list:
            self.list.count(Person.state == "infected")


#__________________________________________________________________________


# pygame thing
class Person(pygame.sprite.Sprite):
    """
    Class: Person
    Description: a sprite that moves around, can be infected and infect others
    Methods: __init__()
            move()
            beinfected()
            check_bounds()
            determineSides()
            changeDirection()
            collide()
    Usage: represents a person in our sim
    """
    def __init__(self,
                 screen_width,
                 screen_height,
                 s,
                 color,
                 width = 15,
                 height = 15,
                 speed=1,inx=None,iny=None):
        """ Constructor. Pass in the color of the block,
        and its size. """
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.id = Config.pid
        Config.pid +=1


        self.state = states[s]

        # screen width and height used to know
        # when to change direction at edge of screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        # size of our sprite
        self.width = width
        self.height = height

        # direction x and direction y
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])

        self.daysinfected = 0
        speeds = range(1,6)
        # pixels per game loop
        #self.speed = random.choice([1,7])
        self.speed = speed
        self.original_speed = speed

        self.color = color

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.

        # pygame thing
        self.image = pygame.image.load(Config.sprite_images[self.color])
        # pygame thing
        self.image = pygame.transform.scale(self.image,
                                            (self.width, self.height))

        # Fetch the rectangle object that has the dimensions of the image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y

        if inx is None:
            # creates a random location between bounds of screen size
            x = int(random.random() * self.screen_width)
        else:
            x = inx

        if iny is None:
            # creates a random location between bounds of screen size
            y = int(random.random() * self.screen_height)
        else:
            y = iny

        # pygame thing
        self.rect = self.image.get_rect(center=(x, y))

        self.lastCollisionTime = 0

    def move(self):
    """
    Public: move(self)
    Description: moves the sprite
    Params: self
    Returns: none
    """        
        self.check_bounds()

        # add speed pixels to current location
        # multiplied by direction


        if self.lastCollisionTime > 0 and Config.myClock - self.lastCollisionTime > 2:
           # print(f"current-time = {Config.myClock} last: {self.lastCollisionTime}")
            self.speed = self.original_speed
            self.lastCollisionTime = 0
           # print(f"speed: {self.speed}")

        # pygame thing
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy
    
    def beinfected(self, s, d):
    """
    Public: beinfected(self, s, d)
    Description: keeps track of days infected and controls recovery
    Params: self, s(the days before recovery), d(days passed in game loop)
    Returns: none
    """
        if self.state == "infected":
            self.daysinfected += 1
        
        if self.daysinfected == s:
            self.state = "recovered"
            self.image = pygame.image.load(Config.sprite_images["green"])
            self.image = pygame.transform.scale(self.image,
                                                (self.width, self.height))

    def check_bounds(self):
    """
    Public: check_bounds(self)
    Description: keeps people from going out of bounds
    Params: self
    Returns: none
    """
        # if our x goes less than zero or more than width negate dx.
        if self.rect.x >= self.screen_width-self.width or self.rect.x <= 0:
            self.dx *= -1

        #
        if self.rect.y >= self.screen_height-self.width or self.rect.y <= 0:
            self.dy *= -1

    def determineSides(self, other):
    """
    Public: determineSides(self, other)
    Description: makes sides for the character's hitbox
    Params: self
    Returns: d (the box)
    """
        d = []
        if self.rect.midtop[1] < other.rect.midtop[1]:
            d.append("top")
        if self.rect.midleft[0] < other.rect.midleft[0]:
            d.append("left")
        if self.rect.midright[0] > other.rect.midright[0]:
            d.append("right")
        if self.rect.midbottom[1] > other.rect.midbottom[1]:
            d.append("bottom")

        return d
    
    def changeDirection(self,other):
    """
    Public: changeDirection(self,other)
    Description: makes person change direction if they collide with the sides
    Params: self, other
    Returns: none
    """
        sides = self.determineSides(other)

        self.lastCollisionTime = Config.myClock

        #print(self.lastCollisionTime)
        
        self.speed *= .5

        #print(f"{self.color} {sides}")
        if "right" in sides:
            self.dx = -1
            self.rect.x -= 5
        if "left" in sides:
            self.dx = 1
            self.rect.x += 5
        if "top" in sides:
            self.dy = -1
            self.rect.y -= 5
        if "bottom" in sides:
            self.rect.y += 5
            self.dy = 1


    def collide(self, si, other, sd = 6):
    """
    Public: collide(self, si, other, sd = 6)
    Description: checks if colliding with other person and if they get infected
    Params: self, si (variable for infection rt), other (other person), sd (social distance)
    Returns: none
    """
        if not other.state == states[1]:
             return

        # getting x,y for both sprites
        x1, y1 = self.rect.center
        x2, y2 = other.rect.center
        # distance
        d = math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
        
        if d < sd:
            self.changeDirection(other)
            #print(f"d:{d} collision:{self.width*1.2}")

        # if distance is less than some threshold , then do something
        if d < self.width*1 and random.random() < si.beta:
            self.image = pygame.image.load(Config.sprite_images["red"])
            self.image = pygame.transform.scale(self.image,
                                                (self.width, self.height))
            self.state = "infected"

#__________________________________________________________________________
# adjust everything in person class to take in these variables
class Community(population):
    """
    Class: Community(population)
    Description: a formation of a population inside the sim
    Methods: __init__()
            travel()
            move()
    Usage: represents a physical bounding of a population
    """
    def __init__(self):
                    #  x1 , y1  x2 , y2
        self.bounds = [100,100,300,300]

    def travel(self):
    """
    Public: travel(self)
    Description: sets where people should travel to
    Params: self
    Returns: p (array of people)
    """
        i = random.randint(0,len(self.people))
        p = self.people[i]
        del self.people[i]
        return p

    def move(self):
    """
    Public: move(self)
    Description: moves a person
    Params: self
    Returns: none
    """
        for p in population.list:
            p.move(self.bounds)


class sim(object):
    """
    Class: sim
    Description: controls the variables for the simulation
    Methods: setters and getters for these variables:
        self.communities = []
        self.beta = .25 # probability of infection
        self.gamma = 14 # recovery time
        self.nu = 9 # time until treated
        self.init_susceptible = 1 # % of pop initially susceptible
        self.init_infected = 2 # num of pop initially infected
        self.init_recovered = 0 # % of pop initially removed
        self.iterations = 365 # days to run sim
        self.hospital_capacity = .10 # % of pop hospital can hold
        self.fatality_rt = .3 # % of cases that are fatal
        self.self_qt_rt = .50 # % of pop that self quarantines
        self.self_qt_strct = .25 # % of people who might not
        self.encounters_per_day = 10 # num of encounters / day
        self.travel_radius = 5 # distance individuals travel
        self.transmission_rt = .4 # probability of transmission
        self.days_incubation = 7 # days before symptoms
        self.days_symptoms = 7 # days with symptoms
        self.pop_size = 50 # population size
    Usage: used to change/control variables that run the sim
    """
    def __init__(self):
        self.communities = []
        self.beta = .25 # probability of infection
        self.gamma = 14 # recovery time
        self.nu = 9 # time until treated
        self.init_susceptible = 1 # % of pop initially susceptible
        self.init_infected = 2 # num of pop initially infected
        self.init_recovered = 0 # % of pop initially removed
        self.iterations = 365 # days to run sim
        self.hospital_capacity = .10 # % of pop hospital can hold
        self.fatality_rt = .3 # % of cases that are fatal
        self.self_qt_rt = .50 # % of pop that self quarantines
        self.self_qt_strct = .25 # % of people who might not
        self.encounters_per_day = 10 # num of encounters / day
        self.travel_radius = 5 # distance individuals travel
        self.transmission_rt = .4 # probability of transmission
        self.days_incubation = 7 # days before symptoms
        self.days_symptoms = 7 # days with symptoms
        self.pop_size = 50 # population size

    # I'm not commenting every one of these methods
    def set_beta(self, b):
        self.beta = b

    def get_beta(self):
        return self.beta
      
    def set_gamma(self, g):
        self.gamma = g

    def get_gamma(self):
        return self.gamma

    def set_nu(self, n):
        self.nu = n

    def get_nu(self):
        return self.nu

    def set_init_susceptible(self, i):
        self.init_susceptible = i

    def get_init_susceptible(self):
        return self.init_susceptible

    def set_init_infected(self, i):
        self.init_infected = i

    def get_init_infected(self):
        return self.init_infected

    def set_init_recovered(self, r):
        self.init_recovered = r

    def get_init_recovered(self):
        return self.init_recovered

    def set_iterations(self, i):
        self.set_iterations = i

    def get_iterations(self):
        return self.iterations

    def set_hospital_capacity(self, h):
        self.hospital_capacity = h

    def get_hospital_capacity(self):
        return self.hospital_capacity
    
    def set_fatality_rt(self, f):
        self.fatality_rt = f

    def get_fatality_rt(self):
        return self.fatality_rt

    def set_self_qt_rt(self, q):
        self.self_qt_rt = q

    def get_self_qt_rt(self):
        return self.self_qt_rt

    def set_self_qt_strct(self, q):
        self.self_qt_strct = q

    def get_self_qt_strct(self):
        return self.self_qt_strct

    def set_encounters_per_day(self, e):
        self.encounters_per_day = e

    def get_encounters_per_day(self):
        return self.encounters_per_day

    def set_travel_radius(self, t):
        self.travel_radius = t

    def get_travel_radius(self):
        return self.travel_radius

    def set_transmission_rt(self, t):
        self.transmission_rt = t

    def get_transmission_rt(self):
        return self.transmission_rt

    def set_days_incubation(self, d):
        self.days_incubation = d

    def get_days_incubation(self):
        return self.days_incubation

    def set_days_symptoms(self, d):
        self.days_symptoms = d

    def get_days_symptoms(self):
        return self.days_symptoms

    def set_pop_size(self, p):
        self.pop_size = p

    def get_pop_size(self):
        return self.pop_size


#__________________________________________________________________________

if __name__=='__main__':
    days = 0 # counter for days
    x = 0 # counter for uh a day extender? look inside the game loop for info
    pygame.init()
    clock = pygame.time.Clock()
    # Set up the drawing window
    screen = pygame.display.set_mode([Config.width, Config.height])
    s = sim() # instance of simulation
    # sprites should be in a sprite group
    sprites_list = pygame.sprite.Group()
    
    # a list to hold all of our people sprites
    pop = population() #instance of population

    # list of colors
    colors = ["blue", "light_blue", "white", "yellow","orange","red"]
    
    #speeds = [x for x in range(1,3)] #pythonic
    for i in range(s.init_infected):
        pop.add_people(Person(Config.width, Config.height, 1, colors[5],Config.sprite_width,Config.sprite_height,Config.sprite_speed))
    # loop N times
    for i in range(s.pop_size - s.init_infected):
        # add a "person" to our list of people
        # create an "instance" of our class
        pop.add_people(Person(Config.width, Config.height, 0, colors[3],Config.sprite_width,Config.sprite_height,Config.sprite_speed))

    # Run until the user asks to quit
    running = True
    
    ## this is our simulation object??
    while running:
        x = x +1
        if x == 24: # x is hours! every game loop is one hour so that the days don't go super fast
                    # I thought that was a cool idea
            days = days + 1
            x = 0
            print("day: ", days)
            for i in range(s.pop_size):
                pop.list[i].beinfected(s.gamma, days)
           
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                #print(pos)
                pop.add_people(Person(Config.width, Config.height, 1, colors[5],15,15,1,pos[0],pos[1])) #random.choice(speeds)


        # Fill the background with blackish
        screen.fill((30, 30, 30))

        sprites_list.draw(screen)

        # loop through each person
        # and call a move method
        for p in pop.list:
            p.move()

            # loop through each person
            # and check for collision (could be better)
            for sp in pop.list:
                if not p == sp:  #and sp.state == 'infected':
                    p.collide(s, sp, 25)

        # Flip the display
        pygame.display.flip()

        #Number of frames per secong e.g. 60
        clock.tick(40)
      
        Config.myClock += 1
    
    # Done! Time to quit.
    if days == s.iterations:
        pygame.QUIT()