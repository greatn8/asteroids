#asteroids game
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("https://dl.dropboxusercontent.com/u/73216150/splash2.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("https://dl.dropboxusercontent.com/u/73216150/double_shipcordell2.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 75)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
 
# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("https://dl.dropboxusercontent.com/u/73216150/asteroid_blue2.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

#sounds
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        
        # update angle
        self.angle += self.angle_vel
      
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        global a_missile
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 10, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
    def get_pos(self):
        return self.pos    
    def get_radius(self):
        return self.radius
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.lifespan = info.get_lifespan()
        self.age = 0
        self.animated = info.get_animated()
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + (self.age * self.image_size[0]), self.image_center[1]], self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        remove = False
        # update angle
        self.angle += self.angle_vel
        self.age += 1
        if self.age > self.lifespan:
            remove = True 
            return remove
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
    
    def get_pos(self):
        return self.pos
    def get_radius(self):
        return self.radius
    def collisiontest(self, other_object):
        collision = False
        if dist(self.get_pos(), other_object.get_pos()) < (self.get_radius() + other_object.get_radius()):
            collision = True
        return collision    
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started,score,lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
    score = 0
    lives = 3
    soundtrack.play()
def draw(canvas):
    global time, started,lives,score,rock_group
   
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives Remaining:", [40, 50], 22, "White")
    canvas.draw_text("Commision Earnt:", [580, 50], 22, "White")
    canvas.draw_text(str(lives), [40, 80], 22, "White")
    canvas.draw_text("$" + str(score), [580, 80], 22, "White")

    # draw ship and sprites
    my_ship.draw(canvas)
    a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 10, missile_image, missile_info, missile_sound)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    lives -= group_collide(rock_group, my_ship)
    score += group_group_collide(rock_group, missile_group)
    process_sprite_group(explosion_group, canvas)
    a_missile.update()
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    # draw splash screen if live < 0
    
    if lives < 0:
        lives = 0
        started = False
        soundtrack.rewind()
        soundtrack.pause()
        rock_group = set()
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
       
#take my rock_group set and call update and draw methods for each sprite in the set
def process_sprite_group(sprites,canvas):   
     for sprite in set(sprites): 
        sprite.draw(canvas)
        if sprite.update() == True:
            sprites.remove(sprite)   
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock,rock_group
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    rock_vel = [random.randrange(-3,3) * 0.9, random.randrange(-3,3)*0.9] 
    rock_avel = random.random() * .2 - .1
    a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
    if len(rock_group) < 50 and started:
         if (dist(a_rock.get_pos(), my_ship.get_pos())) >(a_rock.get_radius() + (1.5 * my_ship.get_radius()) + 100):
            rock_group.add(a_rock)
# function to test for group colliding with 1 object     
def group_collide(group, other_object):
    
    collisions = 0
    for item in set(group):
        if item.collisiontest(other_object):
            collisions += 1
            explosion = Sprite(item.get_pos(),[0, 0], 0, 0, explosion_image,
                               explosion_info, explosion_sound)
            explosion_group.add(explosion)
            group.remove(item)            
    return collisions
#function to test for any object in a group colliding with any object in group
def group_group_collide(group1, group2):
    
    collisions = 0
    for item in set(group1):
        if group_collide(group2, item) > 0:
            collisions += 1 + random.randrange(10,100)
            group1.remove(item)
    return collisions            
# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
rock_group = set()
missile_group = set()
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, .1, asteroid_image, asteroid_info)
explosion_group = set()


# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
label = frame.add_label('Controls:')
label = frame.add_label('Left & Right to Rotate')
label = frame.add_label('Forward to Move Forward')
label = frame.add_label('Spacebar to Shoot')
timer = simplegui.create_timer(610.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
