import {createContext, useState, useContext, ReactNode} from "react"

interface AppContextType {
  loading: boolean;
  setLoading: (loading: boolean) => void;
}

const AppContext = createContext<AppContextType | null>(null)

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useAppContext must be used within an AppProvider");
  }
  return context;
};

export default function AppProvider({ children }: { children: ReactNode }) {
  const [loading, setLoading] = useState<boolean>(false);
  console.log(loading);
  const value = {
    loading,
    setLoading
  }

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}