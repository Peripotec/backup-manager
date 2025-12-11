from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.catalog import Vendor, DeviceModel, BackupTemplate

router = APIRouter()

# --- Vendors ---

@router.post("/vendors/", response_model=Vendor)
def create_vendor(vendor: Vendor, session: Session = Depends(get_session)):
    session.add(vendor)
    session.commit()
    session.refresh(vendor)
    return vendor

@router.get("/vendors/", response_model=List[Vendor])
def read_vendors(session: Session = Depends(get_session)):
    return session.exec(select(Vendor)).all()

@router.delete("/vendors/{vendor_id}")
def delete_vendor(vendor_id: int, session: Session = Depends(get_session)):
    vendor = session.get(Vendor, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    session.delete(vendor)
    session.commit()
    return {"ok": True}

# --- Device Models ---

@router.post("/models/", response_model=DeviceModel)
def create_model(model: DeviceModel, session: Session = Depends(get_session)):
    session.add(model)
    session.commit()
    session.refresh(model)
    return model

@router.get("/models/", response_model=List[DeviceModel])
def read_models(vendor_id: Optional[int] = None, session: Session = Depends(get_session)):
    query = select(DeviceModel)
    if vendor_id:
        query = query.where(DeviceModel.vendor_id == vendor_id)
    return session.exec(query).all()

# --- Templates ---

@router.post("/templates/", response_model=BackupTemplate)
def create_template(template: BackupTemplate, session: Session = Depends(get_session)):
    session.add(template)
    session.commit()
    session.refresh(template)
    return template

@router.get("/templates/", response_model=List[BackupTemplate])
def read_templates(vendor_id: Optional[int] = None, session: Session = Depends(get_session)):
    query = select(BackupTemplate)
    if vendor_id:
        query = query.where(BackupTemplate.vendor_id == vendor_id)
    return session.exec(query).all()

@router.delete("/templates/{template_id}")
def delete_template(template_id: int, session: Session = Depends(get_session)):
    template = session.get(BackupTemplate, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    session.delete(template)
    session.commit()
    return {"ok": True}
