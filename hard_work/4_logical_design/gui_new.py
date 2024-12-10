'''
все внутреннее состояние окна храним внутри объекта
'''
from tkinter import *

from editor2d import ksWaamApp
from dataclasses import dataclass

DEFAULT_SLICE_NAME = "Слайс"
DEFAULT_PART_3D_NAME = "Отсутствует"
DEFAULT_ENTRY_WIDTH = 10

tkElement = Entry | Button | Label | Checkbutton

@dataclass
class GridOptions:
    ipadx: int = 5
    sticky: str = "nsew"
    columspan: int = 1

@dataclass
class Element:
    tk_elem: tkElement
    grid_options: GridOptions = GridOptions()
    
Elements = tuple[Element]

@dataclass
class GuiLine:
    def elements(self, parent) -> Elements:
        raise NotImplementedError()
    
@dataclass 
class EntryLine(GuiLine):
    text_left: str
    entry_width: int = DEFAULT_ENTRY_WIDTH
    textvariable: StringVar|None = None
    text_right: str = ""
    
    def elements(self, parent):
        return [Element(tk_elem = Label(parent=parent, text=self.text_left, justify=RIGHT, anchor="e")), 
                Element(tk_elem = Entry(parent=parent, width=self.entry_width, textvariable=self.textvariable)), 
                Element(tk_elem = Label(parent=parent, text=self.text_right))]


@dataclass
class OneButtonLine:
    btn_text: str
    btn_command: callable
    
    def elements(self, parent):
        return []

@dataclass
class CheckBoxLine:
    text: str
    bool_var: BooleanVar = lambda: True

@dataclass    
class TextLine:
    text: str
    is_hint: bool = False
    
@dataclass
class EmptyLine(TextLine):
    text: str = ""

@dataclass
class ValueLine:
    text_left: str
    state_var: StringVar|None = None
    text_right: str|None = None


    
@dataclass
class Frame:
    name: str
    gui_lines: list[GuiLine]

GuiConfiguration = list[Frame]

class ksNotebookWindow(Tk):
    def __init__(self, gui_config: GuiConfiguration):
        self._notebook = ttk.Notebook(self)
        self._notebook.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')
        
        self._from_gui_config(gui_config)
        
    def _from_config(self,  gui_config: GuiConfiguration):
        for frame in gui_config:
            self._add_frame(frame)
        
    def _add_frame(self, frame: Frame):
        new_frame = ttk.Frame(self._notebook)
        self._notebook.add(new_frame, text = frame.name)
        
        for row, gui_line in enumerate(frame.gui_lines):
            self._add_line(new_frame, gui_line, row)
        
        return new_frame
    
    def _add_line(self, parent, gui_line: GuiLine, row: int):
        for col, element in enumerate(gui_line.elements(parent)):
            element.tk_elem.grid(row = row, column = col,
                                 ipadx = element.grid_options.ipadx,
                                 columnspan=element.grid_options.columnspan,
                                 sticky = element.grid_options.sticky)


class WaamGUI:
    def __init__(self, waam_app: ksWaamApp):
        self._init_stringvars()
        self._window = ksNotebookWindow(self.config)

    # возможно эту тучу строковых переменных можно хранить в контейнере более компактно
    def _init_stringvars(self):
        self.str_hstart = StringVar()
        self.str_hmain = StringVar()
        self.str_n = StringVar()
        self.str_n.set("1")
        self.str_name = StringVar()
        self.str_name.set("Слайс")
        self.current_part3d_name = StringVar()
        self.current_part3d_name.set("Отсутствует")
        self.str_snake_angle_deg =  StringVar()
        self.str_snake_angle_deg.set("0")
        self.str_snake_step = StringVar()
        self.str_snake_step.set(10)
        self.str_Npath = StringVar()
        self.str_Npath.set("0")
        self.str_job_name =  StringVar()
        self.str_job_name.set("NC")
        self.str_v = StringVar()
        self.str_o = StringVar()
        self.str_a = StringVar()
        self.str_t = StringVar()
        self.str_p1 = StringVar()
        self.str_p2 = StringVar()
        self.str_arcon = StringVar()
        self.str_arcof = StringVar()
        
        self.str_v_down = StringVar()
        self.str_v_free = StringVar()
        self.str_accuracy = StringVar()
        self.str_h_safe = StringVar()
        self.str_end = StringVar()
        self.str_z_prefix = StringVar()        
        
    @property
    def config(self):
        ans = GuiConfiguration(
            [
                Frame("3D", [
                    TextLine("Слайсер"),
                    EntryLine("Имя семейства слоев", 30, self.str_name, ""), 
                    EntryLine("Начальные высоты (через запятую), мм", 30, self.str_hstart), 
                    EntryLine("Типовая высота", 30, self.str_hmain, "мм"), 
                    EntryLine("Количество слоев", 30, self.str_n, ""), 
                    TextLine("Дождитесь сообщения о завершении", is_hint = True), 
                    OneButtonLine("Получить слайсы", self._cmd_slice)
                ]),
                Frame("2D",
                      [ TextLine("Змейка"), 
                        TextLine("Выделите объект", is_hint = True),
                        EntryLine("Угол -90..90", 30, self.str_snake_angle_deg, "град"), 
                        OneButtonLine("Добавить змейку", self._cmd_add_snake), 
                        TextLine("Лечение слоя"),
                        OneButtonLine("Вылечить слой", self._cmd_repair_slice),
                        EmptyLine(), 
                        TextLine("Контура"), 
                        OneButtonLine("Реверс", self._cmd_reverse),
                        TextLine("Конвертация"),
                        OneButtonLine("Контур -> автолиния", self._convert_contour_to_autoline),
                        TextLine("Маркеры"),
                        OneButtonLine("Показать маркеры", self._cmd_show_markers),
                        OneButtonLine("Скрыть маркеры", self._cmd_remove_markers),
                      ]
                      ),
                Frame("Path",[]),
                Frame("Job",[]),
                Frame("NC",[]), 
                
            ]
        )
        return ans
        
    def _cmd_add_snake(self):
        ...
    
    def _cmd_repair_slice(self):
        ...
    
    def _cmd_slice(self):
        ...
        
    def _cmd_reverse(self):
        ...
    
    def _cmd_show_markers(self):
        ...
        
    def _cmd_remove_markers(self):
        ...
        
    def _convert_contour_to_autoline(self):
        ...
        
    def _cmd_reset(self):
        ...
        
    def _cmd_append_to_buf(self):
        ...
        
    def _cmd_clean(self):
        ...
        
    def _cmd_export(self):
        ...
        
        