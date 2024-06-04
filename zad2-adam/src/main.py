import matplotlib.pyplot as plt
import numpy as np
import random
from Reader import Reader
from network import Layer, sigmoidal_function, derivative_of_sigmoidal_function, identity_function, derivative_of_identity_function, MLP

def main(layers, learn_speed, momentum, epok_min, epok_max) -> None:
    reader = Reader()
    learning_data = reader.load_learning_data()
    testing_data = reader.load_testing_data()

    learning_normalize, data_learning_min, data_learning_max = Reader.normalize(learning_data)
    testing_normalize, data_testing_min, data_testing_max = Reader.normalize(testing_data)

    learning_data_shuffled = []
    for i in range(len(learning_data)):
        learning_data_shuffled.append([learning_normalize[i][0], learning_normalize[i][1], learning_data[i][2], learning_data[i][3]])

    a = MLP(layers)

    MSE_learn_archive = []
    MSE_test_archive = []
    network_outputs_list = []
    last_output_list = []
    licznik = 1
    warunek = True
    learn_speed_init = learn_speed

    while warunek:
        random.shuffle(learning_data_shuffled)
        print(licznik, layers, learn_speed)

        print('0', end='')
        for j in range(len(learning_data_shuffled)):
            _ = a.learn([learning_data_shuffled[j][0], learning_data_shuffled[j][1]], [learning_data_shuffled[j][2], learning_data_shuffled[j][3]], learn_speed, momentum)
            print('\r', j, '/', (len(learning_normalize)), end='')

        suma = 0
        print('\rlearn ', end='')
        for j in range(len(learning_normalize)):
            network_outputs_l = a.forward([learning_normalize[j][0], learning_normalize[j][1]])
            correct_outputs_l = [learning_data[j][2], learning_data[j][3]]
            errors_2 = [(correct - network) * (correct - network) for correct, network in zip(correct_outputs_l, network_outputs_l)]
            suma += sum(errors_2)
        MSE_l = suma / (len(learning_normalize) * 2)
        print(MSE_l)

        suma = 0
        print('testt ', end='')
        network_outputs_list = []
        for j in range(len(testing_normalize)):
            network_outputs_t = a.forward([testing_normalize[j][0], testing_normalize[j][1]])
            correct_outputs_t = [testing_data[j][2], testing_data[j][3]]
            errors_2 = [(correct - network) * (correct - network) for correct, network in zip(correct_outputs_t, network_outputs_t)]
            suma += sum(errors_2)
            output_list = [network_outputs_t[0], network_outputs_t[1], correct_outputs_t[0], correct_outputs_t[1]]
            network_outputs_list.append(output_list)
        MSE_t = suma / (len(testing_normalize) * 2)
        print(MSE_t)

        if ((licznik > epok_min and MSE_t >= MSE_test_archive[-1]) or licznik >= epok_max):
            print('if ', licznik, ' ', MSE_t, '>', MSE_test_archive[-1])
            warunek = False
        else:
            MSE_learn_archive.append(MSE_l)
            MSE_test_archive.append(MSE_t)
            last_output_list = network_outputs_list

        licznik += 1

    plt.subplots(nrows=1, ncols=3, figsize=(18, 6))
    plt.subplot(1, 3, 1)
    plt.plot(MSE_learn_archive)
    plt.plot(MSE_test_archive)

    testing_data_error_input = []
    for i in range(len(testing_data)):
        testing_data_error_input.append(abs(testing_data[i][0] - testing_data[i][2]))
        testing_data_error_input.append(abs(testing_data[i][1] - testing_data[i][3]))
    testing_data_error_input = sorted(testing_data_error_input)

    n = len(testing_data_error_input)
    ecdf_values_test = np.arange(1, n + 1) / n

    output_data_error_input = []
    for i in range(len(last_output_list)):
        output_data_error_input.append(abs(last_output_list[i][0] - last_output_list[i][2]))
        output_data_error_input.append(abs(last_output_list[i][1] - last_output_list[i][3]))
    output_data_error_input = sorted(output_data_error_input)

    n = len(output_data_error_input)
    ecdf_values_output = np.arange(1, n + 1) / n

    plt.subplot(1, 3, 2)
    plt.plot(testing_data_error_input, ecdf_values_test)
    plt.plot(output_data_error_input, ecdf_values_output)
    plt.grid(True)

    plt.subplot(1, 3, 3)
    x_values = [item[0] for item in testing_data]
    y_values = [item[1] for item in testing_data]
    plt.scatter(x_values, y_values)
    x_values = [item[0] for item in last_output_list]
    y_values = [item[1] for item in last_output_list]
    plt.scatter(x_values, y_values)
    x_values = [item[2] for item in testing_data]
    y_values = [item[3] for item in testing_data]
    plt.scatter(x_values, y_values)
    title = str(layers) + '-' + str(learn_speed_init) + '-' + str(momentum)
    plt.suptitle(title)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    layers = [11]
    learn_speed = 0.01
    momentum = 0.9
    epok_min = 15
    epok_max = 150
    main(layers, learn_speed, momentum, epok_min, epok_max)
