class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None,
       children: HTMLNode | None = None, props: dict[str, str] | None = None
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
