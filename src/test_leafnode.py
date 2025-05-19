import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        print("Testing LeafNode... ")
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node = LeafNode("a", "Test Link", {"href": "google.com", "tag": "test_tag"})
        self.assertEqual(node.to_html(), '<a href="google.com" tag="test_tag">Test Link</a>')
        try:
            node = LeafNode("a", props={"href": "google.com"})
            self.assertTrue(False)
        except ValueError as e:
            self.assertTrue(True)
        print("Passed!")
    
if __name__ == "__main__":
    unittest.main()