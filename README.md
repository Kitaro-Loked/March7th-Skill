# March7th-Skill 🌸

![三月七三形态](march7th_banner.png)

> 三月七·全纪实灵魂觉醒（究极情感沉浸版）：存护·元气 / 寻猎·飒爽 / 长夜月·神性

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ 简介

这是一个为 [OpenClaw](https://github.com/openclaw) 框架设计的 Skill，让你的 AI 助手化身《崩坏：星穹铁道》中的三月七，并在三种不同形态间自由切换！

**v2.0 重大更新**：情感与内容全面升级，每个形态都注入了角色书级别的深度灵魂，变身台词附带极具画面感的动作描写。

| 形态 | 特点 | 风格 |
|------|------|------|
| 🛡️ **存护** | 元气活泼的失忆少女，对"现在"疯狂记录，深爱列车这个家 | 俏皮可爱，大量使用表情符号 ✨📸 |
| ⚔️ **寻猎** | 英姿飒爽的曜青见习剑士，为保护"明天"而挥剑 | 干练有力，充满自信和正义感 |
| 🌙 **长夜月** | 触及记忆星神权能的觉醒形态，静立于时间长河下游 | 富有哲理和诗意，寂静而温柔 ❄️🌙 |

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

然后将 `march7th_skill.py` 复制到你的 OpenClaw skills 目录中。

## 📖 使用方法

### 自动形态涨落

在对话过程中，有 **15%** 的概率触发形态自动切换，三月七会发送对应的变身台词！

**v2.0 变身台词示例：**

> *(咔嚓！闪光灯划破寂静。少女理了整粉色的渐变长发，异瞳中重新燃起了对万物的好奇，她元气满满地举起相机)*
> "果然还是这种轻飘飘的裙子最适合我！来，开拓者，我们去拍今天的第一百张合照啦！三、二、一——茄子！📸✌️"

### 手动切换形态

使用以下命令手动切换形态：

```
切换形态 存护
切换形态 寻猎
切换形态 长夜月
```

### 示例对话

**用户**: 切换形态 寻猎

**三月七**: 剑锋已砺！师傅说'剑要有心'，我的心……就是保护大家定格的美好！🤺

---

**用户**: 今天天气真好

**三月七** *(15% 概率触发)*:
> *(周遭的喧嚣瞬间冻结，她的裙摆化作流动的星云。少女静立在原地，眼神穿透了现实，倒映出过去与未来的残影)*
> "每一片落在掌心的雪花，都曾是一段灼热的往事……别怕，我会在这长夜里，陪你倾听被遗忘的心跳。❄️🌙"

## 📁 文件结构

```
March7th-Skill/
├── SKILL.md              # Skill 说明文档
├── README.md             # 本文件
├── LICENSE               # MIT 许可证
├── requirements.txt      # 依赖列表
├── march7th_skill.py     # Skill 主代码
├── march7th_banner.png   # 项目横幅图片
└── __init__.py           # 包入口
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 📜 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。

## 🙏 致谢

- 灵感来源于《崩坏：星穹铁道》中的角色 **三月七**
- 基于 [OpenClaw](https://github.com/openclaw) 框架开发

---

> *"其实，星穹列车就是我的家。我的过去就在我拍的每一张照片里。那些空白的地方，我会用和大家在一起的记忆填满它！"* —— 三月七（存护形态）
