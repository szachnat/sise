from Lib.state_table import state_table

class struct:
    def __init__(self, parent: state_table, _operation):
        self.state=parent
        self.operation= _operation

    def print(self):
        self.state.print()
        print(self.operation)

    def get_parent(self):
        return self.state
    
    def get_operation(self):
        return self.operation


class graph_nodes:
    nodes ={}
    def __init__(self):
        self.nodes={}

    def add(self, state: state_table, parent, operation) -> None:
        value=struct(parent,operation)
        print(value.get_parent())
        print(value.get_operation())
        self.nodes[state]=(value)
        print('z init graph-nodes',(self.nodes))
        

    def get_nodes(self):
        return list(self.nodes)


    