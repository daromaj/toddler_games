# Claude Coding Agent Instructions

This document provides guidelines for AI coding agents working on the Toddler Games project.

## 🎯 Project Context

This is a **zero-build, browser-only JavaScript project** designed for toddlers (ages 2-4). The entire application must run directly from GitHub Pages without any build step, bundlers, or package managers.

**Critical Requirements:**
- 🇵🇱 **All text, sounds, and instructions must be in POLISH**
- 📱 **Optimized for LANDSCAPE orientation on tablets/mobile devices**
- 🎨 **Design for horizontal layout (16:9 or 16:10 aspect ratio)**

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

## 📁 File Structure

Keep it simple! Prefer this structure:

```
toddler_games/
├── index.html          # Main entry point (can contain everything)
├── styles.css          # (Optional) Separate CSS file
├── game.js             # (Optional) Separate JavaScript file
├── assets/             # (Optional) Images, sounds
│   ├── sounds/
│   └── images/
├── README.md           # Project documentation
└── claude.md           # This file
```

**Preferred approach**: Single `index.html` file with inline CSS and JavaScript for maximum simplicity and GitHub Pages compatibility.

## 🎨 Coding Standards

### HTML
```html
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <meta name="mobile-web-app-capable" content="yes">
    <title>Gry dla Maluchów</title>
    <style>
        /* Inline CSS here or link to styles.css */
        /* Optimize for landscape orientation */
        @media (orientation: portrait) {
            body::before {
                content: "Obróć tablet poziomo 🔄";
                /* Suggest landscape rotation */
            }
        }
    </style>
</head>
<body>
    <!-- Game content -->
    <script>
        // Inline JavaScript or link to game.js
    </script>
</body>
</html>
```

**Important HTML Notes:**
- `lang="pl"` - Sets Polish as the document language
- `user-scalable=no` - Prevents accidental zooming on tablets
- UTF-8 charset is critical for Polish characters (ą, ć, ę, ł, ń, ó, ś, ź, ż)
- Title should be in Polish: "Gry dla Maluchów" (Games for Toddlers)

### CSS Guidelines
- Use **CSS Grid** and **Flexbox** for layouts
- Use **CSS Custom Properties** for colors/sizes (easy theming)
- Use **CSS Transforms** for animations (better performance)
- Avoid float-based layouts
- **Landscape-first approach** - design for horizontal orientation
- Minimum touch target: **60px × 60px**
- Design for common tablet resolutions: 1024×768, 1280×800, 1920×1080

Example:
```css
:root {
    --primary-color: #FF6B6B;
    --secondary-color: #4ECDC4;
    --touch-target-min: 60px;
    --border-radius: 15px;
}

/* Landscape-optimized layout */
body {
    min-height: 100vh;
    min-height: 100dvh; /* Dynamic viewport height */
    overflow: hidden;
}

/* Horizontal flex layout for landscape */
.game-container {
    display: flex;
    flex-direction: row; /* Horizontal layout */
    gap: 20px;
    height: 100vh;
}

/* Side navigation for landscape */
.game-menu {
    width: 200px; /* Fixed width sidebar */
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.game-area {
    flex: 1; /* Takes remaining width */
    display: flex;
    align-items: center;
    justify-content: center;
}

.game-button {
    min-width: var(--touch-target-min);
    min-height: var(--touch-target-min);
    font-size: 24px;
    border-radius: var(--border-radius);
    cursor: pointer;
    touch-action: manipulation; /* Prevents double-tap zoom */
}

/* Portrait warning/hint */
@media (orientation: portrait) {
    .rotation-hint {
        display: flex;
        align-items: center;
        justify-content: center;
        position: fixed;
        inset: 0;
        background: var(--primary-color);
        color: white;
        font-size: 48px;
        z-index: 9999;
    }
}
```

### JavaScript Guidelines

#### 1. Module Pattern (No ES Modules)
Use object-based modules since we can't use ES6 imports without a build step:

