import { useState } from "react";
import "../styles/theme.css";
import "../styles/common.css";
import "./DefaultPage.css";

import TabBar from "../components/TabBar";
import DashboardScreen from "../screens/DashboardScreen";
import TimetableScreen from "../screens/TimetableScreen";
import CreateScheduleScreen from "../screens/CreateScheduleScreen";
import ProfileScreen from "../screens/ProfileScreen";
import ProfileEditScreen from "../screens/ProfileEditScreen";
import PreferencesScreen from "../screens/PreferencesScreen";
import AutomationScreen from "../screens/AutomationScreen";
import { TAB_ROOTS, rootTabFor } from "../data/mockData";
import type { ScreenId, Day } from "../types";
import { useUserContext } from "../contexts/UserContext";
import { Navigate } from "react-router-dom";
import LoadingOverlay from "../components/LoadingOverlay";



const getTodayDay = (): Day => {
  const today = new Date().getDay();
  const map: Record<number, Day> = {
    0: "Mon",
    1: "Mon",
    2: "Tue",
    3: "Wed",
    4: "Thu",
    5: "Fri",
    6: "Mon",
  };

  return map[today] ?? "Mon";
};

export default function DefaultPage() {
  const [screen, setScreen] = useState<ScreenId>("screen-dashboard");
  //const [role, setRole] = useState<Role>("student");
  const [activeDay, setActiveDay] = useState<Day>(getTodayDay());

  const activeTab = rootTabFor(screen);
  //console.log("in default page")

  const { user, loading, logout, getUser } = useUserContext();

  if (loading) {
    return <LoadingOverlay text="Loading..." />;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="default-page">
      {/* <RoleSwitch role={role} onChange={setRole} /> */}

      <div className="shell">
        {/* <div className="statusbar"><span>9:41</span><span>Mark</span></div> */}
        {loading && <LoadingOverlay text="loading.."></LoadingOverlay>}
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
            user={user}
            onEdit={() => setScreen("screen-profile-edit")}
            onPreferences={() => setScreen("screen-preferences")}
            onAutomation={() => setScreen("screen-automation")}
            onLogout={() => {
              void logout();
            }}
          />
          <ProfileEditScreen
            active={screen === "screen-profile-edit"}
            user={user}
            onBack={() => setScreen("screen-profile")}
            onSave={async (payload) => {
              try {
                const { updateUser } = await import("../services/AuthService");
                await updateUser(payload);
                await getUser();
                setScreen("screen-profile");
              } catch (error) {
                console.error("Profile update failed:", error);
              }
            }}
          />
          <PreferencesScreen
            active={screen === "screen-preferences"}
            user={user}
            onBack={() => setScreen("screen-profile")}
            onSave={async (payload) => {
              try {
                const { updateUser } = await import("../services/AuthService");
                await updateUser(payload);
                await getUser();
                setScreen("screen-profile");
              } catch (error) {
                console.error("Preferences update failed:", error);
              }
            }}
          />
          <AutomationScreen
            active={screen === "screen-automation"}
            onBack={() => setScreen("screen-profile")}
          />
        </div>

        <TabBar
          activeTab={activeTab}
          onNavigate={(tab) => setScreen(TAB_ROOTS[tab])}
        />
      </div>
    </div>
  );
}
