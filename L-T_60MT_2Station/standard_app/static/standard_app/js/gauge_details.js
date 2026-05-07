let existingSerials = [];
let hasUnsavedChanges = false;
let SUPERUSER_LEVEL = 0;
let validator;

function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : "";
}

function loadGauges() {
    fetch("/api/gauge_details/")
        .then(r => r.json())
        .then(data => {
            if (data.error) {
                return DialogManager.toast({ type: 'error', message: data.error });
            }
            existingSerials = data.existing_serials || [];
            renderTable(data.gauges || []);
        })
        .catch(err => {
            console.error(err);
            DialogManager.toast({ type: 'error', message: 'Failed to load gauges.' });
        });
}

function renderTable(gauges) {
    const tbody = document.getElementById("gaugeTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    if (gauges.length === 0) {
        tbody.appendChild(createRow(null));
    } else {
        gauges.forEach(g => {
            tbody.appendChild(createRow(g));
        });
    }

    hasUnsavedChanges = false;
    updateAddButtonState();
    setTimeout(checkAllOverdueRows, 200);
}

function createRow(g) {
    const row = document.createElement('tr');
    const tbody = document.getElementById("gaugeTableBody");
    const currentRowCount = tbody ? tbody.rows.length : 0;

    let firstColumnContent = '';
    if (SUPERUSER_LEVEL === 2) {
        firstColumnContent = g ? g.gd_id : 'Auto';
    } else {
        firstColumnContent = currentRowCount + 1;
    }

    row.innerHTML = `
    <td class="text-end pe-3">
      ${firstColumnContent}
      <input type="hidden" name="gd_id[]" value="${g ? g.gd_id : ''}">
    </td>
    <td>
      <input type="text" class="form-control" name="gd_serial_number[]" 
             value="${g ? g.gd_serial_number : ''}" placeholder="Enter Serial No" 
             onblur="checkDuplicateSerial(this)" oninput="clearError(this); trackChanges()">
      <div class="invalid-feedback"></div>
    </td>
    <td>
      <select class="form-select" name="gd_medium[]" onchange="clearError(this); trackChanges()">
        <option value="">Select</option>
        <option value="Air" ${g && g.gd_medium === 'Air' ? 'selected' : ''}>Air</option>
        <option value="Hydro" ${g && g.gd_medium === 'Hydro' ? 'selected' : ''}>Hydro</option>
        <option value="Gas" ${g && g.gd_medium === 'Gas' ? 'selected' : ''}>Gas</option>
      </select>
      <div class="invalid-feedback">Required</div>
    </td>
    <td>
      <input type="text" class="form-control" name="gd_pressure_range_psi[]" 
             value="${g ? g.gd_pressure_range_psi : ''}" placeholder="e.g. 0-100" 
             oninput="clearError(this); trackChanges()">
      <div class="invalid-feedback"></div>
    </td>
    <td>
      <input type="text" class="form-control" name="gd_pressure_range_bar[]" 
             value="${g ? g.gd_pressure_range_bar : ''}" placeholder="e.g. 0-7" 
             oninput="clearError(this); trackChanges()">
      <div class="invalid-feedback"></div>
    </td>
    <td>
      <input type="text" class="form-control" name="gd_pressure_range_kgcm2[]" 
             value="${g ? g.gd_pressure_range_kgcm2 : ''}" placeholder="e.g. 0-7" 
             oninput="clearError(this); trackChanges()">
      <div class="invalid-feedback"></div>
    </td>
    <td>
      <input type="date" class="form-control done-date" name="gd_done_date[]" 
             value="${g ? g.gd_done_date : ''}" onblur="validateDates(this)" onchange="clearError(this); validateDates(this); trackChanges(); checkOverdueStatus(this)">
      <div class="invalid-feedback">Required</div>
    </td>
    <td>
      <input type="date" class="form-control due-date" name="gd_due_date[]" 
             value="${g ? g.gd_due_date : ''}" onblur="validateDates(this)" onchange="clearError(this); validateDates(this); trackChanges(); checkOverdueStatus(this)">
      <div class="invalid-feedback">Required</div>
    </td>
    <td>
      <select class="form-select station-select" name="gd_station_id[]" onchange="clearError(this); validateStationRowCount(this); trackChanges();">
        <option value="">Select</option>
        <option value="1" ${g && g.gd_station_id == 1 ? 'selected' : ''}>Station 1</option>
        <option value="2" ${g && g.gd_station_id == 2 ? 'selected' : ''}>Station 2</option>
      </select>
      <div class="invalid-feedback">Required</div>
    </td>
    <td>
      <select class="form-select status-select ${g && g.gd_status == 1 ? 'status-enabled' : (g && g.gd_status == 0 ? 'status-disabled' : '')}" 
        name="gd_status[]" 
        onchange="clearStatusError(this); trackChanges(); checkOverdueStatus(this); updateStatusClass(this);">
        <option value="">Select</option>
        <option value="1" ${g && g.gd_status == 1 ? 'selected' : ''}>Enable</option>
        <option value="0" ${g && g.gd_status == 0 ? 'selected' : ''}>Disable</option>
      </select>
      <div class="invalid-feedback">Required</div>
    </td>
    <td class="text-center">
      <button type="button" class="btn-icon delete" onclick="removeRow(this)" title="Delete">
        <i class="fas fa-trash-alt"></i>
      </button>
    </td>
  `;
    return row;
}

