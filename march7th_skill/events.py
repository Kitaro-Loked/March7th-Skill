"""季节和事件感知系统"""

import json
import logging
import os
import random
from datetime import datetime
from typing import Dict, Optional, Any, List

logger = logging.getLogger(__name__)


class SeasonalEventManager:
    """季节事件管理器"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), "config.json"
        )
        self._events: Dict[str, Dict[str, Any]] = {}
        self._load_events()

    def _load_events(self) -> None:
        """加载事件配置"""
        if not os.path.exists(self.config_path):
            logger.warning(f"Config file not found: {self.config_path}")
            return

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            self._events = config.get("seasonal_events", {})
            logger.info(f"Loaded {len(self._events)} seasonal events")
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Failed to load seasonal events: {e}")
            self._events = {}

    def get_today_event(self) -> Optional[Dict[str, Any]]:
        """获取今天的事件"""
        today = datetime.now().strftime("%m-%d")
        return self._events.get(today)

    def get_event_message(self, lang: str = "zh") -> Optional[str]:
        """获取今天的事件消息"""
        event = self.get_today_event()
        if not event:
            return None
        messages = event.get("messages", {})
        return messages.get(lang) or messages.get("zh")

    def get_event_name(self, lang: str = "zh") -> Optional[str]:
        """获取今天的事件名称"""
        event = self.get_today_event()
        if not event:
            return None
        if lang == "en":
            return event.get("name_en", event.get("name"))
        elif lang == "ja":
            return event.get("name_ja", event.get("name"))
        return event.get("name")

    def list_all_events(self) -> List[Dict[str, str]]:
        """列出所有事件"""
        result = []
        for date, event in self._events.items():
            result.append({
                "date": date,
                "name": event.get("name", ""),
                "name_en": event.get("name_en", ""),
                "name_ja": event.get("name_ja", ""),
            })
        return result


class MinigameManager:
    """小游戏管理器"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), "config.json"
        )
        self._minigames: Dict[str, Dict[str, Any]] = {}
        self._load_minigames()

    def _load_minigames(self) -> None:
        """加载小游戏配置"""
        if not os.path.exists(self.config_path):
            logger.warning(f"Config file not found: {self.config_path}")
            return

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            self._minigames = config.get("minigames", {})
            logger.info(f"Loaded {len(self._minigames)} minigames")
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Failed to load minigames: {e}")
            self._minigames = {}

    def play_photo_game(self, lang: str = "zh") -> str:
        """拍照小游戏"""
        photo_game = self._minigames.get("拍照", {})
        scenes = photo_game.get("scenes", ["星穹列车车厢"])
        poses = photo_game.get("poses", ["元气剪刀手"])

        scene = random.choice(scenes)
        pose = random.choice(poses)

        responses = {
            "zh": (
                f"*(举起相机，眼睛弯成月牙)* 来！我们在**{scene}**拍一张！\n"
                f"摆个**{pose}**的姿势——对！就是这样！\n"
                f"咔嚓！📸\n"
                f"哇！这张超棒的！你的表情很自然呢！"
            ),
            "en": (
                f"*(raising the camera, eyes curved like crescent moons)* Come on! Let's take a photo at the **{scene}**!\n"
                f"Strike a **{pose}** pose—yes! Just like that!\n"
                f"Click! 📸\n"
                f"Wow! This one is amazing! Your expression looks so natural!"
            ),
            "ja": (
                f"*(カメラを掲げて、目を三日月のように曲げる)* ほら！**{scene}**で写真を撮ろう！\n"
                f"**{pose}**のポーズをとって——そう！その調子！\n"
                f"パシャ！📸\n"
                f"わあ！これすっごくいい！表情が自然だね！"
            ),
        }
        return responses.get(lang, responses["zh"])

    def play_sword_game(self, lang: str = "zh") -> str:
        """剑术练习小游戏"""
        sword_game = self._minigames.get("剑术", {})
        moves = sword_game.get("moves", ["惊鸿一剑"])

        move = random.choice(moves)

        responses = {
            "zh": (
                f"*(拔出双剑，剑身在阳光下闪烁着寒光)*\n"
                f"来！跟我一起练习**{move}**！\n"
                f"首先，重心下沉……对，很好！\n"
                f"然后，剑随身转——去！疾！落！\n"
                f"*(剑光如流星划过)*\n"
                f"不错不错！你的天赋比我想象的还要好呢！"
            ),
            "en": (
                f"*(drawing dual swords, the blades gleaming coldly in the sunlight)*\n"
                f"Come! Practice **{move}** with me!\n"
                f"First, lower your center of gravity... Yes, very good!\n"
                f"Then, let the sword follow your body—Go! Swift! Fall!\n"
                f"*(sword light streaking like a meteor)*\n"
                f"Not bad, not bad! Your talent is even better than I imagined!"
            ),
            "ja": (
                f"*(双剣を抜き、剣身が陽光の中で冷たく輝く)*\n"
                f"さあ！一緒に**{move}**を練習しよう！\n"
                f"まず、重心を下げて……そう、その調子！\n"
                f"そして、剣を体に合わせて——行け！疾！落！\n"
                f"*(剣光が流星のように走る)*\n"
                f"なかなかじゃない！想像以上の才能があるね！"
            ),
        }
        return responses.get(lang, responses["zh"])

    def list_games(self, lang: str = "zh") -> str:
        """列出可用小游戏"""
        names = {
            "zh": {"拍照": "📸 拍照小游戏", "剑术": "⚔️ 剑术练习"},
            "en": {"拍照": "📸 Photography Game", "剑术": "⚔️ Sword Practice"},
            "ja": {"拍照": "📸 写真撮影ゲーム", "剑术": "⚔️ 剣術練習"},
        }
        game_names = names.get(lang, names["zh"])
        lines = [game_names.get(k, k) for k in self._minigames.keys()]
        return "\n".join(lines)
