import sys

from Lib.state_table import state_table
from Lib.hashmap_state import graph_nodes


def main(type: str, mode: str, start_filename: str, result_filename: str, info_filename: str):

    with open(start_filename, 'r') as f:
        text = f.read()
    ###############################################################################
    lista=text.split('\n')
    content=[]
    for row in range(len(lista)-1):
        content.append(lista[row].split(" "))
        content[row]=list(map(int,content[row]))
    ###############################################################################
    x = state_table(content)
    y= graph_nodes()
    y.add(x,x,"L")
    x.isGood()
    if (x.isGood()):
        print("true")
    else:
        print("false")
    
    

if __name__ == "__main__":
    # pozyskanie arumentow
    args = sys.argv[1:]
    if len(args) != 5:
        print(f"Oczekiwano 5 argumentów podano {len(args)}")
    else:
        main(args[0], args[1], args[2], args[3], args[4])