import React from 'react';
import { Save } from 'lucide-react';

const Settings = () => {
    return (
        <div className="max-w-2xl mx-auto space-y-8">
            <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-lg font-semibold mb-6 pb-2 border-b">Configuración de Correo (SMTP)</h2>
                <form className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Servidor SMTP</label>
                            <input type="text" className="w-full px-3 py-2 border rounded-lg" placeholder="smtp.gmail.com" />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Puerto</label>
                            <input type="number" className="w-full px-3 py-2 border rounded-lg" placeholder="587" />
                        </div>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Usuario</label>
                        <input type="email" className="w-full px-3 py-2 border rounded-lg" placeholder="notificaciones@empresa.com" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Contraseña</label>
                        <input type="password" className="w-full px-3 py-2 border rounded-lg" placeholder="••••••••" />
                    </div>
                </form>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-lg font-semibold mb-6 pb-2 border-b">Programación y Retención</h2>
                <form className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Hora de Ejecución Diaria</label>
                        <input type="time" className="w-full px-3 py-2 border rounded-lg" defaultValue="03:00" />
                        <p className="text-xs text-gray-500 mt-1">Hora del servidor.</p>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Días de Retención</label>
                        <input type="number" className="w-full px-3 py-2 border rounded-lg" defaultValue="30" />
                        <p className="text-xs text-gray-500 mt-1">Los backups más antiguos se borrarán automáticamente, excepto el último de cada mes.</p>
                    </div>
                </form>
            </div>

            <div className="flex justify-end">
                <button className="bg-blue-600 text-white px-6 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700">
                    <Save size={18} /> Guardar Cambios
                </button>
            </div>
        </div>
    );
};

export default Settings;
