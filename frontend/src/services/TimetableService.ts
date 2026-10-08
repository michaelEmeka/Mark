import axios from "axios";

const BASE_URL = (import.meta as ImportMeta & { env?: { API_BASE_URL?: string } }).env?.API_BASE_URL || "http://localhost:8000";

export interface TimetableEntryApi {
  id: number;
  course_name: string;
  course_code: string;
  semester_name: string;
  day: string;
  start_time: string;
  end_time: string;
  timetable: number;
  is_one_time: boolean;
}

export interface TimetableScheduleApi {
  id: number;
  timetable_entry_id: number;
  course_name: string;
  course_code: string;
  date: string;
  day?: string;
  start_time?: string;
  end_time?: string;
  lecturer_name: string;
  lecture_hall: string;
  attendance_taken: boolean;
  is_one_time: boolean;
}

export interface UserAttendanceApi {
  course: {
    code: string;
    name: string;
  };
  lecturer: string;
  timetable_entry_schedule_id: number;
  date_taken: string;
  time_in: string;
  is_present: boolean;
}

const authHeaders = () => ({
  Authorization: `Bearer ${localStorage.getItem("access")}`,
});

async function fetchTimetableEntries(): Promise<TimetableEntryApi[]> {
  const endpoint = `${BASE_URL}/api/v1/entities/timetable/entries/`;

  try {
    const response = await axios.get(endpoint, { headers: authHeaders() });
    const payload = response.data?.TimetableEntries ?? response.data ?? [];
    return Array.isArray(payload) ? payload : [];
  } catch (error: any) {
    console.error("Fetch timetable entries failed:", error.response?.data || error.message);
    throw error;
  }
}

async function fetchTimetableSchedules(): Promise<TimetableScheduleApi[]> {
  const endpoint = `${BASE_URL}/api/v1/entities/timetable/schedules/`;

  try {
    const response = await axios.get(endpoint, { headers: authHeaders() });
    const payload = response.data?.["TimetableEntries Schedules"] ?? response.data ?? [];
    return Array.isArray(payload) ? payload : [];
  } catch (error: any) {
    console.error("Fetch timetable schedules failed:", error.response?.data || error.message);
    throw error;
  }
}

async function fetchUserAttendance(): Promise<UserAttendanceApi[]> {
  const endpoint = `${BASE_URL}/api/v1/attendance/`;

  try {
    const response = await axios.get(endpoint, { headers: authHeaders() });
    const payload = response.data ?? [];
    return Array.isArray(payload) ? payload : [];
  } catch (error: any) {
    console.error("Fetch user attendance failed:", error.response?.data || error.message);
    throw error;
  }
}

export { fetchTimetableEntries, fetchTimetableSchedules, fetchUserAttendance };
