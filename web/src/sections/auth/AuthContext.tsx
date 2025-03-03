import React, { createContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';

const baseUrl = import.meta.env.VITE_BASE_URL;

interface AuthContextProps {
  isAdmin: boolean;
  fetchUserRole: () => void;
}

interface AuthProviderProps {
  children: ReactNode;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

const getIsAdmin = async (): Promise<boolean> => {
  const token = localStorage.getItem('token');
  if (!token) return false;

  try {
    const response = await axios.get(`${baseUrl}/api/v1/admin/check`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data.isAdmin;
  } catch (error) {
    console.error('Error checking admin status:', error);
    return false;
  }
};

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAdmin, setIsAdmin] = useState(false);

  const fetchUserRole = async () => {
    const adminStatus = await getIsAdmin();
    setIsAdmin(adminStatus);
  };

  useEffect(() => {
    fetchUserRole();
  }, []);

  return (
    <AuthContext.Provider value={{ isAdmin, fetchUserRole }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextProps => {
  const context = React.useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
