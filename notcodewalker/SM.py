import struct

class ByteReader:
    def __init__(self, stream, current_offset):
        self.stream = stream
        self.current_offset = current_offset
        self.system = True
        self.sys_size = 0

    def read_uint32(self):
        i = 0
        len = 4
        cnt = 0
        tmp = bytearray(len)
        i = self.current_offset
        while i < self.current_offset + len:
            tmp[cnt] = self.stream[i]
            cnt += 1
            i += 1
        accum = 0
        i = 0
        shift_by = 0
        while shift_by < 32:
            accum |= (tmp[i] & 0xff) << shift_by
            i += 1
            shift_by += 8
        self.current_offset += 4
        return accum

    def read_offset(self):
        offset = self.read_uint32()
        if offset == 0:
            value = 0
        else:
            if offset >> 28 != 5:
                raise Exception("Expected an offset")
            else:
                value = offset & 0x0fffffff
        return value

    def read_vector4d(self):
        x = self.read_float()
        y = self.read_float()
        z = self.read_float()
        w = self.read_float()
        return Vector4D(x, y, z, w)

    def read_float(self):
        accum = 0
        i = 0
        shift_by = 0
        while shift_by < 32:
            accum |= (self.stream[self.current_offset + i] & 0xff) << shift_by
            i += 1
            shift_by += 8
        self.current_offset += 4
        return struct.unpack('!f', struct.pack('!I', accum))[0]

    def read_uint16(self):
        low = self.stream[self.current_offset] & 0xff
        high = self.stream[self.current_offset + 1] & 0xff
        self.current_offset += 2
        return (high << 8) | low

    def read_int16(self):
        ret = ((self.stream[self.current_offset + 1].to_bytes(2, 'big')[0] << 8) | (self.stream[self.current_offset].to_bytes(2, 'big')[0] & 0xff)).to_bytes(2, 'big')[0]
        self.current_offset += 2
        return ret

    def read_data_offset(self):
        offset = self.read_uint32()
        if offset == 0:
            value = 0
        else:
            if offset >> 28 != 6:
                pass
            value = offset & 0x0fffffff
        return value

    def read_null_terminated_string(self, size):
        sb = ""
        got_null = False
        for i in range(size):
            b = self.read_byte()
            if not got_null:
                if b != 0:
                    sb += chr(b)
                else:
                    got_null = True
        return sb

    def read_null_terminated_string(self):
        sb = ""
        c = chr(self.stream[self.current_offset])
        while ord(c) != 0:
            sb += c
            self.current_offset += 1
            c = chr(self.stream[self.current_offset])
        return sb
    
    def read_string(self, length):
        sb = ""
        for i in range(length):
            c = chr(self.stream[self.current_offset])
            sb += c
            self.current_offset += 1
        return sb

    def to_array(self, bytes):
        arr = bytearray(bytes)
        for i in range(bytes):
            arr[i] = self.stream[self.current_offset]
            self.current_offset += 1
        return arr

    def to_array(self):
        return self.stream

    def to_array(self, start, end):
        ret_size = end - start
        ret_stream = bytearray(ret_size)
        self.set_current_offset(start)
        for i in range(ret_size):
            ret_stream[i] = self.stream[self.current_offset]
            self.current_offset += 1
        return ret_stream

    def read_byte(self):
        self.current_offset += 1
        return self.stream[self.current_offset - 1]

    def get_current_offset(self):
        return self.current_offset

    def set_current_offset(self, offset):
        self.current_offset = offset
        if not self.system:
            self.current_offset += self.sys_size

    def set_sys_size(self, size):
        self.sys_size = size

    def set_system_memory(self, system):
        self.system = system

    def get_byte_buffer(self, size):
        buffer = bytearray(size)
        for i in range(size):
            buffer[i] = self.read_byte()
        return buffer

    def read_bytes(self, p_count):
        buffer = bytearray(p_count)
        for i in range(p_count):
            buffer[i] = self.read_byte()
        return buffer

    @property
    def input_stream(self):
        return memoryview(self.stream)[self.current_offset:self.stream.size - self.current_offset]

    def skip_bytes(self, bytes):
        self.current_offset += bytes

    def has_flag(self, flags, flag):
        return flags & flag == flag

    def more_to_read(self):
        return len(self.stream) - self.current_offset

    def unsigned_int(self):
        i = self.read_uint32()
        return i & 0xffffffff


