from copy import deepcopy, copy
from json import dumps, loads

class General(object):
    def __init__(self):
        pass

    def __deepcopy__(self):
        return super().__deepcopy__()

    def __copy__(self):
        return super().__copy__()

    def __repr__(self):
        return dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __str__(self):
        return dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, json_str:  str):
        self.__dict__ = loads(json_str)
        return self
        
    def serialize(self):
        ob = dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        return ob
        
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def is_deep_eq(self, other):
        if type(self) != type(other):
            return False
            
        if self.__dict__.keys() != other.__dict__.keys():
            return False
            
        for key, value in self.__dict__.items():
            other_value = other.__dict__[key]
            
            if isinstance(value, General):
                if not value.is_deep_eq(other_value):
                    return False
            elif value != other_value:
                return False

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def get_type(self):
        return type(self)
    
    def is_instance(self, instance):
        return isinstance(self, instance)

class Any(General):
    def __init__(self):
        super().__init__()
