/**
 * demo.js – Industrial Pressure Monitoring
 * Teslead Equipment Pvt Ltd
 * Dependencies: Chart.js
 */

/* ─────────────────────────────────────────────
   SCALE CONFIG  ← only change GAUGE_SCALE_MODE
   ─────────────────────────────────────────────
   'classrating'    – uses class name (150/300/600/900…)
   'setpressure'    – set pressure × 2  (on test button click)
   'actualpressure' – live pressure × 2 (from API)
   ───────────────────────────────────────────── */
const GAUGE_SCALE_MODE = 'classrating';   // ← change this

let PSI_MIN = 0;
let PSI_MAX = 500;   // updated automatically by setGaugeScale()

const CLASS_RATING_MAP = {
    '150': 1200, '300': 2000, '600': 1500,
    '900': 2500, '1500': 4000, '2500': 6000
};

/* ─────────────────────────────────────────────
   GAUGE PHYSICAL CONSTANTS
   ───────────────────────────────────────────── */
const GAUGE_MIN_ANGLE = 225;   // needle angle at PSI_MIN (7:30 position)
const GAUGE_MAX_ANGLE = 495;   // needle angle at PSI_MAX (4:30 position)
const SWEEP_START = 225;   // SVG arc start angle
const ARC_SPAN = 270;   // total sweep in degrees

/* ─────────────────────────────────────────────
   CHART CONSTANTS
   ───────────────────────────────────────────── */
const CHART_COLORS = ['#00e5ff', '#ff4081', '#69f0ae', '#ffea00'];
const CHART_LABELS = { s1: 'Station 1', s2: 'Station 2', s3: 'Station 3', s4: 'Station 4' };

const chartInstances = {};
const chartData = {};

/* ─────────────────────────────────────────────
   LIVE DATA STATE
   Filled by updateChart() every 1 s.
   ───────────────────────────────────────────── */
const simState = {
    s1: { current: 0, time: '' },
    s2: { current: 0, time: '' },
    s3: { current: 0, time: '' },
    s4: { current: 0, time: '' }
};
window.simState = simState;

/* ─────────────────────────────────────────────
   PAUSE FLAG  – set true by clearAllCharts(),
                 reset false by resumeCharts()
   ───────────────────────────────────────────── */
let isPaused = false;

/* Clear every chart: reset data arrays + simState, wipe visuals */
window.clearAllCharts = function () {
    isPaused = true;

    // Reset in-memory state
    ['s1', 's2', 's3', 's4'].forEach(key => {
        simState[key].current = 0;
        simState[key].time = '';
        if (chartData[key]) {
            chartData[key].labels = [];
            chartData[key].readings = [];
        }
    });

    // Wipe Chart.js instances
    Object.keys(chartInstances).forEach(key => {
        const chart = chartInstances[key];
        if (!chart) return;
        chart.data.labels = [];
        chart.data.datasets.forEach(ds => { ds.data = []; });
        if (chart.options.plugins?.annotation) {
            chart.options.plugins.annotation.annotations = {};
        }
        chart.update();
    });

    // Reset gauges to zero
    ['s1', 's2', 's3', 's4'].forEach(key => {
        const svgEl = document.getElementById('gauge-svg-' + key);
        if (svgEl) {
            animateNeedle(svgEl, svgEl._currentPsi || 0, 0, 800);
            svgEl._currentPsi = 0;
            const readoutEl = document.getElementById('gauge-readout-' + key);
            if (readoutEl) readoutEl.textContent = '0.0';
        }
    });

    console.log('All charts and gauges cleared.');
};

/* Resume polling when a new test starts */
window.resumeCharts = function () {
    isPaused = false;
    console.log('Chart polling resumed.');
};

/* ═══════════════════════════════════════════════
   SCALE  –  call from template after test btn click
   ═══════════════════════════════════════════════ */

window.setGaugeScale = function (mode, value) {
    console.log(`[setGaugeScale] called with mode="${mode}" value="${value}" GAUGE_SCALE_MODE="${GAUGE_SCALE_MODE}"`);
    if (mode !== GAUGE_SCALE_MODE) return;
    if (mode === 'classrating') {
        // Extract just the digits — handles "150", "Class 150", "#150", etc.
        const digits = String(value).replace(/\D/g, '');
        PSI_MAX = CLASS_RATING_MAP[digits] || 500;
    } else if (mode === 'setpressure' || mode === 'actualpressure') {
        const parsed = parseFloat(value);
        if (isNaN(parsed) || parsed <= 0) return;
        PSI_MAX = Math.ceil(parsed * 2);
    } else {
        return;
    }
    PSI_MIN = 0;
    console.log(`[setGaugeScale] → PSI_MAX=${PSI_MAX}`);

    refreshAllGauges();
    updateAllChartYAxes();
};

