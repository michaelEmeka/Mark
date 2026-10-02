# Mark — student app (TypeScript / Vite)

Same component breakdown as the JS version, converted to .tsx/.ts with
proper prop types and a shared types.ts for the domain model.

src/
  types.ts                     — Role, Day, ScreenId, TabId, TimetableEntry,
                                  TimetableEntrySchedule, WeekStripDay
  main.tsx                     — Vite entry point
  components/
    App.tsx / App.css          — root: screen/role/day state, shell + statusbar
    RoleSwitch.tsx / .css      — preview-only student/course-rep toggle
    TabBar.tsx / .css          — bottom nav
    icons.tsx                  — shared inline SVG icons
    screens/
      LoginScreen, SignupScreen, DashboardScreen, TimetableScreen,
      CreateScheduleScreen (course-rep only), ProfileScreen,
      ProfileEditScreen, PreferencesScreen, AutomationScreen (course-rep only)
      — each takes a typed props interface (active, callbacks, role, etc.)
  data/
    mockData.ts                 — typed ENTRIES/SCHEDULES arrays + nav helpers
  styles/
    theme.css                   — CSS variables (white background, blue accent)
    common.css                  — classes shared by 3+ screens

Root config:
  index.html, vite.config.ts, tsconfig.json, tsconfig.node.json, package.json
  — standard `npm create vite@latest -- --template react-ts` layout, so this
  folder runs as-is: `npm install && npm run dev`.

Screens with no unique CSS (Signup, CreateSchedule, ProfileEdit, Preferences,
Automation) still get their own .css file — they lean entirely on common.css,
kept for a predictable one-component-one-css-file pattern.