#############################

class ReadFunctions:
    def __init__(self, name):
        self.data_in = open(name, "rb")

    def __init__(self, file):
        self.data_in = open(file.absolute_path, "rb")

    def __init__(self, path):
        self.data_in = open(path.to_file().absolute_path, "rb")

    def close_file(self):
        try:
            self.data_in.close()
            return True
        except IOError:
            print("Unable to close file")
            return False

    def read_byte(self):
        try:
            return self.data_in.read(1)[0]
        except IOError:
            return -1

    def read_bytes(self, bytes):
        try:
            self.data_in.readinto(bytes)
        except IOError as e:
            raise RuntimeError(e)

    def read_int(self):
        try:
            return self.swap_int(struct.unpack("<i", self.data_in.read(4))[0])
        except IOError:
            return -1

    def read_short(self):
        try:
            return self.swap_short(struct.unpack("<h", self.data_in.read(2))[0])
        except IOError:
            return -1

    def read_float(self):
        bytes = bytearray(4)
        for i in range(3, -1, -1):
            bytes[i] = self.read_byte()
        return struct.unpack("<f", bytes)[0]

    def read_string(self, size):
        letter = "n"
        woord = ""
        for i in range(size):
            letter = self.read_char()
            woord += letter
        return woord

    def read_null_terminated_string(self, size=None):
        woord = ""
        if size is None:
            b = self.read_byte()
            while b != 0:
                woord += chr(b)
                b = self.read_byte()
        else:
            got_null = False
            for i in range(size):
                b = self.read_byte()
                if not got_null:
                    if b != 0:
                        woord += chr(b)
                    else:
                        got_null = True
        return woord

    def __init__(self, name):
        self.data_in = open(name, "rb")

    def close_file(self):
        self.data_in.close()

    def read_byte(self):
        return self.data_in.read(1)

    def read_bytes(self, size):
        return self.data_in.read(size)

    def read_int(self):
        return struct.unpack("!i", self.data_in.read(4))[0]

    def read_short(self):
        return struct.unpack("!h", self.data_in.read(2))[0]

    def read_float(self):
        return struct.unpack("!f", self.data_in.read(4))[0]

    def read_string(self, size):
        return self.data_in.read(size).decode("utf-8")

    def read_null_terminated_string(self, size=None):
        if size is not None:
            return self.data_in.read(size).rstrip(b'\x00').decode("utf-8")
        else:
            result = b''
            while True:
                b = self.data_in.read(1)
                if b == b'\x00':
                    break
                result += b
            return result.decode("utf-8")

    def read_char(self):
        return self.data_in.read(1).decode("utf-8")

    def swap_int(self, v):
        return (v >> 24) | ((v & 0xff00) << 8) | ((v & 0xff) << 24) | ((v >> 8) & 0xff00)

    def swap_short(self, i):
        return ((i & 0xff) << 8) | ((i >> 8) & 0xff)

    def swap_float(self, f):
        int_value = struct.pack("!f", f)
        int_value = struct.unpack("!i", int_value)[0]
        int_value = self.swap_int(int_value)
        return struct.unpack("!f", struct.pack("!i", int_value))[0]

    def read_vector3d(self):
        return (self.read_float(), self.read_float(), self.read_float())

    def read_vector4d(self):
        return (self.read_float(), self.read_float(), self.read_float(), self.read_float())

    def moreToRead(self):
        try:
            return int(self.dataIn.length() - self.dataIn.filePointer())
        except IOException as ex:
            logging.log(logging.ERROR, ex) #not real
        return 0

    @property
    def byteReader(self):
        try:
            stream = bytearray(dataIn.length())
            dataIn.readinto(stream)
            return ByteReader(stream, 0)
        except IOError:
            return None

    def getByteReader(self, size):
        stream = bytearray(size)
        dataIn.readinto(stream)
        return ByteReader(stream, 0)

    def seek(self, offset):
        try:
            dataIn.seek(offset)
        except IOError:
            logging.error("Error seeking in dataIn")

    def readUnsignedInt(self):
        i = self.readInt()
        return i & 0xffffffff

    def readArray(self, size):
        array = bytearray(size)
        try:
            dataIn.readinto(array)
        except IOError:
            logging.error("Error reading array from dataIn")
        return array


