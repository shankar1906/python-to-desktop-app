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
    if (!text) return "";
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function dismissHint() {
    const hint = document.getElementById('editHint');
    if (hint) hint.style.display = 'none';
    localStorage.setItem('itemDetailsHintDismissed', 'true');
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

    const tbody = document.getElementById('itemDetailsTableBody');
    tbody.innerHTML = '';

    const checkAll = document.getElementById('checkAll');
    if (checkAll) {
        const currentIds = pageData.map(d => String(d.id));
        checkAll.checked = currentIds.length > 0 && currentIds.every(id => selectedIds.has(id));
    }

    if (pageData.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center">No records found</td></tr>';
        return;
    }

    pageData.forEach((item, index) => {
        const tr = document.createElement('tr');
        tr.style.cursor = 'pointer';
        const isChecked = selectedIds.has(String(item.id));
        const statusClass = (item.status || 'Enabled').toLowerCase();

        let fieldCount = 0;
        if (Array.isArray(item.row_details)) {
            fieldCount = item.row_details.length;
        } else if (typeof item.row_details === 'string') {
            try {
                const parsed = JSON.parse(item.row_details);
                fieldCount = Array.isArray(parsed) ? parsed.length : 0;
            } catch (e) { }
        }

        tr.innerHTML = `
            <td onclick="event.stopPropagation()">
                <input type="checkbox" class="form-check-input detail-checkbox" value="${item.id}" ${isChecked ? 'checked' : ''}>
            </td>
            <td class="text-end pe-3">${start + index + 1}</td>
            <td>${escapeHtml(item.column_name)}</td>
            <td><span class="badge bg-light text-dark border">${fieldCount} Fields Configured</span></td>
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
// DYNAMIC ROW LOGIC
// ============================================

window.toggleDropdownAccordion = function (headerEl) {
    const accordion = headerEl.closest('.dropdown-options-accordion');
    const body = accordion.querySelector('.dropdown-accordion-body');
    headerEl.classList.toggle('collapsed');
    body.classList.toggle('collapsed');
};

window.addDropdownOption = function (btnEl) {
    const fieldRow = btnEl.closest('.field-row');
    const listEl = fieldRow.querySelector('.dropdown-options-list');
    const template = document.getElementById('dropdownOptionTemplate');
    const clone = template.content.cloneNode(true);
    listEl.appendChild(clone);
};

window.removeDropdownOption = function (btnEl) {
    btnEl.closest('.dropdown-option-row').remove();
};

function _showDropdownAccordionForFieldRow(rowEl, show) {
    const accordion = rowEl.querySelector('.dropdown-options-accordion');
    if (accordion) accordion.style.display = show ? 'block' : 'none';
}

function _addFieldRow(data = null) {
    const container = document.getElementById('fieldsContainer');
    const template = document.getElementById('fieldRowTemplate');
    const clone = template.content.cloneNode(true);

    const rowEl = clone.querySelector('.field-row');
    const fieldTypeSelect = rowEl.querySelector('.field-type');
    const accordion = rowEl.querySelector('.dropdown-options-accordion');
    const accordionBody = rowEl.querySelector('.dropdown-accordion-body');
    const accordionHeader = rowEl.querySelector('.dropdown-accordion-header');

    if (data) {
        rowEl.querySelector('.field-name').value = data.field_name || '';
        rowEl.querySelector('.field-type').value = data.data_type || 'VARCHAR';
        rowEl.querySelector('.field-mandatory').checked = data.is_mandatory || false;

        // Populate dropdown options when data_type is DROP DOWN
        if (data.data_type === 'DROP DOWN' && Array.isArray(data.dropdown_options)) {
            _showDropdownAccordionForFieldRow(rowEl, true);
            const listEl = rowEl.querySelector('.dropdown-options-list');
            const optTemplate = document.getElementById('dropdownOptionTemplate');
            if (data.dropdown_options.length > 0) {
                data.dropdown_options.forEach(opt => {
                    const optClone = optTemplate.content.cloneNode(true);
                    optClone.querySelector('.dropdown-option-input').value = (typeof opt === 'string' ? opt : opt?.value || opt?.label || '') || '';
                    listEl.appendChild(optClone);
                });
            }
        }
    }

    // Toggle accordion visibility when data type changes
    fieldTypeSelect.addEventListener('change', function () {
        const isDropdown = this.value === 'DROP DOWN';
        _showDropdownAccordionForFieldRow(rowEl, isDropdown);
        if (isDropdown) {
            accordionBody.classList.remove('collapsed');
            accordionHeader.classList.remove('collapsed');
            const listEl = rowEl.querySelector('.dropdown-options-list');
            if (listEl.children.length === 0) addDropdownOption(rowEl.querySelector('.add-option-btn'));
        }
    });

    // Show accordion if DROP DOWN is pre-selected
    if (fieldTypeSelect.value === 'DROP DOWN') {
        _showDropdownAccordionForFieldRow(rowEl, true);
        const listEl = rowEl.querySelector('.dropdown-options-list');
        if (listEl.children.length === 0) addDropdownOption(rowEl.querySelector('.add-option-btn'));
    }

    container.appendChild(clone);
    updateRemoveButtons();
}

window.addFieldRow = function (data) {
    _addFieldRow(data);
};

window.removeFieldRow = function (btn) {
    const row = btn.closest('.field-row');
    row.remove();
    updateRemoveButtons();
};

function updateRemoveButtons() {
    const rows = document.querySelectorAll('.field-row');
    const buttons = document.querySelectorAll('.remove-row-btn');
    // You can implement logic here to show/hide delete buttons if needed
}

function collectFieldData() {
    const rows = document.querySelectorAll('.field-row');
    const fields = [];
    let isValid = true;
    let dropdownError = null;

    rows.forEach(row => {
        const name = row.querySelector('.field-name').value.trim();
        const type = row.querySelector('.field-type').value;
        const mandatory = row.querySelector('.field-mandatory').checked;

        if (!name) isValid = false;

        const fieldData = {
            field_name: name,
            data_type: type,
            is_mandatory: mandatory
        };

        // Collect dropdown options when data type is DROP DOWN
        if (type === 'DROP DOWN') {
            const optionInputs = row.querySelectorAll('.dropdown-option-input');
            const options = [];
            optionInputs.forEach(inp => {
                const val = inp.value.trim();
                if (val) options.push(val);
            });
            fieldData.dropdown_options = options;
            if (options.length === 0) dropdownError = `"${name || 'Field'}" requires at least one dropdown option.`;
        }

        fields.push(fieldData);
    });

    return { fields, isValid, dropdownError };
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

function loadItemDetails() {
    fetch('/api/item_details/')
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
    document.getElementById('itemDetailForm').reset();
    document.getElementById('detailId').value = '';
    document.getElementById('modalTitle').textContent = 'Add Item Detail';
    document.getElementById('fieldsContainer').innerHTML = '';
    document.getElementById('fieldsError').style.display = 'none';

    // Fetch all unique labels to pre-populate for a NEW item
    DialogManager.loading('Fetching existing fields...', 'Please wait');
    fetch('/api/item_details/unique_labels/')
        .then(r => r.json())
        .then(res => {
            DialogManager.closeLoading();
            if (res.success && res.labels && res.labels.length > 0) {
                res.labels.forEach(label => {
                    _addFieldRow({ field_name: label, data_type: 'VARCHAR', is_mandatory: false });
                });
            } else {
                _addFieldRow(); // Fallback to one empty row
            }
        })
        .catch(err => {
            DialogManager.closeLoading();
            console.error(err);
            _addFieldRow();
        });

    const btn = document.getElementById('saveBtn');
    btn.textContent = 'Save';
    btn.className = 'btn btn-primary';
    const modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('itemDetailModal'));
    modal.show();
};

function openEditModal(item) {
    document.getElementById('detailId').value = item.id;
    document.getElementById('columnName').value = item.column_name;
    document.getElementById('status').value = item.status;
    document.getElementById('modalTitle').textContent = 'Edit Item Detail';
    document.getElementById('fieldsContainer').innerHTML = '';
    document.getElementById('fieldsError').style.display = 'none';

    let rows = [];
    if (typeof item.row_details === 'string') {
        try { rows = JSON.parse(item.row_details); } catch (e) { }
    } else if (Array.isArray(item.row_details)) {
        rows = item.row_details;
    }

    if (rows && rows.length > 0) {
        rows.forEach(row => _addFieldRow(row));
    } else {
        _addFieldRow();
    }

    const btn = document.getElementById('saveBtn');
    btn.textContent = 'Update';
    btn.className = 'btn btn-info text-white';
    const modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('itemDetailModal'));
    modal.show();
}

function deleteDetail(id) {
    DialogManager.confirmAction({
        title: "Delete Column Detail?",
        text: "Are you sure you want to delete this configuration?",
        confirmText: "Yes, Delete",
        url: `/api/item_details/delete/${id}/`,
        method: "POST",
        onSuccess: () => loadItemDetails()
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
        text: "Are you sure you want to delete selected columns?",
        confirmText: "Yes, Delete",
        url: "/api/item_details/bulk_delete/",
        method: "POST",
        data: { ids: ids },
        onSuccess: () => {
            selectedIds.clear();
            loadItemDetails();
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
            d.column_name.toLowerCase().includes(q)
        );
        initPagination(filtered);
    };
}

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', function () {
    if (localStorage.getItem('itemDetailsHintDismissed') === 'true') {
        dismissHint();
    }

    loadItemDetails();
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

    validator = new FormValidator('itemDetailForm', {
        column_name: {
            rules: [ValidationRules.required],
            // Updated async rule to handle the new Item name check
            asyncRule: (val, signal, form) => new Promise((resolve) => {
                setTimeout(() => {
                    const currentId = form.querySelector('[name="id"]')?.value;
                    const exists = allData.some(item => {
                        if (currentId && String(item.id).trim() === String(currentId).trim()) return false;
                        return item.column_name?.trim().toLowerCase() === val.trim().toLowerCase();
                    });
                    resolve(exists ? "Item name already exists" : true);
                }, 300);
            })
        },
        status: { rules: [ValidationRules.required] }
    });

    document.getElementById('itemDetailForm').onsubmit = async function (e) {
        e.preventDefault();

        // 1. Validate main fields
        if (!(await validator.validateAll())) return;

        // 2. Validate dynamic rows
        const { fields, isValid, dropdownError } = collectFieldData();

        const errorDiv = document.getElementById('fieldsError');
        if (fields.length === 0) {
            errorDiv.textContent = "At least one field is required.";
            errorDiv.style.display = 'block';
            return;
        }

        if (!isValid) {
            errorDiv.textContent = "All field names are required.";
            errorDiv.style.display = 'block';
            return;
        }

        if (dropdownError) {
            errorDiv.textContent = dropdownError;
            errorDiv.style.display = 'block';
            return;
        }

        errorDiv.style.display = 'none';

        const id = document.getElementById('detailId').value;
        const url = id ? `/api/item_details/edit/${id}/` : '/api/item_details/add/';
        const formData = new FormData(this);

        formData.append('row_details', JSON.stringify(fields));

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
                    bootstrap.Modal.getInstance(document.getElementById('itemDetailModal')).hide();
                    loadItemDetails();
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

    document.getElementById('itemDetailModal').addEventListener('hidden.bs.modal', function () {
        validator.reset();
    });
});
