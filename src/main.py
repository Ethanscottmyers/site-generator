from textnode import TextNode, TextType



def main():
    node = TextNode("test text", TextType.NORMAL, "localhost.com")
    print(node)

main()