#####################
class Vector3D:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, v3d):
        self.x += v3d.x
        self.y += v3d.y
        self.z += v3d.z

    def __sub__(self, v3d):
        self.x -= v3d.x
        self.y -= v3d.y
        self.z -= v3d.z

    def __mul__(self, v3d):
        self.x *= v3d.x
        self.y *= v3d.y
        self.z *= v3d.z

    def __str__(self):
        return "{}, {}, {}".format(self.x, self.y, self.z)


#########

import math

class Vector4D:
    def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __add__(self, v4d):
        self.x += v4d.x
        self.y += v4d.y
        self.z += v4d.z
        self.w += v4d.w

    def __sub__(self, v4d):
        self.x -= v4d.x
        self.y -= v4d.y
        self.z -= v4d.z
        self.w -= v4d.w

    def __add__(self, v3d):
        self.x += v3d.x
        self.y += v3d.y
        self.z += v3d.z

    def __sub__(self, v3d):
        self.x -= v3d.x
        self.y -= v3d.y
        self.z -= v3d.z

    def print(self, name):
        print("{}: {}, {}, {}, {}".format(name, self.x, self.y, self.z, self.w))

    @property
    def axisAngle(self):
        scale = -1.0
        rot = Vector4D()
        rot.x = self.x / scale
        rot.y = self.y / scale
        rot.z = self.z / scale
        rot.w = math.acos(self.w) * 2.0
        rot.w = math.degrees(rot.w)
        return rot

    def __str__(self):
        return "{}, {}, {}, {}".format(self.x, self.y, self.z, self.w)

    def toVector3D(self):
        return Vector3D(self.x, self.y, self.z)


##########

import struct

class WriteBuffer:
    def __init__(self):
        self.byte_buffer = bytearray()

    def writeByte(self, waarde):
        self.byte_buffer.append(waarde)
        return 1

    def writeInt(self, waarde):
        bytes = struct.pack("<i", waarde)
        for b in bytes:
            self.writeByte(b)
        return 4

    def writeVector(self, x, y, z, w):
        self.writeFloat(x)
        self.writeFloat(y)
        self.writeFloat(z)
        if w != -1.0:
            self.writeFloat(w)
        else:
            self.writeInt(2139095041)
        return 16

    def writeVector(self, vec):
        self.writeFloat(vec.x)
        self.writeFloat(vec.y)
        self.writeFloat(vec.z)
        self.writeInt(2139095041)
        return 16

    def writeOffset(self, waarde):
        s_waarde = waarde
        bytes = struct.pack("<h", s_waarde)
        self.writeShort(waarde)
        self.writeShort(20480)
        return 4
# missing short2arr, float2arr, int2arr, and writefloat
import struct

class WriteBuffer:
    def __init__(self):
        self.byte_buffer = bytearray()

    def replaceDataOffset(self, offset_offset, new_offset):
        print("Newoffset: 0x{:x} {}".format(new_offset, new_offset))
        bytes = struct.pack(">i", new_offset)
        self.byte_buffer[offset_offset] = bytes[3]
        self.byte_buffer[offset_offset + 1] = bytes[2]
        self.byte_buffer[offset_offset + 2] = bytes[1]

    @property
    def array(self):
        return bytes(self.byte_buffer)

    @staticmethod
    def float2arr(f):
        n = struct.pack("<f", f)
        return n

    @staticmethod
    def short2arr(i):
        s = i
        bytes = struct.pack("<h", s)
        return bytes

    @staticmethod
    def int2arr(value):
        bytes = struct.pack("<i", value)
        return bytes



##########

import struct

