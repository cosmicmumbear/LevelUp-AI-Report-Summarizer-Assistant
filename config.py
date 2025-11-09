"""
Configuration Module for Azure 

This module handles:
- Environment variables loading
- Credentials management
- Client initialization
- Configuration validation
"""


import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.identity import DefaultAzureCredential

# Set the value of your computer vision endpoint as environment variable:
try:
    endpoint = os.environ["VISION_ENDPOINT"]
except KeyError:
    print("Missing environment variable 'VISION_ENDPOINT'.")
    print("Set it before running this sample.")
    exit()

# Create an Image Analysis client for synchronous operations,
# using Entra ID authentication
client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
)