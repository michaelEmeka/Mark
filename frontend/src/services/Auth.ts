import axios from "axios";
const BASE_URL = import.meta.env.API_BASE_URL || "http://localhost:8000";

interface LoginRequest {
    email: string;
    password: string;
}

interface LoginResponse {
    token: string;
    user: {
        access: string;
        refresh: string;
    };
}

async function Login({ email, password }: LoginRequest): Promise<LoginResponse> {
    let url = `${BASE_URL}/api/v1/users/login/`;
    try {
        const res = await axios.post(url, { email, password });
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

export { Login };