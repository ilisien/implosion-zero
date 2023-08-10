from enum import Enum

class ImageType(Enum):
    RGB565 = "c"
    GRAYSCALE = "g"

class ImageSizePreset(Enum):
    FS_96X96 = "96"
    FS_QQVGA = "QQ"
    FS_QCIF = "QC"
    FS_HQVGA = "HQ"
    FS_240X240 = "24"
    FS_QVGA = "QV"
    FS_CIF = "CI"
    FS_HVGA = "HV"
    FS_VGA = "VG"
    FS_SVGA = "SV"
    FS_XGA = "XG"
    FS_HD = "HD"
    FS_SXGA = "SX"
    FS_UXGA = "UX"
    FS_FHD = "FH"
    FS_P_HD = "PH"
    FS_P_3MP = "P3"
    FS_QXGA = "QX"
    FS_QHD = "QH"
    FS_WQXGA = "WQ"
    FS_P_FHD = "PF"
    FS_QSXGA = "QS"

class MessageType(Enum):
    UNICODE_MESSAGE = "u"
    ERROR_MESSAGE = "e"
    REQUEST_IMAGE_MESSAGE = "r"
    IMAGE_MESSAGE = "i"

FRAME_RES = {
    "96":(96,96), #     96X96
    "QQ":(160,120), #   QQVGA
    "QC":(176,144), #   QCIF
    "HQ":(240,176), #   HQVGA
    "24":(240,240), #   240X240
    "QV":(320,240), #   QVGA
    "CI":(400,296), #   CIF
    "HV":(480,320), #   HVGA
    "VG":(640,480), #   VGA
    "SV":(800,600), #   SVGA
    "XG":(1024,768), #  XGA
    "HD":(1280,720), #  HD
    "SX":(1280,1024), # SXGA
    "UX":(1600,1200), # UXGA
    "FH":(1920,1080), # FHD
    "PH":(720,1280), #  P_HD
    "P3":(864,1536), #  P_3MP
    "QX":(2048,1536), # QXGA
    "QH":(2560,1440), # QHD
    "WQ":(2560,1600), # WQXGA
    "PF":(1080,1920), # P_FHD
    "QS":(2560,1920), # QSXGA
}