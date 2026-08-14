import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from extract_from_text import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_link,
    split_nodes_image,
    split_nodes_delimiter,
    text_to_textnodes,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "aba")
        node2 = TextNode("This is a text node", TextType.BOLD, "aba")
        node3 = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        node4 = TextNode("This is a text node", TextType.LINK, "https://boot.dev")

        self.assertEqual(node, node2)
        self.assertNotEqual(node2, node3)
        self.assertEqual(node3, node4)


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        with self.assertRaises(ValueError):
            node = LeafNode("NO VALUE", "")
            node.to_html()

        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("p", "This is a paragraph of text.")
        node3 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        # node4 = LeafNode(None, "NO TAG!!")
        # node5 = LeafNode("NO VALUE!!", None)

        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(
            node3.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

    def test_italic(self):
        node = TextNode("This is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic")

    def test_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_bold(self):
        node = TextNode(
            "This is text with a **bolded phrase** in the middle", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_italic(self):
        node = TextNode("This is text with an _italic word_ in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic word", TextType.ITALIC),
                TextNode(" in it", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_delimiters(self):
        node = TextNode("`code1` and `code2`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            [
                TextNode("code1", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("code2", TextType.CODE),
            ],
            new_nodes,
        )

    def test_delimiter_at_start(self):
        node = TextNode("`code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            [
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delimiter_at_end(self):
        node = TextNode("word `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            [
                TextNode("word ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
            ],
            new_nodes,
        )

    def test_non_text_node_untouched(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            [
                TextNode("already bold", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_multiple_old_nodes(self):
        node1 = TextNode("This has `code` in it", TextType.TEXT)
        node2 = TextNode("This is bold already", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)

        self.assertEqual(
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" in it", TextType.TEXT),
                TextNode("This is bold already", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_no_delimiter_in_text(self):
        node = TextNode("Plain text with no special syntax", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            [
                TextNode("Plain text with no special syntax", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This has an unclosed `code block", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "Text with ![first](https://i.imgur.com/1.png) and ![second](https://i.imgur.com/2.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("first", "https://i.imgur.com/1.png"),
                ("second", "https://i.imgur.com/2.png"),
            ],
            matches,
        )

    def test_extract_markdown_images_none(self):
        text = "This is text with no images [link](https://boot.dev)"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_single(self):
        text = "This is text with a [link](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multiple(self):
        text = "Links to [boot dev](https://www.boot.dev) and [youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("boot dev", "https://www.boot.dev"),
                ("youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_links_does_not_extract_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://boot.dev")], matches)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_image_single(self):
        node = TextNode(
            "Here is an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Here is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) is at the start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is at the start", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode(
            "This is just plain text without any images.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is just plain text without any images.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_consecutive(self):
        node = TextNode(
            "![first](https://i.imgur.com/first.png)![second](https://i.imgur.com/second.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "https://i.imgur.com/first.png"),
                TextNode("second", TextType.IMAGE, "https://i.imgur.com/second.png"),
            ],
            new_nodes,
        )


class TestTextToTextnodes(unittest.TestCase):
    def test_all_at_once(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
