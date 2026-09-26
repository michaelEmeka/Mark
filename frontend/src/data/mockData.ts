import type { TimetableEntry, TimetableEntrySchedule, WeekStripDay, Day, ScreenId, TabId } from "../types";

export const ENTRIES: TimetableEntry[] = [
  { id: 1, day: "Mon", time: "8:00", course: "Power Electronics", venue: "Lab 2" },
  { id: 2, day: "Mon", time: "12:00", course: "Engineering Ethics", venue: "Lecture Hall 1" },
  { id: 3, day: "Tue", time: "9:00", course: "Microprocessor Systems", venue: "Lab 1" },
  { id: 4, day: "Wed", time: "10:00", course: "Instrumentation", venue: "Lecture Hall 2" },
  { id: 5, day: "Thu", time: "8:00", course: "Power Electronics", venue: "Lab 2" },
  { id: 6, day: "Thu", time: "11:00", course: "Control Systems", venue: "Lecture Hall 1" },
  { id: 7, day: "Thu", time: "14:00", course: "Digital Signal Processing", venue: "Lecture Hall 3" },
  { id: 8, day: "Fri", time: "10:00", course: "Engineering Ethics", venue: "Lecture Hall 1" },
];

export const SCHEDULES: TimetableEntrySchedule[] = [
  { entry_id: 1, date: "2026-09-07", one_time: false },
  { entry_id: 5, date: "2026-09-10", one_time: false },
  { entry_id: 6, date: "2026-09-10", one_time: false },
  { entry_id: 3, date: "2026-09-08", one_time: false },
  { entry_id: 8, date: "2026-09-11", one_time: true },
];

export const DAYS: Day[] = ["Mon", "Tue", "Wed", "Thu", "Fri"];

// Chip labels fixed here so the dashboard's day-strip and the
// timetable's day-tabs always agree on how a day is written.
export const WEEK_STRIP: WeekStripDay[] = [
  { label: "Mon", date: 7 },
  { label: "Tue", date: 8 },
  { label: "Wed", date: 9 },
  { label: "Thu", date: 10 },
  { label: "Fri", date: 11 },
  { label: "Sat", date: 12 },
];

export const TODAY_LABEL: Day = "Thu";

export const TAB_ROOTS: Record<TabId, ScreenId> = {
  dashboard: "screen-dashboard",
  timetable: "screen-timetable",
  profile: "screen-profile",
};

export function rootTabFor(screenId: ScreenId): TabId | null {
  if (screenId === "screen-dashboard") return "dashboard";
  if (screenId === "screen-timetable" || screenId === "screen-create-schedule") return "timetable";
  if (
    screenId === "screen-profile" ||
    screenId === "screen-profile-edit" ||
    screenId === "screen-preferences" ||
    screenId === "screen-automation"
  ) {
    return "profile";
  }
  return null;
}