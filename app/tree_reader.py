import os

def generate_tree_structure(folder_path):
  tree_structure = {}

  for root, dirs, _ in os.walk(folder_path):
    for dir_name in dirs:
      dir_path = os.path.join(root, dir_name)
      files_in_dir = [os.path.splitext(file)[0] for file in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, file))]
      # Append the directory and its files to the tree structure
      tree_structure[dir_name] = {
          'videos': files_in_dir
      }
      
  return tree_structure

x = generate_tree_structure("./songs")