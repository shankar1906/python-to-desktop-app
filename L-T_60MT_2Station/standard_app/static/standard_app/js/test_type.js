let testTypes = [];
let categoryOptions = [];
let searchQuery = '';
let sortColumn = -1;
let sortDirection = 'asc';
let filteredData = [];
let validator;

function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : "";
}

function loadTestTypes() {
    fetch('/api/testtype/testtypes/')
        .then(r => r.json())
        .then(data => {
            if (data.error) {
                return DialogManager.toast({ type: 'error', message: data.error });
            }
            testTypes = data.testtypes || [];
            categoryOptions = data.categories || [];
            renderTable();
        })
        .catch(err => {
            console.error(err);
            DialogManager.toast({ type: 'error', message: 'Failed to load test types.' });
        });
}

window.updateInMemory = function (id, field, value) {
    const index = testTypes.findIndex(t => t.test_type_id == id);
    if (index !== -1) {
        testTypes[index][field] = value;
    }
};

window.handleStatusChange = function (selectElement, id) {
    const newStatus = selectElement.value;
    window.updateInMemory(id, 'status', newStatus);
    selectElement.className = 'form-select ' + (newStatus === 'ENABLE' ? 'status-enabled' : 'status-disabled');
};

window.handleCategoryChange = function (selectElement, id) {
    let newCategoryId = selectElement.value;
    if (newCategoryId === 'NONE' || newCategoryId === 'None' || newCategoryId === 'none') {
        newCategoryId = '';
    }
    window.updateInMemory(id, 'category_id', newCategoryId);
    if (newCategoryId && newCategoryId !== '') {
        selectElement.style.border = '';
        selectElement.classList.remove('is-invalid');
    }
};

function renderTable() {
    const tbody = document.getElementById("testTypeTableBody");
    if (!tbody) return;
    filteredData = testTypes.filter(tt => {
        if (!searchQuery) return true;
        const q = searchQuery.toLowerCase();
        return [tt.test_type_id, tt.test_name, tt.category_name, tt.status].join(' ').toLowerCase().includes(q);
    });

    if (sortColumn >= 0) {
        filteredData.sort((a, b) => {
            let va, vb;
            if (sortColumn === 0) { va = a.test_type_id; vb = b.test_type_id; }
            else if (sortColumn === 1) { va = (a.test_name || '').toLowerCase(); vb = (b.test_name || '').toLowerCase(); }
            else if (sortColumn === 2) { va = (a.category_name || '').toLowerCase(); vb = (b.category_name || '').toLowerCase(); }
            else if (sortColumn === 3) { va = (a.status || '').toLowerCase(); vb = (b.status || '').toLowerCase(); }
            if (va < vb) return sortDirection === 'asc' ? -1 : 1;
            if (va > vb) return sortDirection === 'asc' ? 1 : -1;
            return 0;
        });
    }

    tbody.innerHTML = '';
    if (filteredData.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" class="text-center text-muted py-4">No test types found</td></tr>`;
    } else {
        filteredData.forEach(tt => {
            tbody.appendChild(createRow(tt));
        });
    }
}

function createRow(tt) {
    const row = document.createElement('tr');
    const id = tt.test_type_id;
    const currentCategoryId = tt.category_id || '';
    const catOpts = categoryOptions.length ? categoryOptions.map(c =>
        `<option value="${c.id}" ${String(c.id) === String(currentCategoryId) ? 'selected' : ''}>${c.name}</option>`
    ).join('') : '';

    row.innerHTML = `
    <td class="text-end pe-3">${tt.test_type_id}</td>
    <td>
      <input type="text" class="form-control" value="${tt.test_name}" 
        onblur="checkDuplicate(this); window.updateInMemory(${id}, 'test_name', this.value)">
      <div class="invalid-feedback"></div>
    </td>
    <td>
      <select class="form-select" onchange="handleCategoryChange(this, ${id})">
         <option value="" ${currentCategoryId === '' ? 'selected' : ''}>None</option>
         ${catOpts}
      </select>
    </td>
    <td>
      <select class="form-select ${tt.status === 'ENABLE' ? 'status-enabled' : 'status-disabled'}" 
        onchange="handleStatusChange(this, ${id})">
         <option value="ENABLE" ${tt.status === 'ENABLE' ? 'selected' : ''}>Enable</option>
         <option value="DISABLE" ${tt.status === 'DISABLE' ? 'selected' : ''}>Disable</option>
      </select>
    </td>
  `;
    return row;
}

