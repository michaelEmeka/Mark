import "./SignupPage.css";
import { useNavigate } from "react-router-dom";
import { createUser, fetchDepartments, fetchLevels, fetchSchools, fetchUnis, type Department, type Level, type School, type University } from "../services/SignupService";
import { useEffect, useState } from "react";

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

interface SignupScreenProps {
  onSignUp: () => void;
}

export default function SignupPage({ onSignUp }: SignupScreenProps) {
  const navigate = useNavigate();
  const [universities, setUniversities] = useState<University[]>([]);
  const [schools, setSchools] = useState<School[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [levels, setLevels] = useState<Level[]>([]);

  const [selectedUniversity, setSelectedUniversity] = useState<string>("");
  const [selectedSchool, setSelectedSchool] = useState<string>("");
  const [selectedDepartment, setSelectedDepartment] = useState<string>("");
  const [selectedLevel, setSelectedLevel] = useState<string>("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [matricNumber, setMatricNumber] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [firstNameError, setFirstNameError] = useState("");
  const [lastNameError, setLastNameError] = useState("");
  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [confirmPasswordError, setConfirmPasswordError] = useState("");
  const [formError, setFormError] = useState("");

  const validateName = (value: string, field: string) => {
    if (!value.trim()) return `${field} is required.`;
    return "";
  };

  const validateEmail = (value: string) => {
    if (!value.trim()) return "Email is required.";
    if (!emailRegex.test(value.trim())) return "Enter a valid email address.";
    return "";
  };

  const validatePassword = (value: string) => {
    if (!value) return "Password is required.";
    if (value.length < 8) return "Password must be at least 8 characters.";
    return "";
  };

  useEffect(() => {
    const loadUniversities = async () => {
      try {
        const data = await fetchUnis();
        setUniversities(data);
      } catch {
        console.log("Couldn't retrieve universities..");
      }
    };

    const loadLevels = async () => {
      try {
        const data = await fetchLevels();
        setLevels(data);
      } catch {
        console.log("Couldn't retrieve levels..");
      }
    };

    loadUniversities();
    loadLevels();
  }, []);

  useEffect(() => {
    const loadSchools = async () => {
      if (!selectedUniversity) {
        setSchools([]);
        setSelectedSchool("");
        return;
      }

      try {
        const data = await fetchSchools(selectedUniversity);
        setSchools(data);
        setSelectedSchool("");
        setDepartments([]);
        setSelectedDepartment("");
      } catch {
        console.log("Couldn't retrieve schools for the selected university..");
      }
    };

    loadSchools();
  }, [selectedUniversity]);

  useEffect(() => {
    const loadDepartments = async () => {
      if (!selectedSchool) {
        setDepartments([]);
        setSelectedDepartment("");
        return;
      }

      try {
        const data = await fetchDepartments(selectedSchool);
        setDepartments(data);
        setSelectedDepartment("");
      } catch {
        console.log("Couldn't retrieve departments for the selected school..");
      }
    };

    loadDepartments();
  }, [selectedSchool]);

  const isSignupComplete =
    selectedUniversity !== "" &&
    selectedSchool !== "" &&
    selectedDepartment !== "" &&
    selectedLevel !== "" &&
    firstName.trim() !== "" &&
    lastName.trim() !== "" &&
    matricNumber.trim() !== "" &&
    email.trim() !== "" &&
    password !== "" &&
    confirmPassword !== "" &&
    !validateName(firstName, "First name") &&
    !validateName(lastName, "Last name") &&
    !validateEmail(email) &&
    !validatePassword(password) &&
    password === confirmPassword;

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setFormError("");

    const nextFirstNameError = validateName(firstName, "First name");
    const nextLastNameError = validateName(lastName, "Last name");
    const nextEmailError = validateEmail(email);
    const nextPasswordError = validatePassword(password);
    const nextConfirmError = !confirmPassword
      ? "Please confirm your password."
      : password !== confirmPassword
        ? "Passwords do not match."
        : "";

    setFirstNameError(nextFirstNameError);
    setLastNameError(nextLastNameError);
    setEmailError(nextEmailError);
    setPasswordError(nextPasswordError);
    setConfirmPasswordError(nextConfirmError);

    if (nextFirstNameError || nextLastNameError || nextEmailError || nextPasswordError || nextConfirmError) {
      return;
    }

    try {
      const selectedUni = universities.find((uni) => String(uni.id) === selectedUniversity);
      const selectedSch = schools.find((school) => String(school.id) === selectedSchool);
      const selectedDept = departments.find((dept) => String(dept.id) === selectedDepartment);
      const selectedLevelItem = levels.find((levelItem) => String(levelItem.id) === selectedLevel);

      await createUser({
        email: email.trim(),
        username: `${firstName.trim()} ${lastName.trim()}`,
        firstname: firstName.trim(),
        lastname: lastName.trim(),
        middlename: "",
        password,
        reg_number: matricNumber.trim(),
        university: selectedUni?.id as number | undefined,
        school: selectedSch?.id as number,
        department: selectedDept?.id as number,
        level: selectedLevelItem?.id as number,
      });

      if (onSignUp) onSignUp();
      navigate("/login");
    } catch (error: any) {
      const backendErrors = error?.response?.data;
      const errorMessage = backendErrors
        ? Object.values(backendErrors)
            .flatMap((item) => Array.isArray(item) ? item : [item])
            .map((item) => String(item))
            .join(" ")
        : "Account creation failed. Please review the details and try again.";

      setFormError(errorMessage || "Account creation failed. Please review the details and try again.");
    }
  };

  return (
    <div className="pad auth-shell" style={{ paddingTop: 60 }}>
      <div className="auth-mark">FP</div>
      <div className="h1">Create account</div>
      <div className="muted" style={{ marginTop: 4 }}>Same details, straight onto your dashboard</div>
      <div style={{ height: 20 }} />

      <form onSubmit={handleSubmit} noValidate>
        <div className="field-row">
          <div className="field">
            <label>First name</label>
            <input
              value={firstName}
              onChange={(e) => {
                setFirstName(e.target.value);
                if (firstNameError) setFirstNameError(validateName(e.target.value, "First name"));
              }}
              onBlur={() => setFirstNameError(validateName(firstName, "First name"))}
              placeholder="Chiamaka"
              className={firstNameError ? "is-invalid" : ""}
              aria-invalid={Boolean(firstNameError)}
            />
            {firstNameError && <p className="field-error">{firstNameError}</p>}
          </div>

          <div className="field">
            <label>Last name</label>
            <input
              value={lastName}
              onChange={(e) => {
                setLastName(e.target.value);
                if (lastNameError) setLastNameError(validateName(e.target.value, "Last name"));
              }}
              onBlur={() => setLastNameError(validateName(lastName, "Last name"))}
              placeholder="Nwosu"
              className={lastNameError ? "is-invalid" : ""}
              aria-invalid={Boolean(lastNameError)}
            />
            {lastNameError && <p className="field-error">{lastNameError}</p>}
          </div>
        </div>

        <div className="field">
          <label>University</label>
          <select value={selectedUniversity} onChange={(e) => setSelectedUniversity(String(e.target.value))}>
            <option value="">Select university</option>
            {universities.map((university) => (
              <option key={university.id} value={String(university.id)}>{university.name}</option>
            ))}
          </select>
        </div>

        <div className="field">
          <label>School</label>
          <select value={selectedSchool} onChange={(e) => setSelectedSchool(String(e.target.value))} disabled={!selectedUniversity || schools.length === 0}>
            <option value="">{selectedUniversity ? "Select school" : "Select a university first"}</option>
            {schools.map((school) => (
              <option key={school.id} value={String(school.id)}>{school.name}</option>
            ))}
          </select>
        </div>

        <div className="field">
          <label>Department</label>
          <select value={selectedDepartment} onChange={(e) => setSelectedDepartment(String(e.target.value))} disabled={!selectedSchool || departments.length === 0}>
            <option value="">{selectedSchool ? "Select department" : "Select a school first"}</option>
            {departments.map((department) => (
              <option key={department.id} value={String(department.id)}>{department.name}</option>
            ))}
          </select>
        </div>

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
            placeholder="you@futo.edu.ng"
            className={emailError ? "is-invalid" : ""}
            aria-invalid={Boolean(emailError)}
          />
          {emailError && <p className="field-error">{emailError}</p>}
        </div>

        <div className="field-row">
          <div className="field">
            <label>Matric no.</label>
            <input
              value={matricNumber}
              onChange={(e) => setMatricNumber(e.target.value)}
              placeholder="EEE/2021/xxx"
            />
          </div>
          <div className="field"><label>Level</label>
            <select value={selectedLevel} onChange={(e) => setSelectedLevel(String(e.target.value))}>
              <option value="">Select level</option>
              {levels.map((levelItem) => (
                <option key={levelItem.id} value={String(levelItem.id)}>{levelItem.code}L</option>
              ))}
            </select>
          </div>
        </div>

        <div className="field-row">
          <div className="field">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                if (passwordError) setPasswordError(validatePassword(e.target.value));
                if (confirmPasswordError && confirmPassword) {
                  setConfirmPasswordError(e.target.value === confirmPassword ? "" : "Passwords do not match.");
                }
              }}
              onBlur={() => setPasswordError(validatePassword(password))}
              placeholder="••••••••"
              className={passwordError ? "is-invalid" : ""}
              aria-invalid={Boolean(passwordError)}
            />
            {passwordError && <p className="field-error">{passwordError}</p>}
          </div>
          <div className="field">
            <label>Confirm</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => {
                setConfirmPassword(e.target.value);
                if (confirmPasswordError) {
                  setConfirmPasswordError(
                    password !== e.target.value ? "Passwords do not match." : ""
                  );
                }
              }}
              onBlur={() => {
                if (!confirmPassword) {
                  setConfirmPasswordError("Please confirm your password.");
                } else if (password !== confirmPassword) {
                  setConfirmPasswordError("Passwords do not match.");
                } else {
                  setConfirmPasswordError("");
                }
              }}
              placeholder="••••••••"
              className={confirmPasswordError ? "is-invalid" : ""}
              aria-invalid={Boolean(confirmPasswordError)}
            />
            {confirmPasswordError && <p className="field-error">{confirmPasswordError}</p>}
          </div>
        </div>

        {formError && <p className="form-error">{formError}</p>}

        <button className="btn btn-primary" type="submit" disabled={!isSignupComplete}>
          Sign up
        </button>
        <div className="auth-foot">Have and account? <span className="link" onClick={() => navigate("/login")}>Login</span></div>
      </form>
    </div>
  );
}
