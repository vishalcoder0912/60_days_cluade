"use client";
import React, { createContext, useContext } from "react";
import { useRouter } from "next/navigation";

interface User {
  id: string;
  name: string;
  email: string;
}

interface AuthCtx {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthCtx>({} as AuthCtx);

const localUser: User = {
  id: "local-demo-user",
  name: "Local User",
  email: "local@ats-optimizer.app",
};

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const router = useRouter();

  const login = async (email: string, password: string) => {
    router.push("/dashboard");
  };

  const register = async (name: string, email: string, password: string) => {
    router.push("/dashboard");
  };

  const logout = () => {
    router.push("/dashboard");
  };

  return (
    <AuthContext.Provider value={{ user: localUser, loading: false, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
