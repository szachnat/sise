def save_three_lists_to_file(list1, list2, list3, filename):
    """
    Zapisuje trzy listy liczb zmiennoprzecinkowych do jednego pliku.

    Args:
    list1 (list of float): Pierwsza lista liczb zmiennoprzecinkowych.
    list2 (list of float): Druga lista liczb zmiennoprzecinkowych.
    list3 (list of float): Trzecia lista liczb zmiennoprzecinkowych.
    filename (str): Nazwa pliku do zapisu.
    """
    with open(filename, 'w') as file:
        for item in list1:
            file.write(f"{item}\n")
        file.write("\n")  # Dodajemy pustą linię jako separator
        for item in list2:
            file.write(f"{item}\n")
        file.write("\n")  # Dodajemy pustą linię jako separator
        for item in list3:
            file.write(f"{item}\n")

# Przykładowe użycie
list1 = [1.1, 2.3, 3.1]
list2 = [4.4, 5.5, 6.6]
list3 = [7.7, 8.8, 9.9]
save_three_lists_to_file(list1, list2, list3, 'wyniki.txt')


def read_three_lists_from_file(filename):
    """
    Odczytuje trzy listy liczb zmiennoprzecinkowych z jednego pliku.

    Args:
    filename (str): Nazwa pliku do odczytu.

    Returns:
    tuple of lists: Trzy listy liczb zmiennoprzecinkowych odczytane z pliku.
    """
    with open(filename, 'r') as file:
        content = file.read().strip().split('\n\n')  # Dzielimy na trzy części według pustych linii
        list1 = [float(item) for item in content[0].split('\n')]
        list2 = [float(item) for item in content[1].split('\n')]
        list3 = [float(item) for item in content[2].split('\n')]
    return list1, list2, list3

# Przykładowe użycie
list1, list2, list3 = read_three_lists_from_file('wyniki.txt')
print("Odczytana lista 1:", list1)
print("Odczytana lista 2:", list2)
print("Odczytana lista 3:", list3)



def save_three_2d_lists_to_file(list1, list2, list3, filename):
    """
    Zapisuje trzy dwuwymiarowe listy do jednego pliku.

    Args:
    list1 (list of lists of float): Pierwsza dwuwymiarowa lista.
    list2 (list of lists of float): Druga dwuwymiarowa lista.
    list3 (list of lists of float): Trzecia dwuwymiarowa lista.
    filename (str): Nazwa pliku do zapisu.
    """
    with open(filename, 'w') as file:
        for sublist in list1:
            file.write(' '.join(map(str, sublist)) + "\n")
        file.write("\n")  # Dodajemy pustą linię jako separator
        for sublist in list2:
            file.write(' '.join(map(str, sublist)) + "\n")
        file.write("\n")  # Dodajemy pustą linię jako separator
        for sublist in list3:
            file.write(' '.join(map(str, sublist)) + "\n")

# Przykładowe użycie
list1 = [[1.1, 2.2], [3.3, 4.4]]
list2 = [[5.5, 6.6], [7.7, 8.8]]
list3 = [[9.9, 10.10], [11.11, 12.12]]
save_three_2d_lists_to_file(list1, list2, list3, 'wyniki.txt')


def read_three_2d_lists_from_file(filename):
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
        list3 = [list(map(float, line.split())) for line in content[2].split('\n')]
    return list1, list2, list3

# Przykładowe użycie
list1, list2, list3 = read_three_2d_lists_from_file('wyniki.txt')
print("Odczytana lista 1:", list1)
print("Odczytana lista 2:", list2)
print("Odczytana lista 3:", list3)
