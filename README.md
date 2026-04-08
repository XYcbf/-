# 批量图片编号助手

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-2ea44f?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="MIT">
</p>

一个轻量、开箱即用的 Python 工具，专为**批量整理图片命名**而设计。  
它会根据文件夹名称和递增序号自动生成统一文件名，让素材管理更整洁、更可追踪。

---

## 🌟 项目亮点

- 多格式支持：`jpg` / `jpeg` / `png` / `gif` / `bmp`
- 统一命名：`action_{文件夹名}_{序号}.{后缀}`
- 灵活参数：可设置补零位数、起始编号、是否递归
- 顺序稳定：按文件名排序后执行重命名
- 冲突保护：遇到重名自动跳过并寻找下一个可用序号
- 新手友好：支持交互式输入，直接回车即可用默认参数

---

## 🧩 适用场景

- 摄影项目素材归档
- 电商商品图统一命名
- 社媒运营图片批处理
- 设计/开发资源目录规范化

---

## 🧠 命名规则示例

假设目标文件夹名是 `photos`，重命名结果将类似：

- `action_photos_001.jpg`
- `action_photos_002.png`
- `action_photos_003.jpeg`

---

## 🚀 快速开始

### 1) 环境要求

- Python 3.8 或更高版本

### 2) 运行方式

#### 方式 A：交互式运行（推荐）

```bash
python rename_images.py
```

脚本会提示输入图片目录路径，直接回车可使用当前目录。

#### 方式 B：命令行参数运行

```bash
python rename_images.py <文件夹路径> <补零位数> <起始序号> <是否递归>
```

参数说明：

- `<文件夹路径>`：目标图片目录
- `<补零位数>`：例如 `3` 会生成 `001`
- `<起始序号>`：例如 `1`、`100`
- `<是否递归>`：`0` 表示否，`1` 表示是

示例：

```bash
python rename_images.py ./images 4 100 1
```

含义：递归处理 `./images` 及子目录，编号从 `0100` 开始。

---

## 📦 项目结构

```text
cmm/
├─ rename_images.py
└─ README.md
```

---

## ⚠️ 使用建议

- 建议先备份原始图片，再执行批量操作
- 建议先在少量样本目录试跑参数
- Windows 下可直接粘贴带引号路径，脚本会自动处理

---

## 🛣️ 后续可扩展方向

- 增加“预览模式”（只显示将要改名，不立即执行）
- 支持自定义命名前缀模板
- 输出重命名日志（CSV / TXT）

---

## 📜 License

MIT
