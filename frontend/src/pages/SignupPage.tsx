import "./SignupPage.css";
import { useNavigate } from "react-router-dom"

interface SignupScreenProps {
  onSignUp: () => void;
}

export default function SignupPage({onSignUp}: SignupScreenProps) {
  const navigate = useNavigate()

  //console.log("loaded signup")
  return (
    <>
      <div className="auth-mark">M</div>
      <div className="pad" style={{ paddingTop: 14 }}>
        <div className="h1">Create account</div>
        <div className="muted" style={{ marginTop: 4 }}>Same details, straight onto your dashboard</div>
        <div style={{ height: 20 }} />
        <div className="field"><label>Full name</label><input placeholder="Chiamaka Nwosu" /></div>
        <div className="field"><label>School email</label><input type="email" placeholder="you@futo.edu.ng" /></div>
        <div className="field-row">
          <div className="field"><label>Matric no.</label><input placeholder="EEE/2021/xxx" /></div>
          <div className="field"><label>Level</label>
            <select defaultValue="400L"><option>100L</option><option>200L</option><option>300L</option><option>400L</option><option>500L</option></select>
          </div>
        </div>
        <div className="field"><label>Department</label>
          <select defaultValue="Electrical & Electronic Engineering">
            <option>Electrical & Electronic Engineering</option><option>Mechanical Engineering</option><option>Chemical Engineering</option><option>Computer Engineering</option>
          </select>
        </div>
        <div className="field-row">
          <div className="field"><label>Password</label><input type="password" placeholder="••••••••" /></div>
          <div className="field"><label>Confirm</label><input type="password" placeholder="••••••••" /></div>
        </div>
        <button className="btn btn-primary" onClick={onSignUp}>Sign up</button>
        <div className="auth-foot">Have and account? <span className="link" onClick={()=>navigate("/login")}>Login</span></div>
      </div>
    </>
  );
}
