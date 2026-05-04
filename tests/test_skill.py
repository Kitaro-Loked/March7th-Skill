"""March7thMultiverse Skill 完整测试套件 v3.0"""

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock openclaw.sdk 以避免依赖问题
class MockBaseSkill:
    def __init__(self):
        pass

class MockDecorator:
    def __call__(self, func):
        return func

def mock_on_command(cmd):
    return MockDecorator()

def mock_on_message():
    return MockDecorator()

# 注入 mock 模块
mock_sdk = type(sys)('openclaw.sdk')
mock_sdk.BaseSkill = MockBaseSkill
mock_sdk.on_command = mock_on_command
mock_sdk.on_message = mock_on_message
sys.modules['openclaw'] = type(sys)('openclaw')
sys.modules['openclaw.sdk'] = mock_sdk

from march7th_skill.march7th_skill import March7thMultiverse
from march7th_skill.memory import EmotionMemory, MemoryEntry
from march7th_skill.form_manager import FormManager, FormStats, FormConfig
from march7th_skill.events import SeasonalEventManager, MinigameManager
from march7th_skill.prompts import get_form_prompt, get_supported_languages


class TestPrompts(unittest.TestCase):
    """测试提示词系统"""

    def test_get_form_prompt_zh(self):
        prompt = get_form_prompt("存护", "zh")
        self.assertIn("Identity", prompt)
        self.assertIn("三月七", prompt)

    def test_get_form_prompt_en(self):
        prompt = get_form_prompt("存护", "en")
        self.assertIn("Identity", prompt)
        self.assertIn("March 7th", prompt)

    def test_get_form_prompt_ja(self):
        prompt = get_form_prompt("存护", "ja")
        self.assertIn("Identity", prompt)
        self.assertIn("三月なのか", prompt)

    def test_get_form_prompt_all_forms(self):
        for form in ["存护", "寻猎", "长夜月"]:
            for lang in ["zh", "en", "ja"]:
                prompt = get_form_prompt(form, lang)
                self.assertTrue(len(prompt) > 0, f"{form}/{lang} prompt is empty")

    def test_supported_languages(self):
        langs = get_supported_languages()
        self.assertEqual(langs, ["zh", "en", "ja"])


