import subprocess
import platform

class DiagnosticService:
    @staticmethod
    def ping(host: str, count: int = 4) -> bool:
        """
        Ejecuta un ping al host. Devuelve True si responde, False si no.
        """
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, str(count), host]
        
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.returncode == 0
        except Exception:
            return False

    @staticmethod
    def traceroute(host: str) -> str:
        """
        Ejecuta traceroute (o tracert en Windows) y devuelve la salida.
        """
        cmd = 'tracert' if platform.system().lower() == 'windows' else 'traceroute'
        try:
            result = subprocess.run([cmd, host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout
        except Exception as e:
            return f"Error ejecutando traceroute: {str(e)}"
