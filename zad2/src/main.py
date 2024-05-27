import matplotlib.pyplot as plt
import numpy as np

from scipy.stats import norm

from Reader import Reader
from network import Layer,sigmoidal_function, derivative_of_sigmoidal_function,identity_function,derivative_of_identity_function,MLP


def main(layers,learn_speed,momentum) -> None:
    reader = Reader()
    learning_data = reader.load_learning_data()
    testing_data = reader.load_testing_data()

    learning_normalize, data_learning_min, data_learning_max=Reader.normalize(learning_data)
    testing_normalize, data_testing_min, data_testing_max=Reader.normalize(testing_data)
    
    a=MLP(layers)

    #######################################################################################################################################

    MSE_learn_archive=[]
    MSE_test_archive=[]
    network_outputs_list=[]
    last_output_list=[]
    epoki=50#0
    licznik=1
    warunek=True



    while warunek:
            print(licznik)


            for j in range(len(learning_normalize)):
                #_=a.learn([learning_normalize[j][0],learning_normalize[j][1]],[learning_normalize[j][2],learning_normalize[j][3]],learn_speed,momentum)
                _=a.learn([learning_normalize[j][0],learning_normalize[j][1]],[learning_data[j][2],learning_data[j][3]],learn_speed,momentum)



            suma=0
            for j in range(len(learning_normalize)):
                network_outputs_l=a.forward([learning_normalize[j][0],learning_normalize[j][1]])
                #correct_outputs_l=[learning_normalize[j][2],learning_normalize[j][3]]
                correct_outputs_l=[learning_data[j][2],learning_data[j][3]]
                errors_2=[(correct - network)*(correct - network) for correct, network in zip(correct_outputs_l, network_outputs_l)]
                suma+=sum(errors_2)
            MSE_l=suma/(len(learning_normalize)*2)
            print('learn',MSE_l)


            suma=0
            network_outputs_list=[]
            for j in range(len(testing_normalize)):
                network_outputs_t=a.forward([testing_normalize[j][0],testing_normalize[j][1]])
                #correct_outputs_t=[testing_normalize[j][2],testing_normalize[j][3]]
                correct_outputs_t=[testing_data[j][2],testing_data[j][3]]
                errors_2=[(correct - network)*(correct - network) for correct, network in zip(correct_outputs_t, network_outputs_t)]
                suma+=sum(errors_2)
                output_list=[network_outputs_t[0],network_outputs_t[1],correct_outputs_t[0],correct_outputs_t[1]]
                network_outputs_list.append(output_list)
            MSE_t=suma/(len(testing_normalize)*2)
            print('testt',MSE_t)


            if ((licznik>10 and MSE_t >= MSE_test_archive[-1]) or licznik >= epoki):
                print('if ',licznik,' ',MSE_t,'>',MSE_test_archive[-1])
                warunek=False
            else:
                MSE_learn_archive.append(MSE_l)
                MSE_test_archive.append(MSE_t)
                last_output_list=network_outputs_list


            licznik+=1


            
    plt.subplots(nrows=1, ncols=3, figsize=(18, 6))
    plt.subplot(1,3,1)
    plt.plot(MSE_learn_archive)
    plt.plot(MSE_test_archive)




    testing_data_error_input=[]
    for i in range (len(testing_data)):
            testing_data_error_input.append(abs(testing_data[i][0]-testing_data[i][2]))
            testing_data_error_input.append(abs(testing_data[i][1]-testing_data[i][3]))
    testing_data_error_input=sorted(testing_data_error_input)

    n = len(testing_data_error_input)
    ecdf_values_test = np.arange(1, n + 1) / n

    #print(last_output_list)
    #last_output_list=Reader.denormalize(last_output_list, data_testing_min, data_testing_max)
    output_data_error_input=[]
    for i in range (len(last_output_list)):
            output_data_error_input.append(abs(last_output_list[i][0]-last_output_list[i][2]))
            output_data_error_input.append(abs(last_output_list[i][1]-last_output_list[i][3]))
    output_data_error_input=sorted(output_data_error_input)

    n = len(output_data_error_input)
    ecdf_values_output = np.arange(1, n + 1) / n



    plt.subplot(1,3,2)
    plt.plot(testing_data_error_input, ecdf_values_test)
    plt.plot(output_data_error_input, ecdf_values_output)
    plt.grid(True)



    plt.subplot(1,3,3)
    x_values = [item[0] for item in testing_data]
    y_values = [item[1] for item in testing_data]
    plt.scatter(x_values,y_values)
    x_values = [item[0] for item in last_output_list]
    y_values = [item[1] for item in last_output_list]
    plt.scatter(x_values,y_values)
    x_values = [item[2] for item in testing_data]
    y_values = [item[3] for item in testing_data]
    plt.scatter(x_values,y_values)
    plt.suptitle(str(layers))
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    n=int(input('podaj ilosc warstw ukrytych:'))
    layers=[]
    for i in range(n):
         layers.append(int(input('podaj ilosc neuronow na warstwie ukrytej:')))

    learn_speed=float(input('podaj szybkosc uczenia(0.05):'))
    momentum=float(input('podaj człon momentum(0.9):'))

    main(layers,learn_speed,momentum)

