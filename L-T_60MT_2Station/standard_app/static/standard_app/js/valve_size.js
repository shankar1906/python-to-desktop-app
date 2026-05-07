let allValves = [];
let filteredData = [];
let searchQuery = '';
let currentPage = 1;
let itemsPerPage = 10;
let selectedIds = new Set();
let durationColumnNames = [];
let SUPERUSER_LEVEL = 0;
let valveValidator;

/** Escape HTML to prevent XSS */
function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : "";
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
            input.value = '';
            searchQuery = '';
            wrapper.classList.remove('active');
            currentPage = 1;
            renderTable();
        }
    });
}

function updateBulkDelete() {
    const count = selectedIds.size;
    const btn = document.getElementById('bulkDeleteBtn');
    if (btn) btn.disabled = count === 0;
}

function handleBulkDelete() {
    const selected = Array.from(selectedIds);
    if (selected.length === 0) return;

    DialogManager.confirmAction({
        title: `Delete ${selected.length} items?`,
        text: "This cannot be undone.",
        confirmText: 'Yes, Delete',
        url: '/api/valvesize/bulk_delete/',
        method: "POST",
        data: { ids: selected },
        onSuccess: () => {
            selectedIds.clear();
            loadValvesize();
            const selectAll = document.getElementById('selectAll');
            if (selectAll) selectAll.checked = false;
        }
    });
}

function handleRowInteraction(id, name) {
    const options = {
        title: `Action for "${name}"`,
        message: "Choose an action",
        confirmText: "Update",
        confirmButtonClass: 'dm-btn-info',
        cancelText: "Cancel",
        onConfirm: () => {
            DialogManager.confirm({
                title: "Edit Valve Size?",
                message: `Are you sure you want to edit "${name}"?`,
                confirmText: "Yes, Update",
                confirmButtonClass: 'dm-btn-info',
                onConfirm: () => openEditModal(id)
            });
        }
    };

    if (SUPERUSER_LEVEL == 2) {
        options.denyText = "Delete";
        options.onDeny = () => delete_valve(id);
    }

    DialogManager.confirm(options);
}

function loadValvesize() {
    fetch("/api/valvesize/")
        .then(r => r.json())
        .then(data => {
            allValves = data.valve_list || [];
            selectedIds.clear();
            renderTable();
        })
        .catch(err => {
            console.error("Error fetching valves:", err);
            const tbody = document.getElementById("vsTablebody");
            if (tbody) tbody.innerHTML = `<tr><td colspan="7" class="text-center text-danger">Error loading data</td></tr>`;
        });
}

