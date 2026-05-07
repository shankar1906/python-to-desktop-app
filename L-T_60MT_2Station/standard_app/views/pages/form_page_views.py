from django.shortcuts import render
from standard_app.decorators import login_required
from standard_app.services.form_service import get_valve_size, get_valve_class, get_valve_standard, get_valve_type, get_shell_material, get_assemblers, get_testers
from standard_app.services.valve_details_service import ValveDetailsService
from standard_app.services.item_details_service import ItemDetailsService


def build_form_context():
    valve_standards = get_valve_standard()
    valve_sizes = get_valve_size()
    valve_classes = get_valve_class()
    valve_types = get_valve_type()
    shell_materials = get_shell_material()
    assemblers = get_assemblers()
    testers = get_testers()
    # Still passed to sap_form.html; dual-station form.html no longer shows Duration Type
    duration_types = ["IOGP", "Non IOGP"]
    valve_details = [vd for vd in ValveDetailsService.get_all_valve_details() if (vd.get('status') or '').lower() == 'enabled']

    _dropdown_sources = {
        'assembled by': assemblers,
        'witnessed by': assemblers,
        'tested by': testers,
        'applicability': ['ARAMCO', 'NON-ARAMCO'],
        'stem orient': ['Vertical', 'Horizontal'],
        'steam orient': ['Vertical', 'Horizontal'],
        'shift': ['Shift 1', 'Shift 2', 'Shift 3'],
    }
    top_header_fields = []
    normal_fields = []
    for vd in valve_details:
        col = vd.get('column_name') or ''
        col_lower = col.lower()
        vd['dropdown_options'] = _dropdown_sources.get(col_lower, [])
        vd['field_id'] = col_lower.replace(' ', '').replace('/', '').replace('.', '')
        if vd.get('is_top_header') in (1, True, '1'):
            top_header_fields.append(vd)
        else:
            normal_fields.append(vd)

    def _top_order(vd):
        col = (vd.get('column_name') or '').lower()
        return (0 if col == 'serial number' else 1 if col == 'assembly id' else 2)

    top_header_fields.sort(key=_top_order)

    def _field_name(vd, suffix):
        col = (vd.get('column_name') or '').lower()
        if col == 'serial number' or col == 'valve serial no':
            if suffix == 's1':
                return 'VALVE_SER_NO'
            elif suffix == 's2':
                return 'VALVE_SER_NO_s2'
            elif suffix == 's3':
                return 'VALVE_SER_NO_s3'
            elif suffix == 's4':
                return 'VALVE_SER_NO_s4'
        if col == 'assembly id':
            if suffix == 's1':
                return 'ASSEMBLY_NO_s1'
            elif suffix == 's2':
                return 'ASSEMBLY_NO_s2'
            elif suffix == 's3':
                return 'ASSEMBLY_NO_s3'
            elif suffix == 's4':
                return 'ASSEMBLY_NO_s4'
        return vd.get('column_name')

    # Filter out ASSEMBLY_NO fields as they are removed from the form
    mandatory_fields_s1 = [_field_name(vd, 's1') for vd in valve_details if vd.get('is_mandatory') in (1, True, '1') and vd.get('column_name', '').lower() != 'assembly id']
    mandatory_fields_s2 = [_field_name(vd, 's2') for vd in valve_details if vd.get('is_mandatory') in (1, True, '1') and vd.get('column_name', '').lower() != 'assembly id']
    mandatory_fields_s3 = [_field_name(vd, 's3') for vd in valve_details if vd.get('is_mandatory') in (1, True, '1') and vd.get('column_name', '').lower() != 'assembly id']
    mandatory_fields_s4 = [_field_name(vd, 's4') for vd in valve_details if vd.get('is_mandatory') in (1, True, '1') and vd.get('column_name', '').lower() != 'assembly id']

    item_details_all = ItemDetailsService.get_all_item_details()
    item_details_columns = [item for item in item_details_all if (item.get('status') or '').lower() == 'enabled']
    
    # Process item details to structure them by rows for the template
    # Pivot from Columns -> Rows to Rows -> Columns
    max_rows = 0
    for col in item_details_columns:
        if isinstance(col.get('row_details'), list):
            max_rows = max(max_rows, len(col['row_details']))

    # Process item details to structure them for the template
    # New logic: Transpose so Column Names are side labels and Row Labels are top headers
    
    # 1. Identify all unique row labels (collected from field_names across all columns)
    item_header_labels = []
    fallback_names = ['Body 1 / Upper', 'Bottom / Plug', 'Disc', 'Seat Retainer', 'Stem 1 / Upper'] # Keep fallback_names here as it's used in this block
    for i in range(max_rows):
        label = ""
        # Try to find a field name for this row index across all columns
        for col in item_details_columns:
            details = col.get('row_details', [])
            if i < len(details) and details[i].get('field_name'):
                label = details[i].get('field_name')
                break
        
        # Fallback if field_name is missing
        if not label:
            if i < len(fallback_names):
                label = fallback_names[i]
            else:
                label = f"Item {i+1}"
        item_header_labels.append(label)

    # 2. Build rows structure where each row corresponds to a column_name
    item_rows_structure = []
    for col in item_details_columns:
        row_data = {
            'label': col.get('column_name'),
            'columns': []
        }
        
        details = col.get('row_details', [])
        for i in range(max_rows):
            field = details[i] if i < len(details) else {}
            row_data['columns'].append({
                'row_label': item_header_labels[i],
                'field': field
            })
        
        item_rows_structure.append(row_data)

    return {
        "valve_standards": valve_standards,
        "valve_sizes": valve_sizes,
        "valve_classes": valve_classes,
        "valve_types": valve_types,
        "shell_materials": shell_materials,
        "duration_types": duration_types,
        "assemblers": assemblers,
        "testers": testers,
        "valve_details": valve_details,
        "top_header_fields": top_header_fields,
        "normal_fields": normal_fields,
        "mandatory_fields_s1": mandatory_fields_s1,
        "mandatory_fields_s2": mandatory_fields_s2,
        "mandatory_fields_s3": mandatory_fields_s3,
        "mandatory_fields_s4": mandatory_fields_s4,
        "item_details_columns": item_details_columns,
        "item_header_labels": item_header_labels,
        "item_rows_structure": item_rows_structure,
    }


@login_required
def form_page(request):
    return render(request, "form.html", build_form_context())