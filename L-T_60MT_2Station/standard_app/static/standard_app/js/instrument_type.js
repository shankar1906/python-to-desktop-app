// ==========================================
//  Instrument Type Management
// ==========================================

const PAGE_KEY = 'instrument_type_page';
const PER_PAGE_KEY = 'instrument_type_per_page';

let instrumentTypes = [];
let filteredData = [];
let searchQuery = '';
let sortColumn = '';
let sortDirection = 'asc';
let currentPage = 1;
let itemsPerPage = 10;

document.addEventListener('DOMContentLoaded', () => {
    // Restore Session
    const savedPage = localStorage.getItem(PAGE_KEY);
    const savedPPI = localStorage.getItem(PER_PAGE_KEY);
    if (savedPage) currentPage = parseInt(savedPage);
    if (savedPPI) itemsPerPage = parseInt(savedPPI);

    loadInstrumentTypes();
    initSearchToggle();
    initSortHeaders();
});

function initSortHeaders() {
    document.querySelectorAll('th.sortable').forEach(header => {
        header.addEventListener('click', () => {
            const col = header.dataset.column;
            if (sortColumn === col) {
                sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                sortColumn = col;
                sortDirection = 'asc';
            }

            // Update UI
            document.querySelectorAll('th.sortable i').forEach(i => i.className = 'fas fa-sort');
            const icon = header.querySelector('i');
            icon.className = sortDirection === 'asc' ? 'fas fa-sort-up' : 'fas fa-sort-down';

            renderTable();
        });
    });
}

function initSearchToggle() {
    const wrapper = document.getElementById('searchInputWrapper');
    const toggleBtn = document.getElementById('searchToggleBtn');
    const closeBtn = document.getElementById('searchCloseBtn');
    const input = document.getElementById('customSearchInput');

    if (!wrapper || !toggleBtn || !closeBtn || !input) return;

    toggleBtn.addEventListener('click', () => {
        wrapper.classList.add('active');
        input.focus();
    });

    closeBtn.addEventListener('click', () => {
        input.value = '';
        searchQuery = '';
        wrapper.classList.remove('active');
        currentPage = 1;
        renderTable();
    });

    input.addEventListener('keyup', (e) => {
        searchQuery = e.target.value.trim();
        currentPage = 1;
        renderTable();
    });

    document.addEventListener('click', (e) => {
        if (!wrapper.contains(e.target) && !toggleBtn.contains(e.target) && wrapper.classList.contains('active')) {
            if (input.value.trim() === '') {
                wrapper.classList.remove('active');
            }
        }
    });
}

// --- Data Operations ---

function getUid() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

function loadInstrumentTypes() {
    fetch('/api/instrument_type/')
        .then(r => r.json())
        .then(data => {
            if (!data.success) {
                return DialogManager.toast({ type: 'error', message: data.error || 'Failed to load data' });
            }

            // Normalize Data
            instrumentTypes = (data.instrument_types || []).map(item => ({
                instrument_type_id: item.instrument_type_id || '', // Using instrument_type_id
                instrument_name: item.instrument_name || '',
                instrument_serial_no: item.instrument_serial_no || '',
                instrument_done_date: item.instrument_done_date || '',
                instrument_due_date: item.instrument_due_date || '',
                instrument_due_alarm: item.instrument_due_alarm || '',
                status: item.status || 'ENABLE',
                _uid: getUid()
            }));

            renderTable();
        })
        .catch(err => {
            console.error(err);
            DialogManager.toast({ type: 'error', message: 'Failed to load instrument types.' });
        });
}

function renderTable() {
    const tbody = document.getElementById("instrument_tbody");
    if (!tbody) return;

    // 1. Filter
    filteredData = instrumentTypes.filter(tt => {
        if (!searchQuery) return true;
        const q = searchQuery.toLowerCase();
        return (tt.instrument_name || '').toLowerCase().includes(q) ||
            (tt.instrument_serial_no || '').toLowerCase().includes(q) ||
            (tt.status || '').toLowerCase().includes(q);
    });

    // 2. Sort
    if (sortColumn) {
        filteredData.sort((a, b) => {
            let va = (a[sortColumn] || '').toString().toLowerCase();
            let vb = (b[sortColumn] || '').toString().toLowerCase();
            if (va < vb) return sortDirection === 'asc' ? -1 : 1;
            if (va > vb) return sortDirection === 'asc' ? 1 : -1;
            return 0;
        });
    }

    // 3. Paginate
    const totalItems = filteredData.length;
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    if (currentPage > totalPages) currentPage = totalPages || 1;
    if (currentPage < 1) currentPage = 1;

    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const pageData = filteredData.slice(start, end);

    // 4. Render Rows
    tbody.innerHTML = '';
    if (pageData.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center text-muted py-4">No instrument types found</td></tr>`;
    } else {
        pageData.forEach((tt, idx) => {
            tbody.appendChild(createRow(tt, start + idx + 1));
        });
    }

    renderPagination(totalPages, totalItems);
}

