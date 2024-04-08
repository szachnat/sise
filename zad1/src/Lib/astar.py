import queue

from Lib.graph import graph_node
from Lib.state import state

class PriorityQueue:
    #####################################################################################################
    def __init__(self) -> None:
        self.items = {}
    #####################################################################################################
    def put(self, item: object, prority: int) -> None:
        if not self.items.get(prority, None):
            self.items[prority] = queue.Queue()
        self.items[prority].put(item)
    #####################################################################################################
    def get(self) -> object | None:
        for k in sorted(self.items.keys()):
            if not self.items[k].empty():
                return self.items[k].get()
        return None
    #####################################################################################################
    def empty(self) -> bool:
        for k in self.items.keys():
            if not self.items[k].empty():
                return False
        return True
#####################################################################################################   
class HeuristicError(Exception):
    #####################################################################################################
    def __init__(self, msg, *args: object) -> None:
        super().__init__(*args)
        self.msg = msg
#####################################################################################################
class ASTAR:
    #####################################################################################################
    def get_result(self, node: graph_node, goal:state, mode:str):
        if node.state.isGood():
            return node, 1, 1, 0
        
        if mode == 'hamm':
            heuristic = self.hamming_heuristic
        elif mode == 'manh':
            heuristic = self.manhattan_heuristic
        
        # potrzebne później w pliku z info
        visited_num = 0
        closed_num = 0
        reached_depth = 0

        priority = PriorityQueue()
        closedlist=set()
        priority.put((node, 0, 0), 0)
        visited_num += 1

        while not priority.empty():
            v, current_g, current_depth = priority.get()

            #print(v.state.toStr_state())
            if current_depth > reached_depth:
                reached_depth = current_depth

            if not (v in closedlist):

                closedlist.add(v)
                closed_num += 1

                if v.state.isGood():
                    return v, visited_num, closed_num, reached_depth
                
                for n in v.neighbours():
                    if not (n in closedlist):
                        visited_num += 1
                        n_g = current_g + heuristic(node.state, n.state)
                        n_h = heuristic(n.state, goal)
                        f = n_g + n_h
                        priority.put((n, n_g, current_depth + 1), f)
        print('false')
        return None, visited_num, closed_num, reached_depth
    #####################################################################################################
    def hamming_heuristic(self, s1: state, s2: state) -> int:
        if s1.rows != s2.rows:
            raise HeuristicError("Oba objekty State mają inną ilość wierszy co uniemożliwia zastosowanie heurystyki Hamminga")
        if s1.columns != s2.columns:
            raise HeuristicError("Oba objekty State mają inną ilość kolumn co uniemożliwia zastosowanie heurystyki Hamminga")
        
        bad = 0
        for w in range(s1.rows):
            for k in range(s1.columns):
                if(s1.box[w][k] != s2.box[w][k]):
                    bad += 1
        return bad
    #####################################################################################################
    def manhattan_heuristic(self, s1: state, s2: state) -> int:
        if s1.rows != s2.rows:
            raise HeuristicError("Oba objekty State mają inną ilość wierszy co uniemożliwia zastosowanie heurystyki Hamminga")
        if s1.columns != s2.columns:
            raise HeuristicError("Oba objekty State mają inną ilość kolumn co uniemożliwia zastosowanie heurystyki Hamminga")
        
        distance = 0
        for w in range(s1.rows):
            for k in range(s1.columns):
                distance += abs(s1.box[w][k] - s2.box[w][k])
        return distance