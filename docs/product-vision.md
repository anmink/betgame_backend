# Product Vision — Matchday

## 1. Vision & Mission

### Vision Statement

A world where every football fan has a skilled, competitive identity — not just a team they support, but a track record that proves how well they read the game.

### Mission Statement

Matchday gives sports fans a free, social prediction game where real match outcomes determine who really knows their football — no money, no luck, just skill and nerve.

### Founder's Why

Anne Minkenberg didn't start Matchday from a whiteboard. She started it from a working app. The Kinetic Analyst — a sports betting simulation with a FastAPI backend, live fixture data, automatic result resolution, and a polished dark-terminal UI — already existed and worked. The question wasn't "can I build this?" but "what should this actually become, and how do I use it to demonstrate real full-stack skills?"

The gap she identified is real: there is no clean, zero-stakes, social prediction game built around real football fixtures. The existing alternatives are either too casual (WhatsApp prediction threads with no tracking) or too serious (Kickbase, Bet365). The middle ground — a skill-based leaderboard game for football fans who care about being right — is underserved.

Matchday is also a deliberate technical challenge. Anne knows her gaps: TypeScript, testing, CI/CD, state management. The plan is to build the portfolio piece and close the gaps at the same time, so that when she demos the app in an interview she can speak to not just what it does but how it's built — type safety, custom hooks, automated tests, a real CI pipeline. The code is the portfolio.

### Core Values

**Real data, real stakes.** Every prediction in Matchday is tied to a real football match happening in the world. The game is only interesting because the outcomes are real. This means the data pipeline must never be faked, patched with stale data, or approximated. If no live data is available, the feed is empty — not populated with placeholder fixtures.

**Skill should be visible.** The whole point is proving you know your football. The leaderboard, win rate, streaks, and badges exist to make skill legible. The design should make a user's record prominent, not buried. Someone with a 70% win rate over 50 predictions deserves to look different from a new account.

**Simplicity of action, depth of identity.** Placing a prediction takes three taps. That's intentional. The complexity lives in the game's progression layer — achievements, rank, streak history — not in the core action. New users can play immediately; invested users have things to chase.

**Code quality is product quality.** Because this is also a portfolio project, the codebase itself is a deliverable. TypeScript coverage, test coverage, CI passes — these are not nice-to-haves. They are as important as the features. Every PR should leave the codebase in a better state than it found it.

### Strategic Pillars

**Tie everything to real events.** The feature set lives or dies by the football calendar. Achievements, streaks, and leaderboard momentum all derive meaning from real Bundesliga or Champions League rounds. When there are no matches, the app communicates that honestly rather than filling space with noise.

**Skill-based progression over luck.** Virtual coins are a score, not a gambling mechanic. The leaderboard ranks by win rate and accuracy, not by balance size. Achievements reward correct predictions and streaks, not volume of play. This positioning is how Matchday stays clearly distinct from betting products.

**Ship one game loop first.** The friends system, league tables, and multi-sport expansion are great features — but only after the core loop works perfectly: see matches → make prediction → watch match → see result → see your rank change. Everything else is polish on top of that.

### Success Looks Like

In twelve months, Matchday is Anne's centerpiece portfolio project. The GitHub repo has a clean README, CI badges passing, TypeScript strict mode on, 80%+ test coverage on critical paths, and well-documented architectural decisions. She can walk a technical interviewer through the codebase and explain why she chose Zustand over Context, how the Supabase RLS policies protect user data, and what the CI pipeline does on a PR. The app runs in production — whether on the App Store or as an Expo Go link shared with friends — with a small community of real users who actually use it to compete during Bundesliga matchdays. She's landed the Full-Stack or Frontend role she wanted.

---

## 2. User Research

### Primary Persona

**Luca, 26, software developer, Berlin.**

Luca follows the Bundesliga and Champions League closely. He checks scores on his phone during commute, has three football group chats, and runs informal prediction threads every matchday weekend. He's competitive about it — he knows his record is better than his friends', but there's no clean way to prove it.

He's technically comfortable with apps. He uses Robinhood-style interfaces without friction, dislikes onboarding flows that waste his time, and abandons apps that feel slow or require too many permissions upfront. He will not spend money on a prediction app — not because he can't afford it, but because paying introduces a different kind of stress to something that's supposed to be fun.

His current workflow: receive fixture list in a WhatsApp group on Thursday, post his picks, watch matches Saturday, argue about the results Sunday, forget the whole thing by Tuesday. There's no tracking. No history. No proof. When Matchday enters his life, it's because a friend shares a "look at my leaderboard rank" moment that makes him curious.

### Secondary Personas

**The casual viewer who wants a reason to care.** She watches matches when her partner has them on but doesn't follow standings closely. Matchday gives her a stake in the outcome — a personal investment in what happens on the pitch — without requiring her to understand tactical formations or transfer news. She plays casually, doesn't chase the leaderboard, and appreciates the achievement system as a gentle encouragement layer.

