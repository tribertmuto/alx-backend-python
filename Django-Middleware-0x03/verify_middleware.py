#!/usr/bin/env python3
"""
Script to verify middleware configuration in Django-Middleware-0x03
"""

import os
import sys
from pathlib import Path

def check_middleware_configuration():
    """Check if middleware is properly configured."""
    
    project_root = Path(__file__).parent
    
    # Check if settings.py exists
    settings_path = project_root / "settings.py"
    
    print("🔍 Checking middleware configuration...")
    
    # Check settings.py at root level
    if settings_path.exists():
        print(f"✅ settings.py exists at root level: {settings_path}")
        
        # Check if middleware is configured
        with open(settings_path, 'r') as f:
            content = f.read()
            
            # Check for all required middleware
            required_middleware = [
                'chats.middleware.RequestLoggingMiddleware',
                'chats.middleware.RestrictAccessByTimeMiddleware',
                'chats.middleware.OffensiveLanguageMiddleware',
                'chats.middleware.RolepermissionMiddleware'
            ]
            
            missing_middleware = []
            for middleware in required_middleware:
                if middleware in content:
                    print(f"✅ {middleware} is configured")
                else:
                    print(f"❌ {middleware} is missing")
                    missing_middleware.append(middleware)
            
            if not missing_middleware:
                print("\n🎉 All middleware are properly configured!")
                return True
            else:
                print(f"\n⚠️  Missing middleware: {missing_middleware}")
                return False
    else:
        print(f"❌ settings.py does not exist at root level: {settings_path}")
        return False

if __name__ == "__main__":
    check_middleware_configuration()
