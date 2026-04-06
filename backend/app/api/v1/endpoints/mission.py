from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.mission import MissionCreate, MissionResponse
from app.models.mission import Mission
from app.api.deps import get_db, get_current_user
from app.models.user import User
from datetime import datetime
from app.core.response import success_response

router = APIRouter()


# ✅ CRIAR MISSÃO
@router.post("/")
def create_mission(
    mission: MissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if mission.difficulty < 0 or mission.difficulty > 10:
        raise HTTPException(status_code=400, detail="Dificuldade deve ser 0-10")

    if mission.urgency < 0 or mission.urgency > 10:
        raise HTTPException(status_code=400, detail="Urgência deve ser 0-10")

    xp = mission.difficulty + mission.urgency

    db_mission = Mission(
        title=mission.title,
        description=mission.description,
        difficulty=mission.difficulty,
        urgency=mission.urgency,
        xp=xp,
        due_date=mission.due_date,
        completed=False,
        owner_id=current_user.id
    )

    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)

    return success_response(db_mission)


# ✅ CONCLUIR MISSÃO
@router.put("/{mission_id}/complete")
def complete_mission(
    mission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()

    if not mission:
        raise HTTPException(status_code=404, detail="Missão não encontrada")

    if mission.completed:
        raise HTTPException(status_code=400, detail="Missão já concluída")

    if mission.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    mission.completed = True
    mission.completed_at = datetime.utcnow()

    xp_final = mission.xp

    if mission.due_date and datetime.utcnow() > mission.due_date:
        xp_final = int(xp_final * 0.5)

    xp_final = int(xp_final * (mission.approved_percentage / 100))

    current_user.xp += xp_final

    db.commit()

    return success_response({
        "message": "Missão concluída",
        "xp_ganho": xp_final,
        "xp_total": current_user.xp
    })


# ✅ LISTAR TODAS MISSÕES DO USUÁRIO
@router.get("/")
def get_my_missions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    missions = db.query(Mission).filter(
        Mission.owner_id == current_user.id
    ).all()

    return success_response(missions)


# ✅ HISTÓRICO
@router.get("/history")
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    missions = db.query(Mission).filter(
        Mission.owner_id == current_user.id,
        Mission.completed == True
    ).all()

    return success_response(missions)


# ✅ ESTATÍSTICAS
@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    missions = db.query(Mission).filter(
        Mission.owner_id == current_user.id
    ).all()

    total = len(missions)
    completed = len([m for m in missions if m.completed])
    pending = total - completed

    return success_response({
        "total_missions": total,
        "completed": completed,
        "pending": pending,
        "xp_total": current_user.xp
    })


# ✅ MISSÕES PENDENTES
@router.get("/pending")
def get_pending_missions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    missions = db.query(Mission).filter(
        Mission.owner_id == current_user.id,
        Mission.completed == False
    ).all()

    return success_response(missions)


# ✅ MISSÕES CONCLUÍDAS
@router.get("/completed")
def get_completed_missions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    missions = db.query(Mission).filter(
        Mission.owner_id == current_user.id,
        Mission.completed == True
    ).all()

    return success_response(missions)