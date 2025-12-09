from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum

class ProtocolEnum(str, Enum):
    SSH = "ssh"
    TELNET = "telnet"

class DeviceBase(SQLModel):
    name: str = Field(index=True, unique=True)
    ip_address: str = Field(index=True)
    vendor: str
    model: Optional[str] = None
    username: str
    password: str # In a real app, this should be encrypted
    protocol: ProtocolEnum = ProtocolEnum.SSH
    port: int = 22
    enabled: bool = True

class Device(DeviceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    backups: List["Backup"] = Relationship(back_populates="device")

class DeviceCreate(DeviceBase):
    pass

class DeviceRead(DeviceBase):
    id: int

class DeviceUpdate(SQLModel):
    name: Optional[str] = None
    ip_address: Optional[str] = None
    vendor: Optional[str] = None
    model: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    protocol: Optional[ProtocolEnum] = None
    port: Optional[int] = None
    enabled: Optional[bool] = None

class BackupStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"

class BackupBase(SQLModel):
    device_id: int = Field(foreign_key="device.id")
    timestamp: datetime = Field(default_factory=datetime.now)
    file_path: Optional[str] = None
    status: BackupStatus
    log_content: Optional[str] = None
    file_size: Optional[int] = 0

class Backup(BackupBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    device: Optional[Device] = Relationship(back_populates="backups")

class BackupRead(BackupBase):
    id: int
