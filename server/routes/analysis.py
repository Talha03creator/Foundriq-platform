from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from server.database import get_db
from server.models.project import Project
from server.models.report import Report
from server.models.user import User
from server.auth.security import get_current_user
from server.services.ai_service import analyze_business, generate_strategy

router = APIRouter(prefix="/api/analysis", tags=["Analysis"])


@router.post("/{project_id}")
async def run_analysis(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Get project
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.user_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Run AI analysis
    analysis = await analyze_business(
        business_idea=project.business_idea,
        target_market=project.target_market,
        budget=project.budget or 50000,
        pricing_model=project.pricing_model or "Not specified",
        competitors=project.competitors or "Not specified",
    )

    # Delete old report if exists
    old = await db.execute(select(Report).where(Report.project_id == project.id))
    for r in old.scalars().all():
        await db.delete(r)

    # Save new report
    report = Report(
        project_id=project.id,
        validation_score=analysis.get("validation_score"),
        competition_score=analysis.get("competition_score"),
        risk_level=analysis.get("risk_level"),
        swot=analysis.get("swot"),
        revenue_forecast=analysis.get("revenue_forecast"),
        strategy_steps=analysis.get("strategy_steps"),
        break_even=analysis.get("break_even"),
        full_report=analysis,
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)

    return {
        "id": report.id,
        "project_id": project.id,
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


@router.get("/{project_id}")
async def get_analysis(
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

    rr = await db.execute(select(Report).where(Report.project_id == project.id))
    report = rr.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="No analysis report found. Run analysis first.")

    return {
        "id": report.id,
        "project_id": project.id,
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


@router.post("/{project_id}/strategy")
async def run_strategy(
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

    strategy = await generate_strategy(
        business_idea=project.business_idea,
        target_market=project.target_market,
    )
    return strategy


