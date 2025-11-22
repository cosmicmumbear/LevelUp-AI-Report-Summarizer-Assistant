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
from azure.cognitiveservices.vision.customvision.training import (
    CustomVisionTrainingClient,
)



from msrest.authentication import CognitiveServicesCredentials, ApiKeyCredentials

# Load environment variables from .env file
load_dotenv()


class AzureConfig:
    """
    Centralized configuration for Azure Cognitive Services

    AI-102 Best Practice: Keep credentials secure and separate from code
    """

    # Computer Vision Configuration (Tasks 1 & 2)
    VISION_ENDPOINT = os.getenv("VISION_ENDPOINT") or os.getenv("AZURE_VISION_ENDPOINT")
    VISION_KEY = os.getenv("VISION_KEY") or os.getenv("AZURE_VISION_KEY")



    # version for summarizer.py
    # version for data_interpreter.py
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    
    AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
    AZURE_OPENAI_API_KEY= os.getenv("AZURE_OPENAI_KEY")
    OPENAI_API_KEY= os.getenv("AZURE_OPENAI_KEY")

    OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_VERSION")
    API_VERSION = os.getenv("AZURE_OPENAI_VERSION")

    DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    AZURE_OPENAI_DEPLOYMENT_NAME= os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")



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
        if not AzureConfig.VISION_ENDPOINT.startswith("https://"):
            raise ValueError("VISION_ENDPOINT must start with https://")

        print("✓ Computer Vision configuration validated")
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

        if not AzureConfig.VISION_ENDPOINT or not AzureConfig.VISION_KEY:
            raise ValueError("Missing keys VISION in .env file!")

        credentials = CognitiveServicesCredentials(AzureConfig.VISION_KEY)
        client = ComputerVisionClient(AzureConfig.VISION_ENDPOINT, credentials)

        print(
            f"✓ Computer Vision client initialized (Endpoint: {AzureConfig.VISION_ENDPOINT})"
        )

        return client

    
    


# AI-102 Best Practice: Configuration constants
class ImageConfig:
    """Image processing configuration constants"""

    # Supported image formats (AI-102 Exam Topic)
    SUPPORTED_FORMATS = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

    # Maximum image size (AI-102 Limitation)
    MAX_IMAGE_SIZE_MB = 4  # For Custom Vision
    MAX_IMAGE_SIZE_MB_VISION = 50  # For Computer Vision

    # OCR language codes (AI-102 Multi-language support)
    SUPPORTED_OCR_LANGUAGES = {
        "pl": "Polish",
        "en": "English",
        "de": "German",
        "fr": "French",
        "es": "Spanish",
        "it": "Italian",
    }





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
        print(
            """
VISION_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
VISION_KEY=your-key


        """
        )
