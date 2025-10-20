from langchain.agents import Tool
from ..core.browser import get_browser

async def check_visa_availability(url: str = "https://www.eoiparis.gov.in/page/e-visa/") -> str:
    """Check visa slot availability on the Indian embassy website"""
    try:
        browser, page = await get_browser()
        await page.goto(url)
        content = await page.content()
        text_content = await page.inner_text("body")
        await browser.close()
        
        available = "Available" in content
        
        if available:
            return f"✅ VISA SLOTS AVAILABLE! Found availability on {url}"
        else:
            return f"❌ No visa slots currently available on {url}. Content preview: {text_content[:500]}..."
            
    except Exception as e:
        return f"❌ Error checking visa availability: {str(e)}"

visa_check_tool = Tool(
    name="check_visa_availability",
    func=check_visa_availability,
    description="Check visa slot availability on the Indian embassy website. Returns availability status and page content."
)