function createRow(tt, sno) {
    const row = document.createElement('tr');

    row.innerHTML = `
      <td class="text-end text-secondary pe-3">${sno}</td>
      <td>
        <input type="text" class="form-control" value="${escapeHtml(tt.instrument_serial_no)}" data-uid="${tt._uid}"
          onblur="checkDuplicateSerial(this); updateInMemory('${tt._uid}', 'instrument_serial_no', this.value)">
        <div class="invalid-feedback"></div>
      </td>
      <td>
        <input type="text" class="form-control" value="${escapeHtml(tt.instrument_name)}" data-uid="${tt._uid}"
          onblur="checkDuplicate(this); updateInMemory('${tt._uid}', 'instrument_name', this.value)">
        <div class="invalid-feedback"></div>
      </td>
      <td>
        <input type="date" class="form-control" value="${escapeHtml(tt.instrument_done_date)}" data-uid="${tt._uid}"
          onblur="updateInMemory('${tt._uid}', 'instrument_done_date', this.value)">
      </td>
      <td>
        <input type="date" class="form-control" value="${escapeHtml(tt.instrument_due_date)}" data-uid="${tt._uid}"
          onblur="updateInMemory('${tt._uid}', 'instrument_due_date', this.value)">
      </td>
      <td>
        <select class="form-select ${tt.status === 'ENABLE' ? 'status-enabled' : 'status-disabled'}" 
          onchange="updateInMemory('${tt._uid}', 'status', this.value); this.className = 'form-select ' + (this.value === 'ENABLE' ? 'status-enabled' : 'status-disabled');">
           <option value="ENABLE" ${tt.status === 'ENABLE' ? 'selected' : ''}>Enable</option>
           <option value="DISABLE" ${tt.status === 'DISABLE' ? 'selected' : ''}>Disable</option>
        </select>
      </td>
      <td class="text-center">
         <button type="button" class="btn-icon delete" onclick="deleteRow('${tt._uid}')">
           <i class="fas fa-trash-alt"></i>
         </button>
      </td>
    `;
    return row;
}

window.updateInMemory = function (uid, field, value) {
    const item = instrumentTypes.find(t => t._uid === uid);
    if (item) {
        item[field] = value;
    }
};

window.checkDuplicateSerial = function (input) {
    const val = input.value.trim();
    if (!val) return markError(input, 'Required');

    const uid = input.dataset.uid;
    const item = instrumentTypes.find(t => t._uid === uid);

    // 1. In-memory check
    const existsInMemory = instrumentTypes.some(t => t._uid !== uid && t.instrument_serial_no.trim().toLowerCase() === val.toLowerCase());
    if (existsInMemory) return markError(input, 'Duplicate Serial No (in table)');

    // 2. Database check
    const excludeId = item ? item.instrument_type_id : '';
    fetch(`/api/instrument_type/check-serial/?serial_no=${encodeURIComponent(val)}&exclude_id=${excludeId}`)
        .then(r => r.json())
        .then(res => {
            if (res.success && res.is_duplicate) {
                markError(input, 'Serial No already exists in database');
            } else {
                clearError(input);
            }
        })
        .catch(() => clearError(input));

    return true;
};


window.checkDuplicate = function (input) {
    const val = input.value.trim();
    if (!val) return markError(input, 'Required');

    const uid = input.dataset.uid;
    const exists = instrumentTypes.some(t => t._uid !== uid && t.instrument_name.trim().toLowerCase() === val.toLowerCase());

    if (exists) return markError(input, 'Duplicate Name');

    clearError(input);
    return true;
};

function markError(input, msg) {
    input.classList.add('is-invalid');
    const fb = input.parentNode.querySelector('.invalid-feedback');
    if (fb) { fb.textContent = msg; fb.style.display = 'block'; }
    return false;
}


