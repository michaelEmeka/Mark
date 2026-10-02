import "./TabBar.css";
import { HomeIcon, TimetableIcon, ProfileIcon } from "./icons";
import type { TabId } from "../types";

interface TabBarProps {
  activeTab: TabId | null;
  hidden: boolean;
  onNavigate: (tab: TabId) => void;
}

export default function TabBar({ activeTab, onNavigate, hidden }: TabBarProps) {
  return (
    <div className="tabbar" style={{ display: hidden ? "none" : "flex" }}>
      <button className={`tabbtn ${activeTab === "dashboard" ? "active" : ""}`} onClick={() => onNavigate("dashboard")}>
        <HomeIcon /><span>Home</span>
      </button>
      <button className={`tabbtn ${activeTab === "timetable" ? "active" : ""}`} onClick={() => onNavigate("timetable")}>
        <TimetableIcon /><span>Timetable</span>
      </button>
      <button className={`tabbtn ${activeTab === "profile" ? "active" : ""}`} onClick={() => onNavigate("profile")}>
        <ProfileIcon /><span>Profile</span>
      </button>
    </div>
  );
}
