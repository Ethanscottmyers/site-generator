import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        print("Testing HTMLNode props_to_html...")
        node = HTMLNode("div", props={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')
        node = HTMLNode(tag="span", props={"style": "color: red;"})
        self.assertEqual(node.props_to_html(), ' style="color: red;"')
        node = HTMLNode(tag="p", props={})
        self.assertEqual(node.props_to_html(), "")
        node = HTMLNode(tag="a", props=None)
        self.assertEqual(node.props_to_html(), "")
        print("Passed!")


    def test_leaf_to_html(self):
        print("Testing LeafNode... ")
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node = LeafNode("a", "Test Link", {"href": "google.com", "tag": "test_tag"})
        self.assertEqual(node.to_html(), '<a href="google.com" tag="test_tag">Test Link</a>')
        try:
            node = LeafNode("a", None, props={"href": "google.com"})
            self.assertTrue(False)
        except ValueError as e:
            self.assertTrue(True)
        print("Passed!")

    def test_to_html_with_children(self):
        print("Testing ParentNode with children...")
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        child_node2 = LeafNode("a", "This is a link", {"href": "google.com", "test_prop": "test"})
        parent_node = ParentNode("div", [child_node, child_node2], {"test_parent_prop": "test"})
        self.assertEqual(parent_node.to_html(), '<div test_parent_prop="test"><span>child</span><a href="google.com" test_prop="test">This is a link</a></div>')
        print("Passed!")

    def test_to_html_with_grandchildren(self):
        print("Testing ParentNode with grandchildren...")
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        print("Passed!")