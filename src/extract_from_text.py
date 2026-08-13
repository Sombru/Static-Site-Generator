from textnode import TextNode, TextType
import re

def extract_from_node(node: TextNode, delimiter: str, text_type: TextType) -> list[TextNode]:
    if node.text.count(delimiter) % 2 != 0:
        raise Exception(f"Expected closing delimiter: {delimiter}")

    nodes = []
    splited = node.text.split(delimiter)
    for i in range(len(splited)):
        if not splited[i]:
            continue
        if i % 2 == 0:
            nodes.append(TextNode(splited[i], TextType.TEXT))
        else:

            nodes.append(TextNode(splited[i], text_type))
    return nodes


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    res: list[TextNode] = []
    for node in old_nodes:
        if node.type != TextType.TEXT:
            res.append(node)
        else:
            res.extend(extract_from_node(node, delimiter, text_type))

    return res


def extract_markdown_images(text) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    res = []
    for old_node in old_nodes:
        if old_node.type != TextType.TEXT:
           res.append(old_node)
           continue
        links = extract_markdown_links(old_node.text)
        if not links:
            res.append(TextNode(old_node.text, TextType.TEXT))
        remainitng_text = ""
        for link in links:
            if not remainitng_text:
                sections: list[str] = old_node.text.split(f"[{link[0]}]({link[1]})", 1)
            else:
                sections: list[str] = remainitng_text.split(f"[{link[0]}]({link[1]})", 1)
            # for i in range(len(sections)):
            if not sections[0]:
                res.append(TextNode(link[0], TextType.LINK, link[1]))
            else:
                res.append(TextNode(sections[0], TextType.TEXT))
                res.append(TextNode(link[0], TextType.LINK, link[1]))
            new = "".join(sections)
            remainitng_text = "".join(sections[1:])
        if remainitng_text:
            res.append(TextNode(remainitng_text, TextType.TEXT))
            # print("remaining_text:", remainitng_text)
    return res

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    res = []
    for old_node in old_nodes:
        print(old_node)
    for old_node in old_nodes:
        if old_node.type != TextType.TEXT:
            res.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        if not images:
            res.append(TextNode(old_node.text, TextType.TEXT))
        remainitng_text = ""
        for image in images:
            if not remainitng_text:
                sections: list[str] = old_node.text.split(f"![{image[0]}]({image[1]})", 1)
            else:
                sections: list[str] = remainitng_text.split(f"![{image[0]}]({image[1]})", 1)
            # for i in range(len(sections)):
            if not sections[0]:
                res.append(TextNode(image[0], TextType.IMAGE, image[1]))
            else:
                res.append(TextNode(sections[0], TextType.TEXT))
                res.append(TextNode(image[0], TextType.IMAGE, image[1]))
            new = "".join(sections)
            remainitng_text = "".join(sections[1:])
        if remainitng_text:
            res.append(TextNode(remainitng_text, TextType.TEXT))
            # print("remaining_text:", remainitng_text)
    return res

def text_to_textnodes(text: str) -> list[TextNode]:
    italic_delimiter: str = "_"
    bold_delimiter: str = "**"
    code_block_delimiter: str = "`"
    initital = TextNode(text, TextType.TEXT)
    res = []
    res.append(initital)
    res = split_nodes_link(res)
    res = split_nodes_image(res)
    res = split_nodes_delimiter(res, italic_delimiter, TextType.ITALIC)
    res = split_nodes_delimiter(res, bold_delimiter, TextType.BOLD)
    res = split_nodes_delimiter(res, code_block_delimiter, TextType.CODE)
    
    return res

# def main():
#     str = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) check it out"
#     nodes = text_to_textnodes(str)
#     print("==========================")
#     for a in nodes:
#         print(a)
# main()
