import axios from "axios";
const BASE_URL = (import.meta as ImportMeta & { env?: { API_BASE_URL?: string } }).env?.API_BASE_URL || "https://slacked-ranging-deport.ngrok-free.dev";

interface LoginRequest {
    email: string;
    password: string;
}

interface LoginResponse {
    access: string;
    refresh: string;
}

export interface ProfileUpdateRequest {
    username?: string;
    middlename?: string | null;
    push_token?: string | null;
    preferences?: Record<string, unknown> | null;
    set?: number | string | null;
}

async function logout() {
    const accessToken = localStorage.getItem("access");
    const refreshToken = localStorage.getItem("refresh");

    if (refreshToken) {
        try {
            await axios.post(
                `${BASE_URL}/api/v1/user/logout/`,
                { refresh: refreshToken },
                {
                    headers: {
                        Authorization: `Bearer ${accessToken || ""}`,
                    },
                }
            );
        } catch (error) {
            console.warn("Server logout failed, clearing local session anyway.", error);
        }
    }

    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");
}

async function Login({ email, password }: LoginRequest): Promise<LoginResponse> {
    const endpoint = `${BASE_URL}/api/v1/user/login/`;
    try {
        const res = await axios.post(endpoint, { email, password });
        localStorage.setItem("access", res.data.access);
        localStorage.setItem("refresh", res.data.refresh);
        console.log("Login successful:", res.data);
        return res.data as LoginResponse;
    }
    catch (error: any) {
        console.error("Login failed:", error.response?.data || error.message);
        throw error;
    }
}

async function fetchUser() {
    const endpoint = `${BASE_URL}/api/v1/user/`;
    try {
        const res = await axios.get(endpoint, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access")}`
            }
        });
        console.log("User data retrieved:", res.data);
        return res.data;
    } catch (error: any) {
        console.error("Failed to retrieve user data:", error.response?.data || error.message);
        throw error;
    }
}

async function updateUser(payload: ProfileUpdateRequest) {
    const endpoint = `${BASE_URL}/api/v1/user/update/`;
    try {
        const res = await axios.patch(endpoint, payload, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access")}`
            }
        });
        return res.data;
    } catch (error: any) {
        console.error("Failed to update user:", error.response?.data || error.message);
        throw error;
    }
}

export { Login, fetchUser, updateUser, logout };