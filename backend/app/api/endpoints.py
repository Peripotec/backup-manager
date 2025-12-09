from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.models import Device, DeviceCreate, DeviceRead, DeviceUpdate, Backup, BackupRead
from app.services.backup_service import get_backup_strategy
from app.services.diagnostic_service import DiagnosticService

router = APIRouter()

# --- Devices ---

@router.post("/devices/", response_model=DeviceRead)
def create_device(device: DeviceCreate, session: Session = Depends(get_session)):
    db_device = Device.from_orm(device)
    session.add(db_device)
    session.commit()
    session.refresh(db_device)
    return db_device

@router.get("/devices/", response_model=List[DeviceRead])
def read_devices(session: Session = Depends(get_session)):
    devices = session.exec(select(Device)).all()
    return devices

@router.get("/devices/{device_id}", response_model=DeviceRead)
def read_device(device_id: int, session: Session = Depends(get_session)):
    device = session.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.patch("/devices/{device_id}", response_model=DeviceRead)
def update_device(device_id: int, device: DeviceUpdate, session: Session = Depends(get_session)):
    db_device = session.get(Device, device_id)
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    device_data = device.dict(exclude_unset=True)
    for key, value in device_data.items():
        setattr(db_device, key, value)
    session.add(db_device)
    session.commit()
    session.refresh(db_device)
    return db_device

@router.delete("/devices/{device_id}")
def delete_device(device_id: int, session: Session = Depends(get_session)):
    device = session.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    session.delete(device)
    session.commit()
    return {"ok": True}

# --- Backups ---

@router.post("/backups/trigger/{device_id}")
def trigger_backup(device_id: int, session: Session = Depends(get_session)):
    device = session.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    strategy = get_backup_strategy(device.vendor)
    try:
        result = strategy.backup(device)
        # TODO: Guardar resultado en DB
        return {"status": "success", "detail": result}
    except Exception as e:
        # Ejecutar diagnóstico si falla
        is_alive = DiagnosticService.ping(device.ip_address)
        traceroute = DiagnosticService.traceroute(device.ip_address) if not is_alive else "N/A"
        return {
            "status": "failed", 
            "error": str(e),
            "diagnostic": {
                "ping": is_alive,
                "traceroute": traceroute
            }
        }

@router.get("/backups/", response_model=List[BackupRead])
def read_backups(session: Session = Depends(get_session)):
    backups = session.exec(select(Backup)).all()
    return backups
