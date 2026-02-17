// ═══════════════════════════════════════════
// FIELDWORK — main.js
// Competitive Hiring Intelligence
// ═══════════════════════════════════════════

// ─── COMPANY DATA (from real jobs.db queries) ───
const COMPANIES = {
    "Amazon": {
        name: "Amazon",
        industry: "E-Commerce / Cloud",
        roles: 585,
        aws_roles: 410,
        avg_sal: 238159,
        ai_pct: 6.2,
        top_functions: ["Engineering", "Sales", "Operations", "Product"],
        signal: "Aggressive Growth",
        signal_detail: "585 open roles across consumer and AWS divisions",
        seniority: { senior: "45%", vp: "8%", director: "6%" }
    },
    "JPMorganChase": {
        name: "JPMorgan Chase",
        industry: "Financial Services",
        roles: 346,
        avg_sal: 215552,
        ai_pct: 13.9,
        top_functions: ["Product", "Sales", "Engineering", "Data"],
        signal: "Tech Transformation",
        signal_detail: "Heavy product & engineering hiring signals tech buildout",
        seniority: { vp: "67%", senior: "18%", director: "5%" }
    },
    "Deloitte": {
        name: "Deloitte",
        industry: "Professional Services",
        roles: 265,
        avg_sal: 254864,
        ai_pct: 24.5,
        top_functions: ["Sales", "Data", "Consulting"],
        signal: "AI Investment",
        signal_detail: "24.5% AI mention rate, heavy senior-level hiring",
        seniority: { senior: "85%", mid: "12%", vp: "2%" }
    },
    "Google": {
        name: "Google",
        industry: "Technology",
        roles: 257,
        avg_sal: 235568,
        ai_pct: 1.9,
        top_functions: ["Sales", "Engineering", "Operations", "Product"],
        signal: "Selective Hiring",
        signal_detail: "Reduced volume but high-comp roles persist",
        seniority: { senior: "55%", director: "15%", mid: "12%" }
    },
    "Salesforce": {
        name: "Salesforce",
        industry: "Enterprise SaaS",
        roles: 62,
        avg_sal: 287601,
        ai_pct: 12.9,
        top_functions: ["Sales", "Engineering", "Finance", "Marketing"],
        signal: "Aggressive Growth",
        signal_detail: "Highest avg comp in dataset at $288K",
        seniority: { senior: "37%", unknown: "37%", director: "10%" }
    },
    "Meta": {
        name: "Meta",
        industry: "Technology / Social",
        roles: 63,
        avg_sal: 232216,
        ai_pct: 34.9,
        top_functions: ["Engineering", "Sales", "Marketing", "Data"],
        signal: "AI-First Pivot",
        signal_detail: "35% AI mention rate, heavy engineering investment",
        seniority: { senior: "48%", director: "16%", entry: "11%" }
    },
    "ServiceNow": {
        name: "ServiceNow",
        industry: "Enterprise SaaS",
        roles: 52,
        avg_sal: 286280,
        ai_pct: 48.1,
        top_functions: ["Sales", "Engineering", "People"],
        signal: "AI-First Pivot",
        signal_detail: "48% of roles mention AI, highest in enterprise SaaS",
        seniority: { senior: "48%", vp: "6%", director: "4%" }
    },
    "Microsoft": {
        name: "Microsoft",
        industry: "Technology",
        roles: 141,
        avg_sal: 241409,
        ai_pct: 2.8,
        top_functions: ["Engineering", "Sales", "Product"],
        signal: "Steady Build",
        signal_detail: "Consistent hiring at premium comp levels",
        seniority: { senior: "40%", mid: "20%", director: "10%" }
    },
    "Accenture": {
        name: "Accenture",
        industry: "Professional Services",
        roles: 231,
        avg_sal: 232428,
        ai_pct: 13.4,
        top_functions: ["Consulting", "Engineering", "Data"],
        signal: "Expansion Mode",
        signal_detail: "231 active roles with above-market comp",
        seniority: { senior: "50%", mid: "25%", director: "10%" }
    },
    "Apple": {
        name: "Apple",
        industry: "Technology / Hardware",
        roles: 59,
        avg_sal: null,
        ai_pct: 11.9,
        top_functions: ["Engineering", "Product", "Operations"],
        signal: "Selective Hiring",
        signal_detail: "Comp data withheld, typical of Apple's posting strategy",
        seniority: { senior: "50%", mid: "20%", director: "12%" }
    },
    "Synchrony": {
        name: "Synchrony",
        industry: "Financial Services",
        roles: 205,
        avg_sal: 214424,
        ai_pct: 27.3,
        top_functions: ["Engineering", "Data", "Product"],
        signal: "AI Investment",
        signal_detail: "27% AI rate, 3rd highest in financial services",
        seniority: { senior: "45%", vp: "15%", director: "10%" }
    },
    "Adobe": {
        name: "Adobe",
        industry: "Creative Software",
        roles: 34,
        avg_sal: 327201,
        ai_pct: 5.9,
        top_functions: ["Engineering", "Product", "Sales"],
        signal: "Premium Comp",
        signal_detail: "Avg max salary of $327K, 2nd highest tracked",
        seniority: { senior: "45%", director: "15%", mid: "15%" }
    }
};

