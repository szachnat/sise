from random import random
from math import exp

#funkje aktywacji i ich pochodne
#funkcja simigodalna
def sigmoidal_function(x):
    return 1 / (1 + exp(-x))

#pochodna funkcji simigodalnej
def derivative_of_sigmoidal_function(y):
    return y * (1 - y)

# identity function
def identity_function(x):
    return x

# derivative of identity function (argument is not important)
def derivative_of_identity_function(y):
    return 1

#exception
class ActivationFunctionNotFound(Exception):
    pass

#warstwa MLP
class Layer:
    ############################################################################################
    def __init__(self, number_of_neurons, inputs, activation_function, derivative_of_activation_function):
        self.activation_function=activation_function
        self.derivative_of_activation_function=derivative_of_activation_function
        self.weights=[[random() for i in range(inputs)] for j in range(number_of_neurons)]
        self.bias=[0 for i in range(number_of_neurons)]
    ############################################################################################
    def print(self):
        print(self.weights)
        print(self.bias)
    ############################################################################################

#MLP
class MLP:
    ############################################################################################
    def __init__(self, layers) -> None:
        self.layers=[]
        self.layers.append(Layer(layers[0],2,identity_function,derivative_of_identity_function))
        for i in range(len(layers)-1):
            self.layers.append(Layer(layers[i+1],layers[i],sigmoidal_function,derivative_of_sigmoidal_function)) 
        self.layers.append(Layer(2,layers[-1],sigmoidal_function,derivative_of_sigmoidal_function))
    ############################################################################################
    def print(self):
        for i in range(len(self.layers)):
            print(Layer.print(self.layers[i]))
