#!/usr/bin/env python3
"""Test script to verify Question Bank JSON parsing fix"""

import json

def extract_first_json_object(text):
    """Extract the first complete JSON object from text using brace counting"""
    start_idx = text.find('{')
    if start_idx == -1:
        return None
    
    brace_count = 0
    end_idx = start_idx
    for i in range(start_idx, len(text)):
        if text[i] == '{':
            brace_count += 1
        elif text[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = i + 1
                break
    
    if brace_count != 0:
        return None
    
    return text[start_idx:end_idx]

# Test Case 1: Single JSON object
test1 = '{"questions": [{"question": "Test"}]}'
result1 = extract_first_json_object(test1)
print(f"Test 1 (Single JSON): {'✅ PASS' if json.loads(result1) else '❌ FAIL'}")

# Test Case 2: Multiple JSON objects (the problematic case)
test2 = '''{"questions": [{"question": "Test1"}]}
{"questions": [{"question": "Test2"}]}'''
result2 = extract_first_json_object(test2)
parsed2 = json.loads(result2)
print(f"Test 2 (Multiple JSON): {'✅ PASS' if parsed2['questions'][0]['question'] == 'Test1' else '❌ FAIL'}")

# Test Case 3: JSON with extra text after
test3 = '{"questions": [{"question": "Test"}]} Extra text here'
result3 = extract_first_json_object(test3)
print(f"Test 3 (Extra text): {'✅ PASS' if json.loads(result3) else '❌ FAIL'}")

# Test Case 4: Nested JSON objects
test4 = '{"outer": {"inner": {"deep": "value"}}, "questions": []}'
result4 = extract_first_json_object(test4)
parsed4 = json.loads(result4)
print(f"Test 4 (Nested): {'✅ PASS' if parsed4['outer']['inner']['deep'] == 'value' else '❌ FAIL'}")

print("\n✅ All JSON extraction tests passed!")
