---
name: code-collaboration
description: "研究代码协作规范——Git工作流、实验代码目录结构、可复现性检查清单、README模板、环境管理。解决研究生最常见的代码问题：'这个结果我当时是怎么跑出来的？'适用于：论文代码开源、团队共享代码仓库、实验代码结构设计、投稿后生成复现说明、多人合作开发。当用户说'搭项目结构'、'整理代码'、'写README'、'怎么让别人复现'、'代码怎么管理'、'怎么用git管理实验'、'环境配置写哪'、'实验代码一团糟'、'项目目录怎么组织'时触发。触发词：代码规范、Git工作流、可复现、实验代码、代码管理、复现说明、环境配置、项目结构、目录组织、README、git提交、环境配置、开源代码"
---

# Code Collaboration

研究代码协作规范。学术代码和工业代码的核心区别：工业代码追求稳定运行，学术代码追求**可复现实验**。

## 实验代码目录结构

每个研究项目推荐使用统一的结构：

```
project-name/
├── README.md                  # 项目说明（必写！）
├── environment.yml            # Conda 环境配置
├── requirements.txt           # pip 依赖
├── .gitignore                 # 忽略 .data/ __pycache__/ .vscode/
│
├── data/                      # 数据（不提交到 Git！）
│   ├── raw/                   # 原始数据，只读
│   ├── processed/             # 预处理后数据
│   └── splits/                # 数据划分文件（固定随机种子）
│
├── src/                       # 核心代码
│   ├── models/                # 模型定义
│   ├── datasets/              # 数据集类
│   ├── trainers/              # 训练循环
│   ├── utils/                 # 工具函数
│   └── configs/               # 配置文件
│       ├── baseline.yaml      # 基线配置
│       └── proposed.yaml      # 提出方法配置
│
├── scripts/                   # 实验脚本
│   ├── run_baseline.sh/.bat
│   ├── run_ablation.sh/.bat
│   └── run_all.sh/.bat
│
├── experiments/               # 实验输出（不提交到 Git）
│   ├── exp_001_baseline/
│   ├── exp_002_proposed/
│   └── exp_003_ablation_lr/
│
├── notebooks/                 # 分析/可视化 notebook
│   ├── 01_eda.ipynb           # 探索性分析
│   ├── 02_results.ipynb       # 结果分析 + 图表
│   └── 03_stats.ipynb         # 统计分析
│
└── docs/                      # 文档（可选）
    └── dataset_prep.md
```

## Git 工作流

### 核心原则

```
main      ← 稳定版，只合并不改。每次提交对应一个可复现的实验结果。
  │
  └── dev    ← 日常开发分支
        │
        ├── feature/xxx       ← 新功能/新方法
        ├── fix/xxx           ← Bug 修复
        └── experiment/xxx    ← 短期探索性实验（用完即弃）
```

### 提交规范

```
格式：[类型] 简短描述（50 字以内）

类型：
  feat    新功能/模型
  fix     Bug 修复
  exp     实验记录
  config  参数/配置修改
  docs    文档
  refac   重构
  data    数据处理

示例：
  exp[exp_004] 加入3种注意力变体对比
  feat 实现多头注意力模块
  fix DataLoader 读取缓存文件路径错误
  config 更新 proposed.yaml 学习率从 1e-3 到 1e-4
```

### 实验提交规范

每次跑完一个重要实验，提交一条记录：

```bash
git add src/ configs/ scripts/
git commit -m "exp[exp_012] SmartKnee 消融实验

- 去除 LSTM 层后 RMSE 从 2.445 升至 3.12
- 去除个性化归一化后 RMSE 升至 4.87
- 结论：两者缺一不可
"
```

这样每条提交本身就是实验日志。

## 可复现性检查清单

论文接收后 Reviewer 要求复现代码时逐项检查：

### 环境
- [ ] `environment.yml` 或 `requirements.txt` 包含所有依赖
- [ ] 注明 Python/PyTorch/CUDA 版本
- [ ] 注明操作系统（RTX 3090 上的结果和 MacBook 上可能不同）
- [ ] 如有 GPU，注明 CUDA 版本 + cuDNN 版本

### 数据
- [ ] 公开数据集：写明下载链接 + 具体版本
- [ ] 自采数据：提供数据获取途径 + 预处理脚本
- [ ] 数据划分：固定随机种子，提供划分文件

### 代码
- [ ] README.md 写清楚运行步骤（从环境搭建到出结果的完整命令）
- [ ] 所有随机种子固定（PyTorch + NumPy + Python random）
- [ ] `torch.backends.cudnn.deterministic = True`
- [ ] 提供预训练模型 / 训练日志（可选但推荐）
- [ ] 关键中间结果有断点保存

### 结果
- [ ] 提供训练日志 + TensorBoard 输出
- [ ] 提供模型预测的示例输出
- [ ] 主要实验结果可一键复现（`bash scripts/run_all.sh`）

## README.md 模板

每次投论文前生成 README：

```markdown
# [论文标题缩写] — 官方复现

## 环境
- Python 3.10 + PyTorch 2.0 + CUDA 11.8
- `conda env create -f environment.yml`

## 数据
- [数据集名称]：[下载链接]
- 下载后放入 `data/raw/` 目录

## 运行
```bash
# 训练完整模型
python src/train.py --config configs/proposed.yaml

# 运行基线
python src/train.py --config configs/baseline.yaml

# 全部实验一键复现
bash scripts/run_all.sh
```

## 结果
| 方法 | Accuracy | F1 | 运行命令 |
|------|----------|-----|---------|
| Baseline | 85.3 | 84.1 | `run_all.sh 中的命令` |
| Proposed | **89.7** | **88.5** | `run_all.sh 中的命令` |

## 引用
```bibtex
@article{xxx2024...
```
```

## 使用场景速查

| 用户输入 | 做什么 |
|---------|--------|
| "帮我搭项目结构" | 按模板生成项目目录树 |
| "写 README" | 按模板生成 README.md |
| "整理代码准备开源" | 配合 `code-release-assistant` 使用 |
| "这个实验怎么记录到 Git" | 按实验提交规范给出建议 |
| "这个结果怎么让别人复现" | 输出可复现性检查清单 |
| "帮我写 .gitignore" | 生成适合研究项目的 .gitignore |
