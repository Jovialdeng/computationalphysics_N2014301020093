# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 23:11:38 2016

@author: JOVIAL DENG
"""

# -*- coding: utf-8 -*-
import math
import numpy as np
from matplotlib import pyplot as plt 
from matplotlib import animation  
g = 9.8
b2m = 4e-5
r = []
X = []
Y = []
class flight_state:
    def __init__(self, _x = 0, _y = 0, _vx = 0, _vy = 0, _t = 0):
        self.x = _x
        self.y = _y
        self.vx = _vx
        self.vy = _vy
        self.t = _t
class cannon:
    def __init__(self, _fs = flight_state(0, 0, 0, 0, 0), _dt = 0.01):
        self.cannon_flight_state = []
        self.cannon_flight_state.append(_fs)
        self.dt = _dt
    def next_state(self, current_state):
        global g
        next_x = current_state.x + current_state.vx * self.dt
        next_vx = current_state.vx
        next_y = current_state.y + current_state.vy * self.dt
        next_vy = current_state.vy - g * self.dt
        #print next_x, next_y
        return flight_state(next_x, next_y, next_vx, next_vy, current_state.t + self.dt)
    def shoot(self):
        while not(self.cannon_flight_state[-1].y < 0):
            self.cannon_flight_state.append(self.next_state(self.cannon_flight_state[-1]))
        r = - self.cannon_flight_state[-2].y / self.cannon_flight_state[-1].y
        self.cannon_flight_state[-1].x = (self.cannon_flight_state[-2].x + r * self.cannon_flight_state[-1].x) / (r + 1)
        self.cannon_flight_state[-1].y = 0
    def show_trajectory(self):
        x = []
        y = []
        for fs in self.cannon_flight_state:
            x.append(fs.x)
            y.append(fs.y)
        X.append(x)
        Y.append(y)
class drag_cannon(cannon):
    def next_state(self, current_state):
        global g, b2m
        v = math.sqrt(current_state.vx * current_state.vx + current_state.vy * current_state.vy)
        next_x = current_state.x + current_state.vx * self.dt
        next_vx = current_state.vx - b2m * v * current_state.vx * self.dt
        next_y = current_state.y + current_state.vy * self.dt
        next_vy = current_state.vy - g * self.dt - b2m * v * current_state.vy * self.dt
        #print next_x, next_y
        return flight_state(next_x, next_y, next_vx, next_vy, current_state.t + self.dt)
class adiabatic_drag_cannon(cannon):
    def next_state(self, current_state):
        global g, b2m
        factor = (1 - 6.5e-3 * current_state.y / 288.15) ** 2.5
        v = math.sqrt(current_state.vx * current_state.vx + current_state.vy * current_state.vy)
        next_x = current_state.x + current_state.vx * self.dt
        next_vx = current_state.vx - factor * b2m * v * current_state.vx * self.dt
        next_y = current_state.y + current_state.vy * self.dt
        next_vy = current_state.vy - g * self.dt - factor * b2m * v * current_state.vy * self.dt
        #print next_x, next_y
        return flight_state(next_x, next_y, next_vx, next_vy, current_state.t + self.dt)
class isothermal_drag_cannon(cannon):
    def next_state(self, current_state):
        global g, b2m
        factor = math.exp(-current_state.y / 1e4)
        v = math.sqrt(current_state.vx * current_state.vx + current_state.vy * current_state.vy)
        next_x = current_state.x + current_state.vx * self.dt
        next_vx = current_state.vx - factor * b2m * v * current_state.vx * self.dt
        next_y = current_state.y + current_state.vy * self.dt
        next_vy = current_state.vy - g * self.dt - factor * b2m * v * current_state.vy * self.dt
        #print next_x, next_y
        return flight_state(next_x, next_y, next_vx, next_vy, current_state.t + self.dt)
speed = 700
theta = np.arange(30., 56., 0.1)
v_x = [speed * math.cos(i * math.pi / 180) for i in theta]
v_y = [speed * math.sin(i * math.pi / 180) for i in theta]
def wahaha():
    b = []
    for i in range(len(theta)):
        b.append(adiabatic_drag_cannon(flight_state(0, 0, v_x[i], v_y[i], 0)))
        b[i].shoot()
        r.append(b[i].cannon_flight_state[-1].x)
        b[i].show_trajectory()
wahaha()
p = r.index(max(r))
print theta[p], max(r),type(max(r))
fig = plt.figure()  
ax = plt.axes(xlim=(0, 40000), ylim=(0, 18000))  
line, = ax.plot([], [],lw = 2,label = 'adiabatic model' ,color = 'pink') 
angle_text = ax.text(24167, 14400, '')
maxrange_text = ax.text(24167, 12400, '')
plt.xlabel(r'$x(m)$', fontsize=16)
plt.ylabel(r'$y(m)$', fontsize=16)
plt.title('Trajectory of cannon shell') 
plt.legend(loc='upper left', frameon=False)
def init():  
    line.set_data([], [])  
    angle_text.set_text('')
    maxrange_text.set_text('')
    return line, angle_text, maxrange_text
def animate(i):  
    x = X[i]  
    y = Y[i]
    line.set_data(x, y)  
    pct = float(X[i][-1])/float(max(r))*100
    angle_text.set_text('initial speed: 700m/s\n' + 'firing angle: %s' % theta[i] + r'$^{\circ}$' + '\nrange: %f %%' % pct)
    if i > p:
        maxrange_text.set_text('max range: %s' % max(r))
    return line,  angle_text, maxrange_text
fram = len(theta)
anim=animation.FuncAnimation(fig, animate, init_func=init, frames=fram, interval=30, blit=True) 
plt.show()