**The recruiter or technical interviewer reviewing Anne's portfolio.** They are not a user of the app, but they are a consumer of it. What they evaluate: is the TypeScript clean? Are there real tests? Does the CI pipeline exist and pass? Is the README honest and well-written? Does the architecture make sense? For this persona, code quality and documentation are the product.

**The friend group organizer.** 30s, runs a five-a-side group that also does prediction competition during major tournaments. She wants a shared leaderboard her group can point to — something better than a pinned WhatsApp message. She's the vector through which Matchday reaches new users, so the friends/follow feature and shareable profile state matter most to her.

### Jobs To Be Done

*Functional jobs:* Make predictions on upcoming fixtures with clear odds information available. See the outcome of past predictions tracked automatically. Compare my win rate and prediction record to friends and the global community. Earn recognition for a correct prediction streak or a high win rate.

*Emotional jobs:* Feel like my football knowledge is real and provable — not just an opinion. Get a small rush when a match I called correctly resolves. Feel competitive in a low-stakes, fun way. Feel smart when I'm right.

*Social jobs:* Establish a reputation as a good football predictor in my circle. Have something concrete to share or reference when arguing about match outcomes. Show up in a leaderboard that lets others see how good I actually am.

### Pain Points

**Pain 1 — No tracking, no proof (severity: high, frequency: every matchday)**
Prediction threads live in chat. When Saturday ends, the record disappears. There is no cumulative win rate, no streak history, no proof that you've been right 70% of the time over forty matches. This is the core pain Matchday solves. The user currently accepts this loss of history as the price of informal play.

**Pain 2 — No clean leaderboard (severity: high, frequency: weekly)**
Even groups using shared spreadsheets or Kickbase league tables find it clunky to maintain. The admin overhead (updating cells, remembering to post results, manually calculating points) means the effort exceeds the fun. Users want a leaderboard that updates itself.

**Pain 3 — Betting apps feel wrong for casual play (severity: medium, frequency: when seeking an app)**
The obvious alternative — a real sportsbook — introduces financial risk, addiction framing, and a regulatory environment that makes casual use feel heavier than it should. Users like Luca have tried them, found the UX optimized for retention and deposits, and stepped back.

**Pain 4 — Fantasy football requires too much weekly management (severity: medium, frequency: seasonal)**
Kickbase and similar products require active squad management, transfer decisions, and weekly attention. For users who just want to call match outcomes, fantasy football is overkill. The cognitive overhead is too high for the casual engagement they want.

### Current Alternatives & Competitive Landscape

**WhatsApp prediction threads** are the dominant alternative. Zero setup friction, already where the social layer exists. Weakness: no history, no tracking, no automated resolution, the thread gets buried under other messages. Switching to Matchday requires dragging friends away from a convenience habit — the app needs to offer clearly more value, not just different value.

**Kickbase / Fantasy Bundesliga** are well-designed products for the highly engaged football fan. They solve a different problem: comprehensive squad management and weekly points. For Matchday's target user, they are overcomplicated. Switching is not relevant — they serve different use cases.

**Real sportsbooks (Bet365, BetWay, Tipico)** are the most direct functional comparison, but the wrong mental model. They optimize for monetary wagering under regulated frameworks. The UX, copy, and product philosophy are designed for a different kind of engagement. Matchday should never look or feel like them — not even accidentally.

**Doing nothing** is the default state. Most users will play prediction games informally in chat and accept the lack of tracking. Matchday must offer a demonstrably better experience to overcome inertia.

### Key Assumptions to Validate

**Assumption 1 — Users will switch from WhatsApp to a dedicated app.** We assume that the promise of tracking and leaderboards is enough to pull casual predictors away from chat-based play. To validate: measure whether users return after their first session. If 7-day retention is below 30%, the pull isn't strong enough.

**Assumption 2 — The friends system is the growth engine.** We assume users discover Matchday because a friend shares their rank or challenges them. To validate: track referral source in analytics. If organic/direct dominates over social sharing, the friends feature may need to be deeper or easier to share from.

**Assumption 3 — Achievements create retention.** We assume that visible milestones (badges, streaks) give users a reason to return even on weeks with few matches. To validate: compare session frequency between users who have earned ≥1 badge vs. users with zero badges in their first two weeks.

**Assumption 4 — Virtual coins motivate without monetization pressure.** We assume users care about their virtual balance even knowing it has no real value. To validate: observe whether users with low balances (after losses) churn more than users on winning streaks. If so, the balance mechanic may need adjustment.

**Assumption 5 — The data pipeline is reliable enough for a live product.** The football API used by the existing backend provides fixture data and results. We assume it is reliable enough that matches resolve automatically without manual intervention. To validate: run the scheduler in production for two full Bundesliga rounds and monitor for missed resolutions.

