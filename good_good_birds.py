import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from vpython import *
from time import *


vrange = 99
ratio_co = 10
ratio_al = 99
ratio_sep = 99
min_distance = 25
count = 100
width = 400
height = 400
length = 400
max_steer = 0.1
max_velocity = 15

interval = 0.05
speed = 5
egboids_position = np.zeros((3, count))

xaxis1 = box(pos = vector(width/2,0,0), length = width, width = 1, height = 1, color = color.red)
xaxis2 = box(pos = vector(width/2,height,0), length = width, width = 1, height = 1, color = color.red)
xaxis3 = box(pos = vector(width/2,0,length), length = width, width = 1, height = 1, color = color.red)
xaxis4 = box(pos = vector(width/2,height,length), length = width, width = 1, height = 1, color = color.red)

yaxis1 = box(pos = vector(0,height/2,0), length = 1, width = 1, height = height, color = color.red)
yaxis2 = box(pos = vector(0,height/2,length), length = 1, width = 1, height = height, color = color.red)
yaxis3 = box(pos = vector(width,height/2,0), length = 1, width = 1, height = height, color = color.red)
yaxis4 = box(pos = vector(width,height/2,length), length = 1, width = 1, height = height, color = color.red)

zaxis1 = box(pos = vector(0,0,length/2), length = 1, width = length, height = 1, color = color.red)
zaxis2 = box(pos = vector(width,0,length/2), length = 1, width = length, height = 1, color = color.red)
zaxis3 = box(pos = vector(0,height,length/2), length = 1, width = length, height = 1, color = color.red)
zaxis4 = box(pos = vector(width,height,length/2), length = 1, width = length, height = 1, color = color.red)

for i in range(count):
    egboids_position[0, i] = np.random.rand(1) * width
    egboids_position[1, i] = np.random.rand(1) * height
    egboids_position[2, i] = np.random.rand(1) * length
egboids_velocity = np.zeros((3, count))
for i in range(count):
    egboids_velocity[0, i] = np.random.uniform(-1, 1) * 3
    egboids_velocity[1, i] = np.random.uniform(-1, 1) * 3
    egboids_velocity[2, i] = np.random.uniform(-1, 1) * 3

class Boid:

    def __init__(self, x, y, z, vx, vy, vz):
        self.position = np.array([x, y, z])
        self.velocity = np.array([vx, vy, vz])  # 隨機初始化速度

    '''boid=Boid(2,3)
    print(boid.velocity)'''

    def border(self):  #兩側畫面相接(不會飛出去)
        x, y, z = self.position[0], self.position[1], self.position[2]
        x = (x + width) % width
        y = (y + height) % height
        z = (z + length) % length
        self.position[0], self.position[1], self.position[2] = x, y ,z

    def cohesion(self, flock):
        steer = np.array([0, 0, 0], dtype=np.float64)
        num = 0
        for boid in flock.boids:
            distance = np.linalg.norm(boid.position - self.position)
            if 0 < distance < vrange:
                steer += boid.position - self.position
                num += 1
        if num > 0:
            steer /= num
        else:
            steer = np.array([0, 0,0])

        return steer

    def alignment(self, flock):
        avg_velocity = np.array([0, 0, 0], dtype=np.float64)
        num = 0
        #vector=np.linalg.norm(avg_velocity - self.velocity)
        for boid in flock.boids:
            distance = np.linalg.norm(boid.position - self.position)
            if 0 < distance < vrange:
                avg_velocity += boid.velocity
                num += 1
        if num != 0:
            steer = avg_velocity / num
        else:
            steer = np.array([0, 0, 0])

        return steer

    def separation(self, flock):
        steer = np.zeros(3)
        num = 0
        for boid in flock.boids:
            distance = np.linalg.norm(boid.position - self.position)
            if 0 < distance < min_distance:
                steer -= (boid.position - self.position) / distance / distance
                num += 1
        if num != 0:
            steer /= num
        else:
            steer = np.array([0, 0, 0])
        return steer

    def update(self, flock):
        steer = self.cohesion(flock) * ratio_co + self.alignment(
            flock) * ratio_al + self.separation(flock) * ratio_sep

        if np.linalg.norm(steer) > max_steer:
            steer /= np.linalg.norm(steer)
            steer *= max_steer

        self.velocity += steer

        if np.linalg.norm(self.velocity) > max_velocity:
            self.velocity /= np.linalg.norm(self.velocity)
            self.velocity *= max_velocity

        self.position += self.velocity * interval * speed

        self.border()


def cin(flock):
    flock.boids = [
        Boid(egboids_position[0, i], egboids_position[1, i], egboids_position[2, i],
             egboids_velocity[0, i], egboids_velocity[1, i], egboids_velocity[2, i])
        for i in range(count)
    ]


class Flock:

    def __init__(self):
        self.boids = [Boid(0, 0, 0, 0, 0, 0) for i in range(count)]
        cin(self)

    def update(self):
        for boid in self.boids:
            boid.update(self)



'''def update(frame):
    ax.clear()
    for i in range(10):
        flock.update()
    positions = np.array([boid.position for boid in flock.boids])
    ax.scatter(positions[:, 0], positions[:, 1], s=10)
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 600)
    ax.set_xticks([])
    ax.set_yticks([])
    return ax


flock = Flock()
fig, ax = plt.subplots(figsize=(8, 6))
animation = FuncAnimation(fig, update, interval=50)
plt.show()'''

#flock
flock = Flock()
#initialize position
position = [vector(flock.boids[i].position[0], flock.boids[i].position[1], flock.boids[i].position[2])for i in range(count)]
velocity = [vector(flock.boids[i].velocity[0], flock.boids[i].velocity[1], flock.boids[i].velocity[2])for i in range(count)]
#make birds
bird = []
for i in range(count):
    bird.append(arrow(pos = position[i], axis = velocity[i],color = color.white, shininess = 1, shaftwidth = 2,headwidth = 4, headlength = 10,  emmisive = True))


#update
while True:
    flock.update()
    '''for i in range(count):
        print(flock.boids[i].position)
    print('='*30)
    print(len(bird))'''
    position = [vector(flock.boids[i].position[0], flock.boids[i].position[1], flock.boids[i].position[2])for i in range(count)]
    velocity = [vector(flock.boids[i].velocity[0], flock.boids[i].velocity[1], flock.boids[i].velocity[2])for i in range(count)]
    for i in range(count):
        bird[i].pos  = position[i]
        bird[i].axis = velocity[i]
    sleep(interval)
