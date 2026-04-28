import os
import re

target_dir = "content/posts"

print("开始修复 title 中的非法字符...\n")

fixed_count = 0

for filename in os.listdir(target_dir):
    if not filename.endswith(".md"):
        continue
    
    filepath = os.path.join(target_dir, filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 front matter
    match = re.match(r'^(---\s*\n.*?---\s*\n)', content, re.DOTALL)
    if not match:
        continue
    
    frontmatter = match.group(1)
    body = content[match.end():]
    
    # 修复 title 行中的 @ 符号和其它问题
    new_frontmatter = re.sub(
        r'title:\s*["\'](.*?)["\']', 
        lambda m: 'title: "' + m.group(1).replace('@', '').replace('"', "'").strip() + '"',
        frontmatter
    )
    
    # 额外清理：如果 title 里还有冒号等可能引起问题的情况
    new_frontmatter = re.sub(r'title:\s*["\'](.*?)["\']', 
                             lambda m: 'title: "' + re.sub(r'[:@"]', '', m.group(1)).strip() + '"', 
                             new_frontmatter)
    
    if new_frontmatter != frontmatter:
        new_content = new_frontmatter + body
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ 已修复: {filename}")
        fixed_count += 1
    else:
        print(f"  无需修复: {filename}")

print("\n" + "="*50)
print(f"修复完成！共修复 {fixed_count} 个文件")
print("="*50)