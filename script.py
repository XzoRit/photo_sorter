import argparse
import shutil
from pathlib import Path
import photo_sorter

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

for src, dest in photo_sorter.iterate_over_photo_files(photo_folder, dest_folder).items():
    try:
        dest.parent.mkdir(parents = True, exist_ok = True)
        shutil.move(src, dest)
    except Exception as e:
        print(e)