function renderTable() {
    const tbody = document.getElementById("vsTablebody");
    if (!tbody) return;

    filteredData = allValves.filter(item => {
        if (!searchQuery) return true;
        const q = searchQuery.toLowerCase();
        return [item.SIZE_NAME, item.SIZE_DESC, item.PART_NO, item.PART_NAME].join(' ').toLowerCase().includes(q);
    });

    const totalItems = filteredData.length;
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    if (currentPage > totalPages) currentPage = totalPages || 1;
    if (currentPage < 1) currentPage = 1;

    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const pageData = filteredData.slice(start, end);

    const selectAllCheckbox = document.getElementById('selectAll');
    if (selectAllCheckbox) {
        const newSelectAll = selectAllCheckbox.cloneNode(true);
        selectAllCheckbox.parentNode.replaceChild(newSelectAll, selectAllCheckbox);

        const allSelected = pageData.length > 0 && pageData.every(item => selectedIds.has(String(item.SIZE_ID)));
        newSelectAll.checked = allSelected;

        newSelectAll.addEventListener('change', function () {
            const isChecked = this.checked;
            document.querySelectorAll('.row-check').forEach(ch => {
                ch.checked = isChecked;
                const id = ch.value;
                if (isChecked) selectedIds.add(id);
                else selectedIds.delete(id);
            });
            updateBulkDelete();
        });
    }

    tbody.innerHTML = '';
    updateBulkDelete();

    if (pageData.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center text-muted py-4">No valve sizes found</td></tr>`;
    } else {
        pageData.forEach((valve, idx) => {
            const isChecked = selectedIds.has(String(valve.SIZE_ID));
            const tr = document.createElement('tr');
            tr.onclick = (e) => {
                if (e.target.tagName !== 'INPUT' && !e.target.closest('.row-check')) handleRowInteraction(valve.SIZE_ID, valve.SIZE_NAME);
            };

            let checkboxHtml = '';
            if (SUPERUSER_LEVEL == 2) {
                checkboxHtml = `<td onclick="event.stopPropagation()">
              <input type="checkbox" class="row-check" value="${valve.SIZE_ID}" ${isChecked ? 'checked' : ''}>
            </td>`;
            }

            const displayId = (SUPERUSER_LEVEL == 2) ? valve.SIZE_ID : (start + idx + 1);
            const status = valve.STATUS || 'Enabled';
            const statusClass = status.toLowerCase();
            const statusBadge = `<span class="status-badge ${statusClass}">${escapeHtml(status)}</span>`;

            tr.innerHTML = `
            ${checkboxHtml}
            <td class="text-end pe-3">${displayId}</td>
            <td class="text-start">${escapeHtml(valve.SIZE_NAME)}</td>
            <td class="text-start">${escapeHtml(valve.SIZE_DESC || '')}</td>
            <td class="text-start">${escapeHtml(valve.PART_NO || '')}</td>
            <td class="text-start">${escapeHtml(valve.PART_NAME || '')}</td>
            <td class="text-start">${statusBadge}</td>
        `;

            if (SUPERUSER_LEVEL == 2) {
                const ch = tr.querySelector('.row-check');
                ch.addEventListener('change', function () {
                    const id = this.value;
                    if (this.checked) selectedIds.add(id);
                    else selectedIds.delete(id);

                    const newSelectAll = document.getElementById('selectAll');
                    if (newSelectAll) {
                        const currentAll = pageData.every(i => selectedIds.has(String(i.SIZE_ID)));
                        newSelectAll.checked = currentAll;
                    }
                    updateBulkDelete();
                });
            }
            tbody.appendChild(tr);
        });
    }

    renderPagination(totalPages);
}

function renderPagination(totalPages) {
    const wrapper = document.getElementById('customPagination');
    if (!wrapper) return;
    if (filteredData.length === 0) { wrapper.innerHTML = ''; return; }

    const paginationHTML = [];
    paginationHTML.push(`<span class="text-muted small me-3">Total: ${filteredData.length}</span>`);
    paginationHTML.push(`<button class="pagination-btn prev-btn" ${currentPage === 1 ? 'disabled' : ''} onclick="changePage(${currentPage - 1})">Previous</button>`);

    if (totalPages <= 7) {
        for (let i = 1; i <= totalPages; i++) {
            paginationHTML.push(`<button class="pagination-btn ${i === currentPage ? 'active' : ''}" onclick="changePage(${i})">${i}</button>`);
        }
    } else {
        paginationHTML.push(`<button class="pagination-btn ${currentPage === 1 ? 'active' : ''}" onclick="changePage(1)">1</button>`);
        if (currentPage > 3) paginationHTML.push('<span class="pagination-ellipsis">...</span>');
        let start = Math.max(2, currentPage - 1);
        let end = Math.min(totalPages - 1, currentPage + 1);
        for (let i = start; i <= end; i++) {
            paginationHTML.push(`<button class="pagination-btn ${i === currentPage ? 'active' : ''}" onclick="changePage(${i})">${i}</button>`);
        }
        if (currentPage < totalPages - 2) paginationHTML.push('<span class="pagination-ellipsis">...</span>');
        paginationHTML.push(`<button class="pagination-btn ${currentPage === totalPages ? 'active' : ''}" onclick="changePage(${totalPages})">${totalPages}</button>`);
    }

    paginationHTML.push(`<button class="pagination-btn next-btn" ${currentPage >= totalPages ? 'disabled' : ''} onclick="changePage(${currentPage + 1})">Next</button>`);
    paginationHTML.push(`
    <select class="pagination-per-page" onchange="changeItemsPerPage(this.value)">
      <option value="10" ${itemsPerPage === 10 ? 'selected' : ''}>10 / page</option>
      <option value="25" ${itemsPerPage === 25 ? 'selected' : ''}>25 / page</option>
      <option value="50" ${itemsPerPage === 50 ? 'selected' : ''}>50 / page</option>
      <option value="100" ${itemsPerPage === 100 ? 'selected' : ''}>100 / page</option>
    </select>
  `);

    wrapper.innerHTML = paginationHTML.join('');
}

