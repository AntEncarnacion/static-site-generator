from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None or self.tag == "":
            raise ValueError("ParentNode must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have at least one child")

        inner_html = ""
        for child in self.children:
            inner_html += child.to_html()

        if self.props is None:
            return f"<{self.tag}>{inner_html}</{self.tag}>"
        return f"<{self.tag} {self.props}>{inner_html}</{self.tag}>"