/* ═══════════════════════════════════════════════
   GAUGE MATH
   ═══════════════════════════════════════════════ */

function psiToAngle(psi) {
    const clamped = Math.max(PSI_MIN, Math.min(PSI_MAX, psi));
    const ratio = (clamped - PSI_MIN) / (PSI_MAX - PSI_MIN);
    return GAUGE_MIN_ANGLE + ratio * (GAUGE_MAX_ANGLE - GAUGE_MIN_ANGLE);
}

function psiToSvgAngle(psi) {
    return SWEEP_START + ((psi - PSI_MIN) / (PSI_MAX - PSI_MIN)) * ARC_SPAN;
}

function polar(angleDeg, r) {
    const rad = (angleDeg - 90) * Math.PI / 180;
    return { x: 100 + r * Math.cos(rad), y: 100 + r * Math.sin(rad) };
}

/* ═══════════════════════════════════════════════
   NEEDLE ANIMATION
   ═══════════════════════════════════════════════ */

function animateNeedle(svgEl, fromPsi, toPsi, durationMs) {
    const needle = svgEl.querySelector('.gauge-needle');
    if (!needle) return;
    const fromAngle = psiToAngle(fromPsi);
    const toAngle = psiToAngle(toPsi);
    const start = performance.now();

    function easeInOut(t) { return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t; }

    function step(now) {
        const progress = Math.min((now - start) / durationMs, 1.0);
        const angle = fromAngle + (toAngle - fromAngle) * easeInOut(progress);
        needle.setAttribute('transform', `rotate(${angle}, 100, 100)`);
        if (progress < 1.0) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
}

/* ═══════════════════════════════════════════════
   GAUGE SVG BUILDER
   ═══════════════════════════════════════════════ */

function buildGaugeSVG(svgEl, psi) {
    const cx = 100, cy = 100, R = 88;

    // ── Face ──
    let html = `
        <circle cx="${cx}" cy="${cy}" r="99" fill="url(#metalRing)" stroke="#555" stroke-width="1"/>
        <circle cx="${cx}" cy="${cy}" r="91" fill="none" stroke="#ffffff22" stroke-width="2"/>
        <circle cx="${cx}" cy="${cy}" r="${R}" fill="#f0f0f0"/>
        <circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="#cccccc" stroke-width="1.5"/>
    `;

    // ── Color zones: red 0–20%, green 20–80%, red 80–100% ──
    const zones = [
        { from: PSI_MIN, to: PSI_MAX * 0.2, color: '#c62828' },
        { from: PSI_MAX * 0.2, to: PSI_MAX * 0.8, color: '#2e7d32' },
        { from: PSI_MAX * 0.8, to: PSI_MAX, color: '#c62828' },
    ];
    zones.forEach(z => {
        const s = polar(psiToSvgAngle(z.from), R - 10);
        const e = polar(psiToSvgAngle(z.to), R - 10);
        const large = (psiToSvgAngle(z.to) - psiToSvgAngle(z.from)) > 180 ? 1 : 0;
        html += `<path d="M${s.x.toFixed(2)},${s.y.toFixed(2)} A${R - 10},${R - 10} 0 ${large},1 ${e.x.toFixed(2)},${e.y.toFixed(2)}"
                      fill="none" stroke="${z.color}" stroke-width="8" stroke-linecap="butt"/>`;
    });

    // ── Tick marks & labels (dynamic based on PSI_MAX) ──
    const tickStep = Math.max(1, Math.round(PSI_MAX / 20));
    const majorEvery = tickStep * 2;
    const labelEvery = Math.max(1, Math.round(PSI_MAX / 5));

    for (let v = PSI_MIN; v <= PSI_MAX; v += tickStep) {
        const ang = psiToSvgAngle(v);
        const isMajor = (v % majorEvery === 0);
        const inner = isMajor ? R - 12 : R - 7;
        const sw = isMajor ? 1.4 : 0.7;
        const color = (v >= PSI_MAX * 0.8 || v <= PSI_MAX * 0.2) ? '#c62828' : '#333';
        const p1 = polar(ang, R - 2);
        const p2 = polar(ang, inner);

        html += `<line x1="${p1.x.toFixed(2)}" y1="${p1.y.toFixed(2)}"
                       x2="${p2.x.toFixed(2)}" y2="${p2.y.toFixed(2)}"
                       stroke="${color}" stroke-width="${sw}"/>`;

        if (v % labelEvery === 0) {
            const lp = polar(ang, R - 22);
            html += `<text x="${lp.x.toFixed(2)}" y="${lp.y.toFixed(2)}"
                           text-anchor="middle" dominant-baseline="central"
                           font-size="8" font-family="Arial,sans-serif"
                           font-weight="bold" fill="${color}">${v}</text>`;
        }
    }

    // Extra labels at 40%, 60%, 100%
    [0.4, 0.6, 1.0].forEach(pct => {
        const v = Math.round(PSI_MAX * pct);
        const lp = polar(psiToSvgAngle(v), R - 22);
        const color = (pct >= 0.8) ? '#c62828' : '#333';
        html += `<text x="${lp.x.toFixed(2)}" y="${lp.y.toFixed(2)}"
                       text-anchor="middle" dominant-baseline="central"
                       font-size="8" font-family="Arial,sans-serif"
                       font-weight="bold" fill="${color}">${v}</text>`;
    });

    // ── Readout & unit ──
    const key = svgEl.id.replace('gauge-svg-', '');
    const displayUnit = (typeof pressure_unit !== 'undefined' && pressure_unit !== '---') ? pressure_unit : '';
    html += `
        <text id="gauge-readout-${key}" x="${cx}" y="${cy + 60}"
              text-anchor="middle" font-size="20" font-family="Arial,sans-serif"
              fill="#111" font-weight="bold">${psi.toFixed(1)}</text>
        <text x="${cx}" y="${cy + 75}"
              text-anchor="middle" font-size="10" font-family="Arial,sans-serif"
              fill="#666" font-weight="bold">${displayUnit}</text>
    `;

    // ── Needle ──
    const angle = psiToAngle(psi);
    html += `
        <g class="gauge-needle" transform="rotate(${angle}, ${cx}, ${cy})">
            <polygon points="${cx},${cy - 72} ${cx - 2.2},${cy + 18} ${cx + 2.2},${cy + 18}" fill="#111"/>
            <polygon points="${cx},${cy + 18} ${cx - 3},${cy + 26} ${cx + 3},${cy + 26}" fill="#cc0000"/>
        </g>
        <circle cx="${cx}" cy="${cy}" r="6"   fill="#555" stroke="#333" stroke-width="1"/>
        <circle cx="${cx}" cy="${cy}" r="2.5" fill="#e0e0e0"/>
    `;

    // ── Defs & glass overlay ──
    const defs = `<defs>
        <radialGradient id="metalRing" cx="40%" cy="35%" r="65%">
            <stop offset="0%"   stop-color="#b0b8c1"/>
            <stop offset="40%"  stop-color="#7e8fa0"/>
            <stop offset="100%" stop-color="#3a4555"/>
        </radialGradient>
        <radialGradient id="glassShine" cx="35%" cy="25%" r="60%">
            <stop offset="0%"   stop-color="#ffffff" stop-opacity="0.18"/>
            <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
        </radialGradient>
        <filter id="gaugeShadow" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#000" flood-opacity="0.5"/>
        </filter>
    </defs>`;
    const glass = `<ellipse cx="${cx - 10}" cy="${cy - 15}" rx="45" ry="35"
        fill="url(#glassShine)" style="pointer-events:none"/>`;

    svgEl.innerHTML = defs + html + glass;
}

/* ═══════════════════════════════════════════════
   REFRESH HELPERS
   ═══════════════════════════════════════════════ */

function refreshAllGauges() {
    const unit = typeof pressure_unit !== 'undefined' ? pressure_unit : '---';
    ['s1', 's2', 's3', 's4'].forEach(key => {
        const svgEl = document.getElementById('gauge-svg-' + key);
        if (svgEl) buildGaugeSVG(svgEl, svgEl._currentPsi || 0);

        const chart = chartInstances[key];
        if (chart) {
            chart.data.datasets[0].label = CHART_LABELS[key] + ' Pressure (' + unit + ')';
            chart.options.scales.y.title.text = 'Pressure (' + unit + ')';
            chart.update('none');
        }
    });
}
window.refreshGauges = refreshAllGauges;

function updateAllChartYAxes() {
    Object.values(chartInstances).forEach(chart => {
        if (chart) { chart.options.scales.y.max = PSI_MAX; chart.update('none'); }
    });
}
window.updateChartYAxis = updateAllChartYAxes;

/* ═══════════════════════════════════════════════
   CHART FUNCTIONS
   ═══════════════════════════════════════════════ */

function initChart(canvasId, stationKey, color) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    chartData[stationKey] = { labels: [], readings: [] };

    chartInstances[stationKey] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData[stationKey].labels,
            datasets: [{
                label: CHART_LABELS[stationKey] + ' Pressure (' + (typeof pressure_unit !== 'undefined' ? pressure_unit : '---') + ')',
                data: chartData[stationKey].readings,
                borderColor: color,
                backgroundColor: color + '18',
                borderWidth: 2,
                pointRadius: 0, pointHoverRadius: 0, pointHitRadius: 0,
                fill: true, tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 400 },
            plugins: {
                legend: { display: true, labels: { color: '#90a4ae', font: { size: 11 }, boxWidth: 18 } },
                tooltip: { enabled: false }
            },
            scales: {
                x: {
                    ticks: { color: '#546e7a', font: { size: 9 }, maxTicksLimit: 8 },
                    grid: { color: '#1e2733' }
                },
                y: {
                    min: 0, max: PSI_MAX,
                    ticks: { color: '#546e7a', font: { size: 9 } },
                    grid: { color: '#1e2733' },
                    title: {
                        display: true,
                        text: 'Pressure (' + (typeof pressure_unit !== 'undefined' ? pressure_unit : '---') + ')',
                        color: '#607d8b', font: { size: 10 }
                    }
                }
            }
        }
    });
}

