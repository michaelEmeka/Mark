import "./LoginPage.css";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom"
import { Login } from "../services/AuthService";
import { useUserContext } from "../contexts/UserContext";
import LoadingOverlay from "../components/LoadingOverlay";

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export default function LoginPage() {
  const { loading, setLoading, user, getUser } = useUserContext() as {
    loading: boolean;
    setLoading: (value: boolean) => void;
    user: any;
    getUser: () => Promise<void>;
  };
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const validateEmail = (value: string) => {
    if (!value.trim()) return "Email is required.";
    if (!emailRegex.test(value.trim())) return "Enter a valid email address.";
    return "";
  };

  const validatePassword = (value: string) => {
    if (!value) return "Password is required.";
    if (value.length < 5) return "Password must be at least 8 characters.";
    return "";
  };

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    const accessToken = localStorage.getItem("access");

    if (storedUser) {
      navigate("/");
      return;
    }

    if (accessToken && !user) {
      const restoreUser = async () => {
        setLoading(true);
        try {
          await getUser();
          if (localStorage.getItem("user")) {
            navigate("/");
          }
        } catch (error) {
          console.error("Unable to restore session:", error);
        } finally {
          setLoading(false);
        }
      };

      restoreUser();
    }
  }, [user, navigate, getUser, setLoading]);

  const isLoginValid = email.trim() !== "" && password !== "" && !validateEmail(email) && !validatePassword(password);

  const submitForm = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const nextEmailError = validateEmail(email);
    const nextPasswordError = validatePassword(password);

    setEmailError(nextEmailError);
    setPasswordError(nextPasswordError);

    if (nextEmailError || nextPasswordError) {
      return;
    }

    setLoading(true);
    try {
      await Login({
        email: email.trim(),
        password,
      });
      navigate("/");
    } catch (error) {
      alert("Login failed. Please check your credentials and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="pad auth-shell" style={{ paddingTop: 60 }}>
      {loading && <LoadingOverlay text="Signing in.."></LoadingOverlay>}
      <div className="auth-mark">M</div>
      <div className="h1">Welcome back</div>
      <div className="muted" style={{ marginTop: 4 }}>Sign in with your school email</div>
      <div style={{ height: 26 }} />
      <form className="auth-form" onSubmit={submitForm} noValidate>
        <div className="field">
          <label>School email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              if (emailError) setEmailError(validateEmail(e.target.value));
            }}
            onBlur={() => setEmailError(validateEmail(email))}
            placeholder="m.onuekwusi@futo.edu.ng"
            className={emailError ? "is-invalid" : ""}
            aria-invalid={Boolean(emailError)}
          />
          {emailError && <p className="field-error">{emailError}</p>}
        </div>

        <div className="field">
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              if (passwordError) setPasswordError(validatePassword(e.target.value));
            }}
            onBlur={() => setPasswordError(validatePassword(password))}
            placeholder="••••••••"
            className={passwordError ? "is-invalid" : ""}
            aria-invalid={Boolean(passwordError)}
          />
          {passwordError && <p className="field-error">{passwordError}</p>}
        </div>

        <div style={{ textAlign: "right", marginBottom: 18 }}><span className="link" style={{ fontSize: 12.5 }}>Forgot password?</span></div>
        <button className="btn btn-primary" type="submit" disabled={!isLoginValid || loading}>
          {loading ? "Signing in..." : "Sign in"}
        </button>
      </form>
      <div className="auth-foot">No account? <span className="link" onClick={() => navigate("/signup")}>Create one</span></div>
    </div>
  );
}
