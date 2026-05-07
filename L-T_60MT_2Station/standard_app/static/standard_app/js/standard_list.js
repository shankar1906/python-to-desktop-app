// ============================================
// GLOBAL VARIABLES
// ============================================
let SUPERUSER_LEVEL = 0;

// ============================================
// UTILITY FUNCTIONS
// ============================================

/** Get CSRF token from form*/
function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : "";
}

/** Escape HTML to prevent XSS */
function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

/*** Escape JavaScript strings */
function escapeJs(text) {
    return String(text)
        .replace(/\\/g, "\\\\")
        .replace(/'/g, "\\'")
        .replace(/"/g, '\\"')
        .replace(/\n/g, "\\n")
        .replace(/\r/g, "\\r");
}

/** Dismiss hint box */
function dismissHint() {
    document.getElementById('editHint').classList.add('hidden');
}

/** Update bulk delete button state based on checkbox selection */
function updateBulkDeleteButtonState() {
    const bulkDeleteBtn = document.getElementById('bulkDeleteBtn');
    const checkedBoxes = document.querySelectorAll('.row-check:checked');
    if (bulkDeleteBtn) {
        bulkDeleteBtn.disabled = checkedBoxes.length === 0;
    }
}

/** Custom Pagination Variables and Functions */
let currentPage = 1;
let itemsPerPage = 10;
let allData = [];
let selectedIds = new Set();
let originalStandardsData = [];
let validator;

function initCustomPagination(data) {
    allData = data;
    // Restore page persistence
    const savedPage = localStorage.getItem('standardListPage');
    if (savedPage && !isNaN(savedPage)) {
        currentPage = parseInt(savedPage);
        const totalPages = Math.ceil(data.length / itemsPerPage);
        if (currentPage > totalPages && totalPages > 0) currentPage = totalPages;
        if (currentPage < 1) currentPage = 1;
    } else {
        currentPage = 1;
    }

    renderPagination();
    displayPage();
}

function renderPagination() {
    const totalPages = Math.ceil(allData.length / itemsPerPage);
    const paginationHTML = [];

    // Total count
    paginationHTML.push(`<span class="text-muted small me-3">Total: ${allData.length}</span>`);

    // Previous button
    paginationHTML.push(`
    <button class="pagination-btn prev-btn" onclick="goToPage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>
      Previous
    </button>
  `);

    // Page numbers
    if (totalPages <= 7) {
        for (let i = 1; i <= totalPages; i++) {
            paginationHTML.push(`
        <button class="pagination-btn ${i === currentPage ? 'active' : ''}" onclick="goToPage(${i})">
          ${i}
        </button>
      `);
        }
    } else {
        // Always show first page
        paginationHTML.push(`
      <button class="pagination-btn ${currentPage === 1 ? 'active' : ''}" onclick="goToPage(1)">
        1
      </button>
    `);

        if (currentPage > 3) {
            paginationHTML.push('<span class="pagination-ellipsis">...</span>');
        }

        // Show pages around current
        let start = Math.max(2, currentPage - 1);
        let end = Math.min(totalPages - 1, currentPage + 1);

        for (let i = start; i <= end; i++) {
            paginationHTML.push(`
        <button class="pagination-btn ${i === currentPage ? 'active' : ''}" onclick="goToPage(${i})">
          ${i}
        </button>
      `);
        }

        if (currentPage < totalPages - 2) {
            paginationHTML.push('<span class="pagination-ellipsis">...</span>');
        }

        // Always show last page
        paginationHTML.push(`
      <button class="pagination-btn ${currentPage === totalPages ? 'active' : ''}" onclick="goToPage(${totalPages})">
        ${totalPages}
      </button>
    `);
    }

    // Next button
    paginationHTML.push(`
    <button class="pagination-btn next-btn" onclick="goToPage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>
      Next
    </button>
  `);

    // Items per page dropdown
    paginationHTML.push(`
    <select class="pagination-per-page" onchange="changeItemsPerPage(this.value)">
      <option value="10" ${itemsPerPage === 10 ? 'selected' : ''}>10 / page</option>
      <option value="25" ${itemsPerPage === 25 ? 'selected' : ''}>25 / page</option>
      <option value="50" ${itemsPerPage === 50 ? 'selected' : ''}>50 / page</option>
      <option value="100" ${itemsPerPage === 100 ? 'selected' : ''}>100 / page</option>
    </select>
  `);

    document.getElementById('customPagination').innerHTML = paginationHTML.join('');
}

// Make pagination functions global
window.goToPage = function (page) {
    const totalPages = Math.ceil(allData.length / itemsPerPage);
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    localStorage.setItem('standardListPage', page);
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

    const tbody = document.getElementById("standardsTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    // Setup Select All Checkbox for current page
    const selectAllCheckbox = document.getElementById("selectAll");
    if (selectAllCheckbox) {
        const newSelectAll = selectAllCheckbox.cloneNode(true);
        selectAllCheckbox.parentNode.replaceChild(newSelectAll, selectAllCheckbox);

        const currentIds = pageData.map(d => String(d.standard_id));
        const allSelected = currentIds.length > 0 && currentIds.every(id => selectedIds.has(id));
        newSelectAll.checked = allSelected;

        newSelectAll.addEventListener("change", function () {
            const isChecked = this.checked;
            document.querySelectorAll(".row-check").forEach(ch => {
                ch.checked = isChecked;
                const id = ch.dataset.id;
                if (isChecked) {
                    selectedIds.add(id);
                } else {
                    selectedIds.delete(id);
                }
            });
            updateBulkDeleteButton();
        });
    }

    if (pageData.length > 0) {
        pageData.forEach((standard, index) => {
            const row = document.createElement("tr");
            row.dataset.standard_id = standard.standard_id;
            row.dataset.name = standard.name;
            row.dataset.description = standard.description || "";
            row.dataset.status = standard.status || "Enabled";

            const isChecked = selectedIds.has(String(standard.standard_id));
            const statusClass = (standard.status || 'Enabled').toLowerCase();
            const statusBadge = `<span class="status-badge ${statusClass}">${escapeHtml(standard.status || 'Enabled')}</span>`;

            const displayId = (SUPERUSER_LEVEL == 2) ? standard.standard_id : (start + index + 1);

            row.innerHTML = `
        <td onclick="event.stopPropagation()">
          <input type="checkbox" class="row-check" data-id="${standard.standard_id}" ${isChecked ? 'checked' : ''}>
        </td>
        <td class="text-end pe-3">${displayId}</td>
        <td class="text-start">${escapeHtml(standard.name)}</td>
        <td class="text-start">${escapeHtml(standard.description || "")}</td>
        <td class="text-start">${statusBadge}</td>
      `;

            row.onclick = function (e) {
                if (e.target.type !== 'checkbox' && !e.target.closest('.row-check')) {
                    handleRowInteraction({
                        standard_id: standard.standard_id,
                        name: standard.name,
                        description: standard.description,
                        status: standard.status
                    });
                }
            };

            tbody.appendChild(row);
        });

        document.querySelectorAll(".row-check").forEach(checkbox => {
            checkbox.addEventListener("change", function () {
                const id = this.dataset.id;
                if (this.checked) {
                    selectedIds.add(id);
                } else {
                    selectedIds.delete(id);
                }

                const selectAll = document.getElementById("selectAll");
                if (selectAll) {
                    const currentIds = pageData.map(d => String(d.standard_id));
                    const allSelected = currentIds.length > 0 && currentIds.every(id => selectedIds.has(id));
                    selectAll.checked = allSelected;
                }

                updateBulkDeleteButton();
            });
        });

    } else {
        tbody.innerHTML = `<tr><td colspan="5" class="text-center">No standards found</td></tr>`;
    }

    updateBulkDeleteButton();
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
                title: 'Edit Standard?',
                message: 'Are you sure you want to edit "' + (item.name || 'Unknown') + '"?',
                confirmText: 'Yes, Update',
                confirmButtonClass: 'dm-btn-info',
                cancelText: 'Cancel',
                onConfirm: () => {
                    showEditModalInternal(item.standard_id, item.name, item.description, item.status);
                }
            });
        },
        onDeny: () => {
            deleteStandard(item.standard_id);
        }
    });
}