function clearError(input) {
    input.classList.remove('is-invalid');
    const fb = input.parentNode.querySelector('.invalid-feedback');
    if (fb) { fb.style.display = 'none'; }
    return true;
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// --- Pagination ---

function renderPagination(totalPages, totalItems) {
    const wrapper = document.getElementById('customPagination');
    if (!wrapper) return;
    if (totalItems === 0) {
        wrapper.innerHTML = '';
        return;
    }

    let html = '';

    // Prev
    html += `<button class="pagination-btn prev-btn" ${currentPage === 1 ? 'disabled' : ''} onclick="changePage(${currentPage - 1})">Previous</button>`;

    // Pages
    const maxButtons = 5;
    let startPage = Math.max(1, currentPage - 2);
    let endPage = Math.min(totalPages, startPage + maxButtons - 1);

    if (endPage - startPage < maxButtons - 1) {
        startPage = Math.max(1, endPage - maxButtons + 1);
    }

    if (startPage > 1) {
        html += `<button class="pagination-btn" onclick="changePage(1)">1</button>`;
        if (startPage > 2) html += `<span class="pagination-ellipsis">...</span>`;
    }

    for (let i = startPage; i <= endPage; i++) {
        html += `<button class="pagination-btn ${i === currentPage ? 'active' : ''}" onclick="changePage(${i})">${i}</button>`;
    }

    if (endPage < totalPages) {
        if (endPage < totalPages - 1) html += `<span class="pagination-ellipsis">...</span>`;
        html += `<button class="pagination-btn" onclick="changePage(${totalPages})">${totalPages}</button>`;
    }

    // Next
    html += `<button class="pagination-btn next-btn" ${currentPage >= totalPages ? 'disabled' : ''} onclick="changePage(${currentPage + 1})">Next</button>`;

    // Per Page
    html += `
        <select class="pagination-per-page" onchange="changeItemsPerPage(this.value)">
           <option value="10" ${itemsPerPage === 10 ? 'selected' : ''}>10 / page</option>
           <option value="25" ${itemsPerPage === 25 ? 'selected' : ''}>25 / page</option>
           <option value="50" ${itemsPerPage === 50 ? 'selected' : ''}>50 / page</option>
           <option value="100" ${itemsPerPage === 100 ? 'selected' : ''}>100 / page</option>
        </select>
      `;

    wrapper.innerHTML = html;
}

window.changePage = function (p) {
    currentPage = p;
    localStorage.setItem(PAGE_KEY, currentPage);
    renderTable();
};

window.changeItemsPerPage = function (val) {
    itemsPerPage = parseInt(val);
    localStorage.setItem(PER_PAGE_KEY, itemsPerPage);
    currentPage = 1;
    localStorage.setItem(PAGE_KEY, 1);
    renderTable();
};

// --- Actions ---

window.addRow = function () {
    instrumentTypes.push({
        instrument_type_id: '',
        instrument_name: '',
        instrument_serial_no: '',
        instrument_done_date: '',
        instrument_due_date: '',
        instrument_due_alarm: '',
        status: 'ENABLE',
        _uid: getUid()
    });

    const totalPages = Math.ceil(instrumentTypes.length / itemsPerPage);
    currentPage = totalPages;
    localStorage.setItem(PAGE_KEY, currentPage);
    renderTable();
};

window.deleteRow = function (uid) {
    const index = instrumentTypes.findIndex(t => t._uid === uid);
    if (index === -1) return;

    const item = instrumentTypes[index];

    if (!item.instrument_type_id) {
        instrumentTypes.splice(index, 1);
        renderTable();
    } else {
        DialogManager.confirm({
            title: "Delete Instrument Type?",
            message: `Are you sure you want to delete "${item.instrument_name}"? This action cannot be undone.`,
            confirmText: "Yes, Delete",
            onConfirm: () => {
                DialogManager.loading("Deleting...");
                fetch(`/api/instrument_type/delete/${item.instrument_type_id}/`, {
                    method: "POST",
                    headers: { 'X-CSRFToken': getCsrfToken() }
                })
                    .then(r => r.json())
                    .then(res => {
                        DialogManager.closeLoading();
                        if (res.success) {
                            DialogManager.toast({ type: 'success', message: res.message });
                            instrumentTypes.splice(index, 1);
                            renderTable();
                        } else {
                            DialogManager.toast({ type: 'error', message: res.error || 'Delete failed' });
                        }
                    })
                    .catch(err => {
                        DialogManager.closeLoading();
                        DialogManager.toast({ type: 'error', message: 'Network error' });
                    });
            }
        });
    }
};

window.submitForm = function () {
    if (instrumentTypes.length === 0) {
        return DialogManager.toast({ type: 'warning', message: 'No records to save.' });
    }

    // Validation
    let hasError = false;
    const names = new Set();
    const serials = new Set();

    for (const t of instrumentTypes) {
        const name = (t.instrument_name || '').trim();
        const serial = (t.instrument_serial_no || '').trim();

        if (!name || !serial) {
            hasError = true;
            break;
        }
        if (names.has(name.toLowerCase()) || serials.has(serial.toLowerCase())) {
            hasError = true;
            break;
        }
        names.add(name.toLowerCase());
        serials.add(serial.toLowerCase());
    }

    if (hasError) {
        return DialogManager.toast({ type: 'error', message: 'Validation Errors: Names and Serial Nos are required and must be unique.' });
    }


    DialogManager.loading("Saving...");

    const fd = new FormData();
    instrumentTypes.forEach(t => {
        fd.append('instrument_type_id[]', t.instrument_type_id || ''); // Updated key
        fd.append('instrument_name[]', t.instrument_name.trim());
        fd.append('instrument_serial_no[]', t.instrument_serial_no.trim());
        fd.append('instrument_done_date[]', t.instrument_done_date.trim());
        fd.append('instrument_due_date[]', t.instrument_due_date.trim());
        fd.append('status[]', t.status);
    });

    fetch('/api/instrument_type/save/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCsrfToken() },
        body: fd
    })
        .then(r => r.json())
        .then(res => {
            DialogManager.closeLoading();
            if (res.success) {
                DialogManager.toast({ type: 'success', message: res.message });
                loadInstrumentTypes();
            } else {
                DialogManager.toast({ type: 'error', message: res.error || 'Save failed' });
            }
        })
        .catch(err => {
            DialogManager.closeLoading();
            DialogManager.toast({ type: 'error', message: 'Network error' });
        });
};

function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
}
