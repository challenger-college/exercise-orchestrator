
def get_format_std(stream: bytes) -> str:
    """
    Format stderr or stdout stream into a string with trailing whitespace
    removed.

    Args:
        stream (bytes): Stdout or stderr stream.

    Returns:
        str: Format string with trailing whitespace.
    """
    return stream.decode("utf-8").rstrip()