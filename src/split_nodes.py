from extract_markdown import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        #if delimiter not in node.text:
            #raise Exception("delimiter not found")

        strings = node.text.split(delimiter)
        nodes = []

        if len(strings) % 2 == 0:
            raise Exception("Unclosed delimiter")

        for i, string in enumerate(strings):
            if string != "":
                if i % 2 == 0:
                    node = TextNode(string, TextType.PLAIN)
                    nodes.append(node)
                else:
                    node = TextNode(string, text_type)
                    nodes.append(node)

        new_nodes.extend(nodes)

    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN))
    return new_nodes




def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN))
    return new_nodes

def text_to_textnodes(text):
    node = [TextNode(text, TextType.PLAIN)]

    new_nodes = split_nodes_image(node)
    new_nodes = split_nodes_link(new_nodes)

    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)

    #for new_node in new_nodes:
        #print(new_node)

    return new_nodes