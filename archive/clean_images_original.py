import os

# ================= 設定區 =================
images_dir = 'images'  
labels_dir = 'labels'  
# ==========================================

print("=== 🪓 孿生內鬼終結開始 ===")

# 1. 蒐集 labels 的純主檔名
valid_names = set()
for filename in os.listdir(labels_dir):
    if filename.lower().endswith('.txt') and filename != 'classes.txt':
        valid_names.add(os.path.splitext(filename)[0].lower())

# 2. 找出 images 裡面所有重複主檔名的檔案
name_dict = {}
for img_name in os.listdir(images_dir):
    if img_name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp')):
        base = os.path.splitext(img_name)[0].lower()
        if base in valid_names:
            if base not in name_dict:
                name_dict[base] = []
            name_dict[base].append(img_name)

# 3. 開始抓出重複者並清理
delete_count = 0
for base, files in name_dict.items():
    if len(files) > 1:
        print(f"發現重複群組 {base}: {files}")
        # 💡 關鍵決策：Label Studio 轉 YOLO 時，如果照片有不同格式，通常會優先順序。
        # 這裡我們採取最穩妥的策略：優先保留 .jpg 檔，如果沒有 .jpg 則保留第一個。
        # 如果你想手動保留 png，請看這裡。我們這邊幫你自動砍掉多餘的那個。
        # 為了安全，我們保留 .jpg，刪除 .png (依照普遍 Label Studio 匯出習慣)
        has_jpg = any(f.lower().endswith('.jpg') for f in files)
        
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if has_jpg and ext == '.png':  # 如果有 jpg，就把 png 刪掉
                os.remove(os.path.join(images_dir, f))
                print(f"  🔥 刪除重複的 PNG: {f}")
                delete_count += 1
            elif not has_jpg and ext != '.png': # 如果沒有 jpg，保留 png，刪除其他的
                os.remove(os.path.join(images_dir, f))
                print(f"  🔥 刪除重複的其他格式: {f}")
                delete_count += 1

print(f"\n🎉 恭喜！成功清除了 {delete_count} 個重複檔名的內鬼照片！")
print(f"現在 images 資料夾剩下 {len(os.listdir(images_dir))} 張照片。")