import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a test",None,{"class": "text container"})
        self.assertEqual(node.props_to_html(), "class=\"text container\"")
        node2 = HTMLNode("p", "This is a test",None,None)
        self.assertEqual(node2.props_to_html(), "")


if __name__ == "__main__":
    unittest.main()

