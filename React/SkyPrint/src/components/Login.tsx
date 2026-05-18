import React, { useState } from 'react';
import { signInWithCustomToken } from 'firebase/auth';
import { auth } from '../lib/firebase';
import { LogIn, Printer, User, Lock, Loader2, AlertCircle } from 'lucide-react';

export const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username || !password) return;

    setLoading(true);
    setError(null);
    try {
      // 1. Call our custom server to verify credentials and get a custom token
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Erro ao realizar login.');
      }

      // 2. Use the custom token to sign in to Firebase Client SDK
      await signInWithCustomToken(auth, data.token);
      
    } catch (err: any) {
      console.error('Error signing in:', err);
      setError(err.message || 'Erro de conexão com o servidor.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#f5f5f5] px-4">
      <div className="max-w-md w-full space-y-8 bg-white p-12 rounded-[24px] shadow-sm border border-[#e5e5e5]">
        <div className="text-center">
          <div className="mx-auto h-16 w-16 bg-black text-white rounded-2xl flex items-center justify-center mb-6 shadow-lg shadow-black/10">
            <Printer className="h-8 w-8 stroke-[2.5]" />
          </div>
          <h2 className="text-[28px] font-bold tracking-tight text-[#1a1a1a]">SkyPrint</h2>
          <p className="mt-3 text-[14px] text-[#64748b] font-medium leading-relaxed">
            Gestão de filas de impressão.<br />Use suas credenciais para acessar.
          </p>
        </div>

        <form onSubmit={handleLogin} className="mt-10 space-y-4">
          {error && (
            <div className="bg-red-50 border border-red-100 text-red-600 px-4 py-3 rounded-xl text-sm flex items-center gap-2 animate-shake">
              <AlertCircle className="h-4 w-4" />
              {error}
            </div>
          )}

          <div className="space-y-1">
            <label className="text-[11px] font-bold uppercase tracking-wider text-[#64748b] ml-1">Usuário</label>
            <div className="relative">
              <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
                <User className="h-4 w-4" />
              </div>
              <input
                type="text"
                required
                className="w-full bg-[#f8fafc] border border-[#e5e5e5] rounded-xl py-3 pl-11 pr-4 text-[14px] focus:outline-none focus:border-black focus:ring-1 focus:ring-black/5 transition-all"
                placeholder="Ex: admin"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-[11px] font-bold uppercase tracking-wider text-[#64748b] ml-1">Senha</label>
            <div className="relative">
              <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
                <Lock className="h-4 w-4" />
              </div>
              <input
                type="password"
                required
                className="w-full bg-[#f8fafc] border border-[#e5e5e5] rounded-xl py-3 pl-11 pr-4 text-[14px] focus:outline-none focus:border-black focus:ring-1 focus:ring-black/5 transition-all"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-3 py-3.5 px-4 bg-black text-white text-[14px] font-bold rounded-xl hover:bg-gray-800 disabled:opacity-50 transition-all active:scale-[0.98] mt-6 shadow-sm"
          >
            {loading ? <Loader2 className="h-5 w-5 animate-spin" /> : <LogIn className="h-5 w-5" />}
            Acessar Sistema
          </button>
        </form>

        <div className="mt-10">
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-[#f1f5f9]" />
            </div>
            <div className="relative flex justify-center text-[10px] uppercase font-bold tracking-widest">
              <span className="px-3 bg-white text-[#94a3b8]">Acesso Corporativo</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
