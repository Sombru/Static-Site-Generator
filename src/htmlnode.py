class HTMLNode:
    def __init__(
        self, tag: str = None, value: str, children: list[HTMLNode], props: dict[str:str]
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
  