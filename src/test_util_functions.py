import unittest
from leafnode import LeafNode

from textnode import TextNode
from util_functions import (
    extract_markdown_images,
    split_nodes_delimiter,
    extract_markdown_links,
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


if __name__ == "__main__":
    unittest.main()
