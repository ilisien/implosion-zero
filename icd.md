# *xiao-pi serial interface:* - version `0`

## *header*
header for all serial messages
| byte | format | section       | details                                          |
| ---- | ------ | ------------- | ------------------------------------------------ |
| 0,1  | raw    | sync seq      | "1", then "0" byte to sync start of message      |
| 2    | char8  | message type  | character defining the type of message           |
| 3    | uint8  | version       | version of message                               |
| 4-7  | uint32 | message count | total number of messages sent by this node       |
| 8-11 | uint32 | data length   | number of bytes to be looking for in the message |

## *messages*
message types
### *unicode message* - `u`
a debug message with unicode functionality
| byte | format | section | details                          |
| ---- | ------ | ------- | -------------------------------- |
| h+*  | string | message | unicode string sending a message |

### *error message* - `e`
an error message with unicode functionality
| byte | format | section       | details                             |
| ---- | ------ | ------------- | ----------------------------------- |
| h+1  | char   | error type    | the type of error that has occured  |
| h+*  | string | error message | unicode string saying what happened |

### *request image* - `r`
a message to request an image from a given camera or set of cameras
| byte  | format | section           | details                              |
| ----- | ------ | ----------------- | ------------------------------------ |
| h+1   | uint   | camera id         | which camera to take a picture with  |
| h+2   | char   | image type        | see image type in misc codes         |
| h+3,4 | string | image size preset | see image size presets in misc codes |

### *image* - `i`
an image message
| byte  | format          | section           | details                                                          |
| ----- | --------------- | ----------------- | ---------------------------------------------------------------- |
| h+1   | char            | image type        | see image type in misc codes                                     |
| h+2,3 | string          | image size preset | see image size presets in misc codes                             |
| h+*   | array of pixels | pixels of image   | 1bytepp or 2bytepp for grayscale or rgb565 (color), respectively |

## *misc codes*
### *image types*
| char | meaning         |
| ---- | --------------- |
| `c`  | color image     |
| `g`  | grayscale image |

### *image size presets*
| chars | size preset | width (x) | length (y) |
| ----- | ----------- | --------- | ---------- |
| `96`  | 96X96       | 96        | 96         |
| `QQ`  | QQVGA       | 160       | 120        |
| `QC`  | QCIF        | 176       | 144        |
| `HQ`  | HQVGA       | 240       | 176        |
| `24`  | 240X240     | 240       | 240        |
| `QV`  | QVGA        | 320       | 240        |
| `CI`  | CIF         | 400       | 296        |
| `HV`  | HVGA        | 480       | 320        |
| `VG`  | VGA         | 640       | 480        |
| `SV`  | SVGA        | 800       | 600        |
| `XG`  | XGA         | 1024      | 768        |
| `HD`  | HD          | 1280      | 720        |
| `SX`  | SXGA        | 1280      | 1024       |
| `UX`  | UXGA        | 1600      | 1200       |
| `FH`  | FHD         | 1920      | 1080       |
| `PH`  | P_HD        | 720       | 1280       |
| `P3`  | P_3MP       | 864       | 1536       |
| `QX`  | QXGA        | 2048      | 1536       |
| `QH`  | QHD         | 2560      | 1440       |
| `WQ`  | WQXGA       | 2560      | 1600       |
| `PF`  | P_FHD       | 1080      | 1920       |
| `QS`  | QSXGA       | 2560      | 1920       |

