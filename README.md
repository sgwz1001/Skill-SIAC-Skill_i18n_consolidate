# Skill 中文化与整合工具（skill-i18n-consolidate）

> 一个 WorkBuddy / CodeBuddy Skill：对本地已安装的 skill 做批量整理——
> 检索全部 skill、按功能分类、把英文命名与悬停说明翻译成中文、把同主题 skill 整合为一个总控台、
> 并在删除原文件前先做命名清晰的备份。

## 这是什么

当你有一批本地 skill（比如从 GitHub / 市场安装的英文 skill），希望：

- 统一成**中文命名 + 中文说明**（鼠标悬停看到的 description 也变中文）；
- 把**同主题的多个 skill 合并**成一个「总控台」；
- 在动手删除之前，**先完整备份**原始文件；

这个技能把「检索 → 分类 → 中文化 → 整合 → 备份 → 重装」整套流程沉淀为可复用工作流。

## 工作流（严格按顺序）

1. **检索**：枚举所有 `SKILL.md`，提取文件夹名、`name`、悬停 `description`、语言（中/英/混合）。
2. **分类**：按功能分组（浏览器自动化 / 动画动效 / 前端原型 / 图像 / 文档 Office / 文本去痕 / OCR / 写作 / 文件工具……），先给你看分类清单。
3. **整合（可选）**：同主题可「合并为单文件总控台」或「保留独立 + 统一入口」，需先与你确认。
4. **中文化**：
   - 用户级 skill：文件夹名改成中文（与 `name` 一致）+ `name`/`description` 翻译成中文；
   - 插件 / 内置 skill：**不要改文件夹名**（会破坏插件机制），只翻译 frontmatter 的 `name` + `description`；
   - 缺 frontmatter 的 skill：补一段中文 frontmatter。
5. **备份**：完整复制整个 skills 目录到命名清晰的备份文件夹，写 `README.txt` 说明来源与处置建议。
6. **重装与删除**：中文化的原地改写即「新版本」；整合后的 hub 创建即「安装」；删除走沙箱安全机制。
7. **校验**：重跑检索脚本，确认「仍含英文：无」。

## 大批量流水线（数百个插件 / 内置 skill）

附带可复用脚本逻辑：`export_raw.py`（导出）→ `view_batch.py`（分批看）→ `trans_batchNN.py`（翻译）→
`apply_trans.py`（批量改写 name/description）→ `reaudit.py`（全量复检）。文末列出了实测踩过的坑
（跨 base 同名副本、缺 name 字段、frontmatter 键拼错、完全无 frontmatter 等）。

## 文件结构

```
skill-i18n-consolidate/
├── SKILL.md                            # 完整工作流 + 大批量流水线 + 坑位清单
└── references/
    ├── audit_skills.py                 # 枚举所有 SKILL.md 并标注语言
    └── translate_template.py           # 翻译 mapping 字典模板，运行即原地改写
```

## 强约束

- 备份未通过校验前，**绝不**删除原始 skill。
- 内置 skill（在 WorkBuddy 安装目录 `resources/.../builtin-skills/` 下）不要动。
