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

def path_str_from_time(t):
    return Path(time.strftime("%Y/%m/%Y_%m_%d_%H_%M_%S", t))

def path_from_photo_creation_date(photo_file):
    return path_str_from_time(
        creation_date_from_photo(str(photo_file))).with_suffix(photo_file.suffix)

def src_dest_path_from_photo_creation_date(photo_file):
    return {photo_file: path_from_photo_creation_date(photo_file)}

def iterate_over_photo_files(folder):
    src_dest_map = dict()
    for fn in os.listdir(folder):
        try:
            file_path = os.path.join(folder, fn)
            if os.path.isfile(file_path):
                src_dest_map.update(src_dest_path_from_photo_creation_date(Path(file_path)))
        except:
            pass
    return src_dest_map

class TestPhotoSorter(unittest.TestCase):

    def test_iterate_over_photo_files(self):
        folder = "test"
        expected = {
            Path("test/photo_0.jpg"): Path("2015/03/2015_03_01_14_08_43.jpg"),
            Path("test/photo_1.jpg"): Path("2015/03/2015_03_01_14_08_43.jpg"),
            Path("test/photo_2.jpg"): Path("2015/03/2015_03_01_14_08_43.jpg"),
            Path("test/photo_3.jpg"): Path("2015/03/2015_03_01_14_08_43.jpg"),
            Path("test/photo_4.jpg"): Path("2015/03/2015_03_01_14_08_43.jpg"),
            Path("test/photo_5.jpg"): Path("2015/03/2015_03_01_14_08_43.jpg")
        }
        actual = iterate_over_photo_files(folder)
        self.assertDictEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
