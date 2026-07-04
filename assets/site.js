/* ════════════════════════════════════════════════════════════
   LLMotions — Advanced 3D Interactive Runtime
   Three.js morphing particles + GSAP scroll animations
   ════════════════════════════════════════════════════════════ */

/* ── 1. THREE.JS ADVANCED 3D BACKGROUND ── */
(function () {
    const canvas = document.getElementById("bg");
    if (!canvas || typeof THREE === "undefined") return;

    const renderer = new THREE.WebGLRenderer({
        canvas,
        antialias: true,
        alpha: true,
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(window.innerWidth, window.innerHeight);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );
    camera.position.z = 35;

    // Particle system with morphing geometry
    const particleCount = 3000;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    const sizes = new Float32Array(particleCount);

    for (let i = 0; i < particleCount; i++) {
        // Distribute in a sphere
        const radius = 40 + Math.random() * 30;
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(Math.random() * 2 - 1);
        
        positions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
        positions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
        positions[i * 3 + 2] = radius * Math.cos(phi);

        // Color gradient violet to cyan
        const t = Math.random();
        colors[i * 3] = 0.545 * (1 - t) + 0.024 * t;     // R
        colors[i * 3 + 1] = 0.361 * (1 - t) + 0.714 * t; // G
        colors[i * 3 + 2] = 0.965 * (1 - t) + 0.831 * t; // B

        sizes[i] = Math.random() * 2 + 0.5;
    }

    geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));
    geometry.setAttribute("size", new THREE.BufferAttribute(sizes, 1));

    const particleMaterial = new THREE.PointsMaterial({
        size: 0.15,
        vertexColors: true,
        transparent: true,
        opacity: 0.8,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
    });

    const particles = new THREE.Points(geometry, particleMaterial);
    scene.add(particles);

    // Add morphing torus knot — kept very subtle so it never fights content
    const torusGeometry = new THREE.TorusKnotGeometry(14, 0.22, 220, 24, 3, 7);
    const torusMaterial = new THREE.MeshBasicMaterial({
        color: 0x8b5cf6,
        wireframe: true,
        transparent: true,
        opacity: 0.025,
    });
    const torus = new THREE.Mesh(torusGeometry, torusMaterial);
    torus.position.z = -18;
    scene.add(torus);

    // Add floating icosahedrons
    const icosahedrons = [];
    for (let i = 0; i < 5; i++) {
        const icoGeometry = new THREE.IcosahedronGeometry(2, 0);
        const icoMaterial = new THREE.MeshBasicMaterial({
            color: i % 2 === 0 ? 0x8b5cf6 : 0x06b6d4,
            wireframe: true,
            transparent: true,
            opacity: 0.1,
        });
        const ico = new THREE.Mesh(icoGeometry, icoMaterial);
        ico.position.set(
            (Math.random() - 0.5) * 50,
            (Math.random() - 0.5) * 50,
            (Math.random() - 0.5) * 50
        );
        scene.add(ico);
        icosahedrons.push(ico);
    }

    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    window.addEventListener("mousemove", (e) => {
        mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
        mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
    });

    let scrollY = 0;
    window.addEventListener("scroll", () => {
        scrollY = window.pageYOffset;
    }, { passive: true });

    function animate() {
        requestAnimationFrame(animate);

        const time = Date.now() * 0.0003;

        // Smooth camera follow
        targetX += (mouseX * 3 - targetX) * 0.02;
        targetY += (-mouseY * 3 - targetY) * 0.02;

        camera.position.x = targetX;
        camera.position.y = targetY;
        camera.lookAt(scene.position);

        // Rotate particles
        particles.rotation.y = time * 0.3;
        particles.rotation.x = Math.sin(time * 0.5) * 0.2;

        // Animate torus
        torus.rotation.x = time * 0.7;
        torus.rotation.y = time * 0.5;
        torus.position.y = Math.sin(time * 2) * 2;

        // Animate icosahedrons
        icosahedrons.forEach((ico, i) => {
            ico.rotation.x = time * (0.5 + i * 0.1);
            ico.rotation.y = time * (0.3 + i * 0.1);
            ico.position.y += Math.sin(time * 2 + i) * 0.02;
        });

        // Morph particles based on scroll
        const positions = particles.geometry.attributes.position.array;
        for (let i = 0; i < particleCount; i++) {
            const i3 = i * 3;
            const x = positions[i3];
            const y = positions[i3 + 1];
            const z = positions[i3 + 2];

            positions[i3 + 1] = y + Math.sin(time * 3 + x * 0.1) * 0.02;
        }
        particles.geometry.attributes.position.needsUpdate = true;

        renderer.render(scene, camera);
    }

    animate();

    window.addEventListener("resize", () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
})();

/* ── 2. DOM PARTICLES ── */
(function () {
    const container = document.getElementById("particles");
    if (!container) return;

    for (let i = 0; i < 30; i++) {
        const particle = document.createElement("div");
        particle.className = "p";
        
        const isViolet = Math.random() > 0.5;
        const size = 1 + Math.random() * 3;
        const duration = 12 + Math.random() * 18;
        const delay = Math.random() * 15;
        
        particle.style.cssText = `
            left: ${Math.random() * 100}%;
            width: ${size}px;
            height: ${size}px;
            animation-duration: ${duration}s;
            animation-delay: ${delay}s;
            background: rgba(${isViolet ? "139,92,246" : "6,182,212"}, ${0.6 + Math.random() * 0.4});
            box-shadow: 0 0 ${8 + Math.random() * 12}px rgba(${isViolet ? "139,92,246" : "6,182,212"}, 0.8);
        `;
        
        container.appendChild(particle);
    }
})();

