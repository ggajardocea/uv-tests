#!/usr/bin/env python3
"""
Simple test to verify Pydantic v2 syntax works
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict

# Test basic model
class TestUser(BaseModel):
    name: str = Field(..., description="User name")
    age: int = Field(..., ge=0, le=120)
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if len(v) < 2:
            raise ValueError('Name must be at least 2 characters')
        return v.title()

# Test configuration
class TestConfig(BaseModel):
    debug: bool = Field(default=False)
    api_key: str = Field(..., description="API key")
    
    model_config = ConfigDict(
        env_prefix = "TEST_"
    )

def test_basic_validation():
    """Test basic validation works"""
    try:
        user = TestUser(name="john", age=25)
        print(f"✅ User created: {user.name} (age: {user.age})")
        return True
    except Exception as e:
        print(f"❌ User creation failed: {e}")
        return False

def test_name_validation():
    """Test custom validator works"""
    try:
        # This should fail
        user = TestUser(name="a", age=25)
        print(f"❌ Should have failed for short name: {user.name}")
        return False
    except ValueError as e:
        print(f"✅ Name validation caught error: {e}")
        return True

def test_config():
    """Test configuration works"""
    try:
        config = TestConfig(api_key="test123")
        print(f"✅ Config created: debug={config.debug}, api_key={config.api_key[:4]}...")
        return True
    except Exception as e:
        print(f"❌ Config creation failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Pydantic v2 syntax...\n")
    
    tests = [
        test_basic_validation,
        test_name_validation,
        test_config
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Pydantic v2 syntax is working correctly.")
    else:
        print("❌ Some tests failed. Check the errors above.") 