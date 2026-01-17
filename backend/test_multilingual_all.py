import sys
import os

# Add backend directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, 'backend') if 'backend' not in current_dir else current_dir
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.utils.prompt_templates import get_user_prompt, get_system_prompt
from app.routes.mock_interview import get_localized_interviewer_style, normalize_interviewer_style

def test_question_bank_prompts():
    print("\n=== Testing Question Bank Prompts ===")
    
    # Test EN user prompt
    prompt_en = get_user_prompt(
        'question_bank', 'en', 'user_template',
        count=5, resume_content="Resume Content", custom_topic="Java Concurrency"
    )
    assert "Java Concurrency" in prompt_en
    assert "Resume Content" in prompt_en
    assert "generate 5 high-quality interview questions" in prompt_en
    print("✓ Question Bank EN Prompt (Topic) OK")

    # Test ZH user prompt
    prompt_zh = get_user_prompt(
        'question_bank', 'zh', 'user_template',
        count=3, resume_content="简历内容", custom_topic=""
    )
    assert "简历内容" in prompt_zh
    assert "3道" in prompt_zh
    print("✓ Question Bank ZH Prompt (No Topic) OK")

def test_mock_interview_logic():
    print("\n=== Testing Mock Interview Logic ===")
    
    # Test Style Normalization
    assert normalize_interviewer_style("Strict Tech Lead") == "严厉技术官"
    assert normalize_interviewer_style("温柔HR") == "温柔HR"
    print("✓ Style Normalization OK")
    
    # Test Style Localization
    assert get_localized_interviewer_style("严厉技术官", "en") == "Strict Tech Lead"
    assert get_localized_interviewer_style("严厉技术官", "zh") == "严厉技术官"
    print("✓ Style Localization OK")
    
    # Test Start Interview Prompt (EN)
    style_en = get_localized_interviewer_style("严厉技术官", "en") # Strict Tech Lead
    prompt_start_en = get_user_prompt(
        'mock_interview', 'en', 'start_interview',
        style=style_en, resume_content="My Resume"
    )
    assert "Strict Tech Lead-style" in prompt_start_en
    assert "My Resume" in prompt_start_en
    print("✓ Start Interview EN Prompt OK")
    
    # Test Feedback & Question Prompt (EN)
    prompt_fq_en = get_user_prompt(
        'mock_interview', 'en', 'feedback_and_question',
        style=style_en, resume_content="My Resume",
        conversation_history="['hi']", current_question="Intro?", answer="My answer"
    )
    assert "Strict Tech Lead-style" in prompt_fq_en
    assert "My answer" in prompt_fq_en
    print("✓ Feedback & Question EN Prompt OK")

def test_strategy_prompts():
    print("\n=== Testing Strategy Prompts ===")
    
    # Test Analysis Prompt (EN)
    prompt_analysis_en = get_user_prompt(
        'strategy', 'en', 'analysis_template',
        resume_content="My CV", background_info="Student", directions='["Backend"]'
    )
    assert "My CV" in prompt_analysis_en
    assert "Student" in prompt_analysis_en
    print("✓ Strategy Analysis EN Prompt OK")
    
    # Test Questions Prompt (EN)
    prompt_questions_en = get_user_prompt(
        'strategy', 'en', 'questions_template',
        company="Google", position="SDE", question_types="['Team']"
    )
    assert "Google" in prompt_questions_en
    assert "SDE" in prompt_questions_en
    print("✓ Strategy Questions EN Prompt OK")

if __name__ == "__main__":
    try:
        test_question_bank_prompts()
        test_mock_interview_logic()
        test_strategy_prompts()
        print("\nAll Tests Passed!")
    except ImportError as e:
        print(f"\nImport Error: {e}")
        print("Make sure you are running this from outside the backend directory or with PYTHONPATH set correctly.")
    except AssertionError as e:
        print(f"\nAssertion Failed!")
        raise e
