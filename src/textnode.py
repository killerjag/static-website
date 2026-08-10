from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.PLAIN:
            new_node = LeafNode(None, text_node.text)
            return new_node
        case TextType.BOLD:
            new_node = LeafNode("b", text_node.text)
            return new_node
        case TextType.ITALIC:
            new_node = LeafNode("i", text_node.text)
            return new_node
        case TextType.CODE:
            new_node = LeafNode("code", text_node.text)
            return new_node
        case TextType.LINK:
            if text_node.url is None:
                raise ValueError("Invalid url")
            new_node = LeafNode("a", text_node.text, {"href": text_node.url})
            return new_node
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("Invalid url")
            new_node = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            return new_node
        case _:
            raise Exception("Invalid type")
