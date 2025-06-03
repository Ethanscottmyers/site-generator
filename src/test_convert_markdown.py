import unittest
from convert_markdown import markdown_to_blocks, markdown_to_html_node, extract_title

class TestConvertMarkdown(unittest.TestCase):
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


    def test_markdown_to_html_node(self):
        print("Testing markdown_to_html_node")
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

        md = """
- this is an
- unordered
- list

and a paragraph with **bold** text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, 
            "<div><ul><li>this is an</li><li>unordered</li><li>list</li></ul><p>and a paragraph with <b>bold</b> text</p></div>")
        
        md = """
1. this is an
2. ordered
3. list

and a paragraph with **bold** text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, 
            "<div><ol><li>this is an</li><li>ordered</li><li>list</li></ol><p>and a paragraph with <b>bold</b> text</p></div>")
        print("Passed!")


    def test_extract_title(self):
        print("Testing extract_title...")
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")
        md = """
This is a test

# Heading 1

-of markdown
-heading extractor
"""
        self.assertEqual(extract_title(md), "Heading 1")
        try:
            md = """
This is a test

## of markdown

with no h1"""
            heading = extract_title(md)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(True)
        print("Passed!")