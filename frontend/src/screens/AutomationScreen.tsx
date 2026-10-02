import "./AutomationScreen.css";
import { BackIcon } from "../components/icons";

interface AutomationScreenProps {
  active: boolean;
  onBack: () => void;
}

export default function AutomationScreen({ active, onBack }: AutomationScreenProps) {
  return (
    <div className={`screen ${active ? "active" : ""}`}>
      <div className="topbar"><div className="backbtn" onClick={onBack}><BackIcon /></div><div className="h2">Automation</div></div>
      <div className="pad" style={{ paddingTop: 8 }}>
        <div className="list-group" style={{ margin: "0 0 6px" }}>
          <div className="pref-row">
            <div className="pref-mid">
              <div className="pref-title">Auto-role weekly timetable</div>
              <div className="pref-sub">Generates non-one-time schedules from entries every Monday, 12:00am</div>
            </div>
            <label className="toggle"><input type="checkbox" defaultChecked /><span className="track"><span className="knob" /></span></label>
          </div>
        </div>
        <div className="callout">Only entries not marked one-time are picked up by the automation. Impromptu classes still need a manual schedule.</div>
      </div>
    </div>
  );
}
