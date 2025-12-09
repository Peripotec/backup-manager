import React from 'react';
import { FileText, Download, AlertTriangle, CheckCircle } from 'lucide-react';

const History = () => {
    return (
        <div className="space-y-6">
            <div className="bg-white rounded-lg shadow overflow-hidden">
                <div className="p-4 border-b border-gray-200">
                    <h2 className="text-lg font-semibold">Últimos Backups</h2>
                </div>
                <div className="divide-y divide-gray-200">
                    {[1, 2, 3, 4, 5].map((i) => (
                        <div key={i} className="p-4 hover:bg-gray-50 flex items-center justify-between">
                            <div className="flex items-center gap-4">
                                <div className={`p-2 rounded-full ${i === 2 ? 'bg-red-100 text-red-600' : 'bg-green-100 text-green-600'}`}>
                                    {i === 2 ? <AlertTriangle size={20} /> : <CheckCircle size={20} />}
                                </div>
                                <div>
                                    <p className="font-medium text-gray-900">Huawei-Core-Switch-0{i}</p>
                                    <p className="text-sm text-gray-500">2023-10-25 03:00:{10 + i} AM</p>
                                </div>
                            </div>

                            <div className="flex items-center gap-3">
                                {i === 2 ? (
                                    <span className="text-sm text-red-600 bg-red-50 px-3 py-1 rounded-full">
                                        Error de Conexión
                                    </span>
                                ) : (
                                    <span className="text-sm text-gray-500">245 KB</span>
                                )}

                                <button className="p-2 text-gray-400 hover:text-blue-600 transition-colors" title="Ver Log">
                                    <FileText size={18} />
                                </button>
                                {i !== 2 && (
                                    <button className="p-2 text-gray-400 hover:text-green-600 transition-colors" title="Descargar Config">
                                        <Download size={18} />
                                    </button>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default History;