/* ── 3. CURSOR GLOW TRACKING ── */
(function () {
    const cursor = document.getElementById("cursor");
    if (!cursor) return;

    let cursorX = 0;
    let cursorY = 0;
    let currentX = 0;
    let currentY = 0;

    window.addEventListener("mousemove", (e) => {
        cursorX = e.clientX;
        cursorY = e.clientY;
    });

    function animateCursor() {
        currentX += (cursorX - currentX) * 0.1;
        currentY += (cursorY - currentY) * 0.1;

        cursor.style.left = currentX + "px";
        cursor.style.top = currentY + "px";

        requestAnimationFrame(animateCursor);
    }

    animateCursor();
})();

/* ── 4. LOADER & PAGE INITIALIZATION ── */
window.addEventListener("load", () => {
    setTimeout(() => {
        const loader = document.getElementById("loader");
        if (loader) {
            loader.classList.add("out");
        }
        initScrollAnimations();
        initHeroAnimation();
    }, 1200);
});

/* ── 5. HERO TEXT ANIMATION ── */
function initHeroAnimation() {
    const words = document.querySelectorAll(".hero h1 .word");
    const heroPara = document.querySelector(".hero p");
    const heroBtns = document.querySelector(".hero-btns");
    const scrollHint = document.querySelector(".scroll-hint");
    const badge = document.querySelector(".hero .badge");

    if (typeof gsap !== "undefined" && words.length > 0) {
        gsap.to(badge, {
            opacity: 1,
            y: 0,
            duration: 0.8,
            delay: 0.3,
            ease: "power3.out"
        });

        words.forEach((word, i) => {
            gsap.to(word, {
                opacity: 1,
                y: 0,
                rotateX: 0,
                duration: 1,
                delay: 0.5 + i * 0.15,
                ease: "power4.out",
            });
        });

        gsap.to(heroPara, {
            opacity: 1,
            y: 0,
            duration: 1,
            delay: 1.5,
            ease: "power3.out",
        });

        gsap.to(heroBtns, {
            opacity: 1,
            y: 0,
            duration: 1,
            delay: 1.8,
            ease: "power3.out",
        });

        gsap.to(scrollHint, {
            opacity: 0.6,
            duration: 1,
            delay: 2.2,
            ease: "power2.out",
        });
    } else {
        // Fallback without GSAP
        words.forEach(w => w.style.opacity = 1);
        if (heroPara) heroPara.style.opacity = 1;
        if (heroBtns) heroBtns.style.opacity = 1;
        if (scrollHint) scrollHint.style.opacity = 0.6;
    }
}

/* ── 6. SCROLL ANIMATIONS ── */
function initScrollAnimations() {
    const nav = document.getElementById("nav");
    
    // Compact nav on scroll
    if (nav) {
        window.addEventListener("scroll", () => {
            nav.classList.toggle("compact", window.scrollY > 80);
        }, { passive: true });
    }

    if (typeof gsap === "undefined" || typeof ScrollTrigger === "undefined") {
        // Fallback: just show all elements
        document.querySelectorAll(".reveal").forEach(el => {
            el.style.opacity = 1;
            el.style.transform = "none";
        });
        return;
    }

    gsap.registerPlugin(ScrollTrigger);

    // Animate all reveal elements
    document.querySelectorAll(".reveal").forEach((el, index) => {
        gsap.to(el, {
            scrollTrigger: {
                trigger: el,
                start: "top 85%",
                toggleActions: "play none none reverse",
            },
            opacity: 1,
            y: 0,
            scale: 1,
            rotateX: 0,
            duration: 1,
            delay: (index % 6) * 0.1,
            ease: "power3.out",
        });
    });

    // Parallax effect on sections
    gsap.utils.toArray("section").forEach((section) => {
        gsap.to(section, {
            scrollTrigger: {
                trigger: section,
                start: "top bottom",
                end: "bottom top",
                scrub: 1,
            },
            y: -50,
            ease: "none",
        });
    });
}

/* ── 7. ENHANCED INTERACTIONS ── */
document.addEventListener("DOMContentLoaded", () => {
    // Add magnetic effect to buttons
    const buttons = document.querySelectorAll(".btn-p, .btn-s, .nav-btn");
    
    buttons.forEach(btn => {
        btn.addEventListener("mouseenter", function() {
            this.style.transform = "translateY(-3px) scale(1.05)";
        });
        
        btn.addEventListener("mouseleave", function() {
            this.style.transform = "";
        });
        
        btn.addEventListener("mousemove", function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            this.style.transform = `translateY(-3px) scale(1.05) translate(${x * 0.1}px, ${y * 0.1}px)`;
        });
    });

    // Add tilt effect to cards
    const cards = document.querySelectorAll(".fcard, .product-orb, .step-card");
    
    cards.forEach(card => {
        card.addEventListener("mousemove", function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;
            
            this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
        });
        
        card.addEventListener("mouseleave", function() {
            this.style.transform = "";
        });
    });

    // IMAGE MODAL/LIGHTBOX
    const modalHTML = `
        <div class="modal-overlay" id="imageModal">
            <div class="modal-content">
                <button class="modal-close">✕</button>
                <img src="" alt="" id="modalImage">
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const closeBtn = modal.querySelector('.modal-close');

    // Add click handlers to all screenshot images
    document.querySelectorAll('.shot img, .gallery img').forEach(img => {
        img.addEventListener('click', function(e) {
            e.preventDefault();
            modalImg.src = this.src;
            modalImg.alt = this.alt;
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    });

    // Close modal handlers
    const closeModal = () => {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    };

    closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });

    // ESC key to close
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
});
