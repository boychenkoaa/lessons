from base import *

class iBlock():
    def __init__(self):
        pass
    
    def __str__(self):
        return "\n <<< ! abstract block ! >>> \n"

# point blocks
# блоки могут однозначно быть представлены строкой - командой для робота (чаще одной, но не обязательно)
# в сам постпроцессор могут прийти разные  траектории
# траектория преобразовывается в набор блоков -- это задача постпроцессора
# разные настройки постпроцессора -- разные используемые блоки
# ну, и по блокам собрать текст УП тоже, но это уже элементарно
# по сути, блоки это промежуточный этап перед окончательной конвертацией в текст УП

class pointBlock(iBlock):
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

class txtBlock(iBlock):
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

# custom blocks

class kwTimerBlock(iBlock):
    def __init__(self, timer_value):
        super().__init__()
        self.timer_value = timer_value

    def __str__(self):
        return ";timer\nTWAIT " + tostr(self.timer_value)

class kwAccuracyBlock(iBlock):
    def __init__(self, accuracy):
        super().__init__()
        self.accuracy = accuracy
    
    def __str__(self):
        return "ACCURACY " + tostr(self.accuracy, 1) + " ALWAYS"

class kwARCONblock(iBlock):
    def __init__(self, proc_num: int):
        super().__init__()
        self.proc_num = proc_num

    def __str__(self):
        return "CALL WELD_PARAMETERS(" +str(self.proc_num) + ")\nCALL arcon"

class Blocks:
    def __init__(self):
        self.blocks = []
    
    def push(self, b: iBlock):
        self.blocks.append(b)
        
    def extend(self, new_blocks):
        self.blocks.extend(new_blocks.blocks)    
        
    def __iter__(self):
        return self.blocks.__iter__()
    
    def __repr__(self):
        return "Blocks: " + str(self.blocks)

class GPointBlock(pointBlock):
    def __init__(self, rpoint: rPoint):
        super().__init__(None, rpoint)  
    
    def _xyz_to_gcode(self, xyz: tuple, precision: int = 1):
        x, y, z = xyz
        ans = ""
        if x != None:
            ans += " X" + tostr(x, precision)
        if y != None:
            ans += " Y" + tostr(y, precision)    
        if z != None:
            ans += " Z" + tostr(z, precision)        
        return ans

class GCodeCommentBlock(txtBlock):
    def __init__(self, txt: str):
        super().__init__(txt)
    
    def __str__(self):
        return "; " + self.txt
    

class G00Block(GPointBlock):
    def __init__(self, rpoint: rPoint):
        super().__init__(rpoint)
    
    def __str__(self):
        return "G00" + self._xyz_to_gcode(self.rpoint.xyz, precision=1)
        
class G01Block(GPointBlock):
    def __init__(self, rpoint: rPoint):
        super().__init__(rpoint)
    
    def __str__(self):
        return "G01" + self._xyz_to_gcode(self.rpoint.xyz, precision=1)        
        
    
