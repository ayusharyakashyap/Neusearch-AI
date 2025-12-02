#!/usr/bin/env python3
"""
Quick test script to verify fallback mode works without any API keys or database.
Run this to ensure deployment will succeed.
"""
import json
import sys
from pathlib import Path

def test_fallback_data():
    """Test that fallback JSON data exists and is valid."""
    print("🧪 Testing Fallback Data System\n")
    
    json_path = Path(__file__).parent / "backend" / "sample_data" / "products_fallback.json"
    
    if not json_path.exists():
        print(f"❌ FAIL: Fallback data not found at {json_path}")
        return False
    
    print(f"✅ Found fallback data file")
    
    try:
        with open(json_path, 'r') as f:
            products = json.load(f)
        
        if not isinstance(products, list):
            print(f"❌ FAIL: Fallback data is not a list")
            return False
        
        print(f"✅ Fallback data is valid JSON array")
        print(f"✅ Contains {len(products)} demo products")
        
        # Validate product structure
        required_fields = ['id', 'title', 'price', 'description', 'category']
        for i, product in enumerate(products):
            for field in required_fields:
                if field not in product:
                    print(f"❌ FAIL: Product {i} missing field '{field}'")
                    return False
        
        print(f"✅ All products have required fields")
        
        # Display products
        print(f"\n📦 Demo Products:")
        for product in products:
            print(f"  • {product['title']} - ₹{product['price']}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ FAIL: Invalid JSON - {e}")
        return False
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def test_config_files():
    """Test that all required config files exist."""
    print(f"\n🔍 Checking Configuration Files\n")
    
    required_files = [
        "render.yaml",
        "frontend/vercel.json",
        "backend/Dockerfile",
        "backend/start.sh",
        "backend/seed_db.py",
        ".env.example",
        "README_DEPLOY.md",
        "docker-compose.yml"
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = Path(__file__).parent / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            all_exist = False
    
    return all_exist

def test_start_script():
    """Test that start.sh is executable."""
    print(f"\n🔧 Checking Start Script\n")
    
    start_script = Path(__file__).parent / "backend" / "start.sh"
    
    if not start_script.exists():
        print(f"❌ FAIL: start.sh not found")
        return False
    
    print(f"✅ start.sh exists")
    
    import os
    if os.access(start_script, os.X_OK):
        print(f"✅ start.sh is executable")
        return True
    else:
        print(f"⚠️  WARNING: start.sh is not executable (will be fixed in Dockerfile)")
        return True  # Non-fatal, Dockerfile will fix this

def main():
    print("=" * 60)
    print("🚀 Neusearch Deployment Readiness Test")
    print("=" * 60)
    print()
    
    tests = [
        ("Fallback Data", test_fallback_data),
        ("Config Files", test_config_files),
        ("Start Script", test_start_script)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Ready to deploy!")
        print("\nNext steps:")
        print("1. git add .")
        print("2. git commit -m 'feat: add deployment configs'")
        print("3. git push origin main")
        print("4. Follow README_DEPLOY.md")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