```javascript
const GameEngine = {
    currentGame: null,
    soundEnabled: true,

    init() {
        this.setupEventListeners();
        this.loadGame('menu');
    },

    loadGame(gameName) {
        if (this.currentGame && this.currentGame.destroy) {
            this.currentGame.destroy();
        }
        this.currentGame = window[gameName];
        if (this.currentGame && this.currentGame.init) {
            this.currentGame.init();
        }
    },

    setupEventListeners() {
        // Event delegation for efficiency
        document.addEventListener('click', this.handleClick.bind(this));
    }
};

const BalloonPopGame = {
    balloons: [],
    animationId: null,

    init() {
        console.log('Balloon Pop initialized');
        this.setupCanvas();
        this.start();
    },

    start() {
        this.spawnBalloon();
        this.gameLoop();
    },

    gameLoop() {
        this.update();
        this.render();
        this.animationId = requestAnimationFrame(() => this.gameLoop());
    },

    destroy() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        this.balloons = [];
    }
};
```

#### 2. Event Handling
- Use **event delegation** where possible
- Prevent default behaviors that interfere with touch
- Handle both `click` and `touchstart` if needed (or just `click` for simplicity)

```javascript
// Good: Event delegation
document.querySelector('#game-container').addEventListener('click', (e) => {
    if (e.target.matches('.balloon')) {
        this.popBalloon(e.target);
    }
});

// Prevent accidental zoom on double-tap
button.style.touchAction = 'manipulation';
```

#### 3. Animation
Use `requestAnimationFrame` for smooth animations:

```javascript
function animate() {
    // Update positions
    updateGameObjects();

    // Render
    render();

    // Continue loop
    requestAnimationFrame(animate);
}
```

Use CSS transforms for best performance:
```javascript
// Good: Use transforms
element.style.transform = `translate(${x}px, ${y}px) scale(${scale})`;

// Avoid: Triggering layout recalculations
element.style.left = x + 'px';
element.style.top = y + 'px';
```

#### 4. Sound
Use Web Audio API or HTML5 Audio:

```javascript
// Simple approach with HTML5 Audio
const sounds = {
    pop: new Audio('data:audio/wav;base64,...'), // Inline base64 or external file
    success: new Audio('data:audio/wav;base64,...')
};

function playSound(soundName) {
    if (GameEngine.soundEnabled && sounds[soundName]) {
        sounds[soundName].currentTime = 0;
        sounds[soundName].play().catch(e => console.log('Sound play failed:', e));
    }
}
```

## 🎮 Game Implementation Pattern

Each game should follow this structure:

```javascript
const MyGame = {
    // Game state
    isActive: false,
    score: 0,

    // Initialize game
    init() {
        this.isActive = true;
        this.setupDOM();
        this.setupEventListeners();
        this.start();
    },

    // Setup DOM elements
    setupDOM() {
        const container = document.querySelector('#game-container');
        container.innerHTML = `
            <div class="my-game">
                <!-- Game UI -->
            </div>
        `;
    },

    // Setup event listeners
    setupEventListeners() {
        // Add listeners
    },

    // Start game loop
    start() {
        this.gameLoop();
    },

    // Main game loop
    gameLoop() {
        if (!this.isActive) return;

        this.update();
        this.render();

        requestAnimationFrame(() => this.gameLoop());
    },

    // Update game state
    update() {
        // Update logic
    },

    // Render game
    render() {
        // Render logic
    },

    // Cleanup
    destroy() {
        this.isActive = false;
        // Remove event listeners
        // Clear intervals/timeouts
        // Cancel animation frames
    }
};
```

## 🎨 Design Implementation

### Colors for Toddlers
```css
:root {
    /* Primary vibrant colors */
    --color-red: #FF6B6B;
    --color-blue: #4ECDC4;
    --color-yellow: #FFE66D;
    --color-green: #95E1D3;
    --color-purple: #C7A7FF;
    --color-orange: #FFAA5C;

    /* Backgrounds */
    --bg-primary: #FFFFFF;
    --bg-secondary: #F7F9FC;

    /* Sizes */
    --touch-min: 60px;
    --spacing-sm: 10px;
    --spacing-md: 20px;
    --spacing-lg: 40px;
}
```

