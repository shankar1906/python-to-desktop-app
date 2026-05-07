// ==========================================
//  Alarm Management
// ==========================================

const PAGE_KEY = 'alarm_page';
const ENTRIES_KEY = 'alarm_entries';
const SEARCH_KEY = 'alarm_search';

let searchQuery = '';
let currentPage = 1;
let entriesPerPage = 10;
let alarmsData = [];
let filteredData = [];
let existingCodes = [];
let currentEditId = null;

// Validators
let addValidator, editValidator;

// --- Regex & Rules ---
const rules = {
    required: { test: (val) => val && val.trim().length > 0, message: 'This field is required' },
    // Code validation: Alphanumeric only
    codeFormat: { test: /^[a-zA-Z0-9]+$/, message: 'Only alphanumeric allowed' }
};

function loadSession() {
    const p = sessionStorage.getItem(PAGE_KEY);
    if (p) currentPage = parseInt(p);
    const e = sessionStorage.getItem(ENTRIES_KEY);
    if (e) entriesPerPage = parseInt(e);
    const q = sessionStorage.getItem(SEARCH_KEY);
    if (q) {
        searchQuery = q;
        document.getElementById('customSearchInput').value = q;
    }
    if (localStorage.getItem('alarmHintDismissed') === 'true') {
        document.getElementById('editHint')?.classList.add('hidden');
    }
}

function saveSession() {
    sessionStorage.setItem(PAGE_KEY, currentPage);
    sessionStorage.setItem(ENTRIES_KEY, entriesPerPage);
    sessionStorage.setItem(SEARCH_KEY, searchQuery);
}

function clearSession() {
    sessionStorage.removeItem(PAGE_KEY);
    sessionStorage.removeItem(ENTRIES_KEY);
    sessionStorage.removeItem(SEARCH_KEY);
}

window.dismissHint = function () { // Added window. to make it global scope accessible
    document.getElementById('editHint')?.classList.add('hidden');
    localStorage.setItem('alarmHintDismissed', 'true');
}

document.addEventListener('DOMContentLoaded', function () {
    const n = performance.getEntriesByType('navigation')[0]?.type || (performance.navigation?.type === 1 ? 'reload' : 'navigate');
    if (n === 'reload') loadSession();
    else clearSession();

    initSearchToggle();
    loadAlarms();

    // -- Initialize Validators --

    // ADD FORM VALIDATOR
    addValidator = new FormValidator('alarmAddForm', {
        alarm_code: {
            rules: [rules.required, rules.codeFormat],
            asyncRule: checkCodeUniqueAsync
        },
        alarm_name: { rules: [rules.required] },
        alarm_status: { rules: [rules.required] },
        alarm_severity: { rules: [rules.required] }
    });

    // EDIT FORM VALIDATOR
    editValidator = new FormValidator('alarmEditForm', {
        alarm_code: {
            rules: [rules.required, rules.codeFormat],
            asyncRule: (val, signal, form) => checkCodeUniqueAsync(val, signal, form, currentEditId)
        },
        alarm_name: { rules: [rules.required] },
        alarm_status: { rules: [rules.required] },
        alarm_severity: { rules: [rules.required] }
    });

    // Bind Submit Buttons
    document.getElementById('saveAddAlarm').addEventListener('click', async () => {
        if (await addValidator.validateAll()) saveAddAlarm();
    });

    document.getElementById('saveEditAlarm').addEventListener('click', async () => {
        if (await editValidator.validateAll()) saveEditAlarm();
    });

    // --- Dynamic Status Colors ---
    const updateStatusColor = (selectEl) => {
        const val = selectEl.value;
        selectEl.classList.remove('status-enabled', 'status-disabled');
        if (val === 'Enabled') selectEl.classList.add('status-enabled');
        else if (val === 'Disabled') selectEl.classList.add('status-disabled');
    };

    ['addAlarmStatus', 'editAlarmStatus'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('change', () => updateStatusColor(el));
            // Initialize
            updateStatusColor(el);
        }
    });

    // Reset forms on modal open
    document.getElementById('addAlarmBtn').addEventListener('click', () => {
        addValidator.reset();
        const addStatus = document.getElementById('addAlarmStatus');
        if (addStatus) {
            addStatus.value = "";
            updateStatusColor(addStatus);
        }
    });
    // Expose updateStatusColor primarily for the edit flow
    window.refreshStatusColors = function () {
        ['addAlarmStatus', 'editAlarmStatus'].forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                const val = el.value;
                el.classList.remove('status-enabled', 'status-disabled');
                if (val === 'Enabled') el.classList.add('status-enabled');
                else if (val === 'Disabled') el.classList.add('status-disabled');
            }
        });
    }
    // Add modal event listeners to prevent stuck/blur issues
    const addModal = document.getElementById('addAlarmModal');
    const editModal = document.getElementById('editAlarmModal');

    // Handle modal hidden events
    addModal.addEventListener('hidden.bs.modal', function () {
        document.body.classList.remove('modal-open');
        document.body.style.overflow = '';
        document.body.style.paddingRight = '';
        document.querySelectorAll('.modal-backdrop').forEach(backdrop => backdrop.remove());
    });

    editModal.addEventListener('hidden.bs.modal', function () {
        document.body.classList.remove('modal-open');
        document.body.style.overflow = '';
        document.body.style.paddingRight = '';
        document.querySelectorAll('.modal-backdrop').forEach(backdrop => backdrop.remove());
        currentEditId = null;
    });

    // Prevent modal from closing on backdrop click during form submission
    addModal.addEventListener('hide.bs.modal', function (e) {
        if (document.querySelector('.loading-overlay')) {
            e.preventDefault();
            return false;
        }
    });

    editModal.addEventListener('hide.bs.modal', function (e) {
        if (document.querySelector('.loading-overlay')) {
            e.preventDefault();
            return false;
        }
    });
});

