# Copyright Alexander Argentakis
# Repo: https://github.com/MFDGaming/mcpe-0.6.1-mod-sdk
# This file is licensed under the GPL v2.0 license

from struct import pack, unpack

MAGIC = b"\xff\x50\x54\x50"
MINECRAFT_VERSION = 209

class NoPatches(Exception):
    pass

class MaxPatchCountReached(Exception):
    pass

class Patch:
    def __init__(self, memory_address = 0, code = b""):
        self.memory_address = memory_address
        self.code = code

    def generate_patch_from_binary(self, binary_path, memory_address, code_length):
        file = open(binary_path, "rb")
        file.seek(memory_address)
        self.code = file.read(code_length)
        file.close()

class Mod:
    def __init__(self):
        self.patches = []

    def add_patch(self, patch):
        if len(self.patches) < 256:
            self.patches.append(patch)
        else:
            raise MaxPatchCountReached("You can't add more than 256 patches.")

    def generate_indices(self):
        indices = []
        if self.patches:
            old_code_length = len(self.patches[0].code) + 4
            old_index = 6 + (len(self.patches) * 4)
            indices.append(old_index)
            for patch in self.patches[1:]:
                old_index = old_index + old_code_length
                old_length = len(patch.code) + 4
                indices.append(old_index)
        return indices

    def save(self, mod_path):
        if self.patches:
            indices = self.generate_indices()
            data = MAGIC + bytes([MINECRAFT_VERSION]) + bytes([len(self.patches)])
            for indice in indices:
                data += pack(">I", indice)
            for patch in self.patches:
                data += pack(">I", patch.memory_address)
                data += patch.code
            file = open(mod_path, "wb")
            file.write(data)
            file.close()
        else:
            raise NoPatches("Cannot save there are no patches.")