### Landscape Layout Design
```css
/* Landscape-first layout for tablets */
.game-container {
    display: flex;
    flex-direction: row; /* Horizontal layout */
    height: 100vh;
    padding: var(--spacing-md);
    gap: var(--spacing-lg);
}

/* Left sidebar for game menu */
.sidebar {
    width: 180px;
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
}

/* Main game area takes remaining space */
.game-area {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg-secondary);
    border-radius: 20px;
}

/* Larger tablets (landscape) */
@media (min-width: 1024px) and (orientation: landscape) {
    .sidebar {
        width: 220px;
    }
    .game-container {
        padding: var(--spacing-lg);
    }
}

/* Warn in portrait mode */
@media (orientation: portrait) {
    .portrait-warning {
        display: flex;
        position: fixed;
        inset: 0;
        background: #FF6B6B;
        color: white;
        font-size: 36px;
        align-items: center;
        justify-content: center;
        z-index: 10000;
    }
}
```

### Animations
```css
/* Smooth, playful animations */
.balloon {
    transition: transform 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.balloon:active {
    transform: scale(0.9);
}

/* Pop animation */
@keyframes pop {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.3); opacity: 0.8; }
    100% { transform: scale(0); opacity: 0; }
}

.popping {
    animation: pop 0.4s ease-out forwards;
}
```

## 🇵🇱 Polish Language Implementation

**CRITICAL: All user-facing text must be in Polish!**

### Polish Text Constants

Create a translations object in your JavaScript:

```javascript
const POLISH = {
    // Main menu
    title: "Gry dla Maluchów",
    home: "Dom",
    back: "Powrót",

    // Controls
    sound: "Dźwięk",
    soundOn: "Włącz dźwięk",
    soundOff: "Wyłącz dźwięk",
    clear: "Wyczyść",
    reset: "Od nowa",

    // Colors (Kolory)
    colors: {
        red: "Czerwony",
        blue: "Niebieski",
        yellow: "Żółty",
        green: "Zielony",
        purple: "Fioletowy",
        orange: "Pomarańczowy"
    },

    // Shapes (Kształty)
    shapes: {
        circle: "Koło",
        square: "Kwadrat",
        triangle: "Trójkąt",
        star: "Gwiazdka",
        heart: "Serce"
    },

    // Animals (Zwierzęta)
    animals: {
        bunny: "Królik",
        puppy: "Piesek",
        kitten: "Kotek",
        bear: "Miś",
        elephant: "Słoń",
        monkey: "Małpka"
    },

    // Encouragement (Zachęta)
    praise: [
        "Brawo!",
        "Świetnie!",
        "Doskonale!",
        "Super!",
        "Wspaniale!",
        "Tak trzymaj!"
    ],

    // Instructions (Instrukcje)
    instructions: {
        tap: "Dotknij",
        draw: "Rysuj",
        feed: "Nakarm zwierzątko",
        choose: "Wybierz",
        tryAgain: "Spróbuj jeszcze raz"
    },

    // Game names
    games: {
        balloonPop: "Baloniki",
        drawing: "Rysowanie",
        feeding: "Karmienie",
        piano: "Pianino",
        shapes: "Kształty",
        bubbles: "Bąbelki"
    },

    // Orientation hint
    rotateDevice: "Obróć tablet poziomo 🔄"
};

// Usage example
function showPraise() {
    const randomPraise = POLISH.praise[Math.floor(Math.random() * POLISH.praise.length)];
    displayMessage(randomPraise);
}
```

### Voice/Audio Guidelines

When adding voice prompts or text-to-speech:

```javascript
// Use Web Speech API for Polish voice
function speak(text) {
    if ('speechSynthesis' in window && GameEngine.soundEnabled) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'pl-PL'; // Polish language
        utterance.rate = 0.9; // Slightly slower for toddlers
        utterance.pitch = 1.2; // Slightly higher pitch (friendly)
        speechSynthesis.speak(utterance);
    }
}

// Example usage
speak(POLISH.praise[0]); // "Brawo!"
speak(POLISH.instructions.feed); // "Nakarm zwierzątko"
```

### HTML with Polish Text

Always use Polish in HTML:

```html
<button class="game-btn" data-game="balloonPop">
    🎈 Baloniki
</button>

<div class="controls">
    <button id="sound-toggle">🔊 Dźwięk</button>
    <button id="home-btn">🏠 Dom</button>
</div>

<div class="color-picker">
    <button data-color="red" style="background: var(--color-red)">
        Czerwony
    </button>
    <button data-color="blue" style="background: var(--color-blue)">
        Niebieski
    </button>
</div>
```

