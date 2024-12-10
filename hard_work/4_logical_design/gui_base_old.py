from tkinter import *
from tkinter.messagebox import showerror, showinfo
from tkinter.filedialog import asksaveasfilename, askopenfilename
import tkinter.font as tkFont
from global_var import * 


def add_entry_line(parent, row: int, text_left: str, entry_width: int|None = None, textvariable: StringVar|None = None, text2: str|None = None):
    lbl_left =  Label(parent, text=text_left, justify=RIGHT, anchor="e")
    lbl_left.grid(column = 0, row=row, sticky='nsew', ipadx=5)
    if entry_width != None:
        txt_entry = Entry(parent,width=entry_width,textvariable=textvariable)
        txt_entry.grid(column=1, ipadx=5, row=row)
    if text2 != None:
        lbl_right =  Label(parent, text=text2)
        lbl_right.grid(column = 2, row=row, sticky='nsew', ipadx=5)
    return row + 1

def add_state_line(parent, row, text_left: str, state_var: StringVar|None = None, text_right: str|None = None):
    lbl_left =  Label(parent, text=text_left, justify=RIGHT, anchor="e")
    lbl_left.grid(column = 0, row=row, sticky='nsew', ipadx=5)
    if state_var != None:
        lbl_state = Label(parent, textvariable=state_var, justify=LEFT)
        lbl_state.grid(column = 1, row=row, sticky='nsew', ipadx=5)
    if text_right != None:
        lbl_right =  Label(parent, text=text_right)
        lbl_right.grid(column = 2, row=row, sticky='nsew', ipadx=5)    
    return row + 1

def add_button_line(parent, row: int, btn_text: str, btn_command: callable):
    btn = Button(parent, text=btn_text, command = btn_command)
    btn.grid(column=0, row=row, ipadx=5, sticky='nsew', columnspan = 3)    
    return row + 1

def add_checkbox_line(parent, row: int, text: str, bool_var: BooleanVar = lambda: True):
    add_text_chk = Checkbutton(parent, text=text, var=bool_var)
    add_text_chk.grid(column=0, row=row, sticky='w', ipadx=5)
    return row + 1

def add_header_line(parent, row, text, is_hint=False):
    if is_hint:
        lbl_left =  Label(parent, text=text, justify=LEFT, anchor="w", font =hint_font)
    else:
        lbl_left =  Label(parent, text=text, justify=LEFT, anchor="w")
        
    lbl_left.grid(column = 0, row=row, sticky='nsew', ipadx=5, columnspan=3)
    return row + 1