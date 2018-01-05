import argparse
import os
import piexif
import shutil
import time

from pathlib import Path

def bytes_to_str(bytes):
    return "".join(map(chr, bytes))

def extract_exif_data(exif_dict):
    return exif_dict["Exif"]

def extract_creation_date(exif_data):
    date_time_original_str = bytes_to_str(exif_data[36867])
    return time.strptime(date_time_original_str, "%Y:%m:%d %H:%M:%S")

def creation_date_from_photo(file_name):
    exif_dict = piexif.load(file_name)
    exif_data = extract_exif_data(exif_dict)
    return extract_creation_date(exif_data)

def path_str_from_date(t):
    return Path(time.strftime("%Y/%m/%Y_%m_%d_%H_%M_%S", t))

def path_from_photo_creation_date(photo_file):
    creation_date = creation_date_from_photo(str(photo_file))
    path_with_creation_date = path_str_from_date(creation_date).with_suffix(photo_file.suffix)
    return Path(os.path.join(photo_file.parent, path_with_creation_date))

def src_dest_path_from_photo_creation_date(photo_file):
    return {photo_file: path_from_photo_creation_date(photo_file)}

def make_reversed_multidict(a_dict):
    reversed_multidict = dict()
    for key, value in a_dict.items():
        reversed_multidict.setdefault(value, list()).append(key)
    return reversed_multidict

def append_counter_to_path(path, counter):
    new_file_name = path.stem + "_" + "{:02}".format(counter) + path.suffix
    return Path(os.path.join(path.parent, new_file_name))

def make_unique_paths_into(src_paths, src_to_dest_paths):
        counter = int(0)
        for src_path in src_paths:
            src_to_dest_paths[src_path] = append_counter_to_path(src_to_dest_paths[src_path], counter)
            counter += 1

def make_dest_paths_unique(src_to_dest_paths):
    dest_paths_to_list_of_src_paths = make_reversed_multidict(src_to_dest_paths)
    list_of_src_paths_with_same_dest_paths = dest_paths_to_list_of_src_paths.values()
    for src_paths in list_of_src_paths_with_same_dest_paths:
        make_unique_paths_into(src_paths, src_to_dest_paths)
    return src_to_dest_paths

def iterate_over_photo_files(folder):
    src_dest_map = dict()
    for fn in os.listdir(folder):
        try:
            file_path = os.path.join(folder, fn)
            if os.path.isfile(file_path):
                src_dest_map.update(src_dest_path_from_photo_creation_date(Path(file_path)))
        except:
            pass
    return make_dest_paths_unique(src_dest_map)


parser = argparse.ArgumentParser(description='renames photo files by creation date')
parser.add_argument('--photo_folder'
                    , required = True
                    , type = Path
                    , help = 'folder containing photos to be renamed')

args = parser.parse_args()
photo_folder = vars(args)['photo_folder']

for src, dest in iterate_over_photo_files(photo_folder).items():
    dest.parent.mkdir(parents = True, exist_ok = True)
    shutil.move(src, dest)
