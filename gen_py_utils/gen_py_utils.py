import os
import glob
import hashlib

import psutil


def check_file_exists(file_path: str) -> bool:
    if os.path.exists(file_path):
        return True
    else:
        raise FileNotFoundError(f'Settings file "{file_path}" not found.')


def get_process_name(exe_path: str) -> str:
    filename = os.path.basename(exe_path)
    return filename


def is_process_running(process_name: str) -> bool:
    for proc in psutil.process_iter():
        try:
            if process_name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def kill_process(process_name: str):
    if is_process_running(process_name):
        os.system(f'taskkill /f /im {process_name}')


def get_processes_by_substring(substring: str) -> list:
    all_processes = psutil.process_iter(['pid', 'name'])
    matching_processes = [proc.info for proc in all_processes if substring.lower() in proc.info['name'].lower()]
    return matching_processes


def get_file_hash(file_path: str) -> str:
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            md5.update(chunk)
    return md5.hexdigest()


def get_do_files_have_same_hash(file_path_one: str, file_path_two: str) -> bool:
    if os.path.exists(file_path_one) and os.path.exists(file_path_two):
        hash_one = get_file_hash(file_path_one)
        hash_two = get_file_hash(file_path_two)
        return hash_one == hash_two
    else:
        return False


def get_files_in_tree(tree_path: str) -> list:
    return glob.glob(tree_path + '/**/*', recursive=True)


def get_file_extension(file_path: str) -> str:
    _, file_extension = os.path.splitext(file_path)
    return file_extension


# returns .extension not extension
def get_file_extensions(file_path: str) -> list:
    extensions = []
    files = get_files_in_tree(file_path)
    for file in files:
        extensions.append(get_file_extension(file))
    return extensions


# returns extension, not .extension
def get_file_extensions_two(directory_with_base_name: str) -> list:
    directory, base_name = os.path.split(directory_with_base_name)
    extensions = set()
    for _, files in os.walk(directory):
        for file in files:
            if file.startswith(base_name):
                _, ext = os.path.splitext(file)
                if ext:
                    extensions.add(ext)
    return list(extensions)


def get_matching_suffix(path_one: str, path_two: str) -> str:
    common_suffix = []

    for char_one, char_two in zip(path_one[::-1], path_two[::-1]):
        if char_one == char_two:
            common_suffix.append(char_one)
        else:
            break

    return ''.join(common_suffix)[::-1]
