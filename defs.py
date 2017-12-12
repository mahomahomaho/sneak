import math

# level specific data
map_size = (1000, 1000)
num_stones = 5
num_rats = 20


# characters
person_speed = 400
rat_speed =  (80, 160)
rat_turn_angle = math.radians(4)
max_courage = 4.0
min_contact_to_get_courage = 2

# gameplay things
freeze_time = 3
grace_time = 2
numrats_change = 3, 1.1  # on advance level, add, multipiler
numstones_change = 1, 1  # on advance level
mapsize_change = 200, 1  # on advance level
lives_add = 2
max_lives = 6
shout_time = 1.8

# physics
coltype_person = 1
coltype_rat = 2
coltype_stone = 3

force_threshold = 1.5
shout_repulsion = 15000

# steering
steering_min_dist = 0.3 # FIXME: remove this setting? 
angle_step = math.radians(4)

# misc
inf = 1.0e10  # potential in place/tile of attraction/repulsion
