from leafnode import LeafNode


def text_node_to_html_node(text_node):
    output_node = None
    match text_node.text_type:
        case "text":
            output_node = LeafNode(tag=None, value=text_node.text)
        case "bold":
            output_node = LeafNode(tag="b", value=text_node.text)
        case "italic":
            output_node = LeafNode(tag="i", value=text_node.text)
        case "code":
            output_node = LeafNode(tag="code", value=text_node.text)
        case "link":
            output_node = LeafNode(tag="a", value=text_node.text, props={"href": ""})
        case "image":
            output_node = LeafNode(tag="img", value="", props={"src": "", "alt": ""})
        case _:
            raise Exception("Invalid text type")
    return output_node
