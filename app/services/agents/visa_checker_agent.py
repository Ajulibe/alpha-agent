from app.services.agents.base_agent import BaseAgent
from app.services.core.browser import get_browser
from app.services.core.email_service import send_email


class VisaCheckerAgent(BaseAgent):
    name = "visa_checker"

    async def run(self):
        """Run the visa checking process"""
        try:
            browser, page = await get_browser()
            await page.goto("https://www.eoiparis.gov.in/page/e-visa/")
            content = await page.content()

            available = "Available" in content  # crude check, can be improved
            await browser.close()

            if available:
                await self.notify("Visa booking slots are available!")
            else:
                print("No availability detected.")
        except (RuntimeError, ConnectionError) as e:
            print(f"Error checking visa availability: {str(e)}")

    async def run_manual(self):
        """Run manual visa check and return detailed results"""
        try:
            browser, page = await get_browser()
            await page.goto("https://www.eoiparis.gov.in/page/e-visa/")
            content = await page.content()

            # Extract text content for inspection
            text_content = await page.inner_text("body")
            await browser.close()

            available = "Available" in content

            return {
                "available": available,
                "page_content": text_content[:2000],
                "url": "https://www.eoiparis.gov.in/page/e-visa/",
            }
        except (RuntimeError, ConnectionError) as e:
            return {
                "available": False,
                "page_content": f"Error: {str(e)}",
                "url": "https://www.eoiparis.gov.in/page/e-visa/",
            }

    async def analyze(self, data):
        """Analyze scraped data using LangGraph or AI model"""
        # TODO: Implement LangGraph integration for intelligent analysis
        return {"status": "analysis_not_implemented", "data": data}

    async def notify(self, message: str):
        """Send email notification about visa availability"""
        try:
            await send_email(
                to="recipient@example.com",
                subject="Visa Slot Alert",
                body=message,
            )
        except (RuntimeError, ConnectionError) as e:
            print(f"Failed to send notification: {str(e)}")
