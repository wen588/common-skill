---
name: ppt
description: 全能PPT助手——集成7角色内容创作、JSON→PPTX构建、编辑/审查/QA三大能力。覆盖从主题生成到最终.pptx文件输出的完整流水线，合并原ppt-generator、pptx-generator、pptx三个技能。同时整合 guizang-ppt-skill 的网页 PPT（单 HTML 文件，横向翻页，WebGL 背景）能力。
dependency:
  python:
    - python-pptx>=1.0.2
    - pillow>=9.0.0
    - openpyxl>=3.1.0
    - markitdown
---

# PPT 全能助手

整合原 `ppt-generator`（内容创作）、`pptx-generator`（文件构建）、`pptx`（通用操作）为一个统一入口。

## 模式选择

用户只需描述需求，系统自动匹配模式：

| 模式 | 触发场景 | 用户怎么说 |
|---|---|---|
| **full** | 从零生成完整 PPT 文件 | "做一份学术汇报PPT"、"生成产品发布会演示文稿" |
| **outline** | 只要大纲和布局建议 | "先给我一个大纲看看"、"帮我规划PPT结构" |
| **content** | 已有大纲，填充内容 | "按这个大纲写内容"、"帮我充实每页" |
| **build** | 已有内容/JSON，生成文件 | "把这份数据生成PPTX"、"转成PPT文件" |
| **edit** | 修改现有 PPTX 文件 | "帮我改一下这个PPT"、"替换第3页的内容" |
| **review** | 读取/分析/审查 PPTX | "看看这个PPT讲了什么"、"检查有没有问题" |
| **web** | 生成网页 PPT（单 HTML 横向翻页） | "做个网页PPT"、"杂志风HTML"、"瑞士风格网页演示" |

---

## 模式详解

### 1. full — 全流程生成

**流程**：主题分析 → 模板推荐 → 内容策划 → 文本创作 → 视觉设计 → 优化编辑 → PPTX构建 → QA

**角色调度**（7 角色流水线）：

| 角色 | 职责 | 输出 |
|---|---|---|
| 主题分析师 | 分析需求、明确受众、确定风格 | PPT 结构大纲 |
| 模板设计师 | 推荐布局类型和配色方案 | 每页布局建议 |
| 内容策划师 | 将大纲映射到页面布局 | 详细页面规划 |
| 文本创作者 | 撰写标题和内容要点 | 每页完整文案 |
| 视觉设计师 | AI 配图建议、图表推荐 | 配图/图表标注 |
| 优化编辑师 | 润色语言、优化结构 | 最终内容文本 |
| PPT 构建师 | 生成 JSON → 调用构建脚本 | `.pptx` 文件 |

**关键规范**（详见 `../ppt-generator/references/`）：
- 结构指南：[`../ppt-generator/references/ppt_structure_guide.md`](../ppt-generator/references/ppt_structure_guide.md)
- 视觉设计：[`../ppt-generator/references/visual_design_guide.md`](../ppt-generator/references/visual_design_guide.md)

**构建步骤**：
1. 整理内容为 JSON（格式参见[`../pptx-generator/references/json_format_spec.md`](../pptx-generator/references/json_format_spec.md)）
2. 验证 JSON：
   ```bash
   python ../pptx-generator/scripts/json_validator.py --input ./ppt_data.json
   ```
3. 生成 PPTX：
   ```bash
   python ../pptx-generator/scripts/pptx_builder.py --input ./ppt_data.json --output ./output.pptx
   ```
4. 验证 PPTX：
   ```bash
   python ../pptx-generator/scripts/pptx_validator.py --input ./output.pptx
   ```
5. 执行 QA（见下方 QA 规范）

---

### 2. outline — 仅大纲

执行角色 1（主题分析师）+ 角色 2（模板设计师），输出：
- PPT 章节结构（封面→目录→主体→结束）
- 每页推荐布局类型
- 风格/配色建议

不进行内容填充，不生成文件。

