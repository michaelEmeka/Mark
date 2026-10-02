import "./RoleSwitch.css";
import type { Role } from "../types";

interface RoleSwitchProps {
  role: Role;
  onChange: (role: Role) => void;
}

// Preview-only control so both permission states (student / course rep)
// can be demoed without a real auth backend. Not part of the app's own UI.
export default function RoleSwitch({ role, onChange }: RoleSwitchProps) {
  return (
    <div className="demo-bar">
      <div className="demo-label">preview role — not part of the app</div>
      <div className="role-switch">
        <button className={role === "student" ? "active" : ""} onClick={() => onChange("student")}>Student</button>
        <button className={role === "courserep" ? "active" : ""} onClick={() => onChange("courserep")}>Course Rep</button>
      </div>
    </div>
  );
}
