class HTMLNode:
    def __init__(self, tag: str | None, value: str | None, children: list["HTMLNode"] | None, props: dict[str, str]) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props == [] or self.props == None:
            return ""
        result = str()
        for prop in self.props:
            result += f' {prop}="{self.props[prop]}"'

        return result

    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"

#----------------------------------------------------------------------------------------------------------------------------------------------

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("No value")
        if self.tag is None:
            return self.value

        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

#----------------------------------------------------------------------------------------------------------------------------------------------

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("No tag")
        if self.children is None:
            raise ValueError("Missing children")

        result = str()

        for child in self.children:
            result += child.to_html()

        return f'<{self.tag}{self.props_to_html()}>{result}</{self.tag}>'