**Assumption 6 — The dark terminal aesthetic resonates beyond its creator.** The design is distinctive and intentional. We assume it feels premium to the target user (technically comfortable, design-aware, 25–35). To validate: show the UI to five target users without explanation and ask what kind of app they think it is.

### User Journey Map

**Awareness.** Luca sees a screenshot in a group chat — a friend posted their leaderboard ranking after a good week. The UI looks different: dark, data-forward, not like any betting app he's seen. He downloads it.

**Consideration.** He lands on the login screen. "THE KINETIC ANALYST" was the old brand — now it reads "MATCHDAY". The dark terminal aesthetic makes it feel serious, not casino-y. He creates an account in under 90 seconds via email.

**First use.** He lands on the Match Feed. This week's Bundesliga fixtures are listed. He picks Bayern vs. Dortmund, selects HOME win at 1.65 odds, bets 50 coins. It takes three taps. He closes the app.

**Magic moment.** Saturday evening, Bayern win 2-1. Matchday resolves the result automatically. Luca opens a push notification: "Bayern won. +82 coins. 🎯 First Correct Call — badge earned." He opens the app, sees the badge in his profile, and checks the leaderboard. He's ranked 847 globally. He wants to move up.

**Habit formation.** Every Thursday he opens the app to make his picks for the weekend. He follows two friends and can see their predictions side by side with his. When he's right and they're wrong, he screenshots it.

**Advocacy.** After two months and a 64% win rate, he shares his profile link. "I've been calling matches better than the odds all season." Two friends download Matchday.

---

## 3. Product Strategy

### Product Principles

**The match is the game.** Every feature should connect to a live fixture. If a feature doesn't make predicting, following, or resolving a match more compelling, it doesn't belong in v1.

**Resolution is the reward.** The emotional peak of the app isn't placing the bet — it's seeing the result resolve. Every design decision around notifications, result display, and balance updates should amplify that moment. The resolution screen is the money shot.

**Progression must be legible.** Win rate, streak, rank, badges — a user should be able to understand their standing within 10 seconds of opening the app. The profile screen is the most important screen after the match feed.

**Earn your features.** Social features (friends, profile sharing) and progression features (badges, ranks) should feel earned through play, not handed out on sign-up. A user who has played for two weeks should have a visibly richer profile than a new account.

**Type safety is a product principle, not just a developer preference.** Every API response, navigation parameter, and component prop should be typed. This is both a code quality commitment and a constraint that forces clarity about data shapes. If you can't type it, you probably don't fully understand it.

### Market Differentiation

The key distinction is what Matchday refuses to be. It refuses to be a gambling product — virtual coins only, no deposit mechanics, no odds manipulation, no addiction-pattern UX. It refuses to be fantasy football — no squad management, no transfers, no weekly admin. It refuses to be casual trivia — predictions must be on real matches with real outcomes, not randomized question banks.

What remains is a narrow but real category: a skill-based prediction game for football fans who want to prove their knowledge in a social context. The closest thing that exists is a WhatsApp thread, which has no UX at all. Matchday is what happens when you take that informal social behavior and give it structure, history, and a leaderboard.

For the target user, this distinction matters because the alternatives carry baggage. A sportsbook makes casual play feel financially weighted. Fantasy football makes casual play feel like homework. Matchday makes it feel like the best version of what already happens in their group chat.

### Magic Moment Design

The magic moment is: first prediction resolves correctly, balance increases, badge pops, leaderboard rank is visible. This needs to happen within the user's first week — ideally their first weekend. The path from sign-up to magic moment is:

1. Create account (< 2 minutes via email)
2. See match feed with upcoming fixtures (immediate — data is pre-loaded)
3. Select a match and place a prediction (< 3 taps)
4. Receive push notification or in-app alert when result resolves
5. See balance update, badge awarded, leaderboard rank

The critical dependency is that step 4 must happen automatically — the scheduler must resolve bets within minutes of a match ending, not hours. If a user has to manually refresh to see their result, the magic moment is broken. The APScheduler job running every 5 minutes on the backend already handles this — ensuring it's reliable in production is non-negotiable for v1.

The leaderboard must be populated. An empty leaderboard on day one is a dead magic moment. Seed it with bot accounts or Anne's own test predictions to ensure new users always have a rank to compare against.

### MVP Definition

**Match feed with live fixture data.** The existing MatchesScreen displays Bundesliga fixtures fetched from the football API, grouped by round, with live/upcoming/finished status, odds for all three outcomes, and scores. This is already built. The MVP task is TypeScript migration, not reimplementation.

**Prediction placement with virtual balance.** The BetScreen already handles prediction selection, amount entry, implied probability display, and balance deduction. The MVP task is TS migration and cleaning up the UX — specifically surfacing the "virtual coins" framing clearly so users never confuse this for real money.

