import "./TimetableScreen.css";
import { DAYS, ENTRIES, SCHEDULES } from "../data/mockData";
import { PlusIcon } from "../components/icons";
import type { Role, Day } from "../types";

interface TimetableScreenProps {
  active: boolean;
  role: Role;
  activeDay: Day;
  setActiveDay: (day: Day) => void;
  onOpenCreateSchedule: () => void;
}

export default function TimetableScreen({ active, role, activeDay, setActiveDay, onOpenCreateSchedule }: TimetableScreenProps) {
  const todaysEntries = ENTRIES.filter((e) => e.day === activeDay);

  return (
    <div className={`screen ${active ? "active" : ""}`}>
      <div className="pad" style={{ paddingBottom: 0 }}>
        <div className="h1">Timetable</div>
        <div className="muted" style={{ marginTop: 4 }}>EEE — 400L · department set</div>
      </div>

      <div className="tt-daytabs">
        {DAYS.map((d) => (
          <div key={d} className={`tt-tab ${d === activeDay ? "active" : ""}`} onClick={() => setActiveDay(d)}>{d}</div>
        ))}
      </div>

      <div className="tt-list">
        {todaysEntries.length === 0 && <div className="tt-empty">No entries in the department set for this day.</div>}
        {todaysEntries.map((e) => {
          const sched = SCHEDULES.find((s) => s.entry_id === e.id);
          return (
            <div key={e.id} className={`tt-entry ${sched ? "scheduled" : ""}`}>
              <div className="tt-time-col">{e.time}</div>
              <div className="tt-mid">
                <div className="tt-course">{e.course}</div>
                <div className="tt-venue">{e.venue}</div>
                <div className="tt-tags">
                  <span className="tt-tag entry-tag">entry · {e.day}</span>
                  {sched ? (
                    <span className={`tt-tag ${sched.one_time ? "onetime-tag" : "sched-tag"}`}>
                      {sched.one_time ? `one-time · ${sched.date}` : `scheduled · ${sched.date}`}
                    </span>
                  ) : (
                    <span className="tt-tag entry-tag">no schedule instance</span>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {role === "courserep" && (
        <button className="fab" onClick={onOpenCreateSchedule}>
          <PlusIcon />
        </button>
      )}
    </div>
  );
}
