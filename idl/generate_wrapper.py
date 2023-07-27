#!/bin/python3

import sys
import subprocess
from pathlib import Path
import argparse
import shutil
import fnmatch

def main():
    parser = argparse.ArgumentParser(
                    prog = 'generate_wrapper.py',
                    description = 'Generate C++ Wrappers from IDL Files',
                    epilog = '(c) by TUM')

    parser.add_argument('-s', '--source')
    parser.add_argument('-d', '--destination')
    parser.add_argument('-i', '--include', default="*")

    args = parser.parse_args()

    source_path = Path(args.source)
    destination_path = Path(args.destination)
    include_pattern = args.include

    temp_destination_path = destination_path / "temp"

    for path in Path('.').rglob('*.idl'):
        if not fnmatch.fnmatch(path.as_posix(), include_pattern):
            print("Skipped file: {0}".format(path))
            continue
        idl_file = path.parent / path.name
        dest_dir = temp_destination_path / path.parent
        if not dest_dir.is_dir():
            dest_dir.mkdir(parents=True)
        subprocess.run(["fastddsgen","-d", dest_dir.as_posix(), "-I", source_path.as_posix(), "-typeros2", "-cs", "-replace", idl_file.as_posix()])

    dest_include_path = destination_path / "include"
    for path in temp_destination_path.rglob('*.h'):
        fpath = path.parent / path.name
        dest_fpath = dest_include_path / fpath.relative_to(temp_destination_path)
        if not dest_fpath.parent.is_dir():
            dest_fpath.parent.mkdir(parents=True)
        shutil.move(fpath.as_posix(), dest_fpath.as_posix())

    dest_src_path = destination_path / "src"
    for path in temp_destination_path.rglob('*.cxx'):
        fpath = path.parent / path.name
        dest_fpath = dest_src_path / fpath.relative_to(temp_destination_path)
        if not dest_fpath.parent.is_dir():
            dest_fpath.parent.mkdir(parents=True)
        shutil.move(fpath.as_posix(), dest_fpath.as_posix())

if __name__ == "__main__":
    main()