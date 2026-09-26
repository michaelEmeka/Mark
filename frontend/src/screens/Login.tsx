import "../styles/Login.css";

interface LoginScreenProps {
  active: boolean;
  onSignIn: () => void;
  onGoSignup: () => void;
}

export default function LoginScreen({ active, onSignIn, onGoSignup }: LoginScreenProps) {
  return (
    <div className={`screen ${active ? "active" : ""}`}>
      <div className="pad" style={{ paddingTop: 60 }}>
        <div className="auth-mark">M</div>
        <div className="h1">Welcome back</div>
        <div className="muted" style={{ marginTop: 4 }}>Sign in with your school email</div>
        <div style={{ height: 26 }} />
        <div className="field"><label>School email</label><input type="email" defaultValue="m.onuekwusi@futo.edu.ng" /></div>
        <div className="field"><label>Password</label><input type="password" defaultValue="••••••••" /></div>
        <div style={{ textAlign: "right", marginBottom: 18 }}><span className="link" style={{ fontSize: 12.5 }}>Forgot password?</span></div>
        <button className="btn btn-primary" onClick={onSignIn}>Sign in</button>
        <div className="auth-foot">No account? <span className="link" onClick={onGoSignup}>Create one</span></div>
      </div>
    </div>
  );
}
