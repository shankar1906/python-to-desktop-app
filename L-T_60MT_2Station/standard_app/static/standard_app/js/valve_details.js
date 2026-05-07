// ============================================
// GLOBAL VARIABLES
// ============================================
let currentPage = 1;
let itemsPerPage = 10;
let allData = [];
let originalData = [];
let selectedIds = new Set();
let validator;

// ============================================
// UTILITY FUNCTIONS
// ============================================

function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    if (token) return token.value;
    return window.CSRF_TOKEN || "";
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function dismissHint() {
    const hint = document.getElementById('editHint');
    if (hint) hint.style.display = 'none';
    localStorage.setItem('valveDetailsHintDismissed', 'true');
}

// ============================================
// PAGINATION LOGIC
// ============================================

function initPagination(data) {
    allData = data;
    currentPage = 1;
    renderPagination();
    displayPage();
}

function renderPagination() {
    const totalPages = Math.ceil(allData.length / itemsPerPage);
    const paginationHTML = [];

    paginationHTML.push(`<span class="text-muted small me-3">Total: ${allData.length}</span>`);

    paginationHTML.push(`
        <button class="pagination-btn prev-btn" onclick="goToPage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>
            Previous
        </button>
    `);

    for (let i = 1; i <= totalPages; i++) {
        if (totalPages > 7 && i > 2 && i < totalPages - 1 && Math.abs(i - currentPage) > 1) {
            if (i === 3 || i === totalPages - 2) paginationHTML.push('<span class="pagination-ellipsis">...</span>');
            continue;
        }
        paginationHTML.push(`
            <button class="pagination-btn ${i === currentPage ? 'active' : ''}" onclick="goToPage(${i})">
                ${i}
            </button>
        `);
    }

    paginationHTML.push(`
        <button class="pagination-btn next-btn" onclick="goToPage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>
            Next
        </button>
    `);

    paginationHTML.push(`
        <select class="pagination-per-page" onchange="changeItemsPerPage(this.value)">
            <option value="10" ${itemsPerPage === 10 ? 'selected' : ''}>10 / page</option>
            <option value="25" ${itemsPerPage === 25 ? 'selected' : ''}>25 / page</option>
            <option value="50" ${itemsPerPage === 50 ? 'selected' : ''}>50 / page</option>
        </select>
    `);

    document.getElementById('customPagination').innerHTML = paginationHTML.join('');
}

window.goToPage = function (page) {
    const totalPages = Math.ceil(allData.length / itemsPerPage);
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    displayPage();
    renderPagination();
};

window.changeItemsPerPage = function (value) {
    itemsPerPage = parseInt(value);
    goToPage(1);
};

function displayPage() {
    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const pageData = allData.slice(start, end);

    const tbody = document.getElementById('valveDetailsTableBody');
    tbody.innerHTML = '';

    const checkAll = document.getElementById('checkAll');
    if (checkAll) {
        const currentIds = pageData.map(d => String(d.id));
        checkAll.checked = currentIds.length > 0 && currentIds.every(id => selectedIds.has(id));
    }

    if (pageData.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">No records found</td></tr>';
        return;
    }

    pageData.forEach((item, index) => {
        const tr = document.createElement('tr');
        tr.style.cursor = 'pointer';
        const isChecked = selectedIds.has(String(item.id));
        const statusClass = (item.status || 'Enabled').toLowerCase();

        tr.innerHTML = `
            <td onclick="event.stopPropagation()">
                <input type="checkbox" class="form-check-input detail-checkbox" value="${item.id}" ${isChecked ? 'checked' : ''}>
            </td>
            <td class="text-end pe-3">${start + index + 1}</td>
            <td>${escapeHtml(item.column_name)}</td>
            <td>${escapeHtml(item.data_type)}</td>
            <td><span class="badge ${item.is_mandatory ? 'bg-success' : 'bg-secondary'}">${item.is_mandatory ? 'Yes' : 'No'}</span></td>
            <td><span class="badge ${item.is_top_header ? 'bg-info' : 'bg-secondary'}">${item.is_top_header ? 'Yes' : 'No'}</span></td>
            <td><span class="status-badge ${statusClass}">${escapeHtml(item.status)}</span></td>
        `;

        tr.onclick = () => handleRowInteraction(item);
        tbody.appendChild(tr);
    });

    document.querySelectorAll('.detail-checkbox').forEach(cb => {
        cb.addEventListener('change', function (e) {
            const id = this.value;
            if (this.checked) selectedIds.add(id);
            else selectedIds.delete(id);
            updateBulkDeleteButton();
        });
    });

    updateBulkDeleteButton();
}

// ============================================
// CORE FUNCTIONALITY
// ============================================

function handleRowInteraction(item) {
    DialogManager.confirm({
        title: `Action for "${item.column_name}"`,
        message: 'Choose an action',
        confirmText: 'Update',
        confirmButtonClass: 'dm-btn-info',
        denyText: 'Delete',
        cancelText: 'Cancel',
        onConfirm: () => {
            openEditModal(item);
        },
        onDeny: () => {
            deleteDetail(item.id);
        }
    });
}

function loadValveDetails() {
    fetch('/api/valve_details/')
        .then(response => response.json())
        .then(res => {
            if (res.success) {
                originalData = res.data;
                initPagination(res.data);
            } else {
                DialogManager.toast({ type: 'error', message: res.message });
            }
        })
        .catch(err => {
            console.error(err);
            DialogManager.toast({ type: 'error', message: 'Failed to load details' });
        });
}