window.changePage = function (p) {
    if (p < 1) return;
    currentPage = p;
    localStorage.setItem('valveSizePage', currentPage);
    renderTable();
};

window.changeItemsPerPage = function (val) {
    itemsPerPage = parseInt(val);
    localStorage.setItem('valveSizePPI', itemsPerPage);
    currentPage = 1;
    localStorage.setItem('valveSizePage', 1);
    renderTable();
};

function get_all_standards(select = null, selectedid = null) {
    fetch('/api/standards/')
        .then(response => response.json())
        .then(data => {
            const standardList = (data.standards || []).filter(
                s => String(s.status || '').toLowerCase() === 'enabled'
            );
            if (select && select.tagName === 'SELECT') {
                select.innerHTML = '<option value="">Select</option>';
                standardList.forEach(std => {
                    const option = document.createElement('option');
                    option.value = String(std.standard_id);
                    option.textContent = std.name;
                    select.appendChild(option);
                });
                if (selectedid != null && selectedid !== '') {
                    select.value = String(selectedid);
                }
            }
        })
        .catch(err => {
            console.error('Error loading standards:', err);
            if (select && select.tagName === 'SELECT') {
                select.innerHTML = '<option value="">Failed to load</option>';
            }
            DialogManager.toast({ type: 'error', message: 'Failed to load standards list.' });
        });
}

function get_all_vlaves(select = null, selectedId = null) {
    fetch('/api/get_valve_type/')
        .then(r => r.json())
        .then(data => {
            const typeList = data.valve_type_list;
            if (select && select.tagName === 'SELECT') {
                select.innerHTML = '<option value="">Select</option>';
                typeList.forEach(t => {
                    const opt = document.createElement('option');
                    opt.value = t.TYPE_ID;
                    opt.textContent = t.TYPE_NAME;
                    select.appendChild(opt);
                });
                if (selectedId) select.value = selectedId;
            }
        });
}

function get_enable_categoryies() {
    return fetch('/api/enabled_categories/')
        .then(r => r.json())
        .then(data => {
            const list = data.enabled_categories_list || [];
            const headerRow = document.getElementById('category-header-row');
            if (headerRow) {
                while (headerRow.children.length > 2) headerRow.removeChild(headerRow.lastChild);
                durationColumnNames = [];
                list.forEach(ctg => {
                    const th = document.createElement('th');
                    th.innerHTML = `${ctg.CATEGORY_NAME}<br><small>(sec)</small>`;
                    headerRow.appendChild(th);
                    durationColumnNames.push(ctg.DURATION_COLUMN_NAME);
                });
            }
        })
        .catch(err => {
            console.error("Error loading categories:", err);
            DialogManager.toast({ type: 'error', message: 'Failed to load test categories.' });
        });
}

function validatePositive(input) {
    const value = input.value.trim();
    const showError = (msg) => {
        input.classList.add('is-invalid');
        let fb = input.parentNode.querySelector('.invalid-feedback');
        if (!fb) {
            fb = document.createElement('div');
            fb.className = 'invalid-feedback';
            input.parentNode.appendChild(fb);
        }
        fb.style.display = 'block';
        fb.innerText = msg;
    };

    if (value === "") { showError("Required"); return false; }
    if (!/^\d*\.?\d+$/.test(value)) { showError("Numbers only"); return false; }
    input.classList.remove('is-invalid');
    const fb = input.parentNode.querySelector('.invalid-feedback');
    if (fb) fb.remove();
    return true;
}

function checkDuplicates(selector, msg) {
    const items = Array.from(document.querySelectorAll(selector));
    const counts = {};
    let valid = true;
    let errorType = null;

    items.forEach(i => {
        i.classList.remove('is-invalid');
        const err = i.parentNode.querySelector('.invalid-feedback');
        if (err) err.remove();
        const v = i.value;
        if (v && v !== "Select" && v !== "Loading...") counts[v] = (counts[v] || 0) + 1;
    });

    items.forEach(i => {
        const v = i.value;
        if (!v || v === "Select" || v === "Loading...") {
            valid = false;
            errorType = 'required';
            i.classList.add('is-invalid');
            const d = document.createElement('div');
            d.className = 'invalid-feedback';
            d.style.display = 'block';
            d.innerText = "Required";
            i.parentNode.appendChild(d);
        } else if (counts[v] > 1) {
            valid = false;
            if (!errorType) errorType = 'duplicate';
            i.classList.add('is-invalid');
            const d = document.createElement('div');
            d.className = 'invalid-feedback';
            d.style.display = 'block';
            d.innerText = msg;
            i.parentNode.appendChild(d);
        }
    });
    return { valid, errorType };
}

