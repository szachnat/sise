

class state_table:
    size = []
    content = []
    zero = []        
                
    def __init__(self,_content:list):
        self.size=(_content[0])
        #print(self.size)

        for row in range(len(_content)-1):
            self.content.append(_content[row+1])
        #print(self.content)

        for y in range(self.size[0]):
            for x in range(self.size[1]):
                if (self.content[x][y] == 0):
                    self.zero=[x,y]
        #print(self.zero)
                    
    def __hash__(self):
        size = str(self.size)
        content = str(self.content)
        zero=str(self.zero)
        return hash((size, content, zero))
    
    def print(self):
        print(self.content)

    def isGood(self):
        #print('size',self.size[0]," ",self.size[1])
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                #print(x,y, self.content[x][y])
                if (self.content[x][y] != (x*4+y+1)):
                    return False
        return True
    