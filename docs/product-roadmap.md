# Product Roadmap — Matchday

> Du baust dieses Projekt selbst — Schritt für Schritt, ohne Agent. Hak jede Task ab wenn du fertig bist.

**Status:** 0/65 Tasks erledigt
**Aktuelle Phase:** Phase 0 — Foundation & TypeScript Migration

---

## Build Philosophy

1. **Jede Phase ergibt eine lauffähige App.** Nach jeder abgeschlossenen Phase kannst du die App starten und zeigen was du gebaut hast.
2. **Erst Infrastruktur, dann Features.** TypeScript-Migration und Projektstruktur kommen zuerst — alle Game-Mechaniken bauen auf einem sauberen, typisierten Fundament auf.
3. **Magic Moment zuerst.** Der komplette Loop (Prediction → Result → Badge → Leaderboard) funktioniert am Ende von Phase 2. Alles danach ist Verbesserung.
4. **Tests schreiben während du implementierst.** Nicht am Ende. Jedes Mal wenn du neue Logik schreibst, schreibst du auch den Test dazu.
5. **Nur echte Daten.** Jedes Spiel im Feed ist ein echtes Match aus der Football API. Keine Fake-Daten in Production.
6. **Nach jeder Phase: PR + Review.** Push deine Arbeit als Pull Request und lass [CodeRabbit](https://coderabbit.ai) (kostenlos für Open Source) drüber schauen. Das findet Fehler die du selbst nicht siehst.
7. **Der Code ist das Portfolio.** Jede Architektur-Entscheidung sollte eine sein, die du im Interview erklären kannst. Lieber verständlich als clever.

---

## Bevor du anfängst: Was du lernen wirst

Diese drei Dinge sind neu für dich. Du musst sie nicht vorher komplett beherrschen — du lernst sie direkt an deinem Code. Aber ein kurzer Überblick hilft, damit du weißt warum du was tust.

### Was ist TypeScript?

JavaScript mit Typen. Das bedeutet: du sagst dem Code im Voraus, welche Art von Daten irgendwo rein- und rauskommt.

**Ohne TypeScript (dein aktueller Code):**
```javascript
function MatchCard({ item, onPress }) {
  // Was ist "item"? Was für Felder hat es? Unbekannt.
}
```

**Mit TypeScript:**
```typescript
interface Match {
  fixture_id: number;
  teamhome_name: string;
  goal_home: number | null;
}

function MatchCard({ item, onPress }: { item: Match; onPress: () => void }) {
  // Jetzt weiß VS Code: item.teamhome_name ist ein string.
  // item.goal_homee → Fehler! Das Feld heißt nicht so.
}
```

Der Vorteil: dein Editor findet Tippfehler, falsche Datentypen und fehlende Felder — bevor du die App startest. Du brauchst weniger `console.log` zum Debuggen.

**Lies das bevor du Phase 0 anfängst (je ~10 Minuten):**
- [TypeScript in 5 minutes](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html) — offiziell, kurz, direkt
- [Interfaces verstehen](https://www.typescriptlang.org/docs/handbook/2/objects.html) — du wirst viele `interface`s schreiben

Du musst nicht alles auf einmal lesen. Lies die Basics, fang an zu tippen, und schau nach wenn du auf etwas stößt das du nicht kennst.

---

### Was ist ein Test?

Ein Test ist Code der deinen anderen Code überprüft. Du beschreibst: "Wenn ich X reingebe, erwarte ich Y raus." Wenn Y nicht stimmt, schlägt der Test fehl und du weißt wo das Problem ist.

**Ein echter Test aus deinem Projekt (TASK-010):**
```typescript
test('zeigt LIVE-Status wenn Spiel läuft', () => {
  // Render die MatchCard mit einem laufenden Spiel
  render(<MatchCard item={{ fixture_status: '1h', ...restOfMatch }} onPress={() => {}} />);

  // Prüfe: ist der Text "LIVE" auf dem Screen?
  expect(screen.getByText('LIVE')).toBeTruthy();
});
```

Das ist alles. `test()` beschreibt was getestet wird. `render()` rendert die Komponente. `expect()` prüft das Ergebnis.

**Warum testet man?** Stell dir vor du änderst in Phase 3 etwas an `MatchCard`. Ohne Test merkst du erst viel später (oder gar nicht) dass der LIVE-Status jetzt kaputt ist. Mit Test: sofort roter Balken, sofort wissen wo das Problem ist.

**Lies das wenn du zu TASK-010 kommst:**
- [Testing Library — Getting Started](https://testing-library.com/docs/react-testing-library/intro/) — erklärt die Grundidee in 5 Minuten
- [Jest expect API](https://jestjs.io/docs/expect) — die Befehle die du am häufigsten brauchst

---

### Was ist CI/CD?

**CI (Continuous Integration)** bedeutet: jedes Mal wenn du Code auf GitHub pushst, läuft automatisch eine Reihe von Prüfungen. TypeScript-Fehler? Test rot? Linting-Problem? GitHub zeigt dir ✅ oder ❌.

**CD (Continuous Deployment)** würde bedeuten: bei ✅ wird automatisch deployed. Das brauchst du für dieses Projekt noch nicht.

Für dich ist CI eine einzige Datei: `.github/workflows/ci.yml`. Die sieht so aus:

```yaml
name: CI

on: [push, pull_request]   # Wann soll das laufen?

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4     # Code herunterladen
      - uses: actions/setup-node@v4   # Node installieren
      - run: npm ci                   # Dependencies installieren
      - run: npx tsc --noEmit         # TypeScript prüfen
      - run: npx jest --ci            # Tests ausführen
```

Das ist es. Eine YAML-Datei, die GitHub sagt was es tun soll. Du schreibst sie einmal in TASK-013 und dann läuft sie automatisch bei jedem Push.

**Warum ist das für Bewerbungen wichtig?** Ein GitHub-Repo mit grünem CI-Badge zeigt: diese Person arbeitet wie ein professionelles Team. Die Tests laufen nicht nur lokal, sie laufen in einer sauberen Umgebung bei jedem Commit.

---

## Phase 0: Foundation & TypeScript Migration

> **Ziel:** Der gesamte Frontend-Code ist auf TypeScript migriert, alle gemeinsamen Typen sind definiert, Zustand-Stores sind eingerichtet, ein typisierter API-Client ist vorhanden, und CI läuft. Die App bootet und alle bestehenden Funktionen funktionieren noch.

**Referenz-Abschnitte für diese Phase:**
- PRD: § 2. Technical Architecture, § 9. Design System, § 10. Auth Implementation
- Vision: § 5. Design Direction > Design Tokens

---

- [ ] **TASK-001** — TypeScript Strict Mode aktivieren und alle gemeinsamen Typen definieren
  Files: `tsconfig.json`, `types/index.ts`

  **Was du lernst:** TypeScript-Interfaces und strikte Typisierung.

  **Schritt für Schritt:**

  1. Öffne `tsconfig.json`. Füge diese drei Zeilen in `"compilerOptions"` hinzu:
     ```json
     "strict": true,
     "noImplicitAny": true,
     "strictNullChecks": true
     ```
     `strict: true` bedeutet: kein `any` erlaubt, `null`-Checks sind Pflicht. Das klingt streng — das ist es auch, aber genau das macht deinen Code sicher.

  2. Erstelle `types/index.ts`. Das ist deine zentrale Datei für alle Typen im Projekt. Schreib die Typen für alle Datenbankentitäten ab — orientiere dich an den Pydantic-Modellen im Backend (die `class Match(BaseModel)` usw.):
     ```typescript
     export interface Match {
       fixture_id: number;
       fixture_date: string;
       fixture_status: string;
       league_name: string;
       teamhome_name: string;
       teamhome_logo: string;
       teamaway_name: string;
       teamaway_logo: string;
       goal_home: number | null;    // "| null" = kann auch null sein
       goal_away: number | null;
       odd_home: number | null;
       odd_draw: number | null;
       odd_away: number | null;
     }

     export interface Bet {
       match_id: string;
       amount: number;
       odds: number;
       prediction: 'home' | 'away' | 'draw';  // nur diese drei Werte erlaubt
     }

     export interface UserProfile {
       id: string;
       username: string;
       balance: number;
       stats: UserStats;
     }

     export interface UserStats {
       total_predictions: number;
       total_wins: number;
       win_rate: number;
       current_streak: number;
       longest_streak: number;
     }

     // Weitere Typen: BetWithMatch, LeaderboardEntry, Achievement,
     // UserAchievement, FriendSummary — anhand der API-Responses in prd.md § 4 definieren
     ```

  3. Führe `npx tsc --noEmit` aus. Das kompiliert den Code ohne Output — nur um Fehler zu zeigen. Wahrscheinlich werden viele rote Fehler erscheinen. Das ist normal und erwartet. Du wirst sie in den nächsten Tasks beheben.

  **Verifizieren:** `npx tsc --noEmit` läuft durch (oder zeigt nur Fehler in .jsx-Dateien — die migrierst du noch).

---

- [ ] **TASK-002** — Typisierten API-Client erstellen (`lib/api.ts`)
  Files: `supabase/supabase.ts`, `lib/api.ts`

  **Was du lernst:** Wie man eine zentrale, typisierte API-Schicht baut.

  **Schritt für Schritt:**

  1. Erstelle den Ordner `lib/` und darin `lib/api.ts`. Diese Datei ersetzt `supabase/api.js` als dein zentraler Ort für alle API-Calls.

  2. Jede Funktion bekommt einen Rückgabe-Typ mit `Promise<TypName>`:
     ```typescript
     import { Match, Bet, UserProfile } from '../types';

     const BASE_URL = process.env.EXPO_PUBLIC_API_URL;

     async function getHeaders(token: string): Promise<HeadersInit> {
       return {
         'Content-Type': 'application/json',
         'Authorization': `Bearer ${token}`,
       };
     }

     export async function getMatchesByRounds(token: string): Promise<{ current: { round: number; matches: Match[] }[] }> {
       const res = await fetch(`${BASE_URL}/matches/rounds`, {
         headers: await getHeaders(token),
       });
       if (!res.ok) throw new Error('Failed to fetch matches');
       return res.json();
     }

     export async function placeBet(token: string, bet: Bet): Promise<{ message: string }> {
       const res = await fetch(`${BASE_URL}/bets/`, {
         method: 'POST',
         headers: await getHeaders(token),
         body: JSON.stringify(bet),
       });
       if (!res.ok) throw new Error('Failed to place bet');
       return res.json();
     }
     // ... weitere Funktionen für alle Endpoints aus prd.md § 4
     ```

  3. Schreib Funktionen für: `getBets`, `deleteBet`, `getUserProfile`, `getLeaderboard`, `getAchievements`, `followUser`, `unfollowUser`, `getFriendProfile`.

  4. Füge in `supabase/api.js` oben einen Kommentar ein: `// DEPRECATED — use lib/api.ts instead`

  **Verifizieren:** Importiere `getMatchesByRounds` in einer Datei. VS Code sollte dir Autocomplete auf dem Rückgabewert anbieten.

---

- [ ] **TASK-003** — Zod-Schemas für alle API-Responses hinzufügen
  Files: `lib/schemas.ts`

  **Was du lernst:** Den Unterschied zwischen Compile-Zeit-Typen (TypeScript) und Laufzeit-Validierung (Zod).

  **Konzept zuerst:** TypeScript prüft deinen Code bevor er läuft. Aber wenn zur Laufzeit die API plötzlich ein Feld zurückgibt das `null` ist statt einer Zahl — fliegt dein Code. Zod prüft die Daten *wenn sie ankommen* und wirft einen verständlichen Fehler statt einem kryptischen `Cannot read property of undefined`.

  **Schritt für Schritt:**

  1. Installiere Zod: `npx expo install zod`

  2. Erstelle `lib/schemas.ts`:
     ```typescript
     import { z } from 'zod';

     // z.object() beschreibt ein Objekt
     // z.string(), z.number(), z.nullable() — die Typen
     export const matchSchema = z.object({
       fixture_id: z.number(),
       fixture_date: z.string(),
       fixture_status: z.string(),
       teamhome_name: z.string(),
       teamaway_name: z.string(),
       goal_home: z.number().nullable(),
       goal_away: z.number().nullable(),
       odd_home: z.number().nullable(),
       odd_draw: z.number().nullable(),
       odd_away: z.number().nullable(),
     });

     // TypeScript-Typ automatisch aus dem Schema ableiten
     export type Match = z.infer<typeof matchSchema>;
     // Kein manuelles interface mehr nötig — Zod generiert es

     export const matchArraySchema = z.array(matchSchema);
     // ... weitere Schemas für alle Response-Typen
     ```

  3. In `lib/api.ts` jede Response durch das Schema jagen:
     ```typescript
     export async function getMatches(token: string): Promise<Match[]> {
       const res = await fetch(`${BASE_URL}/matches/`);
       const data = await res.json();
       return matchArraySchema.parse(data); // wirft Fehler wenn Daten falsch sind
     }
     ```

  **Verifizieren:** Ändere im Schema einen Typ auf einen falschen Wert und ruf die Funktion auf. Zod sollte einen Fehler mit einer klaren Meldung werfen.

---

- [ ] **TASK-004** — Zustand-Stores für Auth- und User-State einrichten
  Files: `store/authStore.ts`, `store/userStore.ts`

  **Was du lernst:** State Management — wann `useState` nicht mehr reicht.

  **Konzept zuerst:** Im Moment hast du z.B. den eingeloggten User oder den Token vielleicht in mehreren Komponenten als `useState`. Das Problem: wenn sich der Token ändert, müssen alle Komponenten einzeln aktualisiert werden. Zustand ist eine globale State-Bibliothek — ein Store, den jede Komponente lesen und schreiben kann, ohne Props durchzureichen.

  **Vergleich:**
  ```typescript
  // Ohne Zustand: Token in jeder Komponente übergeben
  <MatchesScreen token={token} />
  <UserScreen token={token} />
  <BetScreen token={token} />

  // Mit Zustand: jede Komponente liest direkt
  const token = useAuthStore((state) => state.token);
  ```

  **Schritt für Schritt:**

  1. Installiere: `npx expo install zustand expo-secure-store`

  2. Erstelle `store/authStore.ts`:
     ```typescript
     import { create } from 'zustand';
     import * as SecureStore from 'expo-secure-store';
     import { Session } from '@supabase/supabase-js';

     // Definiere den Shape des Stores
     interface AuthState {
       token: string | null;
       session: Session | null;
       setSession: (session: Session) => void;
       clearSession: () => void;
     }

     // create() gibt einen Hook zurück
     export const useAuthStore = create<AuthState>((set) => ({
       token: null,
       session: null,

       setSession: (session) => {
         // Token sicher auf dem Gerät speichern
         SecureStore.setItemAsync('jwt', session.access_token);
         set({ token: session.access_token, session });
       },

       clearSession: () => {
         SecureStore.deleteItemAsync('jwt');
         set({ token: null, session: null });
       },
     }));
     ```

  3. Erstelle `store/userStore.ts` analog mit `{ user: UserProfile | null, setUser, updateBalance }`.

  4. Wie du den Store in einer Komponente benutzt:
     ```typescript
     // Lesen
     const token = useAuthStore((state) => state.token);
     // Schreiben
     const setSession = useAuthStore((state) => state.setSession);
     setSession(mySession);
     ```

  **Verifizieren:** Importiere `useAuthStore` in `LoginScreen`, ruf `setSession` nach erfolgreichem Login auf, navigiere zu einer anderen Screen und lies `token` dort aus — er sollte da sein.

---

- [ ] **TASK-005** — `app/index.jsx` → `app/index.tsx` mit Auth-Guard migrieren
  Files: `app/index.tsx`

  **Was du lernst:** Deinen ersten JSX → TSX Schritt machen.

  **Schritt für Schritt:**

  1. Benenne die Datei um: `index.jsx` → `index.tsx` (einfach im Explorer umbenennen oder `mv app/index.jsx app/index.tsx`).

  2. TypeScript wird sofort Fehler zeigen. Das ist normal — bearbeite sie einen nach dem anderen.

  3. Implementiere den Auth-Guard:
     ```typescript
     import { useEffect } from 'react';
     import { useRouter } from 'expo-router';
     import * as SecureStore from 'expo-secure-store';
     import { supabase } from '../supabase/supabase';
     import { useAuthStore } from '../store/authStore';

     export default function Index() {
       const router = useRouter();
       const setSession = useAuthStore((state) => state.setSession);

       useEffect(() => {
         async function checkAuth() {
           const token = await SecureStore.getItemAsync('jwt');
           if (token) {
             const { data } = await supabase.auth.getSession();
             if (data.session) {
               setSession(data.session);
               router.replace('/screens/MatchesScreen');
               return;
             }
           }
           router.replace('/screens/LoginScreen');
         }
         checkAuth();
       }, []);

       return null; // Keine UI — nur Weiterleitung
     }
     ```

  **Verifizieren:** Lösche den gespeicherten Token (oder log aus), starte die App neu — sie landet auf LoginScreen. Log dich ein, starte neu — sie landet auf MatchesScreen.

---

- [ ] **TASK-006** — `LoginScreen.jsx` → `LoginScreen.tsx` migrieren
  Files: `app/screens/LoginScreen.tsx`

  **Was du lernst:** `react-hook-form` mit Zod-Validierung — professionelle Formular-Handhabung.

  **Konzept zuerst:** Aktuell hast du wahrscheinlich für jedes Input-Feld ein `useState`. `react-hook-form` zentralisiert das — weniger Re-Renders, eingebaute Validierung, konsistente Fehler-Anzeige. Das sieht in Interviews sehr gut aus.

  **Schritt für Schritt:**

  1. Installiere: `npx expo install react-hook-form @hookform/resolvers zod`

  2. Definiere das Formular-Schema mit Zod:
     ```typescript
     import { z } from 'zod';
     import { useForm, Controller } from 'react-hook-form';
     import { zodResolver } from '@hookform/resolvers/zod';

     const loginSchema = z.object({
       email: z.string().email('Ungültige E-Mail'),
       password: z.string().min(6, 'Mindestens 6 Zeichen'),
     });

     type LoginFormData = z.infer<typeof loginSchema>;
     ```

  3. Ersetze die `useState`-Felder durch `useForm`:
     ```typescript
     const { control, handleSubmit, formState: { errors } } = useForm<LoginFormData>({
       resolver: zodResolver(loginSchema),
     });

     const onSubmit = async (data: LoginFormData) => {
       // data.email und data.password sind jetzt validiert
       const { data: authData, error } = await supabase.auth.signInWithPassword({
         email: data.email,
         password: data.password,
       });
       if (error) { /* Fehler anzeigen */ return; }
       setSession(authData.session!);
       router.replace('/screens/MatchesScreen');
     };
     ```

  4. Jedes TextInput in ein `<Controller>` einwickeln:
     ```typescript
     <Controller
       control={control}
       name="email"
       render={({ field: { onChange, value } }) => (
         <TextInput
           value={value}
           onChangeText={onChange}
           // ... deine bestehenden StyleSheet-Props
         />
       )}
     />
     {errors.email && <Text>{errors.email.message}</Text>}
     ```

  **Verifizieren:** Tippe eine ungültige E-Mail → Fehlermeldung erscheint. Korrekte Credentials → navigate zu MatchesScreen.

---

- [ ] **TASK-007** — `RegisterScreen.jsx` → `RegisterScreen.tsx` migrieren
  Files: `app/screens/RegisterScreen.tsx`

  **Was du lernst:** Dasselbe Muster wie TASK-006 anwenden — das wird jetzt schneller gehen.

  **Schritt für Schritt:**

  1. Schema:
     ```typescript
     const registerSchema = z.object({
       email: z.string().email(),
       password: z.string().min(8, 'Mindestens 8 Zeichen'),
       username: z.string().min(3).max(50),
     });
     ```

  2. Die Passwort-Stärke-Bar bleibt wie sie ist — aber statt `useState` für den Passwort-Wert nutzt du `watch('password')` von react-hook-form:
     ```typescript
     const password = watch('password') ?? '';
     const strengthSegments = Math.min(Math.floor(password.length / 3), 3);
     ```

  3. Submit ruft `POST /auth/register` auf. Fehlerbehandlung: Status 400 mit "Username already taken" → Inline-Fehler "USERNAME TAKEN" unter dem username-Feld.

  **Verifizieren:** Mit neuen Credentials registrieren → landet auf MatchesScreen. Doppelter Username → Fehler erscheint.

---

- [ ] **TASK-008** — Typisierten Custom Hook `useMatches` erstellen
  Files: `hooks/useMatches.ts`

  **Was du lernst:** Custom Hooks — Datenfetch-Logik aus Komponenten herausziehen.

  **Konzept zuerst:** Im Moment hast du in `MatchesScreen` wahrscheinlich ein `useEffect` das die Matches fetcht, plus `useState` für loading/error/data. Das sind drei Dinge die immer zusammengehören. Ein Custom Hook bündelt sie — und du kannst die gleiche Logik in mehreren Screens nutzen ohne Code zu kopieren.

  **Vergleich:**
  ```typescript
  // Vorher — alles in der Komponente:
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => { fetch(...).then(setMatches) }, []);

  // Nachher — ein Hook:
  const { matches, loading, error } = useMatches();
  ```

  **Schritt für Schritt:**

  1. Erstelle den Ordner `hooks/` und darin `hooks/useMatches.ts`:
     ```typescript
     import { useState, useEffect, useCallback } from 'react';
     import { getMatchesByRounds } from '../lib/api';
     import { useAuthStore } from '../store/authStore';

     interface MatchRound {
       round: number;
       matches: Match[];
     }

     export function useMatches() {
       const token = useAuthStore((state) => state.token);
       const [matches, setMatches] = useState<MatchRound[]>([]);
       const [loading, setLoading] = useState(true);
       const [error, setError] = useState<string | null>(null);

       const fetchMatches = useCallback(async () => {
         if (!token) return;
         try {
           setLoading(true);
           setError(null);
           const data = await getMatchesByRounds(token);
           setMatches(data.current ?? []);
         } catch (e) {
           setError('Feed nicht verfügbar.');
         } finally {
           setLoading(false);
         }
       }, [token]);

       useEffect(() => {
         fetchMatches();
       }, [fetchMatches]);

       return { matches, loading, error, refetch: fetchMatches };
     }
     ```

  2. Der `useCallback` um `fetchMatches` verhindert, dass der `useEffect` bei jedem Render neu feuert — wichtig um Endlos-Loops zu vermeiden.

  **Verifizieren:** Importiere den Hook in MatchesScreen, ersetze den bestehenden Fetch-Code — die Matches sollten weiterhin laden.

---

- [ ] **TASK-009** — `MatchesScreen.jsx` → `MatchesScreen.tsx` migrieren mit `useMatches`
  Files: `app/screens/MatchesScreen.tsx`

  **Was du lernst:** Eine bestehende Komponente sauber tipisieren.

  **Schritt für Schritt:**

  1. Datei umbenennen: `.jsx` → `.tsx`
  2. Ersetze den Fetch-Code durch: `const { matches, loading, error, refetch } = useMatches();`
  3. Extrahiere `MatchCard` in eine eigene Datei `components/MatchCard.tsx` (TASK-010 folgt direkt danach).
  4. Tipisiere die Props der verbleibenden Komponenten direkt in der Datei:
     ```typescript
     interface MatchCardProps {
       item: Match;
       onPress: () => void;
     }
     ```
  5. Die Navigation zu BetScreen mit typisiertem Param:
     ```typescript
     router.push({
       pathname: '/screens/BetScreen',
       params: { match: JSON.stringify(item) },
     });
     ```

  **Verifizieren:** App starten, Match Feed lädt, Karte antippen → BetScreen öffnet sich.

---

- [ ] **TASK-010** — `MatchCard` in eigene Komponente auslagern + erste Tests schreiben
  Files: `components/MatchCard.tsx`, `__tests__/components/MatchCard.test.tsx`

  **Was du lernst:** Wie man einen Test schreibt — von Null an.

  **Schritt für Schritt — erst die Komponente, dann den Test:**

  **Teil 1: Komponente auslagern**

  Verschiebe `MatchCard` aus `MatchesScreen.tsx` nach `components/MatchCard.tsx`. Props-Interface bleibt wie in TASK-009 definiert. Importiere sie in MatchesScreen zurück.

  **Teil 2: Testing-Setup**

  Installiere: `npx expo install jest-expo @testing-library/react-native @testing-library/jest-native`

  Füge in `package.json` hinzu:
  ```json
  "jest": {
    "preset": "jest-expo",
    "setupFilesAfterFramework": ["@testing-library/jest-native/extend-expect"]
  }
  ```

  **Teil 3: Deinen ersten Test schreiben**

  Erstelle `__tests__/components/MatchCard.test.tsx`:
  ```typescript
  import React from 'react';
  import { render, screen, fireEvent } from '@testing-library/react-native';
  import MatchCard from '../../components/MatchCard';

  // Hilfsfunktion: ein Basis-Match-Objekt für Tests
  const baseMatch = {
    fixture_id: 1,
    fixture_date: '2025-01-15T15:00:00Z',
    fixture_status: 'NS',         // Not Started
    teamhome_name: 'Bayern',
    teamaway_name: 'Dortmund',
    goal_home: null,
    goal_away: null,
    odd_home: 1.65,
    odd_draw: 3.80,
    odd_away: 5.20,
    // ... weitere Pflichtfelder aus deinem Match-Interface
  };

  // test() beschreibt was geprüft wird
  // der zweite Parameter ist eine Funktion die den Test ausführt
  test('zeigt "VS" wenn das Spiel noch nicht angefangen hat', () => {
    render(<MatchCard item={baseMatch} onPress={() => {}} />);
    expect(screen.getByText('VS')).toBeTruthy();
  });

  test('zeigt den Score wenn Tore vorhanden sind', () => {
    const matchWithGoals = { ...baseMatch, goal_home: 2, goal_away: 1 };
    render(<MatchCard item={matchWithGoals} onPress={() => {}} />);
    expect(screen.getByText('2 : 1')).toBeTruthy();
  });

  test('zeigt "LIVE" wenn das Spiel läuft', () => {
    const liveMatch = { ...baseMatch, fixture_status: '1h' };
    render(<MatchCard item={liveMatch} onPress={() => {}} />);
    expect(screen.getByText('LIVE')).toBeTruthy();
  });

  test('ruft onPress auf wenn die Karte angetippt wird', () => {
    // jest.fn() erstellt eine Mock-Funktion die aufzeichnet ob sie aufgerufen wurde
    const mockOnPress = jest.fn();
    render(<MatchCard item={baseMatch} onPress={mockOnPress} />);

    // fireEvent.press simuliert einen Tap
    fireEvent.press(screen.getByText('Bayern'));

    // toHaveBeenCalledTimes(1) prüft: wurde die Funktion genau einmal aufgerufen?
    expect(mockOnPress).toHaveBeenCalledTimes(1);
  });
  ```

  **Was `screen.getByText()` macht:** Es sucht in der gerenderten Komponente nach einem Element das diesen Text enthält. Wenn es den Text nicht findet, schlägt der Test fehl. Das ist der Kern von React Native Testing Library — du testest was der User sieht, nicht interne Implementierungsdetails.

  **Tests ausführen:** `npx jest MatchCard.test.tsx --verbose`

  **Verifizieren:** Alle 4 Tests grün. Ändere im Test `'VS'` zu `'vs'` → Test wird rot (zeigt dass er wirklich prüft).

---

- [ ] **TASK-011** — `BetScreen.jsx` → `BetScreen.tsx` migrieren
  Files: `app/screens/BetScreen.tsx`

  **Was du lernst:** Typisierte Navigation-Parameter mit Expo Router.

  **Schritt für Schritt:**

  1. Datei umbenennen.
  2. Navigation-Params typisieren und mit Zod parsen:
     ```typescript
     import { useLocalSearchParams } from 'expo-router';
     import { matchSchema } from '../lib/schemas';

     const params = useLocalSearchParams<{ match: string }>();
     // matchSchema.parse() validiert + konvertiert zu typisierten Daten
     const match = matchSchema.parse(JSON.parse(params.match));
     ```
  3. `OddButton` und `ProbabilityFlux` tipisieren:
     ```typescript
     interface OddButtonProps {
       label: string;
       value: number | null;
       isSelected: boolean;
       onPress: () => void;
     }
     ```
  4. Amount-Input mit react-hook-form wrappen. Zod-Schema: `z.number().positive()`.
  5. Alle `useState` tipisieren: `useState<'home' | 'away' | 'draw' | null>(null)`.

  **Verifizieren:** Von MatchesScreen zu BetScreen navigieren — Match-Daten werden korrekt angezeigt.

---

- [ ] **TASK-012** — Custom Hook `useBets` + `UserScreen` migrieren
  Files: `hooks/useBets.ts`, `app/screens/UserScreen.tsx`, `components/BetCard.tsx`

  **Was du lernst:** Dasselbe Hook-Pattern wie `useMatches` auf eine neue Ressource anwenden.

  `useBets()` gibt zurück: `{ bets: BetWithMatch[], loading: boolean, error: string | null }`. Implementierung analog zu `useMatches` — ruft `getBets(token)` aus `lib/api.ts` auf.

  `UserScreen.tsx`: JSX → TSX, Fetch-Code durch `useBets()` ersetzen, Balance und Username aus `useUserStore()` lesen. `BetCard` nach `components/BetCard.tsx` auslagern.

  **Verifizieren:** Profil-Screen zeigt Bet-History, Balance stimmt mit Datenbank überein.

---

- [ ] **TASK-013** — GitHub Actions CI für das Frontend einrichten
  Files: `sports-bets-frontend/.github/workflows/ci.yml`

  **Was du lernst:** Deine erste CI-Pipeline schreiben.

  **Schritt für Schritt:**

  1. Erstelle die Ordnerstruktur: `.github/workflows/`
  2. Erstelle die Datei `ci.yml`:
     ```yaml
     name: Frontend CI

     # Wann soll die Pipeline laufen?
     on:
       push:
         branches: [main]
       pull_request:
         branches: [main]

     jobs:
       ci:
         runs-on: ubuntu-latest   # GitHub stellt einen frischen Linux-Server bereit

         steps:
           # Schritt 1: Deinen Code herunterladen
           - name: Checkout code
             uses: actions/checkout@v4

           # Schritt 2: Node.js installieren
           - name: Setup Node.js
             uses: actions/setup-node@v4
             with:
               node-version: '20'
               cache: 'npm'

           # Schritt 3: npm-Pakete installieren (schneller als npm install)
           - name: Install dependencies
             run: npm ci

           # Schritt 4: TypeScript prüfen — kompiliert ohne Output, nur Fehler zeigen
           - name: TypeScript check
             run: npx tsc --noEmit

           # Schritt 5: Linting — Code-Stil prüfen
           - name: Lint
             run: npx eslint . --max-warnings 0

           # Schritt 6: Tests ausführen
           - name: Run tests
             run: npx jest --ci --passWithNoTests
     ```

  3. Committe und pushe diese Datei auf GitHub.
  4. Öffne dein GitHub-Repo → Tab "Actions". Du siehst die Pipeline laufen.

  **Was passiert jetzt automatisch:** Bei jedem Push und jedem Pull Request läuft diese Pipeline. Wenn TypeScript-Fehler, kaputte Tests oder Linting-Probleme auftreten, siehst du ein ❌ auf GitHub — bevor du merkst dass etwas kaputt ist.

  **Verifizieren:** Gehe auf GitHub → Actions → siehst du einen grünen Haken neben dem letzten Commit? ✅

---

- [ ] **TASK-014** — pytest-Suite + GitHub Actions CI für das Backend einrichten
  Files: `tests/conftest.py`, `tests/test_bet_service.py`, `.github/workflows/ci.yml` (im API-Repo)

  **Was du lernst:** pytest — das Test-Framework für Python. Und wie man Abhängigkeiten in Tests "mockt".

  **Konzept zuerst — Was ist ein Mock?** Dein `BetService` ruft Supabase auf. Im Test willst du aber keine echte Datenbank ansprechen — das wäre langsam, abhängig von der Internetverbindung, und würde echte Daten verändern. Stattdessen erstellst du einen "Mock" — eine gefälschte Version von Supabase die nur das zurückgibt was du für den Test brauchst.

  **Schritt für Schritt:**

  1. Installiere: `pip install pytest pytest-mock --break-system-packages`

  2. Erstelle `tests/conftest.py` — das ist die Konfigurationsdatei für pytest:
     ```python
     import pytest
     from unittest.mock import MagicMock

     @pytest.fixture
     def mock_supabase(mocker):
         """
         Ein 'fixture' ist eine wiederverwendbare Test-Vorbereitung.
         Diese Funktion erstellt eine gefälschte Supabase-Instanz.
         """
         mock = MagicMock()
         # Ersetze das echte Supabase-Objekt durch das Mock
         mocker.patch('app.db.supabase_client.supabase', mock)
         return mock
     ```

  3. Erstelle `tests/test_bet_service.py`:
     ```python
     import pytest
     from fastapi import HTTPException
     from app.services.bet_service import BetService
     from app.models.bet import Bet

     # "mock_supabase" in den Parametern bedeutet:
     # pytest ruft automatisch die conftest.py-Fixture auf
     def test_place_bet_success(mock_supabase):
         # Arrangiere: Mock gibt zurück dass User 500 Coins hat
         mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
             {"id": "user-1", "balance": 500}
         ]
         mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = None
         mock_supabase.table.return_value.insert.return_value.execute.return_value = None

         bet = Bet(match_id="match-1", amount=50, odds=1.65, prediction="home")

         # Aktion: place_bet aufrufen
         import asyncio
         result = asyncio.run(BetService.place_bet(bet, "user-1"))

         # Behauptung: die Antwort enthält die Erfolgsmeldung
         assert result["message"] == "Bet placed successfully"

     def test_place_bet_insufficient_balance(mock_supabase):
         # User hat nur 30 Coins, will aber 50 setzen
         mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
             {"id": "user-1", "balance": 30}
         ]

         bet = Bet(match_id="match-1", amount=50, odds=1.65, prediction="home")

         # HTTPException erwartet — pytest.raises prüft ob die Exception geworfen wird
         with pytest.raises(HTTPException) as exc_info:
             import asyncio
             asyncio.run(BetService.place_bet(bet, "user-1"))

         assert exc_info.value.status_code == 400
     ```

  4. Tests ausführen: `pytest tests/ -v`
     - `-v` = verbose: zeigt jeden Test mit Namen
     - Grüner Punkt = bestanden, rotes F = fehlgeschlagen

  5. Backend-CI (`sports-bets-api/.github/workflows/ci.yml`):
     ```yaml
     name: Backend CI

     on:
       push:
         branches: [main]
       pull_request:
         branches: [main]

     jobs:
       ci:
         runs-on: ubuntu-latest

         steps:
           - uses: actions/checkout@v4

           - name: Setup Python
             uses: actions/setup-python@v5
             with:
               python-version: '3.11'

           - name: Install dependencies
             run: pip install -r requirements.txt pytest pytest-mock

           - name: Run tests
             run: pytest tests/ -v
     ```

  **Verifizieren:** `pytest tests/ -v` lokal — alle Tests grün. Push auf GitHub — Actions-Tab zeigt ✅.

---

## Phase 1: Core Prediction Loop

> **Ziel:** Der komplette Prediction-Flow funktioniert von Anfang bis Ende — Prediction platzieren, in der History sehen, löschen (wenn das Spiel noch nicht angefangen hat), und automatisch auflösen wenn ein Match endet.

**Referenz-Abschnitte für diese Phase:**
- PRD: § 3. Data Model, § 4. API Specification > Bets routes, § 6. Functional Requirements (FR-001 bis FR-004), § 8. UI/UX Requirements > Bet Screen und User Profile

---

- [ ] **TASK-015** — `useUser` Hook erstellen und mit `userStore` verbinden
  Files: `hooks/useUser.ts`
  Notes: `useUser()` ruft `GET /user/profile` auf und gibt `{ user: UserProfile | null, loading: boolean, refetch: () => void }` zurück. Bei Erfolg: `userStore.setUser(data)` aufrufen. Hook fetcht einmal beim Mount — `refetch()` explizit nach bet-Platzierung aufrufen um Balance zu aktualisieren. Verifizieren: Balance in UserScreen stimmt mit Datenbank-Wert überein.

- [ ] **TASK-016** — Bet-Platzierung mit Balance-Update in der UI verbinden
  Files: `app/screens/BetScreen.tsx`, `hooks/useBets.ts`
  Notes: Nach erfolgreichem `POST /bets/`: `userStore.updateBalance(currentBalance - amount)` aufrufen (lokale Berechnung ist für MVP ausreichend). Verifizieren: Bet platzieren → zu UserScreen navigieren → Balance ist korrekt reduziert.

- [ ] **TASK-017** — Bet-Löschung mit Balance-Rückerstattung implementieren
  Files: `app/screens/UserScreen.tsx`, `components/BetCard.tsx`
  Notes: BetCard für "open" Bets zeigt einen Löschen-Button (X-Icon). Bei Tap: Bestätigung via `Alert.alert`. Ruft `DELETE /bets/?bet_id=...&match_id=...` auf. Fehler "MATCH IN PROGRESS" als Inline-Fehler. Verifizieren: offenen Bet löschen → Bet verschwindet aus Liste, Balance wird zurückgebucht.

- [ ] **TASK-018** — User-Stats zum UserScreen-Header hinzufügen
  Files: `app/screens/UserScreen.tsx`, `components/ui/StatRow.tsx`
  Notes: `GET /user/profile` gibt jetzt zurück: `stats: { total_predictions, total_wins, win_rate, current_streak, longest_streak }`. `StatRow` erstellen: 4-spaltiger horizontaler Row mit Label (uppercase, on-surface-dim) und Wert (on-surface). Anzeige: TOTAL / WON (cyan) / WIN RATE / STREAK. Verifizieren: 2 Bets platzieren, einen als gewonnen auflösen → Win Rate zeigt 50%, Streak zeigt 1.

- [ ] **TASK-019** — APScheduler-Auflösung verifizieren und testen
  Files: `app/services/bet_service.py`, `tests/test_bet_service.py`
  Notes: `check_bets()` existiert bereits. Tests für drei Fälle hinzufügen: (1) Match beendet, Prediction richtig → Status "won", Balance erhöht; (2) Match beendet, Prediction falsch → Status "lost", Balance unverändert; (3) Match noch nicht beendet → überspringen. Verifizieren: Match manuell in Supabase auf "Match Finished" setzen, `check_bets()` direkt aufrufen — Bet-Status aktualisiert sich.

- [ ] **TASK-020** — Backend-Endpoint `GET /user/profile` mit vollständigen Stats
  Files: `app/routes/user.py`, `app/services/user_service.py`, `app/models/user.py`
  Notes: `current_streak` in UserService implementieren: Bets nach `created_at DESC` sortieren, konsekutive "won"-Bets vom neuesten zählen. `win_rate = total_wins / total_predictions` (0 wenn keine Predictions). Response-Model `UserProfileResponse` in `app/models/user.py` hinzufügen. Verifizieren: `GET /user/profile` gibt korrekte Stats zurück.

- [ ] **TASK-021** — Error Boundaries für alle Screens
  Files: `components/ErrorBoundary.tsx`, alle Screen-Dateien
  Notes: React Error Boundary als Klassen-Komponente erstellen — fängt Runtime-Fehler und zeigt: "SYSTEM ERROR"-Label, Fehler-Meldung, "RELOAD"-Button. Jeden Screen in `<ErrorBoundary>` wrappen. Verifizieren: absichtlich einen Fehler in MatchesScreen werfen — Boundary fängt ihn.

---

## Phase 2: Achievements & Leaderboard (Magic Moment)

> **Ziel:** Der Magic Moment funktioniert komplett — User platziert eine Prediction, sie wird aufgelöst, ein Badge erscheint, und der Leaderboard-Rang ist sichtbar. Alle fünf Achievements sind implementiert und der globale Leaderboard ist live.

**Referenz-Abschnitte für diese Phase:**
- PRD: § 3. Data Model (achievements, user_achievements, leaderboard_snapshots), § 4. API Specification > Leaderboard- und Achievement-Routes, § 6. Functional Requirements (FR-005, FR-006), § 8. UI/UX Requirements > Leaderboard Screen

---

- [ ] **TASK-022** — `achievements`- und `user_achievements`-Tabellen in Supabase anlegen
  Files: Supabase SQL-Editor
  Notes: SQL aus prd.md § 3. Data Model ausführen. Mit den 5 Achievement-Rows seeden (first_correct_call, winning_streak_5, sharp_analyst, early_bird, upset_special). Verifizieren: `SELECT * FROM achievements` — zeigt 5 Zeilen.

- [ ] **TASK-023** — `AchievementService` mit allen 5 Trigger-Bedingungen implementieren
  Files: `app/services/achievement_service.py`, `app/models/achievement.py`
  Notes: `AchievementService.check_and_award(user_id, context)`. Alle 5 Bedingungen per FR-006 aus prd.md: `first_correct_call` (erster gewonnener Bet), `winning_streak_5` (letzte 5 Bets alle gewonnen), `sharp_analyst` (≥60% Win Rate bei ≥10 Predictions), `early_bird` (alle Fixtures einer Runde getippt bevor das erste Spiel startet), `upset_special` (gewonnener Bet wo Odds > 3.0). Upsert/INSERT OR IGNORE verhindert Duplikate.

- [ ] **TASK-024** — `AchievementService` in `BetService.check_bets()` integrieren
  Files: `app/services/bet_service.py`
  Notes: Nach Bet-Status-Update: `AchievementService.check_and_award()` aufrufen. Exceptions loggen ohne die Bet-Auflösung zu crashen. Verifizieren: Match auf "Match Finished" setzen mit korrekter Prediction — passendes Achievement erscheint in `user_achievements`.

- [ ] **TASK-025** — Backend-Achievement-Routes hinzufügen
  Files: `app/routes/achievements.py`, `app/services/achievement_service.py`
  Notes: `GET /achievements/` (kein Auth, gibt Katalog zurück). `GET /achievements/me` (Auth erforderlich, gibt verdiente Achievements zurück). Verifizieren: nach first_correct_call-Verdienst `GET /achievements/me` aufrufen — Badge erscheint.

- [ ] **TASK-026** — `useAchievements` Hook und `AchievementBadge` Komponente
  Files: `hooks/useAchievements.ts`, `components/AchievementBadge.tsx`
  Notes: Hook ruft beide Achievement-Endpoints auf und berechnet welche locked/earned sind. `AchievementBadge`: 48×48px, Lucide-Icon nach `achievement.icon`, Glow-Shadow in `achievement.color`. Locked: Icon bei opacity 0.2, kein Glow. Earned: volle Farbe + Glow. Verifizieren: Komponente mit earned=true und earned=false rendern — visueller Unterschied erkennbar.

- [ ] **TASK-027** — Achievements-Sektion zum UserScreen hinzufügen
  Files: `app/screens/UserScreen.tsx`
  Notes: Horizontales ScrollView mit allen 5 Badges unter der Stats-Row. Earned = glühend, locked = gedimmt. Tap auf earned Badge: Modal mit Name und Beschreibung. Verifizieren: first_correct_call verdienen, UserScreen öffnen — Badge glüht.

- [ ] **TASK-028** — `leaderboard_snapshots`-Tabelle und `LeaderboardService`
  Files: `app/services/leaderboard_service.py`, `app/models/leaderboard.py`
  Notes: SQL aus prd.md § 3 ausführen. `refresh_leaderboard()`: alle User mit ≥5 aufgelösten Predictions abfragen, Win Rate berechnen, sortieren, Rang zuweisen, in leaderboard_snapshots upserten. `get_leaderboard(limit, offset)`: aus Snapshot lesen. Verifizieren: 3 Test-User mit ≥5 Predictions, refresh ausführen, Ranking prüfen.

- [ ] **TASK-029** — Leaderboard zum Scheduler hinzufügen + Leaderboard-Routes erstellen
  Files: `app/jobs/scheduler.py`, `app/routes/leaderboard.py`
  Notes: Scheduler-Job: jede Stunde. `GET /leaderboard/` (kein Auth, Top 50). `GET /leaderboard/me` (Auth, eigener Rang oder 404 wenn nicht qualifiziert). Verifizieren: nach refresh `GET /leaderboard/` aufrufen — Einträge nach Win Rate sortiert.

- [ ] **TASK-030** — `LeaderboardScreen.tsx` mit `useLeaderboard` Hook bauen
  Files: `app/screens/LeaderboardScreen.tsx`, `hooks/useLeaderboard.ts`, `components/LeaderboardRow.tsx`
  Notes: `useLeaderboard()` gibt `{ entries, loading, myRank }` zurück. `LeaderboardRow`: Rang, Username, Win Rate, Streak. Eigene Zeile: cyan linker Rand (3px). Nicht-qualifiziert-Banner: "NOT RANKED — MAKE 5 PREDICTIONS TO QUALIFY". Verifizieren: navigieren zu LeaderboardScreen, eigene hervorgehobene Zeile.

- [ ] **TASK-031** — Leaderboard zur Navigation hinzufügen
  Files: `app/index.tsx` oder Tab-Navigator
  Notes: Leaderboard-Screen über Bottom-Tab oder Navbar erreichbar machen. Lucide `Trophy`-Icon. Verifizieren: zwischen MatchesScreen, UserScreen und LeaderboardScreen navigieren ohne App-Neustart.

- [ ] **TASK-032** — pytest-Tests für AchievementService und LeaderboardService
  Files: `tests/test_achievement_service.py`, `tests/test_leaderboard_service.py`
  Notes: Jede der 5 Achievement-Bedingungen mit Mock-Daten testen. Leaderboard-Tests: Ranking-Reihenfolge prüfen, User mit <5 Predictions ausgeschlossen. Verifizieren: `pytest tests/ -v` — alle neuen Tests grün.

---

## Phase 3: Social — Friends & Follow

> **Ziel:** User können anderen Usern vom Leaderboard folgen, deren Profile mit Stats und Predictions sehen, und eine Following-Liste im eigenen Profil haben.

**Referenz-Abschnitte für diese Phase:**
- PRD: § 3. Data Model (friendships-Tabelle), § 4. API Specification > Friends-Routes, § 6. Functional Requirements (FR-010), § 8. UI/UX Requirements > Friend Profile Screen

---

- [ ] **TASK-033** — `friendships`-Tabelle in Supabase anlegen
  Files: Supabase SQL-Editor
  Notes: SQL aus prd.md § 3 ausführen — UNIQUE-Constraint und CHECK (kein Self-Follow). Indexes anlegen. Verifizieren: Test-Row einfügen, Duplikat schlägt fehl, Self-Follow schlägt fehl.

- [ ] **TASK-034** — `FriendshipService` mit Follow/Unfollow-Logik implementieren
  Files: `app/services/friendship_service.py`, `app/models/friendship.py`
  Notes: `follow`, `unfollow`, `get_following`, `get_friend_profile`. Offene Bets (status="open") werden NICHT in `get_friend_profile` zurückgegeben. Verifizieren: follow() aufrufen, dann get_following() — gefolgter User erscheint.

- [ ] **TASK-035** — Friend-Routes in FastAPI erstellen
  Files: `app/routes/friends.py`
  Notes: Alle 4 Endpoints aus prd.md § 4. Auth überall erforderlich. Verifizieren: `POST /friends/follow` mit gültiger user_id, dann `GET /friends/following` — User erscheint.

- [ ] **TASK-036** — `FriendProfileScreen.tsx` mit Follow/Unfollow bauen
  Files: `app/screens/FriendProfileScreen.tsx`, `hooks/useFriends.ts`
  Notes: `useFriends()` gibt `{ following, follow(userId), unfollow(userId) }` zurück. Screen zeigt: Username, Stats-Row, Achievements, letzte 10 aufgelöste Predictions (BetCard read-only). FOLLOW/UNFOLLOW-Button oben rechts — Optimistic UI (Button wechselt sofort, ohne auf Server-Response zu warten). Verifizieren: Freund-Profil öffnen, folgen — Button wechselt zu UNFOLLOW.

- [ ] **TASK-037** — Leaderboard-Rows mit FriendProfileScreen verbinden
  Files: `app/screens/LeaderboardScreen.tsx`, `components/LeaderboardRow.tsx`
  Notes: Tap auf fremde Zeile → FriendProfileScreen mit `{ userId }`. Eigene Zeile → UserScreen. Verifizieren: fremde Zeile antippen → FriendProfileScreen mit korrekten Daten.

- [ ] **TASK-038** — FOLLOWING-Tab zum UserScreen hinzufügen
  Files: `app/screens/UserScreen.tsx`
  Notes: Zwei Tabs: "MY PICKS" (bestehende Bet-History) und "FOLLOWING" (Liste gefolgter User). Kein Following: "NOT FOLLOWING ANYONE YET." Verifizieren: 2 Usern folgen, FOLLOWING-Tab öffnen — beide erscheinen.

- [ ] **TASK-039** — pytest-Tests für FriendshipService
  Files: `tests/test_friendship_service.py`
  Notes: Follow (Erfolg), Follow (Duplikat → kein Fehler), Unfollow (Erfolg), get_friend_profile (gibt nur aufgelöste Bets zurück, keine offenen). Verifizieren: `pytest tests/test_friendship_service.py -v` — alle Tests grün.

---

## Phase 4: Rebrand, Polish & Portfolio-Vorbereitung

> **Ziel:** Die App ist vollständig zu Matchday umgebrandmarkt, alle Edge Cases und Empty States sind behandelt, der README ist geschrieben — der Code ist interview-ready.

**Referenz-Abschnitte für diese Phase:**
- PRD: § 7. Non-Functional Requirements, § 12. Edge Cases & Error Handling
- Vision: § 1. Vision & Mission, § 4. Brand Strategy > Voice & Tone, § 5. Design Direction > Accessibility

---

- [ ] **TASK-040** — App zu Matchday umbranden
  Files: `app.json`, `app/screens/LoginScreen.tsx`, `app/screens/MatchesScreen.tsx`, `assets/`
  Notes: `app.json`: `name: "Matchday"`. Hero-Headline auf LoginScreen: "MATCHDAY". Eyebrow: "PREDICTION GAME". Splash/Icon ersetzen: dunkler Hintergrund + "MATCHDAY" in Inter 900 reicht. Verifizieren: App bootet, Login zeigt "MATCHDAY".

- [ ] **TASK-041** — Vollständiges Empty- und Error-State-Audit
  Files: Alle Screen-Dateien
  Notes: Jeden Screen in jedem Datenzustand prüfen per prd.md § 8. Kein Screen darf bei leeren Daten einen weißen Bereich zeigen oder crashen. Verifizieren: jeden Screen manuell mit leeren Daten testen.

- [ ] **TASK-042** — Gambling-Sprache aus der UI entfernen
  Files: Alle Screen-Dateien
  Notes: Jedes "bet", "wager", "place bet" in UI-Labels ersetzen durch "prediction", "call", "make your call". API und Datenbank können intern "bet" behalten. Verifizieren: App durchklicken — kein sichtbares "bet" in der UI.

- [ ] **TASK-043** — Accessibility-Labels zu allen interaktiven Elementen hinzufügen
  Files: Alle Screen- und Komponenten-Dateien
  Notes: `accessibilityLabel`, `accessibilityRole`, `accessibilityHint` zu allen Pressable-Komponenten, TextInputs, Navigation-Buttons hinzufügen. Verifizieren: iOS VoiceOver im Simulator aktivieren, MatchesScreen durchnavigieren.

- [ ] **TASK-044** — Rate Limiting für FastAPI-Auth-Routes
  Files: `app/main.py`, `requirements.txt`
  Notes: `slowapi` installieren. `@limiter.limit("10/minute")` auf `/auth/login` und `/auth/register`. Verifizieren: 11 schnelle POST-Requests an /auth/login — der 11. gibt 429 zurück.

- [ ] **TASK-045** — Minimum Balance Floor implementieren
  Files: `app/services/bet_service.py`
  Notes: Nach Bet-Verlust: wenn Balance < 50, auf 100 aufstocken. Log: "User {user_id} balance topped up to 100". Verifizieren: User mit 30 Coins verliert Bet — Balance wird 100.

- [ ] **TASK-046** — Leaderboard-Seed-Skript
  Files: `scripts/seed_leaderboard.py`
  Notes: 20 Bot-User mit realistischen Prediction-Historien (40%–75% Win Rate) anlegen. Usernames: "AlphaAnalyst", "HeatmapHero" etc. Einmalig bei Deployment ausführen. Verifizieren: Skript ausführen, Leaderboard-Screen zeigt 20 Einträge.

- [ ] **TASK-047** — Umfassenden README schreiben
  Files: `README.md` (in beiden Repos)
  Notes: Abschnitte: (1) Was ist Matchday; (2) Tech Stack; (3) Architektur-Entscheidungen — warum FastAPI, warum Zustand, wie funktioniert die automatische Auflösung; (4) Setup-Anleitung; (5) Tests ausführen; (6) CI-Badge. Ehrlich bleiben — erwähne was schwierig war und warum. Verifizieren: eine Person die das Projekt nicht kennt kann dem README folgen und beide Services lokal starten.

- [ ] **TASK-048** — Finales TypeScript-Audit: null `any`-Typen
  Files: Alle `.ts`- und `.tsx`-Dateien
  Notes: `grep -r ": any" --include="*.ts" --include="*.tsx" .` ausführen. Jede Fundstelle entweder typisieren oder mit `// @ts-expect-error — [Begründung]` und TODO-Kommentar versehen. Ziel: null unerklärte `any`-Typen. Verifizieren: `npx tsc --noEmit` gibt 0 zurück.

- [ ] **TASK-049** — mypy-Typprüfung fürs Backend
  Files: `requirements.txt`, `.github/workflows/ci.yml` (API-Repo)
  Notes: `mypy` installieren. `mypy app/ --ignore-missing-imports` ausführen, Fehler beheben. Backend-CI um `mypy app/`-Step erweitern. Verifizieren: `mypy app/` läuft lokal und in CI ohne Fehler.

- [ ] **TASK-050** — Frontend-Testabdeckung erweitern
  Files: `__tests__/components/BetScreen.test.tsx`, `__tests__/hooks/useMatches.test.ts`
  Notes: `BetScreen.test.tsx`: CTA disabled ohne Outcome, CTA disabled ohne Amount, korrekte Wahrscheinlichkeit bei 1.65 Odds (60.6%), "INSUFFICIENT BALANCE" bei zu wenig Balance. `useMatches.test.ts`: loading=true beim Mount, Daten nach Resolve, error-String bei API-Fehler, refetch() ruft API erneut auf. Verifizieren: `npx jest --coverage` — ≥70% Coverage auf getesteten Dateien.

---

## Phase 5: Post-Launch Iteration (v2 Features)

> **Ziel:** Nach dem Portfolio-Launch und wenn Interviews laufen — diese Tasks erweitern das Projekt um zusätzliche technische Skills.

**Referenz-Abschnitte für diese Phase:**
- PRD: § 14. Out of Scope, § 15. Open Questions

---

- [ ] **TASK-051** — Private Ligen / Custom Groups (Backend)
  Files: `app/services/league_service.py`, `app/routes/leagues.py`, `app/models/league.py`
  Notes: Tabellen: `leagues` (id, name, creator_id, invite_code), `league_members`. Routes: `POST /leagues/` (erstellen), `POST /leagues/join` (beitreten per Invite-Code), `GET /leagues/{id}/leaderboard`. Zeigt relationales Datenbankdesign — gutes Interview-Thema.

- [ ] **TASK-052** — Private Ligen Frontend
  Files: `app/screens/LeaguesScreen.tsx`, `app/screens/CreateLeagueScreen.tsx`, `hooks/useLeagues.ts`
  Notes: LeaguesScreen: Liste der Ligen des Users mit eigenem Rang. CreateLeagueScreen: Name-Input + Submit. Invite-Link per Expo Linking.

- [ ] **TASK-053** — Push-Notifications für Bet-Auflösung
  Files: `app/services/notification_service.py`, Expo-Notifications-Setup
  Notes: Expo Push Notification API. Backend ruft Expo-Endpoint nach Auflösung auf. Frontend registriert Push-Token beim Login. Erfordert EAS-Production-Credentials.

- [ ] **TASK-054** — Multi-Sport-Architektur
  Files: `app/services/match_service.py`, `app/models/match.py`
  Notes: `sport: VARCHAR(20) DEFAULT 'football'` zur matches-Tabelle hinzufügen. Sport-Filter zu `GET /matches/`. Zweiten Sport anbinden. Zeigt API-Integration und Schema-Erweiterbarkeit.

- [ ] **TASK-055** — Storybook für Komponenten-Dokumentation
  Files: `storybook/`-Verzeichnis, Story-Dateien für Kern-Komponenten
  Notes: `@storybook/react-native` installieren. Stories für: MatchCard, BetCard, AchievementBadge, LeaderboardRow, alle Button-Varianten. Jede Story zeigt alle States. Guter Portfolio-Zusatz für Frontend-Rollen.

- [ ] **TASK-056** — Performance-Audit und Supabase-Query-Optimierung
  Files: `app/services/*.py`
  Notes: Langsamste Endpoints profilen. Häufigste Kandidaten: `check_bets()` macht Queries in einem Loop — auf Batch-Queries umstellen. Vorher/Nachher in einem Kommentar dokumentieren.

---

## Wenn du selbst baust: Tipps für den Alltag

### Wie du eine Task angehst

1. **Lese zuerst.** Öffne die entsprechenden PRD-Abschnitte bevor du code schreibst. Versteh was das Ziel ist.
2. **Schreib dann.** Eine Datei nach der anderen. Nicht alles auf einmal.
3. **Verifiziere.** Jede Task hat ein "Verifizieren"-Schritt — mach ihn wirklich, bevor du abhakst.
4. **Committe.** Ein Commit pro Task: `git commit -m "TASK-006: LoginScreen zu TSX migriert mit react-hook-form"`
5. **Hake ab.** Ändere `- [ ]` zu `- [x]` in dieser Datei.

### Wenn du steckenbleibst

- Fehlermeldung in TypeScript? Lies sie von rechts nach links — das Ende sagt meistens wo das Problem ist.
- Test schlägt fehl? Lies die Fehlermeldung: sie zeigt was erwartet wurde und was tatsächlich kam.
- CI rot? Klicke auf das rote ❌ auf GitHub → "Details" → siehst genau welcher Schritt fehlgeschlagen ist und warum.
- Grundsätzlich unklar? Frag — ich helfe dir durch jeden Schritt.

### Nach jeder Phase

Push deine Arbeit als Pull Request:
```bash
git checkout -b phase-0/foundation-and-ts-migration
git add .
git commit -m "Phase 0 complete: TypeScript migration + CI setup"
git push origin phase-0/foundation-and-ts-migration
```
Dann auf GitHub einen PR öffnen. [CodeRabbit](https://coderabbit.ai) auf dem Repo aktivieren — es kommentiert automatisch auf jeden PR. Das ist wie Code-Review von einem erfahrenen Entwickler, kostenlos.

### Status aktualisieren

Wenn du Tasks abhakst, aktualisiere die Zeile oben:
`**Status:** 14/65 Tasks erledigt` und `**Aktuelle Phase:** Phase 1 — Core Prediction Loop`
