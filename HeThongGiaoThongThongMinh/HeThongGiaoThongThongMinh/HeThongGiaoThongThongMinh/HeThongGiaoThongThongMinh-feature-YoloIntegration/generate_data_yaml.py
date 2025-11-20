import yaml
import os

# === Đường dẫn tới thư mục gốc project (nơi chứa datasets/) ===
project_root = os.path.dirname(os.path.abspath(__file__))
datasets_dir = os.path.join(project_root, "datasets")

# === Đường dẫn tới file class song ngữ ===
base_dir = os.path.join(project_root, "Data_mẫu", "archive")
en_file = os.path.join(base_dir, "classes_en.txt")
vie_file = os.path.join(base_dir, "classes_vie.txt")
code_file = os.path.join(base_dir, "classes.txt")  # nếu cần dùng mã số class

# === Kiểm tra sự tồn tại của file class ===
for path in [en_file, vie_file]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Không tìm thấy file: {path}")

# === Đọc file lớp ===
with open(en_file, "r", encoding="utf-8") as f_en, \
     open(vie_file, "r", encoding="utf-8") as f_vie:
    en_names = [line.strip() for line in f_en if line.strip()]
    vie_names = [line.strip() for line in f_vie if line.strip()]

# === Kiểm tra độ dài 2 file khớp nhau ===
if len(en_names) != len(vie_names):
    raise ValueError(
        f"Số dòng không khớp: classes_en.txt ({len(en_names)}) vs classes_vie.txt ({len(vie_names)})"
    )

# === Kết hợp song ngữ ===
names = [f"{en} - {vie}" for en, vie in zip(en_names, vie_names)]

# === Tạo cấu trúc YAML với đường dẫn tương đối ===
data = {
    "train": os.path.join("datasets", "train", "images"),
    "val": os.path.join("datasets", "val", "images"),
    "test": os.path.join("datasets", "test", "images"),
    "nc": len(names),
    "names": names
}

# === Ghi ra file data.yaml tại project root ===
yaml_path = os.path.join(project_root, "data.yaml")
with open(yaml_path, "w", encoding="utf-8") as f:
    yaml.dump(data, f, allow_unicode=True, sort_keys=False)

print(f"✅ File data.yaml đã được tạo thành công với {len(names)} lớp (song ngữ Anh - Việt).")
print(f"📂 Lưu tại: {yaml_path}")
