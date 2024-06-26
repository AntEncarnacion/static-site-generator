from leafnode import LeafNode
from textnode import TextNode
import re
import text_types as tt
import block_types as bt


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
                    split_nodes.append(TextNode(text, tt.text_type_text))
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


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            new_nodes.append(old_node)
            continue
        elif old_node.text == "":
            continue
        matches = extract_markdown_images(old_node.text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
        elif len(matches) > 0:
            split_nodes = []
            for match_index, match in enumerate(matches):
                if match_index == 0:
                    split_text = old_node.text.split(f"![{match[0]}]({match[1]})", 1)
                else:
                    split_text = split_nodes.pop().text.split(
                        f"![{match[0]}]({match[1]})", 1
                    )

                for text_index, text in enumerate(split_text):
                    if text_index == 0 and text != "":
                        split_nodes.append(TextNode(text, tt.text_type_text))
                    elif text_index == 1:
                        split_nodes.append(
                            TextNode(match[0], tt.text_type_image, url=match[1])
                        )
                    if text_index == 1 and text != "":
                        split_nodes.append(TextNode(text, tt.text_type_text))
            new_nodes.extend(split_nodes)
        else:
            raise Exception(f"Invalid markdown detected in text: '{old_node.text}'")
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            new_nodes.append(old_node)
            continue
        elif old_node.text == "":
            continue
        matches = extract_markdown_links(old_node.text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
        elif len(matches) > 0:
            split_nodes = []
            for match_index, match in enumerate(matches):
                if match_index == 0:
                    split_text = old_node.text.split(f"[{match[0]}]({match[1]})", 1)
                else:
                    split_text = split_nodes.pop().text.split(
                        f"[{match[0]}]({match[1]})", 1
                    )

                for text_index, text in enumerate(split_text):
                    if text_index == 0 and text != "":
                        split_nodes.append(TextNode(text, tt.text_type_text))
                    elif text_index == 1:
                        split_nodes.append(
                            TextNode(match[0], tt.text_type_link, url=match[1])
                        )
                    if text_index == 1 and text != "":
                        split_nodes.append(TextNode(text, tt.text_type_text))
            new_nodes.extend(split_nodes)
        else:
            raise Exception(f"Invalid markdown detected in text: '{old_node.text}'")
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, "text")]
    nodes = split_nodes_delimiter(nodes, "**", tt.text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", tt.text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", tt.text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    if markdown == "":
        return []
    results = markdown.split("\n\n")
    buffer = []
    for result in results:
        stripped_result = result.strip("\n\t ")
        if stripped_result == "":
            continue
        buffer.append(stripped_result)

    return buffer


def block_to_block_type(markdown_text):
    split_markdown_text = markdown_text.split("\n")

    heading_regex = r"^#{1,6}\ .*$"
    if re.match(heading_regex, markdown_text):
        return bt.block_type_heading

    code_regex = r"^```[\S\s]*```$"
    if re.match(code_regex, markdown_text):
        return bt.block_type_code

    quote_regex = r"^>[\S\s]*$"
    quote_validation = None
    for index, markdown_text_line in enumerate(split_markdown_text):
        if index == 0:
            quote_validation = re.search(quote_regex, markdown_text_line) != None
        else:
            quote_validation = (
                quote_validation
                and re.search(quote_regex, markdown_text_line.lstrip()) != None
            )
    if quote_validation:
        return bt.block_type_quote

    unordered_list_regex = r"^[\-\*]\ [\S\s]*$"
    unordered_list_validation = None
    for index, markdown_text_line in enumerate(split_markdown_text):
        if index == 0:
            unordered_list_validation = (
                re.match(unordered_list_regex, markdown_text_line) != None
            )
        else:
            unordered_list_validation = (
                unordered_list_validation
                and re.search(unordered_list_regex, markdown_text_line.lstrip()) != None
            )
    if unordered_list_validation:
        return bt.block_type_unordered_list

    ordered_list_validation = None
    for index, markdown_text_line in enumerate(split_markdown_text):
        ordered_list_regex = rf"^{index+1}\.\ [\S\s]*$"
        if index == 0:
            ordered_list_validation = (
                re.search(ordered_list_regex, markdown_text_line) != None
            )
        else:
            ordered_list_validation = (
                ordered_list_validation
                and re.search(ordered_list_regex, markdown_text_line.lstrip()) != None
            )
    if ordered_list_validation:
        return bt.block_type_ordered_list

    return bt.block_type_paragraph
