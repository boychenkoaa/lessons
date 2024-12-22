import pythoncom
from win32com.client import Dispatch, gencache
from tkinter import *
from global_var import * 

# Класс - точка входа в приложение, связь с API компаса
# задействуется в логике более высоких уровней (kompasManipulator3d, kompasManipulator2d)
# через вызов app.api7.<здесь метод API>
# to5 и to7 конвертируют объекты api 7 и 5 версии в их аналоги в 5 и 7 соответственно
# через свойства api5 и api7 идет доступ к дочерним методам, описанным в документации к SDK
# если создан до запуска Компаса, вносит необратимые до перезагрузки изменения в реестр -- нужна перезагрузка ОС

class KompasApp:
    def __init__(self):
        self.constants = gencache.EnsureModule("{75C9F5D0-B5B8-4526-8681-9903C567D2ED}", 0, 1, 0).constants
        self.constants_3d = gencache.EnsureModule("{2CAF168C-7961-4B90-9DA2-701419BEEFE3}", 0, 1, 0).constants

        # Подключаемся к API5
        self._api5 = gencache.EnsureModule("{0422828C-F174-495E-AC5D-D31014DBBE87}", 0, 1, 0)
        self._object5 = self._api5.KompasObject(Dispatch("Kompas.Application.5")._oleobj_.QueryInterface(self._api5.KompasObject.CLSID, pythoncom.IID_IDispatch))
        
        # Подключаемся к API7
        self._api7 = gencache.EnsureModule("{69AC2981-37C0-4379-84FD-5DD2F3C0A520}", 0, 1, 0)
        self._object7 = self.api7.IKompasAPIObject(Dispatch("Kompas.Application.7")._oleobj_.QueryInterface(self.api7.IKompasAPIObject.CLSID, pythoncom.IID_IDispatch))
        
        # Подключение к нтерфейсу программы Kompas 3D
        print("Подключение к КОМПАС...")
        self.app7 = self._object7.Application      # Получаем основной интерфейс
        self.app7.Visible = True    # Показываем окно пользователю (если скрыто)
        #self.app7.HideMessage = self.constants.ksHideMessageNo   # Отвечаем НЕТ на любые вопросы программы
        self.application = self.api7.IApplication(Dispatch("Kompas.Application.7")._oleobj_.QueryInterface(self.api7.IApplication.CLSID, pythoncom.IID_IDispatch))
    
    @property
    def api7(self):
        return self._api7
    
    @property
    def object5(self):
        return self._object5
        
    @property
    def active_doc(self):
        return self.application.ActiveDocument

    @property
    def active_doc3d(self):
        doc = self.active_doc
        if doc == None:
            raise ValueError("Нет активного 3D-документа")
        return self.api7.IKompasDocument3D(doc)
    
    @property
    def active_doc2d(self):
        doc = self.active_doc
        if doc == None:
            raise ValueError("Нет активного 2D-документа")        
        return self.api7.IKompasDocument2D(doc)    
    
    def to5(self, object):
        return self.object5.TransferInterface (object, 1, 2)
    
    def to7(self, object):
        return self.object5.TransferInterface (object, 2, 1)
    
    @property
    def active_doc_dim(self):
        if self.active_doc.DocumentType == 2:
            return 2
        if self.active_doc.DocumentType == 4:
            return 3
        return None
    

def to_tuple(variant_entity):
    if variant_entity is None:
        return tuple([])
    if type(variant_entity) == tuple:
        return variant_entity
    return tuple([variant_entity])

