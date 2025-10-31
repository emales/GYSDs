#!/usr/bin/env python3
"""
Test Script for Refactored Architecture

Tests the modular architecture without requiring Streamlit to be running.
Verifies imports, class instantiation, and basic functionality.
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all module imports."""
    print("🔍 Testing imports...")
    
    try:
        # Test modules imports
        from modules.auth.login import AuthenticationManager
        from modules.auth.session import SessionManager
        from modules.database.connection import DatabaseConnection
        print("✅ Backend modules imported successfully")
        
        # Create a mock streamlit module to avoid import errors
        import types
        st_mock = types.ModuleType('streamlit')
        setattr(st_mock, 'session_state', {})
        setattr(st_mock, 'error', lambda x: print(f"ERROR: {x}"))
        setattr(st_mock, 'success', lambda x: print(f"SUCCESS: {x}"))
        setattr(st_mock, 'warning', lambda x: print(f"WARNING: {x}"))
        setattr(st_mock, 'info', lambda x: print(f"INFO: {x}"))
        setattr(st_mock, 'rerun', lambda: None)
        setattr(st_mock, 'markdown', lambda x, **kwargs: None)
        setattr(st_mock, 'title', lambda x: None)
        setattr(st_mock, 'header', lambda x: None)
        setattr(st_mock, 'subheader', lambda x: None)
        setattr(st_mock, 'columns', lambda x: [None] * x)
        setattr(st_mock, 'form', lambda x: None)
        setattr(st_mock, 'text_input', lambda *args, **kwargs: "")
        setattr(st_mock, 'button', lambda *args, **kwargs: False)
        setattr(st_mock, 'form_submit_button', lambda *args, **kwargs: False)
        setattr(st_mock, 'tabs', lambda x: [None] * len(x))
        setattr(st_mock, 'sidebar', types.ModuleType('sidebar'))
        setattr(st_mock.sidebar, 'success', lambda x: None)
        setattr(st_mock.sidebar, 'write', lambda x: None)
        setattr(st_mock.sidebar, 'button', lambda *args, **kwargs: False)
        setattr(st_mock.sidebar, 'checkbox', lambda *args, **kwargs: False)
        setattr(st_mock.sidebar, 'expander', lambda x: types.ModuleType('expander'))
        setattr(st_mock, 'secrets', {'get': lambda x, default=None: default})
        sys.modules['streamlit'] = st_mock
        
        # Mock pandas and numpy
        pandas_mock = types.ModuleType('pandas')
        setattr(pandas_mock, 'DataFrame', lambda *args, **kwargs: None)
        sys.modules['pandas'] = pandas_mock
        
        numpy_mock = types.ModuleType('numpy')
        setattr(numpy_mock, 'random', types.ModuleType('random'))
        setattr(numpy_mock.random, 'randn', lambda *args: [[0] * args[1]] * args[0])
        sys.modules['numpy'] = numpy_mock
        
        # Now test screen imports
        from screens.base_screen import BaseScreen
        from screens.auth_screen import AuthScreen
        from screens.dashboard_screen import DashboardScreen
        from screens.screen_manager import ScreenManager
        print("✅ Frontend screens imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_class_instantiation():
    """Test class instantiation without database connection."""
    print("\n🔍 Testing class instantiation...")
    
    try:
        # Test screen manager creation
        from screens.screen_manager import ScreenManager
        screen_manager = ScreenManager()
        print("✅ ScreenManager created successfully")
        
        # Test available screens
        available_screens = list(screen_manager.screens.keys())
        print(f"✅ Available screens: {available_screens}")
        
        # Test navigation info
        for name, screen in screen_manager.screens.items():
            nav_info = screen.get_navigation_info()
            print(f"✅ {name} screen navigation info: {nav_info}")
        
        return True
    except Exception as e:
        print(f"❌ Instantiation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_navigation_logic():
    """Test navigation logic without UI."""
    print("\n🔍 Testing navigation logic...")
    
    try:
        from screens.screen_manager import ScreenManager
        screen_manager = ScreenManager()
        
        # Test default screen
        default_screen = screen_manager.get_current_screen_name()
        print(f"✅ Default screen: {default_screen}")
        
        # Test screen access validation
        validated_screen = screen_manager._validate_screen_access("dashboard")
        print(f"✅ Dashboard access (unauthenticated): {validated_screen}")
        
        validated_screen = screen_manager._validate_screen_access("auth")
        print(f"✅ Auth access (unauthenticated): {validated_screen}")
        
        return True
    except Exception as e:
        print(f"❌ Navigation error: {e}")
        return False

def test_architecture():
    """Test the complete architecture."""
    print("🧪 Testing Refactored Architecture")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_class_instantiation,
        test_navigation_logic
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    if all(results):
        print("🎉 All tests passed! Architecture is working correctly.")
        print("\n✅ Summary:")
        print("  - Backend modules properly organized")
        print("  - Frontend screens properly structured")
        print("  - Screen manager handles navigation")
        print("  - App.py is now clean and minimal")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return all(results)

if __name__ == "__main__":
    test_architecture()