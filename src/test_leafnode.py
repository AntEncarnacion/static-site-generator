import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode(
            tag="p", value="This is a test", props={"class": "text container"}
        )
        self.assertEqual(node.to_html(), '<p class="text container">This is a test</p>')
        node2 = LeafNode(tag="p", value="This is a paragraph of text.")
        self.assertEqual(node2.to_html(), "<p>This is a paragraph of text.</p>")
        node3 = LeafNode(
            tag="a", value="Click me!", props={"href": "https://www.google.com"}
        )
        self.assertEqual(
            node3.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )


if __name__ == "__main__":
    unittest.main()