class TestMemory(unittest.TestCase):
    """测试情感记忆系统"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.memory_path = os.path.join(self.temp_dir, "memory.json")
        self.memory = EmotionMemory(max_entries=10, storage_path=self.memory_path)

    def tearDown(self):
        if os.path.exists(self.memory_path):
            os.remove(self.memory_path)
        os.rmdir(self.temp_dir)

    def test_add_memory(self):
        self.memory.add("你好", "你好呀！", "存护", 0.5, ["问候"])
        self.assertEqual(self.memory.memory_count, 1)

    def test_get_recent(self):
        for i in range(5):
            self.memory.add(f"msg{i}", f"resp{i}", "存护")
        recent = self.memory.get_recent(3)
        self.assertEqual(len(recent), 3)
        self.assertEqual(recent[-1].user_message, "msg4")

    def test_max_entries_limit(self):
        for i in range(15):
            self.memory.add(f"msg{i}", f"resp{i}", "存护")
        self.assertEqual(self.memory.memory_count, 10)

    def test_get_relevant_memories(self):
        self.memory.add("拍照", "咔嚓！", "存护", keywords=["拍照"])
        self.memory.add("战斗", "看剑！", "寻猎", keywords=["战斗"])
        relevant = self.memory.get_relevant_memories("拍照", top_k=1)
        self.assertEqual(len(relevant), 1)
        self.assertEqual(relevant[0].user_message, "拍照")

    def test_memory_summary(self):
        self.memory.add("你好", "你好呀！", "存护")
        summary = self.memory.get_memory_summary()
        self.assertIn("Recent Memories", summary)

    def test_emotion_trend(self):
        self.memory.add("a", "b", "存护", 0.5)
        self.memory.add("c", "d", "存护", 0.3)
        trend = self.memory.get_emotion_trend()
        self.assertAlmostEqual(trend, 0.4, places=1)

    def test_form_frequency(self):
        self.memory.add("a", "b", "存护")
        self.memory.add("c", "d", "寻猎")
        self.memory.add("e", "f", "存护")
        freq = self.memory.get_form_frequency()
        self.assertEqual(freq["存护"], 2)
        self.assertEqual(freq["寻猎"], 1)

    def test_preferences(self):
        self.memory.set_preference("language", "en")
        self.assertEqual(self.memory.get_preference("language"), "en")
        self.assertEqual(self.memory.get_preference("unknown", "default"), "default")

    def test_generate_diary(self):
        for i in range(5):
            self.memory.add(f"msg{i}", f"resp{i}", "存护", 0.2)
        diary = self.memory.generate_diary()
        self.assertIn("日记", diary)
        self.assertIn("msg", diary)

    def test_clear(self):
        self.memory.add("a", "b", "存护")
        self.memory.clear()
        self.assertEqual(self.memory.memory_count, 0)

    def test_persistence(self):
        self.memory.add("test", "response", "存护")
        # 创建新实例，应该能加载之前的记忆
        memory2 = EmotionMemory(max_entries=10, storage_path=self.memory_path)
        self.assertEqual(memory2.memory_count, 1)


class TestFormManager(unittest.TestCase):
    """测试形态管理器"""

    def setUp(self):
        self.manager = FormManager()

    def test_get_all_forms(self):
        forms = self.manager.get_all_forms()
        self.assertIn("存护", forms)
        self.assertIn("寻猎", forms)
        self.assertIn("长夜月", forms)

    def test_get_form(self):
        strategy = self.manager.get_form("存护")
        self.assertIsNotNone(strategy)
        self.assertEqual(strategy.form_name, "存护")

    def test_get_config(self):
        config = self.manager.get_config("存护")
        self.assertIsNotNone(config)
        self.assertEqual(config.name, "存护")
        self.assertIsInstance(config.stats, FormStats)

    def test_get_random_form(self):
        form = self.manager.get_random_form()
        self.assertIn(form, self.manager.get_all_forms())

    def test_get_random_form_exclude(self):
        form = self.manager.get_random_form(exclude="存护")
        self.assertNotEqual(form, "存护")

    def test_suggest_form(self):
        # 包含存护关键词
        suggested = self.manager.suggest_form("拍照 相机 照片")
        self.assertEqual(suggested, "存护")

        # 包含寻猎关键词
        suggested = self.manager.suggest_form("剑术 师傅 战斗")
        self.assertEqual(suggested, "寻猎")

        # 无关键词
        suggested = self.manager.suggest_form("abcdefg")
        self.assertIsNone(suggested)

    def test_get_form_stats_display(self):
        display = self.manager.get_form_stats_display("存护", "zh")
        self.assertIn("防御", display)
        self.assertIn("存护", display)

    def test_form_prompts(self):
        for form in self.manager.get_all_forms():
            strategy = self.manager.get_form(form)
            prompt = strategy.get_system_prompt("zh")
            self.assertTrue(len(prompt) > 0)

    def test_emotion_keywords(self):
        strategy = self.manager.get_form("存护")
        response = strategy.get_emotion_response("拍照")
        self.assertIsNotNone(response)

    def test_shift_messages(self):
        for form in self.manager.get_all_forms():
            strategy = self.manager.get_form(form)
            msg = strategy.get_shift_message()
            self.assertTrue(len(msg) > 0)
            self.assertIn("*", msg)  # 动作描写标记

    def test_switch_replies(self):
        for form in self.manager.get_all_forms():
            strategy = self.manager.get_form(form)
            reply = strategy.get_switch_reply()
            self.assertTrue(len(reply) > 0)


class TestEvents(unittest.TestCase):
    """测试事件系统"""

    def setUp(self):
        self.event_manager = SeasonalEventManager()
        self.minigame_manager = MinigameManager()

    def test_seasonal_event_loading(self):
        events = self.event_manager.list_all_events()
        self.assertTrue(len(events) > 0)

    def test_event_message_structure(self):
        events = self.event_manager.list_all_events()
        for event in events:
            self.assertIn("date", event)
            self.assertIn("name", event)

    def test_photo_game(self):
        result = self.minigame_manager.play_photo_game("zh")
        self.assertIn("咔嚓", result)

    def test_photo_game_en(self):
        result = self.minigame_manager.play_photo_game("en")
        self.assertIn("Click", result)

    def test_photo_game_ja(self):
        result = self.minigame_manager.play_photo_game("ja")
        self.assertIn("パシャ", result)

    def test_sword_game(self):
        result = self.minigame_manager.play_sword_game("zh")
        self.assertIn("剑", result)

    def test_list_games(self):
        games = self.minigame_manager.list_games("zh")
        self.assertIn("拍照", games)
        self.assertIn("剑术", games)


class TestMarch7thMultiverse(unittest.TestCase):
    """测试主 Skill 类"""

    def setUp(self):
        self.skill = March7thMultiverse()

    def test_initialization(self):
        self.assertEqual(self.skill.name, "March7th_Multiverse_Skill")
        self.assertEqual(self.skill.current_form, "存护")
        self.assertEqual(self.skill.language, "zh")
        self.assertEqual(self.skill.version, "3.0.0")

    def test_default_form(self):
        self.assertIn(self.skill.current_form, self.skill._form_manager.get_all_forms())

    def test_form_switch(self):
        # 模拟切换
        old_form = self.skill.current_form
        self.skill.current_form = "寻猎"
        self.assertEqual(self.skill.current_form, "寻猎")
        self.assertNotEqual(old_form, self.skill.current_form)

    def test_get_current_strategy(self):
        strategy = self.skill._get_current_strategy()
        self.assertIsNotNone(strategy)
        self.assertEqual(strategy.form_name, "存护")

    def test_language_switch(self):
        self.skill.language = "en"
        self.assertEqual(self.skill.language, "en")
        self.skill.language = "ja"
        self.assertEqual(self.skill.language, "ja")

    def test_localized_text(self):
        text = self.skill._get_localized_text("current_form", form="存护")
        self.assertIn("存护", text)

    def test_localized_text_en(self):
        self.skill.language = "en"
        text = self.skill._get_localized_text("current_form", form="Preservation")
        self.assertIn("Preservation", text)

    def test_record_interaction(self):
        # 使用独立的临时内存路径
        import tempfile
        temp_dir = tempfile.mkdtemp()
        memory_path = os.path.join(temp_dir, "memory.json")
        self.skill._memory = EmotionMemory(max_entries=50, storage_path=memory_path)
        self.skill.record_interaction("你好", "你好呀！", 0.5)
        self.assertEqual(self.skill._memory.memory_count, 1)

    def test_get_memory_summary(self):
        self.skill.record_interaction("你好", "你好呀！")
        summary = self.skill.get_memory_summary()
        self.assertIn("Recent Memories", summary)

    def test_get_current_form_info(self):
        info = self.skill.get_current_form_info()
        self.assertEqual(info["form"], "存护")
        self.assertIn("stats", info)
        self.assertIn("keywords", info)

    def test_check_emotion_keywords(self):
        response = self.skill._check_emotion_keywords("拍照")
        self.assertIsNotNone(response)
        self.assertIn("相机", response)

    def test_check_emotion_keywords_no_match(self):
        response = self.skill._check_emotion_keywords("xyzabc")
        self.assertIsNone(response)

    def test_suggest_form_switch(self):
        suggested = self.skill._suggest_form_switch("剑术 修炼")
        self.assertEqual(suggested, "寻猎")

    def test_config_loading(self):
        self.assertTrue(hasattr(self.skill, "_skill_config"))
        self.assertIn("auto_shift_probability", self.skill._skill_config)

    def test_form_stats(self):
        config = self.skill._form_manager.get_config("存护")
        self.assertIsNotNone(config)
        self.assertGreater(config.stats.defense, 0)
        self.assertGreater(config.stats.speed, 0)


class TestFormStats(unittest.TestCase):
    """测试形态属性"""

    def test_form_stats_creation(self):
        stats = FormStats(defense=95, hp=90, speed=60, attack=45, crit_rate=10)
        self.assertEqual(stats.defense, 95)
        self.assertEqual(stats.hp, 90)

    def test_form_stats_to_dict(self):
        stats = FormStats(defense=95, hp=90, speed=60, attack=45, crit_rate=10)
        d = stats.to_dict()
        self.assertEqual(d["defense"], 95)
        self.assertEqual(d["hp"], 90)

    def test_form_stats_from_dict(self):
        d = {"defense": 95, "hp": 90, "speed": 60, "attack": 45, "crit_rate": 10}
        stats = FormStats.from_dict(d)
        self.assertEqual(stats.defense, 95)


class TestIntegration(unittest.TestCase):
    """集成测试"""

    def setUp(self):
        self.skill = March7thMultiverse()

    def test_full_conversation_flow(self):
        """测试完整对话流程"""
        # 使用独立的临时内存路径
        import tempfile
        temp_dir = tempfile.mkdtemp()
        memory_path = os.path.join(temp_dir, "memory.json")
        self.skill._memory = EmotionMemory(max_entries=50, storage_path=memory_path)
        
        # 1. 初始状态
        self.assertEqual(self.skill.current_form, "存护")

        # 2. 记录对话
        self.skill.record_interaction("你好三月七", "你好呀开拓者！", 0.8)
        self.assertEqual(self.skill._memory.memory_count, 1)

        # 3. 切换形态
        self.skill.current_form = "寻猎"
        self.skill.record_interaction("教我剑术", "好！看好了！", 0.6)

        # 4. 检查记忆
        freq = self.skill._memory.get_form_frequency()
        self.assertEqual(freq["存护"], 1)
        self.assertEqual(freq["寻猎"], 1)

        # 5. 生成日记
        diary = self.skill._memory.generate_diary()
        self.assertIn("日记", diary)

    def test_multi_language_support(self):
        """测试多语言支持"""
        for lang in ["zh", "en", "ja"]:
            self.skill.language = lang
            prompt = self.skill._get_current_strategy().get_system_prompt(lang)
            self.assertTrue(len(prompt) > 0, f"Prompt for {lang} is empty")

    def test_memory_persistence(self):
        """测试记忆持久化"""
        import tempfile
        temp_dir = tempfile.mkdtemp()
        memory_path = os.path.join(temp_dir, "memory.json")
        self.skill._memory = EmotionMemory(max_entries=50, storage_path=memory_path)
        
        self.skill.record_interaction("测试", "收到！", 0.0)
        count_before = self.skill._memory.memory_count

        # 创建新实例，使用相同路径
        skill2 = March7thMultiverse()
        skill2._memory = EmotionMemory(max_entries=50, storage_path=memory_path)
        self.assertEqual(skill2._memory.memory_count, count_before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
