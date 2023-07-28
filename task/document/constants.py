from pypandoc import get_pandoc_formats


_from_formats, _to_formats = get_pandoc_formats()

INPUT_FORMATS = [(str(i), f) for i, f in enumerate(_from_formats)]
OUTPUT_FORMATS = [(str(i), f) for i, f in enumerate(_to_formats)]
