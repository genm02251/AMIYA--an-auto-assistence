#!/usr/bin/env python3
"""
Test script to verify AMIYA AI Assistant installation and basic functionality.
"""

import sys
import traceback
from pathlib import Path


def test_imports():
    """Test that all core modules can be imported."""
    print("Testing imports...")
    
    try:
        import amiya
        print("✓ Main package imported")
    except ImportError as e:
        print(f"✗ Failed to import main package: {e}")
        return False
    
    try:
        from amiya import AmiyaAssistant
        print("✓ AmiyaAssistant imported")
    except ImportError as e:
        print(f"✗ Failed to import AmiyaAssistant: {e}")
        return False
    
    try:
        from amiya.core.screen_capture import ScreenCapture
        print("✓ ScreenCapture imported")
    except ImportError as e:
        print(f"✗ Failed to import ScreenCapture: {e}")
        return False
    
    try:
        from amiya.vision.detector import VisionProcessor
        print("✓ VisionProcessor imported")
    except ImportError as e:
        print(f"✗ Failed to import VisionProcessor: {e}")
        return False
    
    try:
        from amiya.interaction.controller import InteractionController
        print("✓ InteractionController imported")
    except ImportError as e:
        print(f"✗ Failed to import InteractionController: {e}")
        return False
    
    return True


def test_core_functionality():
    """Test basic functionality of core components."""
    print("\nTesting core functionality...")
    
    try:
        from amiya import AmiyaAssistant
        assistant = AmiyaAssistant(safety_mode=True)
        print("✓ Assistant initialized")
    except Exception as e:
        print(f"✗ Failed to initialize assistant: {e}")
        return False
    
    try:
        status = assistant.get_status()
        assert isinstance(status, dict)
        assert 'initialized' in status
        assert status['initialized'] is True
        print("✓ Status check passed")
    except Exception as e:
        print(f"✗ Status check failed: {e}")
        return False
    
    try:
        analysis = assistant.capture_and_analyze()
        assert isinstance(analysis, dict)
        assert 'ui_elements' in analysis
        assert 'text_regions' in analysis
        print("✓ Screen analysis passed")
    except Exception as e:
        print(f"✗ Screen analysis failed: {e}")
        return False
    
    try:
        suggestions = assistant.get_assistance_suggestions()
        assert isinstance(suggestions, list)
        print(f"✓ Suggestions generated: {len(suggestions)} items")
    except Exception as e:
        print(f"✗ Suggestions failed: {e}")
        return False
    
    return True


def test_dependencies():
    """Test availability of key dependencies."""
    print("\nTesting dependencies...")
    
    dependencies = [
        ('cv2', 'OpenCV'),
        ('numpy', 'NumPy'),
        ('PIL', 'Pillow'),
        ('click', 'Click')
    ]
    
    all_available = True
    
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"✓ {name} available")
        except ImportError:
            print(f"✗ {name} not available")
            all_available = False
    
    # Optional dependencies
    optional_deps = [
        ('ultralytics', 'Ultralytics YOLO'),
        ('pyautogui', 'PyAutoGUI'),
        ('pynput', 'Pynput')
    ]
    
    print("\nOptional dependencies:")
    for module, name in optional_deps:
        try:
            __import__(module)
            print(f"✓ {name} available")
        except ImportError:
            print(f"○ {name} not available (optional)")
    
    return all_available


def test_cli():
    """Test CLI functionality."""
    print("\nTesting CLI...")
    
    try:
        from amiya.cli import cli
        print("✓ CLI module imported")
    except ImportError as e:
        print(f"✗ Failed to import CLI: {e}")
        return False
    
    # Test that we can create the CLI without errors
    try:
        import click.testing
        runner = click.testing.CliRunner()
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        print("✓ CLI help command works")
    except Exception as e:
        print(f"✗ CLI help test failed: {e}")
        return False
    
    return True


def test_examples():
    """Test that examples can be imported."""
    print("\nTesting examples...")
    
    examples_path = Path(__file__).parent / "examples.py"
    if not examples_path.exists():
        print("○ Examples file not found (optional)")
        return True
    
    try:
        import examples
        print("✓ Examples module imported")
        return True
    except Exception as e:
        print(f"✗ Failed to import examples: {e}")
        return False


def run_tests():
    """Run all tests and return overall result."""
    print("AMIYA AI Assistant - Installation Test")
    print("=" * 40)
    
    tests = [
        ("Import Tests", test_imports),
        ("Dependency Tests", test_dependencies),
        ("Core Functionality Tests", test_core_functionality),
        ("CLI Tests", test_cli),
        ("Examples Tests", test_examples),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * len(test_name))
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"✗ Test crashed: {e}")
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "=" * 40)
    print("TEST SUMMARY")
    print("=" * 40)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✓ PASS" if results[i] else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AMIYA is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)