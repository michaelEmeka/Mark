export type Role = "student" | "courserep";

export type Day = "Mon" | "Tue" | "Wed" | "Thu" | "Fri";

export type ScreenId =
  | "screen-login"
  | "screen-signup"
  | "screen-dashboard"
  | "screen-timetable"
  | "screen-create-schedule"
  | "screen-profile"
  | "screen-profile-edit"
  | "screen-preferences"
  | "screen-automation";

export type TabId = "dashboard" | "timetable" | "profile";

// TimetableEntry: the recurring, department-set slot. Owns `day`.
export interface TimetableEntry {
  id: number;
  day: Day;
  time: string;
  course: string;
  venue: string;
}

// TimetableEntrySchedule: a dated instance of an entry. Owns `date`.
// one_time = impromptu (course rep created it individually);
// !one_time = counts toward the automated weekly population.
export interface TimetableEntrySchedule {
  entry_id: number;
  date: string;
  one_time: boolean;
}

export interface WeekStripDay {
  label: Day | "Sat" | "Sun";
  date: number;
}
