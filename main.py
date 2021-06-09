import glob
import re

from anytree import Node, RenderTree, search, Resolver, ChildResolverError


def main():

    pass


def get_python_files(starting_path, exclude_pattern="venv|test_|__init__"):

    glob_path = f"{starting_path}/**/*.py"
    print(f"glob_path: {glob_path}")
    files = glob.glob(glob_path, recursive=True)
    included_files = [f for f in files if not re.findall(exclude_pattern, f)]
    return included_files


def create_tree(files):
    root = Node("project")
    parent_node = root

    r = Resolver("name")
    for file in files:
        parent_node = root
        print(f"\n\nfile: {file}")
        paths = []
        path = "/project"
        for part in file.split("/"):
            path = path + "/" + part
            print(f"\nprocessing {part} for {path}")
            try:
                found_node_already = r.get(root, path)
                parent_node = found_node_already
            except ChildResolverError:
                print(f"\tadding node: {path} to {parent_node}")
                current_node = Node(part, parent=parent_node)
                parent_node = current_node
                print(f"\t\t\t{current_node.path}")

    print("\n\n")
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


def get_ascii_tree(root):
    tree_text = ""
    for pre, _, node in RenderTree(root):
        tree_text = tree_text + f"{pre}{node.name}\n"
    return tree_text


if __name__ == "__main__":
    main()