**Automatic result resolution.** The scheduler already runs BetService.check_bets() every 5 minutes. The MVP task is ensuring this is reliable in production and adding proper error logging.

**User profile with stats.** The UserScreen shows balance and bet history. The MVP version adds: win rate, total predictions, current win streak, and at least 3 earned badges displayed visibly.

**Global leaderboard.** New screen. Ranks all users by win rate (minimum 5 predictions to qualify). Shows rank, username, win rate, streak. Simple list, no pagination required for MVP.

**Achievement system (5 core badges).** First Correct Call, Winning Streak (5 in a row), Sharp Analyst (10+ predictions at 60%+ win rate), Early Bird (predict all fixtures before a round starts), Upset Special (correctly call an underdog victory). Triggered automatically by the scheduler on result resolution.

**Friends — follow system.** Users can follow other users. The match feed can be filtered to show "Friends' Picks" alongside their own. A followed user's profile is visible. No private messaging, no notifications for follows.

### Explicitly Out of Scope

**Multi-sport support.** The architecture should accommodate it (sport-agnostic data models), but v1 ships with Bundesliga and Champions League only. Adding basketball or tennis means integrating new data sources and is a post-launch milestone.

**Private groups or leagues.** Creating a custom league with friends is a compelling feature — but it requires group creation flows, invite links, and league administration. This is a v2 feature once the core social loop (global leaderboard + friends) is proven.

**Push notifications (production).** Expo notifications require proper setup, production credentials, and a notification service. For MVP, in-app alerts and badge updates on open are sufficient. Add real push in v2.

**Web version.** React Native for iOS and Android only. A web companion is interesting for portfolio reasons (it would let Anne demonstrate Next.js knowledge) but is out of scope for this phase.

**Real money or paid features.** Never. Not now, not later. The free positioning is a product principle, not a constraint.

**Social feed / activity stream.** A timeline of friends' recent predictions is appealing but adds complexity without improving the core loop. Deferred to v2.

### Feature Priority (MoSCoW)

**Must Have**
- Match feed displaying upcoming/live/finished fixtures with odds
- Prediction placement (select outcome, set coin amount, confirm)
- Virtual balance management (deduct on bet, credit on win)
- Automatic result resolution via scheduler
- User profile with win rate, streak, prediction history
- Global leaderboard (win rate-based)
- Achievement system with 5 core badges
- TypeScript migration of all frontend screens
- Custom hooks (useMatches, useBets, useLeaderboard, useUser)
- Zustand global state for auth + user data
- Supabase Auth (email + magic link)
- Unit tests for BetService and MatchService (pytest)
- Component tests for BetScreen and MatchCard (Jest + RNTL)
- GitHub Actions CI pipeline

**Should Have**
- Friends / follow system with friend prediction visibility
- Typed Expo Router navigation parameters
- Error boundaries on all screens
- Zod schema validation on API responses in frontend
- Comprehensive pytest suite for all routes
- README with architecture documentation and setup instructions
- Form validation with react-hook-form on prediction inputs
- Accessibility labels on all interactive elements

**Could Have**
- Streak tracking displayed visually in match cards
- Extended achievement set (10+ badges)
- Profile sharing via deep link
- Storybook documentation for design system components
- Supabase RLS policy documentation

**Won't Have (this time)**
- Private groups or custom leagues
- Multi-sport support (architecture must support it; implementation waits)
- Real push notifications
- Web version
- Any real-money features

### Core User Flows

**Flow 1: Place a prediction**
Trigger: User opens app during an active Bundesliga week with upcoming fixtures.
Steps: (1) Lands on Match Feed, sees upcoming matches grouped by round. (2) Taps a match card. (3) BetScreen opens: match header, odds buttons (HOME / DRAW / AWAY), Probability Flux bar, coin input. (4) User selects odds and enters amount. (5) Taps CONFIRM — prediction registered, balance deducted. (6) Returns to feed with confirmed state visible on the match card.
Outcome: Prediction stored in Supabase bets table with status "open".
Success criteria: Prediction placed in under 30 seconds from opening the app. Confirmation visible immediately.

**Flow 2: Result resolves, badge awarded**
Trigger: APScheduler runs check_bets() after a match finishes.
Steps: (1) Scheduler queries open bets for finished matches. (2) For each resolved bet: updates status to won/lost, credits balance if won. (3) Achievement service checks triggered milestones — if "First Correct Call" criterion met, inserts achievement record. (4) User opens app, sees updated profile badge, updated balance, updated leaderboard rank.
Outcome: User's profile reflects the result; badge displayed; leaderboard recalculates.
Success criteria: Resolution happens within 10 minutes of match end. User profile updates correctly without manual refresh.

