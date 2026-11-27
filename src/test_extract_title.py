import unittest

from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = extract_title("""
# This is a heading

This is a paragraph of text
"""
)
        self.assertEqual(md, "This is a heading")

    def test_no_title(self):

        with self.assertRaises(ValueError):
            extract_title("""
This is a paragraph of text
"""
)


if __name__ == "__main__":
    unittest.main()
