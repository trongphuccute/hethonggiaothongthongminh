import os
import random
import shutil

# === Thư mục gốc project (nơi chứa script này) ===
script_dir = os.path.dirname(os.path.abspath(__file__))

# === Đường dẫn input (ảnh + nhãn gốc) ===
images_dir = os.path.join(script_dir, "Data_mẫu", "archive", "images")
labels_dir = os.path.join(script_dir, "Data_mẫu", "archive", "labels")

# === Đường dẫn output (datasets chuẩn YOLO) ===
output_dir = os.path.join(script_dir, "datasets")
train_img_dir = os.path.join(output_dir, "train", "images")
train_lbl_dir = os.path.join(output_dir, "train", "labels")
val_img_dir = os.path.join(output_dir, "val", "images")
val_lbl_dir = os.path.join(output_dir, "val", "labels")
test_img_dir = os.path.join(output_dir, "test", "images")
test_lbl_dir = os.path.join(output_dir, "test", "labels")

# === Tạo thư mục nếu chưa có ===
for d in [train_img_dir, train_lbl_dir, val_img_dir, val_lbl_dir, test_img_dir, test_lbl_dir]:
    os.makedirs(d, exist_ok=True)

# === Lấy danh sách ảnh ===
images = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
random.shuffle(images)

n_total = len(images)
n_train = int(0.8 * n_total)
n_val = int(0.1 * n_total)

train_files = images[:n_train]
val_files = images[n_train:n_train + n_val]
test_files = images[n_train + n_val:]

def copy_files(file_list, target_img_dir, target_lbl_dir):
    copied = 0
    for img_file in file_list:
        base = os.path.splitext(img_file)[0]
        img_path = os.path.join(images_dir, img_file)
        lbl_path = os.path.join(labels_dir, f"{base}.txt")
        if os.path.exists(lbl_path):
            shutil.copy(img_path, target_img_dir)
            shutil.copy(lbl_path, target_lbl_dir)
            copied += 1
        else:
            print(f"⚠️ Bỏ qua {img_file} (không có nhãn).")
    return copied

print("🔄 Đang chia dữ liệu...")
train_c = copy_files(train_files, train_img_dir, train_lbl_dir)
val_c = copy_files(val_files, val_img_dir, val_lbl_dir)
test_c = copy_files(test_files, test_img_dir, test_lbl_dir)
total = train_c + val_c + test_c

print("\n✅ Hoàn tất chia dữ liệu:")
print(f"   Tổng ảnh có nhãn: {total}/{n_total}")
print(f"   Train: {train_c} ảnh")
print(f"   Val:   {val_c} ảnh")
print(f"   Test:  {test_c} ảnh")
