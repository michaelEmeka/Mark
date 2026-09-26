import { useState } from "react";
import "./styles/theme.css";
import "./styles/common.css";
import "./App.css";
import SignupScreen from "./screens/Signup";
import LoginScreen from "./screens/Login";
import DashboardScreen from "./screens/Dashboard";
import TimetableScreen from "./screens/Timetable";
import TabBar from "./TabBar";
import { TAB_ROOTS, rootTabFor } from "./data/mockData";
import type { ScreenId, Day, Role} from "./types";


export default function App() {
  const [screen, setScreen] = useState<ScreenId>("screen-login");
  const [role, setRole] = useState<Role>("student");
  const [activeDay, setActiveDay] = useState<Day>("Thu");

  const isAuth = screen === "screen-login" || screen === "screen-signup";
  const activeTab = rootTabFor(screen);

  return (
    <div className="mark-root">
      <div className="shell">
        <div className="screens">
          <LoginScreen
            active={screen === "screen-login"}
            onSignIn={() => setScreen("screen-dashboard")}
            onGoSignup={() => setScreen("screen-signup")}
          />
          <SignupScreen
            active={screen === "screen-signup"}
            onBack={() => setScreen("screen-login")}
            onSignUp={() => setScreen("screen-dashboard")}
          />
          <DashboardScreen active={screen === "screen-dashboard"} />
          <TimetableScreen
            active={screen === "screen-timetable"}
            role={role}
            activeDay={activeDay}
            setActiveDay={setActiveDay}
            onOpenCreateSchedule={() => setScreen("screen-create-schedule")}
          />
        </div>

        <TabBar
          activeTab={activeTab}
          hidden={isAuth}
          onNavigate={(tab) => setScreen(TAB_ROOTS[tab])}
        />
        </div>
      </div>
  );
}
