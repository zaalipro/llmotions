/* ════════════════════════════════════════════════════════════
   LLMotions — shared runtime for product detail pages
   Three.js particle field + DOM particles + cursor glow + loader
   + GSAP scroll reveals. Degrades gracefully if libs are absent.
   ════════════════════════════════════════════════════════════ */

/* ── 1. THREE.JS BACKGROUND ── */
(function () {
    const canvas = document.getElementById("bg");
    if (!canvas || typeof THREE === "undefined") return;

    const renderer = new THREE.WebGLRenderer({
        canvas,
        antialias: true,
        alpha: true,
    });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.setSize(innerWidth, innerHeight);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
        70,
        innerWidth / innerHeight,
        0.1,
        1000,
    );
    camera.position.z = 28;

    const N = 2400;
    const geo = new THREE.BufferGeometry();
    const pos = new Float32Array(N * 3);
    const col = new Float32Array(N * 3);
    for (let i = 0; i < N; i++) {
        pos[i * 3] = (Math.random() - 0.5) * 75;
        pos[i * 3 + 1] = (Math.random() - 0.5) * 75;
        pos[i * 3 + 2] = (Math.random() - 0.5) * 75;
        const t = Math.random();
        col[i * 3] = 0.486 * (1 - t);
        col[i * 3 + 1] = 0.227 * (1 - t) + 0.714 * t;
        col[i * 3 + 2] = 0.929 * (1 - t) + 0.831 * t;
    }
    geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    geo.setAttribute("color", new THREE.BufferAttribute(col, 3));
    const pts = new THREE.Points(
        geo,
        new THREE.PointsMaterial({
            size: 0.11,
            vertexColors: true,
            transparent: true,
            opacity: 0.7,
            blending: THREE.AdditiveBlending,
            depthWrite: false,
        }),
    );
    scene.add(pts);

    const tk = new THREE.Mesh(
        new THREE.TorusKnotGeometry(7, 0.25, 180, 28, 3, 5),
        new THREE.MeshBasicMaterial({
            color: 0x7c3aed,
            wireframe: true,
            transparent: true,
            opacity: 0.05,
        }),
    );
    scene.add(tk);

    let mx = 0,
        my = 0;
    addEventListener("mousemove", (e) => {
        mx = (e.clientX / innerWidth - 0.5) * 2;
        my = (e.clientY / innerHeight - 0.5) * 2;
    });

    (function tick() {
        requestAnimationFrame(tick);
        const t = Date.now() * 0.00028;
        pts.rotation.y = t * 0.28;
        pts.rotation.x = t * 0.13;
        tk.rotation.x = t * 0.7;
        tk.rotation.y = t * 0.45;
        camera.position.x += (mx * 2.5 - camera.position.x) * 0.02;
        camera.position.y += (-my * 2.5 - camera.position.y) * 0.02;
        camera.lookAt(scene.position);
        renderer.render(scene, camera);
    })();

    addEventListener("resize", () => {
        camera.aspect = innerWidth / innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(innerWidth, innerHeight);
    });
})();

/* ── 2. DOM PARTICLES ── */
(function () {
    const c = document.getElementById("particles");
    if (!c) return;
    for (let i = 0; i < 24; i++) {
        const el = document.createElement("div");
        el.className = "p";
        const violet = Math.random() > 0.5;
        el.style.cssText = `
      left:${Math.random() * 100}%;
      width:${1 + Math.random() * 2}px;
      height:${1 + Math.random() * 2}px;
      animation-duration:${9 + Math.random() * 15}s;
      animation-delay:${Math.random() * 10}s;
      background:rgba(${violet ? "124,58,237" : "6,182,212"},${0.5 + Math.random() * 0.5});
      box-shadow:0 0 ${4 + Math.random() * 6}px rgba(${violet ? "124,58,237" : "6,182,212"},.8);
    `;
        c.appendChild(el);
    }
})();

/* ── 3. CURSOR GLOW ── */
(function () {
    const cur = document.getElementById("cursor");
    if (!cur) return;
    addEventListener("mousemove", (e) => {
        cur.style.left = e.clientX + "px";
        cur.style.top = e.clientY + "px";
    });
})();

/* ── 4. LOADER + REVEALS ── */
addEventListener("load", () => {
    setTimeout(() => {
        const l = document.getElementById("loader");
        if (l) l.classList.add("out");
        initReveals();
    }, 900);
});

function initReveals() {
    // Nav compact on scroll
    const nav = document.getElementById("nav");
    if (nav) {
        addEventListener(
            "scroll",
            () => nav.classList.toggle("compact", scrollY > 60),
            { passive: true },
        );
    }

    if (typeof gsap === "undefined") {
        // No GSAP — just show everything.
        document
            .querySelectorAll(".reveal")
            .forEach((el) => (el.style.opacity = 1));
        return;
    }

    gsap.registerPlugin(ScrollTrigger);
    document.querySelectorAll(".reveal").forEach((el, i) => {
        gsap.to(el, {
            scrollTrigger: {
                trigger: el,
                start: "top 88%",
                toggleActions: "play none none reverse",
            },
            opacity: 1,
            y: 0,
            duration: 0.8,
            delay: (i % 3) * 0.08,
            ease: "power3.out",
        });
    });
}
