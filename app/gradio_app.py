import asyncio
import os

import nest_asyncio
from dotenv import load_dotenv

from .ui.gradio_interface import GradioInterface

# Allow nested event loops for Jupyter compatibility
nest_asyncio.apply()

# Load environment variables
load_dotenv()


async def main():
    """Main function to launch the Gradio interface"""
    print("🚀 Starting Alpha Agents - Visa Checker & Browser Automation")
    print("📋 Loading environment variables...")

    # Check for required environment variables
    required_vars = ["OPENROUTER_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"⚠️  Warning: Missing environment variables: {missing_vars}")
        print("Some features may not work properly.")

    # Initialize and launch the interface
    interface = GradioInterface()

    print("🌐 Launching Gradio interface...")
    print("📱 You can access the interface at: http://localhost:7860")
    print("🔄 Press Ctrl+C to stop the server")

    try:
        await interface.launch(share=False, server_port=7860)
    except KeyboardInterrupt:
        print("\n👋 Shutting down Alpha Agents...")
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
