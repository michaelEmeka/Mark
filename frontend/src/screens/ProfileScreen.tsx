import "./ProfileScreen.css";
import { EditIcon, SettingsIcon, LogoutIcon, ChevIcon } from "../components/icons";
import type { User } from "../contexts/UserContext";

interface ProfileScreenProps {
  active: boolean;
  user: User | null;
  onEdit: () => void;
  onPreferences: () => void;
  onAutomation: () => void;
  onLogout: () => void;
}

export default function ProfileScreen({ active, user, onEdit, onPreferences, onLogout }: ProfileScreenProps) {
  const initials = `${user?.firstname?.[0] ?? ""}${user?.lastname?.[0] ?? ""}`.toUpperCase();
  const fullName = [user?.firstname, user?.lastname].filter(Boolean).join(" ") || "User";
  const regNumber = user?.reg_number || "";
  const level = user?.level_code ? `${user.level_code}L` : "";
  const department = user?.department_name || "";

  return (
    <div className={`screen ${active ? "active" : ""}`}>
      <div className="profile-head">
        <div className="profile-avatar">{initials || "U"}</div>
        <div className="h2">{fullName}</div>
        <div className="profile-meta">{[regNumber, level, department].filter(Boolean).join(" · ") || "Profile information pending"}</div>
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