function deleteStandard(id) {
    DialogManager.confirmAction({
        title: "Delete Standard?",
        text: "Are you sure you want to delete this standard?",
        confirmText: "Yes, Delete",
        cancelText: "Cancel",
        url: `/api/standards/delete/${id}/`,
        method: "POST",
        data: null,
        reverseButtons: true,
        allowOutsideClick: false,
        onSuccess: () => loadStandards(),
        onError: (response) => {
            console.error("Error deleting standard:", response);
        }
    });
}

/** Initialize search functionality */
function initSearchToggle() {
    const searchToggleBtn = document.getElementById('searchToggleBtn');
    const searchInputWrapper = document.getElementById('searchInputWrapper');
    const searchInput = document.getElementById('customSearchInput');
    const searchCloseBtn = document.getElementById('searchCloseBtn');

    if (!searchToggleBtn || !searchInputWrapper || !searchInput || !searchCloseBtn) return;

    searchToggleBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        if (!searchInputWrapper.classList.contains('active')) {
            searchInputWrapper.classList.add('active');
            searchToggleBtn.classList.add('active');
            setTimeout(() => searchInput.focus(), 300);
        }
    });

    searchCloseBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        searchInputWrapper.classList.remove('active');
        searchToggleBtn.classList.remove('active');
        searchInput.value = '';
        initCustomPagination(originalStandardsData);
    });

    searchInput.addEventListener('keyup', function () {
        const query = this.value.toLowerCase().trim();
        if (!query) {
            initCustomPagination(originalStandardsData);
            return;
        }
        const filtered = originalStandardsData.filter(item =>
            (item.name && item.name.toLowerCase().includes(query)) ||
            (item.description && item.description.toLowerCase().includes(query))
        );
        initCustomPagination(filtered);
    });

    searchInputWrapper.addEventListener('click', function (e) {
        e.stopPropagation();
    });

    document.addEventListener('click', function (e) {
        if (!searchInputWrapper.contains(e.target) && !searchToggleBtn.contains(e.target) && searchInputWrapper.classList.contains('active')) {
            searchInputWrapper.classList.remove('active');
            searchToggleBtn.classList.remove('active');
            searchInput.value = '';
            initCustomPagination(originalStandardsData);
        }
    });
}

