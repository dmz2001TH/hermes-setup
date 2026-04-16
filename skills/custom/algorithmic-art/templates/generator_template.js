/**
 * P5.JS GENERATIVE ART - BEST PRACTICES
 * 
 * Structure and principles for p5.js generative art.
 * Your algorithmic philosophy should guide what you build.
 */

// 1. PARAMETERS - Keep all tunable params in one object
let params = {
    seed: 12345,
    // Add your parameters based on your algorithm
    // e.g. particleCount, speed, noiseScale, colorPalette, etc.
};

// 2. SEEDED RANDOMNESS (Critical for reproducibility)
function initializeSeed(seed) {
    randomSeed(seed);
    noiseSeed(seed);
}

// 3. P5.JS LIFECYCLE
function setup() {
    createCanvas(800, 800);
    initializeSeed(params.seed);
    // Initialize your generative system
    // For static art: call noLoop() at the end of setup
}

function draw() {
    // Your algorithm here
}

// 4. UTILITY FUNCTIONS
function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? { r: parseInt(result[1], 16), g: parseInt(result[2], 16), b: parseInt(result[3], 16) } : null;
}

function easeInOutCubic(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

function vectorFromAngle(angle, magnitude = 1) {
    return createVector(cos(angle), sin(angle)).mult(magnitude);
}

// 5. PARAMETER UPDATES
function updateParameter(paramName, value) {
    params[paramName] = value;
}

function regenerate() {
    initializeSeed(params.seed);
    // Reinitialize your system
}

function exportImage() {
    saveCanvas('generative-art-' + params.seed, 'png');
}
