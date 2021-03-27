#!/usr/bin/env python3

import sys
import struct
import zlib
from elftools.elf.elffile import ELFFile

with open(sys.argv[1], "r+b") as f:
    elf = ELFFile(f)
    elf.get_section_by_name("")
    sec_index = elf._section_name_map["compressed"]
    section = elf._get_section_header(sec_index)

    section_offset = section["sh_offset"]
    section_size = section["sh_size"]

    sec_size_index = elf._section_name_map["compressed_size"]
    size_section = elf._get_section_header(sec_size_index)
    size_section_offset = size_section["sh_offset"]

    f.seek(section_offset)
    section_data = f.read(section_size)

    compressed_data = zlib.compress(section_data, level=9)
    if len(compressed_data) > section_size:
        print(len(compressed_data), len(section_data))
        raise RuntimeError("Smeh")
    f.seek(section_offset)
    f.write(compressed_data)
    f.write(b"\0" * (section_size - len(compressed_data)))

    binary_size = struct.pack("=Q", len(compressed_data))
    f.seek(size_section_offset)
    print(len(section_data), len(compressed_data))
    f.write(binary_size)

    print(section)