### Important Polish Characters

Ensure UTF-8 encoding supports these Polish characters:
- **ą, ć, ę, ł, ń, ó, ś, ź, ż**
- **Ą, Ć, Ę, Ł, Ń, Ó, Ś, Ź, Ż**

Test that they render correctly in all fonts and contexts.

## 🔧 Common Tasks

### Adding a New Game

1. Create game object following the pattern above
2. Add game icon/button to menu
3. Wire up game loading in GameEngine
4. Test on mobile device

### Adding Sound Effects

Option 1: External files
```javascript
const popSound = new Audio('./assets/sounds/pop.mp3');
```

Option 2: Inline base64 (keeps everything in one file)
```javascript
const popSound = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEA...');
```

Option 3: Web Audio API (more control)
```javascript
const audioContext = new (window.AudioContext || window.webkitAudioContext)();

function playTone(frequency, duration) {
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);

    oscillator.frequency.value = frequency;
    oscillator.type = 'sine';

    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration);

    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + duration);
}
```

### Drawing on Canvas

```javascript
const canvas = document.querySelector('#game-canvas');
const ctx = canvas.getContext('2d');

// Set canvas size
function resizeCanvas() {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
}

// Draw balloon
function drawBalloon(x, y, color, radius) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();

    // String
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(x, y + radius);
    ctx.lineTo(x, y + radius + 50);
    ctx.stroke();
}
```

### Particle Effects

```javascript
class Particle {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.vx = (Math.random() - 0.5) * 10;
        this.vy = (Math.random() - 0.5) * 10;
        this.life = 1.0;
        this.color = color;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.vy += 0.5; // Gravity
        this.life -= 0.02;
    }

    draw(ctx) {
        ctx.globalAlpha = this.life;
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, 5, 5);
        ctx.globalAlpha = 1.0;
    }

    isDead() {
        return this.life <= 0;
    }
}
```

## 🧪 Testing Checklist

When implementing features, verify:

- [ ] Works on tablets in **landscape mode** (primary use case)
- [ ] Portrait mode shows rotation hint
- [ ] Works on mobile (touch events)
- [ ] Works on desktop (mouse events)
- [ ] No console errors
- [ ] Smooth 60fps animation
- [ ] Touch targets are 60px+ minimum
- [ ] **All text is in Polish** (no English text visible)
- [ ] Polish characters display correctly (ą, ć, ę, ł, ń, ó, ś, ź, ż)
- [ ] UTF-8 encoding is set (`<meta charset="UTF-8">`)
- [ ] `lang="pl"` is set on `<html>` tag
- [ ] Loads without internet (after first load)
- [ ] Works in GitHub Pages environment
- [ ] No build step required
- [ ] All assets are self-contained or in repo
- [ ] Layout optimized for 1024×768 and 1280×800 (common tablet resolutions)

## 🚫 Common Pitfalls to Avoid

1. **Don't use English text** - ALL text must be in Polish
   ```javascript
   // ❌ Don't do this
   button.textContent = "Start Game";

   // ✅ Do this instead
   button.textContent = "Rozpocznij grę";
   ```

2. **Don't forget `lang="pl"`** - HTML document must specify Polish language
   ```html
   <!-- ❌ Wrong -->
   <html lang="en">

   <!-- ✅ Correct -->
   <html lang="pl">
   ```

3. **Don't design for portrait** - Optimize for landscape orientation
   ```css
   /* ❌ Avoid vertical layouts */
   .container {
       flex-direction: column;
       height: 100vh;
   }

   /* ✅ Use horizontal layouts */
   .container {
       flex-direction: row;
       width: 100vw;
   }
   ```

4. **Don't use import/export** - Not supported without build tools
   ```javascript
   // ❌ Don't do this
   import { Game } from './game.js';

   // ✅ Do this instead
   const Game = window.Game || {};
   ```

5. **Don't rely on npm packages** - Everything must be self-contained

6. **Don't use template literals in HTML** - Use DOM manipulation or innerHTML

7. **Don't forget tablet landscape testing** - Test on 1024×768 and 1280×800

8. **Don't use small touch targets** - Minimum 60px × 60px

