from typing import Optional, List, Dict
from sqlmodel import Field, SQLModel, Relationship, JSON
from app.models.models import ProtocolEnum

class Vendor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    code: str = Field(index=True, unique=True)  # e.g., 'huawei', 'cisco'
    
    models: List["DeviceModel"] = Relationship(back_populates="vendor")

class DeviceModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    vendor_id: int = Field(foreign_key="vendor.id")
    
    vendor: Vendor = Relationship(back_populates="models")
    templates: List["BackupTemplate"] = Relationship(back_populates="device_model")

class BackupTemplate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    vendor_id: int = Field(foreign_key="vendor.id")
    device_model_id: Optional[int] = Field(default=None, foreign_key="devicemodel.id") # Optional if generic for vendor
    
    protocol: ProtocolEnum = ProtocolEnum.SSH
    commands: List[str] = Field(sa_type=JSON) # List of commands to execute
    
    device_model: Optional[DeviceModel] = Relationship(back_populates="templates")
