import "../styles/Signup.css";
import { BackIcon } from "../icons";

interface SignupScreenProps {
  active: boolean;
  onSignUp: () => void;
  onBack: () => void;
}

export default function SignupScreen({ active, onSignUp, onBack }: SignupScreenProps) {
  return (
    <div className={`screen ${active ? "active" : ""}`}>
      <div className="topbar" style={{ paddingTop: 22 }}>
        <div className="backbtn" onClick={onBack}><BackIcon /></div>
      </div>
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
      </div>
    </div>
  );
}