function pushReading(stationKey, psi, time) {
    const data = chartData[stationKey];
    if (!data) return;
    data.labels.push(time);
    data.readings.push(+psi.toFixed(2));
    const chart = chartInstances[stationKey];
    if (chart) {
        chart.data.labels = data.labels;
        chart.data.datasets[0].data = data.readings;
        chart.update('none');
    }
}

/* ═══════════════════════════════════════════════
   MAIN INIT
   ═══════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function () {
    updateChart();
    setInterval(function () { if (!isPaused) updateChart(); }, 1000);

    fetch('/api/livepage/get_active_testbtn/')
        .then(r => r.json())
        .then(data => {
            const stationKeys = data.test_buttons.map(t => `s${t.test_id}`);

            // Build gauges
            stationKeys.forEach(key => {
                const svgEl = document.getElementById('gauge-svg-' + key);
                if (!svgEl) return;
                svgEl._currentPsi = parseFloat(svgEl.getAttribute('data-pressure') || '0');
                buildGaugeSVG(svgEl, svgEl._currentPsi);
            });

            // Init charts
            stationKeys.forEach((key, i) => initChart('chart-' + key, key, CHART_COLORS[i]));

            // Live update loop — every 2 s reads simState (filled by updateChart)
            setInterval(function () {
                if (isPaused) return;   // ← skip when cycle complete
                stationKeys.forEach(key => {
                    const svgEl = document.getElementById('gauge-svg-' + key);
                    if (!svgEl) return;

                    const newPsi = simState[key].current;
                    const fromPsi = svgEl._currentPsi || 0;
                    svgEl._currentPsi = newPsi;

                    animateNeedle(svgEl, fromPsi, newPsi, 1200);

                    const readoutEl = document.getElementById('gauge-readout-' + key);
                    if (readoutEl) readoutEl.textContent = newPsi.toFixed(1);

                    pushReading(key, newPsi, simState[key].time);
                });
            }, 2000);
        });
});

/* ═══════════════════════════════════════════════
   API POLLER  – fetches real pressure every 1 s
   ═══════════════════════════════════════════════ */

function updateChart() {
    fetch('/api/livepage/get_pressure_data/')
        .then(r => r.json())
        .then(data => {
            Object.keys(data.pressure_data).forEach(key => {
                const { pressure, time } = data.pressure_data[key];
                if (window.simState && window.simState[key]) {
                    window.simState[key].current = parseFloat(pressure);
                    window.simState[key].time = time;
                }
            });
        });
}
