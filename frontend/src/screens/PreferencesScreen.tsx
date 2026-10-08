import "./PreferencesScreen.css";
import { useEffect, useState } from "react";
import { BackIcon } from "../components/icons";
import type { User } from "../contexts/UserContext";

interface PreferencesScreenProps {
  active: boolean;
  user: User | null;
  onBack: () => void;
  onSave: (payload: { preferences: Record<string, unknown> }) => Promise<void> | void;
}

const defaultPreferences = {
  push_notifications: true,
  email_notifications: false,
  dark_mode: false,
};

export default function PreferencesScreen({ active, user, onBack, onSave }: PreferencesScreenProps) {
  const [preferences, setPreferences] = useState<Record<string, unknown>>(defaultPreferences);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    const stored = (user?.preferences && typeof user.preferences === "object" ? user.preferences : {}) as Record<string, unknown>;
    setPreferences({
      ...defaultPreferences,
      ...stored,
    });
  }, [user]);

  const updatePreference = (key: string, value: boolean) => {
    setPreferences((current) => ({
      ...current,
      [key]: value,
    }));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await onSave({ preferences });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className={`screen ${active ? "active" : ""}`}>
      <div className="topbar"><div className="backbtn" onClick={onBack}><BackIcon /></div><div className="h2">Preferences</div></div>
      <div className="pad" style={{ paddingTop: 8 }}>
        <div className="list-group" style={{ margin: "0 0 16px" }}>
          <div className="pref-row">
            <div className="pref-mid"><div className="pref-title">Push notifications</div><div className="pref-sub">Class reminders, schedule changes</div></div>
            <label className="toggle">
              <input
                type="checkbox"
                checked={Boolean(preferences.push_notifications)}
                onChange={(e) => updatePreference("push_notifications", e.target.checked)}
              />
              <span className="track"><span className="knob" /></span>
            </label>
          </div>
          <div className="pref-row">
            <div className="pref-mid"><div className="pref-title">Email notifications</div><div className="pref-sub">Weekly attendance summary</div></div>
            <label className="toggle">
              <input
                type="checkbox"
                checked={Boolean(preferences.email_notifications)}
                onChange={(e) => updatePreference("email_notifications", e.target.checked)}
              />
              <span className="track"><span className="knob" /></span>
            </label>
          </div>
          <div className="pref-row">
            <div className="pref-mid"><div className="pref-title">Dark mode</div><div className="pref-sub">Off by default in this build</div></div>
            <label className="toggle">
              <input
                type="checkbox"
                checked={Boolean(preferences.dark_mode)}
                onChange={(e) => updatePreference("dark_mode", e.target.checked)}
              />
              <span className="track"><span className="knob" /></span>
            </label>
          </div>
        </div>

        <button className="btn btn-primary" onClick={handleSave} disabled={saving}>
          {saving ? "Saving..." : "Save preferences"}
        </button>
      </div>
    </div>
  );
}
