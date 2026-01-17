#!/usr/bin/env python3
"""
Test script to verify Strategy Portrait Analysis i18n fix
"""
import sys
import os

# Add backend directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from app.utils.prompt_templates import get_user_prompt, get_system_prompt

def test_strategy_analysis_prompts():
    """Test that strategy analysis prompts specify output language"""
    print("=" * 60)
    print("Testing Strategy Analysis Prompt Language Specification")
    print("=" * 60)
    
    # Test Chinese prompt
    zh_prompt = get_user_prompt(
        'strategy', 'zh', 'analysis_template',
        resume_content="测试简历",
        background_info="应届毕业生",
        directions='["后端开发"]'
    )
    
    # Check that Chinese prompt specifies Chinese output
    assert '中文' in zh_prompt or '必须使用' in zh_prompt, "❌ Chinese prompt doesn't specify Chinese output language"
    assert '输出要求' in zh_prompt, "❌ Chinese prompt missing output requirements section"
    print("✅ Chinese analysis prompt correctly specifies Chinese output")
    print(f"   Language specification found in prompt")
    
    # Test English prompt
    en_prompt = get_user_prompt(
        'strategy', 'en', 'analysis_template',
        resume_content="Test resume",
        background_info="Fresh graduate",
        directions='["Backend Development"]'
    )
    
    # Check that English prompt specifies English output
    assert 'English' in en_prompt or 'must be in' in en_prompt, "❌ English prompt doesn't specify English output language"
    assert 'Output Requirements' in en_prompt, "❌ English prompt missing output requirements section"
    print("✅ English analysis prompt correctly specifies English output")
    print(f"   Language specification found in prompt")
    
    return True

def test_strategy_questions_prompts():
    """Test that strategy questions prompts specify output language"""
    print("\n" + "=" * 60)
    print("Testing Strategy Questions Prompt Language Specification")
    print("=" * 60)
    
    # Test Chinese prompt
    zh_prompt = get_user_prompt(
        'strategy', 'zh', 'questions_template',
        company="腾讯",
        position="后端工程师",
        question_types='["团队文化", "技术栈"]'
    )
    
    assert '中文' in zh_prompt or '必须使用' in zh_prompt, "❌ Chinese questions prompt doesn't specify Chinese output"
    assert '输出要求' in zh_prompt, "❌ Chinese questions prompt missing output requirements"
    print("✅ Chinese questions prompt correctly specifies Chinese output")
    
    # Test English prompt
    en_prompt = get_user_prompt(
        'strategy', 'en', 'questions_template',
        company="Google",
        position="Backend Engineer",
        question_types='["Team Culture", "Tech Stack"]'
    )
    
    assert 'English' in en_prompt or 'must be in' in en_prompt, "❌ English questions prompt doesn't specify English output"
    assert 'Output Requirements' in en_prompt, "❌ English questions prompt missing output requirements"
    print("✅ English questions prompt correctly specifies English output")
    
    return True

def test_system_prompts():
    """Test that system prompts are also localized"""
    print("\n" + "=" * 60)
    print("Testing Strategy System Prompts")
    print("=" * 60)
    
    # Test Chinese system prompts
    zh_analysis_sys = get_system_prompt('strategy', 'zh', 'analysis_system')
    zh_questions_sys = get_system_prompt('strategy', 'zh', 'questions_system')
    
    # Chinese system prompts should be in Chinese
    assert any(ord(c) > 127 for c in zh_analysis_sys), "❌ Chinese analysis system prompt not in Chinese"
    assert any(ord(c) > 127 for c in zh_questions_sys), "❌ Chinese questions system prompt not in Chinese"
    print("✅ Chinese system prompts are in Chinese")
    
    # Test English system prompts
    en_analysis_sys = get_system_prompt('strategy', 'en', 'analysis_system')
    en_questions_sys = get_system_prompt('strategy', 'en', 'questions_system')
    
    # English system prompts should be in English (all ASCII)
    assert all(ord(c) < 128 for c in en_analysis_sys if c.isalpha()), "❌ English analysis system prompt contains non-ASCII"
    assert all(ord(c) < 128 for c in en_questions_sys if c.isalpha()), "❌ English questions system prompt contains non-ASCII"
    print("✅ English system prompts are in English")
    
    return True

def print_sample_prompts():
    """Print sample prompts for manual inspection"""
    print("\n" + "=" * 60)
    print("Sample Chinese Analysis Prompt (First 200 chars)")
    print("=" * 60)
    
    zh_prompt = get_user_prompt(
        'strategy', 'zh', 'analysis_template',
        resume_content="测试简历内容",
        background_info="应届毕业生",
        directions='["后端开发", "云计算"]'
    )
    print(zh_prompt[:200] + "...")
    
    print("\n" + "=" * 60)
    print("Sample English Analysis Prompt (First 200 chars)")
    print("=" * 60)
    
    en_prompt = get_user_prompt(
        'strategy', 'en', 'analysis_template',
        resume_content="Test resume content",
        background_info="Fresh graduate",
        directions='["Backend Dev", "Cloud Computing"]'
    )
    print(en_prompt[:200] + "...")

if __name__ == "__main__":
    try:
        print("\n🔍 Strategy Portrait Analysis i18n Fix Verification\n")
        
        all_passed = True
        all_passed &= test_strategy_analysis_prompts()
        all_passed &= test_strategy_questions_prompts()
        all_passed &= test_system_prompts()
        
        print_sample_prompts()
        
        print("\n" + "=" * 60)
        if all_passed:
            print("✅ ALL TESTS PASSED!")
            print("=" * 60)
            print("\nThe Strategy i18n fix is working correctly:")
            print("1. ✅ Chinese prompts specify Chinese output")
            print("2. ✅ English prompts specify English output")
            print("3. ✅ System prompts are properly localized")
            print("4. ✅ Both analysis and questions templates fixed")
            print("\nDeepSeek will now generate content in the correct language!")
            sys.exit(0)
        else:
            print("❌ SOME TESTS FAILED")
            print("=" * 60)
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
