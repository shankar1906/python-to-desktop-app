let SUPERUSER_LEVEL = 0;
let validator;

function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : "";
}

function loadCategories() {
    fetch("/api/category/")
        .then(r => r.json())
        .then(data => {
            if (data.status === 'error') {
                return DialogManager.toast({ type: 'error', message: data.message || 'Error loading data' });
            }
            renderTable(data.categories || []);
        })
        .catch(err => {
            console.error(err);
            DialogManager.toast({ type: 'error', message: 'Failed to load categories.' });
        });
}

function renderTable(categories) {
    const tbody = document.getElementById("categoryTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    if (categories.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted">No categories found</td></tr>';
    } else {
        categories.forEach((c, index) => {
            tbody.appendChild(createRow(c, index));
        });
    }
}

function createRow(c, index) {
    const row = document.createElement('tr');
    const firstColumnContent = SUPERUSER_LEVEL === 2 ? c.id : (index + 1);

    row.innerHTML = `
    <td class="text-end pe-3">
      <input type="hidden" name="category_id[]" value="${c.id}">
      ${firstColumnContent}
    </td>
    <td>
      <input type="text" class="form-control" name="testname[]" value="${c.category_name}" onblur="checkDuplicate(this)">
      <div class="invalid-feedback"></div>
    </td>
    <td>
      <select class="form-select" name="medium[]">
        <option value="" ${!c.medium || c.medium === '' ? 'selected' : ''}>Select</option>
        <option value="Air" ${c.medium === 'Air' ? 'selected' : ''}>Air</option>
        <option value="Hydro" ${c.medium === 'Hydro' ? 'selected' : ''}>Hydro</option>
        <option value="Gas" ${c.medium === 'Gas' ? 'selected' : ''}>Gas</option>
      </select>
    </td>
    <td>
      <select class="form-select ${c.status === 'ENABLE' ? 'status-enabled' : 'status-disabled'}" name="status[]"
        onchange="this.className = 'form-select ' + (this.value === 'ENABLE' ? 'status-enabled' : 'status-disabled');">
        <option value="ENABLE" ${c.status === 'ENABLE' ? 'selected' : ''}>Enable</option>
        <option value="DISABLE" ${c.status === 'DISABLE' ? 'selected' : ''}>Disable</option>
      </select>
    </td>
  `;
    return row;
}

window.markError = function (input, msg) {
    input.classList.add('is-invalid');
    const fb = input.parentNode.querySelector('.invalid-feedback');
    if (fb) { fb.textContent = msg; fb.style.display = 'block'; }
};

window.clearError = function (input) {
    input.classList.remove('is-invalid');
    const fb = input.parentNode.querySelector('.invalid-feedback');
    if (fb) { fb.style.display = 'none'; }
};

window.checkDuplicate = function (input) {
    const val = input.value.trim();
    if (!val) {
        window.markError(input, 'Category name required');
        return false;
    }
    const valLower = val.toLowerCase();
    let found = false;
    const allInputs = document.querySelectorAll('input[name="testname[]"]');
    allInputs.forEach(el => {
        if (el !== input && el.value.trim().toLowerCase() === valLower) found = true;
    });
    if (found) {
        window.markError(input, 'Duplicate Name');
        return false;
    } else {
        window.clearError(input);
        return true;
    }
};

document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.table-container-wrapper');
    if (container) {
        SUPERUSER_LEVEL = parseInt(container.dataset.superuserLevel) || 0;
    }
    loadCategories();

    const form = document.getElementById('categoryForm');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            let hasError = false;
            const inputs = document.querySelectorAll('input[name="testname[]"]');
            inputs.forEach(input => {
                if (!window.checkDuplicate(input)) hasError = true;
            });
            if (hasError) return DialogManager.toast({ type: 'error', message: 'Please fix validation errors.' });

            const rows = document.querySelectorAll('#categoryTableBody tr');
            const errors = [];
            rows.forEach((row, index) => {
                const statusSelect = row.querySelector('select[name="status[]"]');
                const mediumSelect = row.querySelector('select[name="medium[]"]');
                if (statusSelect && mediumSelect) {
                    if (statusSelect.value === 'ENABLE' && (!mediumSelect.value || mediumSelect.value === '')) {
                        hasError = true;
                        errors.push(`Row ${index + 1}: Please select a medium when category is enabled`);
                        mediumSelect.classList.add('is-invalid');
                    } else {
                        mediumSelect.classList.remove('is-invalid');
                    }
                }
            });

            if (hasError && errors.length > 0) {
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
                return;
            }

            DialogManager.loading("Saving...", "Updating categories");
            const ids = Array.from(document.querySelectorAll('input[name="category_id[]"]')).map(el => el.value);
            const names = Array.from(inputs).map(el => el.value);
            const mediums = Array.from(document.querySelectorAll('select[name="medium[]"]')).map(el => el.value);
            const statuses = Array.from(document.querySelectorAll('select[name="status[]"]')).map(el => el.value);
            const payload = { category_ids: ids, testnames: names, mediums: mediums, statuses: statuses };

            fetch("/api/category/", {
                method: "POST",
                headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRFToken() },
                body: JSON.stringify(payload)
            })
                .then(r => r.json())
                .then(data => {
                    DialogManager.closeLoading();
                    if (data.status === 'success') {
                        DialogManager.toast({ type: 'success', message: data.message });
                        loadCategories();
                    } else {
                        DialogManager.toast({ type: 'error', message: data.message || 'Error updating categories' });
                    }
                })
                .catch(err => {
                    DialogManager.closeLoading();
                    console.error(err);
                    DialogManager.toast({ type: 'error', message: 'Network Error' });
                });
        });
    }
});
