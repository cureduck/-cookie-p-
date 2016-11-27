# Used information from:
# http://stackoverflow.com/questions/463832/using-dpapi-with-python
# http://www.linkedin.com/groups/Google-Chrome-encrypt-Stored-Cookies-36874.S.5826955428000456708

from ctypes import *
from ctypes.wintypes import DWORD




LocalFree = windll.kernel32.LocalFree
memcpy = cdll.msvcrt.memcpy
CryptProtectData = windll.crypt32.CryptProtectData
CryptUnprotectData = windll.crypt32.CryptUnprotectData
CRYPTPROTECT_UI_FORBIDDEN = 0x01

class DATA_BLOB(Structure):
    _fields_ = [("cbData", DWORD), ("pbData", POINTER(c_char))]

def getData(blobOut):
    cbData = int(blobOut.cbData)
    pbData = blobOut.pbData
    buffer = c_buffer(cbData)
    memcpy(buffer, pbData, cbData)
    LocalFree(pbData)
    return buffer.raw

def encrypt(plainText):
    bufferIn = c_buffer(plainText, len(plainText))
    blobIn = DATA_BLOB(len(plainText), bufferIn)
    blobOut = DATA_BLOB()

    if CryptProtectData(byref(blobIn), u"python_data", None,
                       None, None, CRYPTPROTECT_UI_FORBIDDEN, byref(blobOut)):
        return getData(blobOut)
    else:
        raise Exception("Failed to encrypt data")

def decrypt(cipherText):
    bufferIn = c_buffer(cipherText, len(cipherText))
    blobIn = DATA_BLOB(len(cipherText), bufferIn)
    blobOut = DATA_BLOB()

    if CryptUnprotectData(byref(blobIn), None, None, None, None,
                              CRYPTPROTECT_UI_FORBIDDEN, byref(blobOut)):
        return getData(blobOut)
    else:
        raise Exception("Failed to decrypt data")



a=b"\x01\x00\x00\x00\xd0\x8c\x9d\xdf\x01\x15\xd1\x11\x8cz\x00\xc0O\xc2\x97\xeb\x01\x00\x00\x00\x03\xb4\xdb\xed\xceMLK\x97W\x02\x95\x1f\x95\x9d\xc3\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x10f\x00\x00\x00\x01\x00\x00 \x00\x00\x00\xc3\xf6\xbe}x\x1dY\xd6\xb6\x8c\xd1\x89\xb1*\x1evby\xdd\xe2\x01\x0cli\x05\xd3\x19\xb2\x98\xbf\x99N\x00\x00\x00\x00\x0e\x80\x00\x00\x00\x02\x00\x00 \x00\x00\x00g\x1eo\xac\xdf6\x8b~\x9c\xd6\xda\xab\xc1`\xa7\xfeS1,R\x12\xdd\xeb\xcf\x08C\xda\x0f\x1c4_\xf50\x00\x00\x00\xb4\x8d'Egos=h\xf9o\xc6U\x81\xd9\x8d\x8b\x18\xc4\x97/\x1e\xb5\x10w\xabG\xf5J5\x84S1\xfb\xc8\xe5\x00\xfe8\x1d\x0e\x860\xd4\xe1q)\xa4@\x00\x00\x00`S\x84\xcfZ\xb1\xec\xc8?\xc3\xec\t\xe1\xcaC\xe2\x83i\xdd\xb9:,\x19\xa5\xfc\xd7\xe0x\xae#\xbb\x0b\xac^\xbe@H\xe60\x15q\xf3nP\xb1o\x9a\x8e\x8f\x9a\x8f\xa2\xb0\xd93q&k\xf1\xb2\xfc\xcc\x84\xc8"
print(decrypt(a))

