import os
import shutil

source_folder = "/home/Bonzz/Downloads"

file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".mov"],
    "Music": [".mp3", ".wav"],
    "Archives": [".zip", ".rar", ".7z"],
}

def get_category(extension):
    for category, exts in file_types.items():
        print(category, exts)
        if extension.lower() in exts:
            return category
    return "Other"

def organize_file(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

        if os.path.isdir(file_path): continue

        _, ext = os.path.splitext(filename)
        category = get_category(ext)

        target_folder = os.path.join(folder, category)
        os.makedirs(target_folder, exist_ok=True)

        shutil.move(file_path, os.path.join(target_folder, filename))
        print(f"Moved: {filename} -> {category}/")


organize_file(source_folder)
print("Selesai merapikan folder")