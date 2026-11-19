const width = 800;
const height = 600;

class Particle {
    constructor(x, y, type) {
        this.x = x;
        this.y = y;
        this.type = type;
        this.life = 0;
        this.maxLife = 100;
    }
}

const floatParticles = [];
const burstParticles = [];

const FLOAT_COUNT = 140;

for (let i = 0; i < FLOAT_COUNT; i++) {
    const p = new Particle(
        Math.random() * width,
        Math.random() * height,
        "float"
    );

    p.life = Math.random() * p.maxLife;
    floatParticles.push(p);
}

function spawnHeartBurst(x, y) {
    const count = 140;

    for (let i = 0; i < count; i++) {
        burstParticles.push(new Particle(x, y, "burst"));
    }
}

const BLUE_SHADES = [
    "#3b82f6",
    "#60a5fa",
    "#93c5fd",
    "#2563eb",
    "#bfdbfe",
    "#1d4ed8"
];

console.log("Particles created:", floatParticles.length);
console.log("Blue shades:", BLUE_SHADES);
