import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


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
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("p", "This is a paragraph of text.")
        node3 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node4 = LeafNode(None, "No TAG!!")

        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(node3.to_html(), '<a href="https://www.google.com">Click me!</a>')
        self.assertEqual(node4.to_html(), "No TAG!!")


if __name__ == "__main__":
    unittest.main()
