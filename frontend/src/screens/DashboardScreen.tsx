import "./DashboardScreen.css";
import { useEffect, useMemo, useState } from "react";
import { CheckIcon, MissIcon } from "../components/icons";
import { useUserContext } from "../contexts/UserContext";
import {
  fetchTimetableEntries,
  fetchTimetableSchedules,
  fetchUserAttendance,
  type TimetableEntryApi,
  type TimetableScheduleApi,
  type UserAttendanceApi,
} from "../services/TimetableService";

interface DashboardScreenProps {
  active: boolean;
}

const dayMap: Record<number, string> = {
  0: "Sun",
  1: "Mon",
  2: "Tue",
  3: "Wed",
  4: "Thu",
  5: "Fri",
  6: "Sat",
};

const normalizeDay = (value?: string): string | null => {
  const mapped: Record<string, string> = {
    MON: "Mon",
    TUE: "Tue",
    WED: "Wed",
    THU: "Thu",
    FRI: "Fri",
  };

  return mapped[(value ?? "").toUpperCase()] ?? null;
};

const formatTime = (value?: string) => {
  if (!value) return "--:--";
  const normalized = value.includes(":") ? value : `${value.slice(0, 2)}:${value.slice(2)}`;
  return normalized.length >= 5 ? normalized.slice(0, 5) : normalized;
};

const formatDateKey = (date: Date) => date.toISOString().slice(0, 10);

const buildWeekStrip = () => {
  const today = new Date();
  const mondayOffset = (today.getDay() + 6) % 7;
  const monday = new Date(today);
  monday.setHours(0, 0, 0, 0);
  monday.setDate(today.getDate() - mondayOffset);

  return Array.from({ length: 7 }, (_, index) => {
    const current = new Date(monday);
    current.setDate(monday.getDate() + index);

    return {
      label: dayMap[current.getDay()],
      date: current.getDate(),
      iso: formatDateKey(current),
    };
  });
};

export default function DashboardScreen({ active }: DashboardScreenProps) {
  const context = useUserContext();
  const [entries, setEntries] = useState<TimetableEntryApi[]>([]);
  const [schedules, setSchedules] = useState<TimetableScheduleApi[]>([]);
  const [attendance, setAttendance] = useState<UserAttendanceApi[]>([]);
  const [loading, setLoading] = useState(false);

  if (!context) {
    throw new Error("useUser must be used within a UserProvider");
  }

  const { user } = context;

  useEffect(() => {
    const loadDashboardData = async () => {
      setLoading(true);
      try {
        const [entriesData, schedulesData, attendanceData] = await Promise.all([
          fetchTimetableEntries(),
          fetchTimetableSchedules(),
          fetchUserAttendance(),
        ]);
        setEntries(entriesData);
        setSchedules(schedulesData);
        setAttendance(attendanceData);
      } catch (error) {
        console.error("Failed to load dashboard timetable data:", error);
        setEntries([]);
        setSchedules([]);
        setAttendance([]);
      } finally {
        setLoading(false);
      }
    };

    void loadDashboardData();
  }, []);

  const today = useMemo(() => new Date(), []);
  const todayIso = formatDateKey(today);
  const todayLabel = dayMap[today.getDay()];
  const weekStrip = useMemo(() => buildWeekStrip(), [todayIso]);

  const attendancePercent = useMemo(() => {
    if (!attendance.length) return 0;
    const present = attendance.filter((record) => record.is_present).length;
    return Math.round((present / attendance.length) * 100);
  }, [attendance]);

  const todaysEntries = entries.filter((entry) => normalizeDay(entry.day) === todayLabel);
  const todayScheduleLookup = useMemo(() => {
    const lookup = new Map<number, TimetableScheduleApi>();

    schedules.forEach((schedule) => {
      if (schedule.date === todayIso) {
        lookup.set(schedule.timetable_entry_id, schedule);
      }
    });

    return lookup;
  }, [schedules, todayIso]);

  const greetingText = new Intl.DateTimeFormat("en-US", {
    weekday: "long",
    day: "numeric",
    month: "long",
  }).format(today);

  return (
    <div className={`screen ${active ? "active" : ""}`}>
      <div className="pad" style={{ paddingBottom: 6 }}>
        <div className="greet-row">
          <div>
            <div className="h1">Hi, {user?.firstname}</div>
            <div className="muted" style={{ marginTop: 2 }}>{greetingText}</div>
          </div>
          <div className="greet-avatar">{user?.firstname?.charAt(0) || "MO"}</div>
        </div>
      </div>

      <div className="daystrip">
        {weekStrip.map(({ label, date, iso }) => (
          <div key={`${label}-${iso}`} className={`daychip ${label === todayLabel ? "today" : ""}`}>
            <div className="dname">{label}</div>
            <div className="dnum">{date}</div>
          </div>
        ))}
      </div>

      <div className="today-list">
        {loading && <div className="tt-empty">Loading current timetable...</div>}

        {!loading && todaysEntries.length === 0 && (
          <div className="tt-empty">No classes scheduled for today.</div>
        )}

        {!loading && todaysEntries.map((entry) => {
          const schedule = todayScheduleLookup.get(entry.id);
          const scheduled = Boolean(schedule);
          const venue = schedule?.lecture_hall || "Not assigned";

          return (
            <div key={entry.id} className="class-row">
              <span className="class-time">{`${formatTime(entry.start_time)} - ${formatTime(entry.end_time)}`}</span>
              <span className={`class-bar ${scheduled ? "" : "dim"}`} />
              <div className="class-mid">
                <div className="class-course">{entry.course_name}</div>
                <div className="class-venue">{venue}</div>
              </div>
              <span className={`class-badge ${scheduled ? "on" : "off"}`}>
                {scheduled ? "Scheduled" : "Not scheduled"}
              </span>
            </div>
          );
        })}
      </div>

      <div className="stat-cards">
        <div className="stat-card">
          <div className="lab">Attendance so far</div>
          <div className="ring-mini-wrap">
            <svg width="56" height="56" viewBox="0 0 56 56">
              <circle className="ring-mini-track" cx="28" cy="28" r="22" />
              <circle
                className="ring-mini-val"
                cx="28"
                cy="28"
                r="22"
                strokeDasharray="138"
                strokeDashoffset={138 - (attendancePercent / 100) * 138}
              />
            </svg>
            <div className="ring-mini-num">{attendancePercent}%</div>
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
