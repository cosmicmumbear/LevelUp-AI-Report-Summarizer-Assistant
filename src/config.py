"""
Configuration Module for Azure Computer Vision Project
AI-102 Concept: Centralized configuration management for Azure Cognitive Services

This module handles:
- Environment variables loading
- Credentials management
- Client initialization
- Configuration validation
"""

import os
from dotenv import load_dotenv
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import CognitiveServicesCredentials, ApiKeyCredentials

# Load environment variables from .env file
load_dotenv()


class AzureConfig:
    """
    Centralized configuration for Azure Cognitive Services
    
    AI-102 Best Practice: Keep credentials secure and separate from code
    """
    
    # Computer Vision Configuration (Tasks 1 & 2)
    VISION_ENDPOINT = os.getenv('VISION_ENDPOINT')
    VISION_KEY = os.getenv('VISION_KEY')
    
    # Custom Vision Training Configuration (Task 3)
    CUSTOM_VISION_TRAINING_ENDPOINT = os.getenv('CUSTOM_VISION_TRAINING_ENDPOINT')
    CUSTOM_VISION_TRAINING_KEY = os.getenv('CUSTOM_VISION_TRAINING_KEY')
    
    # Custom Vision Prediction Configuration (Task 3)
    CUSTOM_VISION_PREDICTION_ENDPOINT = os.getenv('CUSTOM_VISION_PREDICTION_ENDPOINT')
    CUSTOM_VISION_PREDICTION_KEY = os.getenv('CUSTOM_VISION_PREDICTION_KEY')
    CUSTOM_VISION_PREDICTION_RESOURCE_ID = os.getenv('CUSTOM_VISION_PREDICTION_RESOURCE_ID')
    
    @staticmethod
    def validate_computer_vision_config():
        """
        Validate Computer Vision configuration
        
        AI-102 Exam Tip: Always validate credentials before making API calls
        """
        if not AzureConfig.VISION_ENDPOINT or not AzureConfig.VISION_KEY:
            raise ValueError(
                "Computer Vision credentials not found. "
                "Please set VISION_ENDPOINT and VISION_KEY in .env file."
            )
        
        # Validate endpoint format
        if not AzureConfig.VISION_ENDPOINT.startswith('https://'):
            raise ValueError("VISION_ENDPOINT must start with https://")
        
        print("✓ Computer Vision configuration validated")
        return True
    
    @staticmethod
    def validate_custom_vision_config():
        """
        Validate Custom Vision configuration
        
        AI-102 Note: Custom Vision requires separate Training and Prediction resources
        """
        required_vars = {
            'CUSTOM_VISION_TRAINING_ENDPOINT': AzureConfig.CUSTOM_VISION_TRAINING_ENDPOINT,
            'CUSTOM_VISION_TRAINING_KEY': AzureConfig.CUSTOM_VISION_TRAINING_KEY,
            'CUSTOM_VISION_PREDICTION_ENDPOINT': AzureConfig.CUSTOM_VISION_PREDICTION_ENDPOINT,
            'CUSTOM_VISION_PREDICTION_KEY': AzureConfig.CUSTOM_VISION_PREDICTION_KEY,
            'CUSTOM_VISION_PREDICTION_RESOURCE_ID': AzureConfig.CUSTOM_VISION_PREDICTION_RESOURCE_ID
        }
        
        missing_vars = [var for var, value in required_vars.items() if not value]
        
        if missing_vars:
            raise ValueError(
                f"Custom Vision credentials incomplete. Missing: {', '.join(missing_vars)}\n"
                "Please set all required variables in .env file."
            )
        
        print("✓ Custom Vision configuration validated")
        return True
    
    @staticmethod
    def get_computer_vision_client():
        """
        Initialize and return Computer Vision client
        
        AI-102 Pattern: Client initialization with key-based authentication
        
        Returns:
            ComputerVisionClient: Initialized client for Computer Vision API
        """
        AzureConfig.validate_computer_vision_config()
        
        # AI-102 Concept: CognitiveServicesCredentials for authentication
        credentials = CognitiveServicesCredentials(AzureConfig.VISION_KEY)
        client = ComputerVisionClient(AzureConfig.VISION_ENDPOINT, credentials)
        
        print(f"✓ Computer Vision client initialized (Endpoint: {AzureConfig.VISION_ENDPOINT})")
        return client
    
    @staticmethod
    def get_custom_vision_training_client():
        """
        Initialize and return Custom Vision Training client
        
        AI-102 Pattern: Separate clients for training and prediction
        
        Returns:
            CustomVisionTrainingClient: Client for training custom models
        """
        AzureConfig.validate_custom_vision_config()
        
        # AI-102 Concept: ApiKeyCredentials for Custom Vision
        credentials = ApiKeyCredentials(in_headers={"Training-key": AzureConfig.CUSTOM_VISION_TRAINING_KEY})
        client = CustomVisionTrainingClient(AzureConfig.CUSTOM_VISION_TRAINING_ENDPOINT, credentials)
        
        print(f"✓ Custom Vision Training client initialized")
        return client
    
    @staticmethod
    def get_custom_vision_prediction_client():
        """
        Initialize and return Custom Vision Prediction client
        
        Returns:
            CustomVisionPredictionClient: Client for making predictions
        """
        AzureConfig.validate_custom_vision_config()
        
        credentials = ApiKeyCredentials(in_headers={"Prediction-key": AzureConfig.CUSTOM_VISION_PREDICTION_KEY})
        client = CustomVisionPredictionClient(AzureConfig.CUSTOM_VISION_PREDICTION_ENDPOINT, credentials)
        
        print(f"✓ Custom Vision Prediction client initialized")
        return client


