import matplotlib.pyplot as plt
import cupy as cp
from network import MLP
from reader import Reader

def main(layers, learn_speed, momentum):
    reader = Reader()
    learning_data = reader.load_learning_data()
    testing_data = reader.load_testing_data()

    learning_normalize, data_learning_min, data_learning_max = Reader.normalize(learning_data)
    testing_normalize, data_testing_min, data_testing_max = Reader.normalize(testing_data)

    a = MLP(layers)

    MSE_learn_archive = []
    MSE_test_archive = []
    network_outputs_list = []
    last_output_list = []
    epok_min = 40
    epok_max = 50
    licznik = 1
    warunek = True

    while warunek:
        print(licznik)

        for j in range(len(learning_normalize)):
            _ = a.learn(cp.array([learning_normalize[j][0], learning_normalize[j][1]]),
                        cp.array([learning_data[j][2], learning_data[j][3]]), learn_speed, momentum)
            print('\r', j, '/', (len(learning_normalize)), end='')

        suma = 0
        for j in range(len(learning_normalize)):
            network_outputs_l = a.forward(cp.array([learning_normalize[j][0], learning_normalize[j][1]]))
            correct_outputs_l = cp.array([learning_data[j][2], learning_data[j][3]])
            errors_2 = cp.square(correct_outputs_l - network_outputs_l)
            suma += cp.sum(errors_2)
        MSE_l = suma / (len(learning_normalize) * 2)
        print(MSE_l)

        suma = 0
        network_outputs_list = []
        for j in range(len(testing_normalize)):
            network_outputs_t = a.forward(cp.array([testing_normalize[j][0], testing_normalize[j][1]]))
            correct_outputs_t = cp.array([testing_data[j][2], testing_data[j][3]])
            errors_2 = cp.square(correct_outputs_t - network_outputs_t)
            suma += cp.sum(errors_2)
            output_list = [network_outputs_t[0].item(), network_outputs_t[1].item(), correct_outputs_t[0], correct_outputs_t[1]]
            network_outputs_list.append(output_list)
        MSE_t = suma / (len(testing_normalize) * 2)
        print(MSE_t)

        if (licznik > epok_min and MSE_t >= MSE_test_archive[-1]) or licznik >= epok_max:
            warunek = False
        else:
            MSE_learn_archive.append(MSE_l.item())
            MSE_test_archive.append(MSE_t.item())
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
    plt.suptitle(f'{layers}, {learn_speed}, {momentum}')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    n = int(input('Enter the number of hidden layers: '))
    layers = []
    for i in range(n):
        layers.append(int(input('Enter the number of neurons in the hidden layer: ')))

    learn_speed = float(input('Enter the learning rate (0.05): '))
    momentum = float(input('Enter the momentum term (0.9): '))

    main(layers, learn_speed, momentum)