window.markError = function (input, msg) {
    input.classList.add('is-invalid');
    const fb = input.parentNode.querySelector('.invalid-feedback');
    if (fb) { fb.textContent = msg; fb.style.display = 'block'; }
    return false;
};

window.clearError = function (input) {
    input.classList.remove('is-invalid');
    const fb = input.parentNode.querySelector('.invalid-feedback');
    if (fb) { fb.style.display = 'none'; }
    return true;
};

window.checkDuplicate = function (input) {
    const val = input.value.trim();
    if (!val) return window.markError(input, 'Required');
    const valLow = val.toLowerCase();
    const row = input.closest('tr');
    const idText = row.cells[0].textContent.trim();
    const currentId = parseInt(idText);
    if (testTypes.some(t => t.test_type_id !== currentId && t.test_name.trim().toLowerCase() === valLow)) {
        return window.markError(input, 'Duplicate Name');
    }
    window.clearError(input);
    return true;
};

window.submitForm = function () {
    let hasError = false;
    const items = [];
    const errors = [];
    document.querySelectorAll('.form-control, .form-select').forEach(el => {
        el.classList.remove('is-invalid');
        el.style.border = '';
    });
    const tbody = document.getElementById('testTypeTableBody');
    const rows = tbody.querySelectorAll('tr');
    testTypes.forEach((t, index) => {
        const row = rows[index];
        if (!row) return;
        const nameInput = row.querySelector('input[type="text"]');
        const categorySelect = row.querySelectorAll('select')[0];
        const statusSelect = row.querySelectorAll('select')[1];
        if (!t.test_name || !t.test_name.trim()) {
            hasError = true;
            errors.push(`Row ${index + 1}: Test name is required`);
            if (nameInput) { nameInput.classList.add('is-invalid'); nameInput.style.border = '2px solid #dc3545'; }
        }
        if (t.test_name && t.test_name.trim()) {
            const nameLow = t.test_name.trim().toLowerCase();
            const count = testTypes.filter(x => x.test_name && x.test_name.trim().toLowerCase() === nameLow).length;
            if (count > 1) {
                hasError = true;
                errors.push(`Row ${index + 1}: Duplicate test name "${t.test_name}"`);
                if (nameInput) { nameInput.classList.add('is-invalid'); nameInput.style.border = '2px solid #dc3545'; }
            }
        }
        if (t.status === 'ENABLE' && (!t.category_id || t.category_id === '' || t.category_id === 'NONE')) {
            hasError = true;
            errors.push(`Row ${index + 1}: Please select a category when enabling this test type`);
            if (categorySelect) { categorySelect.classList.add('is-invalid'); categorySelect.style.border = '2px solid #dc3545'; }
            if (statusSelect) { statusSelect.style.border = '2px solid #ffc107'; }
        }
        items.push(t);
    });

    if (hasError) {
        const errorList = errors.map(err => `• ${err}`).join('<br>');
        const errorHtml = `
      <div style="text-align: left; max-height: 400px; overflow-y: auto;">
        <strong style="color: #dc3545; font-size: 1.1em;">⚠️ Validation Failed</strong>
        <div style="margin-top: 10px; padding: 10px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;">
          ${errorList}
        </div>
      </div>
    `;
        DialogManager.alert({ title: 'Validation Errors', message: errorHtml, type: 'error' });
        const firstError = document.querySelector('.is-invalid');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            setTimeout(() => firstError.focus(), 300);
        }
        return;
    }

    DialogManager.loading("Saving...", "Updating test types");
    fetch('/api/testtype/testtypes/update/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCSRFToken() },
        body: JSON.stringify({ items })
    })
        .then(r => r.json())
        .then(res => {
            DialogManager.closeLoading();
            if (res.error) DialogManager.toast({ type: 'error', message: res.error });
            else { DialogManager.toast({ type: 'success', message: res.message || 'Updated Successfully' }); loadTestTypes(); }
        })
        .catch(err => {
            DialogManager.closeLoading();
            console.error(err);
            DialogManager.toast({ type: 'error', message: 'Network Error' });
        });
};

document.addEventListener('DOMContentLoaded', () => {
    loadTestTypes();
    document.querySelectorAll('th.sortable').forEach(header => {
        header.addEventListener('click', () => {
            const col = parseInt(header.dataset.column);
            if (sortColumn === col) sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
            else { sortColumn = col; sortDirection = 'asc'; }
            document.querySelectorAll('th.sortable i').forEach(i => i.className = 'fas fa-sort');
            const icon = header.querySelector('i');
            icon.className = sortDirection === 'asc' ? 'fas fa-sort-up' : 'fas fa-sort-down';
            renderTable();
        });
    });
});
