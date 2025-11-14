# Claude Coding Agent Instructions

This document provides guidelines for AI coding agents working on the Toddler Games project.

## 🎯 Project Context

**Zero-build, browser-only JavaScript project** for toddlers (ages 2-4). Runs directly from GitHub Pages without build tools. Features include:
- 3 active games: Balloons (pop), Drawing (canvas), Bubbles (bubble wrap)
- PWA support with manifest.json and icons
- Polish speech synthesis (Web Speech API)
- Web Audio API-based sound effects
- Particle effects system
- LocalStorage state persistence

**Critical Requirements:**
- 🇵🇱 **All text, sounds, and instructions must be in POLISH**
- 📱 **Optimized for LANDSCAPE orientation on tablets/mobile devices**
- 🎨 **Design for horizontal layout (16:9 or 16:10 aspect ratio)**
- 📱 **Supports small phones in landscape (down to 667×375 resolution)**

## ⚠️ Critical Constraints

### MUST NOT Use:
- ❌ Node.js or npm
- ❌ Build tools (webpack, vite, parcel, etc.)
- ❌ Package managers
- ❌ TypeScript (unless inline with browser support)
- ❌ JSX or template languages requiring compilation
- ❌ External CDN dependencies (prefer inline/self-hosted)
- ❌ Module bundlers
- ❌ CSS preprocessors (SASS, LESS)
- ❌ Any framework (React, Vue, Angular, etc.)

### MUST Use:
- ✅ Pure vanilla JavaScript (ES6+ is fine if widely supported)
- ✅ Inline JavaScript or single/few `.js` files
- ✅ Pure CSS (CSS3 features are fine)
- ✅ HTML5 APIs (Canvas, Web Audio, LocalStorage, etc.)
- ✅ Self-contained code in repository
- ✅ Modern browser features (last 2-3 years)

## 📁 Current File Structure

```
toddler_games/
├── index.html              # Main menu with game selection
├── manifest.json           # PWA manifest (landscape, Polish)
├── icon.svg                # App icon (SVG)
├── icon-192.png            # App icon 192×192 (maskable)
├── icon-512.png            # App icon 512×512 (maskable)
├── games/                  # Individual game files
│   ├── balloons.html       # Balloon pop game (SVG balloons, score tracking)
│   ├── bubbles.html        # Bubble wrap game (visual feedback, patterns)
│   └── drawing.html        # Drawing canvas (rainbow mode, brush sizes)
├── shared/                 # Shared resources
│   ├── common.js           # SpeechManager, SoundManager, Utils, POLISH_TEXT
│   └── common.css          # Design system, animations, responsive layout
├── generate-icons.html     # Browser-based icon generator
├── create_icons.py         # Python icon generator (fallback)
├── .github/workflows/      # CI/CD automation
│   └── generate-icons.yml  # Auto-generate icons on push
├── README.md               # Project documentation
└── claude.md               # This file
```

## 🎨 Coding Standards

### HTML Template
```html
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Nazwa Gry - Gry dla Maluchów</title>
    <link rel="stylesheet" href="../shared/common.css">
</head>
<body>
    <div class="game-header">
        <a href="../index.html" class="home-btn">🏠 Dom</a>
        <h1>🎮 Nazwa Gry</h1>
        <button id="sound-toggle" class="sound-btn">🔊 Dźwięk</button>
    </div>
    <div id="game-container"></div>
    <script src="../shared/common.js"></script>
    <script>
        // Game code here
    </script>
</body>
</html>
```

**Key Points:**
- Always `lang="pl"` and UTF-8 charset (ą, ć, ę, ł, ń, ó, ś, ź, ż)
- Link to shared CSS/JS for consistency
- Include home button and sound toggle in header

### CSS - Use shared/common.css
**Available CSS Variables:**
- Colors: `--color-red`, `--color-blue`, `--color-yellow`, `--color-green`, `--color-purple`, `--color-orange`, `--color-pink`
- Spacing: `--spacing-sm` (10px), `--spacing-md` (20px), `--spacing-lg` (40px)
- Touch targets: `--touch-min` (60px), `--touch-lg` (100px)
- Transitions: `--transition-fast` (150ms), `--transition-medium` (300ms), `--transition-slow` (500ms)

**Available Animations:** `pop`, `float-up`, `bounce`, `pulse`, `shake`, `celebrate`, `rainbow`, `particle-burst`

**Key Principles:**
- Landscape-first design (horizontal layout)
- Min touch targets: 60px × 60px
- Use CSS transforms for animations (GPU accelerated)
- `touch-action: manipulation` to prevent zoom
- Portrait mode automatically shows rotation hint (via common.css)

