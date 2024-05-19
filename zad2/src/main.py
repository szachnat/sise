
from Reader import Reader
from network import Layer,sigmoidal_function, derivative_of_sigmoidal_function,identity_function,derivative_of_identity_function,MLP


def main() -> None:
    print("Reading data...")
    reader = Reader()
    learning_data = reader.load_learning_data()
    testing_data = reader.load_testing_data()
    #print(learning_data)
    #print(testing_data)

def test_layer_MLP():
    x= Layer(2, 1, identity_function, derivative_of_identity_function)
    #Layer.print(x)
    y= Layer(3, 2, sigmoidal_function, derivative_of_sigmoidal_function)
    #Layer.print(y)
    z= Layer(2, 3, sigmoidal_function, derivative_of_sigmoidal_function)
    #Layer.print(z)

    #print('a')
    a=MLP([2])
    MLP.print(a)
    a.learn([1,2],[1,2])
    MLP.print(a)
    #print("b")
    #b=MLP([2,3,2])
    #MLP.print(b)

if __name__ == "__main__":
    main()
    test_layer_MLP()
