import "./TimetableScreen.css";
import { useEffect, useState } from "react";
import type { Day } from "../types";
import { fetchTimetableEntries, type TimetableEntryApi } from "../services/TimetableService";

const DAYS: Day[] = ["Mon", "Tue", "Wed", "Thu", "Fri"];

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

const normalizeDay = (day: string): Day | null => {
  const map: Record<string, Day> = {
    MON: "Mon",
    TUE: "Tue",
    WED: "Wed",
    THU: "Thu",
    FRI: "Fri",
  };

  return map[day?.toUpperCase?.() ?? ""] ?? null;
};

const formatTime = (value?: string) => {
  if (!value) return "--:--";
  const time = value.includes(":") ? value : `${value.slice(0, 2)}:${value.slice(2)}`;
  return time.length >= 5 ? time.slice(0, 5) : time;
};

interface TimetableScreenProps {
  active: boolean;
  activeDay: Day;
  setActiveDay: (day: Day) => void;
  onOpenCreateSchedule: () => void;
}

export default function TimetableScreen({ active, activeDay, setActiveDay }: TimetableScreenProps) {
  const [entries, setEntries] = useState<TimetableEntryApi[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (active) {
      setActiveDay(getTodayDay());
    }
  }, [active, setActiveDay]);

  useEffect(() => {
    const loadEntries = async () => {
      setLoading(true);
      try {
        const data = await fetchTimetableEntries();
        setEntries(data);
      } catch {
        setEntries([]);
      } finally {
        setLoading(false);
      }
    };

    loadEntries();
  }, []);

  const todaysEntries = entries.filter((entry) => {
    const normalizedDay = normalizeDay(entry.day);
    return normalizedDay === activeDay;
  });

  return (
    <div className={`screen ${active ? "active" : ""}`}>
      <div className="pad" style={{ paddingBottom: 0 }}>
        <div className="h1">Timetable</div>
        <div className="muted" style={{ marginTop: 4 }}>
          {loading ? "Loading timetable..." : "Department timetable"}
        </div>
      </div>

      <div className="tt-daytabs">
        {DAYS.map((d) => (
          <div key={d} className={`tt-tab ${d === activeDay ? "active" : ""}`} onClick={() => setActiveDay(d)}>{d}</div>
        ))}
      </div>

      <div className="tt-list">
        {todaysEntries.length === 0 && (
          <div className="tt-empty">
            {loading ? "Loading entries..." : "No entries in the department set for this day."}
          </div>
        )}

        {todaysEntries.map((entry) => (
          <div key={entry.id} className="tt-entry">
            <div className="tt-time-col">{`${formatTime(entry.start_time)} - ${formatTime(entry.end_time)}`}</div>
            <div className="tt-mid">
              <div className="tt-course">{entry.course_name}</div>
              <div className="tt-venue">{entry.course_code}</div>
              <div className="tt-tags">
                <span className="tt-tag entry-tag">{entry.semester_name}</span>
                <span className={`tt-tag ${entry.is_one_time ? "onetime-tag" : "sched-tag"}`}>
                  {entry.is_one_time ? "One-time" : "Recurring"}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/*role === "courserep" && (
        <button className="fab" onClick={onOpenCreateSchedule}>
          <PlusIcon />
        </button>
      )*/}
    </div>
  );
}
