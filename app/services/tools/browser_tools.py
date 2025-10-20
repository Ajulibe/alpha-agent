from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_async_playwright_browser


class BrowserToolsService:
    """Service for managing Playwright browser tools"""

    def __init__(self):
        self.async_browser = None
        self.toolkit = None
        self.tools = []

    async def initialize(self, headless: bool = True):
        """Initialize the browser and toolkit"""
        if self.async_browser is None:
            self.async_browser = create_async_playwright_browser(headless=headless)
            self.toolkit = PlayWrightBrowserToolkit.from_browser(
                async_browser=self.async_browser
            )
            self.tools = self.toolkit.get_tools()

    async def get_tools(self) -> list:
        """Get all browser tools"""
        if not self.tools:
            await self.initialize()
        return self.tools

    async def get_tool_by_name(self, name: str):
        """Get a specific tool by name"""
        tools = await self.get_tools()
        tool_dict = {tool.name: tool for tool in tools}
        return tool_dict.get(name)

    async def navigate_to_url(self, url: str) -> str:
        """Navigate to a URL and return status"""
        try:
            navigate_tool = await self.get_tool_by_name("navigate_browser")
            if navigate_tool:
                await navigate_tool.arun({"url": url})
                return f"Successfully navigated to {url}"
            else:
                raise RuntimeError("Navigate tool not available")
        except (TimeoutError, ConnectionError) as e:
            raise RuntimeError(f"Error navigating to {url}: {str(e)}") from e

    async def extract_page_text(self) -> str:
        """Extract text from current page"""
        try:
            extract_tool = await self.get_tool_by_name("extract_text")
            if extract_tool:
                text = await extract_tool.arun({})
                return text
            else:
                return "Extract text tool not available"
        except (AttributeError, RuntimeError) as e:
            return f"Error extracting text: {str(e)}"

    async def take_screenshot(self, filename: str = "screenshot.png") -> str:
        """Take a screenshot of the current page"""
        try:
            screenshot_tool = await self.get_tool_by_name("screenshot")
            if screenshot_tool:
                await screenshot_tool.arun({"filename": filename})
                return f"Screenshot saved as {filename}"
            else:
                # Fallback: use the browser directly
                if self.async_browser:
                    page = self.async_browser.get_current_page()
                    await page.screenshot(path=filename)
                    return f"Screenshot saved as {filename}"
                else:
                    return "Screenshot tool not available"
        except (RuntimeError, OSError) as e:
            return f"Error taking screenshot: {str(e)}"

    async def list_available_tools(self) -> list:
        """List all available browser tools"""
        tools = await self.get_tools()
        return [tool.name for tool in tools]

    async def close(self):
        """Close the browser"""
        if self.async_browser:
            await self.async_browser.close()
            self.async_browser = None
