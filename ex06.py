# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 22:39:25 2016

@author: JOVI
"""

import time
import math
import matplotlib.pyplot as plt

print 'Input x_target ->',
x_target = float(raw_input())
print 'Input y_target ->',
y_target = float(raw_input())

def correct(string,y_t):
    x_record = string[0][-1] 
    y_record = y_t
    while True:
        if (string[1][-1] < y_t):
            if (string[1][-1] < y_t and string[1][-2] > y_t):
                x_record = string[0][-1] 
                y_record = string[1][-1]               
            del string[0][-1]
            del string[1][-1]
        else:
            string[0].append(string[0][-1]+(y_t - string[1][-1])*(string[0][-1] - x_record)/(string[1][-2] - y_record))
            string[1].append(y_t)
            break
    return string[0],string[1]
       
def calculate(v,theta):
    vx = []
    vy = []
    vx.append( v * math.cos(theta*math.pi/180))
    vy.append( v * math.sin(theta*math.pi/180))
    dt = 0.1
    t = []
    x = []
    y = []
    t.append(0)
    x.append(0)
    y.append(0)
    i = 1
    while (y[-1] >= 0):
        x.append(x[i - 1] + vx[i - 1]*dt)
        vx.append(vx[i - 1] - dt*0.00004*math.sqrt(vx[i - 1]**2+vy[i - 1]**2)*vx[i - 1]*(1-(0.0065*y[i - 1])/280)**2.5)
        y.append(y[i - 1] + vy[i - 1]*dt)
        vy.append(vy[i - 1]-9.8*dt -dt*0.00004*math.sqrt(vx[i - 1]**2+vy[i - 1]**2)*vy[i - 1]*(1-(0.0065*y[i - 1])/280)**2.5)
        t.append(t[i - 1] + dt)
        i+= 1
    r = y[-2] / y[-1]
    x[-1] = (x[-2] + r * x[-1]) / (r + 1)
    y[-1] = 0
    return x, y
   
def find_maxheight(string):
    for i in range(len(string[1])):
        if ( string[1][0] < string[1][i] ):
            string[1][0] = string[1][i]
    return string[1][0]

def scan_angle(v,theta, x_t, y_t, degree):
    ran_a = [20, 5, 2, 0.8, 0.2]
    delta = [1, 0.5, 0.1, 0.05, 0.01]
    theta = theta - ran_a[degree]
    theta_record = []
    x = []
    data = [[],[]]
    for i in range(int(ran_a[degree]*2/delta[degree]+1)):
        data = calculate(v,theta)[:]
        if ( find_maxheight(data) < y_t):
            theta = theta + delta[degree]
            x.append(100000000)
            theta_record.append(theta)
        else:
            data = correct(data,y_t)[:]
            x.append(data[0][-1])
            theta_record.append(theta)
            theta = theta + delta[degree]
    for j in range(len(x)):
        if ( abs(x[0] - x_t) > abs(x[j] - x_t)):
            x[0] = x[j]
            theta_record[0] = theta_record[j]
    return theta_record[0],x[0]

def scan_v(v,theta, x_target, y_target, degree):
    ran_v = [100, 10, 2, 0.8, 0.2]
    delta = [10, 2, 0.5, 0.1, 0.02]
    v = v - ran_v[degree]
    x = []
    theta_record = []
    v_record = []
    for i in range(int(ran_v[degree]*2/delta[degree]+1)):
        record_v = scan_angle(v,theta, x_target, y_target, degree)[:]
        x.append(record_v[1])
        theta_record.append(record_v[0])
        v_record.append(v)
        v = v + delta[degree]
    for j in range(len(x)):
        if ( abs(x[0] - x_target) > abs(x[j] - x_target)):
            x[0] = x[j]
            v_record[0] = v_record[j]
            theta_record[0] = theta_record[j]
    print v_record
    print theta_record
    print x
    return v_record[0],theta_record[0]
    
def deep_scan(v, theta, x_target, y_target, precision):
    degree = 0
    record = [[],[]]
    for i in range(precision):
        record = scan_v(v,theta,x_target,y_target,degree)[:]
        v = record[0]
        theta = record[1]
        degree = degree + 1
    return record
        
def judge_hitting(string,x_t,y_t):
    alpha = 0
    for i in range(len(string[0])):
        if ( x_t - 8 < string[0][-1] < x_t + 8 ):
            alpha = 1
    if (alpha == 1):
        print 'Successfully hitted'
        return 1
    else:
        print 'Miss'
        return 0

               
def main():
    start = time.clock()
    data_record = deep_scan(700,60,x_target,y_target,5)
    v = data_record[0]
    theta = data_record[1]
    cannon_record = correct(calculate(v, theta),y_target)
    x_max = cannon_record[0][-1]
    judge_hitting(cannon_record,x_target,y_target)
    print '%f ' % x_max
    print '%f ' % theta
    print '%f ' %v
    end = time.clock()
    print "read: %f s" % (end - start)
    plt.figure(figsize = (8,6))
    plt.title('Trajectory of cannon shell')
    plt.xlabel('x(m)')
    plt.ylabel('y(m)')
    plt.plot(x_target,y_target,'k*',linewidth = 10,label='Target')
    plt.plot(cannon_record[0],cannon_record[1],label= 'Trajectroy')
    plt.legend(loc = 'upper left')
    plt.savefig('chapter2.png',dpi = 144)
    plt.show()
        
main()