/** Load all standards from API and populate table */
function loadStandards() {
    fetch("/api/standards/")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showTableError(data.error);
                return;
            }

            if (data.standards && data.standards.length > 0) {
                selectedIds.clear();
                originalStandardsData = data.standards;
                initCustomPagination(data.standards);
            } else {
                const tbody = document.getElementById("standardsTableBody");
                if (tbody) tbody.innerHTML = `<tr><td colspan="5" class="text-center">No standards found</td></tr>`;
                const pag = document.getElementById('customPagination');
                if (pag) pag.innerHTML = '';
            }

            const actions = document.getElementById('tableActionButtons');
            if (actions) {
                actions.innerHTML = `
          <button class="bulk-delete-btn" id="bulkDeleteBtn" disabled>
            <i class="fas fa-trash-alt"></i> Delete
          </button>
        `;
                document.getElementById('bulkDeleteBtn').addEventListener('click', handleBulkDelete);
            }

            const actionsAdd = document.getElementById('tableActionButtons-add');
            if (actionsAdd) {
                actionsAdd.innerHTML = `
          <button class="master-add-btn" onclick="openAddModal()">
            <i class="fas fa-plus"></i> Add
          </button>
        `;
            }
        })
        .catch(error => {
            console.error("Error loading standards:", error);
            showTableError("Error loading standards. Please refresh the page.");
        });
}

function showTableError(message) {
    const tbody = document.getElementById("standardsTableBody");
    if (tbody) tbody.innerHTML = `<tr><td colspan="5" class="text-center text-danger">${message}</td></tr>`;
}

function updateBulkDeleteButton() {
    const selectedCount = selectedIds.size;
    const btn = document.getElementById("bulkDeleteBtn");
    if (btn) {
        btn.disabled = selectedCount === 0;
    }
}

function handleBulkDelete() {
    const selected = Array.from(selectedIds);
    if (selected.length === 0) {
        return DialogManager.toast({ type: 'warning', message: 'No items selected.' });
    }
    DialogManager.confirmAction({
        title: "Delete Standards?",
        text: `Delete ${selected.length} standard${selected.length > 1 ? 's' : ''}? This cannot be undone.`,
        confirmText: "Yes, Delete",
        url: "/api/standards/bulk_delete/",
        method: "POST",
        data: { ids: selected },
        onSuccess: () => {
            selectedIds.clear();
            loadStandards();
        }
    });
}