window.updateStatusClass = function (select) {
    select.className = 'form-select status-select ' + (select.value === '1' ? 'status-enabled' : (select.value === '0' ? 'status-disabled' : ''));
    validateStationRowCountOnStatusChange(select);
};

window.clearStatusError = function (select) {
    clearError(select);
};

window.addRow = function () {
    const tbody = document.getElementById("gaugeTableBody");
    if (!tbody) return;
    tbody.appendChild(createRow(null));
    hasUnsavedChanges = true;
    const container = document.querySelector('.table-responsive');
    if (container) container.scrollTop = container.scrollHeight;
};

window.removeRow = function (btn) {
    const tbody = document.getElementById("gaugeTableBody");
    if (!tbody) return;
    if (tbody.rows.length <= 1) {
        DialogManager.toast({ type: 'warning', message: 'Cannot delete the last row. At least one row must remain.' });
        return;
    }
    const row = btn.closest('tr');
    const idInput = row.querySelector('input[name="gd_id[]"]');
    const id = idInput ? idInput.value : '';
    if (id) {
        DialogManager.confirmAction({
            title: "Delete Gauge?",
            text: "Delete this gauge from the database?",
            confirmText: "Yes, Delete",
            url: `/api/gauge_details/delete/${id}/`,
            method: 'POST',
            onSuccess: () => {
                row.remove();
                hasUnsavedChanges = false;
                setTimeout(updateAddButtonState, 100);
            }
        });
    } else {
        row.remove();
        hasUnsavedChanges = false;
        setTimeout(updateAddButtonState, 100);
    }
};

window.trackChanges = function () {
    hasUnsavedChanges = true;
    setTimeout(updateAddButtonState, 100);
};

function updateAddButtonState() {
    const addBtn = document.getElementById('addRowBtn');
    if (addBtn) {
        addBtn.disabled = false;
        addBtn.title = "Add Row";
    }
}

window.checkOverdueStatus = function (element) {
    const row = element.closest('tr');
    if (!row) return;
    const dueInput = row.querySelector('.due-date');
    const statusSelect = row.querySelector('.status-select');
    if (!dueInput || !statusSelect) return;
    const dueDate = dueInput.value;
    const status = statusSelect.value;
    if (dueDate && (status === '1' || status === '0')) {
        const today = new Date(); today.setHours(0, 0, 0, 0);
        const due = new Date(dueDate); due.setHours(0, 0, 0, 0);
        if (due < today) row.classList.add('overdue-row');
        else row.classList.remove('overdue-row');
    } else {
        row.classList.remove('overdue-row');
    }
};