class WriteFunctions:
    def __init__(self, name: str):
        self.dataOut = open(name, "wb")

    def closeFile(self) -> bool:
        try:
            self.dataOut.close()
        except IOError:
            return False
        return True

    def writeByte(self, value: int):
        try:
            self.dataOut.write(struct.pack('b', value))
        except IOError:
            pass

    def write(self, value: int):
        try:
            self.dataOut.write(struct.pack('i', value))
        except IOError:
            value = -1

    def writeShort(self, value: int):
        try:
            self.dataOut.write(struct.pack('h', value))
        except IOError:
            value = -1

def closeFile(self):
    try:
        self.dataOut.close()
        return True
    except Exception as e:
        return False

def writeByte(self, value: int):
    self.dataOut.write(value.to_bytes(1, "little"))

def write(self, value: int):
    value = int.from_bytes(value.to_bytes(4, "big"), "little")
    self.dataOut.write(value.to_bytes(4, "little"))

def writeShort(self, value: int):
    value = int.from_bytes(value.to_bytes(2, "big"), "little")
    self.dataOut.write(value.to_bytes(2, "little"))

def write(self, value: float):
    value = struct.pack("<f", value)
    self.dataOut.write(value)

def writeChar(self, value: str):
    self.dataOut.write(value.encode())

def writeString(self, value: str):
    for letter in value:
        self.writeChar(letter)

def writeNullTerminatedString(self, value: str):
    for letter in value:
        self.writeChar(letter)
    self.writeByte(0)

def write(self, vector: Vector3D):
    self.write(vector.x)
    self.write(vector.y)
    self.write(vector.z)

def write(self, vector: Vector4D):
    self.write(vector.x)
    self.write(vector.y)
    self.write(vector.z)
    self.write(vector.w)

def write(self, array: List[int]):
    for i in array:
        self.writeByte(i)

def seek(self, pos: int):
    self.dataOut.seek(pos)

def gotoEnd(self):
    self.dataOut.seek(0, 2)

@property
def fileSize(self):
    return self.dataOut.tell()


#########
class GtaDat:
    def __init__(self, path: str, game_dir: str):
        self.file_name = path
        self.game_dir = game_dir
        self.changed = False
        self.img = []
        self.ipl = []
        self.ide = []
        self.img_list = []
        self.water = []
        self.col_file = []
        self.splash = []
        self.load_gta_dat()
    
    def load_gta_dat(self):
        with open(self.file_name) as input_file:
            for line in input_file:
                if not line.startswith("#") and line.strip():
                    split = line.split(" ")
                    file_path = split[1].replace("platform:", "pc").replace("common:", "common").replace("IPL", "WPL")
                    if split[0] == "IMG":
                        self.img.append(file_path)
                    elif split[0] == "IDE":
                        self.ide.append(file_path)
                    elif split[0] == "IPL":
                        self.ipl.append(file_path)
                    elif split[0] == "IMGLIST":
                        self.img_list.append(file_path)
                    elif split[0] == "WATER":
                        self.water.append(file_path)
                    elif split[0] == "SPLASH":
                        self.splash.append(file_path)
                    elif split[0] == "COLFILE":
                        self.col_file.append(file_path)
        self.load_images_from_img_list()
    
    def load_images_from_img_list(self):
        for img_texts in range(len(self.img_list)):
            try:
                with open(self.game_dir + self.img_list[img_texts]) as input_img_text:
                    for line in input_img_text:
                        if line.startswith("platformimg:"):
                            self.img.append(line.replace("platformimg:", "pc").replace("\t", ""))
            except Exception as ex:
                print(f"Error: {ex}")


    def save(self):
        with open(self.fileName, "w") as output:
            output.write("# gta.dat generated by Shadow-Mapper\n\n")
            output.write("#\n")
            output.write("# Imglist\n")
            output.write("#\n\n")
            for i in range(len(self.imgList)):
                output.write("IMGLIST " + self.imgList[i].replace("pc", "platform:").replace("common", "common:"))
                output.write("\n")
            output.write("\n")
            output.write("#\n")
            output.write("# Water\n")
            output.write("#\n\n")
            for i in range(len(self.water)):
                output.write("WATER " + self.water[i].replace("pc", "platform:").replace("common", "common:"))
                output.write("\n")
            output.write("\n")
            output.write("#\n")
            output.write("# Object types\n")
            output.write("#\n\n")
            for i in range(len(self.ide)):
                output.write("IDE " + self.ide[i].replace("pc", "platform:").replace("common", "common:"))
                output.write("\n")
            output.write("\n")
            output.write("#\n")
            output.write("# IPL\n")
            output.write("#\n\n")
            for i in range(len(ide)):
                output.write("IDE " + ide[i].replace("pc", "platform:").replace("common", "common:"))
                output.write("\n")
        
            output.write("#\n")
            output.write("# IPL\n")
            output.write("#\n")
            output.write("\n")

            for i in range(len(ipl)):
                output.write("IPL " + ipl[i].replace("pc", "platform:").replace("common", "common:").replace("wpl", "ipl"))
                output.write("\n")
        
        output.flush()
        output.close()


