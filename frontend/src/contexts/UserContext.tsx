import {createContext, useState, useContext} from "react"

interface UserContextType {
  loading: boolean;
  setLoading: (loading: boolean) => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined)
export const useUserContext = () => useContext(UserContext)
export default function UserProvider({ children }: { children: React.ReactNode }) {
  const [loading, setLoading] = useState(false);
  console.log(loading);
  const value = {
    loading,
    setLoading
  }

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
}