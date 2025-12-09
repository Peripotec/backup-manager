import React, { useState } from 'react';
import { Plus, Search, Edit2, Trash2, HelpCircle, Loader } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import api from '../api/axios';

const Inventory = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const { data: devices, isLoading, isError } = useQuery({
        queryKey: ['devices'],
        queryFn: async () => {
            const response = await api.get('/devices/');
            return response.data;
        }
    });

    return (
        <div className="space-y-6">
            {/* Toolbar */}
            <div className="flex justify-between items-center">
                <div className="relative w-64">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
                    <input
                        type="text"
                        placeholder="Buscar equipo..."
                        className="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                    />
                </div>
                <button
                    onClick={() => setIsModalOpen(true)}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700 transition-colors"
                >
                    <Plus size={18} /> Nuevo Dispositivo
                </button>
            </div>

            {/* Table */}
            <div className="bg-white rounded-lg shadow overflow-hidden">
                {isLoading ? (
                    <div className="p-8 text-center text-gray-500 flex justify-center items-center gap-2">
                        <Loader className="animate-spin" size={20} /> Cargando inventario...
                    </div>
                ) : isError ? (
                    <div className="p-8 text-center text-red-500">
                        Error al cargar dispositivos. Verifique la conexión con el backend.
                    </div>
                ) : (
                    <table className="w-full">
                        <thead className="bg-gray-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">IP</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Vendor</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Protocolo</th>
                                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                            {devices?.length === 0 ? (
                                <tr>
                                    <td colSpan="5" className="px-6 py-4 text-center text-gray-500">
                                        No hay dispositivos registrados.
                                    </td>
                                </tr>
                            ) : (
                                devices?.map((device) => (
                                    <tr key={device.id} className="hover:bg-gray-50">
                                        <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">{device.name}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-gray-500">{device.ip_address}</td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">
                                                {device.vendor}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-gray-500">{device.protocol}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                            <button className="text-blue-600 hover:text-blue-900 mr-3"><Edit2 size={16} /></button>
                                            <button className="text-red-600 hover:text-red-900"><Trash2 size={16} /></button>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                )}
            </div>

            {/* Modal (Simplified) */}
            {isModalOpen && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
                    <div className="bg-white rounded-lg max-w-md w-full p-6">
                        <h2 className="text-xl font-bold mb-4">Nuevo Dispositivo</h2>
                        <form className="space-y-4">
                            <FormField label="Nombre" placeholder="ej. Switch-Core-01" help="Identificador único para el equipo." />
                            <FormField label="Dirección IP" placeholder="192.168.1.1" help="IP de gestión accesible desde el servidor." />
                            <div className="grid grid-cols-2 gap-4">
                                <FormField label="Vendor" placeholder="Huawei" help="Marca del equipo." />
                                <FormField label="Protocolo" placeholder="SSH" help="SSH es más seguro que Telnet." />
                            </div>
                            <div className="flex justify-end gap-3 mt-6">
                                <button
                                    type="button"
                                    onClick={() => setIsModalOpen(false)}
                                    className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
                                >
                                    Cancelar
                                </button>
                                <button
                                    type="button"
                                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                                >
                                    Guardar
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

const FormField = ({ label, placeholder, help }) => (
    <div>
        <label className="block text-sm font-medium text-gray-700 mb-1 flex items-center gap-2">
            {label}
            {help && (
                <div className="group relative">
                    <HelpCircle size={14} className="text-gray-400 cursor-help" />
                    <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-gray-800 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity w-48 text-center pointer-events-none">
                        {help}
                    </div>
                </div>
            )}
        </label>
        <input
            type="text"
            className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            placeholder={placeholder}
        />
    </div>
);

export default Inventory;
