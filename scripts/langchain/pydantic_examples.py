import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional
from datetime import datetime

# Load environment variables
load_dotenv()

# Example 1: Basic Pydantic Model
class User(BaseModel):
    name: str = Field(..., description="User's full name")
    email: str = Field(..., description="User's email address")
    age: int = Field(..., ge=0, le=120, description="User's age")
    is_active: bool = Field(default=True, description="Whether user is active")

# Example 2: Nested Models
class Address(BaseModel):
    street: str = Field(..., description="Street address")
    city: str = Field(..., description="City name")
    country: str = Field(..., description="Country name")
    postal_code: str = Field(..., description="Postal/ZIP code")

class Company(BaseModel):
    name: str = Field(..., description="Company name")
    industry: str = Field(..., description="Industry sector")
    founded_year: int = Field(..., ge=1800, le=datetime.now().year)
    address: Address = Field(..., description="Company address")

# Example 3: Advanced Validation with Custom Validators
class Product(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0, description="Product price in USD")
    category: str = Field(..., description="Product category")
    tags: List[str] = Field(default=[], description="Product tags")
    
    @field_validator('name')
    @classmethod
    def name_must_be_title_case(cls, v):
        if not v.istitle():
            raise ValueError('Name must be in title case')
        return v
    
    @field_validator('tags')
    @classmethod
    def tags_must_be_unique(cls, v):
        if len(v) != len(set(v)):
            raise ValueError('Tags must be unique')
        return v

# Example 4: LangChain Integration - Structured AI Output
class CodeReview(BaseModel):
    score: int = Field(..., ge=1, le=10, description="Code quality score (1-10)")
    issues: List[str] = Field(..., description="List of code issues found")
    suggestions: List[str] = Field(..., description="Improvement suggestions")
    complexity: str = Field(..., description="Code complexity level")
    estimated_fix_time: str = Field(..., description="Estimated time to fix issues")

# Example 5: Configuration Management
class AppConfig(BaseModel):
    debug: bool = Field(default=False, description="Enable debug mode")
    api_key: str = Field(..., description="API key for external service")
    max_retries: int = Field(default=3, ge=1, le=10, description="Maximum retry attempts")
    timeout: float = Field(default=30.0, gt=0, description="Request timeout in seconds")
    
    model_config = ConfigDict(
        env_file = ".env",  # Load from .env file
        env_prefix = "APP_"  # Look for APP_ prefixed variables
    )

# Example 6: Data Transformation
class DataPoint(BaseModel):
    timestamp: datetime = Field(..., description="Data collection timestamp")
    value: float = Field(..., description="Measured value")
    unit: str = Field(..., description="Unit of measurement")
    
    def to_dict(self):
        """Convert to dictionary format"""
        return {
            "time": self.timestamp.isoformat(),
            "value": self.value,
            "unit": self.unit
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary format"""
        return cls(
            timestamp=datetime.fromisoformat(data["time"]),
            value=data["value"],
            unit=data["unit"]
        )

# Example 7: Error Handling and Validation
def demonstrate_validation():
    """Show how Pydantic handles validation errors"""
    print("=== Pydantic Validation Examples ===\n")
    
    # Valid data
    try:
        user = User(
            name="John Doe",
            email="john@example.com",
            age=30
        )
        print(f"✅ Valid user created: {user.name}")
    except Exception as e:
        print(f"❌ User creation failed: {e}")
    
    # Invalid data
    try:
        invalid_user = User(
            name="",  # Empty name
            email="invalid-email",  # Invalid email format
            age=150  # Age too high
        )
    except Exception as e:
        print(f"❌ Invalid user caught: {e}")
    
    # Nested validation
    try:
        company = Company(
            name="Tech Corp",
            industry="Technology",
            founded_year=2020,
            address=Address(
                street="123 Main St",
                city="San Francisco",
                country="USA",
                postal_code="94105"
            )
        )
        print(f"✅ Company created: {company.name} in {company.address.city}")
    except Exception as e:
        print(f"❌ Company creation failed: {e}")
    
    # Product validation
    try:
        product = Product(
            name="Python Book",  # Should be "Python Book" (title case)
            price=29.99,
            category="Education",
            tags=["python", "programming", "python"]  # Duplicate tag
        )
    except Exception as e:
        print(f"❌ Product validation failed: {e}")

# Example 8: LangChain Output Parser Integration
def demonstrate_langchain_integration():
    """Show how Pydantic integrates with LangChain"""
    print("\n=== LangChain Integration Example ===\n")
    
    try:
        from langchain_core.output_parsers import PydanticOutputParser
        
        # Create parser for our CodeReview model
        parser = PydanticOutputParser(pydantic_object=CodeReview)
        
        # Get format instructions
        format_instructions = parser.get_format_instructions()
        print("Format instructions for AI:")
        print(format_instructions)
        
        # Example of what the AI should return
        example_output = {
            "score": 7,
            "issues": ["Missing error handling", "No input validation"],
            "suggestions": ["Add try-catch blocks", "Validate user input"],
            "complexity": "Medium",
            "estimated_fix_time": "2-3 hours"
        }
        
        # Parse the AI's response
        # Note: In real usage, you'd get this from the AI response
        # For demo purposes, we're using a dict directly
        parsed_review = CodeReview(**example_output)
        print(f"\n✅ Parsed review score: {parsed_review.score}")
        print(f"   Issues found: {len(parsed_review.issues)}")
        
    except ImportError:
        print("LangChain not available, but Pydantic models are ready!")

# Example 9: Configuration from Environment
def demonstrate_config_management():
    """Show configuration management with Pydantic"""
    print("\n=== Configuration Management Example ===\n")
    
    # Set some environment variables for demonstration
    os.environ["APP_DEBUG"] = "true"
    os.environ["APP_API_KEY"] = "demo_key_123"
    os.environ["APP_MAX_RETRIES"] = "5"
    
    try:
        config = AppConfig(api_key="required_key")
        print(f"✅ Config loaded:")
        print(f"   Debug mode: {config.debug}")
        print(f"   Max retries: {config.max_retries}")
        print(f"   Timeout: {config.timeout}s")
    except Exception as e:
        print(f"❌ Config loading failed: {e}")

if __name__ == "__main__":
    print("Pydantic Examples and Use Cases\n")
    
    # Run examples
    demonstrate_validation()
    demonstrate_langchain_integration()
    demonstrate_config_management()
    
    print("\n=== Pydantic Benefits Summary ===")
    print("✅ Type safety and validation")
    print("✅ Automatic data conversion")
    print("✅ Clear error messages")
    print("✅ IDE support and autocomplete")
    print("✅ Easy serialization/deserialization")
    print("✅ Integration with LangChain")
    print("✅ Configuration management")
    print("✅ Nested data structures")
    print("✅ Custom validators")
    print("✅ Environment variable support") 