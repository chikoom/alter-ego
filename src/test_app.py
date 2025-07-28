#!/usr/bin/env python3
"""
Test script to verify the modular structure works correctly
"""

def test_imports():
    """Test that all modules can be imported correctly"""
    try:
        from config import Config
        print("✓ Config module imported successfully")
        
        from notifications import NotificationService
        print("✓ NotificationService module imported successfully")
        
        from tools import tools, tool_functions
        print("✓ Tools module imported successfully")
        
        from personality import Personality
        print("✓ Personality module imported successfully")
        
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_config():
    """Test configuration values"""
    try:
        from config import Config
        
        name = Config.get_person_name()
        print(f"✓ Person name: {name}")
        
        linkedin_path = Config.get_linkedin_profile_path()
        print(f"✓ LinkedIn path: {linkedin_path}")
        
        summary_path = Config.get_summary_path()
        print(f"✓ Summary path: {summary_path}")

        resume_path = Config.get_resume_path()
        print(f"✓ Resume path: {resume_path}")
        
        return True
    except Exception as e:
        print(f"✗ Config test error: {e}")
        return False

def test_personality_creation():
    """Test personality creation"""
    try:
        from personality import Personality
        
        personality = Personality()
        print(f"✓ Personality created for: {personality.name}")
        print(f"✓ LinkedIn profile loaded: {len(personality.linkedin)} characters")
        print(f"✓ Summary loaded: {len(personality.summary)} characters")
        print(f"✓ Resume loaded: {len(personality.resume)} characters")
        
        return True
    except Exception as e:
        print(f"✗ Personality creation error: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing Alter Ego modular structure...\n")
    
    tests = [
        test_imports,
        test_config,
        test_personality_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The modular structure is working correctly.")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 