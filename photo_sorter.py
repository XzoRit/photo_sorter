import time
import piexif

exif_dict = piexif.load("photo.jpg")
exif_data = exif_dict["Exif"]
date_time_original = exif_data[36867]
date_time_original_str = "".join(map(chr,date_time_original))
struct_time = time.strptime(date_time_original_str, "%Y:%m:%d %H:%M:%S")

print(struct_time)