## decrypter

import logging
import codecs
from Crypto.Cipher import AES

class Decrypter:
    def __init__(self, key):
        self.cipher = AES.new(key, AES.MODE_ECB)
        self.temp_buffer = bytearray(16)
        
    def decrypt16byteBlock(self, rf):
        rf.readBytes(self.temp_buffer)
        for j in range(16):
            try:
                self.temp_buffer = self.cipher.decrypt(self.temp_buffer)
            except Exception as ex:
                logging.getLogger(__name__).log(logging.ERROR, ex)
        return self.temp_buffer
    
    def decrypt(self, data):
        temp_data = data
        for j in range(16):
            try:
                temp_data = self.cipher.decrypt(temp_data)
            except Exception as ex:
                logging.getLogger(__name__).log(logging.ERROR, ex)
        return temp_data


## encrypter

import javax.crypto.Cipher
import javax.crypto.spec.SecretKeySpec

class Encrypter:
    def __init__(self, key):
        self.cipher = Cipher.getInstance("Rijndael/ECB/NoPadding")
        self.cipher.init(Cipher.ENCRYPT_MODE, SecretKeySpec(key, "Rijndael"))

    def encryptAES(self, data):
        return self.cipher.doFinal(data)


## key extract, update to new keys for 1.0.8.0 and up

class EncryptionKeyExtractor:
    version_data = []

    def __init__(self):
        self.version_data = self.load_version_data()

    def load_version_data(self):
        try:
            ini_editor = IniEditor()
            with open(self.__class__.__name__.getResourceAsStream("/versions.ini"), "rb") as f:
                ini_editor.load(f)

            return [
                Version(section_map.get(INI_KEY_NAME), section_map.get(INI_KEY_OFFSET))
                for section_map in (
                    ini_editor.getSectionMap(section_name)
                    for section_name in ini_editor.sectionNames()
                )
                if section_map.get(INI_KEY_NAME) and section_map.get(INI_KEY_OFFSET)
            ]
        except Exception as e:
            return []

    def get_key(self, game_dir):
        rf = ReadFunctions(f"{game_dir}GTAIV.exe")
        key = bytearray(32)

        version = next((version_data for version_data in self.version_data if version_data.offset == rf.seek(version_data.offset) and rf.readBytes(key) and HASHED_KEY == SHA1Hasher.hash(key)), None)

        rf.close_file()

        return key if version else None

    class Version:
        def __init__(self, name, offset):
            self.name = name
            self.offset = int(offset)

    HASHED_KEY = "DEA375EF1E6EF2223A1221C2C575C47BF17EFA5E"
    INI_KEY_NAME = "name"
    INI_KEY_OFFSET = "offset"

##hashing

### hashtable

class HashTable:
    def __init__(self, hasher):
        self.hashes = {}
        self.hasher = hasher
        self.missed_hash_count = 0

    def add(self, value):
        self.hashes[self.hasher.hash(value)] = value

    def add_with_hash(self, hash, value):
        if hash not in self.hashes:
            print(f"Hash was not generated by IDE entries '{value}'")
            self.missed_hash_count += 1
        self.hashes[hash] = value

    def __getitem__(self, hash):
        return self.hashes.get(hash)

