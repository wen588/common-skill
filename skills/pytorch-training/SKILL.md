---
name: pytorch-training
description: "PyTorch 训练全栈——训练循环、DataLoader 优化、混合精度、DDP 分布式。适用于任何 PyTorch 训练任务，从单卡调试到多卡分布式。"
metadata:
  category: tooling
  trigger-keywords: "training,pytorch,torch,deep learning,neural network,model,DataLoader,精度,分布式,DDP,混合精度"
  applicable-stages: "10,12"
  priority: "3"
  version: "2.0"
  references: "PyTorch Performance Tuning Guide, pytorch.org"
---

## PyTorch Training Best Practice

### 训练循环
```python
import torch
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)
torch.backends.cudnn.deterministic = True

model.train()
for epoch in range(num_epochs):
    for batch in train_loader:
        optimizer.zero_grad(set_to_none=True)
        loss = criterion(model(batch['input']), batch['target'])
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
    scheduler.step()
```

### DataLoader 优化
```python
DataLoader(
    dataset,
    num_workers=min(8, os.cpu_count()),  # 多进程加载
    pin_memory=True,                      # GPU 加速传输
    persistent_workers=True,              # 避免重复 spawn
)
```

### 混合精度 (AMP)
```python
scaler = torch.cuda.amp.GradScaler()
for batch in dataloader:
    optimizer.zero_grad()
    with torch.cuda.amp.autocast():
        output = model(batch)
        loss = criterion(output, target)
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
# BF16 优先于 FP16（Ampere+ 架构）
```

### 分布式 DDP
```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

dist.init_process_group(backend='nccl')
model = DDP(model)
sampler = DistributedSampler(dataset)
DataLoader(..., sampler=sampler)
# 只在 rank 0 保存 checkpoint
```
