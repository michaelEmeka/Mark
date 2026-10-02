import "./ProfileScreen.css";
import { EditIcon, SettingsIcon, AutomationIcon, LogoutIcon, ChevIcon } from "../components/icons";
import type { Role } from "../types";

interface ProfileScreenProps {
  active: boolean;
  onEdit: () => void;
  onPreferences: () => void;
  onAutomation: () => void;
  onLogout: () => void;
}

export default function ProfileScreen({ active, onEdit, onPreferences, onAutomation, onLogout }: ProfileScreenProps) {
  return (
    <div className={`screen ${active ? "active" : ""}`}>
      <div className="profile-head">
        <div className="profile-avatar">MO</div>
        <div className="h2">Michael Onuekwusi</div>
        <div className="profile-meta">EEE/2021/xxx · 400L · Electrical & Electronic Engineering</div>
        {/* {role === "courserep" && <div className="rep-chip">Course Representative</div>} */}
      </div>

      <div className="list-group">
        <div className="list-item" onClick={onEdit}>
          <div className="li-icon"><EditIcon /></div>
          <div className="li-text">Edit profile</div>
          <ChevIcon />
        </div>
        <div className="list-item" onClick={onPreferences}>
          <div className="li-icon"><SettingsIcon /></div>
          <div className="li-text">Preferences</div>
          <ChevIcon />
        </div>
        {/* {role === "courserep" && (
          <div className="list-item" onClick={onAutomation}>
            <div className="li-icon"><AutomationIcon /></div>
            <div>
              <div className="li-text">Automation</div>
              <div className="li-sub">Weekly timetable auto-role</div>
            </div>
            <ChevIcon />
          </div>
        )} */}
      </div>

      <div className="list-group">
        <div className="list-item danger" onClick={onLogout}>
          <div className="li-icon" style={{ color: "var(--coral)" }}><LogoutIcon /></div>
          <div className="li-text">Log out</div>
        </div>
      </div>
    </div>
  );
}
