# Claude Coding Agent Instructions

This document provides guidelines for AI coding agents working on the Toddler Games project.

## 🎯 Project Context

This is a **zero-build, browser-only JavaScript project** designed for toddlers (ages 2-4). The entire application must run directly from GitHub Pages without any build step, bundlers, or package managers.

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
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Toddler Games</title>
    <style>
        /* Inline CSS here or link to styles.css */
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

### CSS Guidelines
- Use **CSS Grid** and **Flexbox** for layouts
- Use **CSS Custom Properties** for colors/sizes (easy theming)
- Use **CSS Transforms** for animations (better performance)
- Avoid float-based layouts
- Mobile-first approach with media queries
- Minimum touch target: **60px × 60px**

Example:
```css
:root {
    --primary-color: #FF6B6B;
    --secondary-color: #4ECDC4;
    --touch-target-min: 60px;
    --border-radius: 15px;
}

.game-button {
    min-width: var(--touch-target-min);
    min-height: var(--touch-target-min);
    font-size: 24px;
    border-radius: var(--border-radius);
    cursor: pointer;
    touch-action: manipulation; /* Prevents double-tap zoom */
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

### Responsive Design
```css
/* Mobile first */
.game-container {
    padding: var(--spacing-md);
}

/* Tablet and up */
@media (min-width: 768px) {
    .game-container {
        padding: var(--spacing-lg);
        max-width: 1200px;
        margin: 0 auto;
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

- [ ] Works on mobile (touch events)
- [ ] Works on desktop (mouse events)
- [ ] No console errors
- [ ] Smooth 60fps animation
- [ ] Touch targets are 60px+ minimum
- [ ] Loads without internet (after first load)
- [ ] Works in GitHub Pages environment
- [ ] No build step required
- [ ] All assets are self-contained or in repo

## 🚫 Common Pitfalls to Avoid

1. **Don't use import/export** - Not supported without build tools
   ```javascript
   // ❌ Don't do this
   import { Game } from './game.js';

   // ✅ Do this instead
   const Game = window.Game || {};
   ```

2. **Don't rely on npm packages** - Everything must be self-contained

3. **Don't use template literals in HTML** - Use DOM manipulation or innerHTML

4. **Don't forget mobile testing** - Desktop testing isn't enough

5. **Don't use small touch targets** - Minimum 60px

6. **Don't forget to clean up** - Remove event listeners, cancel animations in destroy()

7. **Don't use relative paths incorrectly** - GitHub Pages serves from a subdirectory
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
- [ ] Works on mobile (iOS Safari, Chrome Android)
- [ ] No build step required
- [ ] No console errors or warnings
- [ ] Smooth performance (60fps)
- [ ] Touch targets meet minimum size
- [ ] Includes appropriate comments
- [ ] Cleanup code (destroy method) implemented
- [ ] Tested with actual device/touch screen

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

---

**Remember**: Keep it simple, keep it fun, keep it working without any build tools! 🎮