## hasher

class Hasher:
    def hash(self, value: str) -> int:
        pass


## one-at-a-time, faster here to just group the lookup table array
class OneAtATimeHasher:
    def hash(self, value: str) -> int:
        return self.getHashKey(value)
    
    @staticmethod
    def getHashKeySubString(str: str, initialHash: int) -> int:
        hash = initialHash
        for c in str:
            hash += ord(c.upper())
            hash += (hash << 10)
            hash = hash ^ (hash >> 6)
        return hash

    @staticmethod
    def getHashKeyFinalize(str: str, initialHash: int) -> int:
        hash = OneAtATimeHasher.getHashKeySubString(str, initialHash)
        hash += (hash << 3)
        hash = hash ^ (hash >> 11)
        hash += (hash << 15)
        return hash

    @staticmethod
    def getHashKey(str: str, initialHash: int = 0) -> int:
        return OneAtATimeHasher.getHashKeyFinalize(str, initialHash)


## sha1 hasher

import hashlib
import binascii

def sha1_hash(input):
    try:
        sha1 = hashlib.sha1()
        sha1.update(input)
        return binascii.hexlify(sha1.digest()).decode('utf-8')
    except:
        return None


##### file chooser

class ExtensionFilter:
    def init(self, extensions, description):
        self.extensions = extensions
        self.description = description
    def accept(self, file):
        if file.is_directory():
            return True

        for extension in self.extensions:
            if extension == file.extension:
                return True

        return False

    def get_description(self):
        return f"{self.description} ({', '.join(self.extensions)})"

### chooser util

import tkinter as tk
from tkinter import filedialog

class FileChooserUtil:
    @staticmethod
    def open_file_chooser(parent, filter, initial_path=None):
        chooser = tk.filedialog.askopenfilename(
            initialdir=initial_path,
            title="Open file..",
            filetypes=filter
            )
        return chooser if chooser else None


### name filter

class FileNameFilter(FileFilter):
    def __init__(self, file_names, description):
        self.file_names = file_names
        self.description = description

    def accept(self, file):
        if file.isDirectory():
            return True
        return any(file_name == file.getName() for file_name in self.file_names)

    def getDescription(self):
        return f"{self.description} ({', '.join(self.file_names)})"


### constants

class Constants:
# file types
    ftDFF = 0
    ftTXD = 1
    ftCOL = 2
    ftIPL = 3
    ftIDE = 4
    ftWDR = 5
    ftWDD = 6
    ftWFT = 7
    ftWBN = 8
    ftWBD = 9
    ftWTD = 10
    ftWPL = 11
    ftWAD = 12
    ftIFP = 13
# Resource types
    rtWDR = 110
    rtWDD = 110
    rtWFT = 112
    rtWBN = 32
    rtWBD = 32
    rtWTD = 8
    rtWPL = 1919251285
    rtWAD = 1
    rtCUT = 1162696003

# Placement
    pINST = 0
    pCULL = 1
    pPATH = 2
    pGRGE = 3
    pENEX = 4
    pPICK = 5
    pJUMP = 6
    pTCYC = 7
    pAUZO = 8
    pMULT = 9
    pCARS = 10
    pOCCL = 11
    pZONE = 12

# IDE
    i2DFX = 0
    iANIM = 1
    iCARS = 2
    iHIER = 3
    iMLO = 4
    iOBJS = 5
    iPATH = 6
    iPEDS = 7
    iTANM = 8
    iTOBJ = 9
    iTREE = 10
    iTXDP = 11
    iWEAP = 12

### gametype

class GameType:
    GTA_III = ("III", "GTA III", "gta3.exe")
    GTA_VC = ("VC", "GTA VC", "gta-vc.exe")
    GTA_SA = ("SA", "GTA SA", "gta-sa.exe")
    GTA_IV = ("IV", "GTA IV", "GTAIV.exe")
    GTA_V = ("V", "GTA V", "GTA5.exe")

    @classmethod
    def by_id(cls, id: str):
        if id == "III":
            return cls.GTA_III
        elif id == "VC":
            return cls.GTA_VC
        elif id == "SA":
            return cls.GTA_SA
        elif id == "IV":
            return cls.GTA_IV
        elif id == "V":
            return cls.GTA_V
        else:
            return None


