// Common JavaScript utilities for Toddler Games
// Polish language support and shared functions

// Polish text constants
const POLISH_TEXT = {
  // General UI
  home: 'Dom',
  sound: 'Dźwięk',
  soundOn: '🔊 Dźwięk',
  soundOff: '🔇 Cisza',

  // Celebrations
  celebrations: [
    'Brawo!',
    'Super!',
    'Wspaniale!',
    'Świetnie!',
    'Doskonale!',
    'Cudownie!',
    'Fantastycznie!'
  ],

  // Colors
  colors: {
    red: 'Czerwony',
    blue: 'Niebieski',
    yellow: 'Żółty',
    green: 'Zielony',
    purple: 'Fioletowy',
    orange: 'Pomarańczowy',
    pink: 'Różowy'
  },

  // Animals
  animals: {
    bunny: 'Królik',
    puppy: 'Piesek',
    kitten: 'Kotek',
    bear: 'Miś',
    elephant: 'Słoń',
    monkey: 'Małpka'
  },

  // Shapes
  shapes: {
    circle: 'Koło',
    square: 'Kwadrat',
    triangle: 'Trójkąt',
    star: 'Gwiazdka',
    heart: 'Serce'
  },

  // Actions
  clear: 'Wyczyść',
  reset: 'Od nowa',
  tryAgain: 'Spróbuj jeszcze raz',
  chooseColor: 'Wybierz kolor',
  feedAnimal: 'Nakarm zwierzątko'
};

// Sound management
class SoundManager {
  constructor() {
    this.audioContext = null;
    this.enabled = true;
    this.initAudioContext();

    // Load sound state from localStorage
    const savedState = localStorage.getItem('soundEnabled');
    if (savedState !== null) {
      this.enabled = savedState === 'true';
    }
  }

  initAudioContext() {
    try {
      this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    } catch (e) {
      console.warn('Web Audio API not supported', e);
    }
  }

  toggle() {
    this.enabled = !this.enabled;
    localStorage.setItem('soundEnabled', this.enabled);
    return this.enabled;
  }

  isEnabled() {
    return this.enabled;
  }

  // Play a pop sound
  playPop() {
    if (!this.enabled || !this.audioContext) return;

    const oscillator = this.audioContext.createOscillator();
    const gainNode = this.audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(this.audioContext.destination);

    oscillator.frequency.setValueAtTime(800, this.audioContext.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(100, this.audioContext.currentTime + 0.1);

    gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.1);

    oscillator.start(this.audioContext.currentTime);
    oscillator.stop(this.audioContext.currentTime + 0.1);
  }

  // Play a celebration sound
  playCelebration() {
    if (!this.enabled || !this.audioContext) return;

    const notes = [523.25, 659.25, 783.99, 1046.50]; // C, E, G, C
    notes.forEach((freq, i) => {
      const oscillator = this.audioContext.createOscillator();
      const gainNode = this.audioContext.createGain();

      oscillator.connect(gainNode);
      gainNode.connect(this.audioContext.destination);

      oscillator.frequency.setValueAtTime(freq, this.audioContext.currentTime + i * 0.1);
      gainNode.gain.setValueAtTime(0.2, this.audioContext.currentTime + i * 0.1);
      gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + i * 0.1 + 0.3);

      oscillator.start(this.audioContext.currentTime + i * 0.1);
      oscillator.stop(this.audioContext.currentTime + i * 0.1 + 0.3);
    });
  }

  // Play a musical note
  playNote(frequency, duration = 0.2) {
    if (!this.enabled || !this.audioContext) return;

    const oscillator = this.audioContext.createOscillator();
    const gainNode = this.audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(this.audioContext.destination);

    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(frequency, this.audioContext.currentTime);

    gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + duration);

    oscillator.start(this.audioContext.currentTime);
    oscillator.stop(this.audioContext.currentTime + duration);
  }

  // Play a success sound
  playSuccess() {
    if (!this.enabled || !this.audioContext) return;

    const oscillator = this.audioContext.createOscillator();
    const gainNode = this.audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(this.audioContext.destination);

    oscillator.frequency.setValueAtTime(400, this.audioContext.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(800, this.audioContext.currentTime + 0.2);

    gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.2);

    oscillator.start(this.audioContext.currentTime);
    oscillator.stop(this.audioContext.currentTime + 0.2);
  }

  // Play a whoosh sound
  playWhoosh() {
    if (!this.enabled || !this.audioContext) return;

    const oscillator = this.audioContext.createOscillator();
    const gainNode = this.audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(this.audioContext.destination);

    oscillator.type = 'sawtooth';
    oscillator.frequency.setValueAtTime(200, this.audioContext.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(50, this.audioContext.currentTime + 0.15);

    gainNode.gain.setValueAtTime(0.2, this.audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.15);

    oscillator.start(this.audioContext.currentTime);
    oscillator.stop(this.audioContext.currentTime + 0.15);
  }
}

// Create global sound manager instance
const soundManager = new SoundManager();

// Utility functions
const Utils = {
  // Get random item from array
  randomItem(array) {
    return array[Math.floor(Math.random() * array.length)];
  },

  // Get random celebration text
  getCelebration() {
    return Utils.randomItem(POLISH_TEXT.celebrations);
  },

  // Show celebration message
  showCelebration(text = null) {
    const msg = document.createElement('div');
    msg.className = 'celebration-msg';
    msg.textContent = text || Utils.getCelebration();
    document.body.appendChild(msg);

    soundManager.playCelebration();

    setTimeout(() => {
      msg.remove();
    }, 1000);
  },

  // Create particle effect
  createParticles(x, y, color, count = 10) {
    for (let i = 0; i < count; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.left = x + 'px';
      particle.style.top = y + 'px';
      particle.style.background = color;

      const angle = (Math.PI * 2 * i) / count;
      const velocity = 50 + Math.random() * 100;
      const tx = Math.cos(angle) * velocity;
      const ty = Math.sin(angle) * velocity;

      particle.style.setProperty('--tx', tx + 'px');
      particle.style.setProperty('--ty', ty + 'px');

      document.body.appendChild(particle);

      setTimeout(() => particle.remove(), 600);
    }
  },

  // Random number in range
  random(min, max) {
    return Math.random() * (max - min) + min;
  },

  // Random integer in range
  randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  },

  // Vibrate device if supported
  vibrate(duration = 50) {
    if ('vibrate' in navigator) {
      navigator.vibrate(duration);
    }
  }
};

// Setup sound toggle button
function setupSoundToggle() {
  const soundToggle = document.querySelector('.sound-toggle');
  if (!soundToggle) return;

  // Set initial state
  updateSoundButton(soundToggle);

  soundToggle.addEventListener('click', () => {
    soundManager.toggle();
    updateSoundButton(soundToggle);
    soundManager.playPop();
  });
}

function updateSoundButton(button) {
  button.textContent = soundManager.isEnabled() ? POLISH_TEXT.soundOn : POLISH_TEXT.soundOff;
}

// Resume audio context on user interaction (required by browsers)
function resumeAudioContext() {
  if (soundManager.audioContext && soundManager.audioContext.state === 'suspended') {
    soundManager.audioContext.resume();
  }
}

// Add event listeners to resume audio context
document.addEventListener('click', resumeAudioContext, { once: true });
document.addEventListener('touchstart', resumeAudioContext, { once: true });

// Initialize on DOM load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', setupSoundToggle);
} else {
  setupSoundToggle();
}

// Export for use in games
window.POLISH_TEXT = POLISH_TEXT;
window.soundManager = soundManager;
window.Utils = Utils;
