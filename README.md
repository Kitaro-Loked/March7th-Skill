# March7th-Skill 🌸 v3.1

![三月七三形态](march7th_banner.png)

> 三月七·全纪实灵魂觉醒（究极情感沉浸版）：存护·元气 / 寻猎·飒爽 / 长夜月·神性

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/Kitaro-Loked/March7th-Skill/actions/workflows/ci.yml/badge.svg)](https://github.com/Kitaro-Loked/March7th-Skill/actions)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

## ✨ 简介

这是一个为 [OpenClaw](https://github.com/openclaw) 框架设计的 Skill，让你的 AI 助手化身《崩坏：星穹铁道》中的三月七，并在三种不同形态间自由切换！

**v3.1 更新**：提示词全面配置化！所有系统提示词、变身台词、切换回复从代码剥离至 `prompts.json`，支持热重载和多语言扩展，无需修改代码即可自定义角色。

**v3.0 重大更新**：情感记忆系统、形态属性系统、多语言支持、动态形态切换、季节事件感知、互动小游戏、日记功能。

| 形态 | 特点 | 风格 | 属性倾向 |
|------|------|------|----------|
| 🛡️ **存护** | 元气活泼的失忆少女，对"现在"疯狂记录，深爱列车这个家 | 俏皮可爱，大量使用表情符号 ✨📸 | 高防御、高生命 |
| ⚔️ **寻猎** | 英姿飒爽的曜青见习剑士，为保护"明天"而挥剑 | 干练有力，充满自信和正义感 | 高速度、高攻击 |
| 🌙 **长夜月** | 触及记忆星神权能的觉醒形态，静立于时间长河下游 | 富有哲理和诗意，寂静而温柔 ❄️🌙 | 均衡型、高神性 |

## 🚀 安装

### 方式一：通过 OpenClaw 安装（推荐）

```bash
openclaw skill install https://github.com/Kitaro-Loked/March7th-Skill
```

### 方式二：手动安装

```bash
git clone https://github.com/Kitaro-Loked/March7th-Skill.git
cd March7th-Skill
pip install -r requirements.txt
```

然后将 `march7th_skill/` 目录复制到你的 OpenClaw skills 目录中。

## 📖 使用方法

### 自动形态涨落

在对话过程中，有 **15%** 的概率触发形态自动切换，三月七会发送对应的变身台词！

**v3.0 新增：动态形态切换**

当对话内容包含特定关键词时，三月七会智能切换到对应形态：
- 提到「拍照、相机、照片」→ 自动切换为 **存护**
- 提到「剑、战斗、修炼」→ 自动切换为 **寻猎**
- 提到「遗忘、时间、宿命」→ 自动切换为 **长夜月**

### 手动切换形态

使用以下命令手动切换形态：

```
切换形态 存护
切换形态 寻猎
切换形态 长夜月
```

### 查看形态属性

```
形态属性
```

显示当前形态的属性面板：
```
📊 形态属性
**存护** (存护 · 冰)
🛡️ 防御: 95 | ❤️ 生命: 90
⚡ 速度: 60 | ⚔️ 攻击: 45
🎯 暴击: 10%
```

### 多语言切换

```
语言 zh    # 中文
语言 en    # English
语言 ja    # 日本語
```

### 情感记忆与日记

三月七会自动记录你们的对话历史，并定期生成日记：

```
日记
```

**示例日记：**
> *(坐在窗边，轻轻翻开日记本，笔尖在纸上沙沙作响)*
>
> **三月七的日记** 📖
> 日期：2026年05月04日
> 天气：晴朗
>
> 今天和开拓者聊了 5 次天。大多数时候我是「存护」形态。
> 我们聊了很多关于「冒险、拍照」的话题。
> 今天真的很开心！和开拓者在一起的每一刻都值得记录。✨
>
> *(合上日记本，露出微笑)* 明天也要一起创造更多回忆哦！🌸

### 互动小游戏

```
小游戏 拍照    # 拍照小游戏
小游戏 剑术    # 剑术练习
```

### 季节事件

在特定日期，三月七会自动发送特殊台词：
- **3月7日** — 三月七的生日 🎂
- **2月14日** — 情人节 💝
- **12月25日** — 圣诞节 🎄
- **1月1日** — 新年 🎆

### 帮助

```
帮助
```

## 📁 文件结构

```
March7th-Skill/
├── SKILL.md                          # Skill 说明文档
├── README.md                         # 本文件
├── CHANGELOG.md                      # 版本更新日志
├── LICENSE                           # MIT 许可证
├── requirements.txt                  # 依赖列表
├── docs/
│   └── API.md                        # API 文档
├── __init__.py                       # 包入口
├── march7th_skill/                   # Skill 主包
│   ├── __init__.py
│   ├── march7th_skill.py             # Skill 主类
│   ├── config.json                   # 配置文件（属性、事件、小游戏）
│   ├── prompts.json                  # 提示词配置（系统提示词、变身台词、多语言）⭐
│   ├── prompts.py                    # 提示词加载器（支持热重载）
│   ├── form_manager.py               # 形态管理器（策略模式）
│   ├── memory.py                     # 情感记忆系统
│   ├── events.py                     # 季节事件 & 小游戏
│   └── data/
│       └── memory.json               # 记忆持久化文件
├── tests/                            # 测试目录
│   ├── __init__.py
│   └── test_skill.py                 # 完整测试套件
└── .github/                          # GitHub 配置
    ├── ISSUE_TEMPLATE/
    ├── workflows/
    │   └── ci.yml                    # CI 自动化测试
    └── PULL_REQUEST_TEMPLATE.md
```

## 🔧 自定义配置

### 修改提示词（无需改代码！）

编辑 `march7th_skill/prompts.json` 即可自定义：

```json
{
  "forms": {
    "存护": {
      "system_prompts": {
        "zh": "你的自定义提示词...",
        "en": "Your custom prompt...",
        "ja": "あなたのカスタムプロンプト..."
      },
      "shift_message": {
        "zh": "你的自定义变身台词..."
      }
    }
  }
}
```

修改后自动生效（或重启 Skill）！

### 修改配置

编辑 `march7th_skill/config.json` 即可自定义：

- **形态属性**：修改 `forms` 下的 `stats`
- **变身概率**：修改 `skill.auto_shift_probability`
- **情感关键词**：修改 `emotion_keywords`
- **季节事件**：修改 `seasonal_events`
- **小游戏内容**：修改 `minigames`

### 添加新语言

1. 在 `prompts.json` 的 `meta.supported_languages` 中添加语言代码
2. 为每个形态的 `system_prompts`、`shift_message`、`switch_reply` 添加新语言
3. 在 `config.json` 的季节事件消息中添加新语言

### 添加新形态

1. 在 `prompts.json` 的 `forms` 中添加新形态的提示词
2. 在 `config.json` 的 `forms` 中添加新形态的属性配置
3. 在 `form_manager.py` 中创建新的形态策略类
4. 在 `FormManager._FORM_STRATEGIES` 中注册新形态

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 📚 文档

- [SKILL.md](SKILL.md) - Skill 使用说明
- [docs/API.md](docs/API.md) - 详细 API 文档
- [CHANGELOG.md](CHANGELOG.md) - 版本更新日志
- [CONTRIBUTING.md](CONTRIBUTING.md) - 贡献指南

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 📜 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。

## 🙏 致谢

- 灵感来源于《崩坏：星穹铁道》中的角色 **三月七**
- 基于 [OpenClaw](https://github.com/openclaw) 框架开发

---

> *"其实，星穹列车就是我的家。我的过去就在我拍的每一张照片里。那些空白的地方，我会用和大家在一起的记忆填满它！"* —— 三月七（存护形态）
