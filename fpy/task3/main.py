from typing import Callable
from functools import reduce
from pymonad.tools import curry

@curry(2)
def tag_base(tag_value: str, s: str) -> str:
    return f"<{tag_value}>{s}</{tag_value}>"


@curry(3)
def tag(tag_value: str, attr: dict, s: str) -> str:
    attrs = " ".join(f'{k}="{v}"' for k, v in attr.items())
    return f"<{tag_value} {attrs}>{s}</{tag_value}>"


def main():
    bold = tag_base("b")
    italic = tag_base("i")
    result = tag('li', {'class': 'list-group'}, 'item 23')
    print(result)

if __name__ == "__main__":
    main()
