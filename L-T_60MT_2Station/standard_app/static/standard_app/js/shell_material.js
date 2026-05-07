
// ============================================
// CONSTANTS & STATE
// ============================================
let CLASS_OPTIONS = [];
let CATEGORIES = [];
let EXISTING_NAMES = [];
let SUPERUSER_LEVEL = 0;

let masterMaterialsData = []; // Full dataset
let currentPage = 1;
let itemsPerPage = 10;
let selectedIds = new Set();

// Make validator global so it can be accessed in reset function
let validator;

// ============================================
// UTILITY FUNCTIONS
// ============================================

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function escapeHtml(text) {
    if (!text) return "";
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', function () {
    initSearchToggle();

    // Load data
    loadMetaData().then(() => {
        loadMaterials();
    });

    // Simple Form Validation - Allow any characters, check uniqueness
    validator = new FormValidator('shellMaterialForm', {
        name: {
            rules: [ValidationRules.required],
            asyncRule: (val, signal, form) => new Promise((resolve) => {
                setTimeout(() => {
                    const currentId = form.querySelector('[name="shell_material_id"]')?.value;
                    const exists = masterMaterialsData.some(item => {
                        // Compare with shell_material_id
                        if (currentId && item.shell_material_id == currentId) return false; // Exclude current item in edit mode
                        return item.name?.toLowerCase() === val.toLowerCase();
                    });
                    resolve(exists ? "Name already exists" : true);
                }, 300);
            })
        }
    });

    // Add modal hidden event listener to reset form and validator
    const modalEl = document.getElementById('shellMaterialModal');
    modalEl.addEventListener('hidden.bs.modal', function () {
        resetShellMaterialForm();
    });
});

// ============================================
// DATA LOADING
// ============================================

// Load Metadata
function loadMetaData() {
    return fetch("/api/shell-material/meta/")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Meta Error:", data.error);
                return;
            }

            CLASS_OPTIONS = data.classes;
            CATEGORIES = data.categories;
            EXISTING_NAMES = data.existing_names;
            SUPERUSER_LEVEL = data.superuser_level;

            if (data.all_categories_disabled) {
                // Keep Swal for this specific logic
                Swal.fire({
                    icon: 'error',
                    title: 'All Categories Disabled!',
                    text: 'Please enable at least one category to continue.',
                    confirmButtonText: 'Go to Category Page',
                    showCancelButton: true,
                }).then((result) => {
                    if (result.isConfirmed) window.location.href = '/category/';
                });
            }

            renderDataTableHeaders();
            renderPressureTableHeaders();
        })
        .catch(err => console.error("Meta Fetch Error:", err));
}

// Load Materials
function loadMaterials() {
    fetch("/api/shell-material/")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showTableError(data.error);
                return;
            }

            masterMaterialsData = data.materials || [];
            selectedIds.clear();
            initCustomPagination(masterMaterialsData);
        })
        .catch(error => {
            console.error("Load Error:", error);
            showTableError("Failed to load data.");
        });
}

function renderDataTableHeaders() {
    const tableHeaderRow = document.getElementById("table-header-row");
    const idLabel = SUPERUSER_LEVEL === 2 ? "MATERIAL ID" : "S.No";

    tableHeaderRow.innerHTML = `
    <th>
      <input type="checkbox" id="selectAll" onclick="toggleSelectAll()">
    </th>
    <th style="width: 60px;" class="text-end pe-3">${idLabel}</th>
    <th class="text-start">Material Name</th>
    <th class="text-start">Description</th>
    <th class="text-start">Status</th>
`;
}

function renderPressureTableHeaders() {
    const headerRow = document.getElementById("pressureTableHeadRow");
    // Static headers: Add Btn, Class
    let html = `
  <th>
    <button type="button" class="btn btn-sm btn-brand" onclick="addPressureRow()" title="Add Row">
      <i class="bi bi-plus-lg"></i>
    </button>
  </th>
  <th>Class <span class="text-danger">*</span></th>
`;

    // Dynamic headers from categories
    CATEGORIES.forEach(cat => {
        html += `<th>${cat.name}<br><small class="text-muted">(Bar)</small></th>`;
    });
    headerRow.innerHTML = html;
}

// ============================================
// PAGINATION & DISPLAY
// ============================================