9. **Don't forget to clean up** - Remove event listeners, cancel animations in destroy()

10. **Don't use relative paths incorrectly** - GitHub Pages serves from a subdirectory
    ```html
    <!-- ✅ Good -->
    <link rel="stylesheet" href="./styles.css">
    <script src="./game.js"></script>

    <!-- ❌ Might break on GitHub Pages -->
    <link rel="stylesheet" href="/styles.css">
    ```

## 📝 Code Comments

Add helpful comments for future developers:

```javascript
/**
 * Balloon Pop Game
 * Simple game where toddlers tap floating balloons to pop them
 */
const BalloonPopGame = {
    // Configuration
    spawnRate: 2000, // milliseconds between balloon spawns
    maxBalloons: 10,

    /**
     * Initialize the game
     * Sets up canvas, event listeners, and starts game loop
     */
    init() {
        // Implementation
    }
};
```

## 🎯 Performance Tips

1. **Use CSS transforms** instead of top/left for animations
2. **Limit DOM manipulation** - batch updates when possible
3. **Use requestAnimationFrame** for all animations
4. **Debounce resize events**
5. **Remove event listeners** in destroy methods
6. **Reuse objects** instead of creating new ones in loops
7. **Use event delegation** instead of multiple listeners

## 📦 Deployment

To deploy to GitHub Pages:

1. Push code to `main` branch (or designated branch)
2. Enable GitHub Pages in repository settings
3. Select source branch
4. Access via `https://username.github.io/toddler_games/`

No build step needed! The files run directly as-is.

## 🎨 Asset Guidelines

### Images
- Use **inline SVG** for scalable graphics (balloons, shapes, icons)
- Use **base64 encoded** images for small assets
- Keep image files **small** (<100KB each if possible)
- Use **emoji** for quick icons (🎈🎨🐰🎹)

### Sounds
- Keep sound files **short** (<2 seconds)
- Use **compressed formats** (MP3, OGG)
- Provide **fallback** if sound fails to load
- Make sounds **optional** (mute button)

## ✅ Definition of Done

A feature is complete when:

- [ ] Code works in Chrome, Firefox, Safari, Edge
- [ ] Works on tablets in **landscape mode** (iOS Safari, Chrome Android)
- [ ] **All text is in Polish** - no English visible
- [ ] Polish characters render correctly
- [ ] `lang="pl"` set on HTML tag
- [ ] Layout optimized for landscape (horizontal orientation)
- [ ] Shows rotation hint in portrait mode
- [ ] No build step required
- [ ] No console errors or warnings
- [ ] Smooth performance (60fps)
- [ ] Touch targets meet minimum size (60px × 60px)
- [ ] Includes appropriate comments
- [ ] Cleanup code (destroy method) implemented
- [ ] Tested with actual tablet device in landscape orientation

---

## 💡 Quick Reference

**Load new game:**
```javascript
GameEngine.loadGame('BalloonPopGame');
```

**Play sound:**
```javascript
playSound('pop');
```

**Speak in Polish:**
```javascript
speak("Brawo!"); // Uses Polish voice (pl-PL)
```

**Show Polish praise:**
```javascript
const randomPraise = POLISH.praise[Math.floor(Math.random() * POLISH.praise.length)];
displayMessage(randomPraise);
```

**Create animation:**
```javascript
element.style.animation = 'pop 0.4s ease-out forwards';
```

**Handle touch:**
```javascript
element.addEventListener('click', handleClick); // Works for both mouse and touch
```

**Random color:**
```javascript
const colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3', '#C7A7FF'];
const randomColor = colors[Math.floor(Math.random() * colors.length)];
```

**Set Polish text:**
```javascript
button.textContent = POLISH.games.balloonPop; // "Baloniki"
title.textContent = POLISH.title; // "Gry dla Maluchów"
```

**Detect orientation:**
```javascript
const isLandscape = window.innerWidth > window.innerHeight;
if (!isLandscape) {
    showRotationHint(POLISH.rotateDevice); // "Obróć tablet poziomo 🔄"
}
```

---

**Remember**:
- 🇵🇱 Always use Polish language
- 📱 Always design for landscape orientation
- 🎮 Keep it simple, keep it fun, keep it working without any build tools!
