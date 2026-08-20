---
name: Skill中文化与整合工具
description: 对本地已安装的 WorkBuddy skill 做批量整理：检索全部 skill、按功能分类、把英文命名与悬停说明(description)翻译成中文、把同主题 skill 整合为一个总控台、并在删除原文件前先做命名清晰的备份。当用户说"整理一下我的 skill""把 skill 翻译成中文""把英文 skill 中文化""把某类 skill 整合到一起""给 skill 做备份再重装"时使用。
---

# Skill 中文化与整合工具

把"检索 → 分类 → 中文化 → 整合 → 备份 → 重装"这套流程沉淀为可复用技能。
适用于用户有一批本地 skill（如从 GitHub / 市场安装的英文 skill），希望统一成中文命名与中文说明、并把同主题 skill 合并。

## 何时使用

- 用户要求：整理 skill / 把 skill 翻译成中文 / 英文 skill 中文化 / 把某类 skill 整合到一起 / 备份并重装 skill
- 前置：确认 skill 目录位置（默认用户级 `C:\Users\<用户>\.workbuddy\skills\`，项目级 `<workspace>\.workbuddy\skills\`）

## 工作流（严格按顺序）

### 1. 检索并列出全部 skill
用脚本枚举所有 `SKILL.md`，提取每个的文件夹名、`name` 字段、悬停 `description` 字段、以及语言（中文/英文/混合）。
参考脚本：`references/audit_skills.py`（输出每行 `FOLDER | name | lang`）。

### 2. 分类
按功能分组（浏览器自动化 / 动画动效 / 前端原型 / 图像生成 / 文档Office / 文本去痕 / OCR / 写作内容 / 文件工具 / 某主题家族…）。
向用户展示分类清单，再进入不可逆操作。

### 3. 整合同主题 skill（需先与用户确认方式）
常见方式，二选一（问用户）：
- **合并为单文件总控台（推荐）**：新建一个 hub skill，把各子技能原文存进 `references/`，主 `SKILL.md` 做路由表 + 各能力摘要。删除原分散 skill。
- **保留独立 + 统一入口**：各 skill 原样保留，仅新建一个路由入口。
整合前必须 `grep` 全目录，确认没有其他 skill 引用这些待删 skill 的文件夹名（仅内部互相引用则可安全删除）。

### 4. 中文化命名与说明（关键约束）
- **UI 列表通常显示文件夹名**，因此仅改 frontmatter 的 `name` 可能不够；要让 UI 显示中文，**用户级 skill 的文件夹名必须改成中文**。
- **用户级 skill（`~/.workbuddy/skills/`）**：
  - 把文件夹名重命名为中文（与 `name` 字段一致）。
  - 同步把 `name` 字段与悬停 `description` 翻译成中文。
  - 重命名前用脚本检查 skill 之间是否互相引用文件夹名；实测用户级 skill 基本没有这类引用，可安全重命名。
- **插件/内置 skill（`plugins/`、`resources/builtin-skills/`）**：
  - 不要改文件夹名，否则可能破坏插件管理/应用更新机制。
  - 仅翻译 frontmatter 的 `name` + `description`；若 UI 仍显示英文文件夹名，需接受这是插件系统的限制，或在得到用户明确授权后由用户手动在插件市场选择显示语言。
- 缺 `name`/`description`（无 frontmatter）的 skill：补一段中文 frontmatter。
- 参考脚本：`references/translate_template.py`（提供 mapping 字典模板，运行即原地改写并支持文件夹重命名）。

### 5. 备份（删除前必做）
完整复制整个 skills 目录到一个命名清晰的备份文件夹，并在其中写 `README.txt` 说明"这是原始 skill 文件的备份、生成时间、来源、处置建议"。
命名示例：`备份-原始skill文件-YYYYMMDD`（放在 workspace 下，避免被当成 skill 加载）。
验证备份完整（文件夹数量、关键文件存在）后再继续。

### 6. 重装与删除
- 中文化的 skill：原地改写即视为"新版本"（原始英文已在备份中）。
- 整合后的 hub：创建即"安装"；删除被整合掉的原始 skill 文件夹。
- **删除走沙箱安全机制**：直接 `rm -rf` 可能被 safe-delete 拦截并"fail-closed"。验证方法：用 Python `os.path.exists` 检查目标是否消失（safe-delete 实际会把文件送回收站，文件从原目录消失即可）。若部分删除失败，重试或改用 `mv` 把残留移出 skills 目录。

### 7. 校验
重跑 `audit_skills.py`：确认 `STILL-ENGLISH: NONE`，且整合后的 hub 存在、其 `references/` 完整。

## 8. 插件/内置 skill 大批量中文化流水线（数百个）

当要翻译的插件/内置 skill 数量很大（数百个）时，逐条处理不现实。采用"导出 → 分批翻译 → 批量改写 → 全量复检"的流水线。本技能附带的可复用脚本（位于某次执行的工作目录，逻辑可复制）：`export_raw.py`、`view_batch.py`、`apply_trans.py`、`reaudit.py`。

### 8.1 四个基准目录（必须全部扫描）
```
external_plugins : ~/.workbuddy/plugins/marketplaces/codebuddy-plugins-official/external_plugins
marketplace_plugins: ~/.workbuddy/plugins/marketplaces/codebuddy-plugins-official/plugins
builtin_plugin  : ~/.workbuddy/plugins/cache/workbuddy-builtin
app_builtin     : <WorkBuddy安装目录>/resources/app.asar.unpacked/resources/builtin-skills
```

### 8.2 流程
1. **导出**：`export_raw.py` 遍历四个目录，把所有 `name` 或 `description` 缺中文的 `SKILL.md` 导出为 `skill_en_raw.json`（rel-key 相对各 base）。
2. **分批查看**：`view_batch.py a b` 以紧凑形式打印区间内的 `rel / name / desc`，每批约 45 条。
3. **翻译**：每批写一个 `trans_batchNN.py`，定义 `TRANS = { rel或绝对路径: (cn_name, cn_desc) }`。
   - 仅译 name 时 `cn_desc=None`（保留原 description）；仅译 desc 时 `cn_name=None`。
   - 描述写成 `>-` 折叠块，续行缩进 2 空格。
4. **批量改写**：`apply_trans.py trans_batchNN.py` 只改 `name` 与 `description` 两个字段，其余 frontmatter 原样保留。
5. **全量复检**：`reaudit.py` 遍历四个目录全部 `SKILL.md`，统计仍缺中文的 `name`/`description` 与缺 frontmatter 的文件。

### 8.3 必须规避的坑（实测踩过）
- **跨 base 同名副本**：同一个 skill 可能同时存在于 `external_plugins` 与 `marketplace_plugins`（rel-key 相同）。`export_raw.py` 用 dict 按 rel-key 存储会**只保留最后一个 base 的副本**，导致 `apply_trans.py` 按 rel-key 解析时只改到其中一个副本，另一个副本仍是英文。→ **复检必须用绝对路径遍历所有 base**，把所有残留副本逐一修正。
- **缺 `name:` 字段**：部分 skill（如 `frontend-design-pro/*`、`oh-my-codebuddy/playwright`）frontmatter 里**根本没有 `name:` 行**，只有 `description:`。此时"替换 name"无处可替。→ 必须在开 `---` 之后**插入** `name: 中文` 行（插在闭合 `---` 之后会被 YAML 忽略）。
- **frontmatter 键拼错**：如 `gget` 把 `description` 错拼成 `descriptipn:`，解析器匹配不到 → 描述永远不被改写。→ 先修正拼写再写入中文描述。
- **描述已中文但 name 英文**：（如大量 `magicai-hub`、`obsidian-skills`、`cloudbase` 引用）只需译 name，`cn_desc=None` 避免覆盖已有中文。
- **完全无 frontmatter**：如 `lucide-icons/SKILL.md` 直接以 `# 标题` 开头。→ 补一段含中文 `name`/`description` 的 frontmatter 块。
- **app_builtin 的 skill-creator** 等通用 skill 在多个 base 都有副本，确保每个副本都译到。

### 8.4 完成判据
`reaudit.py` 输出 `name 仍无中文: 0` 且 `description 仍无中文: 0` 且 `缺 frontmatter: 0`，即全量中文化完成。用户级 skill 同理纳入 `reaudit.py` 的扫描范围一并校验。

## 强约束 / 注意事项

- 备份未通过校验前，**绝不**删除原始 skill。
- 删除只针对用户明确要整理的范围；内置 skill（在 WorkBuddy 安装目录 `resources/.../builtin-skills/` 下）不要动。
- 中文 `description` 用双引号包裹成单行 YAML 字符串，避免折叠块(`>-`)带来的多行解析问题。
- 整合时保留子技能原文到 `references/`，保证单入口仍能拿到完整细节。
