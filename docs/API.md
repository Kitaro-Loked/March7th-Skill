# March7th-Skill API 文档

> 版本: v3.1.0
> 最后更新: 2026-05-04

## 目录

- [March7thMultiverse](#march7thmultiverse)
- [FormManager](#formmanager)
- [EmotionMemory](#emotionmemory)
- [PromptLoader](#promptloader)
- [SeasonalEventManager](#seasonaleventmanager)
- [MinigameManager](#minigamemanager)

---

## March7thMultiverse

Skill 主类，继承自 `BaseSkill`。

### 初始化

```python
from march7th_skill import March7thMultiverse

skill = March7thMultiverse(config_path="path/to/config.json")
```

**参数：**
- `config_path` (Optional[str]): 配置文件路径，默认使用内置 `config.json`

### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `name` | str | Skill 名称 |
| `description` | str | Skill 描述 |
| `version` | str | 版本号 |
| `current_form` | str | 当前形态名称 |
| `language` | str | 当前语言代码 (zh/en/ja) |
| `auto_shift_probability` | float | 自动变身概率 (0.0-1.0) |

### 方法

#### `record_interaction(user_message, bot_response, emotion_score=0.0, keywords=None)`

记录一次交互到情感记忆。

```python
skill.record_interaction(
    user_message="你好",
    bot_response="你好呀！",
    emotion_score=0.8,
    keywords=["问候"]
)
```

#### `get_memory_summary() -> str`

获取记忆摘要，用于注入系统提示词。

```python
summary = skill.get_memory_summary()
```

#### `get_current_form_info() -> dict`

获取当前形态信息。

```python
info = skill.get_current_form_info()
# {
#     "form": "存护",
#     "language": "zh",
#     "stats": {"defense": 95, "hp": 90, ...},
#     "keywords": ["拍照", "相机", ...]
# }
```

### 指令处理器

| 指令 | 方法 | 说明 |
|------|------|------|
| `@on_message()` | `handle_message` | 处理普通消息 |
| `切换形态 <形态>` | `cmd_switch_form` | 手动切换形态 |
| `形态属性` | `cmd_form_stats` | 查看形态属性 |
| `语言 <zh/en/ja>` | `cmd_language` | 切换语言 |
| `日记` | `cmd_diary` | 生成对话日记 |
| `清空记忆` | `cmd_clear_memory` | 清空记忆 |
| `小游戏 <名称>` | `cmd_minigame` | 玩小游戏 |
| `帮助` | `cmd_help` | 显示帮助 |

---

## FormManager

形态管理器，使用策略模式管理多个形态。

### 初始化

```python
from march7th_skill.form_manager import FormManager

manager = FormManager(config_path="path/to/config.json")
```

### 方法

#### `get_form(name: str) -> Optional[FormStrategy]`

获取指定形态的策略实例。

```python
strategy = manager.get_form("存护")
prompt = strategy.get_system_prompt("zh")
```

#### `get_all_forms() -> List[str]`

获取所有形态名称列表。

```python
forms = manager.get_all_forms()  # ["存护", "寻猎", "长夜月"]
```

#### `get_config(name: str) -> Optional[FormConfig]`

获取形态配置（包含属性、关键词等）。

```python
config = manager.get_config("存护")
print(config.stats.defense)  # 95
print(config.keywords)  # ["拍照", "相机", ...]
```

#### `suggest_form(message: str) -> Optional[str]`

基于消息内容智能推荐形态。

```python
suggested = manager.suggest_form("我想学剑术")  # "寻猎"
```

#### `get_form_stats_display(form_name, lang="zh") -> str`

获取形态属性展示文本。

```python
display = manager.get_form_stats_display("存护", "zh")
```

#### `reload()`

重新加载配置。

```python
manager.reload()
```

---

## EmotionMemory

情感记忆管理器，支持持久化和日记生成。

### 初始化

```python
from march7th_skill.memory import EmotionMemory

memory = EmotionMemory(
    max_entries=50,
    storage_path="path/to/memory.json"
)
```

### 方法

#### `add(user_message, bot_response, form, emotion_score=0.0, keywords=None, context_summary="")`

添加一条记忆。

```python
memory.add(
    user_message="你好",
    bot_response="你好呀！",
    form="存护",
    emotion_score=0.5,
    keywords=["问候"]
)
```

#### `get_recent(n: int) -> List[MemoryEntry]`

获取最近 n 条记忆。

```python
recent = memory.get_recent(5)
```

#### `get_relevant_memories(query: str, top_k=3) -> List[MemoryEntry]`

基于关键词获取相关记忆。

```python
relevant = memory.get_relevant_memories("拍照", top_k=3)
```

#### `get_memory_summary() -> str`

生成记忆摘要。

```python
summary = memory.get_memory_summary()
```

#### `get_emotion_trend() -> float`

获取近期情感趋势（-1.0 到 1.0）。

```python
trend = memory.get_emotion_trend()
```

#### `generate_diary() -> str`

生成日记摘要。

```python
diary = memory.generate_diary()
```

#### `set_preference(key, value) / get_preference(key, default)`

设置/获取用户偏好。

```python
memory.set_preference("language", "en")
lang = memory.get_preference("language", "zh")
```

#### `clear()`

清空所有记忆。

```python
memory.clear()
```

---

## PromptLoader

提示词加载器，支持从 JSON 文件加载和热重载。

### 初始化

```python
from march7th_skill.prompts import PromptLoader

loader = PromptLoader("path/to/prompts.json")
```

### 方法

#### `get_form_prompt(form_name, lang="zh") -> str`

获取形态系统提示词。

```python
prompt = loader.get_form_prompt("存护", "zh")
```

#### `get_shift_message(form_name, lang="zh") -> str`

获取变身台词。

```python
msg = loader.get_shift_message("寻猎", "zh")
```

#### `get_switch_reply(form_name, lang="zh") -> str`

获取切换回复。

```python
reply = loader.get_switch_reply("长夜月", "zh")
```

#### `get_common_message(key, lang="zh") -> str`

获取通用消息。

```python
error_msg = loader.get_common_message("error_messages", "zh")
```

#### `reload()`

强制重新加载提示词。

```python
loader.reload()
```

### 便捷函数

```python
from march7th_skill.prompts import (
    get_form_prompt,
    get_shift_message,
    get_switch_reply,
    get_common_message,
    get_supported_languages,
    reload_prompts,
)

# 获取支持的语言
langs = get_supported_languages()  # ["zh", "en", "ja"]

# 重新加载所有提示词
reload_prompts()
```

---

## SeasonalEventManager

季节事件管理器。

### 方法

#### `get_today_event() -> Optional[dict]`

获取今天的事件。

```python
event = manager.get_today_event()
```

#### `get_event_message(lang="zh") -> Optional[str]`

获取今天的事件消息。

```python
msg = manager.get_event_message("zh")
```

#### `list_all_events() -> List[dict]`

列出所有事件。

```python
events = manager.list_all_events()
```

---

## MinigameManager

小游戏管理器。

### 方法

#### `play_photo_game(lang="zh") -> str`

拍照小游戏。

```python
result = manager.play_photo_game("zh")
```

#### `play_sword_game(lang="zh") -> str`

剑术练习小游戏。

```python
result = manager.play_sword_game("zh")
```

#### `list_games(lang="zh") -> str`

列出可用小游戏。

```python
games = manager.list_games("zh")
```

---

## 配置文件说明

### config.json

```json
{
  "skill": {
    "name": "Skill名称",
    "version": "3.1.0",
    "default_form": "存护",
    "default_language": "zh",
    "auto_shift_probability": 0.15,
    "memory_max_entries": 50,
    "diary_interval": 10
  },
  "forms": {
    "形态名": {
      "name_en": "英文名称",
      "name_ja": "日文名称",
      "path": "命途",
      "element": "属性",
      "stats": {
        "defense": 95,
        "hp": 90,
        "speed": 60,
        "attack": 45,
        "crit_rate": 10
      },
      "keywords": ["关键词1", "关键词2"],
      "emotion_tags": ["标签1", "标签2"]
    }
  },
  "emotion_keywords": {
    "形态名": {
      "关键词": "响应文本"
    }
  },
  "seasonal_events": {
    "MM-DD": {
      "name": "事件名",
      "messages": {
        "zh": "中文消息",
        "en": "English message",
        "ja": "日本語メッセージ"
      }
    }
  },
  "minigames": {
    "游戏名": {
      "scenes": ["场景1", "场景2"],
      "poses": ["姿势1", "姿势2"]
    }
  }
}
```

### prompts.json

```json
{
  "meta": {
    "version": "3.1.0",
    "supported_languages": ["zh", "en", "ja"]
  },
  "forms": {
    "形态名": {
      "name": {
        "zh": "中文名",
        "en": "English Name",
        "ja": "日本語名"
      },
      "system_prompts": {
        "zh": "中文系统提示词",
        "en": "English system prompt",
        "ja": "日本語システムプロンプト"
      },
      "shift_message": {
        "zh": "中文变身台词",
        "en": "English shift message",
        "ja": "日本語変身セリフ"
      },
      "switch_reply": {
        "zh": "中文切换回复",
        "en": "English switch reply",
        "ja": "日本語切り替え返答"
      }
    }
  },
  "common": {
    "error_messages": {
      "zh": "中文错误消息",
      "en": "English error message",
      "ja": "日本語エラーメッセージ"
    }
  }
}
```
