import unittest
from textnode import TextType, TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        print("Testing TextNode equals")
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)
        node1 = TextNode("This is another text node", TextType.NORMAL, "index.html")
        node2 = TextNode("This is another text node", TextType.NORMAL, "index.html")
        self.assertEqual(node1, node2)
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different node", TextType.BOLD)
        self.assertNotEqual(node1, node2)
        node1 = TextNode("This is a text node", TextType.NORMAL, "hi.com")
        node2 = TextNode("This is a text node", TextType.CODE, "hi.com")
        self.assertNotEqual(node1, node2)
        node1 = TextNode("This is a text node", TextType.NORMAL, "hello.com")
        node2 = TextNode("This is a text node", TextType.NORMAL, "hi.com")
        self.assertNotEqual(node1, node2)
        node1.url = "hi.com"
        self.assertEqual(node1, node2)
        print("Passed!")

if __name__ == "__main__":
    unittest.main()