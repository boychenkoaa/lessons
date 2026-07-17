from pymonad.tools import curry
from pymonad.reader import Compose


@curry(2)
def tag_base(tag: str, content: str) -> str:
    return f"<{tag}>{content}</{tag}>"


@curry(2)
def add_attrs(attr: dict, s: str) -> str:
    attrs = " ".join(f'{k}="{v}"' for k, v in attr.items())
    idx = s.index(">")
    return f"{s[:idx]} {attrs}{s[idx:]}"


@curry(3)
def tag(tag_value: str, attr: dict, content: str) -> str:
    return Compose(tag_base(tag_value)).then(add_attrs(attr))(content)


def main():
    result = tag("li")({"class": "list-group", "href": "/page"})("item 23")
    print(result)


if __name__ == "__main__":
    main()
