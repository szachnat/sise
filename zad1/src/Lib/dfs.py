
from Lib.graph import graph_node

class DFS:
    #####################################################################################################
    def get_result(self, node:graph_node):
        if node.state.isGood():
            return node, 1, 1, 0
        
        # potrzebne później w pliku z info
        visited_num = 0
        closed_num = 0
        reached_depth = 0

        openlist = []           #S
        closed = dict()#set()          #T

        openlist.append((node, 0))
        visited_num += 1

        while not len(openlist) == 0:
            v, current_depth = openlist.pop()
            
            if current_depth > reached_depth:
                reached_depth = current_depth

            if not v in closed: 
                if (v.state.isGood() == True):
                        return v, visited_num, closed_num, reached_depth
                    
                closed[v]=current_depth
                closed_num +=1

                if current_depth < 21:
                        for n in reversed(v.neighbours()):
                            openlist.append((n, current_depth + 1))
                            visited_num += 1
            else:
                if (closed.get(v) > current_depth):
                     openlist.append((v,current_depth))
                     closed.pop(v)
                     closed_num -= 1

        print('false')
        return None, visited_num, closed_num, reached_depth