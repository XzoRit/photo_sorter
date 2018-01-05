import os
import piexif
import time

import unittest

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

def make_dest_paths_unique(src_to_dest_paths):
    dest_paths_to_list_of_src_paths = make_reversed_multidict(src_to_dest_paths)

    list_of_src_paths_with_same_dest_paths = [
        list_of_src_paths
        for _, list_of_src_paths in dest_paths_to_list_of_src_paths.items()
        if len(list_of_src_paths) > 1
    ]

    for src_paths in list_of_src_paths_with_same_dest_paths:
        counter = int(0)
        for src_path in src_paths:
            src_to_dest_paths[src_path] = append_counter_to_path(src_to_dest_paths[src_path], counter)
            counter += 1

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

class TestPhotoSorter(unittest.TestCase):

    def test_iterate_over_photo_files(self):
        folder = "test"
        expected = {  Path("test/photo_0.jpg"): Path("test/2015/03/2015_03_01_14_08_43_00.jpg")
                    , Path("test/photo_1.jpg"): Path("test/2015/03/2015_03_01_14_08_43_01.jpg")
                    , Path("test/photo_2.jpg"): Path("test/2015/03/2015_03_01_14_08_43_02.jpg")
                    , Path("test/photo_3.jpg"): Path("test/2015/03/2015_03_01_14_08_43_03.jpg")
                    , Path("test/photo_4.jpg"): Path("test/2015/03/2015_03_01_14_08_43_04.jpg")
                    , Path("test/photo_5.jpg"): Path("test/2015/03/2015_03_01_14_08_43_05.jpg")
        }
        actual = iterate_over_photo_files(folder)
        self.assertDictEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
