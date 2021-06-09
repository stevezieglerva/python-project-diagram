import re
import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from main import *


class UnitTests(unittest.TestCase):
    def test_get_python_files__given_valid_starting_dir__then_files_returned(self):
        # Arrange
        exclude_pattern = "venv|test|__init__"

        # Act
        results = get_python_files(".", exclude_pattern)
        print(results)

        # Assert
        self.assertNotEqual(results, [])
        excluded_files = [f for f in results if re.findall(exclude_pattern, f)]
        self.assertEqual(len(excluded_files), 0)

    def test_create_tree__given__list_of_list__then_dict_correct(self):
        # Arrange
        input = ["a/b.py", "a/c.py", "d/e.py"]

        # Act
        results = create_tree(input)
        tree_text = get_ascii_tree(results)
        print("tree:" + tree_text)

        # Assert
        expected = """project
├── a
│   ├── b.py
│   └── c.py
└── d
    └── e.py
"""
        self.assertEqual(tree_text, expected)


class IntegrationTests(unittest.TestCase):
    def test_create_tree_from_real_files__given_project_dir__then_tree_correct(self):
        # Arrange
        files = get_python_files("tests/data/project")
        print(files)

        # Act
        tree = create_tree(files)
        tree_text = get_ascii_tree(tree)
        print(tree_text)

        # Assert
        expected = """project
└── tests
    └── data
        └── project
            ├── file1.py
            └── dir1
                └── file2.py
"""
        self.assertEqual(tree_text, expected)


if __name__ == "__main__":
    unittest.main()