const FEATURED = ["Salesforce", "ServiceNow", "JPMorganChase"];
const COMPANY_KEYS = Object.keys(COMPANIES);


// ─── HELPERS ───

function formatSalary(sal) {
    if (!sal) return "Undisclosed";
    return "$" + Math.round(sal / 1000) + "K";
}

function signalIcon(signal) {
    if (signal.includes("AI")) return "&#9889;";
    if (signal.includes("Growth") || signal.includes("Expansion")) return "&#8599;";
    if (signal.includes("Premium")) return "&#9733;";
    return "&#8226;";
}


// ─── COMPETITOR CARD RENDERING ───

function renderCompetitorCard(key, options) {
    options = options || {};
    var c = COMPANIES[key];
    if (!c) return "";
    var isFeatured = options.featured || false;
    var isBlurred = options.blurred || false;

    var salDisplay = c.avg_sal ? formatSalary(c.avg_sal) : "Undisclosed";
    var fns = c.top_functions.slice(0, 4).map(function(f) {
        return '<span class="card-fn-tag">' + f + '</span>';
    }).join("");

    return '<div class="competitor-card' + (isFeatured ? ' featured' : '') + (isBlurred ? ' blurred' : '') + '">' +
        '<div class="card-company">' + c.name + '</div>' +
        '<div class="card-industry">' + c.industry + '</div>' +
        '<div class="card-stats">' +
            '<div class="card-stat">' +
                '<div class="card-stat-val ember">' + c.roles + '</div>' +
                '<div class="card-stat-label">Open Roles</div>' +
            '</div>' +
            '<div class="card-stat">' +
                '<div class="card-stat-val teal">' + salDisplay + '</div>' +
                '<div class="card-stat-label">Avg Max Salary</div>' +
            '</div>' +
        '</div>' +
        '<div class="card-section-title">Top Functions Hiring</div>' +
        '<div class="card-fn-tags">' + fns + '</div>' +
        '<div class="card-ai-bar">' +
            '<div class="card-ai-label">' +
                '<span>AI Adoption</span>' +
                '<span>' + c.ai_pct + '%</span>' +
            '</div>' +
            '<div class="card-ai-track">' +
                '<div class="card-ai-fill" style="width: ' + Math.min(c.ai_pct * 2, 100) + '%"></div>' +
            '</div>' +
        '</div>' +
        '<div class="card-signal">' +
            '<span class="card-signal-icon">' + signalIcon(c.signal) + '</span>' +
            '<span class="card-signal-text">' + c.signal + ': ' + c.signal_detail + '</span>' +
        '</div>' +
    '</div>';
}

function renderCards(selected) {
    var container = document.getElementById("competitor-cards");
    if (!container) return;
    var html = "";

    var visible = selected ? [selected] : FEATURED.slice(0, 2);
    visible.forEach(function(key) {
        html += renderCompetitorCard(key, { featured: key === (selected || FEATURED[0]) });
    });

    if (selected && visible.length === 1) {
        var second = FEATURED.find(function(f) { return f !== selected; }) || FEATURED[0];
        html += renderCompetitorCard(second);
    }

    var blurredKey = COMPANY_KEYS.find(function(k) {
        return visible.indexOf(k) === -1 && k !== (selected || "");
    });
    if (blurredKey) {
        html += renderCompetitorCard(blurredKey, { blurred: true });
    }

    html += '<div class="blur-overlay">' +
        '<div class="blur-cta">' +
            '<p>10+ more companies available in your custom report</p>' +
            '<a href="#sample-report" class="fw-btn fw-btn--primary fw-btn--sm">Get Full Report</a>' +
        '</div>' +
    '</div>';

    container.innerHTML = html;
}


// ─── SEARCH / DROPDOWN ───

