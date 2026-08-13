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

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        original_text = node.text
        matches = extract_markdown_images(node.text)
        nodes = []

        for match in matches:

            image_alt, image_url = match
            sections = original_text.split(f"![{image_alt}]({image_url})", 1)

            for i, section in enumerate(sections):
                if section != "" and i % 2 == 0:
                    new_node = TextNode(section, TextType.PLAIN)
                    nodes.append(new_node)
                else:
                    new_node = TextNode(image_alt, TextType.IMAGE, image_url)
                    nodes.append(new_node)
                    original_text = section

        if original_text != "":
            new_node = TextNode(original_text, TextType.PLAIN)
            nodes.append(new_node)

        new_nodes.extend(nodes)

    return new_nodes




def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        original_text = node.text
        matches = extract_markdown_links(node.text)
        nodes = []

        for match in matches:
            link_alt, link_url = match
            sections = original_text.split(f"[{link_alt}]({link_url})", 1)

            for i, section in enumerate(sections):
                if section != "" and i % 2 == 0:
                    new_node = TextNode(section, TextType.PLAIN)
                    nodes.append(new_node)
                else:
                    new_node = TextNode(link_alt, TextType.LINK, link_url)
                    nodes.append(new_node)
                    original_text = section

        if original_text != "":
            new_node = TextNode(original_text, TextType.PLAIN)
            nodes.append(new_node)

        new_nodes.extend(nodes)

    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.PLAIN)

    new_nodes = split_nodes_image(split_nodes_link([node]))

    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)

    #for new_node in new_nodes:
        #print(new_node)

    return new_nodes