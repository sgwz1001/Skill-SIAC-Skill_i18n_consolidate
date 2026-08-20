# 审计本地已安装 skill 的命名语言
# 用法：python audit_skills.py
# 遍历 skills 目录，输出每个顶层 skill 的 文件夹名 / name 字段 / 语言(EN/CN/MIXED/EMPTY)
import os, re

SKILLS = r"C:\Users\Administrator\.workbuddy\skills"  # 按需修改

def frontmatter(text):
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end != -1:
            return text[3:end]
    return ''

def lang(s):
    if not s.strip():
        return 'EMPTY'
    cjk = sum(1 for ch in s if '\u4e00' <= ch <= '\u9fff')
    letters = sum(1 for ch in s if ch.isascii() and ch.isalpha())
    if cjk == 0 and letters > 0:
        return 'EN'
    if cjk >= max(1, letters * 0.25):
        return 'CN'
    return 'MIXED'

def get_desc(fm):
    desc_lines = []
    capture = False
    for line in fm.split('\n'):
        if line.startswith('description:'):
            rest = line[len('description:'):].strip()
            if rest and not rest.startswith('>') and not rest.startswith('|'):
                desc_lines = [rest]
                capture = False
            else:
                capture = True
                continue
        elif capture:
            if re.match(r'^[A-Za-z_][\w-]*:', line):
                break
            if line.startswith(' ') or line.startswith('\t'):
                desc_lines.append(line.strip())
            elif line.strip() == '':
                desc_lines.append('')
            else:
                break
    return ' '.join(desc_lines)

top = []
for d in sorted(os.listdir(SKILLS)):
    fp = os.path.join(SKILLS, d, 'SKILL.md')
    if os.path.isfile(fp):
        top.append(d)

print('TOP-LEVEL SKILLS:', len(top))
en = []
for d in top:
    fm = frontmatter(open(os.path.join(SKILLS, d, 'SKILL.md'), encoding='utf-8').read())
    name_m = re.search(r'^name:\s*(.+)$', fm, re.M)
    name = name_m.group(1).strip() if name_m else '(none)'
    desc = get_desc(fm)
    lg = lang(desc)
    if lg == 'EN':
        en.append(d)
    print(f"FOLDER: {d} | name: {name} | lang: {lg}")
print('STILL-ENGLISH:', en if en else 'NONE')
