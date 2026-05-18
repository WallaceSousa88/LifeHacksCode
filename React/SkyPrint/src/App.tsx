import React, { useState, useEffect, useMemo } from 'react';
import {
  onAuthStateChanged,
  User as FirebaseUser,
  signOut
} from 'firebase/auth';
import {
  collection,
  onSnapshot,
  query,
  orderBy,
  where,
  doc,
  getDoc,
  getDocs,
  setDoc,
  addDoc,
  updateDoc,
  serverTimestamp,
  limit,
  writeBatch
} from 'firebase/firestore';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy
} from '@dnd-kit/sortable';
import {
  Printer as PrinterIcon,
  LogOut,
  Plus,
  History,
  LayoutList,
  ChevronRight,
  ShieldCheck,
  User as UserIcon,
  Loader2,
  Users,
  UserPlus
} from 'lucide-react';
import { auth, db, handleFirestoreError } from './lib/firebase';
import { Login } from './components/Login';
import { SortableServiceItem } from './components/SortableServiceItem';
import { Printer, Service, UserProfile, OperationType, UserRole } from './types';
import { cn } from './lib/utils';
import { motion, AnimatePresence } from 'motion/react';

export default function App() {
  const [user, setUser] = useState<FirebaseUser | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [printers, setPrinters] = useState<Printer[]>([]);
  const [services, setServices] = useState<Service[]>([]);
  const [activePrinterId, setActivePrinterId] = useState<string | null>(null);
  const [showHistory, setShowHistory] = useState(false);
  const [showUserAdmin, setShowUserAdmin] = useState(false);
  const [newServiceDesc, setNewServiceDesc] = useState('');
  const [isAddingService, setIsAddingService] = useState(false);

  // User Management State
  const [allUsers, setAllUsers] = useState<UserProfile[]>([]);
  const [newUser, setNewUser] = useState({ username: '', role: 'operator' as UserRole });

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  // Authentication monitoring
  useEffect(() => {
    return onAuthStateChanged(auth, async (u) => {
      setUser(u);
      if (u) {
        try {
          const userRef = doc(db, 'users', u.uid);
          const userSnap = await getDoc(userRef);

          if (userSnap.exists()) {
            setProfile(userSnap.data() as UserProfile);
          }
        } catch (error) {
          console.error("Error fetching user profile:", error);
        }
      } else {
        setProfile(null);
      }
      setLoading(false);
    });
  }, []);

  // Fetch all users for Admin
  useEffect(() => {
    if (profile?.role !== 'manager' || !showUserAdmin) return;
    const q = query(collection(db, 'users'), orderBy('createdAt', 'desc'));
    return onSnapshot(q, (snapshot) => {
      setAllUsers(snapshot.docs.map(d => d.data() as UserProfile));
    });
  }, [profile, showUserAdmin]);

  // Fetch Printers
  useEffect(() => {
    if (!profile) return;

    const q = query(collection(db, 'printers'), orderBy('name', 'asc'));
    return onSnapshot(q, (snapshot) => {
      const pData = snapshot.docs.map(d => ({ id: d.id, ...d.data() } as Printer));
      setPrinters(pData);
      if (pData.length > 0 && !activePrinterId) {
        setActivePrinterId(pData[0].id);
      }

      // Auto-create initial printers if none exist
      if (pData.length === 0 && profile.role === 'manager') {
        const initialPrinters = ['Impressora Alfa', 'Impressora Beta'];
        initialPrinters.forEach(name => {
          addDoc(collection(db, 'printers'), { name });
        });
      }
    }, (error) => handleFirestoreError(error, OperationType.LIST, 'printers'));
  }, [profile, activePrinterId]);

  // Fetch Services (Active or History)
  useEffect(() => {
    if (!activePrinterId || !profile) return;

    const servicesRef = collection(db, 'printers', activePrinterId, 'services');
    const q = query(
      servicesRef,
      where('status', '==', showHistory ? 'completed' : 'pending'),
      orderBy(showHistory ? 'completedAt' : 'order', showHistory ? 'desc' : 'asc')
    );

    return onSnapshot(q, (snapshot) => {
      const sData = snapshot.docs.map(d => ({ id: d.id, ...d.data() } as Service));
      setServices(sData);
    }, (error) => handleFirestoreError(error, OperationType.LIST, `printers/${activePrinterId}/services`));
  }, [activePrinterId, showHistory, profile]);

  const handleAddService = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newServiceDesc.trim() || !activePrinterId || !profile || profile.role !== 'manager') return;

    setIsAddingService(true);
    try {
      const servicesRef = collection(db, 'printers', activePrinterId, 'services');
      const nextOrder = services.length > 0 ? Math.max(...services.map(s => s.order)) + 1 : 0;

      await addDoc(servicesRef, {
        description: newServiceDesc.trim(),
        status: 'pending',
        order: nextOrder,
        printerId: activePrinterId,
        createdAt: serverTimestamp(),
      });
      setNewServiceDesc('');
    } catch (error) {
      handleFirestoreError(error, OperationType.CREATE, 'services');
    } finally {
      setIsAddingService(false);
    }
  };

  const handleCompleteService = async (serviceId: string) => {
    if (!activePrinterId || !profile || profile.role !== 'manager') return;

    try {
      const serviceRef = doc(db, 'printers', activePrinterId, 'services', serviceId);
      await updateDoc(serviceRef, {
        status: 'completed',
        completedAt: serverTimestamp(),
        completedBy: profile.uid,
        completedByEmail: profile.email,
      });
    } catch (error) {
      handleFirestoreError(error, OperationType.UPDATE, 'services');
    }
  };

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newUser.username || !profile || profile.role !== 'manager') return;

    try {
      const idToken = await auth.currentUser?.getIdToken();
      const response = await fetch('/api/users/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          managerToken: idToken,
          newUser: {
            username: newUser.username,
            role: newUser.role
          }
        }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.error);

      setNewUser({ username: '', role: 'operator' });
      alert(`Usuário ${newUser.username} criado com sucesso! A senha padrão é 123456`);
    } catch (error: any) {
      alert(`Erro: ${error.message}`);
    }
  };

  const handleDragEnd = async (event: DragEndEvent) => {
    const { active, over } = event;
    if (!over || active.id === over.id || !activePrinterId || profile?.role !== 'manager') return;

    const activeId = active.id.toString();
    const overId = over.id.toString();

    const oldIndex = services.findIndex((s) => s.id === activeId);
    const newIndex = services.findIndex((s) => s.id === overId);

    if (oldIndex === -1 || newIndex === -1) return;

    const newServices = arrayMove(services, oldIndex, newIndex);
    setServices(newServices); // Optimistic update

    try {
      const batch = writeBatch(db);
      newServices.forEach((service: Service, index: number) => {
        const serviceRef = doc(db, 'printers', activePrinterId, 'services', service.id);
        batch.update(serviceRef, { order: index });
      });
      await batch.commit();
    } catch (error) {
      handleFirestoreError(error, OperationType.UPDATE, 'reorder');
    }
  };

  const handleLogout = () => signOut(auth);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Loader2 className="h-8 w-8 text-blue-500 animate-spin" />
      </div>
    );
  }

  if (!user) {
    return <Login />;
  }

  return (
    <div className="min-h-screen bg-[#f5f5f5] text-[#1a1a1a] font-sans flex flex-col h-screen overflow-hidden">
      {/* Top Navbar */}
      <nav className="h-16 bg-white border-b border-[#e5e5e5] flex items-center justify-between px-6 flex-shrink-0 z-30">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-black rounded-lg flex items-center justify-center">
            <PrinterIcon className="h-[18px] w-[18px] text-white stroke-[2.5]" />
          </div>
          <span className="font-bold text-[18px] tracking-tight">SkyPrint</span>
        </div>

        <div className="flex items-center gap-4">
          <div className="hidden sm:block text-right">
            <div className="text-[13px] font-semibold leading-tight">{profile?.displayName}</div>
            <div className="text-[10px] text-[#64748b] font-bold uppercase tracking-wider mt-0.5">
              {profile?.role === 'manager' ? 'Perfil: Gerente' : 'Perfil: Operador'}
            </div>
          </div>
          <div className="w-9 h-9 bg-[#e2e8f0] rounded-full flex items-center justify-center font-bold text-sm text-gray-700">
            {profile?.displayName?.charAt(0).toUpperCase()}
          </div>
          <button
            onClick={handleLogout}
            className="p-2 text-gray-400 hover:text-red-500 transition-colors"
            title="Sair"
          >
            <LogOut className="h-5 w-5" />
          </button>
        </div>
      </nav>

      <div className="flex-1 flex flex-col md:flex-row overflow-hidden relative">
        {/* Sidebar - Mobile/Desktop Navigation */}
        <aside className="w-full md:w-[260px] bg-[#eeeeee] flex-shrink-0 flex flex-col p-4 overflow-hidden h-full">
          <div className="flex-1 space-y-6">
            <div>
              <p className="text-[11px] uppercase font-bold text-[#64748b] mb-3 tracking-widest px-1">Visualização</p>
              <nav className="space-y-1">
                <button
                  onClick={() => { setShowHistory(false); setShowUserAdmin(false); }}
                  className={cn(
                    "w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm transition-all duration-200",
                    (!showHistory && !showUserAdmin) ? "bg-white shadow-sm text-black font-semibold" : "text-[#64748b] hover:bg-white/50 hover:text-black"
                  )}
                >
                  <LayoutList className="h-4 w-4" />
                  Fila de Impressão
                </button>
                <button
                  onClick={() => { setShowHistory(true); setShowUserAdmin(false); }}
                  className={cn(
                    "w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm transition-all duration-200",
                    (showHistory && !showUserAdmin) ? "bg-white shadow-sm text-black font-semibold" : "text-[#64748b] hover:bg-white/50 hover:text-black"
                  )}
                >
                  <History className="h-4 w-4" />
                  Histórico Realizado
                </button>
                {profile?.role === 'manager' && (
                  <button
                    onClick={() => setShowUserAdmin(true)}
                    className={cn(
                      "w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm transition-all duration-200",
                      showUserAdmin ? "bg-white shadow-sm text-black font-semibold" : "text-[#64748b] hover:bg-white/50 hover:text-black"
                    )}
                  >
                    <Users className="h-4 w-4" />
                    Gestão de Usuários
                  </button>
                )}
              </nav>
            </div>

            {!showUserAdmin && (
              <div>
                <p className="text-[11px] uppercase font-bold text-[#64748b] mb-3 tracking-widest px-1">Impressoras</p>
                <div className="space-y-1.5">
                  {printers.map((printer) => (
                    <button
                      key={printer.id}
                      onClick={() => setActivePrinterId(printer.id)}
                      className={cn(
                        "w-full flex flex-col items-start px-4 py-3 rounded-2xl text-left transition-all duration-200 border",
                        activePrinterId === printer.id
                          ? "bg-white border-transparent shadow-sm"
                          : "border-transparent text-[#64748b] hover:bg-white/30"
                      )}
                    >
                      <div className="flex items-center justify-between w-full">
                        <span className={cn("text-[13px] font-bold truncate", activePrinterId === printer.id ? "text-black" : "")}>
                          {printer.name}
                        </span>
                        {activePrinterId === printer.id && <ChevronRight className="h-4 w-4 text-black" />}
                      </div>
                      <span className="text-[10px] text-[#64748b] mt-0.5">Status: Online</span>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </aside>

        {/* Main Workspace */}
        <main className="flex-1 flex flex-col bg-transparent overflow-hidden">
          <div className="flex-1 overflow-y-auto p-4 md:p-8">
            <div className="max-w-3xl mx-auto w-full flex flex-col h-full">

              {showUserAdmin ? (
                <div className="animate-in fade-in duration-300">
                  <div className="flex items-center justify-between mb-8">
                    <div>
                      <h2 className="text-[20px] font-bold tracking-tight">Gestão de Usuários</h2>
                      <p className="text-[13px] text-[#64748b]">Configure os acessos da equipe.</p>
                    </div>
                  </div>

                  <form onSubmit={handleCreateUser} className="bg-white p-6 rounded-2xl border border-[#e5e5e5] shadow-sm mb-10 space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-1">
                        <label className="text-[10px] uppercase font-bold text-[#64748b] ml-1">Nome de Usuário</label>
                        <input
                          type="text"
                          required
                          className="w-full bg-[#f8fafc] border border-[#e5e5e5] rounded-xl py-2.5 px-4 text-sm focus:outline-none focus:border-black"
                          placeholder="Ex: operador01"
                          value={newUser.username}
                          onChange={e => setNewUser({ ...newUser, username: e.target.value })}
                        />
                      </div>
                      <div className="space-y-1">
                        <label className="text-[10px] uppercase font-bold text-[#64748b] ml-1">Cargo</label>
                        <select
                          className="w-full bg-[#f8fafc] border border-[#e5e5e5] rounded-xl py-2.5 px-4 text-sm focus:outline-none focus:border-black appearance-none"
                          value={newUser.role}
                          onChange={e => setNewUser({ ...newUser, role: e.target.value as UserRole })}
                        >
                          <option value="operator">Operador</option>
                          <option value="manager">Gerente</option>
                        </select>
                      </div>
                    </div>
                    <button
                      type="submit"
                      className="w-full bg-black text-white py-3 rounded-xl text-sm font-bold hover:bg-gray-800 transition-colors"
                    >
                      Criar Acesso
                    </button>
                  </form>

                  <div className="space-y-3">
                    <p className="text-[11px] uppercase font-bold text-[#64748b] mb-4 tracking-widest px-1">Equipe Cadastrada</p>
                    {allUsers.map(u => (
                      <div key={u.uid} className="bg-white p-4 rounded-2xl border border-[#e5e5e5] flex items-center justify-between shadow-sm">
                        <div className="flex items-center gap-3">
                          <div className="h-10 w-10 bg-[#f8fafc] rounded-xl flex items-center justify-center text-[#64748b] border border-[#e5e5e5]">
                            <UserIcon className="h-5 w-5" />
                          </div>
                          <div>
                            <p className="text-sm font-bold">{u.displayName}</p>
                            <p className="text-[11px] text-[#64748b] font-medium uppercase tracking-tight">{u.role === 'manager' ? 'Gerente' : 'Operador'}</p>
                          </div>
                        </div>
                        <div className="text-[11px] text-[#94a3b8] font-mono">{u.email}</div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <>
                  <div className="flex items-center justify-between mb-8">
                    <div>
                      <h2 className="text-[20px] font-bold tracking-tight">
                        {printers.find(p => p.id === activePrinterId)?.name}
                      </h2>
                      <p className="text-[13px] text-[#64748b]">
                        {showHistory ? 'Histórico de serviços concluídos' : 'Acompanhamento da fila em tempo real'}
                      </p>
                    </div>
                  </div>

                  {!showHistory && profile?.role === 'manager' && (
                    <form onSubmit={handleAddService} className="mb-6">
                      <div className="relative group">
                        <input
                          type="text"
                          placeholder="Identifique o novo item da fila..."
                          className="w-full bg-white border border-[#e5e5e5] rounded-xl py-3.5 pl-4 pr-16 text-[13px] text-[#1a1a1a] placeholder-[#94a3b8] focus:outline-none focus:border-black transition-all shadow-sm"
                          value={newServiceDesc}
                          onChange={(e) => setNewServiceDesc(e.target.value)}
                          disabled={isAddingService}
                        />
                        <button
                          type="submit"
                          disabled={!newServiceDesc.trim() || isAddingService}
                          className="absolute right-2 top-1/2 -translate-y-1/2 bg-black text-white px-3 py-1.5 rounded-lg text-[11px] font-bold hover:bg-gray-800 disabled:opacity-50 transition-all"
                        >
                          {isAddingService ? '...' : 'Adicionar'}
                        </button>
                      </div>
                    </form>
                  )}

                  <div className="space-y-4 pb-12 flex-1">
                    {services.length === 0 ? (
                      <div className="flex flex-col items-center justify-center py-24 bg-white/50 rounded-3xl border border-dashed border-[#cbd5e1]">
                        <div className="h-10 w-10 text-[#94a3b8] mb-3 opacity-50">
                          {showHistory ? <History className="h-full w-full" /> : <LayoutList className="h-full w-full" />}
                        </div>
                        <p className="text-[13px] text-[#94a3b8] font-medium">Nenhum serviço registrado</p>
                      </div>
                    ) : (
                      <DndContext
                        sensors={sensors}
                        collisionDetection={closestCenter}
                        onDragEnd={handleDragEnd}
                      >
                        <SortableContext
                          items={services.map((s) => s.id)}
                          strategy={verticalListSortingStrategy}
                        >
                          <AnimatePresence initial={false}>
                            {services.map((service) => (
                              <motion.div
                                key={service.id}
                                initial={{ opacity: 0, y: 5 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, scale: 0.98 }}
                                layout
                                className={cn(showHistory ? "border-l-2 border-[#e5e5e5] pl-6 ml-2 relative before:content-[''] before:absolute before:-left-[5.5px] before:top-2 before:w-2.5 before:h-2.5 before:rounded-full before:bg-[#94a3b8]" : "")}
                              >
                                <SortableServiceItem
                                  service={service}
                                  isManager={profile?.role === 'manager' && !showHistory}
                                  onComplete={handleCompleteService}
                                />
                              </motion.div>
                            ))}
                          </AnimatePresence>
                        </SortableContext>
                      </DndContext>
                    )}
                  </div>
                </>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
