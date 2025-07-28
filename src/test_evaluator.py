#!/usr/bin/env python3
"""
Test script for the evaluator functionality
"""

def test_evaluator():
    """Test the evaluator functionality"""
    try:
        from evaluator import Evaluator, example_evaluation
        
        print("Testing Evaluator...")
        
        # Test basic initialization
        evaluator = Evaluator()
        print("✓ Evaluator initialized successfully")
        
        # Test example evaluation
        print("\nRunning example evaluation...")
        evaluation = example_evaluation()
        
        print(f"✓ Evaluation completed: {evaluation.is_acceptable}")
        print(f"✓ Feedback: {evaluation.feedback}")
        
        return True
        
    except Exception as e:
        print(f"✗ Evaluator test error: {e}")
        return False

def main():
    """Run the evaluator test"""
    print("Testing Evaluator functionality...\n")
    
    if test_evaluator():
        print("\n🎉 Evaluator test passed!")
    else:
        print("\n❌ Evaluator test failed!")

if __name__ == "__main__":
    main() 