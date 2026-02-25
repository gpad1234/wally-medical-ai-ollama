#!/usr/bin/env python3
"""Quick test script to validate OpenAI API key"""
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    print("❌ No OPENAI_API_KEY found in environment or .env file")
    exit(1)

print(f"✓ Key found: {api_key[:15]}...{api_key[-4:]}")
print(f"✓ Key length: {len(api_key)} characters")
print(f"✓ Key format: {'sk-proj-' if api_key.startswith('sk-proj-') else 'sk-' if api_key.startswith('sk-') else 'unknown'}")

# Test the key with a minimal API call
try:
    import openai
    openai.api_key = api_key
    
    print("\n🔄 Testing API key with OpenAI...")
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'test successful' if you receive this."}],
        max_tokens=10
    )
    
    result = response['choices'][0]['message']['content']
    print(f"✅ API key is VALID! Response: {result}")
    
except Exception as e:
    error_str = str(e)
    if "Incorrect API key" in error_str or "invalid_api_key" in error_str:
        print(f"❌ API key is INVALID: {error_str[:200]}")
    elif "quota" in error_str.lower():
        print(f"⚠️  API key is valid but quota exceeded: {error_str[:200]}")
    else:
        print(f"❌ API call failed: {error_str[:200]}")
    exit(1)