window.validateValvetype = function () { return checkDuplicates("#tableBody2 select[name='valve_type[]']", "Duplicate Valve Type"); };
window.validateStandards = function () { return checkDuplicates("#tableBody select[name='standard[]']", "Duplicate Standard"); };

function validateForm() {
    const nameInput = document.getElementById("valve_name");
    let name = nameInput.value.trim();
    if (name && !name.endsWith('"')) {
        name += '"';
        nameInput.value = name;
    }

    const u1 = window.validateStandards();
    const u2 = window.validateValvetype();

    let hasInvalidFormat = false;
    let hasEmptyRequired = false;

    document.querySelectorAll('#tableBody input, #tableBody2 input').forEach(inp => {
        if (inp.required || (inp.getAttribute('oninput') && inp.getAttribute('oninput').includes('validatePositive'))) {
            const isValid = validatePositive(inp);
            if (!isValid) {
                if (inp.value.trim() === "") hasEmptyRequired = true;
                else hasInvalidFormat = true;
            }
        }
    });

    if (hasInvalidFormat) {
        DialogManager.toast({ type: "warning", message: "Please correct invalid values (positive numbers only)." });
        return false;
    }

    if (!u1.valid || !u2.valid || hasEmptyRequired) {
        const isDuplicate = (u1.valid === false && u1.errorType === 'duplicate') ||
            (u2.valid === false && u2.errorType === 'duplicate');
        if (isDuplicate) {
            DialogManager.toast({ type: "warning", message: "Please fix duplicate entries in the table." });
        } else {
            DialogManager.toast({ type: "warning", message: "Please fill the mandatory fields" });
        }
        return false;
    }

    return true;
}

window.addRow = function (category = null) {
    const tableBody = document.getElementById('tableBody');
    const headerRow = document.getElementById('category-header-row');
    const addBtn = document.getElementById('standard-add-row-btn');
    if (!tableBody || !headerRow) return;
    const categoryCount = headerRow.children.length - 2;
    const tr = document.createElement("tr");

    let html = `<td><button type="button" class="btn btn-sm text-danger" onclick="removeRow(this)"><i class="bi bi-trash"></i></button></td>`;
    html += `<td style="display:none;"><input name="original_id" class="duration-id" value="${category?.id || ''}" readonly></td>`;
    html += `<td><select class="form-select form-select-sm standard-select" name="standard[]" onchange="validateStandards(this)" required><option>Loading...</option></select></td>`;

    let values = [];
    if (category) {
        values = Object.keys(category).filter(k => k.startsWith("COL") && k.endsWith("_DUR")).sort().map(k => category[k]);
    }

    for (let i = 0; i < categoryCount; i++) {
        const v = values[i] !== undefined ? values[i] : "";
        html += `<td><input type="text" name="category_value[]" class="form-control text-end" oninput="validatePositive(this)" value="${v}" required></td>`;
    }
    tr.innerHTML = html;
    tableBody.appendChild(tr);

    const sel = tr.querySelector('.standard-select');
    get_all_standards(sel, category?.standard ?? category?.duration_type);

    if (addBtn) {
        if (tableBody.rows.length >= 2) addBtn.style.display = 'none';
        else addBtn.style.display = 'inline-block';
    }
};

