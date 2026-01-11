from app.domain.models.plan import Plan
from app.infrastructure.repositories.plan_repository import PlanRepository


class PlanService:
    def __init__(self, repo: PlanRepository):
        self.repo = repo

    async def list_plans(self) -> list[Plan]:
        return await self.repo.list_active()