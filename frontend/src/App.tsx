import DefaultPage from "./pages/DefaultPage"
import LoginPage from "./pages/LoginPage"
import SignupPage from "./pages/SignupPage"
import UserProvider from "./contexts/UserContext"
import { Routes, Route } from "react-router-dom"

export default function App() {
  return (
    <UserProvider>
      <Routes>
        <Route path="/" element={<DefaultPage />}></Route>
        <Route path="/signup" element={<SignupPage />}></Route>
        <Route path="/login" element={<LoginPage />}></Route>
      </Routes>
    </UserProvider>
  );
}