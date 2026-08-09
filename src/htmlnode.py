from __future__ import annotations

from textnode import TextNode, TextType

class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        res = ""
        for key, value in self.props.items():
            res += f' {key}="{value}"'
        return res

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("Expected value in LeafNode")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None) -> str:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Expected tag in ParentNode")
        if not self.children:
            raise ValueError("Expected children in ParentNode")
        res = f"<{self.tag}>"
        for node in self.children:
            res += node.to_html()
        res += f"</{self.tag}>"
        return res


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.type not in TextType:
        raise NotImplementedError(f"Node type: {text_node.type} is not supported")

    if text_node.type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