// --- Async Simulation ---
function checkCodeUniqueAsync(code, signal, form, excludeId = null) {
    return new Promise((resolve, reject) => {
        if (signal?.aborted) return reject(new DOMException('Aborted', 'AbortError'));

        setTimeout(() => {
            if (signal?.aborted) return reject(new DOMException('Aborted', 'AbortError'));

            const normalize = s => (s || '').toString().toLowerCase().trim();
            const target = normalize(code);

            const exists = alarmsData.some(alarm => {
                if (excludeId && alarm.alarm_id == excludeId) return false; // Use alarm_id
                return normalize(alarm.alarm_code) === target;
            });

            if (exists) resolve("Code already exists");
            else resolve(true);

        }, 300);
    });
}

function initSearchToggle() {
    const t = document.getElementById('searchToggleBtn');
    const w = document.getElementById('searchInputWrapper');
    const i = document.getElementById('customSearchInput');
    const c = document.getElementById('searchCloseBtn');

    t.addEventListener('click', e => {
        e.stopPropagation();
        if (!w.classList.contains('active')) {
            w.classList.add('active');
            t.classList.add('active');
            setTimeout(() => i.focus(), 300);
        }
    });

    c.addEventListener('click', e => {
        e.stopPropagation();
        w.classList.remove('active');
        i.value = '';
        searchQuery = '';
        saveSession();
        applySearch();
    });

    i.addEventListener('keyup', e => {
        searchQuery = e.target.value.toLowerCase();
        saveSession();
        applySearch();
    });

    document.addEventListener('click', e => {
        if (w.classList.contains('active') && !w.contains(e.target)) {
            w.classList.remove('active');
        }
    });
}

function applySearch() {
    if (searchQuery === '') filteredData = alarmsData;
    else filteredData = alarmsData.filter(r =>
        (r.alarm_code || '').toLowerCase().includes(searchQuery) ||
        (r.alarm_name || '').toLowerCase().includes(searchQuery)
    );
    renderTable();
}

function loadAlarms() {
    fetch('/api/alarm/').then(r => r.json()).then(d => {
        alarmsData = d.alarms || [];
        existingCodes = d.existing_codes || [];
        applySearch();
    }).catch(e => DialogManager.toast({ type: 'error', message: 'Failed to load data' }));
}

