from textnode import TextNode, TextType

def main():
    dummy = TextNode("anchor text", TextType.LINK, "https://www.boot.dev")

    print(dummy)

main()