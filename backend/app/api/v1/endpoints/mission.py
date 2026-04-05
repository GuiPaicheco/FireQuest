from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.mission import MissionCreate, MissionResponse
from app.models.mission import Mission
from app.api.deps import get_db, get_current_user
from app.models.user import User
from datetime import datetime
from app.models.user import User
from app.core.response import success_response

router = APIRouter()


@router.post("/", response_model=MissionResponse)
def create_mission(
    mission: MissionCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    # validação
    if mission.difficulty < 0 or mission.difficulty > 10:
        raise HTTPException(status_code=400, detail="Dificuldade deve ser 0-10")

    if mission.urgency < 0 or mission.urgency > 10:
        raise HTTPException(status_code=400, detail="Urgência deve ser 0-10")

    xp = mission.difficulty + mission.urgency
    user = db.query(User).filter(User.username == current_user).first()
    
    db_mission = Mission(
        title=mission.title,
        description=mission.description,
        difficulty=mission.difficulty,
        urgency=mission.urgency,
        xp=xp,
        due_date=mission.due_date,
        owner_id=user.id
    )

    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)

    return success_response(db_mission)

@router.put("/{mission_id}/complete")
def complete_mission(
    mission_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()

    if not mission:
        raise HTTPException(status_code=404, detail="Missão não encontrada")

    if mission.completed:
        raise HTTPException(status_code=400, detail="Missão já concluída")

    # pega usuário primeiro
    user = db.query(User).filter(User.username == current_user).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # valida dono da missão
    if mission.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    # arca como concluída
    mission.completed = True
    mission.completed_at = datetime.utcnow()

    # cálculo do xp
    xp_final = mission.xp

    if mission.due_date and datetime.utcnow() > mission.due_date:
        xp_final = int(xp_final * 0.5)

    xp_final = int(xp_final * (mission.approved_percentage / 100))

    user.xp += xp_final

    db.commit()

    return {
        "message": "Missão concluída",
        "xp_ganho": xp_final,
        "xp_total": user.xp
    }
    
@router.get("/")
def get_my_missions(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == current_user).first()

    missions = db.query(Mission).filter(Mission.owner_id == user.id).all()

    return missions

@router.get("/history")
def get_history(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == current_user).first()

    missions = db.query(Mission).filter(
        Mission.owner_id == user.id,
        Mission.completed == True
    ).all()

    return missions

@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == current_user).first()

    missions = db.query(Mission).filter(Mission.owner_id == user.id).all()

    total = len(missions)
    completed = len([m for m in missions if m.completed])
    pending = total - completed

    total_xp = user.xp

    return {
        "total_missions": total,
        "completed": completed,
        "pending": pending,
        "xp_total": total_xp
    }
    
@router.get("/pending")
def get_pending_missions(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == current_user).first()

    missions = db.query(Mission).filter(
        Mission.owner_id == user.id,
        Mission.completed == False
    ).all()

    return missions

@router.get("/completed")
def get_completed_missions(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == current_user).first()

    missions = db.query(Mission).filter(
        Mission.owner_id == user.id,
        Mission.completed == True
    ).all()

    return missions