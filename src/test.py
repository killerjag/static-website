from textnode import TextNode, TextType
from split_nodes import split_nodes_image, split_nodes_link, text_to_textnodes
from blocks import markdown_to_blocks

def main():
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png). And there won't be a 3rd one.",
        TextType.PLAIN,
    )

    node2 = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.PLAIN,
    )

    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

    markdown = ""

    split_nodes_image([node])
    split_nodes_link([node2])
    text_to_textnodes(text)

    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

    markdown_to_blocks(md)

main()