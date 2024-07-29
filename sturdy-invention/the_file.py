import os
import re

from shutil import copy2

DIRS = {
    "memories",
    "chat_media",
}

ymd_pattern = r'^(?P<date>\d{4}-\d{2}-\d{2})'

def format_seconds(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return f"{int(hours):02d}.{int(minutes):02d}.{int(seconds):02d}"

class TheFile:
    def __init__(self, og_path, dest):
        self.dest = dest
        self.og_path = og_path
        self.og_basename = os.path.basename(og_path)
        _, self.ext = os.path.splitext(og_path)
    
    @property
    def destination_dir(self):
        return f"{self.dest}/{self.destination_parent_dir}"

    @property
    def destination_parent_dir(self):
        if not self.filename_is_ymd_format:
            return "other"

        pardir = os.path.basename(os.path.dirname(self.og_path))
        
        return pardir if pardir in DIRS else "other"

    @property
    def filename_is_ymd_format(self):
        return bool(re.search(ymd_pattern, self.og_basename))
    
    @property
    def full_dest(self):
        return f"{self.destination_dir}/{self.new_filename}"
    
    @property
    def new_filename(self):
        match = re.match(ymd_pattern, self.og_basename)

        if not match:
            return self.og_basename
        
        date = match.group("date")

        seconds = 0
        filename = lambda seconds: f"{date} {format_seconds(seconds)}{self.ext}"

        while os.path.exists(f"{self.destination_dir}/{filename(seconds)}"):
            seconds += 1

        return filename(seconds)
    
    def copy(self):
        return copy2(self.og_path, self.full_dest)