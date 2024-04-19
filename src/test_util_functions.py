import unittest
from leafnode import LeafNode

import block_types as bt
from textnode import TextNode
from util_functions import (
    block_to_block_type,
    extract_markdown_images,
    markdown_to_blocks,
    split_nodes_delimiter,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestUtil(unittest.TestCase):
    def test_split_nodes_delimiter_1(self):
        node = TextNode("This is a text *node*", "text")
        expected_result = [
            TextNode("This is a text ", "text"),
            TextNode("node", "bold"),
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", "bold"), expected_result)

    def test_split_nodes_delimiter_2(self):
        node = TextNode("This is a text `node`", "text")
        expected_result = [
            TextNode("This is a text ", "text"),
            TextNode("node", "code"),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", "code"), expected_result)

    def test_split_nodes_delimiter_3(self):
        node = TextNode("This is **a** *text* `node`", "text")
        expected_result = [
            TextNode("This is ", "text"),
            TextNode("a", "italic"),
            TextNode(" ", "text"),
            TextNode("text", "bold"),
            TextNode(" ", "text"),
            TextNode("node", "code"),
        ]
        result = split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_delimiter([node], "`", "code"), "**", "italic"
            ),
            "*",
            "bold",
        )
        self.assertEqual(result, expected_result)

    def test_split_nodes_delimiter_4(self):
        node = TextNode("This is a text node", "text")
        expected_result = [
            TextNode("This is a text node", "text"),
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", "bold"), expected_result)

    def test_split_nodes_delimiter_5(self):
        node = TextNode("", "text")
        expected_result = [
            TextNode("", "text"),
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", "bold"), expected_result)

    def test_split_nodes_delimiter_6(self):
        node = LeafNode("Test", "p")
        expected_result = [LeafNode("Test", "p")]
        self.assertEqual(
            split_nodes_delimiter([node], "*", "bold")[0].to_html(),
            expected_result[0].to_html(),
        )

    def test_extract_markdown_images_1(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        expected_result = [
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("another", "https://i.imgur.com/dfsdkjfd.png"),
        ]
        self.assertEqual(extract_markdown_images(text), expected_result)

    def test_extract_markdown_images_2(self):
        text = "This is text with nothing"
        expected_result = []
        self.assertEqual(extract_markdown_images(text), expected_result)

    def test_extract_markdown_links_1(self):
        text = "This is text with an [url](https://i.imgur.com/zjjcJKZ.png) and [another](https://i.imgur.com/dfsdkjfd.png)"
        expected_result = [
            ("url", "https://i.imgur.com/zjjcJKZ.png"),
            ("another", "https://i.imgur.com/dfsdkjfd.png"),
        ]
        self.assertEqual(extract_markdown_links(text), expected_result)

    def test_extract_markdown_links_2(self):
        text = "This is text with nothing"
        expected_result = []
        self.assertEqual(extract_markdown_images(text), expected_result)

    def test_split_nodes_image_1(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text",
        )
        new_nodes = split_nodes_image([node])
        expected_result = [
            TextNode("This is text with an ", "text"),
            TextNode(
                "image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", "text"),
            TextNode(
                "second image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]

        self.assertEqual(new_nodes, expected_result)

    def test_split_nodes_image_2(self):
        node = TextNode(
            "This is text with a no images.",
            "text",
        )
        new_nodes = split_nodes_image([node])
        expected_result = [
            TextNode("This is text with a no images.", "text"),
        ]

        self.assertEqual(new_nodes, expected_result)

    def test_split_nodes_image_3(self):
        node = TextNode(
            "This is text with a broken ![broken image](",
            "text",
        )
        new_nodes = split_nodes_image([node])
        expected_result = [
            TextNode("This is text with a broken ![broken image](", "text"),
        ]

        self.assertEqual(new_nodes, expected_result)

    def test_split_nodes_image_4(self):
        node = TextNode(
            "This is text with a [link]()",
            "text",
        )
        new_nodes = split_nodes_image([node])
        expected_result = [
            TextNode("This is text with a [link]()", "text"),
        ]

        self.assertEqual(new_nodes, expected_result)

    def test_split_nodes_image_5(self):
        new_nodes = split_nodes_image([])
        expected_result = []

        self.assertEqual(new_nodes, expected_result)

    def test_split_nodes_link_1(self):
        node = TextNode(
            "This is text with a [link](https://storage.googleapis.com/) and another [second link](https://storage.googleapis.com/)",
            "text",
        )
        new_nodes = split_nodes_link([node])
        expected_result = [
            TextNode("This is text with a ", "text"),
            TextNode(
                "link",
                "link",
                "https://storage.googleapis.com/",
            ),
            TextNode(" and another ", "text"),
            TextNode(
                "second link",
                "link",
                "https://storage.googleapis.com/",
            ),
        ]

        self.assertEqual(new_nodes, expected_result)

    def test_split_nodes_link_2(self):
        node = TextNode(
            "This is text with no links.",
            "text",
        )
        new_nodes = split_nodes_link([node])
        expected_result = [
            TextNode("This is text with no links.", "text"),
        ]

        self.assertEqual(new_nodes, expected_result)

    def test_split_nodes_link_3(self):
        node = TextNode(
            "This is text with a broken link [broken link](",
            "text",
        )
        new_nodes = split_nodes_link([node])
        expected_result = [
            TextNode("This is text with a broken link [broken link](", "text"),
        ]

        self.assertEqual(new_nodes, expected_result)

    def test_split_nodes_link_4(self):
        node = TextNode(
            "This is text with an ![image]()",
            "text",
        )
        new_nodes = split_nodes_link([node])
        expected_result = [
            TextNode("This is text with an ![image]()", "text"),
        ]

        self.assertEqual(new_nodes, expected_result)

    def test_split_nodes_link_5(self):
        new_nodes = split_nodes_link([])
        expected_result = []

        self.assertEqual(new_nodes, expected_result)

    def test_text_to_textnodes_1(self):
        result = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        expected_result = [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode(
                "image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ]

        self.assertEqual(result, expected_result)

    def test_text_to_textnodes_2(self):
        result = text_to_textnodes("This is a simple text")
        expected_result = [
            TextNode("This is a simple text", "text"),
        ]

        self.assertEqual(result, expected_result)

    def test_text_to_textnodes_3(self):
        result = text_to_textnodes("")
        expected_result = []

        self.assertEqual(result, expected_result)

    def test_text_to_textnodes_4(self):
        result = text_to_textnodes(
            "This is a simple text with **bold** **bold** ![image](linkhere)"
        )
        expected_result = [
            TextNode("This is a simple text with ", "text"),
            TextNode("bold", "bold"),
            TextNode(" ", "text"),
            TextNode("bold", "bold"),
            TextNode(" ", "text"),
            TextNode("image", "image", "linkhere"),
        ]

        self.assertEqual(result, expected_result)

    def test_markdown_to_blocks_1(self):
        result = markdown_to_blocks(
            """This is **bolded** paragraph

            This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line

            * This is a list
            * with items"""
        )
        expected_result = [
            "This is **bolded** paragraph",
            """This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line""",
            """* This is a list
            * with items""",
        ]

        self.assertEqual(result, expected_result)

    def test_markdown_to_blocks_2(self):
        result = markdown_to_blocks(
            """This is **bolded** paragraph
            This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line

            * This is a list
            * with items"""
        )
        expected_result = [
            """This is **bolded** paragraph
            This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line""",
            """* This is a list
            * with items""",
        ]

        self.assertEqual(result, expected_result)

    def test_markdown_to_blocks_3(self):
        result = markdown_to_blocks(
            """This is **bolded** paragraph
            This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line
            * This is a list
            * with items"""
        )
        expected_result = [
            """This is **bolded** paragraph
            This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line
            * This is a list
            * with items""",
        ]

        self.assertEqual(result, expected_result)

    def test_markdown_to_blocks_4(self):
        result = markdown_to_blocks("")
        expected_result = []

        self.assertEqual(result, expected_result)

    def test_markdown_to_blocks_5(self):
        result = markdown_to_blocks("One liner")
        expected_result = ["One liner"]

        self.assertEqual(result, expected_result)

    def test_markdown_to_blocks_6(self):
        result = markdown_to_blocks(
            """This is **bolded** paragraph

            This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line

            * This is a list
            * with items



            """
        )
        expected_result = [
            "This is **bolded** paragraph",
            """This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line""",
            """* This is a list
            * with items""",
        ]

        self.assertEqual(result, expected_result)

    def test_markdown_to_blocks_7(self):
        result = markdown_to_blocks(
            """This is **bolded** paragraph

            This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line




            * This is a list
            * with items
            """
        )
        expected_result = [
            "This is **bolded** paragraph",
            """This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line""",
            """* This is a list
            * with items""",
        ]

        self.assertEqual(result, expected_result)

    def test_markdown_to_blocks_8(self):
        result = markdown_to_blocks("")
        expected_result = []

        self.assertEqual(result, expected_result)

    def test_block_to_block_type_1(self):
        result = block_to_block_type("""### This is a heading test""")
        expected_result = bt.block_type_heading

        self.assertEqual(result, expected_result)

    def test_block_to_block_type_2(self):
        result = block_to_block_type(
            """```
        This is a heading test```"""
        )
        expected_result = bt.block_type_code

        self.assertEqual(result, expected_result)

    def test_block_to_block_type_3(self):
        result = block_to_block_type(
            """>quote
            >test
            >here"""
        )
        expected_result = bt.block_type_quote

        self.assertEqual(result, expected_result)

    def test_block_to_block_type_4(self):
        result = block_to_block_type(
            """- quote
            - test
            * here"""
        )
        expected_result = bt.block_type_unordered_list

        self.assertEqual(result, expected_result)

    def test_block_to_block_type_5(self):
        result = block_to_block_type(
            """1. quote
            2. test
            3. here"""
        )
        expected_result = bt.block_type_ordered_list

        self.assertEqual(result, expected_result)

    def test_block_to_block_type_6(self):
        result = block_to_block_type("""#######This is a heading test""")
        expected_result = bt.block_type_paragraph

        self.assertEqual(result, expected_result)

    def test_block_to_block_type_2(self):
        result = block_to_block_type(
            """``
        This is a heading test```"""
        )
        expected_result = bt.block_type_paragraph

        self.assertEqual(result, expected_result)

    def test_block_to_block_type_3(self):
        result = block_to_block_type(
            """>quote
            test
            >here"""
        )
        expected_result = bt.block_type_paragraph

        self.assertEqual(result, expected_result)

    def test_block_to_block_type_4(self):
        result = block_to_block_type(
            """- quote
            -test
            * here"""
        )
        expected_result = bt.block_type_paragraph

        self.assertEqual(result, expected_result)

    def test_block_to_block_type_5(self):
        result = block_to_block_type(
            """1. quote
            3. test
            3. here"""
        )
        expected_result = bt.block_type_paragraph

        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
