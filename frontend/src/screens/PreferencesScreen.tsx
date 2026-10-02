import "./PreferencesScreen.css";
import { BackIcon } from "../components/icons";

interface PreferencesScreenProps {
  active: boolean;
  onBack: () => void;
}

export default function PreferencesScreen({ active, onBack }: PreferencesScreenProps) {
  return (
    <div className={`screen ${active ? "active" : ""}`}>
      <div className="topbar"><div className="backbtn" onClick={onBack}><BackIcon /></div><div className="h2">Preferences</div></div>
      <div className="pad" style={{ paddingTop: 8 }}>
        <div className="list-group" style={{ margin: "0 0 16px" }}>
          <div className="pref-row">
            <div className="pref-mid"><div className="pref-title">Push notifications</div><div className="pref-sub">Class reminders, schedule changes</div></div>
            <label className="toggle"><input type="checkbox" defaultChecked /><span className="track"><span className="knob" /></span></label>
          </div>
          <div className="pref-row">
            <div className="pref-mid"><div className="pref-title">Email notifications</div><div className="pref-sub">Weekly attendance summary</div></div>
            <label className="toggle"><input type="checkbox" /><span className="track"><span className="knob" /></span></label>
          </div>
          <div className="pref-row">
            <div className="pref-mid"><div className="pref-title">Dark mode</div><div className="pref-sub">Off by default in this build</div></div>
            <label className="toggle"><input type="checkbox" /><span className="track"><span className="knob" /></span></label>
          </div>
        </div>
      </div>
    </div>
  );
}
