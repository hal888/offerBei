#!/usr/bin/env python3
"""
Test script to verify Mock Interview i18n fix
"""
import sys
import os

# Add backend directory to sys path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from app.utils.prompt_templates import get_user_prompt, get_system_prompt

def test_start_interview_prompts():
    """Test that start_interview prompts specify output language"""
    print("=" * 60)
    print("Testing Mock Interview Start Prompts")
    print("=" * 60)
    
    # Test Chinese prompt
    zh_prompt = get_user_prompt(
        'mock_interview', 'zh', 'start_interview',
        style="温柔HR",
        resume_content="测试简历"
    )
    
    # Check for Chinese language specification
    assert '中文' in zh_prompt or '必须使用' in zh_prompt, "❌ Chinese start_interview doesn't specify Chinese output"
    assert '所有对话内容' in zh_prompt or '问候语' in zh_prompt, "❌ Chinese start_interview missing conversation content language spec"
    print("✅ Chinese start_interview prompt specifies Chinese output")
    print(f"   Found language specification in prompt")
    
    # Test English prompt
    en_prompt = get_user_prompt(
        'mock_interview', 'en', 'start_interview',
        style="Gentle HR",
        resume_content="Test resume"
    )
    
    # Check for English language specification
    assert 'English' in en_prompt and 'must be in' in en_prompt, "❌ English start_interview doesn't specify English output"
    assert 'conversation content' in en_prompt or 'greetings' in en_prompt, "❌ English start_interview missing conversation content spec"
    print("✅ English start_interview prompt specifies English output")
    print(f"   Found language specification in prompt")
    
    return True

def test_feedback_and_question_prompts():
    """Test that feedback_and_question prompts specify output language"""
    print("\n" + "=" * 60)
    print("Testing Mock Interview Feedback & Question Prompts")
    print("=" * 60)
    
    # Test Chinese prompt
    zh_prompt = get_user_prompt(
        'mock_interview', 'zh', 'feedback_and_question',
        style="温柔HR",
        resume_content="测试简历",
        conversation_history="['你好']",
        current_question="请自我介绍",
        answer="我叫张三"
    )
    
    # Check for Chinese language specification in both feedback and question
    assert '反馈内容必须使用中文' in zh_prompt, "❌ Chinese feedback_and_question doesn't specify Chinese for feedback"
    assert '问题内容必须使用中文' in zh_prompt, "❌ Chinese feedback_and_question doesn't specify Chinese for questions"
    assert '所有文本内容使用中文' in zh_prompt, "❌ Chinese feedback_and_question missing general language requirement"
    print("✅ Chinese feedback_and_question prompt specifies Chinese output")
    print(f"   Feedback language: specified ✓")
    print(f"   Question language: specified ✓")
    
    # Test English prompt
    en_prompt = get_user_prompt(
        'mock_interview', 'en', 'feedback_and_question',
        style="Gentle HR",
        resume_content="Test resume",
        conversation_history="['Hello']",
        current_question="Please introduce yourself",
        answer="My name is John"
    )
    
    # Check for English language specification in both feedback and question
    assert 'Feedback content must be in English' in en_prompt, "❌ English feedback_and_question doesn't specify English for feedback"
    assert 'Question content must be in English' in en_prompt, "❌ English feedback_and_question doesn't specify English for questions"
    assert 'All text content must be in English' in en_prompt, "❌ English feedback_and_question missing general language requirement"
    print("✅ English feedback_and_question prompt specifies English output")
    print(f"   Feedback language: specified ✓")
    print(f"   Question language: specified ✓")
    
    return True

def print_sample_prompts():
    """Print sample prompts for manual inspection"""
    print("\n" + "=" * 60)
    print("Sample Chinese Start Interview Prompt (First 250 chars)")
    print("=" * 60)
    
    zh_prompt = get_user_prompt(
        'mock_interview', 'zh', 'start_interview',
        style="温柔HR",
        resume_content="工作经历：阿里巴巴后端工程师"
    )
    print(zh_prompt[:250] + "...")
    
    print("\n" + "=" * 60)
    print("Sample English Start Interview Prompt (First 250 chars)")
    print("=" * 60)
    
    en_prompt = get_user_prompt(
        'mock_interview', 'en', 'start_interview',
        style="Gentle HR",
        resume_content="Experience: Backend Engineer at Google"
    )
    print(en_prompt[:250] + "...")

if __name__ == "__main__":
    try:
        print("\n🔍 Mock Interview i18n Fix Verification\n")
        
        all_passed = True
        all_passed &= test_start_interview_prompts()
        all_passed &= test_feedback_and_question_prompts()
        
        print_sample_prompts()
        
        print("\n" + "=" * 60)
        if all_passed:
            print("✅ ALL TESTS PASSED!")
            print("=" * 60)
            print("\nThe Mock Interview i18n fix is working correctly:")
            print("1. ✅ Chinese prompts specify Chinese output for all content")
            print("2. ✅ English prompts specify English output for all content")
            print("3. ✅ Both start_interview and feedback_and_question fixed")
            print("4. ✅ Greetings, questions, and feedback all localized")
            print("\nMock Interview will now conduct interviews fully in the user's language!")
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
