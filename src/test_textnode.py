import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node, split_nodes_delimiter


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
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
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

if __name__ == "__main__":
    unittest.main()
