"""
Was used for sorting through SnapChat media.
"""

import os
import pathlib

from dotenv import load_dotenv
from send2trash import send2trash
from the_file import TheFile

load_dotenv()

destination_dir = pathlib.Path(os.environ.get("DESTINATION_DIR"))
processing_dir = pathlib.Path(os.environ.get("PROCESSING_DIR"))

if not os.path.exists(destination_dir):
    print("Destination directory does not exist. Stopping.")
    exit()

if not os.path.exists(processing_dir):
    print("Processing directory does not exist. Stopping.")
    exit()


paths_to_trash = set()
for filepath in processing_dir.rglob("*"):
    if os.path.isdir(filepath):
        paths_to_trash.add(filepath)
        continue

    the_file = TheFile(
        dest=destination_dir,
        og_path=filepath
    )

    new_filepath = the_file.copy()
    print(f"{the_file.og_path} -> {new_filepath}")


for path_to_trash in paths_to_trash:
    if os.path.isdir(path_to_trash) and not len(os.listdir(path_to_trash)):
        send2trash(path_to_trash)