# 🌿 PCOS Saathi — AI-Powered Personal Health Copilot
### Frontend Application (Vite + React + CSS)

> **Hackathon Edition**: A complete, polished, interactive frontend designed to feel and behave like a state-of-the-art health-tech companion. 
> Built strictly as a **standalone frontend** with realistic mock data, local state, and `localStorage` persistence.

---

## 🚀 Quick Setup & Launch

```bash
# 1. Navigate to the frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start the Vite development server
npm run dev
```

The application will be live at: **`http://localhost:5173`**

To preview the production bundle:
```bash
npm run build
npm run preview
```

---

## 🛠️ Technology Stack
* **Framework**: React 18 & Vite
* **Routing**: React Router DOM (`react-router-dom`)
* **Styling**: Vanilla CSS3 design system (`variables.css`, `global.css`, `components.css`, `responsive.css`)
* **Icons**: Emoji & SVG icons (zero external icon runtime crashes)
* **Voice & Audio**: Web Speech API (`SpeechRecognition` for speech-to-text in Telugu `te-IN` and English `en-IN`, `SpeechSynthesis` for audio playback)
* **Persistence**: Browser `localStorage` via custom React hook `useLocalStorage`

---

## 📁 Complete Folder Structure

```text
frontend/
├── public/
│   └── favicon.svg
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── Button.jsx                 # Reusable variants & sizes
│   │   ├── Modal.jsx                  # Accessible dialog with escape listener
│   │   ├── ProgressBar.jsx            # Day & cycle progress indicators
│   │   ├── EmptyState.jsx             # Clean fallback for missing records
│   │   ├── StatCard.jsx               # Metric snapshot cards with badges
│   │   ├── PageHeader.jsx             # Standard title, subtitle, and action row
│   │   ├── NotificationPanel.jsx      # Top dropdown with unread badge
│   │   ├── ChatMessage.jsx            # Message bubbles with sources & audio
│   │   ├── MealCard.jsx               # Indian dish with protein/fibre breakdown
│   │   ├── ReportCard.jsx             # Document card with biomarker flags
│   │   ├── ReminderCard.jsx           # Task item with completion toggle
│   │   ├── CommunityPost.jsx          # Discussion card with educator badges
│   │   ├── Navbar.jsx                 # Top bar with language & notifications
│   │   ├── Sidebar.jsx                # Left desktop navigation
│   │   ├── MobileNavigation.jsx       # Bottom navigation for mobile viewports
│   │   └── SafetyBanner.jsx           # Persistent medical ethics disclaimer
│   ├── pages/
│   │   ├── Welcome.jsx                # Introduction & demo landing page
│   │   ├── Dashboard.jsx              # Main home overview & snapshot cards
│   │   ├── HealthProfile.jsx          # Personal diet, age, and cycle preferences
│   │   ├── HealthAssistant.jsx        # Bilingual Telugu/English AI Chat
│   │   ├── CycleTracker.jsx           # Menstrual calendar & cautious variance
│   │   ├── FoodCompanion.jsx          # Indian PCOS meal planner & filters
│   │   ├── MedicalReports.jsx         # Lab panel organizer & plain language OCR
│   │   ├── DoctorPreparation.jsx      # 1-page printable consultation brief
│   │   ├── SmartReminders.jsx         # Medication and care routine tracker
│   │   ├── Community.jsx              # Safe anonymous moderated Q&A
│   │   ├── Settings.jsx               # Privacy transparency & demo data reset
│   │   └── NotFound.jsx               # 404 fallback page
│   ├── features/
│   │   ├── assistant/
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── QuickQuestions.jsx
│   │   │   └── LanguageSelector.jsx
│   │   ├── cycle/
│   │   │   ├── CycleCalendar.jsx
│   │   │   ├── CycleSummary.jsx
│   │   │   └── CycleLogForm.jsx
│   │   ├── nutrition/
│   │   │   ├── MealPlanner.jsx
│   │   │   ├── MealFilters.jsx
│   │   │   └── MealDetails.jsx
│   │   ├── reports/
│   │   │   ├── UploadPanel.jsx
│   │   │   └── ReportSummary.jsx
│   │   └── community/
│   │       ├── CreatePost.jsx
│   │       ├── PostFeed.jsx
│   │       └── ReportPostModal.jsx
│   ├── data/
│   │   ├── sampleMeals.js
│   │   ├── sampleQuestions.js
│   │   ├── sampleReports.js
│   │   ├── sampleReminders.js
│   │   └── samplePosts.js
│   ├── hooks/
│   │   └── useLocalStorage.js
│   ├── utils/
│   │   ├── dateUtils.js
│   │   ├── formatters.js
│   │   └── mockResponses.js
│   ├── styles/
│   │   ├── variables.css
│   │   ├── global.css
│   │   ├── components.css
│   │   └── responsive.css
│   ├── App.jsx
│   └── main.jsx
├── index.html
├── package.json
├── vite.config.js
└── .gitignore
```

---

## 🌟 Key Functional Features
1. **Bilingual Telugu & English AI Assistant**:
   - Web Speech API speech-to-text in Telugu (`te-IN`) and English (`en-IN`).
   - Browser speech synthesis for audio answer playback.
   - Grounded knowledge base for PCOS education with source citations.
2. **Indian Food PCOS Companion**:
   - Familiar dishes: *Moong Dal Pesarattu*, *Ragi Idli*, *Korralu (Foxtail Millet) Dal*, *Kala Chana Chaat*, *Paneer*, and *Fish Curry*.
   - Filter by diet (Veg, Egg, Non-Veg) and budget pantry staples.
   - Daily meal planner for Breakfast, Lunch, and Dinner.
3. **Menstrual Cycle Intelligence**:
   - Models natural PCOS cycle variability (±4-6 days) rather than false exact calendar dates.
   - Color-coded calendar showing recorded period days, estimated windows, and today.
4. **Doctor Visit Preparation Assistant**:
   - Aggregates cycle logs, symptoms, flagged lab biomarkers (e.g., TSH 4.85 mIU/L), and high-yield questions into an appointment-ready **1-page clinical sheet**.
   - Native `window.print()` print formatting.
5. **Medical Record Organizer**:
   - Upload panel supporting PDF/JPG drag-and-drop.
   - Biomarker extraction table with status badges and plain-language translations.
6. **Safe PCOS Community**:
   - Anonymous pseudonyms by default.
   - Verified educator response badges.
   - Misinformation reporting modal.

---

## 🛡️ Medical Safety & Ethical Boundaries
- **Educational Only**: The AI explains terminology and ranges; it does not issue medical diagnoses or alter prescriptions.
- **Urgent Red Flags**: Queries mentioning severe pelvic pain or heavy bleeding trigger an immediate emergency clinical referral notice.
- **Privacy Notice**: All demo data is held in browser `localStorage`. No identifiable medical records are uploaded to external servers.
