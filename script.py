import argparse
import os
import shutil
from pathlib import Path
from photo_sorter import PhotoSorter

def iterate_over_photo_files(folder, dest_folder):
    src_dest_map = dict()
    sorter = PhotoSorter(folder, dest_folder)
    for fn in os.listdir(folder):
        file_path = os.path.join(folder, fn)
        if os.path.isfile(file_path):
            try:
                src_dest_map.update(
                    sorter.src_dest_path_from_photo_creation_date(Path(file_path), dest_folder))
            except Exception as e:
                print(e)
    print(src_dest_map)
    return sorter.make_dest_paths_unique(src_dest_map)

parser = argparse.ArgumentParser(description='renames photo files by creation date')
parser.add_argument('--photo_folder'
                    , required = True
                    , type = Path
                    , help = 'folder containing photos to be renamed')
parser.add_argument('--destination_folder'
                    , required = True
                    , type = Path
                    , help = 'folder where renamed photos shall moved into')

args = parser.parse_args()
photo_folder = vars(args)['photo_folder']
dest_folder = vars(args)['destination_folder']

try:
    for src, dest in iterate_over_photo_files(photo_folder, dest_folder).items():
        try:
            dest.parent.mkdir(parents = True, exist_ok = True)
            shutil.move(src, dest)
        except Exception as e:
            print(e)
except Exception as e:
    print(e)
