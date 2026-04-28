import os
import shutil
from datetime import datetime

# ================== 配置区域 ==================
source_dir = r"D:\posts"                    # 你的源文件夹
target_dir = "content/posts"                # Hugo 目标目录
draft = False                               # 是否默认作为草稿
# =============================================

# 创建目标目录（如果不存在）
os.makedirs(target_dir, exist_ok=True)

print("开始从 D:\\posts 批量导入 Markdown 文件...\n")

count = 0
skipped = 0

for filename in os.listdir(source_dir):
    if not filename.endswith(".md"):
        continue
    
    source_path = os.path.join(source_dir, filename)
    target_path = os.path.join(target_dir, filename)
    
    # 如果目标文件已存在，跳过（防止覆盖）
    if os.path.exists(target_path):
        print(f"已跳过（文件已存在）: {filename}")
        skipped += 1
        continue
    
    # 读取文件内容
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # 如果已经有 front matter，跳过
    if content.startswith('---'):
        print(f"已跳过（已有 front matter）: {filename}")
        skipped += 1
        continue
    
    # 从文件名提取日期和标题
    name_no_ext = os.path.splitext(filename)[0]
    parts = name_no_ext.split('-', 3)
    
    if len(parts) >= 3 and len(parts[0]) == 4 and len(parts[1]) == 2:
        date_str = f"{parts[0]}-{parts[1]}-{parts[2]}"
        title = parts[3] if len(parts) > 3 else "-".join(parts[2:])
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")
        title = name_no_ext
    
    # 清理标题
    title = title.replace('-', ' ').replace('_', ' ').strip()
    
    # 生成 front matter
    frontmatter = f"""---
title: "{title}"
date: {date_str}T12:00:00+08:00
draft: {str(draft).lower()}
description: ""
tags: []
categories: []
ShowToc: true
---

"""

    # 写入新文件
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)
    
    print(f"✓ 成功导入: {filename}  →  {title}")
    count += 1

print("\n" + "="*50)
print(f"批量导入完成！")
print(f"成功导入: {count} 个文件")
print(f"已跳过: {skipped} 个文件")
print(f"目标目录: {target_dir}")
print("="*50)