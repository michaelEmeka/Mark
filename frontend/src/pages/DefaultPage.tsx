import { useState } from "react";
import "../styles/theme.css";
import "../styles/common.css";
import "./DefaultPage.css";

//import RoleSwitch from "./RoleSwitch";
import TabBar from "../components/TabBar";
//import LoginScreen from "./pages/LoginPage";
//import SignupScreen from "./pages/SignupPage";
import DashboardScreen from "../screens/DashboardScreen";
import TimetableScreen from "../screens/TimetableScreen";
import CreateScheduleScreen from "../screens/CreateScheduleScreen";
import ProfileScreen from "../screens/ProfileScreen";
import ProfileEditScreen from "../screens/ProfileEditScreen";
import PreferencesScreen from "../screens/PreferencesScreen";
import AutomationScreen from "../screens/AutomationScreen";
import { TAB_ROOTS, rootTabFor } from "../data/mockData";
import type { ScreenId, Day } from "../types";

export default function DefaultPage() {
  const [screen, setScreen] = useState<ScreenId>("screen-dashboard");
  //const [role, setRole] = useState<Role>("student");
  const [activeDay, setActiveDay] = useState<Day>("Thu");

  const isAuth = screen === "screen-login" || screen === "screen-signup";
  const activeTab = rootTabFor(screen);
  //console.log("in default page")
  return (
    <div className="default-page">
      {/* <RoleSwitch role={role} onChange={setRole} /> */}

      <div className="shell">
        <div className="statusbar"><span>9:41</span><span>Mark</span></div> 

        <div className="screens">
          <DashboardScreen active={screen === "screen-dashboard"} />
          <TimetableScreen
            active={screen === "screen-timetable"}
            activeDay={activeDay}
            setActiveDay={setActiveDay}
            onOpenCreateSchedule={() => setScreen("screen-create-schedule")}
          />
          <CreateScheduleScreen
            active={screen === "screen-create-schedule"}
            onBack={() => setScreen("screen-timetable")}
            onCreate={() => setScreen("screen-timetable")}
          />
          <ProfileScreen
            active={screen === "screen-profile"}
            //role={role}
            onEdit={() => setScreen("screen-profile-edit")}
            onPreferences={() => setScreen("screen-preferences")}
            onAutomation={() => setScreen("screen-automation")}
            onLogout={() => setScreen("screen-login")}
          />
          <ProfileEditScreen
            active={screen === "screen-profile-edit"}
            onBack={() => setScreen("screen-profile")}
            onSave={() => setScreen("screen-profile")}
          />
          <PreferencesScreen
            active={screen === "screen-preferences"}
            onBack={() => setScreen("screen-profile")}
          />
          <AutomationScreen
            active={screen === "screen-automation"}
            onBack={() => setScreen("screen-profile")}
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
