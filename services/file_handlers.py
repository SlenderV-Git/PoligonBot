import os, sys

book: dict[int, str] = {}
PAGE_SIZE = 1050
BOOK_PATH = "database/book.txt"
book: dict[int, str] = {}


def _get_part_text(text, start, page_size):
    if len(text[start:]) <= page_size:
        return text[start:], len(text[start:])
    else:
        cursor = start + page_size-1
        filt = ",.!:;?"
        while text[cursor] not in filt or (text[cursor] in filt and text[cursor+1] in filt):
            cursor -= 1
        result = text[start : cursor+1]
        return result, len(result)
    


# Дополните эту функцию, согласно условию задачи
def prepare_book(path: str) -> None:
    with open(path, 'rt', encoding= "UTF-8") as file:
        text = file.read()
    start, coun, len_file = 0, 1, len(text)
    while len_file!=0:
        text_part, len_text = _get_part_text(text, start, PAGE_SIZE)
        book[coun] = text_part.strip()
        coun += 1
        start += len_text
        len_file -= len_text

prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))