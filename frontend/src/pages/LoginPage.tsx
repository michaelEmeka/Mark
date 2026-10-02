import "./LoginPage.css";
import { Navigate, useNavigate } from "react-router-dom"
import { Login } from "../services/Auth";
import { useUserContext } from "../contexts/UserContext";
import LoadingOverlay from "../components/LoadingOverlay";


export default function LoginPage() {
  const { loading, setLoading } = useUserContext() as {
    loading: boolean;
    setLoading: (value: boolean) => void;
  };
  const navigate = useNavigate();

  const submitForm = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    try {
        let response = await Login({
          email: (e.currentTarget.elements[0] as HTMLInputElement).value,
          password: (e.currentTarget.elements[1] as HTMLInputElement).value
        });
        navigate("/");
    }
    catch (error) {
        alert("Login failed. Please check your credentials and try again.");
    }
    finally {
        setLoading(false);
    }
  };

  return (
    <div className="pad" style={{ paddingTop: 60 }}>
      {loading && <LoadingOverlay text="Signing in.."></LoadingOverlay>}
      <div className="auth-mark">M</div>
      <div className="h1">Welcome back</div>
      <div className="muted" style={{ marginTop: 4 }}>Sign in with your school email</div>
      <div style={{ height: 26 }} />
      <form className="auth-form" onSubmit={submitForm}>
        <div className="field"><label>School email</label><input type="email" placeholder="m.onuekwusi@futo.edu.ng" /></div>
        <div className="field"><label>Password</label><input type="password" placeholder="••••••••" /></div>
      
        <div style={{ textAlign: "right", marginBottom: 18 }}><span className="link" style={{ fontSize: 12.5 }}>Forgot password?</span></div>
        <button className="btn btn-primary" type="submit">Sign in</button>
      </form>
      <div className="auth-foot">No account? <span className="link" onClick={() => navigate("/signup")}>Create one</span></div>
    </div>
  
  );
}
