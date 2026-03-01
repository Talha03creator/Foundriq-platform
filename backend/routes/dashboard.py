from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.database import get_db
from backend.models.project import Project
from backend.models.report import Report
from backend.models.user import User
from backend.auth.security import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("")
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Total projects
    result = await db.execute(
        select(func.count(Project.id)).where(Project.user_id == current_user.id)
    )
    total_projects = result.scalar() or 0

    # Average validation score
    result = await db.execute(
        select(func.avg(Report.validation_score)).join(
            Project, Report.project_id == Project.id
        ).where(Project.user_id == current_user.id)
    )
    avg_validation = round(result.scalar() or 0, 1)

    # Average competition score
    result = await db.execute(
        select(func.avg(Report.competition_score)).join(
            Project, Report.project_id == Project.id
        ).where(Project.user_id == current_user.id)
    )
    avg_competition = round(result.scalar() or 0, 1)

    # Recent projects
    result = await db.execute(
        select(Project).where(Project.user_id == current_user.id)
        .order_by(Project.created_at.desc()).limit(5)
    )
    recent = result.scalars().all()
    recent_projects = []
    for p in recent:
        rr = await db.execute(select(Report).where(Report.project_id == p.id))
        report = rr.scalar_one_or_none()
        recent_projects.append({
            "id": p.id,
            "business_idea": p.business_idea[:100],
            "target_market": p.target_market,
            "created_at": str(p.created_at),
            "validation_score": report.validation_score if report else None,
            "risk_level": report.risk_level if report else None,
        })

    # Risk distribution
    result = await db.execute(
        select(Report.risk_level, func.count(Report.id)).join(
            Project, Report.project_id == Project.id
        ).where(Project.user_id == current_user.id).group_by(Report.risk_level)
    )
    risk_dist = {row[0]: row[1] for row in result.all() if row[0]}

    return {
        "total_projects": total_projects,
        "avg_validation_score": avg_validation,
        "avg_competition_score": avg_competition,
        "total_reports": len([p for p in recent_projects if p["validation_score"] is not None]),
        "recent_projects": recent_projects,
        "risk_distribution": risk_dist,
        "user": {"id": current_user.id, "full_name": current_user.full_name, "email": current_user.email},
    }
