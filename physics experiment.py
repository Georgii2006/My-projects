#This program is a part of my physics school project.
#During this project I needed to experementally find
#acceleration of gravity in a mathematical pendulum.
#To create a mathematicall pendulum I possesed
#a metal ball, thread and the stand of height
#of one metre and seventy centemetres. The ball was
#hang up on the thread which was held by clamps on the top
#of the stand. The experiment was held three times. Each time before
#the experiment the distance between the point where the thread
#was hold by the clamps and the centre of the mass were measured.
#During the experiment the ball was deflected on a small angle
#and then the time of 10 accelations were measured. The experiment
#was held three times each time for a different length of a thread.
#During each experiment different lengths of the tread were used.
#Each experiment consisted of 10 measurements.

import math

#measurments for the length of 0.855 metres with the deviation of 0.003 metres
first_list = [18.91,17.98,18.92,18.33,20.51,18.45,18.10,18.42,18.46,19.18]
#measurments for the length of 1 metre with the deviation of 0.006 metres
third_list = [20.35,20.47,21.38,21.49,20.59,20.69,20.44,19.53,20.65,20.64]
#measurments for the length of 1 metre with the deviation of 0.003 metres
fifth_list = [18.02,18.07,17.26,17.37,18.13,17.89,17.90,18.02,18.26,18.49]

def single_g(time, length):
    #this function calculates accelaration of gravity
    #using the formula for mathematical pendulums.
    return (length*4*math.pi**2)/(time**2)
def list_g(time_list, length):
    #this function сreates the list of values acceleration of gravity
    #calculated for each mesuarements in the the time list
    list_of_g = [single_g(time, length) for time in time_list]
    return list_of_g
def g_av(g_list):
    #this function calcutates arithmetical mean out of the values
    #in the list of accelarations of gravity
    g_mean = sum(g_list)/len(g_list)
    return g_mean
def t_means(time_list):
    #this function takes list of time mesuarments as an argument
    #and returns arithmetical mean of values in the list and deviation
    #of time
    t_mean = sum(time_list)/len(time_list)
    t_standart_deviation=(sum([t_mean-result**2 for result in time_list]) / (len(time_list)-1))**0.5
    t_max = t_mean + t_standart_deviation
    t_min = t_mean - t_standart_deviation
    #to calculate the deviation of time the following formula is used:
    delta_time = abs(t_max - t_min)/2
    return t_mean, delta_time

def delta_gs(g, delta_length, length, delta_time, time):
    #this function returns deviation of accelaration og gravity
    #using the following formula
    return ((delta_length/length)+ 2*(delta_time/time))

def g(time_list, length, delta_length):
    #During the experiment it was assumed the delay of human's reaction is 0.3 seconds
    reaction = 0.3
    #To find the time of one accelation the reaction is substracted from each
    #measurment in a list and then the time of 10 measurements without the
    #assumed meassurement error is divided by 10.
    time_list = [(time-0.3)/10 for time in time_list]
    #the obtained list is processed with the function beneath
    #which creates a list of values of accelaration of gravity
    #calculated for each time measurement
    g_list = list_g(time_list, length)
    #calculating arithmetical mean of the values of the accelaration of gravity
    g_mean = g_av(g_list)
    #calculationg arithmetical mean and deviation of time mesuarments
    t_mean, delta_time = t_means(time_list)
    delta_g = delta_gs(g_mean, delta_length, length, delta_time, t_mean)
    print('g = %s  ± %s' % (g_mean, delta_g))
g(first_list, 0.855, 0.003)
g(third_list, 1, 0.006)
g(fifth_list, 0.775, 0.003)

#The size of of the ball was relatively neglegible
#in comparison with the size of the thread. The thread had a mass
#which was significantly lower than the mass of the ball, but yet
#the mass of the former could be the problem that resulted into
#inaccuracy in the resulst of the experiment
