from enum import Enum


class TextType(Enum):
    TEXT = "text"
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, type: TextType, url: str = None):
        self.text = text
        self.type = type
        self.url = url

    def __eq__(self, other):
        if [self.text, self.type, self.url] == [other.text, other.type, other.url]:
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.type}, {self.url})"
