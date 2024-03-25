from leafnode import LeafNode
from textnode import TextNode
import re


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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            new_nodes.append(old_node)
            continue
        split_text = old_node.text.split(delimiter)
        if len(split_text) == 1 or len(split_text) == 0:
            new_nodes.append(old_node)
            continue
        elif len(split_text) % 2 == 0:
            raise Exception(f"Invalid markdown detected in text: '{old_node.text}'")
        else:
            split_nodes = []
            for text_index, text in enumerate(split_text):
                if text_index % 2 == 0 and text != "":
                    split_nodes.append(TextNode(text, "text"))
                elif text != "":
                    split_nodes.append(TextNode(text, text_type))
            new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    regex = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text, re.MULTILINE)
    return matches


def extract_markdown_links(text):
    regex = r"(?<=[^\!])\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text, re.MULTILINE)
    return matches
