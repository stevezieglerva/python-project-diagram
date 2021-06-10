import re
import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from anytree import ChildResolverError, Node, RenderTree, Resolver, search
from main import *


# class UnitTests(unittest.TestCase):
#     def test_get_python_files__given_valid_starting_dir__then_files_returned(self):
#         # Arrange
#         exclude_pattern = "venv|test|__init__"

#         # Act
#         results = get_python_files(".", exclude_pattern)
#         print(results)

#         # Assert
#         self.assertNotEqual(results, [])
#         excluded_files = [f for f in results if re.findall(exclude_pattern, f)]
#         self.assertEqual(len(excluded_files), 0)

#     def test_create_tree__given__list_of_list__then_dict_correct(self):
#         # Arrange
#         input = ["a/b.py", "a/c.py", "d/e.py"]

#         # Act
#         results = create_tree(input)
#         tree_text = get_ascii_tree(results)
#         print("tree:" + tree_text)

#         # Assert
#         expected = """root
# ├── a
# │   ├── b.py
# │   └── c.py
# └── d
#     └── e.py
# """
#         self.assertEqual(tree_text, expected)

#     def test_get_classes_from_file__given_file_with_two_classes__then_two_classes_returned(
#         self,
#     ):
#         # Arrange
#         file_text = """class class_a():
#     pass

# class class_b():
#     pass
# """

#         # Act
#         results = get_classes_from_file(file_text)

#         # Assert
#         self.assertEqual(results, ["class_a", "class_b"])

#     def test_get_classes_from_file__given_file_with_two_inherited_classes__then_two_classes_returned(
#         self,
#     ):
#         # Arrange
#         file_text = """class class_a(BaseA):
#     pass

# class class_b(BaseB):
#     pass
# """

#         # Act
#         results = get_classes_from_file(file_text)

#         # Assert
#         self.assertEqual(results, ["class_a(BaseA)", "class_b(BaseB)"])


class IntegrationTests(unittest.TestCase):
    #     def test_create_tree_from_real_files__given_project_dir__then_tree_correct(self):
    #         # Arrange

    #         # Act
    #         tree = get_tree_from_files("tests/data/project")
    #         tree_text = get_ascii_tree(tree)
    #         print(get_ascii_tree(tree, True))

    #         # Assert
    #         expected = """root (root)
    # └── tests (dir)
    #     └── data (dir)
    #         └── project (dir)
    #             ├── file1.py (file)
    #             │   ├── class_a(BaseA) (Class)
    #             │   └── class_a2(BaseA) (Class)
    #             └── dir1 (dir)
    #                 └── file_2.py (file)
    #                     └── class_b (Class)
    # """
    #         self.assertEqual(tree_text, expected)

    #         python_files = search.findall(tree, filter_=lambda node: ".py" in node.name)
    #         print(python_files)

    def test_create_html_from_tree__given_project_dir__then_diagram_correct(self):
        # Arrange
        tree = get_tree_from_files("tests/data/project")
        tree_text = get_ascii_tree(tree)
        print(get_ascii_tree(tree, True))

        # Act
        results = create_html_from_tree(tree)
        print(f"\n\n------\n{results}\n\n")
        with open("temp_project.html", "w") as file:
            file.write(results)

        # Assert
        self.assertTrue("<html>" in results)
        self.assertEqual(results.count("project"), 1)
        self.assertEqual(results.count("dir1"), 1)
        self.assertEqual(results.count("file_1"), 1)
        self.assertEqual(results.count("file_2"), 1)
        self.assertEqual(results.count("class_a(BaseA)"), 1)
        self.assertEqual(results.count("class_a2(BaseA)"), 1)
        self.assertEqual(results.count("class_b"), 1)

    def test_create_html_from_tree__given_lutils__then_diagram_correct(self):
        # Arrange
        tree = get_tree_from_files(
            "/Users/sziegler/Documents/Github/lutils/sam-app/common_layer_hex"
        )
        tree_text = get_ascii_tree(tree)
        print(get_ascii_tree(tree, True))

        # Act
        results = create_html_from_tree(tree)
        with open("temp_lutils.html", "w") as file:
            file.write(results)

        # Assert
        self.assertTrue("<html>" in results)

    def test_create_html_from_tree__given_project_small_1_dir__then_diagram_correct(
        self,
    ):
        # Arrange
        tree = get_tree_from_files("tests/data/small_1")
        tree_text = get_ascii_tree(tree)
        print(get_ascii_tree(tree, True))

        # Act
        results = create_html_from_tree(tree)
        print(f"\n\n------\n{results}\n\n")
        with open("temp_small_1.html", "w") as file:
            file.write(results)

        # Assert
        self.assertEqual(results.count("small_1"), 1)
        self.assertEqual(results.count("file3.py"), 1)
        self.assertEqual(results.count("class_c"), 1)

    def test_create_html_from_tree__given_project_small_2_dir__then_diagram_correct(
        self,
    ):
        # Arrange
        tree = get_tree_from_files("tests/data/small_2")
        tree_text = get_ascii_tree(tree)
        print(get_ascii_tree(tree, True))

        # Act
        results = create_html_from_tree(tree)
        print(f"\n\n------\n{results}\n\n")
        with open("temp_small_2.html", "w") as file:
            file.write(results)

        # Assert
        self.assertEqual(results.count("small_2"), 1)
        self.assertEqual(results.count("file3.py"), 1)
        self.assertEqual(results.count("class_c"), 1)


if __name__ == "__main__":
    unittest.main()
