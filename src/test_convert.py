import unittest
from htmlnode import LeafNode
from textnode import TextNode, TextType
from convert import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from convert import split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks

class TestConvert(unittest.TestCase):
    def test_text_node_to_html_node(self):
        print("Testing text_node_to_html_node...")
        text_node = TextNode("Testing1", TextType.TEXT)
        leaf_node = LeafNode(None, "Testing1")
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)
        text_node = TextNode("Testing2", TextType.BOLD)
        leaf_node = LeafNode("b", "Testing2")
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)
        text_node = TextNode("Testing3", TextType.ITALIC)
        leaf_node = LeafNode("i", "Testing3")
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)
        text_node = TextNode("Testing4", TextType.CODE)
        leaf_node = LeafNode("code", "Testing4")
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)
        text_node = TextNode("Testing5", TextType.LINK, "google.com")
        leaf_node = LeafNode("a", "Testing5", {"href": "google.com"})
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)
        text_node = TextNode("Testing6", TextType.IMAGE, "image.png")
        leaf_node = LeafNode("img", "", {"src": "image.png", "alt": "Testing6"})
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)
        try:
            text_node = TextNode("Should fail", None)
            text_node_to_html_node(text_node)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(True)
        print("Passed!")

    def test_split_nodes_delimiter(self):
        print("Testing split_nodes_delimiter...")
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])
        node = TextNode("This is `text` with two `code block` words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.CODE),
            TextNode(" with two ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" words", TextType.TEXT)
        ])
        node = TextNode("This is **text** with different _styles_ in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is **text** with different ", TextType.TEXT), 
            TextNode("styles", TextType.ITALIC), 
            TextNode(" in it", TextType.TEXT)
        ])
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT), 
            TextNode("text", TextType.BOLD), 
            TextNode(" with different ", TextType.TEXT),
            TextNode("styles", TextType.ITALIC), 
            TextNode(" in it", TextType.TEXT)
        ])
        print("Passed!")

    def test_extract_markdown_images(self):
        print("Testing extract_markdown_images...")
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png")])
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual(matches, 
                             [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
        print("Passed!")

    def test_extract_markdown_links(self):
        print("Testing extract_markdown_links...")
        matches = extract_markdown_links("This is text with a [linked site](www.google.com)")
        self.assertListEqual(matches, 
                             [("linked site", "www.google.com")])
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual(matches, 
                             [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
        print("Passed!")

    def test_split_nodes_image(self):
        print("Testing split_nodes_image...")
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, 
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ]
        )
        print("Passed!")

    def test_split_nodes_link(self):
        print("Testing split_nodes_link...")
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, 
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ]
        )
        print("Passed!")

    def test_text_to_textnodes(self):
        print("Testing text_to_textnodes...")
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes, 
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ])
        print("Passed!")

    def test_markdown_to_blocks(self):
        print("Testing markdown_to_blocks...")
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, 
                         [
                             "This is **bolded** paragraph",
                             "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                             "- This is a list\n- with items"
                         ])
        md = """
This is a test of multiple blank lines




Second paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "This is a test of multiple blank lines",
            "Second paragraph"
        ])
        print("Passed!")