function renderTable() {
    const tbody = document.querySelector('#alarmTable tbody');
    if (!filteredData.length) {
        tbody.innerHTML = `<tr><td colspan="3" class="text-center py-5 text-muted">No records found</td></tr>`;
        updatePagination(0);
        return;
    }

    const s = (currentPage - 1) * entriesPerPage;
    const e = s + entriesPerPage;
    const p = filteredData.slice(s, e);
    let h = '';

    p.forEach((r, index) => {
        const serialNo = s + index + 1;

        const statusClass = r.alarm_status.toLowerCase();
        const statusBadge = `<span class="status-badge ${statusClass}">${escapeHtml(r.alarm_status)}</span>`;

        // Updated to use alarm_id and escape quotes in names
        h += `<tr onclick="handleRowInteraction(${r.alarm_id}, '${(r.alarm_name || '').replace(/'/g, "\\'")}')">
      <td class="text-center">${serialNo}</td>
        
      ${window.superuser_level == 2 ? `<td class="font-weight-bold">${escapeHtml(r.alarm_code || '-')}</td>` : ''}
      <td class="font-weight-bold">${escapeHtml(r.alarm_name || '-')}</td>
      <td class="font-weight-bold">${escapeHtml(r.alarm_severity_level || '-')}</td>
      <td class="font-weight-bold">${statusBadge}</td>
    </tr>`;
    });

    tbody.innerHTML = h;
    updatePagination(filteredData.length);
}

function escapeHtml(text) {
    if (!text) return text;
    return text.toString()
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

window.handleRowInteraction = function (id, name) { // Added window.
    DialogManager.confirm({
        title: `Action for "${name}"`,
        message: "Choose an action",
        confirmText: "Edit",
        denyText: "Delete",
        cancelText: "Cancel",
        onConfirm: () => {
            DialogManager.confirm({
                title: "Edit Alarm?",
                message: `Are you sure you want to edit "${name}"?`,
                confirmText: "Yes, Edit",
                onConfirm: () => editAlarm(id)
            });
        },
        onDeny: () => deleteAlarm(id)
    });
}

function updatePagination(t) {
    const tp = Math.ceil(t / entriesPerPage);
    const c = document.getElementById('customPagination');
    if (!c) return;
    let h = [];
    h.push(`<span class="text-muted small me-3">Total: ${t}</span>`);
    h.push(`<button class="pagination-btn prev-btn" onclick="goToPage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>Previous</button>`);
    if (tp <= 7) {
        for (let i = 1; i <= tp; i++) h.push(`<button class="pagination-btn ${i === currentPage ? 'active' : ''}" onclick="goToPage(${i})">${i}</button>`);
    } else {
        h.push(`<button class="pagination-btn ${currentPage === 1 ? 'active' : ''}" onclick="goToPage(1)">1</button>`);
        if (currentPage > 3) h.push('<span class="pagination-ellipsis">...</span>');
        let s = Math.max(2, currentPage - 1);
        let e = Math.min(tp - 1, currentPage + 1);
        for (let i = s; i <= e; i++) h.push(`<button class="pagination-btn ${i === currentPage ? 'active' : ''}" onclick="goToPage(${i})">${i}</button>`);
        if (currentPage < tp - 2) h.push('<span class="pagination-ellipsis">...</span>');
        h.push(`<button class="pagination-btn ${currentPage === tp ? 'active' : ''}" onclick="goToPage(${tp})">${tp}</button>`);
    }
    h.push(`<button class="pagination-btn next-btn" onclick="goToPage(${currentPage + 1})" ${currentPage === tp || tp === 0 ? 'disabled' : ''}>Next</button>`);
    h.push(`<select class="pagination-per-page" onchange="changeItemsPerPage(this.value)"><option value="10" ${entriesPerPage === 10 ? 'selected' : ''}>10 / page</option><option value="25" ${entriesPerPage === 25 ? 'selected' : ''}>25 / page</option><option value="50" ${entriesPerPage === 50 ? 'selected' : ''}>50 / page</option><option value="100" ${entriesPerPage === 100 ? 'selected' : ''}>100 / page</option></select>`);
    c.innerHTML = h.join('');
}

window.goToPage = function (p) {
    const t = Math.ceil(filteredData.length / entriesPerPage);
    if (p < 1 || (t > 0 && p > t)) return;
    currentPage = p;
    saveSession();
    renderTable();
};

window.changeItemsPerPage = function (v) {
    entriesPerPage = parseInt(v);
    currentPage = 1;
    saveSession();
    renderTable();
};

function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
}

