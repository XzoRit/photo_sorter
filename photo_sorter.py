import os
import piexif
import time

from pathlib import Path

class PhotoSorter:
    def __init__(self, photo_folder, dest_folder):
        self._photo_folder = photo_folder
        self._dest_folder = dest_folder

    def bytes_to_str(self, bytes):
        return "".join(map(chr, bytes))

    def extract_exif_data(self, exif_dict):
        return exif_dict["Exif"]

    def extract_creation_date(self, exif_data):
        date_time_original_str = self.bytes_to_str(exif_data[36867])
        return time.strptime(date_time_original_str, "%Y:%m:%d %H:%M:%S")

    def creation_date_from_photo(self, file_name):
        exif_dict = piexif.load(file_name)
        exif_data = self.extract_exif_data(exif_dict)
        return self.extract_creation_date(exif_data)

    def path_str_from_date(self, t):
        return Path(time.strftime("%Y/%m/%Y_%m_%d_%H_%M_%S", t))

    def path_from_photo_creation_date(self, photo_file, dest_folder):
        creation_date = self.creation_date_from_photo(str(photo_file))
        path_with_creation_date = self.path_str_from_date(creation_date).with_suffix(photo_file.suffix)
        return Path(os.path.join(dest_folder, path_with_creation_date))

    def src_dest_path_from_photo_creation_date(self, photo_file, dest_folder):
        return {photo_file: self.path_from_photo_creation_date(photo_file, dest_folder)}

    def make_reversed_multidict(self, a_dict):
        reversed_multidict = dict()
        for key, value in a_dict.items():
            reversed_multidict.setdefault(value, list()).append(key)
        return reversed_multidict

    def append_counter_to_path(self, path, counter):
        new_file_name = path.stem + "_" + "{:03}".format(counter) + path.suffix
        return Path(os.path.join(path.parent, new_file_name))

    def make_unique_paths_into(self, src_paths, src_to_dest_paths):
            counter = int(0)
            for src_path in src_paths:
                src_to_dest_paths[src_path] = self.append_counter_to_path(src_to_dest_paths[src_path], counter)
                counter += 1

    def make_dest_paths_unique(self, src_to_dest_paths):
        dest_paths_to_list_of_src_paths = self.make_reversed_multidict(src_to_dest_paths)
        list_of_src_paths_with_same_dest_paths = dest_paths_to_list_of_src_paths.values()
        for src_paths in list_of_src_paths_with_same_dest_paths:
            self.make_unique_paths_into(src_paths, src_to_dest_paths)
        return src_to_dest_paths
