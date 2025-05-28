import re
from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise ValueError("text_node_to_html_node must be passed a TextNode")
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("TextNode has invalid TextType")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise Exception("Only TextNodes can be passed into split_nodes_delimiter!")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else: 
            new_text_list = node.text.split(delimiter, maxsplit=2)
            if len(new_text_list) == 1:
                new_nodes.append(node)
            elif len(new_text_list) == 3:
                text0 = TextNode(new_text_list[0], TextType.TEXT)
                text1 = TextNode(new_text_list[1], text_type)
                text2 = TextNode(new_text_list[2], TextType.TEXT)
                new_nodes.extend([text0, text1])
                new_nodes.extend(split_nodes_delimiter([text2], delimiter, text_type))
            else:
                raise Exception(f"No matching {delimiter} pair was found in {node.text}")
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise Exception("Only TextNodes can be passed into split_nodes_image!")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else: 
            text = node.text
            for alt, src in extract_markdown_images(text):
                sections = text.split(f"![{alt}]({src})", maxsplit=1)
                new0 = TextNode(sections[0], TextType.TEXT)
                new1 = TextNode(alt, TextType.IMAGE, src)
                new_nodes.extend([new0, new1])
                text = sections[1]
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise Exception("Only TextNodes can be passed into split_nodes_links!")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else: 
            text = node.text
            for link, url in extract_markdown_links(text):
                sections = text.split(f"[{link}]({url})", maxsplit=1)
                new0 = TextNode(sections[0], TextType.TEXT)
                new1 = TextNode(link, TextType.LINK, url)
                new_nodes.extend([new0, new1])
                text = sections[1]
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes