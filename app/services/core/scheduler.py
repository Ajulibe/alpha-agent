from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.services.agents.visa_checker_agent import VisaCheckerAgent

scheduler = AsyncIOScheduler()


def start_scheduler():
    agent = VisaCheckerAgent()
    scheduler.add_job(agent.run, "interval", minutes=30)
    scheduler.start()
