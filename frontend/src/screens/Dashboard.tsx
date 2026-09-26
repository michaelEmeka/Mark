import "../styles/Dashboard.css";
import { WEEK_STRIP, TODAY_LABEL } from "../data/mockData";
import { CheckIcon, MissIcon } from "../icons";

interface DashboardScreenProps {
  active: boolean;
}

export default function DashboardScreen({ active }: DashboardScreenProps) {
  return (
    <div className={`screen ${active ? "active" : ""}`}>
      <div className="pad" style={{ paddingBottom: 6 }}>
        <div className="greet-row">
          <div>
            <div className="h1">Hi, Michael</div>
            <div className="muted" style={{ marginTop: 2 }}>Thursday, 10 September</div>
          </div>
          <div className="greet-avatar">MO</div>
        </div>
      </div>

      <div className="daystrip">
        {WEEK_STRIP.map(({ label, date }) => (
          <div key={label} className={`daychip ${label === TODAY_LABEL ? "today" : ""}`}>
            <div className="dname">{label}</div>
            <div className="dnum">{date}</div>
          </div>
        ))}
      </div>

      <div className="today-list">
        <div className="class-row">
          <span className="class-time">8:00</span><span className="class-bar" />
          <div className="class-mid"><div className="class-course">Power Electronics</div><div className="class-venue">Lab 2</div></div>
          <span className="class-badge on">Scheduled</span>
        </div>
        <div className="class-row">
          <span className="class-time">11:00</span><span className="class-bar" />
          <div className="class-mid"><div className="class-course">Control Systems</div><div className="class-venue">Lecture Hall 1</div></div>
          <span className="class-badge on">Scheduled</span>
        </div>
        <div className="class-row">
          <span className="class-time">2:00</span><span className="class-bar dim" />
          <div className="class-mid"><div className="class-course">Digital Signal Processing</div><div className="class-venue">Lecture Hall 3</div></div>
          <span className="class-badge off">Not scheduled</span>
        </div>
      </div>

      <div className="stat-cards">
        <div className="stat-card">
          <div className="lab">Attendance so far</div>
          <div className="ring-mini-wrap">
            <svg width="56" height="56" viewBox="0 0 56 56">
              <circle className="ring-mini-track" cx="28" cy="28" r="22" />
              <circle className="ring-mini-val" cx="28" cy="28" r="22" strokeDasharray="138" strokeDashoffset="35" />
            </svg>
            <div className="ring-mini-num">78%</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="lab">Failure risk</div>
          <div className="infer-row"><span className="infer-num">Low</span><span className="infer-label">14%</span></div>
          <div className="infer-bar"><div className="infer-bar-fill" style={{ width: "14%" }} /></div>
          <div className="infer-note">Based on attendance trend + 2 recent misses</div>
        </div>
      </div>

      <div className="activity-head">
        <div className="h2">Recent activity</div>
        <div className="live-pill"><span className="live-dot" />Live</div>
      </div>
      <div className="activity-list">
        <div className="activity-row">
          <div className="act-icon ok"><CheckIcon /></div>
          <div className="act-mid"><div className="act-course">Power Electronics</div><div className="act-when">Today, 8:04am · Attended</div></div>
        </div>
        <div className="activity-row">
          <div className="act-icon miss"><MissIcon /></div>
          <div className="act-mid"><div className="act-course">Digital Signal Processing</div><div className="act-when">Yesterday · Missed</div></div>
        </div>
        <div className="activity-row">
          <div className="act-icon ok"><CheckIcon /></div>
          <div className="act-mid"><div className="act-course">Control Systems</div><div className="act-when">Wed, 11:02am · Attended</div></div>
        </div>
      </div>
    </div>
  );
}
