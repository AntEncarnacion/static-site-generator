class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        output_string = ""
        if type(self.props) is not dict or self.props == None:
            return ""
        for prop_key in self.props:
            if len(output_string) == 0:
                output_string = output_string + f'{prop_key}="{self.props[prop_key]}"'
                continue
            output_string = output_string + f' {prop_key}="{self.props[prop_key]}"'
        return output_string

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"
