import "./ProfileEditScreen.css";
import { useEffect, useState } from "react";
import { BackIcon } from "../components/icons";
import type { User } from "../contexts/UserContext";
import { fetchSets } from "../services/SignupService";

interface AcademicSetOption {
  id: number | string;
  start_year: number | string;
  end_year: number | string;
  department_name?: string;
}

interface ProfileEditScreenProps {
  active: boolean;
  user: User | null;
  onBack: () => void;
  onSave: (payload: {
    username?: string;
    middlename?: string | null;
    push_token?: string | null;
    set?: number | string | null;
  }) => Promise<void> | void;
}

export default function ProfileEditScreen({ active, user, onBack, onSave }: ProfileEditScreenProps) {
  const [username, setUsername] = useState("");
  const [middlename, setMiddlename] = useState("");
  const [pushToken, setPushToken] = useState("");
  const [selectedSet, setSelectedSet] = useState<string>("");
  const [setOptions, setSetOptions] = useState<AcademicSetOption[]>([]);
  const [saving, setSaving] = useState(false);
  const hasFixedSet = Boolean(user?.set_id != null && user.set_id !== "");

  useEffect(() => {
    if (!user) return;
    setUsername(user.username ?? "");
    setMiddlename(user.middlename ?? "");
    setPushToken(user.push_token ?? "");
    setSelectedSet(user.set_id != null ? String(user.set_id) : "");
  }, [user]);

  useEffect(() => {
    if (!user?.department || !user?.school || !user?.university) {
      setSetOptions([]);
      return;
    }

    const departmentId = user.department ?? undefined;
    const schoolId = user.school ?? undefined;
    const universityId = user.university ?? undefined;

    const loadSets = async () => {
      try {
        const availableSets = await fetchSets({
          departmentId,
          schoolId,
          universityId,
        });
        setSetOptions(availableSets);

        if (!selectedSet && user.set_id != null) {
          setSelectedSet(String(user.set_id));
        }
      } catch (error) {
        console.error("Failed to load department sets:", error);
        setSetOptions([]);
      }
    };

    void loadSets();
  }, [user]);

  const handleSubmit = async () => {
    setSaving(true);
    try {
      await onSave({
        username: username.trim(),
        middlename: middlename.trim() || null,
        push_token: pushToken.trim() || null,
        set: selectedSet ? Number(selectedSet) || selectedSet : null,
      });
    } finally {
      setSaving(false);
    }
  };

  const selectedSetLabel = (() => {
    const currentSet = setOptions.find((option) => String(option.id) === selectedSet);
    if (currentSet) {
      return `${currentSet.start_year} / ${currentSet.end_year}`;
    }
    if (user?.set_years) {
      return `${user.set_years.start_year ?? ""} / ${user.set_years.end_year ?? ""}`;
    }
    return "";
  })();

  return (
    <div className={`screen ${active ? "active" : ""}`}>
      <div className="topbar"><div className="backbtn" onClick={onBack}><BackIcon /></div><div className="h2">Edit profile</div></div>
      <div className="pad" style={{ paddingTop: 8 }}>
        <div className="field">
          <label>First name</label>
          <input value={user?.firstname ?? ""} disabled readOnly />
        </div>
        <div className="field">
          <label>Last name</label>
          <input value={user?.lastname ?? ""} disabled readOnly />
        </div>
        <div className="field">
          <label>Username</label>
          <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Enter a username" />
        </div>
        <div className="field">
          <label>Middle name</label>
          <input value={middlename} onChange={(e) => setMiddlename(e.target.value)} placeholder="Optional" />
        </div>
        <div className="field">
          <label>School email</label>
          <input value={user?.email ?? ""} disabled readOnly />
        </div>
        <div className="field-row">
          <div className="field">
            <label>Matric no.</label>
            <input value={user?.reg_number ?? ""} disabled readOnly />
          </div>
          <div className="field">
            <label>Level</label>
            <input value={user?.level_code ? `${user.level_code}L` : ""} disabled readOnly />
          </div>
        </div>
        <div className="field">
          <label>Department</label>
          <input value={user?.department_name ?? ""} disabled readOnly />
        </div>
        <div className="field">
          <label>Set</label>
          {hasFixedSet ? (
            <input value={selectedSetLabel} disabled readOnly />
          ) : (
            <select
              value={selectedSet}
              onChange={(e) => setSelectedSet(e.target.value)}
              disabled={setOptions.length === 0}
            >
              {setOptions.length === 0 ? (
                <option value="">No set available</option>
              ) : (
                setOptions.map((setOption) => (
                  <option key={String(setOption.id)} value={String(setOption.id)}>
                    {setOption.start_year} / {setOption.end_year}
                  </option>
                ))
              )}
            </select>
          )}
        </div>
        <div className="field">
          <label>Device token</label>
          <input value={pushToken} onChange={(e) => setPushToken(e.target.value)} placeholder="Optional device token" />
        </div>
        <button className="btn btn-primary" onClick={handleSubmit} disabled={saving}>
          {saving ? "Saving..." : "Save changes"}
        </button>
      </div>
    </div>
  );
}