**Flow 3: Check leaderboard, follow a rival**
Trigger: User wants to see how they rank.
Steps: (1) Opens Leaderboard screen via bottom nav. (2) Sees global rankings by win rate — their own row highlighted. (3) Taps on another user's row. (4) Views their profile: win rate, streak, recent picks, badges. (5) Taps Follow. (6) Returns to Match Feed, can now see friend's recent predictions in a secondary tab.
Outcome: Social connection established, friend's predictions visible.
Success criteria: Leaderboard loads in under 2 seconds. Follow action persists across sessions.

### Success Metrics

**Primary metric:** Qualitative — the codebase passes a technical interview review. TypeScript strict, tests green, CI passing, README honest.

**Secondary metrics for app quality:**
- 7-day retention: >30% of registered users return within 7 days of sign-up (good: 30%, great: 50%)
- Magic moment conversion: >60% of new users place at least one prediction in their first session (good: 60%, great: 80%)
- Resolution reliability: >99% of finished matches trigger correct bet resolution within 10 minutes (good: 99%, great: 99.9%)
- Win rate leaderboard: at least 20 qualified users (5+ predictions) within 30 days of launch to make the leaderboard meaningful

**Leading indicators:**
- TypeScript coverage reaching strict mode with zero `any` types in components
- pytest coverage for Services layer >80%
- GitHub Actions CI green on every PR
- README receiving positive recruiter feedback

### Risks

**Risk 1 — Football API reliability.** The third-party football API may have rate limits, downtime, or delayed result reporting. Impact: matches don't resolve, users see stale data. Mitigation: build explicit error handling in the scheduler, log all API failures, test with mock data in CI.

**Risk 2 — TypeScript migration breaks working code.** Migrating from JSX to TSX across 5 screens, a Supabase client, and custom hooks introduces real regression risk. Mitigation: migrate one file at a time, add tests before migrating each component, use `// @ts-expect-error` as a temporary escape hatch with a TODO rather than silent breakage.

**Risk 3 — Empty leaderboard kills the magic moment.** A new user who sees a leaderboard with only themselves ranked has no context for their position. Mitigation: seed the leaderboard with 20–50 realistic bot predictions before any real users join.

**Risk 4 — Achievement system is too thin to retain users.** Five badges may not be enough long-term motivation. Mitigation: the five MVP badges are designed to be achievable quickly (First Correct Call is very easy) — this creates early dopamine. Expanding the badge set is a first v2 task.

**Risk 5 — The tech portfolio reads as a tutorial project.** If the app looks too much like a demo (fake data, only happy-path tests, no error handling), it won't impress a senior engineer. Mitigation: prioritize edge cases, document what was hard and why in the README, and write tests that cover failure states, not just success paths.

**Risk 6 — Supabase free tier limits.** The free tier has row count and API call limits that may be hit during testing or light production use. Mitigation: monitor usage, optimize queries (avoid n+1 patterns in bet resolution), and cache match data locally on the device.

---

## 4. Brand Strategy

### Positioning Statement

For football fans who want to prove their knowledge and compete with friends, Matchday is the free prediction game that turns every real match into a skill competition. Unlike sports betting apps, Matchday uses virtual coins and ranks you on accuracy — it's about being right, not lucky.

### Brand Personality

Matchday is the sharpest person in the group chat. They've done the research, they're confident in their call, and they'll back it up with their record. They're not showy — the data speaks louder than they do. They're respectful of the game and its complexity. They don't hedge ("could go either way") — they commit to a position.

In practice: copy is clipped and declarative. "MAKE YOUR CALL." not "What do you think will happen?" Interface labels are uppercase and terse — "MATCH FEED", "ANALYST", "EXECUTE PREDICTION". Empty states are dry wit, not apologetic: "NO ACTIVE MARKETS. Data stream is quiet." Error states are factual: "INSUFFICIENT BALANCE" not "Uh oh, that didn't work!"

The brand would wear a dark technical jacket, not a neon sportsbook logo. It would be at home at a football analytics conference or a developer meetup, but would fit just as naturally in a pub group chat full of people who take their predictions seriously.

### Voice & Tone Guide

**Voice (constant):** Precise. Data-literate. Confident. Spare. Never casual or chatty.

| Context | DO | DON'T |
|---|---|---|
| Onboarding | "INITIALIZE ACCOUNT — set your display name and you're live." | "Welcome to Matchday! We're so excited to have you here 🎉" |
| Prediction confirmation | "PREDICTION LOGGED. 50 coins on HOME. Match resolves Saturday 15:30." | "Great pick! We've saved your bet. Good luck!" |
| Error state | "INSUFFICIENT BALANCE. Add more coins by winning predictions." | "Oops! You don't have enough coins for that." |
| Win state | "CORRECT CALL. Bayern 2–1 Dortmund. +82 coins. Win rate: 64%." | "You won! 🎉 Great job predicting that one!" |
| Empty leaderboard | "NO RANKED ANALYSTS YET. Make 5 predictions to qualify." | "No one here yet! Be the first to join the leaderboard." |

### Messaging Framework

**Tagline:** Your record speaks for itself.

