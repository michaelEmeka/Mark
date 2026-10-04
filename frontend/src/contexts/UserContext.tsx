import {createContext, useState, useContext, useEffect} from "react"
import { useAppContext } from "./AppContext";
import { fetchUser } from "../services/Auth";

interface UserContextType {
  loading: boolean;
  setLoading: (loading: boolean) => void;
  user: User | null;
  getUser: () => Promise<void>;
}

interface User {
  email: String;
  username: String;
  firstname: String;
  lastname: String;
  middlename: String;
  push_token: String;
  preferences: Object;
  reg_number: String;
  department: String;
  level: String;
}

const UserContext = createContext<UserContextType | undefined>(undefined)
export const useUserContext = () => useContext(UserContext)

export default function UserProvider({ children }: { children: React.ReactNode }) {
  const { loading, setLoading } = useAppContext() as {
    loading: boolean;
    setLoading: (value: boolean) => void;
  };
  const [user, setUser] = useState<User | null>(null);

  const getUser = async () => {
    setLoading(true);
    try {
      const userData = await fetchUser();
      setUser(userData);
    } catch (error) {
      console.error("Failed to fetch user data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getUser();
  }, []);

    
  const value = {
    loading,
    setLoading,
    user,
    getUser
  }

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
}