import time
import piexif

import unittest

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

def file_name_from_time(t):
    return time.strftime("%Y_%m_%d_%H_%M_%S", t)

def file_name_from_photo_creation_date(photo_file):
    return file_name_from_time(creation_date_from_photo(photo_file));

class TestPhotoSorter(unittest.TestCase):

    def test_photo_creation_date(self):
        photo_file_name = file_name_from_photo_creation_date("test/photo.jpg")
        self.assertEqual(photo_file_name, "2015_03_01_14_08_43")

if __name__ == '__main__':
    unittest.main()