**Homepage / App Store headline:** The free prediction game where real football results determine who actually knows their football.

**Value propositions:**
1. Zero stakes, real outcomes — virtual coins only, every result from live Bundesliga and Champions League fixtures.
2. Your track record, always visible — win rate, streaks, and badges that prove your prediction quality over time.
3. Compete with friends on a real leaderboard — follow rivals, see their picks, prove you read the game better.

**Objection handlers:**
- "How is this different from betting?" — No money. Ever. You start with virtual coins, keep earning by being right. It's about skill, not risk.
- "Why not just use a group chat?" — Group chats don't track your win rate over 60 matches. They don't give you a leaderboard rank. They don't tell you your win percentage against the odds.

### Elevator Pitches

**5-second:** "It's a free prediction game for football. You call match outcomes with virtual coins, build a win rate, and compete on a leaderboard."

**30-second:** "Matchday is a free social prediction game for football fans. You predict match outcomes on real Bundesliga and Champions League fixtures using virtual coins — no real money. When matches finish, results resolve automatically, your win rate updates, and you see exactly where you rank against everyone else. It's what your group chat prediction thread would be if it kept score."

**2-minute:** "Every football fan has predictions. Every match, millions of people call it in their head or in a group chat. But those predictions disappear — there's no record, no leaderboard, no proof that you've been calling it right for years. Matchday fixes that. It's a free prediction game — virtual coins only, no gambling, no risk — built on real live football fixtures. You make your calls before each match, the scheduler resolves results automatically when the final whistle blows, and your profile builds up a track record: win rate, streak, badges, leaderboard rank. Then you follow friends and compete. Right now, that experience doesn't exist cleanly anywhere. Sportsbooks want your money. Fantasy football takes too much time. WhatsApp threads disappear after the weekend. Matchday is the game that should have always existed for people who want to prove they know their football."

### Competitive Differentiation Narrative

The sports prediction space is full of products that either want your money (sportsbooks), want your weekly time commitment (fantasy football), or offer no structure at all (group chats). Matchday takes a different position: free, low-commitment, skill-centric. Virtual coins remove financial risk entirely — there's no deposit, no loss of real money, no addiction-pattern mechanics. Predictions are on real fixtures with real outcomes — not trivia questions or randomized challenges — which means your win rate actually means something. And the social layer (friends, leaderboard) provides the competitive context that makes any of this interesting. This is a gap in the market that Matchday is specifically designed to fill, and the dark analytics aesthetic reinforces it: this is for people who take the game seriously, not for people who want to spin a wheel.

### Brand Anti-Patterns

**Never use gambling language.** Words like "bet", "wager", "odds boost", "cashout", "bankroll", or "deposit" are banned from the UI. The app uses "prediction", "call", "coins", "return", and "balance". This is non-negotiable — it changes the product category in the user's mind.

**Never use exclamation marks in UI copy.** Exclamations feel casual and celebratory in a way that contradicts the brand. The app is data-forward and confident, not excitable. The one exception is marketing copy aimed at first-time discovery (App Store description, social media).

**Never use emoji in interface labels.** Emoji in app copy feels like a consumer product trying to be friendly. Matchday's friendliness comes from its clarity and speed, not from 🎉. The only emoji use case is user-generated content (usernames, achievements) — and even then, icons should be used instead of emoji in the system UI.

**Never show bright backgrounds or white-dominant screens.** The dark terminal aesthetic is the brand. A light mode version of Matchday would be a different product. Every screen maintains the surface hierarchy: #10141a base, #1a1f28 cards, #00f0ff highlights.

**Never approximate data.** If match data is unavailable, show an honest empty state, not estimated or placeholder fixtures. The entire value proposition rests on real data. A fake fixture destroys trust instantly.

---

## 5. Design Direction

### Design Philosophy

Data density over decoration. Every pixel on screen should earn its place by communicating something — a status, a stat, a relationship. Decorative elements exist only when they reinforce meaning (the cyan glow on a live match card communicates urgency without a word).