window.openAddModal = function () {
    document.getElementById("standardId").value = "";
    document.getElementById("addName").value = "";
    document.getElementById("addDesc").value = "";
    document.getElementById("addStatus").value = "";
    document.getElementById("standardModalTitle").textContent = "Add Standard";
    const btn = document.getElementById("standardSubmitBtn");
    btn.textContent = "Save";
    btn.className = "btn btn-success";
    const modal = bootstrap.Modal.getOrCreateInstance(document.getElementById("standardModal"));
    modal.show();
};

function showEditModalInternal(id, name, desc, status) {
    document.getElementById("standardId").value = id;
    document.getElementById("addName").value = name;
    document.getElementById("addDesc").value = desc || "";
    document.getElementById("addStatus").value = status || "Enabled";
    document.getElementById("standardModalTitle").textContent = "Edit Standard";
    const btn = document.getElementById("standardSubmitBtn");
    btn.textContent = "Update";
    btn.className = "btn btn-info";
    const modal = bootstrap.Modal.getOrCreateInstance(document.getElementById("standardModal"));
    modal.show();
}

window.dismissHint = function () {
    const hint = document.getElementById('editHint');
    if (hint) hint.classList.add('hidden');
};

document.addEventListener('DOMContentLoaded', function () {
    const wrapper = document.querySelector('.table-container-wrapper');
    if (wrapper) {
        SUPERUSER_LEVEL = parseInt(wrapper.dataset.superuserLevel) || 0;
    }

    if (localStorage.getItem('standardHintDismissed') === 'true') {
        const hint = document.getElementById('editHint');
        if (hint) hint.classList.add('hidden');
    }

    loadStandards();
    initSearchToggle();

    validator = new FormValidator('standardForm', {
        name: {
            rules: [ValidationRules.required],
            asyncRule: (val, signal, form) => new Promise((resolve) => {
                setTimeout(() => {
                    const currentId = form.querySelector('[name="standard_id"]')?.value;
                    const exists = allData.some(item => {
                        // If it's the current record being edited, ignore it
                        if (currentId && String(item.standard_id).trim() === String(currentId).trim()) return false;
                        // Otherwise check if name matches (case-insensitive and trimmed)
                        return item.name?.trim().toLowerCase() === val.trim().toLowerCase();
                    });
                    resolve(exists ? "Standard name already exists" : true);
                }, 300);
            })
        },
        status: {
            rules: [ValidationRules.required]
        }
    });

    document.getElementById('standardForm').addEventListener('submit', async function (e) {
        e.preventDefault();
        const isValid = await validator.validateAll();
        if (!isValid) return;

        const id = document.getElementById('standardId').value;
        const name = document.getElementById('addName').value.trim();
        const description = document.getElementById('addDesc').value.trim();
        const status = document.getElementById('addStatus').value.trim();

        DialogManager.loading('Saving...', 'Please wait');
        const url = id ? `/api/standards/edit/${id}/` : '/api/standards/add/';
        const formData = new FormData();
        formData.append('name', name);
        formData.append('description', description);
        formData.append('status', status);

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            body: formData
        })
            .then(r => r.json())
            .then(res => {
                DialogManager.closeLoading();
                if (res.success || !res.error) {
                    DialogManager.toast({ type: 'success', message: res.message || 'Saved successfully' });
                    const modal = bootstrap.Modal.getInstance(document.getElementById('standardModal'));
                    if (modal) modal.hide();
                    loadStandards();
                } else {
                    DialogManager.toast({ type: 'error', message: res.error || 'Error saving standard' });
                }
            })
            .catch(err => {
                DialogManager.closeLoading();
                console.error(err);
                DialogManager.toast({ type: 'error', message: 'Network error' });
            });
    });

    document.getElementById('standardModal').addEventListener('hidden.bs.modal', function () {
        document.getElementById('standardForm').reset();
        document.getElementById('standardId').value = '';
        if (validator) validator.reset();
    });
});