function initSearch() {
    var searchInput = document.getElementById("company-search");
    var dropdown = document.getElementById("company-dropdown");
    if (!searchInput || !dropdown) return;

    function renderDropdown(filter) {
        var keys = COMPANY_KEYS;
        if (filter) {
            var lf = filter.toLowerCase();
            keys = COMPANY_KEYS.filter(function(k) {
                return COMPANIES[k].name.toLowerCase().indexOf(lf) !== -1;
            });
        }
        if (keys.length === 0) keys = COMPANY_KEYS;

        dropdown.innerHTML = keys.map(function(k) {
            var c = COMPANIES[k];
            return '<div class="demo-dropdown-item" data-key="' + k + '">' +
                '<span class="company-name">' + c.name + '</span>' +
                '<span class="company-count">' + c.roles + ' roles</span>' +
            '</div>';
        }).join("");

        dropdown.querySelectorAll(".demo-dropdown-item").forEach(function(item) {
            item.addEventListener("click", function() {
                var key = item.dataset.key;
                searchInput.value = COMPANIES[key].name;
                dropdown.classList.remove("open");
                renderCards(key);
            });
        });
    }

    searchInput.addEventListener("focus", function() {
        renderDropdown(searchInput.value);
        dropdown.classList.add("open");
    });

    searchInput.addEventListener("input", function() {
        renderDropdown(searchInput.value);
        dropdown.classList.add("open");
    });

    document.addEventListener("click", function(e) {
        if (!e.target.closest(".demo-search")) {
            dropdown.classList.remove("open");
        }
    });
}


// ─── CTA FORM ───

function initForm() {
    var submitBtn = document.getElementById("cta-submit");
    if (!submitBtn) return;

    submitBtn.addEventListener("click", function() {
        var name = document.getElementById("cta-name").value.trim();
        var email = document.getElementById("cta-email").value.trim();
        var company = document.getElementById("cta-company").value.trim();
        var competitor = document.getElementById("cta-competitor").value.trim();

        var valid = true;
        [["cta-name", name], ["cta-email", email], ["cta-company", company]].forEach(function(pair) {
            var el = document.getElementById(pair[0]);
            var val = pair[1];
            if (!val || (pair[0] === "cta-email" && val.indexOf("@") === -1)) {
                el.style.borderColor = "var(--fw-error, #EF4444)";
                valid = false;
            } else {
                el.style.borderColor = "var(--fw-border-strong)";
            }
        });

        if (!valid) return;

        var lead = {
            name: name,
            email: email,
            company: company,
            competitor: competitor,
            timestamp: new Date().toISOString()
        };
        console.log("New Fieldwork lead:", lead);

        var leads = JSON.parse(localStorage.getItem("fieldwork_leads") || "[]");
        leads.push(lead);
        localStorage.setItem("fieldwork_leads", JSON.stringify(leads));

        document.getElementById("cta-form").style.display = "none";
        document.getElementById("cta-success").style.display = "block";
    });

    document.querySelectorAll(".cta-input").forEach(function(input) {
        input.addEventListener("focus", function() {
            this.style.borderColor = "var(--fw-primary)";
        });
        input.addEventListener("blur", function() {
            this.style.borderColor = "var(--fw-border-strong)";
        });
    });
}


// ─── HERO NUMBER ANIMATION ───

function animateValue(el, end, duration) {
    if (!el) return;
    var numericEnd = parseInt(end.toString().replace(/,/g, ""));
    if (isNaN(numericEnd)) return;

    var start = performance.now();
    function update(now) {
        var elapsed = now - start;
        var progress = Math.min(elapsed / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        var current = Math.round(eased * numericEnd);
        el.textContent = current.toLocaleString();
        if (progress < 1) requestAnimationFrame(update);
    }
    el.textContent = "0";
    requestAnimationFrame(update);
}


// ─── SCROLL FADE-IN ANIMATIONS ───

function initFadeAnimations() {
    var fadeEls = document.querySelectorAll(".fade-in");
    if (!fadeEls.length) return;

    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    fadeEls.forEach(function(el) { observer.observe(el); });
}


// ─── SMOOTH SCROLL ───

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener("click", function(e) {
            var href = this.getAttribute("href");
            if (!href || href === "#") return;
            var target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: "smooth", block: "start" });
                var nav = document.getElementById("main-nav");
                if (nav) nav.classList.remove("open");
            }
        });
    });
}


// ─── MOBILE NAV ───

function initMobileNav() {
    var toggle = document.getElementById("mobile-toggle");
    var nav = document.getElementById("main-nav");
    if (!toggle || !nav) return;

    toggle.addEventListener("click", function() {
        nav.classList.toggle("open");
        toggle.setAttribute("aria-expanded", nav.classList.contains("open"));
    });
}


// ─── INIT ───

document.addEventListener("DOMContentLoaded", function() {
    renderCards(null);
    initSearch();
    initForm();
    initFadeAnimations();
    initSmoothScroll();
    initMobileNav();

    animateValue(document.getElementById("stat-jobs"), 27127, 1800);
    animateValue(document.getElementById("stat-companies"), 11063, 1800);
});
