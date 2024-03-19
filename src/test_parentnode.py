import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_leaf_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_parent_children(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    tag="p",
                    children=[
                        LeafNode(tag="b", value="Bold text"),
                        LeafNode(tag=None, value="Normal text"),
                        LeafNode(tag="i", value="italic text"),
                        LeafNode(tag=None, value="Normal text"),
                    ],
                ),
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_parent_children_3_levels(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    tag="p",
                    children=[
                        ParentNode(
                            tag="p",
                            children=[
                                LeafNode(tag="b", value="Bold text"),
                                LeafNode(tag=None, value="Normal text"),
                                LeafNode(tag="i", value="italic text"),
                                LeafNode(tag=None, value="Normal text"),
                            ],
                        ),
                        LeafNode(tag="b", value="Bold text"),
                        LeafNode(tag=None, value="Normal text"),
                        LeafNode(tag="i", value="italic text"),
                        LeafNode(tag=None, value="Normal text"),
                    ],
                ),
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_no_tag_error(self):
        node = ParentNode(
            None,
            [
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
        )
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children_error(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
        node2 = ParentNode("p", [])
        with self.assertRaises(ValueError):
            node2.to_html()


if __name__ == "__main__":
    unittest.main()
