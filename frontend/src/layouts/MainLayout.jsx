import React, { useState } from 'react';
import { Outlet, useLocation, Link } from 'react-router-dom';
import { LayoutDashboard, Server, History, Settings, HelpCircle, Menu } from 'lucide-react';

const MainLayout = () => {
    const location = useLocation();
    const [showHelp, setShowHelp] = useState(true);

    const getPageTitle = () => {
        switch (location.pathname) {
            case '/': return 'Dashboard';
            case '/inventory': return 'Inventario de Equipos';
            case '/history': return 'Historial de Backups';
            case '/settings': return 'Configuración';
            default: return 'Backup Manager';
        }
    };

    const getHelpContent = () => {
        switch (location.pathname) {
            case '/':
                return (
                    <div>
                        <h3 className="font-bold mb-2">Resumen General</h3>
                        <p className="text-sm text-gray-600">Aquí puede ver el estado actual del sistema. Los gráficos muestran el éxito/fallo de los últimos backups.</p>
                    </div>
                );
            case '/inventory':
                return (
                    <div>
                        <h3 className="font-bold mb-2">Gestión de Equipos</h3>
                        <p className="text-sm text-gray-600 mb-2">Agregue aquí los routers y switches que desea respaldar.</p>
                        <ul className="list-disc list-inside text-xs text-gray-500">
                            <li>Use <strong>SSH</strong> siempre que sea posible.</li>
                            <li>El <strong>Vendor</strong> define los comandos que se enviarán.</li>
                        </ul>
                    </div>
                );
            default: return <p className="text-sm text-gray-600">Seleccione una sección para ver ayuda contextual.</p>;
        }
    };

    return (
        <div className="flex h-screen bg-gray-100">
            {/* Sidebar */}
            <aside className="w-64 bg-slate-800 text-white flex flex-col">
                <div className="p-4 font-bold text-xl flex items-center gap-2">
                    <Server className="text-blue-400" /> BackupMgr
                </div>
                <nav className="flex-1 p-4 space-y-2">
                    <NavLink to="/" icon={<LayoutDashboard size={20} />} label="Dashboard" active={location.pathname === '/'} />
                    <NavLink to="/inventory" icon={<Server size={20} />} label="Inventario" active={location.pathname === '/inventory'} />
                    <NavLink to="/history" icon={<History size={20} />} label="Historial" active={location.pathname === '/history'} />
                    <NavLink to="/settings" icon={<Settings size={20} />} label="Configuración" active={location.pathname === '/settings'} />
                </nav>
                <div className="p-4 border-t border-slate-700">
                    <button
                        onClick={() => setShowHelp(!showHelp)}
                        className="flex items-center gap-2 text-sm text-slate-400 hover:text-white transition-colors"
                    >
                        <HelpCircle size={16} /> {showHelp ? 'Ocultar Ayuda' : 'Mostrar Ayuda'}
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col overflow-hidden">
                <header className="bg-white shadow-sm p-4 flex justify-between items-center">
                    <h1 className="text-xl font-semibold text-gray-800">{getPageTitle()}</h1>
                </header>

                <div className="flex-1 flex overflow-hidden">
                    <div className="flex-1 overflow-auto p-6">
                        <Outlet />
                    </div>

                    {/* Contextual Help Panel */}
                    {showHelp && (
                        <div className="w-64 bg-white border-l border-gray-200 p-4 shadow-lg hidden lg:block">
                            <div className="flex items-center gap-2 text-blue-600 mb-4">
                                <HelpCircle size={20} />
                                <h2 className="font-semibold">Ayuda Contextual</h2>
                            </div>
                            {getHelpContent()}
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
};

const NavLink = ({ to, icon, label, active }) => (
    <Link
        to={to}
        className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${active ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-700'
            }`}
    >
        {icon}
        <span>{label}</span>
    </Link>
);

export default MainLayout;
