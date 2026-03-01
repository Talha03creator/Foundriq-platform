// FoundrIQ – Cinematic Animations & Interaction Engine
document.addEventListener('DOMContentLoaded', () => {

    // ── Navbar scroll effect ──────────────────
    const navbar = document.getElementById('navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            navbar.classList.toggle('scrolled', window.scrollY > 20);
        }, { passive: true });
    }

    // ── Mobile nav toggle ─────────────────────
    const mobileToggle = document.getElementById('mobileToggle');
    const navLinks = document.getElementById('navLinks');
    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', () => {
            mobileToggle.classList.toggle('active');
            navLinks.classList.toggle('active');
        });
    }

    // ── Scroll Reveal (IntersectionObserver) ──
    const revealEls = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');
    if (revealEls.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    // Stagger based on sibling index
                    const parent = entry.target.parentElement;
                    const siblings = parent ? Array.from(parent.querySelectorAll('.reveal, .reveal-left, .reveal-right')) : [];
                    const idx = siblings.indexOf(entry.target);
                    const delay = idx >= 0 ? idx * 100 : 0;
                    setTimeout(() => {
                        entry.target.classList.add('visible');
                    }, delay);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -50px 0px' });

        revealEls.forEach(el => observer.observe(el));
    }

    // ── Counter Animation ─────────────────────
    const counters = document.querySelectorAll('.counter');
    if (counters.length > 0) {
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        counters.forEach(el => counterObserver.observe(el));
    }

    function animateCounter(el) {
        const target = parseInt(el.getAttribute('data-target'));
        const duration = 2000;
        const startTime = performance.now();

        function easeOutExpo(t) { return t === 1 ? 1 : 1 - Math.pow(2, -10 * t); }

        function update(now) {
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const current = Math.round(easeOutExpo(progress) * target);
            el.textContent = current.toLocaleString();
            if (progress < 1) requestAnimationFrame(update);
        }
        requestAnimationFrame(update);
    }

    // ─────────────────────────────────────────────────
    //  CINEMATIC 3D TILT EFFECT
    //  Cards tilt toward the cursor with perspective,
    //  glow follows cursor position, smooth spring return
    // ─────────────────────────────────────────────────
    const tiltTargets = '.tilt-card, .feature-card, .testimonial-card, .ps-card, .stat-card, .chart-card, .swot-card, .pricing-card';
    const tiltEls = document.querySelectorAll(tiltTargets);
    const isMobile = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

    if (!isMobile) {
        tiltEls.forEach(card => {
            // Inject glow spot element
            const glowSpot = document.createElement('div');
            glowSpot.className = 'glow-spot';
            glowSpot.style.cssText = `
                position:absolute; width:300px; height:300px; border-radius:50%;
                background:radial-gradient(circle, rgba(var(--accent-primary-rgb),0.12) 0%, transparent 70%);
                pointer-events:none; opacity:0; transform:translate(-50%,-50%);
                transition:opacity 0.4s ease; z-index:0;
            `;
            card.style.position = card.style.position || 'relative';
            card.style.overflow = 'hidden';
            card.appendChild(glowSpot);

            let animFrame = null;

            card.addEventListener('mousemove', (e) => {
                if (animFrame) cancelAnimationFrame(animFrame);
                animFrame = requestAnimationFrame(() => {
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;
                    const percentX = (x - centerX) / centerX;
                    const percentY = (y - centerY) / centerY;

                    // Tilt: max ±6 degrees
                    const rotateX = percentY * -6;
                    const rotateY = percentX * 6;

                    card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02) translateY(-4px)`;

                    // Position the glow cursor-follow
                    glowSpot.style.left = x + 'px';
                    glowSpot.style.top = y + 'px';
                    glowSpot.style.opacity = '1';
                });
            });

            card.addEventListener('mouseleave', () => {
                if (animFrame) cancelAnimationFrame(animFrame);
                card.style.transform = 'perspective(800px) rotateX(0) rotateY(0) scale3d(1, 1, 1) translateY(0)';
                glowSpot.style.opacity = '0';
            });
        });
    }

    // ─────────────────────────────────────────────────
    //  MAGNETIC BUTTON EFFECT
    //  Buttons subtly pull toward the cursor on hover
    // ─────────────────────────────────────────────────
    const magneticBtns = document.querySelectorAll('.btn-primary, .btn-lg, .magnetic-btn');
    if (!isMobile) {
        magneticBtns.forEach(btn => {
            btn.addEventListener('mousemove', (e) => {
                const rect = btn.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                btn.style.transform = `translate(${x * 0.15}px, ${y * 0.15}px) scale(1.03)`;
            });

            btn.addEventListener('mouseleave', () => {
                btn.style.transform = 'translate(0, 0) scale(1)';
            });
        });
    }

    // ─────────────────────────────────────────────────
    //  PARALLAX BACKGROUND ORBS
    //  Multi-layer parallax following cursor for depth
    // ─────────────────────────────────────────────────
    const parallaxBg = document.getElementById('parallaxBg');
    if (parallaxBg && !isMobile) {
        const orbs = parallaxBg.querySelectorAll('.orb');
        let px = 0, py = 0, cx = 0, cy = 0;

        window.addEventListener('mousemove', (e) => {
            cx = (e.clientX / window.innerWidth - 0.5) * 2;
            cy = (e.clientY / window.innerHeight - 0.5) * 2;
        }, { passive: true });

        // Smooth interpolation loop for butter-smooth movement
        function animateOrbs() {
            px += (cx - px) * 0.04;
            py += (cy - py) * 0.04;

            orbs.forEach((orb, i) => {
                const speed = (i + 1) * 20;
                const rotateSpeed = (i + 1) * 2;
                orb.style.transform = `translate(${px * speed}px, ${py * speed}px) rotate(${px * rotateSpeed}deg)`;
            });
            requestAnimationFrame(animateOrbs);
        }
        animateOrbs();
    }

    // ─────────────────────────────────────────────────
    //  HERO CARD PARALLAX LAYERS
    //  Inner elements shift at different speeds for depth
    // ─────────────────────────────────────────────────
    const heroCard = document.querySelector('.hero-card');
    if (heroCard && !isMobile) {
        const metrics = heroCard.querySelectorAll('.hero-metric');
        const chart = heroCard.querySelector('.hero-mini-chart');
        const score = heroCard.querySelector('.hero-card-score');

        heroCard.addEventListener('mousemove', (e) => {
            const rect = heroCard.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;

            // Each layer moves at a different depth
            if (score) score.style.transform = `translate(${x * 12}px, ${y * 12}px)`;
            if (chart) chart.style.transform = `translate(${x * 6}px, ${y * 6}px)`;
            metrics.forEach((m, i) => {
                m.style.transform = `translate(${x * (4 + i * 3)}px, ${y * (4 + i * 3)}px)`;
            });
        });

        heroCard.addEventListener('mouseleave', () => {
            if (score) score.style.transform = '';
            if (chart) chart.style.transform = '';
            metrics.forEach(m => { m.style.transform = ''; });
        });
    }

    // ─────────────────────────────────────────────────
    //  PROGRESS BAR ANIMATIONS
    //  Bars animate on scroll into view
    // ─────────────────────────────────────────────────
    const progressBars = document.querySelectorAll('[data-progress]');
    if (progressBars.length > 0) {
        const progObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = entry.target;
                    const value = target.getAttribute('data-progress');
                    setTimeout(() => {
                        target.style.width = value + '%';
                    }, 200);
                    progObserver.unobserve(target);
                }
            });
        }, { threshold: 0.5 });
        progressBars.forEach(el => progObserver.observe(el));
    }

    // ─────────────────────────────────────────────────
    //  SMOOTH SCROLL for anchor links
    // ─────────────────────────────────────────────────
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            const target = document.querySelector(anchor.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                if (navLinks) navLinks.classList.remove('active');
                if (mobileToggle) mobileToggle.classList.remove('active');
            }
        });
    });

    // ─────────────────────────────────────────────────
    //  MINI CHART BAR ANIMATION
    //  Hero mini chart bars animate in on load
    // ─────────────────────────────────────────────────
    const miniChartBars = document.querySelectorAll('.hero-mini-chart .bar');
    if (miniChartBars.length > 0) {
        miniChartBars.forEach((bar, i) => {
            const origHeight = bar.style.height;
            bar.style.height = '0%';
            bar.style.transition = `height 0.8s cubic-bezier(0.23, 1, 0.32, 1) ${i * 0.08}s`;
            setTimeout(() => { bar.style.height = origHeight; }, 500);
        });
    }

    // ── Auth-aware nav updates ────────────────
    updateNavAuth();
});

function updateNavAuth() {
    const token = localStorage.getItem('foundriq_token');
    const loginBtn = document.getElementById('navLoginBtn');
    const signupBtn = document.getElementById('navSignupBtn');

    if (token && loginBtn && signupBtn) {
        loginBtn.textContent = 'Dashboard';
        loginBtn.href = '/dashboard';
        signupBtn.textContent = 'Logout';
        signupBtn.href = '#';
        signupBtn.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.removeItem('foundriq_token');
            localStorage.removeItem('foundriq_user');
            window.location.href = '/';
        });
    }
}