/*
 window.addRow2 = function (rowData = null) {
    const tableBody = document.getElementById('tableBody2');
    if (!tableBody) return;
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><button type="button" class="btn btn-sm text-danger" onclick="removeRow2(this)"><i class="bi bi-trash"></i></button></td>
      <td style="display:none;"><input name="original_valve_id" class="original-id" value="${rowData?.id || ''}" readonly></td>
      <td><select name="valve_type[]" class="form-select form-select-sm valve-type-select" onchange="validateValvetype(this)" required><option>Select</option></select></td>
      <td><input type="text" name="open_degree[]" class="form-control form-control-sm text-end" oninput="validatePositive(this)" value="${rowData ? rowData.open_degree : ''}" required></td>
      <td><input type="text" name="close_degree[]" class="form-control form-control-sm text-end" oninput="validatePositive(this)" value="${rowData ? rowData.close_degree : ''}" required></td>
      <td><input type="text" name="loading_unloading_degree[]" class="form-control form-control-sm text-end" oninput="validatePositive(this)" value="${rowData ? rowData.loading_unloading_degree : ''}" required></td>
   `;
    tableBody.appendChild(tr);
    const sel = tr.querySelector('.valve-type-select');
    get_all_vlaves(sel, rowData?.valve_type_id);
}; 
*/

window.removeRow = function (btn) {
    const tableBody = document.getElementById('tableBody');
    const addBtn = document.getElementById('standard-add-row-btn');
    if (tableBody.rows.length > 1) {
        btn.closest('tr').remove();
        if (addBtn) {
            if (tableBody.rows.length >= 2) addBtn.style.display = 'none';
            else addBtn.style.display = 'inline-block';
        }
    } else {
        DialogManager.toast({ type: 'warning', message: 'At least one row is required' });
    }
};
window.removeRow2 = function (btn) {
    if (btn.closest('tbody').rows.length > 1) btn.closest('tr').remove();
    else alert("At least one row needed.");
};

window.openAddForm = async function () {
    try {
        await get_enable_categoryies();
        document.getElementById("valveModalLabel").innerText = "ADD Valve Size";
        const saveBtn = document.getElementById("saveBtn");
        saveBtn.innerText = "Save";
        saveBtn.className = "btn btn-success";
        document.getElementById("size_id_hidden").value = "";

        document.getElementById("valve_name").value = "";
        document.getElementById("valve_size_id").value = "";
        document.getElementById("desc").value = "";
        document.getElementById("part_no").value = "";
        document.getElementById("part_name").value = "";
        document.getElementById("status").value = "";

        document.getElementById("tableBody").innerHTML = '';
        if (valveValidator) valveValidator.reset();

        const modal = bootstrap.Modal.getOrCreateInstance(document.getElementById("valveModal"));
        modal.show();
        addRow();
        // addRow2();
    } catch (err) {
        console.error(err);
        DialogManager.toast({ type: 'error', message: 'Failed to open add form.' });
    }
};

window.openEditModal = async function (id) {
    try {
        await get_enable_categoryies();
        const modalEl = document.getElementById("valveModal");
        const modal = bootstrap.Modal.getOrCreateInstance(modalEl);

        document.getElementById("valveModalLabel").innerText = "Edit Valve Size";
        const saveBtn = document.getElementById("saveBtn");
        saveBtn.innerText = "Update";
        saveBtn.className = "btn btn-info";
        document.getElementById("tableBody").innerHTML = '';
        if (valveValidator) valveValidator.reset();

        DialogManager.loading("Loading data...", "Please wait");
        const resp = await fetch(`/api/valvesize/edit/${id}/`);
        const data = await resp.json();
        DialogManager.closeLoading();

        if (data.error || !data.edit_valve) {
            DialogManager.toast({ type: 'error', message: data.error || 'Failed to load valve data.' });
            return;
        }

        const v = data.edit_valve;
        document.getElementById("size_id_hidden").value = String(id);
        document.getElementById("valve_name").value = v.name || "";
        document.getElementById("valve_size_id").value = v.size_id || id;
        document.getElementById("desc").value = v.description || "";
        document.getElementById("part_no").value = v.part_no || "";
        document.getElementById("part_name").value = v.part_name || "";
        document.getElementById("status").value = v.status || "Enabled";

        // (data.degree_data || []).forEach(r => addRow2(r));
        (data.duration_data || []).forEach(r => addRow(r));

        modal.show();
    } catch (err) {
        DialogManager.closeLoading();
        console.error(err);
        DialogManager.toast({ type: 'error', message: 'Failed to open edit form.' });
    }
};

