import os
import re
from datetime import datetime

source_dir = r"D:\posts"
target_dir = "content/posts"

os.makedirs(target_dir, exist_ok=True)

print("开始优化已存在 front matter 的 Markdown 文件...\n")

count = 0
updated = 0

for filename in os.listdir(source_dir):
    if not filename.endswith(".md"):
        continue
    
    source_path = os.path.join(source_dir, filename)
    target_path = os.path.join(target_dir, filename)
    
    # 读取文件内容
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分离 front matter 和正文
    if not content.strip().startswith('---'):
        print(f"跳过（无 front matter）: {filename}")
        continue
    
    # 提取 front matter
    match = re.match(r'^(---\s*\n.*?---\s*\n)', content, re.DOTALL)
    if not match:
        print(f"无法解析 front matter: {filename}")
        continue
    
    frontmatter = match.group(1)
    body = content[match.end():].strip()
    
    # 检查并补充字段
    new_fm = frontmatter
    
    # 补充 description（如果没有）
    if 'description:' not in new_fm:
        new_fm = new_fm.replace('---', '---\ndescription: ""', 1)
    
    # 补充 tags（如果没有）
    if 'tags:' not in new_fm:
        new_fm = new_fm.replace('---', '---\ntags: []', 1)
    
    # 补充 categories（如果没有）
    if 'categories:' not in new_fm:
        new_fm = new_fm.replace('---', '---\ncategories: []', 1)
    
    # 补充 ShowToc（如果没有）
    if 'ShowToc:' not in new_fm:
        new_fm = new_fm.rstrip() + '\nShowToc: true\n'
    
    # 确保 draft 为 false
    if 'draft: true' in new_fm:
        new_fm = new_fm.replace('draft: true', 'draft: false')
    
    # 写回文件
    new_content = new_fm.strip() + '\n\n' + body + '\n'
    
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ 已优化: {filename}")
    updated += 1
    count += 1

print("\n" + "="*60)
print(f"优化完成！共处理 {count} 个文件")
print(f"实际更新 {updated} 个文件")
print(f"文件已保存到: {target_dir}")
print("="*60)