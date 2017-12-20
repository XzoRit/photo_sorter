import time
import piexif

import unittest

def extract_exif_data(exif_dict):
    return exif_dict["Exif"]

def creation_date_from_photo(file_name):
    exif_dict = piexif.load(file_name)
    exif_data = extract_exif_data(exif_dict)
    date_time_original = exif_data[36867]
    date_time_original_str = "".join(map(chr,date_time_original))
    return time.strptime(date_time_original_str, "%Y:%m:%d %H:%M:%S")

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
