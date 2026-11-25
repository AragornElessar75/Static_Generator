import unittest

from node_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


class Test_inline_markdown(unittest.TestCase):
    def test_delimiter_beginning(self):
        nodes = []
        nodes.append(TextNode("`code block` word is in this text", TextType.TEXT))
        nodes.append(TextNode("This is not a text node", TextType.BOLD))
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("code block", TextType.CODE),
            TextNode(" word is in this text", TextType.TEXT),
            TextNode("This is not a text node", TextType.BOLD)
        ])

    def test_delimiter_middle(self):
        nodes = []
        nodes.append(TextNode("This is text with a `code block` word", TextType.TEXT))
        nodes.append(TextNode("This is not a text node", TextType.BOLD))
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is not a text node", TextType.BOLD)
        ])

    def test_delimiter_end(self):
        nodes = []
        nodes.append(TextNode("This is text that contains a `code block`", TextType.TEXT))
        nodes.append(TextNode("This is not a text node", TextType.BOLD))
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("This is text that contains a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode("This is not a text node", TextType.BOLD)
        ])

    def test_double_delimiter(self):
        nodes = []
        nodes.append(TextNode("There is `code block` word in this text & a `code block` in this text", TextType.TEXT))
        nodes.append(TextNode("This is not a text node", TextType.BOLD))
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("There is ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word in this text & a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" in this text", TextType.TEXT),
            TextNode("This is not a text node", TextType.BOLD)
        ])

    def test_code_bold(self):
        nodes = []
        nodes.append(TextNode("There is `code block` word in this text & a **code block** in this text", TextType.TEXT))
        nodes.append(TextNode("This is not a text node", TextType.BOLD))
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        result2 = split_nodes_delimiter(result, "**", TextType.BOLD)
        self.assertEqual(result2, [
            TextNode("There is ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word in this text & a ", TextType.TEXT),
            TextNode("code block", TextType.BOLD),
            TextNode(" in this text", TextType.TEXT),
            TextNode("This is not a text node", TextType.BOLD)
        ])

    def test_bold_italic(self):
        nodes = []
        nodes.append(TextNode("There is **bold** word in this text & a _italic_ in this text", TextType.TEXT))
        nodes.append(TextNode("This is not a text node", TextType.BOLD))
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        result2 = split_nodes_delimiter(result, "_", TextType.ITALIC)
        self.assertEqual(result2, [
            TextNode("There is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word in this text & a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" in this text", TextType.TEXT),
            TextNode("This is not a text node", TextType.BOLD)
        ])

    def test_unbalanced_delimiter(self):
        nodes = []
        nodes.append(TextNode("This is text with a `code block word", TextType.TEXT))
        nodes.append(TextNode("This is not a text node", TextType.BOLD))
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "`", TextType.CODE)


if __name__ == "__main__":
    unittest.main()
