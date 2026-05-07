// Global State
let masterData = [];
let existingNames = [];
let testTypes = [];
let dataLoaded = false;
let currentPage = 1;
let itemsPerPage = 10;
let selectedIds = new Set();
let SUPERUSER_LEVEL = 0;
let validator;

function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : "";
}

function escapeHtml(text) {
    if (!text) return "";
    return text.toString()
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function dismissHint() {
    const hint = document.getElementById('editHint');
    if (hint) hint.classList.add('hidden');
}

function loadData() {
    const tbody = document.getElementById("valveTableBody");
    if (tbody) {
        tbody.innerHTML = `<tr><td colspan="6" class="text-center py-5 text-muted"><div class="spinner-border text-primary sm" role="status"></div> Loading...</td></tr>`;
    }

    fetch('/api/valve_type/')
        .then(res => res.json())
        .then(data => {
            if (data.error && !Array.isArray(data.valve_types)) {
                if (tbody) tbody.innerHTML = `<tr><td colspan="6" class="text-center text-danger py-5">${data.error}</td></tr>`;
                return;
            }

            masterData = data.valve_types || [];
            testTypes = data.test_types || [];
            existingNames = data.existing_names || masterData.map(v => v.name);
            selectedIds.clear();
            dataLoaded = true;
            renderTestTypeCheckboxes();
            initCustomPagination(masterData);
        })
        .catch(err => {
            console.error(err);
            if (tbody) tbody.innerHTML = `<tr><td colspan="6" class="text-center text-danger py-5">Error loading data.</td></tr>`;
        });
}

function renderTestTypeCheckboxes() {
    const container = document.getElementById('testTypeCheckboxes');
    if (!container) return;
    container.innerHTML = '';

    if (testTypes.length === 0) {
        container.innerHTML = '<div class="col-12 text-muted small">No test types available</div>';
        return;
    }

    testTypes.forEach(tt => {
        const col = document.createElement('div');
        col.className = 'col-md-6 mb-2';
        col.innerHTML = `
           <div class="form-check">
             <input class="form-check-input test-type-check" type="checkbox" value="${tt.id}" id="tt_${tt.id}" name="test_types">
             <label class="form-check-label" for="tt_${tt.id}">
               ${escapeHtml(tt.name)}
             </label>
           </div>
        `;
        container.appendChild(col);
    });
}

function initCustomPagination(data) {
    const savedPage = localStorage.getItem('valveTypePage');
    const totalPages = Math.ceil(data.length / itemsPerPage);

    if (savedPage && !isNaN(savedPage)) {
        currentPage = parseInt(savedPage);
        if (currentPage > totalPages && totalPages > 0) currentPage = totalPages;
        if (currentPage < 1) currentPage = 1;
    } else {
        currentPage = 1;
    }

    renderPagination(data);
    displayPage(currentPage, data);
    updateBulkDeleteButtonState();
}

function renderPagination(data) {
    const totalPages = Math.ceil(data.length / itemsPerPage);
    const paginationWrapper = document.getElementById('customPagination');
    if (!paginationWrapper) return;

    if (data.length === 0) {
        paginationWrapper.innerHTML = '';
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
    paginationWrapper.innerHTML = paginationHTML.join('');
}

function displayPage(page, data) {
    const tbody = document.getElementById("valveTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";
    const selectAllCheckbox = document.getElementById('selectAll');
    const start = (page - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const paginatedItems = data.slice(start, end);

    if (selectAllCheckbox) {
        const allSelected = paginatedItems.length > 0 && paginatedItems.every(item => selectedIds.has(String(item.id)));
        selectAllCheckbox.checked = allSelected;
    }

    updateBulkDeleteButtonState();

    if (data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="text-center text-muted py-4">No valve types found.</td></tr>`;
        return;
    }

    paginatedItems.forEach((item, index) => {
        const globalIndex = start + index + 1;
        const displayId = (SUPERUSER_LEVEL == 2) ? (item.type_id || item.id) : globalIndex;

        let testTypesHtml = '<span class="text-muted small">None</span>';
        if (item.associated_test_types && item.associated_test_types.length > 0) {
            testTypesHtml = item.associated_test_types.map(t => `<span class="badge-test-type">${escapeHtml(t)}</span>`).join('');
        }

        const isChecked = selectedIds.has(String(item.id));
        const status = item.status || 'Enabled';
        const statusClass = status.toLowerCase();
        const statusBadge = `<span class="status-badge ${statusClass}">${escapeHtml(status)}</span>`;

        const tr = document.createElement('tr');
        tr.onclick = (e) => {
            if (e.target.type !== 'checkbox' && !e.target.closest('.row-check') && !e.target.closest('button')) {
                handleRowInteraction(item);
            }
        };

        tr.innerHTML = `
      <td>
         <input type="checkbox" class="row-check" value="${item.id}" ${isChecked ? 'checked' : ''} onclick="event.stopPropagation(); updateBulkDeleteButtonState();">
      </td>
      <td class="text-end fw-bold text-secondary pe-3">${displayId}</td>
      <td class="text-start">${escapeHtml(item.name)}</td>
      <td class="text-muted text-start">${escapeHtml(item.description || "")}</td>
      <td class="text-start">${testTypesHtml}</td>
      <td class="text-start">${statusBadge}</td>
    `;

        const checkbox = tr.querySelector('.row-check');
        checkbox.addEventListener('change', function () {
            const id = this.value;
            if (this.checked) selectedIds.add(id);
            else selectedIds.delete(id);
            if (selectAllCheckbox) {
                const allPage = paginatedItems.every(i => selectedIds.has(String(i.id)));
                selectAllCheckbox.checked = allPage;
            }
            updateBulkDeleteButtonState();
        });
        tbody.appendChild(tr);
    });
    updateBulkDeleteButtonState();
}

function handleRowInteraction(item) {
    DialogManager.confirm({
        title: 'Action for "' + (item.name || 'Unknown') + '"',
        message: 'Choose an action',
        confirmText: 'Update',
        confirmButtonClass: 'dm-btn-info',
        denyText: 'Delete',
        cancelText: 'Cancel',
        onConfirm: () => {
            DialogManager.confirm({
                title: "Edit Valve Type?",
                message: `Are you sure you want to edit ${item.name}?`,
                confirmText: "Yes, Update",
                confirmButtonClass: 'dm-btn-info',
                onConfirm: () => openValveModal('edit', item.type_id)
            });
        },
        onDeny: () => deleteValveType(item.type_id)
    });
}

function deleteValveType(id) {
    DialogManager.confirmAction({
        title: "Delete Valve Type?",
        text: "This action cannot be undone.",
        confirmText: "Yes, Delete",
        url: `/api/valve_type/delete/${id}/`,
        method: "POST",
        onSuccess: () => loadData()
    });
}

window.goToPage = function (page) {
    currentPage = page;
    localStorage.setItem('valveTypePage', page);
    window.triggerFilter();
};

window.changeItemsPerPage = function (select) {
    itemsPerPage = parseInt(select.value);
    window.goToPage(1);
};

function getFilteredData() {
    const searchValue = document.getElementById('customSearchInput').value.toLowerCase().trim();
    if (!searchValue) return masterData;
    return masterData.filter(item => {
        const text = [
            item.name,
            item.description,
            (item.associated_test_types || []).join(' ')
        ].join(' ').toLowerCase();
        return text.includes(searchValue);
    });
}

window.triggerFilter = function () {
    const filtered = getFilteredData();
    renderPagination(filtered);
    displayPage(currentPage, filtered);
};

function initSearchToggle() {
    const searchToggleBtn = document.getElementById('searchToggleBtn');
    const searchInputWrapper = document.getElementById('searchInputWrapper');
    const searchInput = document.getElementById('customSearchInput');
    const searchCloseBtn = document.getElementById('searchCloseBtn');
    if (!searchToggleBtn || !searchInputWrapper || !searchInput || !searchCloseBtn) return;

    searchToggleBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (!searchInputWrapper.classList.contains('active')) {
            searchInputWrapper.classList.add('active');
            setTimeout(() => searchInput.focus(), 300);
        }
    });

    searchCloseBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        searchInput.value = '';
        window.triggerFilter();
        searchInputWrapper.classList.remove('active');
    });

    document.addEventListener('click', (e) => {
        if (!searchInputWrapper.contains(e.target) && !searchToggleBtn.contains(e.target) && searchInputWrapper.classList.contains('active')) {
            searchInputWrapper.classList.remove('active');
            searchInput.value = '';
            window.triggerFilter();
        }
    });
}

window.toggleSelectAll = function () {
    const selectAll = document.getElementById('selectAll');
    if (!selectAll) return;
    const isChecked = selectAll.checked;
    document.querySelectorAll('#valveTableBody .row-check').forEach(c => {
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
    if (btn) btn.disabled = count === 0;
}

window.handleBulkDelete = function () {
    const ids = Array.from(selectedIds);
    if (ids.length === 0) return;
    DialogManager.confirmAction({
        title: "Delete?",
        text: `Delete ${ids.length} valve type(s)?`,
        confirmText: "Yes, Delete",
        url: "/api/valve_type/bulk_delete/",
        method: "POST",
        data: { ids: ids },
        onSuccess: () => {
            selectedIds.clear();
            loadData();
        }
    });
};

window.openValveModal = function (mode, id = null) {
    const title = document.getElementById('valveModalTitle');
    const submitBtn = document.getElementById('submitBtn');
    const modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('valveModal'));
    if (validator) validator.reset();

    if (mode === 'add') {
        title.textContent = "Add Valve Type";
        submitBtn.textContent = "Save";
        submitBtn.className = "btn btn-success";
        document.getElementById('valveId').value = "";
        document.getElementById('valveName').value = "";
        document.getElementById('valveDesc').value = "";
        document.getElementById('status').value = "";
        document.querySelectorAll('.test-type-check').forEach(c => c.checked = false);
        modal.show();
    } else {
        title.textContent = "Edit Valve Type";
        submitBtn.textContent = "Update";
        submitBtn.className = "btn btn-info";
        const item = masterData.find(d => d.type_id == id);
        if (!item) return;
        document.getElementById('valveId').value = item.type_id;
        document.getElementById('valveName').value = item.name;
        document.getElementById('valveDesc').value = item.description || '';
        document.getElementById('status').value = item.status || 'Enabled';
        document.querySelectorAll('.test-type-check').forEach(c => c.checked = false);
        if (item.selected_test_type_ids) {
            item.selected_test_type_ids.forEach(tid => {
                const cb = document.getElementById(`tt_${tid}`);
                if (cb) cb.checked = true;
            });
        }
        modal.show();
    }
};

document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.table-container-wrapper');
    if (container) {
        SUPERUSER_LEVEL = parseInt(container.dataset.superuserLevel) || 0;
    }

    loadData();
    initSearchToggle();

    validator = new FormValidator('valveForm', {
        name: {
            rules: [ValidationRules.required],
            asyncRule: (val, signal, form) => new Promise((resolve) => {
                setTimeout(() => {
                    const currentId = form.querySelector('[name="valve_id"]')?.value;
                    const exists = masterData.some(item => {
                        if (currentId && item.type_id == currentId) return false;
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

    const modalEl = document.getElementById('valveModal');
    if (modalEl) {
        modalEl.addEventListener('hidden.bs.modal', function () {
            document.getElementById('valveForm').reset();
            document.getElementById('valveId').value = '';
            if (validator) validator.reset();
            document.querySelectorAll('.test-type-check').forEach(c => c.checked = false);
        });
    }

    const form = document.getElementById('valveForm');
    if (form) {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();
            const isValid = await validator.validateAll();
            if (!isValid) return;

            const selectedChecks = document.querySelectorAll('.test-type-check:checked');
            if (selectedChecks.length === 0) {
                const err = document.getElementById('testTypeError');
                if (err) err.textContent = 'Select at least one test type.';
                return;
            }

            const id = document.getElementById('valveId').value;
            const data = {
                name: document.getElementById('valveName').value.trim(),
                description: document.getElementById('valveDesc').value.trim(),
                test_types: Array.from(selectedChecks).map(c => parseInt(c.value)),
                status: document.getElementById('status').value.trim()
            };

            DialogManager.loading("Saving...", "Please wait");
            const url = id ? `/api/valve_type/edit/${id}/` : `/api/valve_type/add/`;
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify(data)
            })
                .then(r => r.json())
                .then(res => {
                    DialogManager.closeLoading();
                    if (res.success) {
                        DialogManager.toast({ type: 'success', message: res.message || "Success!" });
                        const modal = bootstrap.Modal.getInstance(document.getElementById('valveModal'));
                        if (modal) modal.hide();
                        loadData();
                    } else {
                        DialogManager.toast({ type: 'error', message: res.error || "Error saving." });
                    }
                })
                .catch(err => {
                    DialogManager.closeLoading();
                    console.error(err);
                    DialogManager.toast({ type: 'error', message: "Server error." });
                });
        });
    }
});
