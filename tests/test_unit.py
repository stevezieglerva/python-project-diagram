import re
import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from anytree import ChildResolverError, Node, RenderTree, Resolver, search
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
        expected = """root
├── a
│   ├── b.py
│   └── c.py
└── d
    └── e.py
"""
        self.assertEqual(tree_text, expected)

    def test_get_classes_from_file__given_file_with_two_classes__then_two_classes_returned(
        self,
    ):
        # Arrange
        file_text = """class class_a():
    pass

class class_b():
    pass
"""

        # Act
        results = get_classes_from_file(file_text)

        # Assert
        self.assertEqual(results, ["class_a", "class_b"])

    def test_get_classes_from_file__given_file_with_two_inherited_classes__then_two_classes_returned(
        self,
    ):
        # Arrange
        file_text = """class class_a(BaseA):
    pass

class class_b(BaseB):
    pass
"""

        # Act
        results = get_classes_from_file(file_text)

        # Assert
        self.assertEqual(results, ["class_a(BaseA)", "class_b(BaseB)"])


class IntegrationTests(unittest.TestCase):
    def test_create_tree_from_real_files__given_project_dir__then_tree_correct(self):
        # Arrange

        # Act
        tree = get_tree_from_files("tests/data/project")
        tree_text = get_ascii_tree(tree)
        print(tree_text)

        # Assert
        expected = """root
└── tests
    └── data
        └── project
            ├── file1.py
            │   └── class_a(BaseA)
            └── dir1
                └── file2.py
                    └── class_b
"""
        self.assertEqual(tree_text, expected)

        python_files = search.findall(tree, filter_=lambda node: ".py" in node.name)
        print(python_files)


if __name__ == "__main__":
    unittest.main()
