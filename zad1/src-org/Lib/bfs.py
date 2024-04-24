from collections import deque

from Lib.graph import graph_node

class BFS:
    #####################################################################################################
    def get_result(self,node:graph_node):
        if node.state.isGood():
            return node, 1, 1, 0
        
        # potrzebne później w pliku z info
        visited_num = 0
        closed_num = 0
        reached_depth = 0

        #listy stanów
        openlist = deque()
        visitedlist = set()

        openlist.append((node,0))
        visitedlist.add(node)
        visited_num += 1

        while not len(openlist) == 0:
            v, current_depth = openlist.popleft()

            if current_depth > reached_depth:
                reached_depth = current_depth

            closed_num += 1
            
            for n in v.neighbours():
                if not n in visitedlist:
                    visitedlist.add(n)
                    visited_num += 1
                    if (n.state.isGood() == True):
                        return n, visited_num, closed_num, reached_depth+1
                    openlist.append((n,current_depth + 1))
                    
        print('false')
        return None, visited_num, closed_num, reached_depth

