import os
import ctypes
from ctypes import wintypes

from PIL import Image


# =========================================================
# Windows DLLs
# =========================================================

shell32 = ctypes.windll.shell32
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32


# =========================================================
# Windows constants
# =========================================================

SHGFI_ICON = 0x000000100
SHGFI_LARGEICON = 0x000000000

DIB_RGB_COLORS = 0
BI_RGB = 0


# =========================================================
# Windows structures
# =========================================================

class SHFILEINFO(ctypes.Structure):

    _fields_ = [

        ("hIcon", wintypes.HICON),

        ("iIcon", ctypes.c_int),

        ("dwAttributes", wintypes.DWORD),

        (
            "szDisplayName",
            wintypes.WCHAR * 260
        ),

        (
            "szTypeName",
            wintypes.WCHAR * 80
        )
    ]


class BITMAPINFOHEADER(ctypes.Structure):

    _fields_ = [

        ("biSize", wintypes.DWORD),

        ("biWidth", wintypes.LONG),

        ("biHeight", wintypes.LONG),

        ("biPlanes", wintypes.WORD),

        ("biBitCount", wintypes.WORD),

        ("biCompression", wintypes.DWORD),

        ("biSizeImage", wintypes.DWORD),

        ("biXPelsPerMeter", wintypes.LONG),

        ("biYPelsPerMeter", wintypes.LONG),

        ("biClrUsed", wintypes.DWORD),

        ("biClrImportant", wintypes.DWORD)
    ]


class BITMAPINFO(ctypes.Structure):

    _fields_ = [

        ("bmiHeader", BITMAPINFOHEADER),

        ("bmiColors", wintypes.DWORD * 3)
    ]


# =========================================================
# Extract Windows icon
# =========================================================

def extract_icon(
    source_path,
    output_path,
    size=64
):

    try:

        # -------------------------------------------------
        # Get Windows icon
        # -------------------------------------------------

        shinfo = SHFILEINFO()

        result = shell32.SHGetFileInfoW(
            source_path,
            0,
            ctypes.byref(shinfo),
            ctypes.sizeof(shinfo),
            SHGFI_ICON | SHGFI_LARGEICON
        )

        if result == 0:

            print(
                "Could not find icon."
            )

            return False


        # -------------------------------------------------
        # Device contexts
        # -------------------------------------------------

        screen_dc = user32.GetDC(0)

        memory_dc = gdi32.CreateCompatibleDC(
            screen_dc
        )

        bitmap = gdi32.CreateCompatibleBitmap(
            screen_dc,
            size,
            size
        )

        old_bitmap = gdi32.SelectObject(
            memory_dc,
            bitmap
        )


        # -------------------------------------------------
        # Draw icon
        # -------------------------------------------------

        user32.DrawIconEx(
            memory_dc,
            0,
            0,
            shinfo.hIcon,
            size,
            size,
            0,
            0,
            0x0003
        )


        # -------------------------------------------------
        # Bitmap information
        # -------------------------------------------------

        bmi = BITMAPINFO()

        bmi.bmiHeader.biSize = ctypes.sizeof(
            BITMAPINFOHEADER
        )

        bmi.bmiHeader.biWidth = size

        bmi.bmiHeader.biHeight = -size

        bmi.bmiHeader.biPlanes = 1

        bmi.bmiHeader.biBitCount = 32

        bmi.bmiHeader.biCompression = BI_RGB


        # -------------------------------------------------
        # Pixel buffer
        # -------------------------------------------------

        buffer_size = size * size * 4

        buffer = ctypes.create_string_buffer(
            buffer_size
        )


        result = gdi32.GetDIBits(
            memory_dc,
            bitmap,
            0,
            size,
            buffer,
            ctypes.byref(bmi),
            DIB_RGB_COLORS
        )

        if result == 0:

            print(
                "Could not read bitmap."
            )

            return False


        # -------------------------------------------------
        # PIL
        # -------------------------------------------------

        image = Image.frombuffer(
            "RGBA",
            (size, size),
            buffer,
            "raw",
            "BGRA",
            0,
            1
        )


        # -------------------------------------------------
        # Save
        # -------------------------------------------------

        directory = os.path.dirname(
            output_path
        )

        if directory:

            os.makedirs(
                directory,
                exist_ok=True
            )

        image.save(
            output_path,
            "PNG"
        )


        # -------------------------------------------------
        # Cleanup
        # -------------------------------------------------

        gdi32.SelectObject(
            memory_dc,
            old_bitmap
        )

        gdi32.DeleteObject(
            bitmap
        )

        gdi32.DeleteDC(
            memory_dc
        )

        user32.ReleaseDC(
            0,
            screen_dc
        )

        user32.DestroyIcon(
            shinfo.hIcon
        )


        return True


    except Exception as error:

        print(
            "Icon extraction error:",
            error
        )

        return False