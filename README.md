# 文字冒险游戏 - Text Adventure Game

基于 Pygame 的黑白文本框风格文字冒险游戏。

## How to Run

### Docker 启动

```bash
# 构建并启动容器
docker-compose up --build -d

# 查看日志
docker-compose logs -f game

# 停止容器
docker-compose down
```

启动后，打开浏览器访问：http://localhost:6080

游戏会自动连接并全屏显示。

### 本地启动

```bash
# 进入前端目录
cd frontend

# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行游戏
python main.py
```

## Services

| 服务名 | 描述 | 端口 |
|--------|------|------|
| game | 文字冒险游戏主程序 (noVNC) | 6080 |

## 测试账号

本游戏为单机游戏，无需账号登录。游戏开始时输入任意名字即可开始冒险。

示例名字：
- 勇者
- 冒险家
- 旅人

## 题目内容

用pygame的形式，并以其中的文本模板为基础，创立一个拥有独立游戏窗口的文字冒险游戏，同时游戏界面简洁，以黑白文本框为基础风格，除了名字输入外，行动选择以点击选项框为模式

### 项目概述

这是一个基于 Pygame 开发的文字冒险游戏，具有以下特点：

- **独立游戏窗口**：使用 Pygame 创建 800x600 的游戏窗口
- **黑白简洁风格**：以黑色背景、白色文字和边框为主要视觉风格
- **文本框交互**：故事内容通过文本框展示
- **点击选项模式**：玩家通过点击选项框进行选择，而非键盘输入
- **名字输入**：游戏开始时支持键盘输入玩家名字

### 游戏玩法

1. 启动游戏后，输入你的名字并按 Enter 键开始
2. 阅读故事文本，了解当前场景
3. 点击下方的选项框做出选择
4. 根据不同选择，故事将走向不同的分支
5. 最终达成不同的结局

### 结局类型

- **完美结局**：光明守护者 - 获得光明之石，拯救森林和村庄
- **胜利结局**：村庄救星 - 击败影子兽，获得宝石
- **良好结局**：无名英雄 - 帮助村民但未获得宝物
- **普通结局**：过客 - 离开这片土地继续旅程
- **失败结局**：迷失者 - 被黑暗吞噬

### 技术栈

- **语言**：Python 3.11
- **游戏框架**：Pygame 2.5.2
- **容器化**：Docker + Docker Compose
- **架构支持**：ARM64 / AMD64 (x86_64)

### 项目结构

```
.
├── docker-compose.yml      # Docker Compose 配置
├── .gitignore              # Git 忽略文件
├── README.md               # 项目说明文档
└── frontend/
    ├── Dockerfile          # Docker 构建文件
    ├── requirements.txt    # Python 依赖
    ├── main.py             # 游戏入口
    └── game/
        ├── __init__.py     # 模块初始化
        ├── config.py       # 游戏配置
        ├── engine.py       # 游戏引擎
        ├── story.py        # 剧情数据
        └── ui.py           # UI 组件
```

### 中文支持

游戏自动检测并加载系统中文字体，支持以下字体：
- Linux: 文泉驿正黑、文泉驿微米黑、Noto Sans CJK
- macOS: 苹方、华文黑体
- Windows: 微软雅黑、黑体

如果系统没有中文字体，将使用默认字体（可能无法正确显示中文）。
