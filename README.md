# Common Skills

通用非科研技能集合，用于 [OpenCode](https://opencode.ai) 等 AI 编程助手。

## 技能列表

### 文档/办公
| Skill | 说明 |
|---|---|
| `docx` | Word 文档创建、读取、编辑（含修订、批注、模板） |
| `xlsx` | Excel 电子表格处理（公式、图表、格式、数据清洗） |
| `ppt` | PPT 演示文稿全流程（主题生成 → 内容填充 → PPTX 输出） |
| `pdf-processing-pro` | PDF 处理（表单、表格、OCR、验证、批量操作） |

### 代码/工程
| Skill | 说明 |
|---|---|
| `code-collaboration` | Git 工作流、实验代码规范、可复现检查清单 |
| `code-release-assistant` | 代码开源准备（README、Dockerfile、许可证） |
| `code-explainer` | 用生活比喻解释代码 |
| `karpathy-guidelines` | Karpathy 编码准则（减少 LLM 编码错误） |
| `doc-coauthoring` | 结构化文档协作写作 |

### 机器学习/深度学习
| Skill | 说明 |
|---|---|
| `cv-classification` | 图像分类（CIFAR/ImageNet/ResNet/ViT） |
| `cv-detection` | 目标检测（YOLO/DETR/Faster R-CNN） |
| `data-loading` | DataLoader 优化（防止 GPU 空闲） |
| `distributed-training` | PyTorch DDP 多 GPU 分布式训练 |
| `mixed-precision` | FP16/BF16 混合精度训练 |
| `nlp-alignment` | RLHF、DPO、指令微调 |
| `nlp-pretraining` | 语言模型预训练与微调 |
| `pytorch-training` | PyTorch 训练循环最佳实践 |
| `rl-policy-optimization` | 强化学习策略优化（PPO/SAC） |

### 通用工具
| Skill | 说明 |
|---|---|
| `ai-image-generation` | AI 图像生成（GPT-Image-2 / FLUX / Gemini / Grok / Stable Diffusion 等 50+ 模型） |
| `article-illustrator` | 文章内容配图生成 |
| `biology-biopython` | Biopython 生物信息学分析 |
| `chemistry-rdkit` | RDKit 计算化学分析 |
| `caveman` | 极简通信模式（减少 token 消耗） |
| `data-storytelling` | 数据叙事（可视化 + 语境 + 说服结构） |
| `multi-agent-meeting` | 多 AI 智能体协作会议与决策 |
| `obsidian-skills-integrated` | Obsidian 知识管理（Canvas / CLI / 网页提取） |
| `skill-creator` | 创建、修改、评测 AI Skill |

---

## 环境复现

### 前置要求

- [Miniforge](https://github.com/conda-forge/miniforge) 或 Miniconda
- Python 3.12+

### 步骤

```bash
# 1. 创建并激活 conda 环境
conda create -n opencode python=3.12 -y
conda activate opencode

# 2. 安装核心依赖
pip install "python-pptx>=1.0.2" "pillow>=9.0.0" "openpyxl>=3.1.0" "xlsxwriter>=3.2" "markitdown" "lxml>=6.1"

# 3. 文档处理
pip install "pdfplumber>=0.10" "pypdf>=6.0" "beautifulsoup4>=4.12"

# 4. 数据科学
pip install "numpy>=2.4" "scipy>=1.17" "pandas>=3.0" "matplotlib>=3.10" "seaborn>=0.13" "plotly>=6.7"

# 5. 机器学习
pip install "scikit-learn>=1.8" "statsmodels>=0.14" "scikit-posthocs>=0.13" "pingouin>=0.6"

# 6. 工具
pip install "requests>=2.31" "PyYAML>=6.0" "nltk>=3.8" "pytesseract>=0.3" "jupyter" "ipykernel"

# 7. 验证安装
python -c "import pptx, PIL, openpyxl, xlsxwriter, pandas, numpy, matplotlib, sklearn, pdfplumber, yaml; print('All dependencies OK')"
```

### 验证

执行以下命令确认各技能所需依赖可用：

```bash
# Office 文档
python -c "import pptx; print(f'python-pptx {pptx.__version__}')"
python -c "import docx; print('python-docx OK')"
python -c "import openpyxl; print(f'openpyxl {openpyxl.__version__}')"

# PDF
python -c "import pdfplumber; print(f'pdfplumber {pdfplumber.__version__}')"

# 图像
python -c "from PIL import Image; print(f'Pillow OK')"

# 数据科学
python -c "import numpy; print(f'numpy {numpy.__version__}')"
python -c "import pandas; print(f'pandas {pandas.__version__}')"
python -c "import matplotlib; print(f'matplotlib {matplotlib.__version__}')"
```

---

## 使用方式

1. 在 OpenCode 配置（`~/.config/opencode/opencode.jsonc`）中添加 skills 路径：

```jsonc
{
  "skills": {
    "paths": ["path/to/common-skill/skills"]
  }
}
```

2. 在对话中触发对应 skill（如"帮我生成一个 PPT" → 自动加载 `ppt` skill）

---

## 说明

本仓库仅包含**非科研通用技能**。科研相关技能（论文写作、文献综述、模拟审稿、Nature 系列等）不在本仓库中。
