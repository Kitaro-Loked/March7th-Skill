"""March7thMultiverse Skill 的基础测试（究极情感沉浸版）"""

import sys
import os

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

from march7th_skill import March7thMultiverse


def test_skill_initialization():
    """测试 Skill 初始化"""
    skill = March7thMultiverse()
    assert skill.name == "March7th_Multiverse_Skill"
    assert skill.current_form == "存护"
    assert "存护" in skill.prompts
    assert "寻猎" in skill.prompts
    assert "长夜月" in skill.prompts


def test_prompts_content():
    """测试各形态提示词不为空且包含丰富情感内容"""
    skill = March7thMultiverse()
    for form, prompt in skill.prompts.items():
        assert len(prompt) > 0, f"{form} 形态的提示词为空"
        # 检查新版提示词包含角色书级别的深度内容
        assert "[" in prompt, f"{form} 形态缺少结构化标记"


def test_shift_messages():
    """测试变身台词完整性"""
    skill = March7thMultiverse()
    for form in skill.prompts.keys():
        assert form in skill.shift_msgs, f"缺少 {form} 的变身台词"
        assert form in skill.switch_replies, f"缺少 {form} 的切换回复"


def test_form_switch_replies():
    """测试切换回复内容"""
    skill = March7thMultiverse()
    assert len(skill.switch_replies["存护"]) > 0
    assert len(skill.switch_replies["寻猎"]) > 0
    assert len(skill.switch_replies["长夜月"]) > 0


def test_prompts_contain_emotion_keywords():
    """测试提示词包含丰富的情感关键词（v2.0 增强点）"""
    skill = March7thMultiverse()
    
    # 存护形态应包含情感关键词
    cundun = skill.prompts["存护"]
    assert "执念" in cundun or "焦虑" in cundun or "深爱" in cundun, \
        "存护形态缺少深层情感描述"
    
    # 寻猎形态应包含情感关键词
    xunlie = skill.prompts["寻猎"]
    assert "热血" in xunlie or "责任感" in xunlie or "保护" in xunlie, \
        "寻猎形态缺少深层情感描述"
    
    # 长夜月形态应包含情感关键词
    changyeyue = skill.prompts["长夜月"]
    assert "悲悯" in changyeyue or "宿命" in changyeyue or "灵魂" in changyeyue, \
        "长夜月形态缺少深层情感描述"


def test_shift_messages_have_action_descriptions():
    """测试变身台词包含画面感动作描写（v2.0 增强点）"""
    skill = March7thMultiverse()
    for form, msg in skill.shift_msgs.items():
        assert "*" in msg, f"{form} 的变身台词缺少动作描写标记 *...*"
        assert len(msg) > 50, f"{form} 的变身台词过于简短，缺少画面感"


if __name__ == "__main__":
    test_skill_initialization()
    print("[PASS] Skill initialization test passed")
    
    test_prompts_content()
    print("[PASS] Prompts content test passed")
    
    test_shift_messages()
    print("[PASS] Shift messages test passed")
    
    test_form_switch_replies()
    print("[PASS] Form switch replies test passed")
    
    test_prompts_contain_emotion_keywords()
    print("[PASS] Emotion keywords test passed")
    
    test_shift_messages_have_action_descriptions()
    print("[PASS] Action descriptions test passed")
    
    print("\n[ALL PASS] March7th Multiverse v2.0 is ready!")
