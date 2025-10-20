from fastapi import APIRouter

from ..services.agents.visa_checker_agent import VisaCheckerAgent

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Alpha Agents are online!"}


@router.post("/check-visa")
async def check_visa_manual():
    agent = VisaCheckerAgent()
    result = await agent.run_manual()
    return {"result": result}
