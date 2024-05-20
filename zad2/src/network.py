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
        self.number_of_inputs=int(inputs)
        self.gradients = [[0 for _ in range(inputs)] for _ in range(number_of_neurons)]
    ############################################################################################
    def print(self):
        print(self.weights)
        print(self.bias)
    ############################################################################################
    def test(self,inputs):
        self.inputs=inputs
        sum = 0
        self.outputs=[]
        for j in range(len(self.weights)):
            neuron=self.weights[j]
            sum=0
            for i in range(len(inputs)):
                #print('neuron=',neuron[i])
                #print('x=',inputs[i])
                sum+=neuron[i]*inputs[i]
                #print('suma=',sum)
            #print('bias=',self.bias[j])
            sum+=self.bias[j]
            #print('suma=',sum)
            self.outputs.append(self.activation_function(sum))
            #print('aktyvation=',self.activation_function(sum))
        #print('outputs=',self.outputs)
        return self.outputs
    ############################################################################################
    def learn(self,errors,learn_speed, momentum, calculate_errors=True):
        # calculate error
        errors_out=[]
        if(calculate_errors):
            for i in range(self.number_of_inputs):
                error_for_input=0
                for j in range(len(self.weights)):
                    error_to_propagate=errors[j]
                    #print('error to propagate=',error_to_propagate)
                    weight=self.weights[j][i]
                    #print('weight=',weight)
                    #print('last output=',self.outputs[j])
                    error_for_input+=error_to_propagate*weight*self.derivative_of_activation_function(self.outputs[j])
                errors_out.append(error_for_input)
                #print("error on input=",error_for_input)
        # calculate gradient
        gradients = []
        for activation, error, old_gradient in zip(self.outputs, errors, self.gradients):
            factor = -error * self.derivative_of_activation_function(activation)
            gradients.append([factor * x + momentum * g for x, g in zip(self.inputs, old_gradient)])
        self.gradients = gradients
        # calculate new weights
        new_weights = []
        for weight, gradient in zip(self.weights, self.gradients):
            new_weights.append([w - learn_speed * g for w, g in zip(weight, gradient)])
            #new_weight=0
            #for w, g in zip(weight, gradient):
            #    new_weight+=w - learn_speed * g
            #new_weights.append(new_weight)
        self.weights = new_weights
        #calculate new bias
        new_biases = []
        for bias, activation, error in zip(self.bias, self.outputs, errors):
            factor = -error * self.derivative_of_activation_function(activation)
            new_bias = bias - learn_speed * factor
            new_biases.append(new_bias)
        self.bias = new_biases
        return errors_out

#MLP
class MLP:
    ############################################################################################
    def __init__(self, layers) -> None:
        self.layers=[]
        self.layers.append(Layer(layers[0],2,sigmoidal_function,derivative_of_sigmoidal_function))
        for i in range(len(layers)-1):
            self.layers.append(Layer(layers[i+1],layers[i],sigmoidal_function,derivative_of_sigmoidal_function)) 
        self.layers.append(Layer(2,layers[-1],sigmoidal_function,derivative_of_sigmoidal_function))
    ############################################################################################
    def print(self):
        for i in range(len(self.layers)):
            print(Layer.print(self.layers[i]))
    ############################################################################################
    def test(self,inputs):
        for layer in self.layers:
            inputs = layer.test(inputs)
        return inputs
    ############################################################################################
    def learn(self,inputs, correct_outputs, learn_speed=0.05, momentum=0.9):
        network_outputs=self.test(inputs)
        #print('wyjsciesieci=',network_outputs)
        errors=[correct_outputs - network_outputs for correct_outputs, network_outputs in zip(correct_outputs, network_outputs)]
        #print("bledy=",errors)
        for layer in reversed(self.layers[1:]):
            errors=layer.learn(errors, learn_speed, momentum)
            #print("bledy=",errors)
        self.layers[0].learn(errors, learn_speed, momentum, False)
        #print("bledy=",errors)
