import axios from "axios";

const BASE_URL = (import.meta as ImportMeta & { env?: { API_BASE_URL?: string } }).env?.API_BASE_URL || "https://slacked-ranging-deport.ngrok-free.dev";

const api = axios.create({
    baseURL: BASE_URL,
    headers: {
        "ngrok-skip-browser-warning": "true",
    },
});

export interface University {
  id: number | string;
  name: string;
  code: string;
  city: string;
  state: string;
  zip_code: string;
}

export interface School {
  id: number | string;
  name: string;
  code?: string;
  university: number | string;
  university_name?: string;
}

export interface Department {
  id: number | string;
  name: string;
  code?: string;
  school: number | string;
  school_name?: string;
  university_id?: number | string;
}

export interface Level {
  id: number | string;
  code: number | string;
}

export interface AcademicSet {
  id: number | string;
  start_year: number | string;
  end_year: number | string;
  department: number | string;
  department_name?: string;
  school_id?: number | string;
  university_id?: number | string;
}

export interface SignupRequest {
  email: string;
  username: string;
  firstname: string;
  lastname: string;
  middlename?: string;
  password: string;
  push_token?: string;
  reg_number: string;
  university: number | undefined;
  school: number;
  department: number;
  level: number;
}

async function fetchUnis(): Promise<University[]> {
  const endpoint = `${BASE_URL}/api/v1/entities/universities/`;

  try {
    const response = await api.get<University[]>(endpoint);
    return response.data;
  } catch (error: any) {
    console.error("Fetch universities failed:", error.response?.data || error.message);
    throw error;
  }
}

async function fetchSchools(universityId?: number | string): Promise<School[]> {
  const endpoint = `${BASE_URL}/api/v1/entities/schools/`;

  try {
    const response = await api.get<School[]>(endpoint, {
      params: universityId ? { university: universityId } : {},
    });
    return response.data;
  } catch (error: any) {
    console.error("Fetch schools failed:", error.response?.data || error.message);
    throw error;
  }
}

async function fetchDepartments(schoolId?: number | string, universityId?: number | string): Promise<Department[]> {
  const endpoint = `${BASE_URL}/api/v1/entities/departments/`;

  try {
    const response = await api.get<Department[]>(endpoint, {
      params: schoolId ? { school: schoolId } : universityId ? { university: universityId } : {},
    });
    return response.data;
  } catch (error: any) {
    console.error("Fetch departments failed:", error.response?.data || error.message);
    throw error;
  }
}

async function fetchLevels(): Promise<Level[]> {
  const endpoint = `${BASE_URL}/api/v1/entities/levels/`;

  try {
    const response = await api.get<Level[]>(endpoint);
    return response.data;
  } catch (error: any) {
    console.error("Fetch levels failed:", error.response?.data || error.message);
    throw error;
  }
}

async function fetchSets(filters?: {
  departmentId?: number | string;
  schoolId?: number | string;
  universityId?: number | string;
}): Promise<AcademicSet[]> {
  const endpoint = `${BASE_URL}/api/v1/entities/sets/`;

  try {
    const response = await api.get<AcademicSet[]>(endpoint, {
      params: {
        ...(filters?.departmentId ? { department: filters.departmentId } : {}),
        ...(filters?.schoolId ? { school: filters.schoolId } : {}),
        ...(filters?.universityId ? { university: filters.universityId } : {}),
      },
    });
    return response.data;
  } catch (error: any) {
    console.error("Fetch sets failed:", error.response?.data || error.message);
    throw error;
  }
}

async function createUser(payload: SignupRequest) {
  const endpoint = `${BASE_URL}/api/v1/user/signup/`;

  try {
    const response = await api.post(endpoint, payload);
    return response.data;
  } catch (error: any) {
    console.error("Signup failed:", error.response?.data || error.message);
    throw error;
  }
}

export { fetchUnis, fetchSchools, fetchDepartments, fetchLevels, fetchSets, createUser };