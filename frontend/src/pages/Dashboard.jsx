import React from 'react';
import { Activity, CheckCircle, XCircle, Clock } from 'lucide-react';

const Dashboard = () => {
    // Mock data - In real app, fetch from API
    const stats = {
        totalDevices: 12,
        lastBackupSuccess: 10,
        lastBackupFailed: 2,
        nextRun: '03:00 AM'
    };

    return (
        <div className="space-y-6">
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <StatCard
                    title="Total Equipos"
                    value={stats.totalDevices}
                    icon={<Activity className="text-blue-500" />}
                    color="bg-blue-50"
                />
                <StatCard
                    title="Backups Exitosos"
                    value={stats.lastBackupSuccess}
                    icon={<CheckCircle className="text-green-500" />}
                    color="bg-green-50"
                />
                <StatCard
                    title="Fallos Recientes"
                    value={stats.lastBackupFailed}
                    icon={<XCircle className="text-red-500" />}
                    color="bg-red-50"
                />
                <StatCard
                    title="Próxima Ejecución"
                    value={stats.nextRun}
                    icon={<Clock className="text-purple-500" />}
                    color="bg-purple-50"
                />
            </div>

            {/* Recent Activity */}
            <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-lg font-semibold mb-4">Actividad Reciente</h2>
                <div className="space-y-4">
                    {[1, 2, 3].map((i) => (
                        <div key={i} className="flex items-center justify-between p-3 border-b last:border-0">
                            <div className="flex items-center gap-3">
                                <div className={`w-2 h-2 rounded-full ${i === 2 ? 'bg-red-500' : 'bg-green-500'}`} />
                                <div>
                                    <p className="font-medium">Core-Switch-{i}</p>
                                    <p className="text-xs text-gray-500">Huawei VRP • 192.168.1.{10 + i}</p>
                                </div>
                            </div>
                            <span className="text-sm text-gray-500">Hace {i * 10} min</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

const StatCard = ({ title, value, icon, color }) => (
    <div className="bg-white p-6 rounded-lg shadow flex items-center justify-between">
        <div>
            <p className="text-sm text-gray-500 mb-1">{title}</p>
            <p className="text-2xl font-bold text-gray-800">{value}</p>
        </div>
        <div className={`p-3 rounded-full ${color}`}>
            {icon}
        </div>
    </div>
);

export default Dashboard;
