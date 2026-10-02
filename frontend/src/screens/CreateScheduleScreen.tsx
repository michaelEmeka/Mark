import "./CreateScheduleScreen.css";
import { BackIcon } from "../components/icons";

interface CreateScheduleScreenProps {
  active: boolean;
  onBack: () => void;
  onCreate: () => void;
}

export default function CreateScheduleScreen({ active, onBack, onCreate }: CreateScheduleScreenProps) {
  return (
    <div className={`screen ${active ? "active" : ""}`}>
      <div className="topbar"><div className="backbtn" onClick={onBack}><BackIcon /></div><div className="h2">New schedule</div></div>
      <div className="pad" style={{ paddingTop: 8 }}>
        <div className="muted" style={{ marginBottom: 18 }}>Create a dated instance of a timetable entry.</div>
        <div className="field"><label>Timetable entry</label>
          <select>
            <option>Mon · Power Electronics · 8:00–10:00</option>
            <option>Thu · Power Electronics · 8:00–10:00</option>
            <option>Thu · Control Systems · 11:00–1:00</option>
            <option>Thu · Digital Signal Processing · 2:00–4:00</option>
            <option>Fri · Engineering Ethics · 10:00–12:00</option>
          </select>
        </div>
        <div className="field"><label>Date</label><input type="date" defaultValue="2026-09-10" /></div>
        <div className="pref-row" style={{ background: "var(--card)", border: "1px solid var(--card-line)", borderRadius: 12, marginBottom: 16 }}>
          <div className="pref-mid">
            <div className="pref-title">One-time</div>
            <div className="pref-sub">Off = counts toward automated weekly population</div>
          </div>
          <label className="toggle"><input type="checkbox" /><span className="track"><span className="knob" /></span></label>
        </div>
        <button className="btn btn-primary" onClick={onCreate}>Create schedule</button>
      </div>
    </div>
  );
}