# utils

class Utils:

    @staticmethod
    def get_hex_string(value: int) -> str:
        hex_value = hex(value).upper().replace("0X", "")
        size = 4
        if len(hex_value) > 4:
            size = 8
        while len(hex_value) != size:
            hex_value = "0" + hex_value
        return "0x" + hex_value

    @staticmethod
    def get_shader_name(type: int) -> str:
        ret = "Unknown"
        if type == 0x2b5170fd:
            ret = "Texture"
        elif type == 0x608799c6:
            ret = "SpecularTexture"
        elif type == 0x46b7c64f:
            ret = "NormalTexture"
        elif type == -718597665:
            ret = "DiffuseMap1"
        elif type == 606121937:
            ret = "DiffuseMap2"
        elif type in [376311761, 1212833469, -15634147, -160355455, -2078982697, -677643234, -1168850544, 424198508, 514782960]:
            ret = "Vector"
        elif type == -260861532:
            ret = "Matrix"
        ret += " ({})".format(type)
        return ret

    @staticmethod
    def get_shader_type(type: int) -> str:
        ret = "Unknown {}".format(type)
        if type == 0:
            ret = "Texture"
        elif type == 4:
            ret = "Matrix"
        elif type == 1:
            ret = "Vector"
        return ret

    @staticmethod
    def get_file_type(file_name: str) -> int:
        file_name = file_name.lower()
        if file_name.endswith(".dff"):
            return Constants.ftDFF
        elif file_name.endswith(".txd"):
            return Constants.ftTXD
        elif file_name.endswith(".col"):
            return Constants.ftCOL
        elif file_name.endswith(".ipl"):
            return Constants.ftIPL
        elif file_name.endswith(".ide"):
            return Constants.ftIDE
        elif file_name.endswith(".wdr"):
            return Constants.ftWDR
        elif file_name.endswith(".wdd"):
            return Constants.ftWDD
        elif file_name.endswith(".wbn"):
            return Constants.ftWBN
        elif file_name.endswith(".wbd"):
            return Constants.ftWBD
        elif file_name.endswith(".wtd"):
            return Constants.ftWTD
        elif file_name.endswith(".wft"):
            return Constants.ftWFT
        elif file_name.endswith(".wad"):
            return Constants.ftWAD
        #finish these wpl ifp

    @staticmethod
    def get_resource_type(file_name: str) -> int:
        file_name = file_name.lower()
        if file_name.endswith(".wdr"):
            return Constants.rtWDR
        elif file_name.endswith(".wdd"):
            return Constants.rtWDD
        elif file_name.endswith(".wbn"):
            return Constants.rtWBN
        elif file_name.endswith(".wbd"):
            return Constants.rtWBD
        elif file_name.endswith(".wtd"):
            return Constants.rtWTD
        elif file_name.endswith(".wft"):
            return Constants.rtWFT
        elif file_name.endswith(".wad"):
            return Constants.rtWAD
        elif file_name.endswith(".wpl"):
            return Constants.rtWPL
        else:
            return -1

    @staticmethod
    def get_total_mem_size(flags: int) -> int:
        return Utils.get_system_mem_size(flags) + Utils.get_graphics_mem_size(flags)

    @staticmethod
    def get_system_mem_size(flags: int) -> int:
        return (flags & 0x7FF) << (((flags >> 11) & 0xF) + 8)

    @staticmethod
    def get_graphics_mem_size(flags: int) -> int:
        return ((flags >> 15) & 0x7FF) << (((flags >> 26) & 0xF) + 8)


# saving

class Saveable:
    def __init__(self):
        self._is_save_required = False

    @property
    def is_save_required(self):
        return self._is_save_required

    def set_save_required(self):
        self._is_save_required = True

    def set_save_required(self, is_save_required: bool):
        self._is_save_required = is_save_required

class SaveableFile(Saveable):
    pass