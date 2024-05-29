import numpy as np

from random import random
from math import exp, sqrt

# Activation functions and their derivatives
def sigmoidal_function(x):
    return 1 / (1 + exp(-x))

def derivative_of_sigmoidal_function(y):
    return y * (1 - y)

def identity_function(x):
    return x

def derivative_of_identity_function(y):
    return 1

class ActivationFunctionNotFound(Exception):
    pass

# Xavier Initialization
def xavier_initialization(inputs, outputs):
    return np.random.randn(outputs, inputs) * sqrt(2 / (inputs + outputs))

# Layer class for MLP
class Layer:
    def __init__(self, number_of_neurons, inputs, activation_function, derivative_of_activation_function):
        self.activation_function = activation_function
        self.derivative_of_activation_function = derivative_of_activation_function
        #self.weights = [[(random() - 0.5) for _ in range(inputs)] for _ in range(number_of_neurons)]
        self.weights = xavier_initialization(inputs, number_of_neurons).tolist()
        self.bias = [0 for _ in range(number_of_neurons)]
        self.number_of_inputs = int(inputs)
        self.gradients = [[0 for _ in range(inputs)] for _ in range(number_of_neurons)]
    
    def print_layer(self):
        print(self.weights)
        print(self.bias)
    
    def forward(self, inputs):
        self.inputs = inputs
        self.outputs = [self.activation_function(sum(w * i for w, i in zip(neuron, inputs)) + b) for neuron, b in zip(self.weights, self.bias)]
        return self.outputs
    
    def learn(self, errors, learn_speed, momentum, calculate_errors=True):
        # Compute the gradient of the error with respect to the activation
        deltas = [error * self.derivative_of_activation_function(output) for error, output in zip(errors, self.outputs)]
        
        # Calculate error to propagate to the previous layer
        if calculate_errors:
            errors_out = [sum(deltas[j] * self.weights[j][i] for j in range(len(self.weights))) for i in range(self.number_of_inputs)]
        else:
            errors_out = None

        # Calculate gradients and update weights and biases
        for j in range(len(self.weights)):
            for i in range(len(self.inputs)):
                self.gradients[j][i] = learn_speed * deltas[j] * self.inputs[i] + momentum * self.gradients[j][i]
                self.weights[j][i] = self.weights[j][i] - self.gradients[j][i]
            self.bias[j] = self.bias[j] - learn_speed * deltas[j]

        return errors_out

# MLP class
class MLP:
    def __init__(self, layers):
        self.layers = []
        self.layers.append(Layer(layers[0], 2, sigmoidal_function, derivative_of_sigmoidal_function))
        for i in range(len(layers) - 1):
            self.layers.append(Layer(layers[i + 1], layers[i], sigmoidal_function, derivative_of_sigmoidal_function))
        self.layers.append(Layer(2, layers[-1], identity_function, derivative_of_identity_function))
        #self.layers.append(Layer(2, layers[-1], sigmoidal_function, derivative_of_sigmoidal_function))
    
    def print(self):
        for layer in self.layers:
            layer.print_layer()
    
    def forward(self, inputs):
        for layer in self.layers:
            inputs = layer.forward(inputs)
        return inputs
    
    def learn(self, inputs, correct_outputs, learn_speed=0.05, momentum=0.9):
        network_outputs = self.forward(inputs)
        #print('Network outputs:', network_outputs)
        
        # Compute initial errors using the derivative of the cost function (MSE)
        errors = [(network - correct) for network, correct in zip(network_outputs, correct_outputs)]
        
        for layer in reversed(self.layers[1:]):
            errors = layer.learn(errors, learn_speed, momentum)
        
        self.layers[0].learn(errors, learn_speed, momentum, False)
        
        return network_outputs
    
