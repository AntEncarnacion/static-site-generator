from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        value,
        tag=None,
        props=None,
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None or self.value == "":
            raise ValueError
        if self.tag == "" or self.tag == None:
            return self.value
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"

        return f"<{self.tag} {super().props_to_html()}>{self.value}</{self.tag}>"