Dark-first is a constraint, not a theme. The dark surface system (#10141a base) is non-negotiable. It reduces eye strain during live sports watching (often in dim rooms), aligns with the terminal/analytics aesthetic, and distinguishes Matchday clearly from consumer sports apps.

Hierarchy through light, not through lines. No 1px borders between elements. Separation is achieved by surface elevation — cards sit on darker backgrounds, active elements float above cards. The design should feel like a control panel, not a form.

Interaction should feel weighted and immediate. Taps should feel like they do something. Predictions are committed, not casual — the UI should reflect that. Confirmation states, loading states, and success states are all first-class citizens.

### Visual Mood

Matchday looks like a Bloomberg Terminal designed by someone who loves football. The reference points are financial data dashboards, sports analytics platforms (StatsBomb, Opta), and command-line interfaces — not consumer apps. The palette is cool and precise: near-black backgrounds, a single electric cyan accent for live/active states, and a secondary purple for pending/processing states. Card elevation creates depth without shadows that feel decorative. Typography is tight, uppercase labels feel like column headers in a data table. The overall mood is: controlled, expert, live.

### Color Palette

| Role | Name | Hex | CSS Variable | Tailwind Token | Usage |
|---|---|---|---|---|---|
| Base background | surface | #10141a | --color-surface | `bg-surface` | Screen backgrounds |
| Recessed | surface-low | #13171f | --color-surface-low | `bg-surface-low` | Input fields, inner recesses |
| Cards | surface-container | #1a1f28 | --color-surface-container | `bg-surface-container` | Match cards, analytics modules |
| Dividers | surface-high | #21262f | --color-surface-high | `bg-surface-high` | Subtle separators, secondary chips |
| Active widgets | surface-highest | #31353c | --color-surface-highest | `bg-surface-highest` | Selected chips, active states |
| Headline text | primary | #dbfcff | --color-primary | `text-primary` | Headings, key data |
| CTA / live indicator | primary-glow | #00f0ff | --color-primary-glow | `text-primary-glow` | CTAs, live dots, scores, badges |
| Text on cyan | on-primary | #003640 | --color-on-primary | `text-on-primary` | Button labels on cyan buttons |
| Pending accent | secondary | #d4b4ff | --color-secondary | `text-secondary` | Pending bet labels, register accent |
| Focus / input | secondary-glow | #9b59ff | --color-secondary-glow | `text-secondary-glow` | Input focus, probability bar fill |
| Error / loss | error | #ff4d6a | --color-error | `text-error` | Error states, lost bets |
| Body text | on-surface | #e2e8f0 | --color-on-surface | `text-on-surface` | Body copy |
| Muted text | on-surface-dim | #8b95a1 | --color-on-surface-dim | `text-on-surface-dim` | Labels, secondary info |
| Won state | success | #00f0ff | --color-success | `text-success` | Alias of primary-glow for won bets |

Dark mode only — no light mode. All surfaces assume the dark palette.

### Typography

**Primary font — Inter.** A geometric sans-serif with excellent legibility at small sizes and strong support for tabular numbers (key for scores, odds, and balances). Load weights: 400 (body), 600 (labels), 700 (subheadings), 800 (headings), 900 (hero data points).

**Mono font — JetBrains Mono** (or system mono fallback). Used sparingly for match IDs, fixture codes, and any data that benefits from monospaced alignment.

**Type scale (base 16px, ratio 1.25):**
- `text-xs`: 10px / 12px line-height — uppercase labels, eyebrow text
- `text-sm`: 12px / 16px — secondary data, timestamps
- `text-base`: 15px / 20px — body copy, odds values
- `text-lg`: 18px / 24px — card headings, team names
- `text-xl`: 20px / 28px — section headers
- `text-2xl`: 24px / 32px — navbar titles
- `text-4xl`: 36px / 40px — hero data (balance display)
- `text-display`: 44px / 48px — brand headline ("MATCHDAY")

**Letter spacing:** Uppercase labels use `tracking-widest` (0.2em+). Headlines use `tracking-tight` (−0.5px). Data values use `tracking-normal`.

### Spacing & Layout

Base unit: 4px. All spacing uses multiples of 4.

Scale: 4 / 8 / 12 / 16 / 20 / 24 / 32 / 40 / 48 / 64 / 96 px

Screen padding: 16px horizontal on all screens. Content groups separated by minimum 24px. Section headers padded 28px from previous section bottom.

Safe area: all screens respect safe area insets (status bar top, home indicator bottom) via Expo's SafeAreaView or equivalent.

Card internal padding: 18px all sides. Card gap in lists: 12px.

Bottom navigation bar height: 64px + safe area bottom.

Max readable line length: 72 characters (not enforced on data-heavy screens).

### Component Philosophy

**Cards** are the primary container. All match data, user data, and prediction data lives inside cards on the surface-container background. Cards have 16px border-radius. No borders — elevation difference from background communicates containment.

**Buttons** follow three tiers: (1) Primary CTA — solid cyan (#00f0ff) fill, dark teal text (#003640), cyan glow shadow. (2) Secondary — transparent fill, 1px rgba(0,240,255,0.2) border (ghost). (3) Tertiary — text only in on-surface-dim. Disabled state removes glow and desaturates to surface-high.

**Inputs** use surface-low background, no visible border at rest. On focus, a 2px bottom underline animates from surface-high to secondary-glow (#9b59ff) with a subtle purple glow shadow. Error state switches underline to error (#ff4d6a).

**Chips/badges** are small pill-shaped containers: 4–6px border-radius, uppercase text-xs with wide letter-spacing. Status variants: LIVE (rgba(0,240,255,0.08) bg, cyan text), FINAL (rgba(139,149,161,0.08) bg, dim text), UPCOMING (surface-high bg, dim text).

**Glow effects** use React Native StyleSheet shadowColor — NativeWind cannot produce glow. Every glow should be intentional and meaningful: cyan for live/active, purple for processing/pending, no glow for neutral states.

### Iconography & Imagery

Icon library: **Lucide React Native**. Outline style, 20px default size, 1.5px stroke weight. Icons used for navigation, actions, and status only — not decorative.

No photography or illustration in the core app. The data is the content. If imagery is needed (e.g. team logos from the API), it should be displayed as small, contained elements within cards — never as backgrounds or hero images.

Achievement badge icons are a design system opportunity: each badge has a specific Lucide icon + a colored glow treatment. First Correct Call: Target + cyan glow. Streak: Zap + purple glow. Sharp Analyst: TrendingUp + cyan glow.

No stock photography. No generic sports imagery. No emoji-style stickers.

### Accessibility Commitments

**Color contrast:** All body text (on-surface #e2e8f0 on surface-container #1a1f28) achieves ≥ 7:1 (AAA). Primary CTA text (on-primary #003640 on primary-glow #00f0ff) achieves ≥ 4.5:1 (AA). Every new color combination must be verified before merge.

**Touch targets:** All interactive elements minimum 44×44px. Chips that are smaller visually must have expanded hit areas via padding or hitSlop.

**Screen reader support:** Every interactive element has an `accessibilityLabel` and `accessibilityRole`. Match cards describe their content: "Bayern vs Dortmund, upcoming Saturday, home odds 1.65". This is checked via automated accessibility audit in CI.

**Focus indicators:** In environments with keyboard/pointer input (iPad, paired keyboard), focused elements show a visible cyan outline.

**Motion:** All animations should respect `prefers-reduced-motion` where detectable. No auto-playing video or looping animation that can't be stopped.

### Motion & Interaction

Default transition duration: 200ms for micro-interactions (button press, chip selection), 300ms for screen transitions and modals.

Easing: `ease-out` for elements entering the screen (decelerate into position), `ease-in-out` for state toggles (button press, selection change).

Input focus: bottom underline color transition over 200ms with a simultaneous box-shadow fade-in on the glow.

Bet confirmation: coin balance decrements with a brief flash (opacity 0.6 → 1.0 over 150ms) to signal the transaction.

Result resolution: balance increment should use a counting animation (number increments visually over 500ms) to make the reward feel physical. This is a UI delight moment — invest in it.

Loading states: `ActivityIndicator` with primary-glow color (#00f0ff) on all async data fetches. Loading text below in text-xs uppercase: "LOADING DATA STREAM", "RESOLVING RESULTS", etc.

### Design Tokens

The single source of truth for implementation. All tokens should be defined in `tailwind.config.js` (colors) and accessed via CSS variables in StyleSheet objects (for glow effects not supported by NativeWind).

| Token Name | CSS Variable | Tailwind Class | Value |
|---|---|---|---|
| surface | --color-surface | bg-surface | #10141a |
| surface-low | --color-surface-low | bg-surface-low | #13171f |
| surface-container | --color-surface-container | bg-surface-container | #1a1f28 |
| surface-high | --color-surface-high | bg-surface-high | #21262f |
| surface-highest | --color-surface-highest | bg-surface-highest | #31353c |
| primary | --color-primary | text-primary | #dbfcff |
| primary-glow | --color-primary-glow | text-primary-glow | #00f0ff |
| on-primary | --color-on-primary | text-on-primary | #003640 |
| secondary | --color-secondary | text-secondary | #d4b4ff |
| secondary-glow | --color-secondary-glow | text-secondary-glow | #9b59ff |
| error | --color-error | text-error | #ff4d6a |
| on-surface | --color-on-surface | text-on-surface | #e2e8f0 |
| on-surface-dim | --color-on-surface-dim | text-on-surface-dim | #8b95a1 |
| radius-card | --radius-card | rounded-2xl | 16px |
| radius-chip | --radius-chip | rounded | 6px |
| radius-button | --radius-button | rounded-xl | 12px |
| shadow-glow-cyan | (StyleSheet only) | — | shadowColor: #00f0ff, opacity: 0.35, radius: 20 |
| shadow-glow-purple | (StyleSheet only) | — | shadowColor: #9b59ff, opacity: 0.35, radius: 20 |
| spacing-card-pad | — | p-[18px] | 18px |
| spacing-screen-pad | — | px-4 | 16px |
| spacing-section-gap | — | mt-7 | 28px |
| duration-micro | — | duration-200 | 200ms |
| duration-transition | — | duration-300 | 300ms |
| font-display | — | font-black text-[44px] | Inter 900, 44px |
| font-data-lg | — | font-extrabold text-[36px] | Inter 800, 36px |
| font-label | — | font-bold text-[10px] tracking-widest | Inter 700, 10px, +0.2em |
