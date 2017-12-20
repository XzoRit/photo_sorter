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

class TestPhotoSorter(unittest.TestCase):

    def test_photo_creation_date(self):
        creation_date = creation_date_from_photo("photo.jpg")
        self.assertEqual(creation_date.tm_year, 2015)
        self.assertEqual(creation_date.tm_mon, 1)
        self.assertEqual(creation_date.tm_mday, 1)
        self.assertEqual(creation_date.tm_hour, 10)
        self.assertEqual(creation_date.tm_min, 8)
        self.assertEqual(creation_date.tm_sec, 1)

if __name__ == '__main__':
    unittest.main()
