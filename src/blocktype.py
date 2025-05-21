from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

#Returns true if every line (\n) in "str" starts with "start"
def all_lines_start_with(str, start):
    starts_with = True
    for line in str.splitlines():
        if not line.startswith(start):
            starts_with = False
    return starts_with

def block_to_block_type(markdown):
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    elif all_lines_start_with(markdown, ">"):
        return BlockType.QUOTE
    elif all_lines_start_with(markdown, "- "):
        return BlockType.UNORDERED_LIST
    if markdown.startswith("1. "):
        is_ordered_list = True
        i = 1
        for line in markdown.splitlines():
            if not line.startswith(f"{i}. "):
                is_ordered_list = False
            i += 1
        if is_ordered_list:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