function initCustomPagination(data) {
    // Try to restore page from localStorage
    const savedPage = localStorage.getItem('shellMaterialPage');
    const totalPages = Math.ceil(data.length / itemsPerPage);

    if (savedPage && !isNaN(savedPage)) {
        currentPage = parseInt(savedPage);
        // Ensure saved page is valid
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

    if (data.length === 0) {
        paginationWrapper.innerHTML = '';
        return;
    }

    const paginationHTML = [];

    // Total count
    paginationHTML.push(`<span class="text-muted small me-3">Total: ${data.length}</span>`);

    // Previous button
    paginationHTML.push(`
      <button class="pagination-btn prev-btn" onclick="goToPage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>
        Previous
      </button>
    `);

    // Page numbers with ellipsis
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
    const tbody = document.getElementById("materialsTableBody");
    tbody.innerHTML = "";

    // items slicing
    const start = (page - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const paginatedItems = data.slice(start, end);

    // Update Select All visual state
    const selectAll = document.getElementById('selectAll');
    if (selectAll) {
        // Use shell_material_id
        const allSelected = paginatedItems.length > 0 && paginatedItems.every(item => selectedIds.has(String(item.shell_material_id)));
        selectAll.checked = allSelected;
    }
    updateBulkDeleteButtonState();

    if (data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="text-center text-muted py-4">No materials found.</td></tr>`;
        return;
    }

    paginatedItems.forEach((item, index) => {
        const globalIndex = start + index + 1;
        // Use shell_material_id for display if Superuser/Debug
        const displayId = (SUPERUSER_LEVEL === 2) ? (item.shell_material_id || "-") : globalIndex;

        const statusClass = item.status.toLowerCase();
        const statusBadge = `<span class="status-badge ${statusClass}">${escapeHtml(item.status)}</span>`;

        // Use shell_material_id for selection
        const isChecked = selectedIds.has(String(item.shell_material_id));

        const tr = document.createElement('tr');
        // Row Click -> Show Action Dialog
        tr.onclick = (e) => {
            // Ignore clicks on checkboxes or specific interactive elements
            if (e.target.type !== 'checkbox' && !e.target.closest('.row-check') && !e.target.closest('button')) {
                handleRowInteraction(item);
            }
        };

        tr.innerHTML = `
    <td>
       <input type="checkbox" class="row-check" value="${item.shell_material_id}" ${isChecked ? 'checked' : ''} onclick="event.stopPropagation(); updateBulkDeleteButtonState();">
    </td>
    <td class="text-end fw-bold text-secondary">${displayId}</td>
    <td>${escapeHtml(item.name)}</td>
    <td class="text-muted">${escapeHtml(item.description || "")}</td>
    <td>${statusBadge}</td>
  `;

        const checkbox = tr.querySelector('.row-check');
        checkbox.addEventListener('change', function () {
            const id = this.value;
            if (this.checked) selectedIds.add(id);
            else selectedIds.delete(id);

            if (selectAll) {
                const allPage = paginatedItems.every(i => selectedIds.has(String(i.shell_material_id)));
                selectAll.checked = allPage;
            }
            updateBulkDeleteButtonState();
        });

        tbody.appendChild(tr);
    });
}

/**
 * Show Action Dialog on Row Click
 */
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
                title: "Edit Material?",
                message: `Are you sure you want to edit ${item.name}?`,
                confirmText: "Yes, Update",
                confirmButtonClass: 'dm-btn-info',
                // Pass item.shell_material_id
                onConfirm: () => openShellMaterialModal('edit', item.shell_material_id)
            });
        },
        onDeny: () => {
            // Pass item.shell_material_id
            deleteMaterial(item.shell_material_id);
        }
    });
}

function goToPage(page) {
    currentPage = page;
    localStorage.setItem('shellMaterialPage', page);
    triggerFilter();
}

function prevPage() {
    if (currentPage > 1) goToPage(currentPage - 1);
}

function nextPage() {
    const searchValue = document.getElementById('customSearchInput').value.toLowerCase().trim();
    // Logic to calculate max page based on filtered data needed.
    // Re-use triggerFilter logic or store filtered state.
    // For specific implementation:
    triggerFilter(true); // Helper to handle next page navigation? 
    // Wait, triggerFilter calls displayPage. 
    // Let's stick to simple logic:
    const filtered = getFilteredData();
    const totalPages = Math.ceil(filtered.length / itemsPerPage);
    if (currentPage < totalPages) goToPage(currentPage + 1);
}

function changeItemsPerPage(select) {
    itemsPerPage = parseInt(select.value);
    goToPage(1);
}

function getFilteredData() {
    const searchValue = document.getElementById('customSearchInput').value.toLowerCase().trim();
    if (!searchValue) return masterMaterialsData;
    return masterMaterialsData.filter(item =>
        (item.name && item.name.toLowerCase().includes(searchValue)) ||
        (item.description && item.description.toLowerCase().includes(searchValue))
    );
}

function triggerFilter(onlyCalc = false) {
    const filtered = getFilteredData();
    if (!onlyCalc) {
        renderPagination(filtered);
        displayPage(currentPage, filtered);
    }
}

function showTableError(msg) {
    document.getElementById("materialsTableBody").innerHTML =
        `<tr><td colspan="4" class="text-center text-danger py-4">${msg}</td></tr>`;
}

// ============================================
// BULK ACTIONS
// ============================================

function toggleSelectAll() {
    const selectAll = document.getElementById('selectAll');
    const isChecked = selectAll.checked;

    document.querySelectorAll('#materialsTableBody .row-check').forEach(c => {
        c.checked = isChecked;
        const id = c.value;
        if (isChecked) selectedIds.add(id);
        else selectedIds.delete(id);
    });
    updateBulkDeleteButtonState();
}

function updateBulkDeleteButtonState() {
    const count = selectedIds.size;
    const btn = document.getElementById('bulkDeleteBtn');
    if (btn) btn.disabled = count === 0;
}

function handleBulkDelete() {
    const ids = Array.from(selectedIds);

    if (ids.length === 0) return;

    DialogManager.confirmAction({
        title: "Delete Materials?",
        text: `Are you sure you want to delete ${ids.length} item(s)?`,
        confirmText: "Yes, Delete",
        url: "/api/shell-material/bulk-delete/",
        method: "POST",
        data: { ids: ids },
        onSuccess: () => {
            selectedIds.clear(); // Clear selections
            loadMetaData().then(() => loadMaterials());
        }
    });
}

// ============================================
// SEARCH
// ============================================

function dismissHint() {
    document.getElementById('editHint').classList.add('hidden');
    // localStorage.setItem('shellHintDismissed', 'true');
}

function initSearchToggle() {
    const searchToggleBtn = document.getElementById('searchToggleBtn');
    const searchInputWrapper = document.getElementById('searchInputWrapper');
    const searchInput = document.getElementById('customSearchInput');
    const searchCloseBtn = document.getElementById('searchCloseBtn');

    searchToggleBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (!searchInputWrapper.classList.contains('active')) {
            searchInputWrapper.classList.add('active');
            searchToggleBtn.classList.add('active');
            setTimeout(() => searchInput.focus(), 300);
        }
    });

    searchCloseBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetSearch();
    });

    searchInput.addEventListener('keyup', () => {
        currentPage = 1;
        triggerFilter();
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
        if (searchInputWrapper.classList.contains('active') && !searchInputWrapper.contains(e.target)) {
            resetSearch();
        }
    });
}

function resetSearch() {
    document.getElementById('searchInputWrapper').classList.remove('active');
    document.getElementById('searchToggleBtn').classList.remove('active');
    document.getElementById('customSearchInput').value = '';
    goToPage(1);
}


// ============================================
// MODAL & FORMS
// ============================================

function openShellMaterialModal(mode, id = null) {
    resetShellMaterialForm();
    const modalEl = document.getElementById("shellMaterialModal");
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    const title = document.getElementById("shellMaterialModalLabel");

    if (mode === 'add') {
        title.textContent = "Add Shell Material";
        document.getElementById("saveBtn").textContent = "Save";
        document.getElementById("saveBtn").className = "btn btn-success";
        addPressureRow(); // Add one empty row
        modal.show();
    } else {
        title.textContent = "Edit Shell Material";
        document.getElementById("saveBtn").textContent = "Update";
        document.getElementById("saveBtn").className = "btn btn-info";
        document.getElementById("shell_material_id").value = id;

        // Load details via shell_material_id
        fetch(`/api/shell-material/${id}/`)
            .then(r => r.json())
            .then(data => {
                if (data.error) { DialogManager.toast({ type: 'error', message: data.error }); return; }

                document.getElementById("material_name").value = data.name;
                document.getElementById("material_name").dataset.currentName = data.name;
                document.getElementById("material_description").value = data.description || "";
                document.getElementById("material_status").value = data.status || "";

                const tbody = document.getElementById("pressureDataTableBody");
                tbody.innerHTML = "";
                if (data.pressure_data && data.pressure_data.length > 0) {
                    data.pressure_data.forEach(row => addPressureRowWithData(row.class_id, row));
                } else {
                    addPressureRow();
                }
                modal.show();
            })
            .catch(err => {
                console.error(err);
                DialogManager.toast({ type: 'error', message: "Failed to load details" });
            });
    }
}

function resetShellMaterialForm() {
    document.getElementById("shellMaterialForm").reset();
    document.getElementById("shell_material_id").value = "";
    document.getElementById("material_name_error").textContent = "";
    document.getElementById("pressureDataTableBody").innerHTML = "";
    document.getElementById("duplicate_class_error").style.display = "none";

    // Reset validator to clear all validation states
    if (validator) {
        validator.reset();
    }

    // Remove any 'is-invalid' classes
    document.querySelectorAll(".is-invalid").forEach(el => el.classList.remove("is-invalid"));
}

// ============================================
// PRESSURE ROWS LOGIC
// ============================================

function addPressureRow() { addPressureRowWithData("", {}); }

function addPressureRowWithData(classId, rowData) {
    let classOpts = `<option value="">Select Class</option>`;
    CLASS_OPTIONS.forEach(cls => {
        const sel = (cls.id == classId) ? "selected" : "";
        classOpts += `<option value="${cls.id}" ${sel}>${cls.name}</option>`;
    });

    let pressureInputs = "";
    CATEGORIES.forEach(cat => {
        const val = rowData[cat.col] || "";
        pressureInputs += `
      <td>
        <input type="text" name="${cat.col}[]" class="form-control form-control-sm" 
               value="${escapeHtml(val)}" 
               oninput="validatePositiveNumber(this)" required>
      </td>
    `;
    });

    const tr = document.createElement('tr');
    tr.innerHTML = `
    <td>
       <button type="button" class="btn btn-sm text-danger" onclick="removePressureRow(this)">
         <i class="bi bi-trash"></i>
       </button>
    </td>
    <td>
       <select name="Class[]" class="form-select form-select-sm" onchange="checkDuplicateClasses()" required>
         ${classOpts}
       </select>
    </td>
    ${pressureInputs}
 `;
    document.getElementById("pressureDataTableBody").appendChild(tr);
    checkDuplicateClasses();
}

function removePressureRow(btn) {
    const tbody = document.getElementById("pressureDataTableBody");
    if (tbody.children.length > 1) {
        btn.closest('tr').remove();
        checkDuplicateClasses();
    } else {
        DialogManager.toast({ type: 'warning', message: "At least one row is required." });
    }
}


// ============================================
// VALIDATIONS
// ============================================

function validatePositiveNumber(input) {
    const val = input.value;
    // Allow decimal
    if (val && !/^\d*\.?\d+$/.test(val)) {
        input.classList.add("is-invalid");
    } else {
        input.classList.remove("is-invalid");
    }
}

function checkDuplicateClasses() {
    const selects = document.querySelectorAll('select[name="Class[]"]');
    const seen = new Set();
    let hasDup = false;
    selects.forEach(s => {
        if (s.value) {
            if (seen.has(s.value)) { s.classList.add("is-invalid"); hasDup = true; }
            else { s.classList.remove("is-invalid"); seen.add(s.value); }
        }
    });
    const err = document.getElementById("duplicate_class_error");
    if (hasDup) err.style.display = "block";
    else err.style.display = "none";

    return !hasDup;
}

function validateMaterialName() {
    const input = document.getElementById("material_name");
    const val = input.value.trim();
    const err = document.getElementById("material_name_error");

    if (!val) {
        input.classList.add("is-invalid");
        err.textContent = "Name required";
        return false;
    }

    const current = input.dataset.currentName || "";
    const exists = EXISTING_NAMES.some(n => n.toLowerCase() === val.toLowerCase() && n.toLowerCase() !== current.toLowerCase());

    if (exists) {
        input.classList.add("is-invalid");
        err.textContent = "Duplicate name";
        return false;
    }

    input.classList.remove("is-invalid");
    err.textContent = "";
    return true;
}

// ============================================
// ACTIONS
// ============================================

document.getElementById("shellMaterialForm").addEventListener("submit", function (e) {
    e.preventDefault();
    if (!validateMaterialName() || !checkDuplicateClasses()) return;

    const formData = new FormData(this);
    const id = formData.get("shell_material_id"); // Changed from material_id
    const url = id ? `/api/shell-material/edit/${id}/` : `/api/shell-material/add/`;

    DialogManager.loading("Saving...", "Please wait");
    fetch(url, {
        method: "POST",
        headers: { "X-CSRFToken": getCSRFToken() },
        body: formData
    })
        .then(r => r.json())
        .then(res => {
            DialogManager.closeLoading();
            if (res.error) {
                DialogManager.toast({ type: 'error', message: res.error });
            } else {
                DialogManager.toast({ type: 'success', message: "Saved successfully!" });
                bootstrap.Modal.getInstance(document.getElementById("shellMaterialModal")).hide();
                // Reload meta to update existing names logic
                return loadMetaData().then(() => loadMaterials());
            }
        })
        .catch(err => {
            DialogManager.closeLoading();
            console.error(err);
            DialogManager.toast({ type: 'error', message: "Error saving data" });
        });
});

function deleteMaterial(shell_id) {
    DialogManager.confirmAction({
        title: "Delete Shell Material?",
        text: "This action cannot be undone.",
        confirmText: "Yes, Delete",
        // The service delete_shell_material expects shell_id (which is SHELL_MATERIAL_ID)
        url: `/api/shell-material/delete/${shell_id}/`,
        method: "POST",
        onSuccess: () => {
            loadMetaData().then(() => loadMaterials());
        }
    });
}
