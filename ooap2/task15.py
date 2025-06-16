'''
Блоки для постпроцессора
Паттерн "посетитель" на минималках
Каждый блок = несколько строк кода для робота
Есть абстрактный класс Block
От него наследуются pointBlock и txtBlock
от них уже наследуются остальные классы блоков
При обходе всех блоков вызывается __str__ и таким образом составляется программа
'''

class Block():
    def __init__(self):
        pass
    
    def __str__(self):
        return "\n <<< ! abstract block ! >>> \n"

class pointBlock(Block):
    def __init__(self, pt_num: int, p9: P9):
        super().__init__()
        self.pt_num = pt_num
        self.p9 = p9
    
    def __str__(self):
        return "<<< " + str(self.pt_num) + " | " + str(self.p9) + ">>>"
 
class pointkwBlock(pointBlock):
    def __init__(self, pt_num: int, p9: P9, z_prefix: str = ""):
        super().__init__(pt_num, p9)
        self.z_prefix = z_prefix
        
    def __str__(self):
        p = self.p9
        z_str = self.z_prefix+tostr(p.z)
        return "POINT p" + str(self.pt_num) + "=TRANS(" + tostr_tpl((p.x, p.y, z_str, p.o, p.a, p.t, 0.0, p.p1, p.p2), 3)+ ")"

class kwLMOVEblock(pointBlock):
    def __init__(self, pt_num: int, p9: P9):
        super().__init__(pt_num, p9)

    def __str__(self):
        return "SPEED " +tostr(self.p9.v, 1) + " MM/S ALWAYS\nLMOVE p" + str(self.pt_num)

class kwC1MOVEblock(pointBlock):
    def __init__(self, pt_num: int, p9: P9):
        super().__init__(pt_num, p9)

    def __str__(self):
        return "C1MOVE p" + str(self.pt_num)

class kwC2MOVEblock(pointBlock):
    def __init__(self, pt_num: int, p9: P9):
        super().__init__(pt_num, p9)

    def __str__(self):
        return "C2MOVE p" + str(self.pt_num)

# text blocks

class txtBlock(Block):
    def __init__(self, txt: str):
        super().__init__()
        self.txt = txt
    
    def __str__(self):
        return self.txt
    
class kwCommentBlock(txtBlock):
    def __init__(self, txt: str):
        super().__init__(txt)

    def __str__(self):
        return ";" + self.txt

class kwARCOFblock(txtBlock):
    def __init__(self, txt: str):
        super().__init__("CALL arcof\n"+txt)

class kwKusakaBlock(txtBlock):
    def __init__(self):
        super().__init__("CALL bite")    
