import functools
import glob
import operator
import re

from anytree import ChildResolverError, Node, RenderTree, Resolver, search


def main():
    pass


def get_tree_from_files(starting_path):
    files = get_python_files(starting_path)
    tree = create_tree(files)
    tree_text = get_ascii_tree(tree)
    python_file_nodes = search.findall(tree, filter_=lambda node: ".py" in node.name)
    python_file_names = []
    for node in python_file_nodes:
        path_names = [n.name for n in node.path]
        node_path_str = functools.reduce(lambda a, b: a + "/" + b, path_names)
        python_file_names.append(node_path_str)
    root_remove_python_filenames = [f.replace("root/", "") for f in python_file_names]
    for file_name in root_remove_python_filenames:
        with open(file_name, "r") as file:
            file_text = file.read()
            classes = get_classes_from_file(file_text)
            r = Resolver("name")
            for found_class in classes:
                tree_path = "/root/" + file_name
                parent_node = r.get(tree, tree_path)
                x = Node(found_class, parent=parent_node, type="Class")
    return tree


def get_python_files(starting_path, exclude_pattern="venv|test_|__init__"):

    glob_path = f"{starting_path}/**/*.py"
    print(f"glob_path: {glob_path}")
    files = glob.glob(glob_path, recursive=True)
    included_files = [f for f in files if not re.findall(exclude_pattern, f)]
    return included_files


def create_tree(files):
    root = Node("root", type="root")
    parent_node = root

    r = Resolver("name")
    for file in files:
        parent_node = root
        paths = []
        path = "/root"
        for part in file.split("/"):
            path = path + "/" + part
            try:
                found_node_already = r.get(root, path)
                parent_node = found_node_already
            except ChildResolverError:
                node_type = "dir"
                if part.endswith(".py"):
                    node_type = "file"
                current_node = Node(part, parent=parent_node, type=node_type)
                parent_node = current_node
    return root

    output = """digraph D {

  subgraph cluster_p {
    label = "Parent";

    subgraph cluster_c1 {
      label = "Child one";
      a;

      subgraph cluster_gc_1 {
        label = "Grand-Child one";
         b;
      }
      subgraph cluster_gc_2 {
        label = "Grand-Child two";
          c;
          d;
      }

    }

    subgraph cluster_c2 {
      label = "Child two";
      e;
    }
  }

    a -> b
    c -> e
}
"""


def get_ascii_tree(root, include_types=False):
    tree_text = ""
    type_text = ""
    for pre, _, node in RenderTree(root):
        if include_types:
            type_text = " (" + node.type + ")"
        tree_text = tree_text + f"{pre}{node.name}{type_text}\n"
    return tree_text


def get_classes_from_file(file_text):
    classes = re.findall("class [^:]+", file_text)
    remove_class_definition = [c.replace("class ", "") for c in classes]
    remove_empty_paran = [c.replace("()", "") for c in remove_class_definition]
    return remove_empty_paran


if __name__ == "__main__":
    main()
