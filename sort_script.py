import sys

from pathlib import Path
import shutil

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
FOLDER_NAME = {
    ('JPEG', 'PNG', 'JPG', 'SVG'): "images",
    ('AVI', 'MP4', 'MOV', 'MKV'): "video",
    ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'): "documents",
    ('MP3', 'OGG', 'WAV', 'AMR'): "audio",
    ('ZIP', 'GZ', 'TAR'): "archives"
}


def translate(name: str):
    TRANS = {}
    string = ""
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    for el in name:
        if el.isalnum() or el.isspace():
            unicode = ord(el)
            string += TRANS.get(unicode, el)
        else:
            string += "_"
    return string


def get_folder_name_extensions(extensions):
    for el in FOLDER_NAME:
        if extensions.lower() in map(str.lower, el):
            return FOLDER_NAME.get(el)


def delete_empty_folder(path: Path):
    try:
        if path.is_dir() and len(list(path.iterdir())) == 0:
            path.rmdir()
            print(f"папка видалена {path}")
    except:
        print(f"папка не пуста  {path}")


def proceed_file(path_file: Path, create_folders: list[Path]):
    file_extension = path_file.suffix[1:]
    file_name = path_file.stem
    normalize_name = translate(file_name)
    target_folder_name = get_folder_name_extensions(file_extension)
    target_folder_path = next((path for path in create_folders if path.stem == target_folder_name), None)
    if target_folder_path:
        if target_folder_path.stem == "archives":
            target_folder_path_normalize_name = target_folder_path.joinpath(normalize_name)
            shutil.unpack_archive(path_file, target_folder_path_normalize_name)
            path_file.unlink()
        else:
            normalize_name_file_extension = f"{normalize_name}.{file_extension}"
            target_folder_path_normalize_name_file_extension = target_folder_path.joinpath(
                normalize_name_file_extension)
            shutil.move(path_file, target_folder_path_normalize_name_file_extension)
        return path_file.parent


def proceed_folder(path, create_folders):
    if path in create_folders:
        return

    for el in path.iterdir():
        if el.is_dir():
            proceed_folder(el, create_folders)
        else:
            result_path = proceed_file(el, create_folders)
            delete_empty_folder(result_path)
    else:
        delete_empty_folder(path)


def main(rood_folder: Path):
    create_folders = list(
        rood_folder.joinpath(folder) for folder in FOLDER_NAME.values())
    for el in create_folders:
        el.mkdir(exist_ok=True)

    proceed_folder(rood_folder, create_folders)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("не корректна кількість аргументів")
    else:
        folder_name = Path(sys.argv[1])
        if not folder_name.is_dir():
            print("папка не існує")
        else:
            main(folder_name)

