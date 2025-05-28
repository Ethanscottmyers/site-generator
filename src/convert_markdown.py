from htmlnode import HTMLNode, LeafNode, ParentNode
from blocktype import BlockType, block_to_block_type
from textnode import TextType, TextNode
from convert import text_node_to_html_node, text_to_textnodes

def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        block = block.strip()
        if block == "" or block.isspace():
            pass
        else:
            blocks.append(block)
    return blocks


def text_to_children(text):
    children = []
    for text_node in text_to_textnodes(text):
        children.append(text_node_to_html_node(text_node))
    return children

#returns number of #'s at the start of a markdown string. 
def heading_number(text):
    num = 0
    while(num < len(text) and text[num] == "#"):
        num += 1
    return num

#returns children lines in HTMLNodes for ordered or unordered lists and removes markdown
def children_lines(block, block_type):
    children = []
    lines = block.split("\n")
    i = 0
    for i in range(len(lines)):
        if block_type == BlockType.UNORDERED_LIST:
            line = lines[i][2:] #remove '- '
        else: #blocktype should be ORDERED_LIST
            line = lines[i][len(str(i))+2:] #remove 'i. ' for however many digits i is
        children.append(ParentNode("li", text_to_children(line)))
    return children

def markdown_to_html_node(markdown):
    children = []
    for block in markdown_to_blocks(markdown):
        type = block_to_block_type(block)
        match type:
            case BlockType.PARAGRAPH:
                children.append(ParentNode("p", text_to_children(block.replace("\n", " "))))
            case BlockType.HEADING:
                h_num = heading_number(block)
                block = block[h_num+1:]
                children.append(ParentNode(f"H{h_num}", text_to_children(block.replace("\n", " "))))
            case BlockType.CODE:
                block = block.strip("`").strip("\n")
                children.append(ParentNode("pre", [LeafNode("code", block)]))
            case BlockType.QUOTE:
                block = block.replace(">", "")
                children.append(ParentNode("blockquote", text_to_children(block)))
            case BlockType.UNORDERED_LIST:
                children.append(ParentNode("ul", children_lines(block, BlockType.UNORDERED_LIST)))
            case BlockType.ORDERED_LIST:
                children.append(ParentNode("ol", children_lines(block, BlockType.ORDERED_LIST)))
    return ParentNode("div", children)