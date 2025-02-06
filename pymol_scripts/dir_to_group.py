
# dir_to_group
#
# Author: Trayder Thomas
# Date  : 2024-10-22
#
import pymol
import os

# example usage
# dir_to_group("Abl_structures/")

def dir_to_group(folder):
    """
    Will load parent_folder as a group, and all subfolders as subgroups
    All pdb files in each folder are loaded into the subgroup
    """
    for root, dirs, files in os.walk(folder):
        for d in dirs:
            foldername = os.path.join(root, d)
            cmd.group(d)
            cmd.group(os.path.basename(root), d)  # group by parent folder
            
            for f in os.listdir(foldername):
                if f.endswith(".pdb"):
                    filepath = os.path.join(foldername, f)
                    basename = os.path.splitext(f)[0]
                    cmd.load(filepath)
                    cmd.group(d, basename)    

cmd.extend("dir_to_group", dir_to_group)
print("A new function 'dir_to_group' was added to PyMOL.")
print("Type 'help dir_to_group' if you need help.")
