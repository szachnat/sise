import matplotlib.pyplot as plt

def read_two_2d_lists_from_file(filename):
    """
    Odczytuje trzy dwuwymiarowe listy z jednego pliku.

    Args:
    filename (str): Nazwa pliku do odczytu.

    Returns:
    tuple of lists: Trzy dwuwymiarowe listy odczytane z pliku.
    """
    with open(filename, 'r') as file:
        content = file.read().strip().split('\n\n')  # Dzielimy na trzy części według pustych linii
        list1 = [list(map(float, line.split())) for line in content[0].split('\n')]
        list2 = [list(map(float, line.split())) for line in content[1].split('\n')]
    return list1, list2

def read_three_lists_from_file(filename):
        with open(filename, 'r') as file:
            content = file.read().strip().split('\n\n')  # Dzielimy na trzy części według pustych linii
            list1 = [float(item) for item in content[0].split('\n')]
            list2 = [float(item) for item in content[1].split('\n')]
            list3 = [float(item) for item in content[2].split('\n')]
        return list1, list2, list3

def read_four_lists_from_file(filename):
        with open(filename, 'r') as file:
            content = file.read().strip().split('\n\n')  # Dzielimy na trzy części według pustych linii
            list1 = [float(item) for item in content[0].split('\n')]
            list2 = [float(item) for item in content[1].split('\n')]
            list3 = [float(item) for item in content[2].split('\n')]
            list4 = [float(item) for item in content[2].split('\n')]
        return list1, list2, list3, list4

def main():
    #dostosuj skalę wykresów 1 i 2 recznie -> w razie potrzeby odkomentuj linijki w kolejnym akapicie
    #height=
    ###############################################################################################################################################
    MSE_learn_archive1, MSE_test_archive1, MSE_test_origin1=read_three_lists_from_file('wykresy1\\wykres_1_2.txt')
    MSE_learn_archive2, MSE_test_archive2, MSE_test_origin2=read_three_lists_from_file('wykresy2\\wykres_1_2.txt')

    plt.figure(figsize=(7,6))
    plt.plot(MSE_learn_archive1)
    plt.plot(MSE_learn_archive2)
    #plt.ylim(top=height)
    plt.legend(['sieć o jednej warstwie ukrytej','sieć o dwuch warstwach ukrytych','sieć o trzech warstwach ukrytych'])
    plt.title('MSE dla zbioru uczącego')
    plt.xlabel('epoki')
    plt.ylabel('wartośc błędu MSE')
    plt.savefig('wykres1.png')
    plt.show()

    plt.figure(figsize=(7,6))
    plt.plot(MSE_test_archive1)
    plt.plot(MSE_test_archive2)
    plt.axhline(y=MSE_test_origin1[0], color='r')
    #plt.ylim(top=height)
    plt.legend(['sieć o jednej warstwie ukrytej','sieć o dwuch warstwach ukrytych','sieć o trzech warstwach ukrytych','błąd pomiarów dynamicznych'])
    plt.title('MSE dla zbioru testowego')
    plt.xlabel('epoki')
    plt.ylabel('wartośc błędu MSE')
    plt.savefig('wykres2.png')
    plt.show()
    ###############################################################################################################################################
    testing_data_error_input1,output_data_error_input1,ecdf_values_test1,ecdf_values_output1=read_four_lists_from_file('wykresy1\\wykres_3.txt')
    testing_data_error_input2,output_data_error_input2,ecdf_values_test2,ecdf_values_output2=read_four_lists_from_file('wykresy2\\wykres_3.txt')

    plt.figure(figsize=(7,6))
    plt.plot(testing_data_error_input1, ecdf_values_test1)
    plt.plot(output_data_error_input1, ecdf_values_output1)
    plt.plot(output_data_error_input2, ecdf_values_output2)
    plt.grid(True)
    plt.legend(['dystrybuanta dla pomiarów dynamicznych','dystrybuanta dla sieci o jednej warstwie ukrytej','dystrybuanta dla sieci o dwuch warstwach ukrytych','dystrybuanta dla sieci o trzech warstwach ukrytych'])
    plt.title('dystrybuanta błędu')
    plt.xlabel('błąd (mm)')
    plt.ylabel('prawdopodobieństwo skumulowane')
    plt.savefig('wykres3.png')
    plt.show()

    ###############################################################################################################################################
    testing_data1,last_output_list1=read_two_2d_lists_from_file('wykresy1\\wykres_4.txt')
    #testing_data1,last_output_list1=read_two_2d_lists_from_file('wykresy2\\wykres_4.txt')

    plt.figure(figsize=(7,6))
    x_values = [item[0] for item in testing_data1]
    y_values = [item[1] for item in testing_data1]
    plt.scatter(x_values,y_values)
    x_values = [item[0] for item in last_output_list1]
    y_values = [item[1] for item in last_output_list1]
    plt.scatter(x_values,y_values)
    x_values = [item[2] for item in testing_data1]
    y_values = [item[3] for item in testing_data1]
    plt.scatter(x_values,y_values)
    plt.legend(['wartości zmierzone','wartości skorygowane','wartości rzeczywiste'])
    plt.title('trasa robota')
    plt.savefig('wykres4.png')
    plt.show()



if __name__ == "__main__":

    main()