**Responsive Breakpoints for Landscape Mode:**
The app uses mobile-first responsive design with specific breakpoints for landscape orientation:

- **≤700px width**: Very small phones (e.g., 667×375 - iPhone SE, iPhone 8)
  - 2-column game grid on main menu
  - Reduced header height (38px), smaller buttons (36px)
  - Drawing game: 80px toolbar width
  - Bubbles game: 4×3 grid, 35-50px bubbles
  - Balloons game: 60-100px balloon sizes
  - Compact fonts and minimal spacing

- **701-768px width**: Small phones and tablets
  - 3-column game grid on main menu
  - Header height 45px, buttons 40px
  - Standard game layouts with moderate scaling

- **769-1024px width**: Medium tablets
  - Full 3-column layout
  - Standard element sizes

- **>1024px width**: Large tablets and desktops
  - Larger fonts and spacing for comfortable viewing

**Always test landscape mode on small devices!** Use browser dev tools to simulate 667×375 resolution.

### JavaScript - Use shared/common.js

**Available Managers & Utilities:**

**SpeechManager** - Polish text-to-speech (Web Speech API, pl-PL):
```javascript
SpeechManager.speak("Brawo!");           // Generic speech
SpeechManager.speakColor("Czerwony");    // Color name
SpeechManager.speakCelebration();        // Random celebration
SpeechManager.speakNumber(42);           // Number pronunciation
SpeechManager.speakWelcome(gameName);    // Welcome message
SpeechManager.toggle();                  // Enable/disable
```

**SoundManager** - Web Audio API sound effects:
```javascript
SoundManager.playPop();                  // Pop sound (800→100Hz)
SoundManager.playCelebration();          // 4-note melody (C-E-G-C)
SoundManager.playSuccess();              // Success sound (rising)
SoundManager.playWhoosh();               // Whoosh effect
SoundManager.playNote(frequency, 0.3);   // Custom frequency
SoundManager.toggle();                   // Enable/disable
```

**Utils** - Helper functions:
```javascript
Utils.randomItem(array);                 // Random array element
Utils.getCelebration();                  // Random Polish praise
Utils.showCelebration(text);             // Show celebration popup
Utils.createParticles(x, y, color, 12);  // Particle burst effect
Utils.random(min, max);                  // Random float
Utils.randomInt(min, max);               // Random integer
Utils.vibrate(30);                       // Haptic feedback
```

**POLISH_TEXT** - Polish language constants:
- `POLISH_TEXT.celebrations[]` - Praise phrases
- `POLISH_TEXT.colors` - Color names
- `POLISH_TEXT.animals` - Animal names
- `POLISH_TEXT.shapes` - Shape names

**Key Principles:**
- Use object-based modules (no ES6 imports)
- Use `requestAnimationFrame` for animations
- Event delegation for efficiency
- CSS transforms over top/left (GPU accelerated)
- State persists via LocalStorage (sound/speech enabled)

## 🎮 Game Implementation Pattern

```javascript
const MyGame = {
    score: 0,
    isActive: false,

    init() {
        this.isActive = true;
        this.setupDOM();
        this.setupEventListeners();
        SpeechManager.speakWelcome("Nazwa Gry");
        this.start();
    },

    setupDOM() {
        document.querySelector('#game-container').innerHTML = `
            <div class="my-game"><!-- Game UI --></div>
        `;
    },

    setupEventListeners() {
        // Add event listeners
    },

    start() {
        this.gameLoop();
    },

    gameLoop() {
        if (!this.isActive) return;
        this.update();
        this.render();
        requestAnimationFrame(() => this.gameLoop());
    },

    update() {
        // Update game state
    },

    render() {
        // Render game
    },

    destroy() {
        this.isActive = false;
        // Clean up: remove listeners, cancel animations
    }
};

// Initialize on load
window.addEventListener('load', () => MyGame.init());
```

## 🇵🇱 Polish Language

**CRITICAL: All text must be in Polish!**

**Use POLISH_TEXT constants** from shared/common.js:
- `POLISH_TEXT.celebrations[]` - "Brawo!", "Super!", "Wspaniale!", etc.
- `POLISH_TEXT.colors` - "Czerwony", "Niebieski", "Żółty", etc.
- `POLISH_TEXT.animals` - "Królik", "Piesek", "Kotek", etc.
- `POLISH_TEXT.shapes` - "Koło", "Kwadrat", "Trójkąt", etc.

