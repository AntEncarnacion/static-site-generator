class TextNode:
    def __init__(self, text, text_type, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url
        return

    def __eq__(self, other) -> bool:
        text_props_equal = self.text == other.text
        text_type_props_equal = self.text_type == other.text_type
        url_props_equal = self.url == other.url
        return text_props_equal and text_type_props_equal and url_props_equal

    def __repr__(self) -> str:
        return f"TextNode({self.text},{self.text_type},{self.url})"
