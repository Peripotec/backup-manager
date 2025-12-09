from abc import ABC, abstractmethod
from app.models.models import Device, ProtocolEnum
from netmiko import ConnectHandler
import logging
import os
from datetime import datetime

class BackupStrategy(ABC):
    @abstractmethod
    def backup(self, device: Device) -> str:
        """
        Realiza el backup y devuelve el contenido o la ruta del archivo.
        Lanza excepciones en caso de fallo.
        """
        pass

class NetmikoBackupStrategy(BackupStrategy):
    def __init__(self, device_type: str):
        self.device_type = device_type

    def backup(self, device: Device) -> str:
        device_params = {
            'device_type': self.device_type,
            'host': device.ip_address,
            'username': device.username,
            'password': device.password,
            'port': device.port,
        }
        
        # Determinación estricta del protocolo (SSH vs Telnet)
        # Esto asegura que se respete la configuración heredada de los scripts bash originales.
        if device.protocol == ProtocolEnum.TELNET:
            device_params['device_type'] += '_telnet'
            logging.info(f"Using TELNET for {device.name} (Legacy Mode)")
        else:
            logging.info(f"Using SSH for {device.name} (Secure Mode)")

        logging.info(f"Connecting to {device.name} ({device.ip_address})...")
        
        try:
            with ConnectHandler(**device_params) as net_connect:
                net_connect.enable()
                
                # NOTA DE DISEÑO:
                # Los scripts originales usaban TFTP para extraer 'vrpcfg.zip'.
                # El nuevo sistema usa captura de CLI ('display current-configuration') para obtener
                # el backup en texto plano. Esto permite:
                # 1. Visualización directa en la Web.
                # 2. Comparación de versiones (Diff).
                # 3. Independencia del servicio TFTP local.
                
                if 'huawei' in self.device_type:
                    # Equivalente moderno a extraer la config
                    output = net_connect.send_command("display current-configuration")
                elif 'cisco' in self.device_type:
                    output = net_connect.send_command("show running-config")
                else:
                    output = net_connect.send_command("show running-config")
                
                return self._save_to_file(device, output)
        except Exception as e:
            logging.error(f"Backup failed for {device.name}: {str(e)}")
            raise e

    def _save_to_file(self, device: Device, content: str) -> str:
        # Estructura: backups/{vendor}/{date}/{hostname}.cfg
        date_str = datetime.now().strftime("%Y-%m-%d")
        base_dir = f"backups/{device.vendor}/{date_str}"
        os.makedirs(base_dir, exist_ok=True)
        
        filename = f"{base_dir}/{device.name}.cfg"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        
        return filename

class HuaweiBackupStrategy(NetmikoBackupStrategy):
    def __init__(self):
        super().__init__('huawei')

class CiscoBackupStrategy(NetmikoBackupStrategy):
    def __init__(self):
        super().__init__('cisco_ios')

class GenericBackupStrategy(BackupStrategy):
    def backup(self, device: Device) -> str:
        raise NotImplementedError("Generic backup not implemented yet")

def get_backup_strategy(vendor: str) -> BackupStrategy:
    v = vendor.lower()
    if "huawei" in v:
        return HuaweiBackupStrategy()
    elif "cisco" in v:
        return CiscoBackupStrategy()
    return GenericBackupStrategy()