window.openAddModal = function () {
    document.getElementById('valveDetailForm').reset();
    document.getElementById('detailId').value = '';
    document.getElementById('modalTitle').textContent = 'Add Valve Detail';
    const btn = document.getElementById('saveBtn');
    btn.textContent = 'Save';
    btn.className = 'btn btn-primary';
    const modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('valveDetailModal'));
    modal.show();
};

function openEditModal(item) {
    document.getElementById('detailId').value = item.id;
    document.getElementById('columnName').value = item.column_name;
    document.getElementById('dataType').value = item.data_type;
    document.getElementById('isMandatory').checked = !!item.is_mandatory;
    document.getElementById('isTopHeader').checked = !!item.is_top_header;
    document.getElementById('status').value = item.status;
    document.getElementById('modalTitle').textContent = 'Edit Valve Detail';
    const btn = document.getElementById('saveBtn');
    btn.textContent = 'Update';
    btn.className = 'btn btn-info text-white';
    const modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('valveDetailModal'));
    modal.show();
}

function deleteDetail(id) {
    DialogManager.confirmAction({
        title: "Delete Column Detail?",
        text: "Are you sure you want to delete this configuration?",
        confirmText: "Yes, Delete",
        url: `/api/valve_details/delete/${id}/`,
        method: "POST",
        onSuccess: () => loadValveDetails()
    });
}

function updateBulkDeleteButton() {
    const btn = document.getElementById('bulkDeleteBtn');
    if (btn) btn.disabled = selectedIds.size === 0;
}

function handleBulkDelete() {
    const ids = Array.from(selectedIds);
    DialogManager.confirmAction({
        title: "Bulk Delete?",
        text: `Are you sure you want to delete ${ids.length} columns?`,
        confirmText: "Yes, Delete",
        url: "/api/valve_details/bulk_delete/",
        method: "POST",
        data: { ids: ids },
        onSuccess: () => {
            selectedIds.clear();
            loadValveDetails();
        }
    });
}

function initSearchToggle() {
    const searchBtn = document.getElementById('searchToggleBtn');
    const wrapper = document.getElementById('searchInputWrapper');
    const input = document.getElementById('customSearchInput');
    const closeBtn = document.getElementById('searchCloseBtn');

    if (!searchBtn || !wrapper || !input || !closeBtn) return;

    searchBtn.onclick = (e) => {
        e.stopPropagation();
        wrapper.classList.add('active');
        searchBtn.classList.add('active');
        setTimeout(() => input.focus(), 300);
    };

    closeBtn.onclick = (e) => {
        e.stopPropagation();
        wrapper.classList.remove('active');
        searchBtn.classList.remove('active');
        input.value = '';
        initPagination(originalData);
    };

    input.onkeyup = () => {
        const q = input.value.toLowerCase().trim();
        if (!q) {
            initPagination(originalData);
            return;
        }
        const filtered = originalData.filter(d =>
            d.column_name.toLowerCase().includes(q) ||
            d.data_type.toLowerCase().includes(q)
        );
        initPagination(filtered);
    };
}

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', function () {
    if (localStorage.getItem('valveDetailsHintDismissed') === 'true') {
        dismissHint();
    }

    loadValveDetails();
    initSearchToggle();

    const checkAll = document.getElementById('checkAll');
    if (checkAll) {
        checkAll.onchange = function () {
            const isChecked = this.checked;
            const pageData = allData.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);
            pageData.forEach(d => {
                if (isChecked) selectedIds.add(String(d.id));
                else selectedIds.delete(String(d.id));
            });
            displayPage();
        };
    }

    const bulkBtn = document.getElementById('bulkDeleteBtn');
    if (bulkBtn) bulkBtn.onclick = handleBulkDelete;

    validator = new FormValidator('valveDetailForm', {
        column_name: {
            rules: [ValidationRules.required],
            asyncRule: (val, signal, form) => new Promise((resolve) => {
                setTimeout(() => {
                    const currentId = form.querySelector('[name="id"]')?.value;
                    const exists = allData.some(item => {
                        // If it's the current record being edited, ignore it
                        if (currentId && String(item.id).trim() === String(currentId).trim()) return false;
                        // Otherwise check if column name matches (case-insensitive and trimmed)
                        return item.column_name?.trim().toLowerCase() === val.trim().toLowerCase();
                    });
                    resolve(exists ? "Column name already exists" : true);
                }, 300);
            })
        },
        data_type: { rules: [ValidationRules.required] },
        status: { rules: [ValidationRules.required] }
    });

    document.getElementById('valveDetailForm').onsubmit = async function (e) {
        e.preventDefault();
        if (!(await validator.validateAll())) return;

        const id = document.getElementById('detailId').value;
        const url = id ? `/api/valve_details/edit/${id}/` : '/api/valve_details/add/';
        const formData = new FormData(this);

        DialogManager.loading('Saving...', 'Please wait');
        fetch(url, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCSRFToken() },
            body: formData
        })
            .then(r => r.json())
            .then(res => {
                DialogManager.closeLoading();
                if (res.success) {
                    DialogManager.toast({ type: 'success', message: res.message });
                    bootstrap.Modal.getInstance(document.getElementById('valveDetailModal')).hide();
                    loadValveDetails();
                } else {
                    DialogManager.toast({ type: 'error', message: res.message });
                }
            })
            .catch(err => {
                DialogManager.closeLoading();
                console.error(err);
                DialogManager.toast({ type: 'error', message: 'Network error' });
            });
    };

    document.getElementById('valveDetailModal').addEventListener('hidden.bs.modal', function () {
        validator.reset();
    });
});
