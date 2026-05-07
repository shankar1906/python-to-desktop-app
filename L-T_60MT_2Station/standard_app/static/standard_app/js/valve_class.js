// Global State
let masterData = [];
let existingNames = [];
let selectedIds = new Set();
let validator;
let currentPage = 1;
let itemsPerPage = 10;
let SUPERUSER_LEVEL = 0;

function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : "";
}

function escapeHtml(text) {
    if (!text) return "";
    return text.toString().replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}

function dismissHint() {
    const hint = document.getElementById('editHint');
    if (hint) hint.style.display = 'none';
}

function loadData() {
    fetch('/api/valve_class/')
        .then(r => r.json())
        .then(data => {
            if (data.error && !Array.isArray(data.valve_classes)) {
                DialogManager.toast({ type: 'error', message: data.error });
                return;
            }
            masterData = data.valve_classes || [];
            existingNames = data.existing_names || (masterData.map(c => c.name));
            selectedIds.clear();
            triggerFilter();
        })
        .catch(err => {
            console.error(err);
            DialogManager.toast({ type: 'error', message: 'Failed to load valve classes.' });
        });
}

function displayPage(page, data) {
    const tbody = document.getElementById('valveClassTableBody');
    if (!tbody) return;
    tbody.innerHTML = '';

    const start = (page - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const pageData = data.slice(start, end);

    const selectAllCheckbox = document.getElementById('selectAll');
    if (selectAllCheckbox) {
        const allSelected = pageData.length > 0 && pageData.every(item => selectedIds.has(String(item.class_id)));
        selectAllCheckbox.checked = allSelected;
    }

    if (data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="text-center py-4 text-muted">No records found</td></tr>`;
        return;
    }

    pageData.forEach((item, index) => {
        const globalIndex = start + index + 1;
        const displayId = (SUPERUSER_LEVEL == 2) ? item.class_id : globalIndex;
        const desc = item.description || '';
        const status = item.status || 'Enabled';
        const isChecked = selectedIds.has(String(item.class_id));

        const statusClass = status.toLowerCase();
        const statusBadge = `<span class="status-badge ${statusClass}">${escapeHtml(status)}</span>`;

        const tr = document.createElement('tr');
        tr.onclick = (e) => {
            if (e.target.closest('input') || e.target.closest('button')) return;
            handleRowInteraction(item);
        };

        let checkboxHtml = '';
        if (SUPERUSER_LEVEL == 2) {
            checkboxHtml = `<td class="text-center">
         <input type="checkbox" class="row-check" value="${item.class_id}" ${isChecked ? 'checked' : ''} onclick="event.stopPropagation()">
      </td>`;
        }

        tr.innerHTML = `
      ${checkboxHtml}
      <td class="fw-bold text-danger small text-end pe-3">${displayId}</td>
      <td class="fw-bold text-dark text-start">${escapeHtml(item.name)}</td>
      <td class="text-muted small text-start">${escapeHtml(desc)}</td>
      <td class="text-start">${statusBadge}</td>
    `;

        if (SUPERUSER_LEVEL == 2) {
            const checkbox = tr.querySelector('.row-check');
            checkbox.addEventListener('change', function () {
                const id = this.value;
                if (this.checked) selectedIds.add(id);
                else selectedIds.delete(id);
                updateBulkDeleteButtonState();
                if (selectAllCheckbox) {
                    const allPageSelected = pageData.every(i => selectedIds.has(String(i.class_id)));
                    selectAllCheckbox.checked = allPageSelected;
                }
            });
        }
        tbody.appendChild(tr);
    });
    updateBulkDeleteButtonState();
}

function getFilteredData() {
    const searchVal = document.getElementById('customSearchInput').value.toLowerCase().trim();
    if (!searchVal) return masterData;
    return masterData.filter(item => {
        const text = (item.name + ' ' + (item.description || '')).toLowerCase();
        return text.includes(searchVal);
    });
}

window.triggerFilter = function () {
    const filtered = getFilteredData();
    const total = Math.ceil(filtered.length / itemsPerPage);
    if (currentPage > total) currentPage = Math.max(1, total);
    renderPagination(filtered);
    displayPage(currentPage, filtered);
};

function initCustomPaginationFromStorage() {
    const stored = localStorage.getItem('valveClassPage');
    if (stored) currentPage = parseInt(stored) || 1;
}

window.goToPage = function (p) {
    currentPage = p;
    localStorage.setItem('valveClassPage', p);
    window.triggerFilter();
};

window.changeItemsPerPage = function (sel) {
    itemsPerPage = parseInt(sel.value);
    window.goToPage(1);
};

function renderPagination(data) {
    const totalPages = Math.ceil(data.length / itemsPerPage);
    const container = document.getElementById('customPagination');
    if (!container) return;
    if (data.length === 0) {
        container.innerHTML = '';
        return;
    }

    const paginationHTML = [];
    paginationHTML.push(`<span class="text-muted small me-3">Total: ${data.length}</span>`);
    paginationHTML.push(`
    <button class="pagination-btn prev-btn" onclick="goToPage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>
      Previous
    </button>
  `);

    if (totalPages <= 7) {
        for (let i = 1; i <= totalPages; i++) {
            paginationHTML.push(`
        <button class="pagination-btn ${i === currentPage ? 'active' : ''}" onclick="goToPage(${i})">${i}</button>
      `);
        }
    } else {
        paginationHTML.push(`<button class="pagination-btn ${currentPage === 1 ? 'active' : ''}" onclick="goToPage(1)">1</button>`);
        if (currentPage > 3) paginationHTML.push('<span class="pagination-ellipsis">...</span>');
        let start = Math.max(2, currentPage - 1);
        let end = Math.min(totalPages - 1, currentPage + 1);
        for (let i = start; i <= end; i++) {
            paginationHTML.push(`<button class="pagination-btn ${i === currentPage ? 'active' : ''}" onclick="goToPage(${i})">${i}</button>`);
        }
        if (currentPage < totalPages - 2) paginationHTML.push('<span class="pagination-ellipsis">...</span>');
        paginationHTML.push(`<button class="pagination-btn ${currentPage === totalPages ? 'active' : ''}" onclick="goToPage(${totalPages})">${totalPages}</button>`);
    }

    paginationHTML.push(`
    <button class="pagination-btn next-btn" onclick="goToPage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>
      Next
    </button>
  `);

    paginationHTML.push(`
    <select class="pagination-per-page" onchange="changeItemsPerPage(this)">
      <option value="10" ${itemsPerPage === 10 ? 'selected' : ''}>10 / page</option>
      <option value="25" ${itemsPerPage === 25 ? 'selected' : ''}>25 / page</option>
      <option value="50" ${itemsPerPage === 50 ? 'selected' : ''}>50 / page</option>
      <option value="100" ${itemsPerPage === 100 ? 'selected' : ''}>100 / page</option>
    </select>
  `);
    container.innerHTML = paginationHTML.join('');
}

function handleRowInteraction(item) {
    const options = {
        title: 'Action for "' + (item.name || 'Unknown') + '"',
        message: 'Choose an action',
        confirmText: 'Update',
        confirmButtonClass: 'dm-btn-info',
        cancelText: 'Cancel',
        onConfirm: () => {
            DialogManager.confirm({
                title: "Edit Valve Class?",
                message: "Do you want to edit this valve class?",
                confirmText: "Yes, Update",
                confirmButtonClass: 'dm-btn-info',
                onConfirm: () => openClassModal('edit', item.class_id)
            });
        }
    };

    if (SUPERUSER_LEVEL == 2) {
        options.denyText = 'Delete';
        options.onDeny = () => deleteValveClass(item.class_id);
    }
    DialogManager.confirm(options);
}

function deleteValveClass(id) {
    DialogManager.confirmAction({
        title: "Delete Valve Class?",
        text: "This action cannot be undone.",
        confirmText: "Yes, Delete",
        url: `/api/valve_class/delete/${id}/`,
        method: "POST",
        onSuccess: () => loadData()
    });
}

window.toggleSelectAll = function () {
    const selectAllCheckbox = document.getElementById('selectAll');
    if (!selectAllCheckbox) return;
    const isChecked = selectAllCheckbox.checked;
    document.querySelectorAll('#valveClassTableBody .row-check').forEach(c => {
        c.checked = isChecked;
        const id = c.value;
        if (isChecked) selectedIds.add(id);
        else selectedIds.delete(id);
    });
    updateBulkDeleteButtonState();
};

function updateBulkDeleteButtonState() {
    const count = selectedIds.size;
    const btn = document.getElementById('bulkDeleteBtn');
    if (btn) btn.disabled = (count === 0);
}

window.handleBulkDelete = function () {
    const ids = Array.from(selectedIds);
    if (ids.length === 0) return;
    DialogManager.confirmAction({
        title: "Delete?",
        text: `Are you sure you want to delete ${ids.length} item(s)?`,
        confirmText: "Yes, Delete All",
        url: "/api/valve_class/bulk_delete/",
        method: "POST",
        data: { ids: ids },
        onSuccess: () => {
            selectedIds.clear();
            loadData();
        }
    });
};

window.openClassModal = function (mode, id = null) {
    const form = document.getElementById('valveClassForm');
    if (!form) return;
    if (validator) validator.reset();
    else form.reset();

    const title = document.getElementById('valveClassModalTitle');
    const submit = document.getElementById('submitBtn');
    const modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('valveClassModal'));

    if (mode === 'add') {
        title.textContent = "Add Valve Class";
        submit.textContent = "Save";
        submit.className = "btn btn-success px-4";
        document.getElementById('classId').value = "";
        document.getElementById('classIdInput').value = "";
        modal.show();
    } else {
        title.textContent = "Edit Valve Class";
        submit.textContent = "Update";
        submit.className = "btn btn-info px-4";
        const item = masterData.find(x => x.class_id == id);
        if (!item) return;
        document.getElementById('classId').value = item.class_id;
        document.getElementById('classIdInput').value = item.class_id;
        document.getElementById('className').value = item.name;
        document.getElementById('classDesc').value = item.description || '';
        document.getElementById('status').value = item.status || 'Enabled';
        modal.show();
    }
};

function initSearchToggle() {
    const wrap = document.getElementById('searchInputWrapper');
    const toggle = document.getElementById('searchToggleBtn');
    const close = document.getElementById('searchCloseBtn');
    const inp = document.getElementById('customSearchInput');
    if (!wrap || !toggle || !close || !inp) return;

    toggle.onclick = (e) => {
        e.stopPropagation();
        if (!wrap.classList.contains('active')) {
            wrap.classList.add('active');
            setTimeout(() => inp.focus(), 300);
        }
    };

    close.onclick = (e) => {
        e.stopPropagation();
        inp.value = '';
        window.triggerFilter();
        wrap.classList.remove('active');
    };

    document.addEventListener('click', (e) => {
        if (!wrap.contains(e.target) && !toggle.contains(e.target) && wrap.classList.contains('active')) {
            inp.value = '';
            window.triggerFilter();
            wrap.classList.remove('active');
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.table-container-wrapper');
    if (container) {
        SUPERUSER_LEVEL = parseInt(container.dataset.superuserLevel) || 0;
    }

    loadData();
    initSearchToggle();
    initCustomPaginationFromStorage();

    validator = new FormValidator('valveClassForm', {
        class_id_input: {
            rules: [ValidationRules.required],
            asyncRule: (val, signal, form) => new Promise((resolve) => {
                if (!val || val.trim() === '') { resolve(true); return; }
                setTimeout(() => {
                    const currentId = form.querySelector('[name="class_id"]')?.value;
                    const exists = masterData.some(item => {
                        if (currentId && item.class_id == currentId) return false;
                        return item.class_id == val;
                    });
                    resolve(exists ? "Class ID already exists" : true);
                }, 300);
            })
        },
        name: {
            rules: [ValidationRules.required],
            asyncRule: (val, signal, form) => new Promise((resolve) => {
                if (!val || val.trim() === '') { resolve(true); return; }
                setTimeout(() => {
                    const currentId = form.querySelector('[name="class_id"]')?.value;
                    const exists = masterData.some(item => {
                        if (currentId && item.class_id == currentId) return false;
                        return item.name?.toLowerCase() === val.toLowerCase();
                    });
                    resolve(exists ? "Name already exists" : true);
                }, 300);
            })
        },
        status: {
            rules: [ValidationRules.required]
        }
    });

    const form = document.getElementById('valveClassForm');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const id = document.getElementById('classId').value;
            const classIdInput = document.getElementById('classIdInput').value.trim();
            const name = document.getElementById('className').value.trim();
            const desc = document.getElementById('classDesc').value.trim();
            const status = document.getElementById('status').value.trim();

            if (!classIdInput) {
                document.getElementById('classIdInput').classList.add('is-invalid');
                document.getElementById('classIdError').textContent = 'Class ID is required.';
                return;
            }

            DialogManager.loading("Saving...", "Please wait");
            const url = id ? `/api/valve_class/edit/${id}/` : `/api/valve_class/add/`;
            const formData = new FormData();
            formData.append('class_id', classIdInput);
            formData.append('name', name);
            formData.append('description', desc);
            formData.append('status', status);

            fetch(url, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCSRFToken() },
                body: formData
            })
                .then(r => r.json())
                .then(res => {
                    DialogManager.closeLoading();
                    if (res.success) {
                        DialogManager.toast({ type: 'success', message: 'Saved successfully.' });
                        const modal = bootstrap.Modal.getInstance(document.getElementById('valveClassModal'));
                        if (modal) modal.hide();
                        loadData();
                    } else {
                        DialogManager.toast({ type: 'error', message: res.error || 'Error saving data.' });
                    }
                })
                .catch(err => {
                    DialogManager.closeLoading();
                    console.error(err);
                    DialogManager.toast({ type: 'error', message: 'Server error.' });
                });
        });
    }
});
