import os
import shutil
from typing import List

def copy_static(recursion_path: str) -> None:
    if recursion_path == "":
        shutil.rmtree("./public")
    current_folder = os.path.join("./static", recursion_path)
    folder_path = os.path.join("./public", recursion_path)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    for path in os.listdir(current_folder):
        current_path = os.path.join(current_folder, path)
        new_file_path = os.path.join("./public", recursion_path, path)
        if os.path.isfile(current_path):
            shutil.copy(current_path, new_file_path)
        else:
            copy_static(os.path.join(recursion_path, path))


def main():
    copy_static("")

# # Open the file in read mode ('r')
#     with open('markdown1.text', 'r') as file:
#         # Read the entire file content
#         content = file.read()
#         print(content)

main()

