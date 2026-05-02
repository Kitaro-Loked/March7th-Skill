"""March7thMultiverse Skill 的基础测试"""

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
    """测试各形态提示词不为空"""
    skill = March7thMultiverse()
    for form, prompt in skill.prompts.items():
        assert len(prompt) > 0, f"{form} 形态的提示词为空"


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


if __name__ == "__main__":
    test_skill_initialization()
    print("[PASS] Skill initialization test passed")
    
    test_prompts_content()
    print("[PASS] Prompts content test passed")
    
    test_shift_messages()
    print("[PASS] Shift messages test passed")
    
    test_form_switch_replies()
    print("[PASS] Form switch replies test passed")
    
    print("\nAll tests passed!")
