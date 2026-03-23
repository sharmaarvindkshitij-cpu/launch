// ==========================================
// Particle Network Background
// ==========================================
const canvas = document.getElementById('particleCanvas');
const ctx = canvas.getContext('2d');
let particles = [];
let animationFrameId;

function initParticles() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    // Number of particles depends on screen size (prevent lag on mobile)
    const particleCount = Math.min(Math.floor((window.innerWidth * window.innerHeight) / 10000), 100); 
    particles = [];

    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.8,
            vy: (Math.random() - 0.5) * 0.8,
            radius: Math.random() * 2 + 0.5
        });
    }
}

function drawParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Update and draw particles
    for (let i = 0; i < particles.length; i++) {
        let p = particles[i];
        p.x += p.vx;
        p.y += p.vy;

        // Bounce off edges
        if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(0, 240, 255, 0.8)';
        ctx.fill();

        // Connect particles
        for (let j = i + 1; j < particles.length; j++) {
            let p2 = particles[j];
            let dx = p.x - p2.x;
            let dy = p.y - p2.y;
            let dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < 120) {
                ctx.beginPath();
                ctx.strokeStyle = `rgba(176, 38, 255, ${1 - dist / 120})`;
                ctx.lineWidth = 0.5;
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.stroke();
            }
        }
    }
    
    animationFrameId = requestAnimationFrame(drawParticles);
}

// Initial Canvas Setup
initParticles();
drawParticles();

window.addEventListener('resize', () => {
    initParticles();
});

// ==========================================
// Launch Interaction
// ==========================================
const launchBtn = document.getElementById('launchBtn');
const uiContainer = document.getElementById('uiContainer');
const sequenceText = document.getElementById('sequenceText');
const flashOverlay = document.getElementById('flashOverlay');
const progressBarContainer = document.getElementById('progressBarContainer');
const progressBar = document.getElementById('progressBar');

function createRipple(x, y) {
    const ripple = document.createElement('div');
    ripple.className = 'ripple';
    ripple.style.left = `${x}px`;
    ripple.style.top = `${y}px`;
    document.body.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 1200); // match new ripple CSS time
}

// Define Launch Sequence Messages
const messages = [
    "Initializing Launch…",
    "Connecting to Innovation Network…",
    "Startup Club Activated 🚀",
    "Successfully Launched ✅"
];

// Launch Flow
let launchTriggered = false;

function triggerLaunch(x, y) {
    if (launchTriggered) return;
    launchTriggered = true;
    
    createRipple(x, y);

    // Disable interactions
    launchBtn.disabled = true;
    
    // Change button text and add charge animation
    const btnText = launchBtn.querySelector('.btn-text');
    if (btnText) btnText.textContent = "LAUNCHING...";
    launchBtn.classList.add('charging');
    
    // Speed up particles enormously for dramatic rapid effect
    particles.forEach(p => {
        p.vx *= 5;
        p.vy *= 5;
    });

    // Wait 800ms for button charge animation, then fade it out
    setTimeout(() => {
        uiContainer.classList.add('hidden');
        
        // Wait 500ms for UI to hide, then start the sequence
        setTimeout(startSequence, 500);
    }, 800); 
}

// Listeners
launchBtn.addEventListener('click', (e) => {
    triggerLaunch(e.clientX, e.clientY);
});

// SPACEBAR trigger exclusively
window.addEventListener('keydown', (e) => {
    if (!launchTriggered && e.code === 'Space') {
        // Prevent default spacebar scroll
        e.preventDefault();
        // Trigger from center of screen on keydown
        triggerLaunch(window.innerWidth / 2, window.innerHeight / 2);
    }
});

function startSequence() {
    let index = 0;
    progressBarContainer.classList.add('active');
    
    // Adjusted durations for better cinematic pacing
    const stepDurations = [700, 700, 800, 800]; 
    
    function showNextMessage() {
        if (index >= messages.length) return; // Done
        
        // Update Text
        sequenceText.textContent = messages[index];
        if (index === messages.length - 1) {
            sequenceText.classList.add('success');
        }
        
        // Update Progress Bar
        const progressPercentage = ((index + 1) / messages.length) * 100;
        progressBar.style.width = `${progressPercentage}%`;
        
        // Fade in
        sequenceText.classList.remove('exit');
        sequenceText.classList.add('active');
        
        const currentDuration = stepDurations[index];

        // Handle next step
        if (index === messages.length - 1) {
            // End of sequence, trigger final effect immediately after currentDuration passes
            setTimeout(() => {
                triggerFinalEffect();
            }, currentDuration);
            
        } else {
            // Show for currentDuration - 200ms fadeOut, then wait 200ms
            setTimeout(() => {
                sequenceText.classList.remove('active');
                sequenceText.classList.add('exit');
                
                // Advance
                index++;
                setTimeout(showNextMessage, 200); 
            }, currentDuration - 200); 
        }
    }
    
    showNextMessage();
}

function triggerFinalEffect() {
    // Particle burst: spawn from center
    const cx = canvas.width / 2;
    const cy = canvas.height / 2;
    particles = []; // Clear existing to prevent clutter
    for(let i=0; i<300; i++) {
        let angle = Math.random() * Math.PI * 2;
        let speed = Math.random() * 25 + 5;
        particles.push({
            x: cx,
            y: cy,
            vx: Math.cos(angle) * speed,
            vy: Math.sin(angle) * speed,
            radius: Math.random() * 3 + 1
        });
    }

    // Flash screen
    flashOverlay.classList.add('active');
    
    // Redirect 1.5 seconds after final effect triggers
    setTimeout(() => {
        window.location.href = 'https://startupclubcu.online';
    }, 1500);
}
