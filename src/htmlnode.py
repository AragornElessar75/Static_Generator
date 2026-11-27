class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None,
       children: list["HTMLNode"] | None = None, props: dict[str, str] | None = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
       raise NotImplementedError

    def props_to_html(self):
        if self.props:
            prop = ""
            for key in self.props:
                prop += f' {key}="{self.props[key]}"'
            return prop
        return ""

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return f"{self.value}"
        if not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list["HTMLNode"],
        props: dict[str, str] | None = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")
        if not self.children:
            raise ValueError("All parent nodes must have children")
        result = ""
        for child in self.children:
            result += f"{child.to_html()}"
        return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"
