import cupy as cp
import numpy as np

def relu_function(x):
    return cp.maximum(0, x)

def derivative_of_relu_function(y):
    return cp.where(y > 0, 1, 0)

def identity_function(x):
    return x

def derivative_of_identity_function(y):
    return 1

def xavier_initialization(inputs, outputs):
    return cp.random.randn(outputs, inputs) * np.sqrt(2 / (inputs + outputs))

class Layer:
    def __init__(self, number_of_neurons, inputs, activation_function, derivative_of_activation_function):
        self.activation_function = activation_function
        self.derivative_of_activation_function = derivative_of_activation_function
        self.weights = xavier_initialization(inputs, number_of_neurons)
        self.bias = cp.zeros(number_of_neurons)
        self.number_of_inputs = int(inputs)
        self.gradients = cp.zeros((number_of_neurons, inputs))
    
    def print_layer(self):
        print(cp.asnumpy(self.weights))
        print(cp.asnumpy(self.bias))
    
    def forward(self, inputs):
        self.inputs = inputs
        self.outputs = self.activation_function(cp.dot(self.weights, inputs) + self.bias)
        return self.outputs
    
    def learn(self, errors, learn_speed, momentum, calculate_errors=True):
        deltas = errors * self.derivative_of_activation_function(self.outputs)
        
        if calculate_errors:
            errors_out = cp.dot(self.weights.T, deltas)
        else:
            errors_out = None

        self.gradients = learn_speed * cp.outer(deltas, self.inputs) + momentum * self.gradients
        self.weights -= self.gradients
        self.bias -= learn_speed * deltas

        return errors_out

class MLP:
    def __init__(self, layers):
        self.layers = []
        self.layers.append(Layer(layers[0], 2, relu_function, derivative_of_relu_function))
        for i in range(len(layers) - 1):
            self.layers.append(Layer(layers[i + 1], layers[i], relu_function, derivative_of_relu_function))
        self.layers.append(Layer(2, layers[-1], identity_function, derivative_of_identity_function))
    
    def forward(self, inputs):
        for layer in self.layers:
            inputs = layer.forward(inputs)
        return inputs
    
    def learn(self, inputs, correct_outputs, learn_speed=0.05, momentum=0.9):
        network_outputs = self.forward(inputs)
        errors = cp.array([network - correct for network, correct in zip(network_outputs, correct_outputs)])
        
        for layer in reversed(self.layers[1:]):
            errors = layer.learn(errors, learn_speed, momentum)
        
        self.layers[0].learn(errors, learn_speed, momentum, False)
        
        return network_outputs
