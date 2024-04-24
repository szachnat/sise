from Lib.state import state

class graph_node:
    def __init__(self, state:state,parent:state, operator:str):
        self.state=state
        self.parent=parent
        self.operator=operator
    #####################################################################################################
    def neighbours(self) -> list:
            neighbours = self.state.neighbours()
            neighbours_nodes=[]
            for n in neighbours:
                 neighbours_nodes.append(graph_node(n[0],self,n[1]))
            return neighbours_nodes
    #####################################################################################################
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, graph_node):
            return self.state == __value.state
        return super().__eq__(__value)
    #####################################################################################################
    def __hash__(self):
        return hash((self.state))
    