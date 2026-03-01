from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional, List
from api.database import get_db
from api.models.project import Project
from api.models.report import Report
from api.models.user import User
from api.auth.security import get_current_user

router = APIRouter(prefix="/api/projects", tags=["Projects"])


class ProjectCreate(BaseModel):
    business_idea: str
    target_market: str
    budget: Optional[float] = None
    pricing_model: Optional[str] = None
    competitors: Optional[str] = None


class ProjectUpdate(BaseModel):
    business_idea: Optional[str] = None
    target_market: Optional[str] = None
    budget: Optional[float] = None
    pricing_model: Optional[str] = None
    competitors: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    business_idea: str
    target_market: str
    budget: Optional[float]
    pricing_model: Optional[str]
    competitors: Optional[str]
    created_at: str
    report: Optional[dict] = None

    class Config:
        from_attributes = True


@router.post("", response_model=dict)
async def create_project(
    req: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = Project(
        user_id=current_user.id,
        business_idea=req.business_idea,
        target_market=req.target_market,
        budget=req.budget,
        pricing_model=req.pricing_model,
        competitors=req.competitors,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return {
        "id": project.id,
        "business_idea": project.business_idea,
        "target_market": project.target_market,
        "budget": project.budget,
        "pricing_model": project.pricing_model,
        "competitors": project.competitors,
        "created_at": str(project.created_at),
    }


@router.get("", response_model=List[dict])
async def list_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Project).where(Project.user_id == current_user.id).order_by(Project.created_at.desc())
    )
    projects = result.scalars().all()
    items = []
    for p in projects:
        # Check for report
        rr = await db.execute(select(Report).where(Report.project_id == p.id))
        report = rr.scalar_one_or_none()
        items.append({
            "id": p.id,
            "business_idea": p.business_idea,
            "target_market": p.target_market,
            "budget": p.budget,
            "pricing_model": p.pricing_model,
            "competitors": p.competitors,
            "created_at": str(p.created_at),
            "has_report": report is not None,
            "validation_score": report.validation_score if report else None,
            "risk_level": report.risk_level if report else None,
        })
    return items


@router.get("/{project_id}", response_model=dict)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.user_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get report if exists
    rr = await db.execute(select(Report).where(Report.project_id == project.id))
    report = rr.scalar_one_or_none()
    report_data = None
    if report:
        report_data = {
            "id": report.id,
            "validation_score": report.validation_score,
            "competition_score": report.competition_score,
            "risk_level": report.risk_level,
            "swot": report.swot,
            "revenue_forecast": report.revenue_forecast,
            "strategy_steps": report.strategy_steps,
            "break_even": report.break_even,
            "full_report": report.full_report,
            "created_at": str(report.created_at),
        }

    return {
        "id": project.id,
        "business_idea": project.business_idea,
        "target_market": project.target_market,
        "budget": project.budget,
        "pricing_model": project.pricing_model,
        "competitors": project.competitors,
        "created_at": str(project.created_at),
        "report": report_data,
    }


@router.put("/{project_id}", response_model=dict)
async def update_project(
    project_id: int,
    req: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.user_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if req.business_idea is not None:
        project.business_idea = req.business_idea
    if req.target_market is not None:
        project.target_market = req.target_market
    if req.budget is not None:
        project.budget = req.budget
    if req.pricing_model is not None:
        project.pricing_model = req.pricing_model
    if req.competitors is not None:
        project.competitors = req.competitors

    await db.commit()
    await db.refresh(project)
    return {"message": "Project updated", "id": project.id}


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.user_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Delete associated reports
    rr = await db.execute(select(Report).where(Report.project_id == project.id))
    for r in rr.scalars().all():
        await db.delete(r)

    await db.delete(project)
    await db.commit()
    return {"message": "Project deleted"}

