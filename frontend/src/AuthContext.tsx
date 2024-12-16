// /frontend/src/AuthContext.tsx
import React, { createContext, useState, useEffect, ReactNode, useMemo } from 'react';
import { authenticateUser } from './utils/authHelpers';

interface AuthContextType {
  token: string | null;
  setToken: (token: string | null) => void;
}

export const AuthContext = createContext<AuthContextType>({
  token: null,
  setToken: () => {},
});

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [token, setTokenState] = useState<string | null>(localStorage.getItem('jwt'));

  useEffect(() => {
    if (token) {
      localStorage.setItem('jwt', token);
    } else {
      localStorage.removeItem('jwt');
    }
  }, [token]);

  useEffect(() => {
    const verifyToken = async () => {
      if (token) {
        const isValid = await authenticateUser(token);
        if (!isValid) {
          setTokenState(null);
        }
      }
    };
    verifyToken();
  }, [token]);

  const setToken = (newToken: string | null) => {
    setTokenState(newToken);
  };

  // Memoize the context value to prevent unnecessary re-renders
  const value = useMemo(() => ({ token, setToken }), [token]);

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