# AI-102 Best Practice: Configuration constants
class ImageConfig:
    """Image processing configuration constants"""
    
    # Supported image formats (AI-102 Exam Topic)
    SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    
    # Maximum image size (AI-102 Limitation)
    MAX_IMAGE_SIZE_MB = 4  # For Custom Vision
    MAX_IMAGE_SIZE_MB_VISION = 50  # For Computer Vision
    
    # OCR language codes (AI-102 Multi-language support)
    SUPPORTED_OCR_LANGUAGES = {
        'pl': 'Polish',
        'en': 'English',
        'de': 'German',
        'fr': 'French',
        'es': 'Spanish',
        'it': 'Italian'
    }


class CustomVisionConfig:
    """Custom Vision specific configuration"""
    
    # AI-102 Requirement: Minimum images per tag
    MIN_IMAGES_PER_TAG = 5
    RECOMMENDED_IMAGES_PER_TAG = 10
    
    # Training configuration
    MAX_TRAINING_ITERATIONS = 10
    TRAINING_TIMEOUT_MINUTES = 30
    
    # Prediction threshold (AI-102 Tuning concept)
    DEFAULT_PREDICTION_THRESHOLD = 0.5
    HIGH_CONFIDENCE_THRESHOLD = 0.8


# Utility functions
def check_configuration():
    """
    Check if all required configuration is present
    
    AI-102 Best Practice: Validate configuration at startup
    """
    print("\n=== Configuration Check ===\n")
    
    print("1. Computer Vision Configuration:")
    try:
        AzureConfig.validate_computer_vision_config()
    except ValueError as e:
        print(f"   ✗ Error: {e}")
        return False
    
    print("\n2. Custom Vision Configuration:")
    try:
        AzureConfig.validate_custom_vision_config()
    except ValueError as e:
        print(f"   ✗ Error: {e}")
        return False
    
    print("\n=== All configurations valid ===\n")
    return True


if __name__ == "__main__":
    """
    Run configuration check when module is executed directly
    """
    print("Azure Computer Vision Configuration Checker")
    print("=" * 50)
    
    if check_configuration():
        print("\n✓ Configuration is ready for use!")
        print("\nYou can now run:")
        print("  - python task1_image_analysis.py")
        print("  - python task2_ocr_processing.py")
        print("  - python task3_custom_vision.py")
    else:
        print("\n✗ Configuration incomplete. Please check .env file.")
        print("\nCreate .env file with:")
        print("""
VISION_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
VISION_KEY=your-key

CUSTOM_VISION_TRAINING_ENDPOINT=https://your-region.api.cognitive.microsoft.com/
CUSTOM_VISION_TRAINING_KEY=your-training-key

CUSTOM_VISION_PREDICTION_ENDPOINT=https://your-region.api.cognitive.microsoft.com/
CUSTOM_VISION_PREDICTION_KEY=your-prediction-key
CUSTOM_VISION_PREDICTION_RESOURCE_ID=/subscriptions/.../resourceGroups/.../providers/Microsoft.CognitiveServices/accounts/your-resource
        """)
