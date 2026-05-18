import React from 'react';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { GripVertical, Clock, CheckCircle, User } from 'lucide-react';
import { Service } from '../types';
import { cn } from '../lib/utils';
import { motion } from 'motion/react';

interface Props {
  service: Service;
  isManager: boolean;
  onComplete?: (id: string) => void;
}

export const SortableServiceItem = ({ service, isManager, onComplete }: Props) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({
    id: service.id,
    disabled: !isManager,
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  const formattedDate = service.createdAt?.toDate
    ? service.createdAt.toDate().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    : '...';

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={cn(
        "bg-white rounded-xl p-4 mb-3 transition-all duration-200 border",
        isDragging 
          ? "shadow-xl z-50 opacity-90 scale-[1.02] border-blue-200" 
          : "shadow-sm border-[#e5e5e5] hover:border-gray-300",
        "flex items-center gap-4 group"
      )}
    >
      {service.status === 'pending' && isManager && (
        <div
          {...attributes}
          {...listeners}
          className="cursor-grab active:cursor-grabbing text-[#94a3b8] hover:text-gray-900 transition-colors p-1"
          title="Arrastar para reordenar"
        >
          <GripVertical className="h-5 w-5" />
        </div>
      )}

      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1.5 text-[10px] font-bold uppercase tracking-wider">
          {service.status === 'pending' ? (
            <span className="text-[#64748b] bg-gray-100 px-2 py-0.5 rounded-full">
              Na Fila
            </span>
          ) : (
            <span className="text-[#166534] bg-[#dcfce7] px-2 py-0.5 rounded-full">
              Concluído
            </span>
          )}
        </div>
        <p className="text-[13px] font-medium text-[#1a1a1a] leading-relaxed">
          {service.description}
        </p>
        <div className="flex items-center gap-3 mt-2 text-[11px] text-[#94a3b8]">
          <span className="flex items-center gap-1">
            <Clock className="h-3 w-3" />
            Adicionado às {formattedDate}
          </span>
          {service.status === 'completed' && service.completedByEmail && (
            <span className="flex items-center gap-1">
              <User className="h-3 w-3" />
              Finalizado por {service.completedByEmail.split('@')[0]}
            </span>
          )}
        </div>
      </div>

      <div className="flex items-center gap-2">
        {service.status === 'pending' && isManager && (
          <button
            onClick={() => onComplete?.(service.id)}
            className="p-2.5 text-gray-400 hover:text-green-600 hover:bg-green-50 rounded-full transition-all duration-200"
            title="Concluir serviço"
          >
            <CheckCircle className="h-6 w-6" />
          </button>
        )}
      </div>
    </div>
  );
};