**Polish Speech Synthesis** (via SpeechManager):
```javascript
// Automatically uses pl-PL voice, 0.9x rate, 1.1x pitch (toddler-optimized)
SpeechManager.speak("Brawo!");
SpeechManager.speakColor("Czerwony");
SpeechManager.speakCelebration(); // Random praise
```

**HTML must use Polish:**
```html
<button>🎈 Baloniki</button>
<button>🔊 Dźwięk</button>
<button>🏠 Dom</button>
```

**Polish Characters:** Ensure UTF-8 encoding supports ą, ć, ę, ł, ń, ó, ś, ź, ż (and capitals).

## 🔧 Common Tasks

### Creating a New Game
1. Create `games/newgame.html` using the HTML template
2. Add game link to `index.html` menu
3. Implement game logic using the pattern above
4. Use shared managers (SpeechManager, SoundManager, Utils)
5. Test in landscape mode on tablet

### Adding Interactive Elements
```javascript
// Particle burst on click
element.addEventListener('click', (e) => {
    Utils.createParticles(e.clientX, e.clientY, '#FF6B6B', 12);
    SoundManager.playPop();
    SpeechManager.speakCelebration();
    Utils.vibrate(30);
});
```

### Canvas Drawing
```javascript
const canvas = document.querySelector('#canvas');
const ctx = canvas.getContext('2d');
canvas.width = canvas.offsetWidth;
canvas.height = canvas.offsetHeight;

// Draw circle
ctx.fillStyle = '#FF6B6B';
ctx.beginPath();
ctx.arc(x, y, radius, 0, Math.PI * 2);
ctx.fill();
```

### Score Tracking with Milestones
```javascript
updateScore() {
    this.score++;
    if (this.score % 10 === 0) {
        SpeechManager.speakNumber(this.score);
        SoundManager.playCelebration();
    } else if (this.score % 5 === 0) {
        SpeechManager.speakCelebration();
    }
}
```

## 🧪 Testing Checklist

- [ ] **Landscape mode works** (primary use case, portrait shows rotation hint)
- [ ] **Tested on small phones** (667×375 resolution in landscape mode)
- [ ] **All text is in Polish** (no English visible)
- [ ] Polish characters display correctly (ą, ć, ę, ł, ń, ó, ś, ź, ż)
- [ ] Touch targets ≥ 60px × 60px (or appropriately scaled for small screens)
- [ ] Smooth 60fps animation
- [ ] No console errors
- [ ] Sound/speech toggle works (state persists)
- [ ] Works without internet (after first load)
- [ ] Works in GitHub Pages
- [ ] No build step required

## 🚫 Common Pitfalls

1. ❌ **English text** → ✅ Use Polish (`POLISH_TEXT` constants)
2. ❌ `<html lang="en">` → ✅ `<html lang="pl">`
3. ❌ Portrait-first design → ✅ Landscape-first (horizontal layouts)
4. ❌ Testing only on tablets → ✅ Test on small phones (667×375) too!
5. ❌ `import/export` → ✅ Object-based modules
6. ❌ npm packages → ✅ Self-contained code
7. ❌ Small touch targets → ✅ Minimum 60px × 60px (scaled appropriately)
8. ❌ Forgetting cleanup → ✅ Remove listeners in `destroy()`
9. ❌ Absolute paths `/styles.css` → ✅ Relative `./shared/common.css`
10. ❌ Fixed layouts → ✅ Add responsive breakpoints (@media queries)

## 🎯 Performance Tips

- Use CSS transforms (not top/left) for animations
- Use `requestAnimationFrame` for game loops
- Event delegation over multiple listeners
- Remove event listeners in `destroy()`
- Batch DOM updates

## 🎨 Assets

**Images:** Use inline SVG or emoji (🎈🎨🐰🎹). Keep PNGs <100KB.
**Sounds:** Use Web Audio API (see SoundManager) or short MP3 files (<2s).

## 📦 Deployment

Push to GitHub → Enable Pages in settings → Access at `https://username.github.io/toddler_games/`
No build step needed!

## 💡 Quick Reference

```javascript
// Speech & Sound
SpeechManager.speak("Brawo!");
SoundManager.playPop();

// Interactions
Utils.createParticles(x, y, color, 12);
Utils.vibrate(30);
Utils.showCelebration("Super!");

// Random
Utils.randomItem(array);
Utils.random(0, 100);

// Polish text
POLISH_TEXT.celebrations[0]; // "Brawo!"
POLISH_TEXT.colors.red;      // "Czerwony"

// Animations
element.style.animation = 'pop 0.4s ease-out forwards';
```

---

**Remember:** 🇵🇱 Polish language | 📱 Landscape orientation | 🎮 No build tools!
