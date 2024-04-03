
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
        #closed = set()          #T

        openlist.append((node, 0))
        visited_num += 1

        #text = 'a'

        while not len(openlist) == 0:
            v, current_depth = openlist.pop()

            #text += "d" + str(current_depth) + " "
            #if (v.operator != None):
            #    text += str(v.operator) + "\n"
            #text += str(v.state.toStr_state()) + '\n'
            
            if current_depth > reached_depth:
                reached_depth = current_depth

            #if not v in closed: #caly if powinien byc wciety - do pomocniczego print
            if (v.state.isGood() == True):
                    return v, visited_num, closed_num, reached_depth
                
            #closed.add(v)
            closed_num +=1

            if current_depth < 21:#max_depth:
                    for n in reversed(v.neighbours()):
                        #if not n in closed:
                            openlist.append((n, current_depth + 1))
                            visited_num += 1
                    #text += "\n"+"generowani sasiediz"+"\n"
                #else:
                    #text += "\n"+"nawrot"+"\n"
        #with open('.\pom.txt', 'w') as f:
        #    f.write(text)
        print('false')
        return None, visited_num, closed_num, reached_depth