---

### 3. content — 内容填充

用户提供大纲或主题，从角色 2 开始执行到角色 6：
- 模板推荐 → 内容策划 → 文本创作 → 视觉设计 → 优化编辑

输出完整内容和配图建议，可选决定是否继续生成 PPTX。

---

### 4. build — 仅构建文件

跳过内容创作，仅执行构建层：

1. 验证 JSON（如果用户提供）：
   ```bash
   python ../pptx-generator/scripts/json_validator.py --input ./ppt_data.json
   ```
2. 生成 PPTX：
   ```bash
   python ../pptx-generator/scripts/pptx_builder.py --input ./ppt_data.json --style {style} --output ./output.pptx
   ```
3. 验证 + QA

支持：
- 自定义风格配置 `--style`
- 模板 PPTX 作为底板 `--template`
- 批量生成 `--input-dir`

---

### 5. edit — 编辑现有 PPTX

**读取内容**：
```bash
python -m markitdown presentation.pptx
```

**编辑流程**（详见 [`../pptx/editing.md`](../pptx/editing.md)）：
1. 用 `thumbnail.py` 生成缩略图分析结构
2. 用 `unpack.py` 解包 → 修改 XML → 清理 → 重新打包

**常用编辑操作**：
- 添加幻灯片：`python ../pptx/scripts/add_slide.py`
- 清理冗余：`python ../pptx/scripts/clean.py`

---

### 6. review — 读取/审查

**文本提取**：
```bash
python -m markitdown presentation.pptx
```

**视觉概览**：
```bash
python ../pptx/scripts/thumbnail.py presentation.pptx
```

---

## QA 规范（必执行）

每生成一个 PPTX 必须执行 QA，不是确认而是**找 bug**。

### 内容 QA
```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```
检查：缺内容、错别字、顺序错误、模板占位符残留。

### 视觉 QA
用 sub-agent 审查缩略图（如果用脚本生成了图片），关注：
- 元素重叠、文字溢出/截断
- 间距不均、边距不足（< 0.5"）
- 低对比度元素
- 布局重复、无视觉元素

---

## 设计原则（创作层必须遵守）

### 配色
- 选与主题匹配的颜色，不要默认蓝色
- 一色主导（60-70%），1-2 辅助色，一个强调色
- 可用调色板：Midnight Executive (`1E2761`/`CADCFC`)、Forest & Moss (`2C5F2D`/`97BC62`)、Coral Energy (`F96167`/`F9E795`) 等

### 排版
- 标题 36-44pt bold，正文 14-16pt，标注 10-12pt
- 标题用有个性的字体（Georgia/Arial Black/Cambria），正文用 Calibri/Arial

### 布局
- 每页必须有视觉元素（图/表/图标），纯文字页 = 失败
- 不要连续使用相同布局，交替使用双栏、卡片网格、大数字标注等
- 正文左对齐，仅标题居中

### 禁区
- **禁止标题下加装饰线**（AI 生成 PPT 的标志性特征）
- **禁止纯文字页**（标题+项目符号的白底页）
- **禁止低对比度**（浅色字配浅底或深色字配深底）

---

## 资源索引

### 内容创作层（原 ppt-generator）
| 资源 | 路径 |
|---|---|
| 生成脚本 | [`../ppt-generator/scripts/generate_pptx.py`](../ppt-generator/scripts/generate_pptx.py) |
| 结构指南 | [`../ppt-generator/references/ppt_structure_guide.md`](../ppt-generator/references/ppt_structure_guide.md) |
| 视觉指南 | [`../ppt-generator/references/visual_design_guide.md`](../ppt-generator/references/visual_design_guide.md) |

