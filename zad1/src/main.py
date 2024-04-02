import sys
import time

from Lib.state import state, StateError
from Lib.graph import graph_node
from Lib.bfs import BFS

def text_split(text:list[list[str]]):
    text=text.split('\n')
    size=text[0].split(" ")
    size=list(map(int,size))
    box=[]
    for row in range(len(text)-2):
        box.append(text[row+1].split(" "))
        box[row]=list(map(int,box[row]))
    return size[0],size[1],box
#####################################################################################################
def make_moves_from_results(end_node: graph_node):
    temp_node = end_node
    moves  = [temp_node.operator]

    while (temp_node.parent) != None:
        temp_node = temp_node.parent
        moves.insert(0, temp_node.operator)
        
    moves.remove(None)
    return moves
#####################################################################################################
def make_result_file(filename: str, end_node: graph_node):
    if end_node != None:
        moves = make_moves_from_results(end_node)
        text = f"{len(moves)}\n{''.join(moves)}"
    else:
        text = '-1'
    with open(filename, 'w') as f:
        f.write(text)
#####################################################################################################
def make_info_file(filename: str, end_node: graph_node, visited_num: int, closed_num: int, reached_depth: int, total_time: float):
    if end_node != None:
        moves = make_moves_from_results(end_node)
        text = f"{len(moves)}\n"
    else:
        text = '-1\n'

    # liczba stanów odwiedzonych
    text += f"{visited_num}\n"

    # liczba stanów przetworzonych
    text += f"{closed_num}\n"

    # maksymalna osiągnięta głębokość rekursji
    text += f"{reached_depth}\n"

    # czas trwania procesu obliczeniowego w milisekundach (z dokładnością do 3 miejsc po przecinku)
    text += f"{round(total_time, 3)}"

    with open(filename, 'w') as f:
        f.write(text)
#####################################################################################################
def do_bfs(box:list[list[int]], rows:int, columns:int, mode:str):
    bfs = BFS()
    start_node = graph_node(state(rows, columns, box, mode), None, None)

    # BFS
    start_time = time.time()
    result = bfs.get_result(start_node)
    total_time = time.time() - start_time
    return result, total_time
#####################################################################################################
def main(type: str, mode: str, start_filename: str, result_filename: str, info_filename: str):

    with open(start_filename, 'r') as f:
        text = f.read()
    
    rows,columns,box=text_split(text)

    try:
        if type == 'bfs':
            (end_node, visited_num, closed_num, reached_depth), total_time = do_bfs(box, rows, columns, mode)
        #elif type == 'dfs':
        #    (end_node, visited_num, closed_num, reached_depth), total_time = do_dfs(box, rows, columns, mode)
        #elif type == 'astr':
        #    (end_node, visited_num, closed_num, reached_depth), total_time = do_astar(box, rows, columns, mode)
        else:
            print(f"Nie została zaimplementowana metoda o podanym akronimie '{type}'.\nDostępne to: 'bfs', 'dfs' oraz 'astr'")
            return
    except StateError as se:
        print(se.msg)
        return
    
    make_result_file(result_filename, end_node)
    make_info_file(info_filename, end_node, visited_num, closed_num, reached_depth, total_time)
#####################################################################################################
if __name__ == "__main__":
    # pozyskanie arumentow
    args = sys.argv[1:]
    if len(args) != 5:
        print(f"Oczekiwano 5 argumentów podano {len(args)}")
    else:
        main(args[0], args[1], args[2], args[3], args[4])