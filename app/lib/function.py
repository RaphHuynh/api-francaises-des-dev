from fastapi import UploadFile


def isInvalidImage(upload: UploadFile):
    signatures = (
        b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A",                # PNG
        b"\xFF\xD8\xFF\xE0",                                # JPEG/JPG
        b"\xFF\xD8\xFF\xE1",                                # JPEG/EXIF
        b"\xFF\xD8\xFF\xE8",                                # JPEG/SPIFF
        b"\xFF\xD8\xFF\xDB",                                # JPEG/JFIF
        b"\x00\x00\x00\x0C\x6A\x50\x20\x20\x0D\x0A\x87\x0A" # JPEG/2000
    )

    header = upload.file.read(12)
    upload.file.close()

    return not any(
        header.startswith(signature) for signature in signatures
    )