### 文件构建层（原 pptx-generator）
| 资源 | 路径 |
|---|---|
| JSON 验证 | [`../pptx-generator/scripts/json_validator.py`](../pptx-generator/scripts/json_validator.py) |
| PPTX 构建 | [`../pptx-generator/scripts/pptx_builder.py`](../pptx-generator/scripts/pptx_builder.py) |
| PPTX 验证 | [`../pptx-generator/scripts/pptx_validator.py`](../pptx-generator/scripts/pptx_validator.py) |
| JSON 格式 | [`../pptx-generator/references/json_format_spec.md`](../pptx-generator/references/json_format_spec.md) |
| 布局指南 | [`../pptx-generator/references/layout_guide.md`](../pptx-generator/references/layout_guide.md) |
| 协作指南 | [`../pptx-generator/references/collaboration_guide.md`](../pptx-generator/references/collaboration_guide.md) |

### 通用操作层（原 pptx）
| 资源 | 路径 |
|---|---|
| 编辑指南 | [`../pptx/editing.md`](../pptx/editing.md) |
| 从零创建 | [`../pptx/pptxgenjs.md`](../pptx/pptxgenjs.md) |
| 缩略图 | [`../pptx/scripts/thumbnail.py`](../pptx/scripts/thumbnail.py) |
| 添加幻灯片 | [`../pptx/scripts/add_slide.py`](../pptx/scripts/add_slide.py) |
| 清理工具 | [`../pptx/scripts/clean.py`](../pptx/scripts/clean.py) |

### 7. web — 网页 PPT（整合 guizang-ppt-skill）

生成**单文件 HTML**横向翻页网页 PPT，无需 Powerpoint 即可在浏览器打开。

#### 风格 A · 电子杂志风
- 衬线标题（Noto Serif SC + Playfair Display）
- WebGL 流体/等高线背景
- 适合：人文分享、行业观察、商业发布

#### 风格 B · 瑞士国际主义
- 全程无衬线（Inter + Helvetica + Noto Sans SC）
- WebGL 极细网格 + 点阵背景
- 极致字号对比、高反差功能色
- 适合：科技产品、数据汇报、设计领域

#### 使用方式
1. 确定风格 A 或 B 以及主题色
2. 拷贝 `guizang-ppt-skill/assets/template.html`（风格 A）或 `template-swiss.html`（风格 B）
3. 从 `guizang-ppt-skill/references/layouts.md` 或 `layouts-swiss.md` 挑选布局
4. 填充内容，图片放入 `images/` 目录
5. 打开 HTML 文件即可预览

#### 资源索引
| 资源 | 路径 |
|---|---|
| 模板（电子杂志风） | [`guizang-ppt-skill/assets/template.html`](../guizang-ppt-skill/assets/template.html) |
| 模板（瑞士风） | [`guizang-ppt-skill/assets/template-swiss.html`](../guizang-ppt-skill/assets/template-swiss.html) |
| 布局（电子杂志风） | [`guizang-ppt-skill/references/layouts.md`](../guizang-ppt-skill/references/layouts.md) |
| 布局（瑞士风） | [`guizang-ppt-skill/references/layouts-swiss.md`](../guizang-ppt-skill/references/layouts-swiss.md) |
| 主题色（电子杂志风） | [`guizang-ppt-skill/references/themes.md`](../guizang-ppt-skill/references/themes.md) |
| 主题色（瑞士风） | [`guizang-ppt-skill/references/themes-swiss.md`](../guizang-ppt-skill/references/themes-swiss.md) |
| 质量检查清单 | [`guizang-ppt-skill/references/checklist.md`](../guizang-ppt-skill/references/checklist.md) |

---

## 注意事项
- 内容创作由 LLM 完成，仅在最终生成 .pptx / .html 时调用脚本
- 三个源技能保留不动，本技能通过路径引用，不复制文件
- JSON 构建阶段支持图表类型：柱状图、折线图、饼图
- 支持图片格式：PNG、JPG、JPEG、GIF
- 生成的 .pptx 文件兼容 PowerPoint、WPS
- **网页 PPT**：如需杂志风或瑞士风 HTML 演示，系统自动路由到 `guizang-ppt-skill`
