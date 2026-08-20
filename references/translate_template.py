# 批量把 skill 的 name + description 翻译成中文，并可选择重命名文件夹
# 用法：
#   1) 在 SKILLS 下填入 skills 目录
#   2) 在 mapping 中填 { 原文件夹名: (新文件夹名, 新name, 新description) }
#      若不想改文件夹名，让 新文件夹名 == 原文件夹名 即可。
#   3) 运行：python translate_template.py
import os, shutil

SKILLS = r"C:\Users\Administrator\.workbuddy\skills"  # 按需修改

# 示例：把要翻译的 skill 写进来。
mapping = {
    # "agent-browser-core": (
    #     "浏览器自动化核心",   # 新文件夹名
    #     "浏览器自动化核心",   # 新 name
    #     "面向 agent-browser 命令行工具的核心能力，提供 AI 友好的网页自动化：快照、引用与结构化命令。",  # 新 description
    # ),
}

def update_frontmatter(text, new_name, new_desc):
    if not text.startswith('---'):
        return None
    end = text.find('\n---', 3)
    if end == -1:
        return None
    fm = text[3:end]
    body = text[end+4:]
    lines = fm.split('\n')
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('name:'):
            out.append(f'name: {new_name}'); i += 1; continue
        if line.startswith('description:'):
            j = i + 1
            while j < len(lines) and (lines[j].startswith(' ') or lines[j].startswith('\t') or lines[j].strip()==''):
                j += 1
            i = j; continue
        out.append(line); i += 1
    new_fm = []
    inserted = False
    for ln in out:
        new_fm.append(ln)
        if ln.startswith('name:') and not inserted:
            new_fm.append(f'description: "{new_desc}"')
            inserted = True
    if not inserted:
        new_fm.insert(0, f'description: "{new_desc}"')
    return '---\n' + '\n'.join(new_fm) + '\n---' + body

count = 0
for folder, item in mapping.items():
    if len(item) == 3:
        new_folder, nm, ds = item
    else:
        new_folder, nm, ds = folder, item[0], item[1]
    fp = os.path.join(SKILLS, folder, 'SKILL.md')
    if not os.path.exists(fp):
        print('MISSING', folder); continue
    text = open(fp, encoding='utf-8').read()
    res = update_frontmatter(text, nm, ds)
    if res is None:
        print('NO FM', folder); continue
    open(fp, 'w', encoding='utf-8').write(res)
    # rename folder if needed
    if new_folder != folder:
        src = os.path.join(SKILLS, folder)
        dst = os.path.join(SKILLS, new_folder)
        if os.path.exists(dst):
            print('COLLISION', dst); continue
        shutil.move(src, dst)
        print('RENAMED', folder, '->', new_folder)
    count += 1
    print(f'UPDATED {folder}: name={nm}')
print('TOTAL UPDATED:', count)
