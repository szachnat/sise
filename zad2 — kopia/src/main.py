import matplotlib.pyplot as plt
import numpy as np
from random import random
from sklearn.neural_network import MLPRegressor

from scipy.stats import norm

from Reader import Reader
from network import Layer,sigmoidal_function, derivative_of_sigmoidal_function,identity_function,derivative_of_identity_function,MLP


def main() -> None:
    reader = Reader()
    learning_data = np.array(reader.load_learning_data(), dtype=float)
    td = reader.load_testing_data()
    testing_data = np.array(td, dtype=float)

    x_train = learning_data[:,:2]
    y_train = learning_data[:,2:]
    x_test = testing_data[:,:2]
    y_test = testing_data[:,2:]

    print(td[:5])
    print(testing_data[:5])

    #print(x_test.shape)
    #print(y_test.shape)

    #regr = MLPRegressor(hidden_layer_sizes=(20,), activation='logistic', solver='sgd', alpha=0.0001, batch_size=112886, max_iter=100, momentum=0.0)
    #regr.fit(x_train, y_train)
    #results = regr.predict(x_test)
    #print(regr.score(x_test, y_test))

    #for x in td:
    #    plt.plot(x[2], x[3], '.b')
    plt.scatter(y_test[:,0], y_test[:,1])
    #plt.scatter(results[:,0], results[:,1])
    plt.show()

if __name__ == "__main__":
    main()

