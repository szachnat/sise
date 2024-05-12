from copy import deepcopy

class StateError(Exception):
    def __init__(self, msg, *args: object) -> None:
        super().__init__(*args)
        self.msg = msg

class state:       
    #####################################################################################################        
    def __init__(self, rows:int,columns:int, box:list[list[int]],mode:str):
        if not self.__is_mode_good(mode):
            raise StateError(f"Wprowadzony tryb {mode} nie jest permutacją ('L', 'R', 'U', 'D')")
        if rows <= 0:
            raise StateError(f"Wprowadzona ilość wierszy ({rows}) jest nieprawidłowa powinna ona być > 0")
        if columns <= 0:
            raise StateError(f"Wprowadzona ilość kolumn ({columns}) jest nieprawidłowa powinna ona być > 0")
        if len(box) != rows:
            raise StateError(f"Ilość wierszy w wprowadzonym pudełku ({len(box)}) nie jest równa podanej ilości wierszy ({rows})")
        for w in range(rows):
            if len(box[w]) != columns:
                raise StateError(f"Ilość kolumn w wierszu nr {w+1} ({len(box[w])}) nie jest równa podanej ilości kolumn ({columns})")
            
        self.rows=(rows)
        self.columns=(columns)
        self.box: list[list[int]] = box

        # szukanie pozycji wartości 0
        # oraz powinny się znajdować liczby od 0 do w*k-1
        unique_numbers: set[int] = set()
        pos_0s: tuple[int, int] = []
        for w in range(self.rows):
            for k in range(self.columns):
                unique_numbers.add(box[w][k])
                if box[w][k] == 0:
                    pos_0s.append((w, k))

        if len(pos_0s) == 0:
            raise StateError("Brakuje wolnego miejsca w wprowadzonym pudełku oznaczonego liczbą 0")
        elif len(pos_0s) != 1:
            raise StateError(f"Powinno być tylko jedno wolne miejsce w wprowadzonym pudełku oznaczone liczbą 0 zaś jest ich {len(pos_0s)}")

        for i, num in enumerate(sorted(unique_numbers)):
            if num != i:
                raise StateError(f"Liczby w pudełku powinny być od 0 do {self.rows*self.columns-1}")

        if len(unique_numbers) != self.rows*self.columns:
            raise StateError("Znaleziono jedną lub więcej liczb więcej niż jeden raz w wprowadzonym pudełku")

        self.w_0, self.k_0 = pos_0s[0]
        self.mode = mode
    #####################################################################################################
    def __is_mode_good(self, mode: str) -> bool:
        if len(mode) != 4:
            return False
        unique: set[str] = set()
        for c in mode:
            if c not in ('L', 'D', 'U', 'R'):
                return False
            unique.add(c)
        if len(unique) != 4:
            return False
        return True
    #####################################################################################################
    def toStr_state(self)->str:
        text = 'state:\n'
        for w in range(self.rows):
            for k in range(self.columns):
                text+=str(self.box[w][k])
                if k < self.columns - 1:
                    text += " "
            if w < self.rows - 1:
                text += "\n"
        return text
    #####################################################################################################
    def __hash__(self):
        return hash((str(self.box)))
    #####################################################################################################
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, state):
            if self.rows != __value.rows:
                return False
            if self.columns != __value.columns:
                return False
            for w in range(self.rows):
                for k in range(self.columns):
                    if self.box[w][k] != __value.box[w][k]:
                        return False
            return True
        return super().__eq__(__value)
    #####################################################################################################
    def isGood(self):
        for x in range(self.rows):
            for y in range(self.columns):
                if (self.box[x][y] != (x*self.rows+y+1) and self.box[x][y] != 0):
                    return False
        return True
    #####################################################################################################
    def neighbours(self)->list:
        neighbours=[]
        for letter in self.mode:
            if letter == 'U':
                if self.w_0 > 0:
                    neighbours.append((self.U_neighbour(),"U"))
            elif letter == 'R':
                if self.k_0 <self.columns - 1:
                    neighbours.append((self.R_neighbour(),"R"))
            elif letter == 'D':
                if self.w_0 < self.rows - 1:
                    neighbours.append((self.D_neighbour(),"D"))
            elif letter == 'L':
                if self.k_0 > 0:
                    neighbours.append((self.L_neighbour(),"L"))       
        return neighbours
    #####################################################################################################
    def U_neighbour(self):
        neighbour=deepcopy(self.box)
        neighbour[self.w_0][self.k_0], neighbour[self.w_0 - 1][self.k_0] = neighbour[self.w_0 - 1][self.k_0], neighbour[self.w_0][self.k_0]
        return state(self.rows,self.columns,neighbour,self.mode)
    #####################################################################################################
    def R_neighbour(self):
        neighbour=deepcopy(self.box)
        neighbour[self.w_0][self.k_0], neighbour[self.w_0][self.k_0 + 1] = neighbour[self.w_0][self.k_0 + 1], neighbour[self.w_0][self.k_0]
        return state(self.rows,self.columns,neighbour,self.mode)
    #####################################################################################################
    def D_neighbour(self):
        neighbour=deepcopy(self.box)
        neighbour[self.w_0][self.k_0], neighbour[self.w_0 + 1][self.k_0] = neighbour[self.w_0 + 1][self.k_0], neighbour[self.w_0][self.k_0]
        return state(self.rows,self.columns,neighbour,self.mode)
    #####################################################################################################
    def L_neighbour(self):
        neighbour=deepcopy(self.box)
        neighbour[self.w_0][self.k_0], neighbour[self.w_0][self.k_0 - 1] = neighbour[self.w_0][self.k_0 - 1], neighbour[self.w_0][self.k_0]
        return state(self.rows,self.columns,neighbour,self.mode)
    #####################################################################################################
    def getMode(self):
        return self.getOperator
    