from sqlalchemy.orm import Session
from app.models.remote_command import RemoteCommand
from datetime import datetime

def resend_command(db: Session, kiosk_id: str):
    command = db.query(RemoteCommand).filter(
        RemoteCommand.kiosk_id == kiosk_id,
        RemoteCommand.status == "pending"
    ).first()

    if not command:
        return None

    # 명령어 전송 로직은 여기에 삽입 가능 (예: send_to_kiosk())
    command.received_at = datetime.utcnow().isoformat()
    db.commit()
    db.refresh(command)

    return command
