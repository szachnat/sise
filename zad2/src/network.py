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

def relu_function(x):
    return np.maximum(0, x)  # Element-wise ReLU activation

def derivative_of_relu_function(y):
    return np.where(y > 0, 1, 0)  # Element-wise derivative of ReLU

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
        #self.weights = xavier_initialization(inputs, number_of_neurons)
        self.weights = [[(random() - 0.5) for _ in range(inputs)] for _ in range(number_of_neurons)]
        self.bias = np.random.randn(number_of_neurons) * np.sqrt(2.0 / number_of_neurons)
        self.number_of_inputs = int(inputs)
        self.gradients = np.zeros((number_of_neurons, inputs))
    
    def forward(self, inputs):
        self.inputs = inputs
        z = np.dot(self.weights, inputs) + self.bias
        self.outputs = self.activation_function(z)
        return self.outputs
    
    def learn(self, errors, learn_speed, momentum, calculate_errors=True):
        deltas = [error * self.derivative_of_activation_function(output) for error, output in zip(errors, self.outputs)]
        
        if self.activation_function == relu_function:
            # Gradient clipping
            max_gradient = 10.0  # Adjust as necessary
            deltas = np.clip(deltas, -max_gradient, max_gradient)
        
        if calculate_errors:
            errors_out = [sum(deltas[j] * self.weights[j][i] for j in range(len(self.weights))) for i in range(self.number_of_inputs)]
        else:
            errors_out = None
        
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
        #self.layers.append(Layer(layers[0], 2, sigmoidal_function, derivative_of_sigmoidal_function))
        #for i in range(len(layers) - 1):
        #    self.layers.append(Layer(layers[i + 1], layers[i], sigmoidal_function, derivative_of_sigmoidal_function))
        self.layers.append(Layer(layers[0], 2, relu_function, derivative_of_relu_function))
        for i in range(len(layers) - 1):
            self.layers.append(Layer(layers[i + 1], layers[i], relu_function, derivative_of_relu_function))
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
    
