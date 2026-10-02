import "./ProfileEditScreen.css";
import { BackIcon } from "../components/icons";

interface ProfileEditScreenProps {
  active: boolean;
  onBack: () => void;
  onSave: () => void;
}

export default function ProfileEditScreen({ active, onBack, onSave }: ProfileEditScreenProps) {
  return (
    <div className={`screen ${active ? "active" : ""}`}>
      <div className="topbar"><div className="backbtn" onClick={onBack}><BackIcon /></div><div className="h2">Edit profile</div></div>
      <div className="pad" style={{ paddingTop: 8 }}>
        <div className="field"><label>Full name</label><input defaultValue="Michael Onuekwusi" /></div>
        <div className="field"><label>School email</label><input defaultValue="m.onuekwusi@futo.edu.ng" /></div>
        <div className="field-row">
          <div className="field"><label>Matric no.</label><input defaultValue="EEE/2021/xxx" /></div>
          <div className="field"><label>Level</label><select defaultValue="400L"><option>300L</option><option>400L</option><option>500L</option></select></div>
        </div>
        <div className="field"><label>Department</label><select defaultValue="Electrical & Electronic Engineering"><option>Electrical & Electronic Engineering</option><option>Mechanical Engineering</option></select></div>
        <button className="btn btn-primary" onClick={onSave}>Save changes</button>
      </div>
    </div>
  );
}
