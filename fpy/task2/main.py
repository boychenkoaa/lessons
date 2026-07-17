from typing import Callable
from pymonad.tools import curry

@curry(2)
def cnt(s1:str, s2: str):
    return f"{s1}{s2}"

def hello2(name: str):
    return cnt("Hello, ", name)

@curry(4)
def hello4(hello: str, name: str, sep: str, sign: str):
    return cnt(hello, cnt(sep+" ", cnt(name, sign)))

# замыкание + каррирование
@curry(3)
def first_step(hello: str, sep: str, sign:str) -> Callable:
    def hello_name(name: str):
        return hello4(hello, name, sep, sign)
    return hello_name

def main():
    final = first_step("Hello")(",")("!")
    result = final("Petya")
    print(result)

if __name__ == "__main__":
    main()
