def convert_bytes(size):
    """Function that converts bytes into kilobytes and megabytes"""

    for x in ["bytes", "KB", "MB"]:
        if size < 1024.0:
            return "%3.0f %s" % (size, x)
        size /= 1024.0
    return size


def extract_extension(file_name):
    """Funtion that returns a file extension"""

    return str(file_name).split(".")[-1].upper()