from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.mission import MissionCreate, MissionResponse
from app.models.mission import Mission
from app.api.deps import get_db, get_current_user
from app.models.user import User
from datetime import datetime

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

    db_mission = Mission(
        title=mission.title,
        description=mission.description,
        difficulty=mission.difficulty,
        urgency=mission.urgency,
        xp=xp,
        due_date=mission.due_date,  # 👈 AQUI
        owner_id=1
    )

    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)

    return db_mission

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

    # marcar como concluída
    mission.completed = True

    # pegar usuário (temporário por username)
    user = db.query(User).filter(User.username == current_user).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    xp_final = mission.xp

    # ⏱ penalidade por atraso
    if mission.due_date and datetime.utcnow() > mission.due_date:
        xp_final = int(xp_final * 0.5)

    # 👍 validação comunitária
    xp_final = int(xp_final * (mission.approved_percentage / 100))

    user.xp += xp_final

    db.commit()

    return {
        "message": "Missão concluída",
        "xp_ganho": mission.xp,
        "xp_total": user.xp
    }