function checkAllOverdueRows() {
    const tbody = document.getElementById("gaugeTableBody");
    if (!tbody) return;
    const rows = tbody.querySelectorAll('tr');
    rows.forEach(row => {
        const dueInput = row.querySelector('.due-date');
        if (dueInput) window.checkOverdueStatus(dueInput);
    });
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

window.checkDuplicateSerial = function (input) {
    const val = input.value.trim();
    if (!val) return window.markError(input, 'Required');
    const allInputs = document.querySelectorAll('input[name="gd_serial_number[]"]');
    for (let inp of allInputs) {
        if (inp !== input && inp.value.trim().toLowerCase() === val.toLowerCase()) {
            return window.markError(input, 'Duplicate in table');
        }
    }
    const row = input.closest('tr');
    const idInput = row.querySelector('input[name="gd_id[]"]');
    const id = idInput ? idInput.value : '';
    const url = `/api/gauge_details/check-serial/?serial=${encodeURIComponent(val)}` + (id ? `&exclude_id=${id}` : '');
    fetch(url).then(r => r.json()).then(d => {
        if (d.exists) window.markError(input, 'Exists in DB');
        else window.clearError(input);
    });
};

window.validateDates = function (input) {
    const row = input.closest('tr');
    if (!row) return;
    const doneInp = row.querySelector('.done-date');
    const dueInp = row.querySelector('.due-date');
    const statusSelect = row.querySelector('.status-select');
    const done = doneInp.value ? new Date(doneInp.value) : null;
    const due = dueInp.value ? new Date(dueInp.value) : null;
    const today = new Date(); today.setHours(0, 0, 0, 0);
    const tomorrow = new Date(today); tomorrow.setDate(tomorrow.getDate() + 1);
    const status = statusSelect.value;
    window.clearError(doneInp);
    window.clearError(dueInp);
    if (status === '1') {
        if (done && due) {
            const minDueDate = new Date(done);
            minDueDate.setDate(minDueDate.getDate() + 1);
            if (due < minDueDate) return window.markError(dueInp, 'Must be at least 1 day after Done Date');
        }
        if (due && due < tomorrow) return window.markError(dueInp, 'Must be from tomorrow onwards');
        if (due && !done) return window.markError(doneInp, 'Required if Due Set');
    }
};

window.validateStationRowCount = function (select) {
    validateCount(select.value, select);
};

window.validateStationRowCountOnStatusChange = function (select) {
    if (select.value !== '1') return;
    const row = select.closest('tr');
    if (!row) return;
    const stSel = row.querySelector('.station-select');
    const doneInp = row.querySelector('.done-date');
    const dueInp = row.querySelector('.due-date');
    const done = doneInp.value ? new Date(doneInp.value) : null;
    const due = dueInp.value ? new Date(dueInp.value) : null;
    const today = new Date(); today.setHours(0, 0, 0, 0);
    const tomorrow = new Date(today); tomorrow.setDate(tomorrow.getDate() + 1);
    let dateError = false;
    if (done && due) {
        const minDueDate = new Date(done);
        minDueDate.setDate(minDueDate.getDate() + 1);
        if (due < minDueDate) dateError = true;
    }
    if (due && due < tomorrow) dateError = true;
    if (dateError) {
        DialogManager.toast({ type: 'warning', message: 'Please fix the due date first. Due date must be at least 1 day after done date and from tomorrow onwards.' });
        select.value = "0";
        select.className = 'form-select status-select status-disabled';
        return;
    }
    if (stSel && stSel.value) validateCount(stSel.value, select);
};

function validateCount(stationId, triggerElement) {
    if (!stationId) return;
    let count = 0;
    document.querySelectorAll('#gaugeTableBody tr').forEach(r => {
        const s = r.querySelector('.station-select').value;
        const st = r.querySelector('.status-select').value;
        if (s === stationId && st === '1') count++;
    });
    if (count > 10) {
        DialogManager.toast({ type: 'warning', message: `Station ${stationId} limit exceeded (Max 10).` });
        triggerElement.value = "";
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.table-container-wrapper');
    if (container) {
        SUPERUSER_LEVEL = parseInt(container.dataset.superuserLevel) || 0;
    }
    loadGauges();

    const form = document.getElementById('gaugeForm');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const invis = document.querySelectorAll('.is-invalid');
            if (invis.length > 0) return DialogManager.toast({ type: 'error', message: 'Please fix validation errors.' });

            const tbody = document.getElementById("gaugeTableBody");
            const rows = tbody.querySelectorAll('tr');
            let hasError = false;
            let hasContent = false;
            rows.forEach(row => {
                const serial = row.querySelector('input[name="gd_serial_number[]"]').value.trim();
                const medium = row.querySelector('select[name="gd_medium[]"]').value;
                const rangePsi = row.querySelector('input[name="gd_pressure_range_psi[]"]').value.trim();
                const rangeBar = row.querySelector('input[name="gd_pressure_range_bar[]"]').value.trim();
                const rangeKgcm2 = row.querySelector('input[name="gd_pressure_range_kgcm2[]"]').value.trim();
                const done = row.querySelector('.done-date').value;
                const due = row.querySelector('.due-date').value;
                const station = row.querySelector('.station-select').value;
                const status = row.querySelector('.status-select').value;
                const isEmpty = !serial && !medium && !rangePsi && !rangeBar && !rangeKgcm2 && !done && !due && !station && !status;
                const hasAnyValue = serial || medium || rangePsi || rangeBar || rangeKgcm2 || done || due || station || status;
                if (isEmpty) {
                    const inputs = row.querySelectorAll('input.form-control, select.form-select');
                    inputs.forEach(el => {
                        if (!el.closest('td').classList.contains('d-none')) { window.markError(el, 'Required'); hasError = true; }
                    });
                    return;
                }
                if (hasAnyValue) {
                    hasContent = true;
                    const inputs = row.querySelectorAll('input.form-control, select.form-select');
                    inputs.forEach(el => {
                        if (!el.value && !el.closest('td').classList.contains('d-none')) { window.markError(el, 'Required'); hasError = true; }
                    });
                }
            });
            if (hasError) return DialogManager.toast({ type: 'error', message: 'Fill all fields for active rows.' });
            if (!hasContent) return DialogManager.toast({ type: 'warning', message: 'No data to save.' });
            DialogManager.loading("Saving...", "Processing details");
            const fd = new FormData(form);
            fetch('/api/gauge_details/save/', {
                method: 'POST',
                headers: { 'X-CSRFToken': getCSRFToken() },
                body: fd
            })
                .then(r => r.json())
                .then(res => {
                    DialogManager.closeLoading();
                    if (res.success) {
                        DialogManager.toast({ type: 'success', message: 'Saved successfully.' });
                        hasUnsavedChanges = false;
                        loadGauges();
                    } else {
                        DialogManager.toast({ type: 'error', message: res.error || 'Save failed.' });
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
