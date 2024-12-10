import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
from gui_base import *
from gui_commands import *
from global_var import * 
import os

def init_window():
    notebook = ttk.Notebook(window)
    notebook.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')
    frame3d = ttk.Frame(notebook)
    notebook.add(frame3d, text = "3D")
    frame2d = ttk.Frame(notebook)
    notebook.add(frame2d, text = "2D")
    frame_job = ttk.Frame(notebook)
    notebook.add(frame_job, text = "JOB")
    frame_path = ttk.Frame(notebook)
    notebook.add(frame_path, text = "PATH")
    frame_buf = ttk.Frame(notebook)
    notebook.add(frame_buf, text = "BUF")    
    
    row = 1
    row = add_header_line(frame3d, row, "Слайсер")
    row = add_entry_line(frame3d, row, "Имя семейства слоев (уникальное)", 30, str_name, "")
    row = add_entry_line(frame3d, row, "Начальные высоты (через запятую), мм", 30, str_hstart)
    row = add_entry_line(frame3d, row, "Типовая высота", 30, str_hmain, "мм")
    row = add_entry_line(frame3d, row, "Количество слоев", 30, str_n, "")
    row = add_header_line(frame3d, row, "Дождитесь сообщения о завершении", True)
    row = add_button_line(frame3d, row, "Получить слайсы", cmd_slice)
    
    row = 1
    row = add_header_line(frame2d, row, "Змейка (выделите объект)")
    row = add_entry_line(frame2d, row, "Угол -90 ... 90", 30, str_snake_angle_deg, "град")
    row = add_entry_line(frame2d, row, "Шаг", 30, str_snake_step, "мм")
    row = add_button_line(frame2d, row, "Добавить змейку", cmd_add_snake)
    row = add_header_line(frame2d, row, " ")
    row = add_header_line(frame2d, row, "Лечение слоя (предварительно проверьте контура на \nзамкнутость средствами компаса и сохраните точки разрыва)", True)
    row = add_button_line(frame2d, row, "Вылечить слой", cmd_repair_slice)
    row = add_header_line(frame2d, row, "")
    row = add_header_line(frame2d, row, "Контура")
    row = add_header_line(frame2d, row, "Реверс (только для дуг, отрезков и контуров из отрезков и дуг)", True)
    row = add_button_line(frame2d, row, "Реверс", cmd_reverse)
    row = add_header_line(frame2d, row, "Конвертация", True)
    row = add_button_line(frame2d, row, "Контур -> Автолиния", cmd_contour_to_autoline)
    row = add_header_line(frame2d, row, "Маркеры", True)
    row = add_button_line(frame2d, row, "Показать маркеры старт и стоп (у контуров)", cmd_show_contours_BE)
    row = add_button_line(frame2d, row, "Удалить маркеры старт и стоп (у контуров)", cmd_remove_all_points)
    
    row = 1
    row = add_header_line(frame_buf, row, "Привязка к детали")
    row = add_header_line(frame_buf, row, "Если деталь не указана, то добавление работает некорректно", True)
    row = add_state_line(frame_buf, row, "Текущая деталь", state_var = current_part3d_name)
    row = add_button_line(frame_buf, row, "Запомнить деталь", cmd_reset)
    row = add_header_line(frame_buf, row, " ")
    row = add_entry_line(frame_buf, row, "Название УП", 30, str_job_name)
    
    row = add_header_line(frame_buf, row, " ")
    row = add_header_line(frame_buf, row, "Можно добавлять только отрезки, автолинии и контура из отрезков и дуг", True)
    row = add_header_line(frame_buf, row, "При добавлении автолинии нужно выделить только первый ее элемент", True)
    row = add_button_line(frame_buf, row, "Добавить", cmd_append_to_buffer)
    row = add_button_line(frame_buf, row, "Очистить", cmd_clean)
    row = add_button_line(frame_buf, row, "Удалить последнюю", cmd_pop)
    row = add_button_line(frame_buf, row, "Подробнее", lambda: True)
    row = add_header_line(frame_buf, row, " ")
    row = add_state_line(frame_buf, row, "Всего траекторий", str_Npath)
    row = add_header_line(frame_buf, row, " ")
    row = add_entry_line(frame_buf, row, "Экспорт УП")
    row = add_button_line(frame_buf, row, "Экспортировать УП", cmd_export)
    
    row = 1
    row = add_header_line(frame_path, row, "Параметры траектории")
    row = add_header_line(frame_path, row, "Пустые поля игнорируются при задании и не допускаются при сохранении", True)
    row = add_entry_line(frame_path, row, "Скорость", 30, str_v, "v")
    row = add_entry_line(frame_path, row, "Номер сварочной программы", 30, str_arcon, "arcon")
    row = add_entry_line(frame_path, row, "Команды после arcof (*)",  30, str_arcof, "arcof")
    row = add_header_line(frame_path, row, "Углы наклона горелки (углы Эйлера ZYZ)", True)
    row = add_entry_line(frame_path, row, "Угол O", 30, str_o, "o")
    row = add_entry_line(frame_path, row, "Угол A", 30, str_a, "a")
    row = add_entry_line(frame_path, row, "Угол T", 30, str_t, "t")
    row = add_header_line(frame_path, row, "Углы поворота осей позиционера**", True)
    row = add_entry_line(frame_path, row, "Первая ось**", 30, str_p1, "p1")
    row = add_entry_line(frame_path, row, "Вторая ось**", 30, str_p2, "p2")
    row = add_header_line(frame_path, row, "* - Для разделения команд используйте разделитель \\n, например: Команда1\\nКоманда2", True)
    row = add_header_line(frame_path, row, "** - Только для опытных пользователей", True)    
    row = add_button_line(frame_path, row, "Задать выделенному**", cmd_send_pathprop)
    row = add_button_line(frame_path, row, "Очистить", cmd_clean_pathprop)
    row = add_button_line(frame_path, row, "Восстановить", cmd_restore_pathprop)
    row = add_button_line(frame_path, row, "Сохранить", cmd_set_pathprop)

    
    row = 1
    row = add_header_line(frame_job, row, "Параметры УП")
    row = add_header_line(frame_job, row, "Обязательные поля (пустые не допускаются)", True)
    row = add_entry_line(frame_job, row, "Скорость подхода к первой точке", 30, str_v_down, "v_down")
    row = add_entry_line(frame_job, row, "Скорость свободного перемещения", 30, str_v_free, "v_free    ")
    row = add_entry_line(frame_job, row, "Радиус скругления углов, мм",  30, str_accuracy, "accuracy")
    row = add_entry_line(frame_job, row, "Высота безопасного отвода ", 30, str_h_safe, "h_safe")
    row = add_header_line(frame_job, row, "Необязательные поля (допускаются пустые)", True)
    row = add_entry_line(frame_job, row, "Текст перед координатой z точки*", 30, str_z_prefix, "z_prefix")
    row = add_entry_line(frame_job, row, "Команды в конце файла**", 30, str_end, "end")
    row = add_header_line(frame_job, row, "* - Используется для повторяющегося слоя, в котором меняется только высота", True)
    row = add_header_line(frame_job, row, "** - Для разделения команд используйте разделитель \\n, например: Команда1\\nКоманда2", True)
    row = add_button_line(frame_job, row, "Восстановить", cmd_restore_jobprop)
    row = add_button_line(frame_job, row, "Сохранить", cmd_set_jobprop)    
 
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=12)    

if not validate_dict(default_job_props, job_own_keys):
    showerror(title="Ошибка", message="Не задан один или несколько параметров УП по умолчанию")  
    
if not validate_dict(default_path_props, path_keysW):
    showerror(title="Ошибка", message="Не задан один или несколько параметров траектории по умолчанию") 


window.title("WAAM")
window.iconbitmap(LWMS_ICO_FILENAME)
init_window()
cmd_restore_jobprop()
cmd_set_pathprop()
window.mainloop()