async function handleFormSubmit(event) {
    if (event) event.preventDefault();
    const saveBtn = document.getElementById("saveBtn");
    if (saveBtn.disabled) return;

    const isTableValid = validateForm();
    const isNameValid = await valveValidator.validateAll();
    if (!isTableValid || !isNameValid) return;

    const id = document.getElementById("size_id_hidden").value;
    const payload = {
        size_id: document.getElementById("valve_size_id").value,
        valve_name: document.getElementById("valve_name").value,
        valve_des: document.getElementById("desc").value,
        part_no: document.getElementById("part_no").value.trim(),
        part_name: document.getElementById("part_name").value.trim(),
        status: document.getElementById("status").value.trim(),
        duration_rows: [],
        degree_rows: []
    };

    document.querySelectorAll("#tableBody tr").forEach(row => {
        const std = row.querySelector("select[name='standard[]']").value;
        const vals = Array.from(row.querySelectorAll("input[name='category_value[]']")).map(i => i.value);
        let obj = { standard: std };
        if (id) obj.ogi_id = row.querySelector("input[name='original_id']")?.value || '';
        durationColumnNames.forEach((c, i) => obj[c] = vals[i] || null);
        payload.duration_rows.push(obj);
    });

    document.querySelectorAll("#tableBody2 tr").forEach(row => {
        let obj = {
            type_id: row.querySelector("select[name='valve_type[]']").value,
            open_degree: row.querySelector("input[name='open_degree[]']").value,
            close_degree: row.querySelector("input[name='close_degree[]']").value,
            loading_unloading_degree: row.querySelector("input[name='loading_unloading_degree[]']").value
        };
        if (id) obj.ogi_type_id = row.querySelector("input[name='original_valve_id']")?.value || '';
        payload.degree_rows.push(obj);
    });

    const url = id ? `/api/valvesize/update/${id}/` : '/api/valvesize/add/';
    const originalText = saveBtn.innerText;
    saveBtn.disabled = true;
    saveBtn.innerText = "Processing...";
    DialogManager.loading("Processing...", "Please wait");

    try {
        const resp = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRFToken() },
            body: JSON.stringify(payload)
        });
        const res = await resp.json();
        DialogManager.closeLoading();
        if (res.status === "success" || res.ok || res.success) {
            DialogManager.toast({ type: "success", message: res.message || "Operation successful" });
            const modal = bootstrap.Modal.getInstance(document.getElementById("valveModal"));
            if (modal) modal.hide();
            loadValvesize();
        } else {
            DialogManager.toast({ type: "error", message: res.message || "Error occurred" });
        }
    } catch (err) {
        DialogManager.closeLoading();
        DialogManager.toast({ type: "error", message: "Network connection error" });
    } finally {
        saveBtn.disabled = false;
        saveBtn.innerText = originalText;
    }
}

function delete_valve(id) {
    DialogManager.confirmAction({
        title: "Delete?",
        text: "Are you sure you want to delete this valve size?",
        confirmText: "Yes, Delete",
        url: `/api/valvesize/delete/${id}/`,
        method: "POST",
        onSuccess: () => loadValvesize()
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.table-container-wrapper');
    if (container) {
        SUPERUSER_LEVEL = parseInt(container.dataset.superuserLevel) || 0;
    }

    const savedPage = localStorage.getItem('valveSizePage');
    const savedPPI = localStorage.getItem('valveSizePPI');
    if (savedPage) currentPage = parseInt(savedPage);
    if (savedPPI) itemsPerPage = parseInt(savedPPI);

    loadValvesize();
    initSearchToggle();
    get_all_vlaves();
    get_enable_categoryies();

    valveValidator = new FormValidator('valveForm', {
        size_id_input: {
            rules: [ValidationRules.required],
            asyncRule: (val, signal, form) => new Promise((resolve) => {
                setTimeout(() => {
                    const currentId = form.querySelector('[name="size_id"]')?.value;
                    const exists = allValves.some(item => {
                        if (currentId && (String(item.SIZE_ID) === String(currentId) || String(item.size_id) === String(currentId))) return false;
                        return String(item.SIZE_ID) === String(val) || String(item.size_id) === String(val);
                    });
                    resolve(exists ? "Size ID already exists" : true);
                }, 300);
            })
        },
        status: {
            rules: [ValidationRules.required]
        },
        name: { rules: [ValidationRules.required] },
        part_no: { rules: [ValidationRules.required] },
        part_name: { rules: [ValidationRules.required] }
    });

    const form = document.getElementById('valveForm');
    if (form) form.addEventListener('submit', handleFormSubmit);
});
