## Pandemic Simulation Usage:

A pandemic simulation which includes models of people using the SIR model that can be infected, susceptible, or recovered. Calculates R based on the amount of infections the average infected person makes.
Update variables in config.json to alter simulation environment.
### Changeable variables include:
 * #### sprite:width and height
    integers, could be used to change the size of the sprites if you really wanted to I guess
 * #### sprite:speed
    integer, if you wanted to make everyone go faster. Starts at 2.
 * #### image files
    if you wanted to get really spicy you could upload images into the images folder and replace the file names with the ones paired with each color. Only the images under Red(infected), Yellow(susceptible), and Green(recovered) are actually utilized in the simulation
 * #### game:height and width
    integers, again, if for some reason you want to change the size of things then change these. I personally think 800x625 is good though
 * #### game:fps
    integer, more technical, can be used to make the simulation run faster/slower
 * #### game:loop_count
    integer, begin at 0, used in game loop to increment
 * #### sim:social_distancing
    bool, set to True/False to alter whether or not the people practice social distancing
 * #### sim:social_distance
    integer, if social_distancing set to True, this is the distance apart they will attempt to stay
 * #### sim:infection_radius
    integer, this is the distance away someone has to be to be able to possibly contract the disease
 * #### sim:infection_rate
    double, the probability of infection when people are within the infection radius. Can be changed to represent better hygiene or masks perhaps
 * #### sim:population_count
    integer, the amount of people total contained in the simulation. This includes those that start out already infected
 * #### sim:pid
    integer, a technical component used to assign all the people an ID number that doesn't actually do anything in the simulation
 * #### sim:communities
    integer, number of communities in the sim, I find 4 to be preferable, mostly because I had a hard enough time getting pygame to draw 4 I had no idea how to get it to work with a variable amount so you should definitely not touch this one
 * #### sim:initial_infected
    double, the percentage of the population that starts out as infected. You probably don't want to reduce this or the population_count to a very low number, unless you want nothing to really happen in the simulation
 * #### sim:initial_susceptible
    double, percentage of the population that is susceptible to the infection in the beginning. Best to keep this the percent thaat isn't infected
 * #### sim:infection_duration
    integer, the amount of days it takes before an infected person becomes recovered and is unable to infect others or become infected

