import {createContext, useState, useContext, useEffect} from "react"
import { useAppContext } from "./AppContext";
import { fetchUser, logout as logoutUser } from "../services/AuthService";

interface UserContextType {
  loading: boolean;
  setLoading: (loading: boolean) => void;
  user: User | null;
  getUser: () => Promise<void>;
  logout: () => Promise<void>;
}

export interface User {
  email: string;
  username: string;
  firstname: string;
  lastname: string;
  middlename?: string | null;
  push_token?: string | null;
  preferences?: Record<string, unknown> | null;
  reg_number: string;
  department?: number | string | null;
  department_name?: string | null;
  school?: number | string | null;
  school_name?: string | null;
  university?: number | string | null;
  university_name?: string | null;
  level?: number | string | null;
  level_code?: number | string | null;
  set_id?: number | string | null;
  set_years?: {
    start_year?: number | string;
    end_year?: number | string;
  } | null;
}

const UserContext = createContext<UserContextType | null>(null)

export const useUserContext = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error("useUserContext must be used within a UserProvider");
  }
  return context;
};

export default function UserProvider({ children }: { children: React.ReactNode }) {
  const { loading, setLoading } = useAppContext() as {
    loading: boolean;
    setLoading: (value: boolean) => void;
  };

  const [user, setUser] = useState<User | null>(() => {
    const savedUser = localStorage.getItem("user");

    if (!savedUser) {
      return null;
    }

    try {
      return JSON.parse(savedUser) as User;
    } catch {
      return null;
    }
  });

  const getUser = async () => {
    const accessToken = localStorage.getItem("access");

    if (!accessToken) {
      setUser(null);
      setLoading(false);
      return;
    }

    setLoading(true);

    try {
      const userData = await fetchUser();
      setUser(userData);
      localStorage.setItem("user", JSON.stringify(userData));
    } catch (error) {
      console.error("Failed to fetch user data:", error);
      setUser(null);
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      localStorage.removeItem("user");
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      await logoutUser();
    } catch (error) {
      console.warn("Client logout cleanup continued after server logout failure.", error);
    } finally {
      setUser(null);
      setLoading(false);
    }
  };

  useEffect(() => {
    const accessToken = localStorage.getItem("access");

    if (!accessToken) {
      setUser(null);
      setLoading(false);
      return;
    }

    getUser();
  }, []);

  const value = {
    loading,
    setLoading,
    user,
    getUser,
    logout
  };

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
}