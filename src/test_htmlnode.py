import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        print("Testing HTMLNode props_to_html...")
        node = HTMLNode("div", props={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), 'class="container" id="main"')
        node = HTMLNode(tag="span", props={"style": "color: red;"})
        self.assertEqual(node.props_to_html(), 'style="color: red;"')
        node = HTMLNode(tag="p", props={})
        self.assertEqual(node.props_to_html(), "")
        node = HTMLNode(tag="a", props=None)
        self.assertEqual(node.props_to_html(), "")
        print("Passed!")