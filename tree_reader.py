import os
import csv

def generate_tree_structure(folder_path):
  tree_structure = {}

  for root, dirs, files in os.walk(folder_path):
    for dir_name in dirs:
      dir_path = os.path.join(root, dir_name)
      files_in_dir = [file for file in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, file))]
      # Append the directory and its files to the tree structure
      tree_structure[dir_name] = {
          'videos': files_in_dir
      }
      
  return tree_structure

def export_to_csv(tree_structure, csv_filename='tree_structure.csv'):
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['Directory', 'Files']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()

        # Write each row in the tree structure
        for entry in tree_structure:
            writer.writerow(entry)

