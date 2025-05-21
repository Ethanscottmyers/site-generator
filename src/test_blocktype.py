import unittest
from blocktype import BlockType, block_to_block_type

class TestBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        print("Testing block_to_block_type...")
        md = "# This is a valid heading"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.HEADING)
        md = "###### This is another valid heading"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.HEADING)
        md = "#THis is an invalid heading"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.PARAGRAPH)

        md = "```This is a valid \ncode \nblock```"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.CODE)
        md = "``This is not valid code``"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.PARAGRAPH)
        md = "```This is also not valid``"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.PARAGRAPH)

        md = "- This is a valid\n- unordered list\n- here"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.UNORDERED_LIST)
        md = "- this is not \n-valid"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.PARAGRAPH)

        md = "1. This is \n2. a valid\n3. ordered list"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.ORDERED_LIST)
        md = "1. This is \n1. not valid"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.PARAGRAPH)
        md = "1.this is also\n2. not valid"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.PARAGRAPH)
        print("Passed!")