// Improved modal closing function to prevent blur/stuck issues
function closeModalProperly(modalId) {
    const modalEl = document.getElementById(modalId);
    if (!modalEl) return;

    const modal = bootstrap.Modal.getInstance(modalEl);
    if (modal) {
        modal.hide();
    }

    setTimeout(() => {
        document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
            backdrop.remove();
        });

        document.body.classList.remove('modal-open');
        document.body.style.overflow = '';
        document.body.style.paddingRight = '';

        modalEl.classList.remove('show');
        modalEl.style.display = 'none';
        modalEl.setAttribute('aria-hidden', 'true');
        modalEl.removeAttribute('aria-modal');

        if (document.activeElement && document.activeElement.closest('.modal')) {
            document.activeElement.blur();
        }
    }, 150);
}

function saveAddAlarm() {
    const form = document.getElementById('alarmAddForm');
    const fd = new FormData(form);

    DialogManager.loading('Saving...');
    fetch('/api/alarm/add/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCsrfToken() },
        body: fd
    }).then(r => r.json()).then(d => {
        DialogManager.closeLoading();
        if (d.success) {
            closeModalProperly('addAlarmModal');
            DialogManager.toast({ type: 'success', message: 'Alarm added successfully' });
            loadAlarms();
            form.reset();
            addValidator.reset();
        } else {
            DialogManager.toast({ type: 'error', message: d.error });
        }
    }).catch(e => {
        DialogManager.closeLoading();
        DialogManager.toast({ type: 'error', message: 'Failed to save alarm' });
    });
}

window.editAlarm = function (id) {
    const e = alarmsData.find(x => x.alarm_id === id); // Use alarm_id
    if (!e) return;

    currentEditId = id;
    editValidator.reset();

    document.getElementById('editAlarmId').value = id;
    document.getElementById('editAlarmCode').value = e.alarm_code || '';
    document.getElementById('editAlarmName').value = e.alarm_name || '';
    document.getElementById('editAlarmSeverity').value = e.alarm_severity_level || '';
    document.getElementById('editAlarmStatus').value = e.alarm_status || '';
    if (window.refreshStatusColors) window.refreshStatusColors();

    new bootstrap.Modal(document.getElementById('editAlarmModal')).show();
};

function saveEditAlarm() {
    const form = document.getElementById('alarmEditForm');
    const fd = new FormData(form);
    const id = document.getElementById('editAlarmId').value;

    DialogManager.loading('Updating...');
    fetch('/api/alarm/edit/' + id + '/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCsrfToken() },
        body: fd
    }).then(r => r.json()).then(d => {
        DialogManager.closeLoading();
        if (d.success) {
            closeModalProperly('editAlarmModal');
            DialogManager.toast({ type: 'success', message: 'Alarm updated successfully' });
            loadAlarms();
            currentEditId = null;
        } else {
            DialogManager.toast({ type: 'error', message: d.error });
        }
    }).catch(e => {
        DialogManager.closeLoading();
        DialogManager.toast({ type: 'error', message: 'Failed to update alarm' });
    });
}

window.deleteAlarm = function (id) {
    DialogManager.confirmAction({
        title: 'Delete Alarm?',
        text: 'This action cannot be undone.',
        confirmText: 'Yes, delete',
        url: '/api/alarm/delete/' + id + '/',
        method: 'POST',
        onSuccess: () => loadAlarms()
    });
};
