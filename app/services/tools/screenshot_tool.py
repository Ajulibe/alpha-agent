import os
from datetime import datetime
from langchain.agents import Tool
from ..tools.browser_tools import BrowserToolsService

# Global browser service instance
browser_service = BrowserToolsService()

async def take_screenshot(filename: str = None) -> str:
    """Take a screenshot of the current browser page"""
    try:
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        # Ensure the screenshots directory exists
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        
        full_path = os.path.join(screenshots_dir, filename)
        
        # Initialize browser if needed
        await browser_service.initialize()
        
        # Take screenshot
        result = await browser_service.take_screenshot(full_path)
        
        return f"✅ Screenshot saved: {full_path}"
        
    except Exception as e:
        return f"❌ Error taking screenshot: {str(e)}"

screenshot_tool = Tool(
    name="take_screenshot",
    func=take_screenshot,
    description="Take a screenshot of the current browser page. Optional parameter: filename (default: auto-generated timestamp)"
)
