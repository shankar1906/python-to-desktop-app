
from django.shortcuts import render

from pyexpat.errors import messages
import re
from re import M
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import DatabaseError, connection
from django.utils.safestring import mark_safe
from django.conf import settings
from django.templatetags.static import static
import os
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.db import connection
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from pymodbus.client import ModbusTcpClient
import time
from django.template.loader import render_to_string
from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone
import os
from datetime import datetime
from django.contrib import messages
import base64
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from weasyprint import HTML
from openpyxl import load_workbook, Workbook
from openpyxl.utils import get_column_letter
import io
import zipfile
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date, timedelta
from django.db import connection
import threading
from zeep import Client, Settings
from django.contrib.staticfiles import finders
from django.contrib.auth.hashers import make_password, check_password as check_pwd
import csv
from .decorators import login_required, permission_required, superuser_required
import webbrowser
webbrowser.open("http://127.0.0.1:8000/")
# Create your views here.
def login(request):
    request.session.flush()  
    request.session.referer = request.META.get('HTTP_REFERER', '/')
    request.session['is_authenticated'] = False
    # return redirect('login')
    return render(request, 'login.html')


def new_username(request):
    """Check if username exists and fetch role using raw SQL + cursor"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()

        if not username:
            return JsonResponse({'status': 'error', 'message': 'Username is required'})

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT name, superuser FROM newapp_employee WHERE name = %s",
                [username]
            )
            row = cursor.fetchone()

        if not row:
            return JsonResponse({'status': 'error', 'message': 'Username not found'})

        name, superuser = row
        # request.session['username'] = name
        # request.session['superuser'] = superuser

        return JsonResponse({
            'status': 'success',
            'username': name,
            'superuser': superuser
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



def new_pwd(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            return JsonResponse({'status': 'error', 'message': 'Missing username or password'})

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT name, password, superuser FROM newapp_employee WHERE name = %s",
                    [username]
                )
                row = cursor.fetchone()

            if not row:
                return JsonResponse({'status': 'error', 'message': 'User not found'})

            db_name, db_password, db_superuser = row
            
            
            

            # if password == db_password:
            if check_pwd(password, db_password):
                # Manually set session
                request.session['username'] = db_name
                request.session['superuser'] = db_superuser
                request.session['is_authenticated'] = True  # Mark as fully authenticated

                return JsonResponse({
                    'status': 'success',
                    'username': db_name,
                    'superuser': 'yes' if db_superuser else 'no',
                    'message': 'Login successful!'
                })
            else:
                return JsonResponse({'status': 'error', 'message': 'Incorrect password'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Server error: {str(e)}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        employee_username = request.session.get('username')
        if not employee_username:
            messages.error(request, "Session expired. Please log in again.")
            return redirect('login')

        try:
            # Fetch employee record using raw SQL
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT password FROM newapp_employee WHERE name = %s",
                    [employee_username]
                )
                row = cursor.fetchone()

            if not row:
                messages.error(request, "User not found.")
                return redirect('login')

            db_password = row[0]

            # Check old password using Django's check_password for hashed passwords
            if not check_pwd(old_password, db_password):
                messages.error(request, "Old password is incorrect.")
                return redirect('change_password')

            # Check new/confirm match
            if new_password != confirm_password:
                messages.error(request, "New password and Confirm password do not match.")
                return redirect('change_password')

            # Hash the new password before storing
            hashed_password = make_password(new_password)
            
            # Update password in DB
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE newapp_employee SET password = %s WHERE name = %s",
                    [hashed_password, employee_username]
                )

            messages.success(request, "Password updated successfully.")
            return redirect('dashboard')

        except Exception as e:
            messages.error(request, f"Error updating password: {str(e)}")
            return redirect('change_password')

    # GET request - render change password page
    return render(request, 'dashboard.html')

@login_required
def check_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            old_password = data.get('old_password')
            employee_username = request.session.get('username')

            if not employee_username:
                return JsonResponse({'valid': False, 'error': 'Session expired'})

            with connection.cursor() as cursor:
                cursor.execute("SELECT password FROM newapp_employee WHERE name = %s", [employee_username])
                row = cursor.fetchone()

            if not row:
                return JsonResponse({'valid': False, 'error': 'User not found'})

            db_password = row[0]
            # Use Django's check_password to verify hashed password
            if check_pwd(old_password, db_password):
                return JsonResponse({'valid': True})
            else:
                return JsonResponse({'valid': False, 'error': 'Old password is incorrect'})
        except Exception as e:
            return JsonResponse({'valid': False, 'error': f'Server error: {str(e)}'})
    return JsonResponse({'error': 'Invalid method'}, status=405)

def custom_logout(request):
    request.session.flush()  
    request.session['logout_message'] = "Logout successful"
    return redirect('login')


def check_gauge_due_alert():
    today = date.today()
    alerts = []

    with connection.cursor() as cursor:
        # ✅ Update DUE_ALARM:
        # Overdue or due today => 1, others => 0
        cursor.execute("""
            UPDATE gauge_details
            SET DUE_ALARM = CASE
                WHEN CAL_DUE_DATE IS NULL THEN 0
                WHEN CAL_DUE_DATE <= %s THEN 1
                ELSE 0
            END
            WHERE ACTIVE_STATUS = 1
        """, [today])

        # ✅ Fetch gauges that need attention
        cursor.execute("""
            SELECT INSTRUMENT_SER_NO, CAL_DUE_DATE
            FROM gauge_details
            WHERE ACTIVE_STATUS = 1 AND DUE_ALARM = 1
            ORDER BY CAL_DUE_DATE ASC
        """)
        results = cursor.fetchall()

    # ✅ Build alert messages
    for serial_no, due_date in results:
        if not due_date:
            continue
        if due_date < today:
            alerts.append(f"Gauge {serial_no} is OVERDUE (Due {due_date})")
        elif due_date == today:
            alerts.append(f"Gauge {serial_no} is DUE TODAY ({due_date})")

    return alerts


@login_required
def dashboard(request):
    with connection.cursor() as cursor:
        # Fetch valve types for dropdown
        cursor.execute("SELECT ID, TYPE_NAME FROM VALVE_TYPE ORDER BY TYPE_NAME ASC")
        valve_types = cursor.fetchall()
        
        # Fetch shifts with associated valve type names
        cursor.execute("""
            SELECT s.ID, s.SHIFT_NAME, s.TYPE_ID, vt.TYPE_NAME
            FROM SHIFT s
            LEFT JOIN VALVE_TYPE vt ON s.TYPE_ID = vt.ID
            WHERE s.IS_ACTIVE = 1
            ORDER BY s.SHIFT_NAME ASC
        """)
        shifts = cursor.fetchall()
    
    valve_types_list = [{'id': row[0], 'name': row[1]} for row in valve_types]
    
    shifts_list = []
    for row in shifts:
        shifts_list.append({
            'id': row[0],
            'name': row[1],
            'valve_type_id': row[2],
            'valve_type_name': row[3] or ''
        })

    # ✅ Check and update gauge alerts
    gauge_alerts = check_gauge_due_alert()
    gauge_alerts_exist = len(gauge_alerts) > 0

    return render(request, 'dashboard.html', {
    'valve_types': valve_types_list,
    'shifts': shifts_list,
    'gauge_alerts': gauge_alerts,
    'gauge_alerts_exist': gauge_alerts_exist,
})





@permission_required("Category")
def category(request):
    # ✅ Fetch all 15 categories from DB - Order by STATUS DESC (ENABLE first), then CATEGORY_ID
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT CATEGORY_ID, CATEGORY_NAME, STATUS
            FROM category
            ORDER BY STATUS DESC, CATEGORY_ID
        """)
        categories = cursor.fetchall()

    if request.method == "POST":
        category_ids = request.POST.getlist("category_id[]")
        testnames = request.POST.getlist("testname[]")
        statuses = request.POST.getlist("status[]")

        # ✅ Check for empty category names
        for i, testname in enumerate(testnames, start=1):
            if not testname.strip():
                messages.error(request, f'Category name cannot be empty at row {i}. Please enter a valid name.')
                return redirect("category")

        # ✅ Check for duplicate category names (case-insensitive)
        with connection.cursor() as cursor:
            # Create a set to track seen names (case-insensitive)
            seen_names = set()
            
            for i, (category_id, testname) in enumerate(zip(category_ids, testnames), start=0):
                category_id = int(category_id)  # Convert to int
                testname_lower = testname.strip().lower()
                
                # Check if duplicate within the same request
                if testname_lower in seen_names:
                    messages.error(request, f'Duplicate category name "{testname}" found. Please use unique names.')
                    return redirect("category")
                
                seen_names.add(testname_lower)
                
                # Check for duplicates in database (case-insensitive)
                cursor.execute("""
                    SELECT CATEGORY_ID, CATEGORY_NAME
                    FROM category
                    WHERE LOWER(CATEGORY_NAME) = %s AND CATEGORY_ID != %s
                """, [testname_lower, category_id])
                
                duplicate = cursor.fetchone()
                if duplicate:
                    duplicate_id, duplicate_name = duplicate
                    messages.error(request, f'Category name "{testname}" already exists (found as "{duplicate_name}"). Please use a unique name.')
                    return redirect("category")

        # ✅ Update each record
        with connection.cursor() as cursor:
            for category_id, testname, status in zip(category_ids, testnames, statuses):
                category_id = int(category_id)  # Convert to int
                cursor.execute("""
                    UPDATE category
                    SET CATEGORY_NAME = %s,
                        STATUS = %s,
                        UPDATED_DATE = NOW()
                    WHERE CATEGORY_ID = %s
                """, [testname, status, category_id])

        messages.success(request, "Category details updated successfully!")
        return redirect("category")  # Reload page after update

    # ✅ Prepare data for template
    data = [
        {
            "id": row[0],
            "category_name": row[1],
            "status": row[2],
        }
        for row in categories
    ]

    return render(request, "category.html", {"categories": data})




@permission_required("Test Type")
def test_type(request):
    # ---------------- Get superuser level from session ----------------
    superuser_level = request.session.get('superuser')
    try:
        if superuser_level is None:
            superuser_level = 0
        else:
            superuser_level = int(superuser_level)
    except (ValueError, TypeError):
        superuser_level = 0
    
    # ---------------- Fetch test types - For superuser level 1, only show enabled test types ----------------
    with connection.cursor() as cursor:
        if superuser_level == 1:
            # For superuser level 1, only fetch enabled test types
            cursor.execute("""
                SELECT id, test_id, test_name, medium, category, status
                FROM test_type
                WHERE status = 'ENABLE'
                ORDER BY test_id
            """)
        else:
            # For other superuser levels, fetch all test types
            cursor.execute("""
                SELECT id, test_id, test_name, medium, category, status
                FROM test_type
                ORDER BY STATUS DESC, test_id
            """)
        test_types = cursor.fetchall()

    # ---------------- Fetch category list for dropdown ----------------
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT CATEGORY_NAME
            FROM category
            WHERE STATUS = 'ENABLE'
            ORDER BY CATEGORY_NAME
        """)
        category_list = [row[0] for row in cursor.fetchall()]

    # Add "NONE" option explicitly
    if "NONE" not in category_list:
        category_list.insert(0, "NONE")

    # ---------------- Handle POST updates ----------------
    if request.method == "POST":
        test_ids = request.POST.getlist("test_id[]")
        testnames = request.POST.getlist("testname[]")
        mediums = request.POST.getlist("medium[]")
        categories = request.POST.getlist("category[]")
        statuses = request.POST.getlist("status[]")

        # ✅ Check for empty test names
        for i, testname in enumerate(testnames, start=1):
            if not testname.strip():
                messages.error(request, f'Test name cannot be empty at row {i}. Please enter a valid name.')
                return redirect("test_type")

        # ✅ Check for duplicate test names (case-insensitive)
        with connection.cursor() as cursor:
            # Create a set to track seen names (case-insensitive)
            seen_names = set()
            
            for i, (test_id, testname) in enumerate(zip(test_ids, testnames), start=0):
                test_id = int(test_id)  # Convert to int
                testname_lower = testname.strip().lower()
                
                # Check if duplicate within the same request
                if testname_lower in seen_names:
                    messages.error(request, f'Duplicate test name "{testname}" found. Please use unique names.')
                    return redirect("test_type")
                
                seen_names.add(testname_lower)
                
                # Check for duplicates in database (case-insensitive)
                cursor.execute("""
                    SELECT test_id, test_name
                    FROM test_type
                    WHERE LOWER(test_name) = %s AND test_id != %s
                """, [testname_lower, test_id])
                
                duplicate = cursor.fetchone()
                if duplicate:
                    duplicate_id, duplicate_name = duplicate
                    messages.error(request, f'Test name "{testname}" already exists (found as "{duplicate_name}"). Please use a unique name.')
                    return redirect("test_type")

        with connection.cursor() as cursor:
            for test_id, testname, medium, category, status in zip(
                    test_ids, testnames, mediums, categories, statuses):
                
                test_id = int(test_id)  # Convert to int

                # Initialize column variables
                pressure_column = None
                duration_column = None

                # Only fetch column names if category is not NONE
                if category != "NONE":
                    cursor.execute("""
                        SELECT PRESSURE_COLUMN_NAME, DURATION_COLUMN_NAME
                        FROM category
                        WHERE CATEGORY_NAME = %s
                    """, (category,))
                    row = cursor.fetchone()
                    if row:
                        pressure_column, duration_column = row

                # Update test_type safely
                cursor.execute("""
                    UPDATE test_type
                    SET test_name = %s,
                        medium = %s,
                        category = %s,
                        status = %s,
                        pre_col_name = %s,
                        dur_col_name = %s,
                        updated_at = NOW()
                    WHERE test_id = %s
                """, [testname, medium, category, status, pressure_column, duration_column, test_id])

        messages.success(request, "Test Type details updated successfully!")
        return redirect("test_type")  # Reload page after update

    # ---------------- Prepare data for template ----------------
    data = [
        {
            "id": row[0],
            "test_id": row[1],
            "test_name": row[2],
            "medium": row[3],
            "category": row[4],
            "status": row[5],
        }
        for row in test_types
    ]

    return render(request, "test_type.html", {
        "categories": data,
        "category_list": category_list,
        "superuser_level": superuser_level
    })


@permission_required("Standard")
def standard_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ID, STANDARD_ID, STANDARD_NAME, STANDARD_DESC, CREATED_DATE, UPDATED_DATE
            FROM standard
            ORDER BY ID
        """)
        standards = cursor.fetchall()

    # Extract only names for frontend duplicate check
    existing_names = [row[2] for row in standards]  # STANDARD_NAME

    return render(request, 'standard_list.html', {
        'standards': standards,
        'existing_names': existing_names,
    })


@permission_required("Standard")
def add_standard(request):
    if request.method == 'POST':
        STANDARD_NAME = request.POST.get("name")
        STANDARD_DESC = request.POST.get("description")

        if STANDARD_NAME:
            with connection.cursor() as cursor:
                # calculate next STANDARD_ID
                cursor.execute("SELECT COALESCE(MAX(STANDARD_ID),0)+1 FROM standard")
                next_standard_id = cursor.fetchone()[0]

                cursor.execute(
                    "INSERT INTO standard (STANDARD_ID, STANDARD_NAME, STANDARD_DESC) VALUES (%s, %s, %s)",
                    [next_standard_id, STANDARD_NAME, STANDARD_DESC]
                )

            messages.success(request, 'Standard added successfully!')
        else:
            messages.error(request, 'Standard name is required.')

    return redirect('standard_list')


@permission_required("Standard")
def edit_standard(request, pk):
    if request.method == 'POST':
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()

        if not name:
            messages.error(request, 'Standard name cannot be empty.')
            return redirect('standard_list')

        with connection.cursor() as cursor:
            # Check for duplicates excluding current ID
            cursor.execute("SELECT 1 FROM standard WHERE STANDARD_NAME=%s AND ID != %s", [name, pk])
            if cursor.fetchone():
                messages.error(request, 'Another standard with this name already exists.')
                return redirect('standard_list')

            # Update record using ID
            cursor.execute("""
                UPDATE standard
                SET STANDARD_NAME=%s, STANDARD_DESC=%s
                WHERE ID=%s
            """, [name, description, pk])

        messages.success(request, 'Standard updated successfully!')

    return redirect('standard_list')

@permission_required("Standard")
def delete_standard(request, pk):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM standard WHERE ID=%s", [pk])
        messages.success(request, 'Standard deleted successfully!')

    return redirect('standard_list')



from django.shortcuts import render, redirect
from django.db import connection, transaction, IntegrityError
from django.contrib import messages

def to_int_or_none(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

@permission_required("Valve Size")
def valve_size_list(request):
    # --- Fetch valves ---
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ID, SIZE_ID, SIZE_NAME, SIZE_DESC
            FROM valvesize
            ORDER BY SIZE_ID
        """)
        valves = cursor.fetchall()

    # --- Fetch standards ---
    with connection.cursor() as cursor:
        cursor.execute("SELECT STANDARD_ID, STANDARD_NAME FROM standard ORDER BY STANDARD_ID")
        standards = cursor.fetchall()

    # --- Fetch enabled categories only ---
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT CATEGORY_NAME, DURATION_COLUMN_NAME
            FROM category
            WHERE STATUS = 'ENABLE'
            ORDER BY CATEGORY_ID
        """)
        categories = cursor.fetchall()

    edit_valve = None
    degree_data = []

    # --- POST (Save) ---
    if request.method == "POST":
        valve_id = request.POST.get("valve_id")
        name = request.POST.get("name", "").strip()
        desc = request.POST.get("description", "").strip()
        standards_selected = request.POST.getlist("standard[]")

        # --- Determine SIZE_ID ---
        with connection.cursor() as cursor:
            if valve_id and valve_id.isdigit():
                # Existing record → fetch its current SIZE_ID
                cursor.execute("SELECT SIZE_ID FROM valvesize WHERE ID=%s", [valve_id])
                result = cursor.fetchone()
                code = str(result[0]) if result else None
            else:
                # New record → auto-generate next SIZE_ID
                cursor.execute("SELECT COALESCE(MAX(SIZE_ID), 0) + 1 FROM valvesize")
                next_size_id = cursor.fetchone()[0]
                code = str(next_size_id)

        if not code:
            messages.error(request, "Unable to determine Valve Code.")
            return redirect("valve_size_list")

        # --- Duplicate code validation ---
        with connection.cursor() as cursor:
            if valve_id and valve_id.isdigit():
                cursor.execute("SELECT COUNT(*) FROM valvesize WHERE SIZE_ID=%s AND ID<>%s", [code, valve_id])
            else:
                cursor.execute("SELECT COUNT(*) FROM valvesize WHERE SIZE_ID=%s", [code])
            if cursor.fetchone()[0] > 0:
                messages.error(request, f"Valve Code '{code}' already exists.")
                return redirect("valve_size_list")

        # --- Collect category values ---
        category_values = {col_name: request.POST.getlist(col_name + "[]") for _, col_name in categories}

        # --- Build rows data ---
        rows_data = []
        for i, std_id in enumerate(standards_selected):
            if not std_id:
                continue
            row = {'standard_id': std_id}
            for _, col_name in categories:
                vals = category_values.get(col_name, [])
                row[col_name] = to_int_or_none(vals[i]) if i < len(vals) else None
            rows_data.append(row)

        # --- Insert / Update logic ---
        with transaction.atomic():
            with connection.cursor() as cursor:
                try:
                    if valve_id and valve_id.isdigit():
                        # --- Update existing valve ---
                        cursor.execute("""
                            UPDATE valvesize
                            SET SIZE_NAME=%s, SIZE_DESC=%s
                            WHERE ID=%s
                        """, [name, desc, valve_id])
                        new_valve_id = valve_id
                    else:
                        # --- Insert new valve ---
                        cursor.execute("""
                            INSERT INTO valvesize (SIZE_ID, SIZE_NAME, SIZE_DESC)
                            VALUES (%s, %s, %s)
                        """, [int(code), name, desc])
                        new_valve_id = cursor.lastrowid

                    # --- Manage master_duration_data ---
                    cursor.execute("SELECT STANDARD_ID FROM master_duration_data WHERE SIZE_ID=%s", [code])
                    existing_std_ids = [str(r[0]) for r in cursor.fetchall()]
                    new_std_ids = [str(r['standard_id']) for r in rows_data]

                    deleted_std_ids = list(set(existing_std_ids) - set(new_std_ids))
                    if deleted_std_ids:
                        cursor.execute(
                            f"DELETE FROM master_duration_data WHERE SIZE_ID=%s AND STANDARD_ID IN ({','.join(['%s']*len(deleted_std_ids))})",
                            [code, *deleted_std_ids]
                        )

                    # --- Insert or Update duration data ---
                    for row in rows_data:
                        col_names = ", ".join(col_name for _, col_name in categories)
                        placeholders = ", ".join(["%s"] * len(categories))
                        update_clause = ", ".join([f"{col}=VALUES({col})" for _, col in categories])

                        cursor.execute(f"""
                            INSERT INTO master_duration_data (SIZE_ID, STANDARD_ID, {col_names})
                            VALUES (%s, %s, {placeholders})
                            ON DUPLICATE KEY UPDATE {update_clause}
                        """, [int(code), row['standard_id'], *[row[col] for _, col in categories]])

                except IntegrityError as e:
                    messages.error(request, f"Database error: {str(e)}")
                    return redirect("valve_size_list")

        messages.success(request, f"Valve Size {code} saved successfully!")
        return redirect("valve_size_list")

    # --- GET Edit ---
    if request.method == "GET" and "edit" in request.GET:
        valve_id = request.GET.get("edit")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT ID, SIZE_ID, SIZE_NAME, SIZE_DESC
                FROM valvesize
                WHERE ID=%s
            """, [valve_id])
            row = cursor.fetchone()
            if row:
                edit_valve = dict(zip(["id", "code", "name", "description"], row))

        # --- Fetch master_duration_data ---
        with connection.cursor() as cursor:
            col_names = ", ".join(col_name for _, col_name in categories)
            cursor.execute(f"""
                SELECT ID, STANDARD_ID, {col_names}
                FROM master_duration_data
                WHERE SIZE_ID=%s
                ORDER BY ID
            """, [edit_valve['code']])
            degree_data = []
            for d in cursor.fetchall():
                entry = {"id": d[0], "standard_id": d[1]}
                for i, (_, col_name) in enumerate(categories):
                    entry[col_name] = d[i + 2]
                degree_data.append(entry)

    # --- Fetch existing codes/names ---
    with connection.cursor() as cursor:
        cursor.execute("SELECT SIZE_ID, SIZE_NAME FROM valvesize")
        existing_rows = cursor.fetchall()
        existing_codes = [str(r[0]) for r in existing_rows]
        existing_names = [r[1] for r in existing_rows if r[1]]

    all_categories_disabled = len(categories) == 0

    return render(request, 'valve_size.html', {
        'valves': valves,
        'edit_valve': edit_valve,
        'degree_data': degree_data,
        'standards': standards,
        'categories': categories,
        'existing_codes': existing_codes,
        'existing_names': existing_names,
        'all_categories_disabled': all_categories_disabled,
    })

from django.db import connection, transaction
from django.db.utils import OperationalError
from django.contrib import messages

@permission_required("Valve Size")
def valve_size_delete(request, pk):
    if request.method == 'POST':
        with transaction.atomic():
            with connection.cursor() as cursor:
                # Look up SIZE_ID (code) for this valve primary key
                cursor.execute("SELECT SIZE_ID FROM valvesize WHERE ID=%s", [pk])
                row = cursor.fetchone()
                size_code = row[0] if row else None
                # Delete related rows by SIZE_ID (code)
                if size_code is not None:
                    cursor.execute("DELETE FROM master_duration_data WHERE SIZE_ID=%s", [size_code])
                # Delete valve_size row by ID
                cursor.execute("DELETE FROM valvesize WHERE ID=%s", [pk])
        messages.success(request, 'Valve Size deleted successfully!')
    return redirect('valve_size_list')


@permission_required("Valve Class")
def valve_class_list(request):
    # --- Fetch all valve classes ---
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID, CLASS_ID, CLASS_NAME, CLASS_DESC FROM valveclass ORDER BY ID")
        rows = cursor.fetchall()
        valves = [{'id': r[0], 'code': r[1], 'name': r[2], 'description': r[3]} for r in rows]

        # Existing codes and names for validation
        cursor.execute("SELECT CLASS_ID FROM valveclass")
        existing_codes_raw = [str(r[0]) for r in cursor.fetchall()]
        cursor.execute("SELECT CLASS_NAME FROM valveclass")
        existing_names_raw = [r[0] for r in cursor.fetchall()]

    existing_codes = mark_safe(json.dumps(existing_codes_raw))
    existing_names = mark_safe(json.dumps(existing_names_raw))

   
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        valve_id = request.POST.get('valve_id')
        name = request.POST.get('name', '').strip()
        code = request.POST.get('code', '').strip()
        description = request.POST.get('description', '').strip()

    
        if not name:
            messages.error(request, "Valve Class Name is required.")
            return redirect('valve_class')

    
        if form_type == 'add' or not code.isdigit():
            with connection.cursor() as cursor:
                cursor.execute("SELECT COALESCE(MAX(CLASS_ID), 0) + 1 FROM valveclass")
                next_id = cursor.fetchone()[0]
            code = str(next_id)

    
        if form_type == 'add':
            with connection.cursor() as cursor:
                # Duplicate check
                cursor.execute(
                    "SELECT COUNT(*) FROM valveclass WHERE CLASS_ID=%s OR LOWER(CLASS_NAME)=LOWER(%s)",
                    [code, name]
                )
                if cursor.fetchone()[0] > 0:
                    messages.error(request, f"Valve Class with ID '{code}' or Name '{name}' already exists.")
                    return redirect('valve_class')

                # Insert new record
                cursor.execute(
                    "INSERT INTO valveclass (CLASS_ID, CLASS_NAME, CLASS_DESC) VALUES (%s, %s, %s)",
                    [int(code), name, description]
                )

            messages.success(request, "Valve Class added successfully!")
            return redirect('valve_class')

 
        elif form_type == 'edit' and valve_id:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    # Duplicate name check excluding current record
                    cursor.execute(
                        "SELECT COUNT(*) FROM valveclass WHERE LOWER(CLASS_NAME)=LOWER(%s) AND ID<>%s",
                        [name, valve_id]
                    )
                    if cursor.fetchone()[0] > 0:
                        messages.error(request, "Valve Class name already exists.")
                        return redirect('valve_class')

                    # Optional: prevent changing CLASS_ID on edit to avoid inserting new ID
                    cursor.execute(
                        "UPDATE valveclass SET CLASS_NAME=%s, CLASS_DESC=%s WHERE ID=%s",
                        [name, description, valve_id]
                    )

            messages.success(request, "Valve Class updated successfully!")
            return redirect('valve_class')

 
    return render(request, 'valve_class.html', {
        'valves': valves,
        'existing_codes': existing_codes,
        'existing_names': existing_names,
    })

@permission_required("Valve Class")
def valve_class_delete(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM valveclass WHERE ID=%s", [pk])
    messages.success(request, 'Valve Class deleted successfully!')
    return redirect('valve_class')





from django.shortcuts import render, redirect
from django.db import connection, transaction, IntegrityError
from django.contrib import messages

def to_float_or_none(value):
    try:
        return float(value) if value not in ("", None) else None
    except ValueError:
        return None

@permission_required("Shell Material")

def shell_material(request):
    # --- Fetch all shell materials ---
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ID, SHELL_MATERIAL_ID, SHELL_MATERIAL_NAME, SHELL_MATERIAL_DESC
            FROM shell_material
            ORDER BY SHELL_MATERIAL_ID
        """)
        materials = cursor.fetchall()

    # --- Fetch valve classes ---
    with connection.cursor() as cursor:
        cursor.execute("SELECT CLASS_ID, CLASS_NAME FROM valveclass ORDER BY CLASS_ID")
        classes = cursor.fetchall()

    # --- Fetch enabled pressure categories ---
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT CATEGORY_NAME, PRESSURE_COLUMN_NAME
            FROM category
            WHERE STATUS='ENABLE'
            ORDER BY ID
        """)
        categories = cursor.fetchall()

    edit_material = None
    pressure_data = []

    # ============================================================
    # --- POST (Save) ---
    # ============================================================
    if request.method == "POST":
        material_id = request.POST.get("material_id")
        name = request.POST.get("name", "").strip()
        desc = request.POST.get("description", "").strip()
        classes_selected = request.POST.getlist("Class[]")

        if not name:
            messages.error(request, "Shell Material Name is required.")
            return redirect("shell_material")

        # --- Determine SHELL_MATERIAL_ID ---
        with connection.cursor() as cursor:
            if material_id and material_id.isdigit():
                # Editing → keep existing ID
                cursor.execute("SELECT SHELL_MATERIAL_ID FROM shell_material WHERE ID=%s", [material_id])
                result = cursor.fetchone()
                code = str(result[0]) if result else None
            else:
                # New record → generate next ID
                cursor.execute("SELECT COALESCE(MAX(SHELL_MATERIAL_ID), 0) + 1 FROM shell_material")
                next_id = cursor.fetchone()[0]
                code = str(next_id)

        if not code:
            messages.error(request, "Unable to determine Shell Material ID.")
            return redirect("shell_material")

        # --- Duplicate ID validation ---
        with connection.cursor() as cursor:
            if material_id and material_id.isdigit():
                cursor.execute("""
                    SELECT COUNT(*) FROM shell_material
                    WHERE SHELL_MATERIAL_ID=%s AND ID<>%s
                """, [code, material_id])
            else:
                cursor.execute("SELECT COUNT(*) FROM shell_material WHERE SHELL_MATERIAL_ID=%s", [code])
            if cursor.fetchone()[0] > 0:
                messages.error(request, f"Shell Material ID '{code}' already exists.")
                return redirect("shell_material")

        # --- Collect category values ---
        category_values = {col: request.POST.getlist(col + "[]") for _, col in categories}

        rows_data = []
        for i, cls_id in enumerate(classes_selected):
            if not cls_id:
                continue
            row = {"class_id": cls_id}
            for _, col in categories:
                vals = category_values.get(col, [])
                row[col] = to_float_or_none(vals[i]) if i < len(vals) else None
            rows_data.append(row)

        # ============================================================
        # --- Insert / Update Logic ---
        # ============================================================
        with transaction.atomic():
            with connection.cursor() as cursor:
                try:
                    # --- Update or Insert shell_material ---
                    if material_id and material_id.isdigit():
                        # ✅ Update existing record
                        cursor.execute("""
                            UPDATE shell_material
                            SET SHELL_MATERIAL_NAME=%s, SHELL_MATERIAL_DESC=%s
                            WHERE ID=%s
                        """, [name, desc, material_id])
                    else:
                        # 🆕 Insert new record
                        cursor.execute("""
                            INSERT INTO shell_material (SHELL_MATERIAL_ID, SHELL_MATERIAL_NAME, SHELL_MATERIAL_DESC)
                            VALUES (%s, %s, %s)
                        """, [int(code), name, desc])

                    # ======================================================
                    # --- Manage master_pressure_data (Update only) ---
                    # ======================================================
                    cursor.execute("SELECT VALVECLASS_ID FROM master_pressure_data WHERE SHELLMATERIAL_ID=%s", [code])
                    existing_class_ids = [str(r[0]) for r in cursor.fetchall()]
                    new_class_ids = [str(r["class_id"]) for r in rows_data]

                    # Delete removed rows
                    deleted_class_ids = list(set(existing_class_ids) - set(new_class_ids))
                    if deleted_class_ids:
                        cursor.execute(
                            f"DELETE FROM master_pressure_data WHERE SHELLMATERIAL_ID=%s AND VALVECLASS_ID IN ({','.join(['%s']*len(deleted_class_ids))})",
                            [code, *deleted_class_ids]
                        )

                    # Insert or update each class row
                    for row in rows_data:
                        class_id = row["class_id"]

                        cursor.execute("""
                            SELECT COUNT(*) FROM master_pressure_data
                            WHERE SHELLMATERIAL_ID=%s AND VALVECLASS_ID=%s
                        """, [code, class_id])
                        exists = cursor.fetchone()[0]

                        if exists:
                            # ✅ Update existing pressure data
                            set_clause = ", ".join([f"{col}=%s" for _, col in categories])
                            cursor.execute(f"""
                                UPDATE master_pressure_data
                                SET {set_clause}
                                WHERE SHELLMATERIAL_ID=%s AND VALVECLASS_ID=%s
                            """, [*[row[col] for _, col in categories], code, class_id])
                        else:
                            # 🆕 Insert new one if not present
                            col_names = ", ".join(col for _, col in categories)
                            placeholders = ", ".join(["%s"] * len(categories))
                            cursor.execute(f"""
                                INSERT INTO master_pressure_data (SHELLMATERIAL_ID, VALVECLASS_ID, {col_names})
                                VALUES (%s, %s, {placeholders})
                            """, [code, class_id, *[row[col] for _, col in categories]])

                except IntegrityError as e:
                    messages.error(request, f"Database error: {str(e)}")
                    return redirect("shell_material")

        messages.success(request, f"Shell Material {code} saved successfully!")
        return redirect("shell_material")

    # ============================================================
    # --- GET (Edit) ---
    # ============================================================
    if request.method == "GET" and "edit" in request.GET:
        material_id = request.GET.get("edit")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT ID, SHELL_MATERIAL_ID, SHELL_MATERIAL_NAME, SHELL_MATERIAL_DESC
                FROM shell_material
                WHERE ID=%s
            """, [material_id])
            row = cursor.fetchone()
            if row:
                edit_material = dict(zip(["id", "code", "name", "description"], row))

        # --- Fetch pressure data ---
        if edit_material:
            with connection.cursor() as cursor:
                col_names = ", ".join(col for _, col in categories)
                cursor.execute(f"""
                    SELECT ID, VALVECLASS_ID, {col_names}
                    FROM master_pressure_data
                    WHERE SHELLMATERIAL_ID=%s
                    ORDER BY ID
                """, [edit_material["code"]])
                pressure_data = []
                for d in cursor.fetchall():
                    entry = {"id": d[0], "class_id": d[1]}
                    for i, (_, col) in enumerate(categories):
                        entry[col] = d[i + 2]
                    pressure_data.append(entry)

    # ============================================================
    # --- Common Data for Template ---
    # ============================================================
    with connection.cursor() as cursor:
        cursor.execute("SELECT SHELL_MATERIAL_ID, SHELL_MATERIAL_NAME FROM shell_material")
        existing_rows = cursor.fetchall()
        existing_codes = [str(r[0]) for r in existing_rows]
        existing_names = [r[1] for r in existing_rows if r[1]]

    all_categories_disabled = len(categories) == 0

    return render(request, "shell_material.html", {
        "materials": materials,
        "edit_material": edit_material,
        "pressure_data": pressure_data,
        "classes": classes,
        "categories": categories,
        "existing_codes": existing_codes,
        "existing_names": existing_names,
        "all_categories_disabled": all_categories_disabled,
    })

@permission_required("Shell Material")
def shell_material_delete(request, pk):
    if request.method == "POST":
        with transaction.atomic():
            with connection.cursor() as cursor:
                # Check if record exists
                cursor.execute("SELECT id FROM shell_material WHERE SHELL_MATERIAL_ID=%s", [pk])
                if not cursor.fetchone():
                    messages.error(request, "Shell Material not found.")
                    return redirect("shell_material")
                
                # Delete record
                cursor.execute("DELETE FROM shell_material WHERE SHELL_MATERIAL_ID=%s", [pk])

                cursor.execute("DELETE FROM master_pressure_data WHERE SHELLMATERIAL_ID=%s", [pk])

        messages.success(request, "Shell Material deleted successfully!")
    else:
        messages.error(request, "Invalid request method.")

    return redirect("shell_material")





@permission_required("Valve Type")
def valve_type_list(request):
    with connection.cursor() as cursor:
        # Fetch all valve types
        cursor.execute("SELECT ID, TYPE_ID, TYPE_NAME, TYPE_DESC FROM valve_type ORDER BY ID")
        rows = cursor.fetchall()
        valve_types = [
            {'id': r[0], 'code': r[1], 'name': r[2], 'description': r[3]} for r in rows
        ]

        # Fetch enabled test types
        cursor.execute("""
            SELECT TEST_ID, TEST_NAME
            FROM test_type
            WHERE STATUS = 'ENABLE'
            ORDER BY TEST_ID
        """)
        test_types = [{'id': r[0], 'name': r[1]} for r in cursor.fetchall()]

        # Existing codes & names
        cursor.execute("SELECT TYPE_ID FROM valve_type")
        existing_codes_raw = [str(r[0]) for r in cursor.fetchall()]
        cursor.execute("SELECT TYPE_NAME FROM valve_type")
        existing_names_raw = [r[0] for r in cursor.fetchall()]

    existing_codes = mark_safe(json.dumps(existing_codes_raw))
    existing_names = mark_safe(json.dumps(existing_names_raw))

    # ---------------- POST ----------------
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        selected_test_types = request.POST.getlist('test_types')

        # --- Common validation ---
        if not name:
            messages.error(request, "Valve Type Name cannot be empty.")
            return redirect('valve_type')

        if not selected_test_types:
            messages.error(request, "Please select at least one Test Type before saving.")
            return redirect('valve_type')

        # ---------- ADD OPERATION ----------
        if form_type == 'add':
            with connection.cursor() as cursor:
                # ✅ Generate the next numeric TYPE_ID safely
                cursor.execute("SELECT COALESCE(MAX(TYPE_ID), 0) + 1 FROM valve_type")
                result = cursor.fetchone()
                next_code = int(result[0]) if result and result[0] is not None else 1

                # ✅ Prevent duplicates
                cursor.execute("SELECT COUNT(*) FROM valve_type WHERE TYPE_NAME=%s", [name])
                if cursor.fetchone()[0] > 0:
                    messages.error(request, f"Valve Type '{name}' already exists.")
                    return redirect('valve_type')

                # ✅ Insert valve type
                cursor.execute("""
                    INSERT INTO valve_type (TYPE_ID, TYPE_NAME, TYPE_DESC)
                    VALUES (%s, %s, %s)
                """, [next_code, name, description])

                # ✅ Insert associated test types
                for test_type_id in selected_test_types:
                    cursor.execute("""
                        INSERT INTO valvetype_testtype (TYPE_ID, TEST_ID)
                        VALUES (%s, %s)
                    """, [next_code, test_type_id])

            messages.success(request, f"Valve Type '{name}' added successfully with Code {next_code}!")
            return redirect('valve_type')

        # ---------- EDIT OPERATION ----------
        elif form_type == 'edit':
            valve_id = request.POST.get('valve_id')
            code = request.POST.get('code', '').strip()

            with connection.cursor() as cursor:
                # Fetch TYPE_ID from ID (to avoid empty code)
                if not code:
                    cursor.execute("SELECT TYPE_ID FROM valve_type WHERE ID=%s", [valve_id])
                    fetched = cursor.fetchone()
                    if fetched and fetched[0]:
                        code = int(fetched[0])
                    else:
                        messages.error(request, "Invalid Valve Type code.")
                        return redirect('valve_type')

                # Check for duplicate name
                cursor.execute("SELECT COUNT(*) FROM valve_type WHERE TYPE_NAME=%s AND ID!=%s", [name, valve_id])
                if cursor.fetchone()[0] > 0:
                    messages.error(request, f"Valve Type '{name}' already exists.")
                    return redirect('valve_type')

                # Update valve_type table
                cursor.execute("""
                    UPDATE valve_type
                    SET TYPE_NAME=%s, TYPE_DESC=%s
                    WHERE ID=%s
                """, [name, description, valve_id])

                # Refresh test type links
                cursor.execute("DELETE FROM valvetype_testtype WHERE TYPE_ID=%s", [code])
                for test_type_id in selected_test_types:
                    cursor.execute("""
                        INSERT INTO valvetype_testtype (TYPE_ID, TEST_ID)
                        VALUES (%s, %s)
                    """, [code, test_type_id])

            messages.success(request, f"Valve Type '{name}' updated successfully!")
            return redirect('valve_type')

    # ---------------- DISPLAY ----------------
    valve_test_types = {}
    with connection.cursor() as cursor:
        for vt in valve_types:
            cursor.execute("SELECT TEST_ID FROM valvetype_testtype WHERE TYPE_ID=%s", [vt['code']])
            selected_tests = [r[0] for r in cursor.fetchall()]
            valve_test_types[vt['code']] = selected_tests

            cursor.execute("""
                SELECT t.TEST_NAME
                FROM test_type t
                INNER JOIN valvetype_testtype vt ON t.TEST_ID = vt.TEST_ID
                WHERE vt.TYPE_ID=%s AND t.STATUS='ENABLE'
            """, [vt['code']])
            vt['associated_test_types'] = [r[0] for r in cursor.fetchall()]
            vt['selected_test_type_ids'] = selected_tests

    return render(request, 'valve_type.html', {
        'valve_types': valve_types,
        'test_types': test_types,
        'valve_test_types': valve_test_types,
        'existing_codes': existing_codes,
        'existing_names': existing_names,
    })

from django.db import transaction

@permission_required("Valve Type")
def valve_type_delete(request, valve_type_id):
    """Delete a valve type and its associated test type links."""
    try:
        with transaction.atomic(), connection.cursor() as cursor:
            cursor.execute("SELECT TYPE_NAME, TYPE_ID FROM valve_type WHERE ID=%s", [valve_type_id])
            result = cursor.fetchone()
            if not result:
                messages.error(request, "Valve Type not found.")
                return redirect('valve_type')

            valve_type_name, type_code = result

            cursor.execute("DELETE FROM valvetype_testtype WHERE TYPE_ID=%s", [type_code])
            cursor.execute("DELETE FROM valve_type WHERE ID=%s", [valve_type_id])

            messages.success(request, f'Valve Type "{valve_type_name}" and its associations deleted successfully!')

    except Exception as e:
        messages.error(request, f'Error deleting valve type: {str(e)}')

    return redirect('valve_type')

@permission_required("Alarm")
def alarm(request):
    with connection.cursor() as cursor:
        # Fetch all alarms
        cursor.execute("SELECT ID, ALARM_ID, ALARM_NAME FROM alarm ORDER BY id")
        rows = cursor.fetchall()
        alarms = [{'id': r[0], 'code': r[1], 'name': r[2]} for r in rows]

        # Existing codes
        cursor.execute("SELECT ALARM_ID FROM alarm")
        existing_codes_raw = [r[0] for r in cursor.fetchall()]

    existing_codes = json.dumps(existing_codes_raw, cls=DjangoJSONEncoder)

    return render(request, 'alaram.html', {
        'alarms': alarms,
        'existing_codes': existing_codes,
    })


@csrf_exempt
@permission_required("Alarm")
def alarm_add_or_edit(request):
    if request.method == 'POST':
        alarm_id = request.POST.get('alarm_id')
        code = request.POST.get('code', '').strip()
        name = request.POST.get('name', '').strip()

        with connection.cursor() as cursor:
            if alarm_id:  # Edit
                cursor.execute(
                    "UPDATE alarm SET ALARM_NAME=%s WHERE ID=%s",
                    [name, alarm_id]
                )
                messages.success(request, 'Alarm updated successfully!')
            else:  # Add new
                # Get next auto ID manually
                cursor.execute("SELECT COALESCE(MAX(ALARM_ID), 0) + 1 FROM alarm")
                next_alarm_id = cursor.fetchone()[0]

                cursor.execute(
                    "INSERT INTO alarm (ALARM_ID, ALARM_NAME) VALUES (%s, %s)",
                    [next_alarm_id, name]
                )
                messages.success(request, 'Alarm added successfully!')

    return redirect('alarm')


@csrf_exempt
@permission_required("Alarm")
def alarm_delete(request, alarm_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM alarm WHERE ID=%s", [alarm_id])
    messages.success(request, 'Alarm deleted successfully!')
    return redirect('alarm')

@csrf_exempt
@login_required
def save_shift_selection(request):
    """Insert a new shift only if none exists for a valve type, else update existing one."""
    
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

    shift_input = request.POST.get('shift_id')  # user-provided shift number or name
    valve_type_id = request.POST.get('valve_type_id')

    if not shift_input or not valve_type_id:
        return JsonResponse({'status': 'error', 'message': 'Both shift and valve type are required'}, status=400)

    with connection.cursor() as cursor:
        # Get TYPE_ID for valve_type
        cursor.execute("SELECT TYPE_ID FROM valve_type WHERE ID = %s", [valve_type_id])
        row = cursor.fetchone()
        type_id = row[0] if row else None

        # Build normalized shift name
        shift_name = f"Shift {shift_input}".strip()

        # Check if a shift exists for this valve type
        cursor.execute("""
            SELECT ID FROM shift WHERE TYPE_ID = %s LIMIT 1
        """, [type_id])
        row = cursor.fetchone()

        if row:
            # ✅ Shift exists → UPDATE existing record
            existing_shift_id = row[0]
            cursor.execute("""
                UPDATE shift
                SET SHIFT_NAME = %s, UPDATED_AT = NOW()
                WHERE ID = %s
            """, [shift_name, existing_shift_id])
            shift_id_to_use = existing_shift_id
        else:
            # ✅ No shift exists → INSERT a new row
            cursor.execute("""
                INSERT INTO shift (SHIFT_NAME, TYPE_ID, IS_ACTIVE, CREATED_AT, UPDATED_AT)
                VALUES (%s, %s, 1, NOW(), NOW())
            """, [shift_name, type_id])
            shift_id_to_use = cursor.lastrowid

        # Fetch valve type name for the response
        cursor.execute("SELECT TYPE_NAME FROM valve_type WHERE ID = %s", [valve_type_id])
        vt_row = cursor.fetchone()
        valve_type_name = vt_row[0] if vt_row else f"ID {valve_type_id}"

    # Save in session
    request.session['selected_shift_id'] = shift_id_to_use
    request.session['selected_valve_type_id'] = valve_type_id

    return JsonResponse({
        'status': 'success',
        'message': f'Shift "{shift_name}" selected for valve type "{valve_type_name}"',
        'shift_id': shift_id_to_use,
        'valve_type_id': valve_type_id
    })


@login_required

def new_test(request):
    current_user = request.session.get('username')   # currently logged-in user
    superuser_flag = request.session.get('superuser')  # 0=normal/tester, 1=admin, 2=superadmin

    # ✅ Initialize all lists to avoid UnboundLocalError
    employees_tester = []
    employees_tester_user = []
    employees_tester_user1 = []
    employees_approver = []
    standards = []
    shell_materials = []
    valve_sizes = []
    valve_classes = []
    valve_types = []

    with connection.cursor() as cursor:
        # Standards
        cursor.execute("SELECT STANDARD_NAME FROM standard ORDER BY STANDARD_NAME")
        standards = [row[0] for row in cursor.fetchall()]

        # Shell materials
        cursor.execute("SELECT SHELL_MATERIAL_NAME FROM shell_material ORDER BY SHELL_MATERIAL_NAME")
        shell_materials = [row[0] for row in cursor.fetchall()]

        # Valve sizes
        cursor.execute("SELECT SIZE_NAME FROM valvesize ORDER BY SIZE_NAME")
        valve_sizes = [row[0] for row in cursor.fetchall()]

        # Valve classes
        cursor.execute("SELECT CLASS_NAME FROM valveclass ORDER BY CLASS_NAME")
        valve_classes = [row[0] for row in cursor.fetchall()]

        # Valve types
        cursor.execute("SELECT TYPE_NAME FROM valve_type ORDER BY TYPE_NAME")
        valve_types = [row[0] for row in cursor.fetchall()]

        # Approvers
        cursor.execute("SELECT name FROM newapp_employee WHERE employee_type='Approver' ORDER BY name")
        employees_approver = [row[0] for row in cursor.fetchall()]

        # Testers
        if superuser_flag in [1, 2]:  # Admin or Superadmin
            cursor.execute("SELECT name FROM newapp_employee WHERE employee_type='Tester' ORDER BY name")
            employees_tester = [row[0] for row in cursor.fetchall()]

        else:  # Tester login → only their own name
            cursor.execute("""
                SELECT employee_type 
                FROM newapp_employee 
                WHERE name = %s
            """, [current_user])
            result = cursor.fetchone()

            if result and result[0] == 'Tester':
                # Current user is a Tester → show only their name
                cursor.execute("""
                    SELECT name 
                    FROM newapp_employee 
                    WHERE name = %s
                """, [current_user])
                employees_tester_user = [row[0] for row in cursor.fetchall()]
            else:
                # Current user not a Tester → show all testers
                cursor.execute("""
                    SELECT name 
                    FROM newapp_employee 
                    WHERE employee_type = 'Tester' 
                    ORDER BY name
                """)
                employees_tester_user1 = [row[0] for row in cursor.fetchall()]

        # Reset master_temp_data
        cursor.execute("""
            UPDATE master_temp_data
            SET STATION_STATUS = %s,
                CYCLE_COMPLETE = %s
            WHERE STATION_STATUS = %s
        """, [1, 0, 1])

    context = {
        "newapp_standard": standards,
        "newapp_shellmaterial": shell_materials,
        "newapp_valvesize": valve_sizes,
        "newapp_valveclass": valve_classes,
        "newapp_valvetype": valve_types,
        "employees_approver": employees_approver,
        "employees_tester": employees_tester,           # For Admin / Superadmin
        "employees_tester_user": employees_tester_user, # For Tester
        "employees_tester_user1": employees_tester_user1 # For non-tester users
    }


    return render(request, "sap_form.html", context)



@csrf_exempt
@login_required
def get_sap_data(request):
    """
    Fetch valve and test data from SAP using the provided serial number.
    Returns JSON response for AJAX integration in valves.html.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

    serial_no = request.POST.get('valveserialno', '').strip()
    if not serial_no:
        return JsonResponse({'status': 'error', 'message': 'Serial number is required.'})

    # Construct WSDL path - located in landtapp/wdsl folder
    wsdl_path = os.path.join(settings.BASE_DIR, 'landtapp', 'wdsl', 'z_qm_get_pres_test_masterbinding.wsdl')
    
    if not os.path.exists(wsdl_path):
        return JsonResponse({'status': 'error', 'message': f'SAP configuration error: WSDL file not found.'})

    is_sap = False

    try:
        # if is_sap is not True:
        #     valve_data = {
        #     "serial_no": "26C105982",
        #     "material": "GA14101GM08ASS_004",
        #     "description": "Gate",
        #     "size": "14\"",
        #     "class": "150",
        #     "sales_order": "0110035345",
        #     "sales_item": "000120",
        #     "tag_no": "2002235237; VGGJ10XB 14.000",
        #     "body_material": "ASTM A216 Gr.WCB",
        #     "cat_no": "117"
        #             }

        # trace_details = {
        #     "BODY": {
        #         "heat_no": "AC1002",
        #         "mpi_no": "MTA26640",
        #         "xray_no": None,
        #         "dpi_no": None
        #     },
        #     "BONNET": {
        #         "heat_no": "AC1002",
        #         "mpi_no": "MTA26642",
        #         "xray_no": None,
        #         "dpi_no": None
        #     }
        # }

        # tests = [
        #     {
        #         "testId" : 1,
        #         "name": "Seat ( Hydro )",
        #         "duration": "120",
        #         "pressure_bar": "22.0",
        #         "pressure_psi": "315.0",
        #         "unit": "SEC"
        #     },
        #     {
        #         "testId" : 2,
        #         "name": "Backseat ( Hydro )",
        #         "duration": "120",
        #         "pressure_bar": "22.0",
        #         "pressure_psi": "315.0",
        #         "unit": "SEC"
        #     },
        #     {   
        #         "testId" : 3,
        #         "name": "Seat ( Air )",
        #         "duration": "120",
        #         "pressure_bar": "7.0",
        #         "pressure_psi": "100.0",
        #         "unit": "SEC"
        #     },
        #     {
        #         "testId" : 4,
        #         "name": "Shell ( Hydro )",
        #         "duration": "300",
        #         "pressure_bar": "30.0",
        #         "pressure_psi": "450.0",
        #         "unit": "SEC"
        #     }
        # ]

        # return JsonResponse({
        #     'status': 'success',
        #     'valve_details': valve_data,
        #     'trace_details': trace_details,
        #     'tests': tests
        # })

        # Initialize Zeep Client
        zeep_settings = Settings(strict=False, xml_huge_tree=True)
        client = Client(wsdl=wsdl_path, settings=zeep_settings)

        # Prepare SAP request data
        search_data = {
            'IpMasterDataAll': 'X',
            'IpMbarcodeNum': serial_no,
            'IpProductCode': '1',
            'IpUsn': '',
            'EtPreTestDurVal': {},
            'EtPreTestDuratM': {},
            'EtPreTestValueM': {},
            'EtScndet': {},
            'EtValveAttrMast': {},
        }

        # Call SAP service
        response = client.service.ZQmGetPresTestMaster(**search_data)

        print("responce >>>",response)
        
        # Validation logic from sap_get_demo.py
        is_success = (response.EpSuccess != '1')

        if is_success:
            # Extract basic details
            details = response.EsValveDetail
            valve_data = {
                'serial_no': details.ZfgSlno,
                'material': details.Matnr,
                'description': details.ZprodDesc,
                'size': details.ZprodSize,
                'size_name': details.ZprodSizeDesc,
                'class': details.ZprodClasRatDesc,
                'sales_order': details.Kdauf,
                'sales_item': details.Kdpos,
                'tag_no': details.Tagnum,
                'body_material': details.ZprodMaterialDesc,
                'cat_no': details.ZprodCatgDesc,
            }

            # Extract trace details (Heat No, MPI No)
            trace_details = {}
            if response.EtScndet and response.EtScndet.item:
                for item in response.EtScndet.item:
                    desc = (item.ZtrDesc or '').upper()
                    trace_details[desc] = {
                       
                        'heat_no': item.ZheatNo,
                        'mpi_no': item.ZmpiNo,
                        'xray_no': item.ZxrayNo,
                        'dpi_no': item.ZdpiNo
                    }

            # Extract test specifications
            tests = []
            if response.EtPreTestDurVal and response.EtPreTestDurVal.item:
                for item in response.EtPreTestDurVal.item:
                    tests.append({
                        'testId' : item.ZprTestType,
                        'name': item.ZprTestTypTxt,
                        'duration': item.ZtestDuration,
                        'pressure_bar': item.ZtestPrValBar,
                        'pressure_psi': item.ZtestPrValPsi,
                        'unit': item.ZtestDurUnit
                    })

            return JsonResponse({
                'status': 'success',
                'valve_details': valve_data,
                'trace_details': trace_details,
                'tests': tests
            })
        else:
            reason = response.EpExcmsg if response.EpExcmsg else "Serial number not found in SAP."
            return JsonResponse({'status': 'error', 'message': reason})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'SAP Connection failed: {str(e)}'})



@require_POST
@login_required
def reset_station_status(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE master_temp_data
                SET STATION_STATUS = %s    
                """,
                [0]
            )
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

@login_required

def tmpv(request):
    current_user = request.session.get('username')  # logged-in user
    superuser_flag = request.session.get('superuser')  # 0=tester, 1=admin, 2=superadmin

    # Initialize empty lists to avoid "UnboundLocalError"
    employees_tester = []
    employees_tester_user = []

    with connection.cursor() as cursor:
        # Standard names
        cursor.execute("SELECT STANDARD_NAME FROM standard ORDER BY STANDARD_NAME")
        standards = [row[0] for row in cursor.fetchall()]

        # ShellMaterial codes
        cursor.execute("SELECT SHELL_MATERIAL_NAME FROM shell_material ORDER BY SHELL_MATERIAL_NAME")
        shell_materials = [row[0] for row in cursor.fetchall()]

        # ValveSize names
        cursor.execute("SELECT SIZE_NAME FROM valvesize ORDER BY SIZE_NAME")
        valve_sizes = [row[0] for row in cursor.fetchall()]

        # ValveClass names
        cursor.execute("SELECT CLASS_NAME FROM valveclass ORDER BY CLASS_NAME")
        valve_classes = [row[0] for row in cursor.fetchall()]

        # ValveType names
        cursor.execute("SELECT TYPE_NAME FROM valve_type ORDER BY TYPE_NAME")
        valve_types = [row[0] for row in cursor.fetchall()]

        # Approver employees
        cursor.execute("SELECT name FROM newapp_employee WHERE employee_type='Approver' ORDER BY name")
        employees_approver = [row[0] for row in cursor.fetchall()]

        # Tester employees (different for tester vs admin/superadmin)
        if superuser_flag in [1, 2]:  # Admin or Superadmin
            cursor.execute("SELECT name FROM newapp_employee WHERE employee_type='Tester' ORDER BY name")
            employees_tester = [row[0] for row in cursor.fetchall()]
        else:  # Tester login → only their own name
            cursor.execute("SELECT name FROM newapp_employee WHERE name=%s", [current_user])
            employees_tester_user = [row[0] for row in cursor.fetchall()]

        # Reset station status
        cursor.execute("""
            UPDATE master_temp_data
            SET STATION_STATUS = %s,
                CYCLE_COMPLETE = %s
            WHERE STATION_STATUS = %s
        """, [0, 0, 1])

    context = {
        "newapp_standard": standards,
        "newapp_shellmaterial": shell_materials,
        "newapp_valvesize": valve_sizes,
        "newapp_valveclass": valve_classes,
        "newapp_valvetype": valve_types,
        "employees_approver": employees_approver,
        "employees_tester": employees_tester,           # All testers (for admin/superadmin)
        "employees_tester_user": employees_tester_user, # Logged-in tester (for tester login)
    }

    return render(request, "tmpv.html", context)

test_name = None
medium = None
test_category = None
pre_col_name = None
dur_col_name = None
duration = None
pressure = None
set_time_unit = None

def get_test_details(test_id):
    global test_name, medium, test_category, pre_col_name, dur_col_name
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT test_name, medium, category,pre_col_name,dur_col_name
            FROM test_type
            WHERE TEST_ID=%s
        """, [test_id])
        test_row = cursor.fetchone()
        if test_row:
            test_name, medium, test_category, pre_col_name, dur_col_name = test_row
        else:
            print(f"No details found for Test ID: {test_id}")

def get_duration(size_id, standard_id, dur_col_name):
    global duration
    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT {dur_col_name}
            FROM master_duration_data
            WHERE SIZE_ID=%s AND STANDARD_ID=%s
        """, [size_id, standard_id])
        duration_row = cursor.fetchone()
        if duration_row:
            duration = duration_row[0]
            print(f"Duration for Size ID {size_id}, Standard ID {standard_id}, Column {dur_col_name}: {duration}")
        else:
            print(f"No duration found for Size ID {size_id}, Standard ID {standard_id}, Column {dur_col_name}")

def get_pressure(class_id, shell_id, pre_col_name):
    global pressure
    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT {pre_col_name}
            FROM master_pressure_data
            WHERE SHELLMATERIAL_ID=%s AND VALVECLASS_ID=%s
        """, [shell_id, class_id])
        pressure_row = cursor.fetchone()
        if pressure_row:
            pressure = pressure_row[0]
            print(f"Pressure for Shell Material ID {shell_id}, Valve Class ID {class_id}, Column {pre_col_name}: {pressure}")
        else:
            print(f"No pressure found for Shell Material ID {shell_id}, Valve Class ID {class_id}, Column {pre_col_name}")

@csrf_exempt
@login_required
def fetch_test_data(request):
    global test_name, medium, test_category, pre_col_name, dur_col_name, duration, pressure, set_time_unit
    set_time_unit = "sec"

    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    # --- Get POST parameters ---
    standard_name = request.POST.get("standard_id")
    valve_size_name = request.POST.get("size")
    valve_class_name = request.POST.get("valve_class")
    shell_name = request.POST.get("bodymaterial")
    valve_type = request.POST.get("valve_type_id")
    pressure_unit = request.POST.get("pressure_unit")

    with connection.cursor() as cursor:
        # --- Fetch all IDs ---
        cursor.execute("SELECT STANDARD_ID FROM standard WHERE STANDARD_NAME=%s", [standard_name])
        standard_row = cursor.fetchone()

        cursor.execute("SELECT SIZE_ID FROM valvesize WHERE SIZE_NAME=%s", [valve_size_name])
        size_row = cursor.fetchone()

        cursor.execute("SELECT CLASS_ID FROM valveclass WHERE CLASS_NAME=%s", [valve_class_name])
        class_row = cursor.fetchone()

        cursor.execute("SELECT SHELL_MATERIAL_ID FROM shell_material WHERE SHELL_MATERIAL_NAME=%s", [shell_name])
        shell_row = cursor.fetchone()

        cursor.execute("SELECT TYPE_ID FROM valve_type WHERE TYPE_NAME=%s", [valve_type])
        valve_row = cursor.fetchone()

        # --- Convert to IDs or None ---
        standard_id = standard_row[0] if standard_row else None
        size_id = size_row[0] if size_row else None
        class_id = class_row[0] if class_row else None
        shell_id = shell_row[0] if shell_row else None
        valve_type_id = valve_row[0] if valve_row else None

        # --- Missing field check ---
        missing_fields = []
        if not standard_id:
            missing_fields.append(f"Standard '{standard_name}'")
        if not size_id:
            missing_fields.append(f"Valve Size '{valve_size_name}'")
        if not class_id:
            missing_fields.append(f"Valve Class '{valve_class_name}'")
        if not shell_id:
            missing_fields.append(f"Body Material '{shell_name}'")
        if not valve_type_id:
            missing_fields.append(f"Valve Type '{valve_type}'")

        if missing_fields:
            return JsonResponse({
                'status': 'error',
                'message': f"Invalid or missing selections: {', '.join(missing_fields)}."
            }, status=400)

        # --- Check combo 1: Shell + Class ---
        cursor.execute("""
            SELECT COUNT(*) 
            FROM master_pressure_data
            WHERE SHELLMATERIAL_ID = %s 
              AND VALVECLASS_ID = %s
        """, [shell_id, class_id])
        shell_class_exists = cursor.fetchone()[0]

        # --- Check combo 2: Size + Standard ---
        cursor.execute("""
            SELECT COUNT(*) 
            FROM master_duration_data
            WHERE SIZE_ID = %s 
              AND STANDARD_ID = %s
        """, [size_id, standard_id])
        size_standard_exists = cursor.fetchone()[0]

        # --- Prepare detailed error message ---
        error_parts = []
        if shell_class_exists == 0:
            error_parts.append(
                f"No matching data found for Shell Material '{shell_name}' and Valve Class '{valve_class_name}'."
            )

        if size_standard_exists == 0:
            error_parts.append(
                f"No matching data found for Valve Size '{valve_size_name}' and Standard '{standard_name}'."
            )

        # --- Return if any combo missing ---
        if error_parts:
            return JsonResponse({
                'status': 'error',
                'message': "<br>".join(error_parts)  # formatted for HTML display
            }, status=400)

        # --- Fetch linked test types ---
        cursor.execute("SELECT TEST_ID FROM valvetype_testtype WHERE TYPE_ID=%s", [valve_type_id])
        test_type_rows = cursor.fetchall()
        if not test_type_rows:
            return JsonResponse({
                'status': 'error',
                'message': f"No test types linked with Valve Type '{valve_type}'."
            }, status=400)

        # --- Process valid tests ---
        cursor.execute("TRUNCATE TABLE temp_testing_data")
        test_type_ids = [row[0] for row in test_type_rows]

        for test_id in test_type_ids:
            cursor.execute("SELECT COUNT(*) FROM test_type WHERE TEST_ID=%s AND status='ENABLE'", [test_id])
            if cursor.fetchone()[0] == 1:
                get_test_details(test_id)
                get_duration(size_id, standard_id, dur_col_name)
                get_pressure(class_id, shell_id, pre_col_name)

                if pressure is None or duration is None:
                    continue

                cursor.execute("""
                    INSERT INTO temp_testing_data
                    (TEST_ID, TEST_NAME, TEST_MEDIUM, TEST_CATEGORY, COL_PRE, COL_DUR,
                     TESTING_PR_UNIT, TESTING_PR_BAR, TESTING_PR_PSI, TESTING_PR_KGCM2,
                     TESTING_DUR_UNIT, TESTING_DUR_SEC, TESTING_DUR_MIN)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, [
                    test_id, test_name, medium, test_category, pre_col_name, dur_col_name,
                    pressure_unit, pressure, pressure * 14.5, pressure,
                    set_time_unit, duration, duration /60
                ])

        # --- Return prepared test data ---
        if pressure_unit == "bar":
            query = "SELECT TEST_NAME, TESTING_PR_BAR, TESTING_DUR_SEC FROM temp_testing_data"
        elif pressure_unit == "psi":
            query = "SELECT TEST_NAME, TESTING_PR_PSI, TESTING_DUR_SEC FROM temp_testing_data"
        elif pressure_unit == "kg/cm2":
            query = "SELECT TEST_NAME, TESTING_PR_KGCM2, TESTING_DUR_SEC FROM temp_testing_data"
        else:
            return JsonResponse({"status": "error", "message": "Invalid pressure unit"}, status=400)

        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            combo_text = (
                f"Standard = {standard_name}, "
                f"Size = {valve_size_name}, "
                f"Valve Class = {valve_class_name}, "
                f"Body Material = {shell_name}"
            )
            return JsonResponse({
                'status': 'error',
                'message': f"No test data found for this combination: {combo_text}."
            }, status=400)

        # --- Map test category ---
        cursor.execute("SELECT test_name, category FROM test_type")
        category_map = dict(cursor.fetchall())

        test_data = []
        for r in rows:
            test_name, pressure_val, duration_val = r
            category = category_map.get(test_name)
            if not category or category.strip().upper() == "NONE":
                continue
            test_data.append({
                "test_name": test_name,
                "pressure": pressure_val,
                "duration": duration_val,
                "category": category
            })

        if not test_data:
            combo_text = (
                f"Standard = {standard_name}, "
                f"Size = {valve_size_name}, "
                f"Valve Class = {valve_class_name}, "
                f"Body Material = {shell_name}"
            )
            return JsonResponse({
                'status': 'error',
                'message': f"No valid test data available for this combination: {combo_text}."
            }, status=400)

        return JsonResponse({'status': 'success', 'test_data': test_data})


@csrf_exempt
@login_required
def sap_pressure_duration(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

    try:
        test_id            = request.POST.get("test_id", "").strip()
        test_name          = request.POST.get("test_name", "").strip()
        test_pressure      = request.POST.get("test_pressure", "").strip()
        test_duration      = request.POST.get("test_duration", "").strip()
        test_pressure_unit = request.POST.get("test_pressure_unit", "psi").strip()
        test_duration_unit = request.POST.get("test_duration_unit", "sec").strip()

        # Convert numeric fields
        pressure_val = float(test_pressure) if test_pressure else None
        duration_val = float(test_duration) if test_duration else None

        if pressure_val is None or duration_val is None:
            return JsonResponse({'status': 'error', 'message': 'Invalid pressure or duration value'}, status=400)

        # Store value ONLY in the matching unit column — all others NULL
        if test_pressure_unit == "bar":
            pressure_bar, pressure_psi, pressure_kgcm2 = pressure_val, None, None
        elif test_pressure_unit == "psi":
            pressure_bar, pressure_psi, pressure_kgcm2 = None, pressure_val, None
        elif test_pressure_unit in ("kg/cm2", "kgcm2"):
            pressure_bar, pressure_psi, pressure_kgcm2 = None, None, pressure_val
        else:
            pressure_bar, pressure_psi, pressure_kgcm2 = pressure_val, None, None

        # Store duration only in the matching unit column — other NULL
        duration_sec = duration_val if test_duration_unit == "sec" else None
        duration_min = duration_val if test_duration_unit == "min" else None

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO temp_testing_data
                (TEST_ID, TEST_NAME, TEST_MEDIUM, TEST_CATEGORY, COL_PRE, COL_DUR,
                 TESTING_PR_UNIT, TESTING_PR_BAR, TESTING_PR_PSI, TESTING_PR_KGCM2,
                 TESTING_DUR_UNIT, TESTING_DUR_SEC, TESTING_DUR_MIN)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, [
                test_id, test_name, None, None, None, None,
                test_pressure_unit, pressure_bar, pressure_psi, pressure_kgcm2,
                test_duration_unit, duration_sec, duration_min
            ])

        # Write 1 to the HMI address of each enabled station
        station_id_addresses = {
            1: 2101,
            2: 2102,
            3: 2103,
            4: 2104
        }
        with connection.cursor() as cursor:
            cursor.execute("SELECT ID FROM master_temp_data WHERE STATION_STATUS = %s", [1])
            active_rows = cursor.fetchall()

        for row in active_rows:
            station_id = row[0]
            hmi_address = station_id_addresses.get(station_id)
            if hmi_address:
                TesleadSmartsyncx.write_register(hmi_address, 1)
                print(f"✅ HMI write: station {station_id} → address {hmi_address} = 1")

        return JsonResponse({'status': 'success', 'message': 'Test data saved successfully'})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    


@csrf_exempt  # since you already add CSRF header, this is optional
@login_required
def check_valve_serial(request):
    if request.method == "POST":
        serial_no = request.POST.get("valve_serial_no")
        if not serial_no:
            return JsonResponse({"exists": False})

        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM master_temp_data WHERE VALVE_SER_NO = %s", [serial_no])
            count = cursor.fetchone()[0]

        return JsonResponse({"exists": count > 0})
    return JsonResponse({"error": "Invalid method"}, status=405)

from django.http import JsonResponse
from django.db import connection

def dict_fetchall(cursor):
    """Return all rows from a cursor as a list of dicts."""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

@login_required
def checksameclassornot(request):
    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                # Find duplicate class names among active rows
                cursor.execute("""
                    SELECT CLASS_NAME
                    FROM master_temp_data
                    WHERE STATION_STATUS=1
                    GROUP BY CLASS_NAME
                    HAVING COUNT(*) > 1
                """)
                dup_classes = [r[0] for r in cursor.fetchall()]

                if dup_classes:
                    placeholders = ",".join(["%s"] * len(dup_classes))
                    cursor.execute(
                        f"""
                        SELECT ID, CLASS_NAME
                        FROM master_temp_data
                        WHERE STATION_STATUS=1 AND CLASS_NAME IN ({placeholders})
                        """,
                        dup_classes,
                    )
                    rows = dict_fetchall(cursor)
                    return JsonResponse({
                        "iserror": True,
                        "message": "Same Class Are Entered.",
                        "data": rows
                    })

                # ✅ No duplicates found
                return JsonResponse({
                    "iserror": False,
                    "message": "Classes Are Different.",
                    "data": []
                })

        except Exception as e:
            # Catch any DB or logic errors and return JSON instead of HTML
            return JsonResponse({
                "iserror": True,
                "message": f"Server error: {str(e)}",
                "data": []
            }, status=500)

    # Optional: handle POST or other methods if needed
    return JsonResponse({"iserror": True, "message": "Invalid request method"}, status=405)

@csrf_protect 
@require_POST  
@login_required
def station_update_all(request):
    if request.method == 'POST':
        try:
            station_id = request.POST.get('station_id')
            record_id = request.POST.get('id')

            # Extract fields
            pressure_unit = request.POST.get('pressure_unit')
            standard_id = request.POST.get('standard_id')
            size = request.POST.get('size')
            valve_class = request.POST.get('class')
            valve_type = request.POST.get('type')
            shell_material = request.POST.get('shell_material')
            
            # print(f"🔍 DEBUG station_update_all - Header fields received:")
            # print(f"  pressure_unit: {pressure_unit}")
            # print(f"  standard_id: {standard_id}")
            # print(f"  size: {size}")
            # print(f"  valve_class: {valve_class}")
            # print(f"  valve_type: {valve_type}")
            # print(f"  shell_material: {shell_material}")
            
            sales_order_no = request.POST.get('sales_order_no')
            sales_item_no = request.POST.get('sales_item_no')
            valve_tag_no = request.POST.get('valve_tag_no')
            valve_serial_no = request.POST.get('valve_serial_no')
            appilicalibility = request.POST.get('appilicalibility')
            body_heat = request.POST.get('body_heat')
            body_mp = request.POST.get('body_mp')
            body_rt = request.POST.get('body_rt')
            tested_by = request.POST.get('tested_by')
            approved_by = request.POST.get('approved_by')
            ga_drg_no = request.POST.get('ga_drg_no')
            cat_no = request.POST.get('catno')
            Bonnet_heat = request.POST.get('Bonnet_heat')
            Bonnet_mp = request.POST.get('Bonnet_mp')
            Bonnet_rt = request.POST.get('Bonnet_rt')
            extn_heat = request.POST.get('extn_heat')
            extn_mp = request.POST.get('extn_mp')
            extn_rt = request.POST.get('extn_rt')

            # Duplicate check for serial no (only if serial no is provided)
            if valve_serial_no:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT ID FROM master_temp_data
                        WHERE VALVE_SER_NO = %s AND ID != %s AND STATION_STATUS = 1
                    """, [valve_serial_no, record_id])
                    duplicate = cursor.fetchone()

                if duplicate:
                    return JsonResponse(
                        {'error': f'Valve Serial No "{valve_serial_no}" already exists.'},
                        status=400
                    )

            # Define column name mappings
            col_names = {
                "COL1_NAME": "Sale Order No",
                "COL2_NAME": "Sale Item no",
                "COL3_NAME": "Applicability",
                "COL4_NAME": "Valve Tag No",
                "COL5_NAME": "GAD No",
                "COL6_NAME": "Witnessed By",
                "COL7_NAME": "Tested By",
                "COL8_NAME": "Body Heat No",
                "COL9_NAME": "Body MP / DP No",
                "COL10_NAME": "Body RT No",
                "COL11_NAME": "Bonnet/Cover Heat No",
                "COL12_NAME": "Bonnet/Cover MP / DP No",
                "COL13_NAME": "Bonnet/Cover RT No",
                "COL14_NAME": "Extn/Bonnet Heat No",
                "COL15_NAME": "Extn/Bonnet MP / DP No",
                "COL16_NAME": "Extn/Bonnet RT No",
                "COL17_NAME": "Cat No",
            }

            # Prepare update fields
            update_fields = []
            update_values = []

            # Always keep the COLx_NAME fields consistent
            for col_name, name_label in col_names.items():
                update_fields.append(f"{col_name} = %s")
                update_values.append(name_label)

            # Now add COLx_VALUE fields
            field_map = {
                "COL1_VALUE": sales_order_no or None,
                "COL2_VALUE": sales_item_no or None,
                "COL3_VALUE": appilicalibility or None,
                "COL4_VALUE": valve_tag_no or None,
                "COL5_VALUE": ga_drg_no or None,
                "COL6_VALUE": approved_by or None,
                "COL7_VALUE": tested_by or None,
                "COL8_VALUE": body_heat or None,
                "COL9_VALUE": body_mp or None,
                "COL10_VALUE": body_rt or None,
                "COL11_VALUE": Bonnet_heat or None,
                "COL12_VALUE": Bonnet_mp or None,
                "COL13_VALUE": Bonnet_rt or None,
                "COL14_VALUE": extn_heat or None,
                "COL15_VALUE": extn_mp or None,
                "COL16_VALUE": extn_rt or None,
                "COL17_VALUE": cat_no or None,
            }

            for field, value in field_map.items():
                update_fields.append(f"{field} = %s")
                update_values.append(value)

            # Other general fields
            update_fields.append("PRESSURE_UNIT = %s")
            update_values.append(pressure_unit or None)
            
            update_fields.append("STANDARD_NAME = %s")
            update_values.append(standard_id or None)
            
            update_fields.append("SIZE_NAME = %s")
            update_values.append(size or None)
            
            update_fields.append("CLASS_NAME = %s")
            update_values.append(valve_class or None)
            
            update_fields.append("TYPE_NAME = %s")
            update_values.append(valve_type or None)
            
            update_fields.append("SHELL_MATERIAL_NAME = %s")
            update_values.append(shell_material or None)
            
            update_fields.append("VALVE_SER_NO = %s")
            update_values.append(valve_serial_no or None)

            # Always set STATION_STATUS active
            update_fields.append("STATION_STATUS = 1")
            update_fields.append("CYCLE_COMPLETE = 0")

            # WHERE clause
            update_values.append(record_id)

            # Execute query
            with connection.cursor() as cursor:
                query = f"UPDATE master_temp_data SET {', '.join(update_fields)} WHERE ID = %s"
                print("🔍 DEBUG SQL:", query)
                cursor.execute(query, update_values)

            print(f"🔍 DEBUG: valve_serial_no={valve_serial_no}, station_id={station_id}")

            # 🆕 CRITICAL: Check if this serial number EXISTS in temp_pressure_analysis
            is_existing_serial = False
            count_id = None
            existing_shift = None
            
            with connection.cursor() as cursor:
                # Check if serial exists in temp_pressure_analysis for THIS station (only COUNT_ID, no SHIFT)
                cursor.execute("""
                    SELECT COUNT_ID 
                    FROM temp_pressure_analysis 
                    WHERE VALVE_SER_NO = %s AND STATION_STATUS = %s
                    ORDER BY ID DESC LIMIT 1
                """, [valve_serial_no, station_id])
                temp_row = cursor.fetchone()
                
                if temp_row:
                    # Serial EXISTS in temp_pressure_analysis - UPDATE mode
                    is_existing_serial = True
                    count_id = temp_row[0]
                    print(f"✅ EXISTING SERIAL - Found in temp_pressure_analysis")
                    print(f"   COUNT_ID: {count_id}")
                else:
                    # Serial NOT in temp_pressure_analysis - NEW INSERT mode
                    is_existing_serial = False
                    count_id = None
                    print(f"🆕 NEW SERIAL - Not found in temp_pressure_analysis")
                    print(f"   COUNT_ID and SHIFT will be NULL")

            # If it's an existing serial, get SHIFT from pressure_gauge_analysis
            if is_existing_serial:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT SHIFT 
                        FROM pressure_gauge_analysis
                        WHERE VALVE_SER_NO = %s AND STATION_ID = %s
                        ORDER BY ID DESC LIMIT 1
                    """, [valve_serial_no, station_id])
                    gauge_row = cursor.fetchone()
                    
                    if gauge_row:
                        existing_shift = gauge_row[0]
                        print(f"✅ Retrieved SHIFT from pressure_gauge_analysis: {existing_shift}")
                    else:
                        existing_shift = None
                        print(f"⚠️ No SHIFT found in pressure_gauge_analysis")

            print(f"🔍 FINAL VALUES: is_existing_serial={is_existing_serial}, count_id={count_id}, shift={existing_shift}")

            # Delete existing records ONLY if it's an UPDATE (existing serial)
            if is_existing_serial:
                with connection.cursor() as cursor:
                    if count_id is not None:
                        cursor.execute("""
                            DELETE FROM pressure_gauge_analysis
                            WHERE VALVE_SER_NO = %s AND COUNT_ID = %s AND STATION_ID = %s
                        """, [valve_serial_no, count_id, station_id])
                        print(f"🗑️ DELETED existing records - valve {valve_serial_no}, COUNT_ID {count_id}, STATION {station_id}")
                    else:
                        cursor.execute("""
                            DELETE FROM pressure_gauge_analysis
                            WHERE VALVE_SER_NO = %s AND STATION_ID = %s
                        """, [valve_serial_no, station_id])
                        print(f"🗑️ DELETED existing records - valve {valve_serial_no}, STATION {station_id}")
            else:
                print(f"➕ NEW INSERT - No deletion needed")

            # Insert records into pressure_gauge_analysis
            with connection.cursor() as cursor:
                # Get gauges for THIS specific station only
                cursor.execute("""
                    SELECT INSTRUMENT_SER_NO, `RANGE`, INSTRUMENT_TYPE, CAL_DONE_DATE, CAL_DUE_DATE
                    FROM gauge_details
                    WHERE STATION_ID = %s AND ACTIVE_STATUS = 1
                """, [station_id])
                gauges = cursor.fetchall()

                if gauges:
                    # Station has gauges - insert each gauge as separate record
                    print(f"✅ Station {station_id}: Found {len(gauges)} gauges")
                    for gauge in gauges:
                        instrument_ser_no = gauge[0]
                        range_val = gauge[1]
                        instrument_type = gauge[2]
                        cal_done_date = gauge[3]
                        cal_due_date = gauge[4]

                        if is_existing_serial:
                            print(f"🔄 UPDATE mode - Inserting gauge {instrument_type} with COUNT_ID {count_id}, SHIFT {existing_shift}")
                        else:
                            print(f"➕ INSERT mode - Inserting gauge {instrument_type} with NULL COUNT_ID and SHIFT")
                        
                        cursor.execute("""
                            INSERT INTO pressure_gauge_analysis
                            (VALVE_SER_NO, INSTRUMENT_SER_NO, `RANGE`, INSTRUMENT_TYPE, 
                             CAL_DUE_DATE, CAL_DONE_DATE, STATION_ID, COUNT_ID, SHIFT, CREATED_DATE)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                        """, [
                            valve_serial_no,
                            instrument_ser_no,
                            range_val,
                            instrument_type,
                            cal_due_date,
                            cal_done_date,
                            station_id,
                            count_id if is_existing_serial else None,  # NULL for new inserts
                            existing_shift if is_existing_serial else None  # NULL for new inserts
                        ])
                else:
                    # Station has no gauges - insert one NULL record
                    if is_existing_serial:
                        print(f"🔄 UPDATE mode - Inserting NULL gauge with COUNT_ID {count_id}, SHIFT {existing_shift}")
                    else:
                        print(f"➕ INSERT mode - Inserting NULL gauge with NULL COUNT_ID and SHIFT")
                    
                    cursor.execute("""
                        INSERT INTO pressure_gauge_analysis
                        (VALVE_SER_NO, INSTRUMENT_SER_NO, `RANGE`, INSTRUMENT_TYPE, 
                         CAL_DUE_DATE, CAL_DONE_DATE, STATION_ID, COUNT_ID, SHIFT, CREATED_DATE)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    """, [
                        valve_serial_no,
                        None,
                        None,
                        None,
                        None,
                        None,
                        station_id,
                        count_id if is_existing_serial else None,  # NULL for new inserts
                        existing_shift if is_existing_serial else None  # NULL for new inserts
                    ])

            return JsonResponse({'status': 'success', 'message': 'Station data updated successfully'})

        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def live_chart(request):

    return render(request, "live_chart.html")


from django.shortcuts import render, redirect
from django.db import connection, transaction


def get_latest_shift_name():
    with connection.cursor() as cursor:
        cursor.execute("SELECT SHIFT_NAME FROM SHIFT ORDER BY ID DESC LIMIT 1")
        row = cursor.fetchone()
    return row[0] if row else ""


def build_pairs_from_post(request):
    """
    Returns list of (label, value) tuples in fixed order to match CC_COL1..CC_COL50.
    Field names are aligned with the HTML form exactly.
    """

    def _t(v, maxlen=100):
        if v is None:
            return ""
        return str(v).strip()[:maxlen]

    # List is in the order you want saved
    FIXED_FIELDS = [

        # Valve Details
        ("Valve Type Name", "valve_type_name"),

        # Valve Torque
        ("At Stem(lb-ft)/(Nm) Closing", "torque_stem_closing"),
        ("At Stem(lb-ft)/(Nm) Break Open", "torque_stem_break_open"),

        # Eye Bolt Torque
        ("Eye Bolt Torque (Nm)", "eye_bolt_torque"),

        # Water Drying Technique (multiple checkbox values)
        ("Water Drying Technique", "water_drying_technique"),

        # Drying Result
        ("Result of Drying", "drying_result"),

        # Water Travel Before Initial Testing
        ("Water Travel Before Initial Testing", "water_travel_before_initial_testing"),

        # Testing Water Temp
        ("Testing Water Temp", "testing_water_temp"),

        # Actuator SR No
        ("Actuator SR No", "actuator_sr_no"),

        # Torque Setting
        ("Torque Setting", "torque_setting"),

        # Actuator Details
        ("Actuator Main", "actuator_main"),
        ("Actuator By Pass 1", "actuator_bypass1"),
        ("Actuator By Pass 2", "actuator_bypass2"),

        # Wiring Diagram
        ("Wiring Main", "wiring_main"),
        ("Wiring By Pass 1", "wiring_bypass1"),
        ("Wiring By Pass 2", "wiring_bypass2"),

        # RPM Values
        ("RPM Main", "rpm_main"),
        ("RPM By Pass 1", "rpm_bypass1"),
        ("RPM By Pass 2", "rpm_bypass2"),

        # Open Time (Open → Close)
        ("Open Time (Open→Close) Main", "open_time_open_to_close_main"),
        ("Open Time (Open→Close) Bypass 1", "open_time_open_to_close_bypass1"),
        ("Open Time (Open→Close) Bypass 2", "open_time_open_to_close_bypass2"),

        # Open Time (Close → Open)
        ("Open Time (Close→Open) Main", "open_time_close_to_open_main"),
        ("Open Time (Close→Open) Bypass 1", "open_time_close_to_open_bypass1"),
        ("Open Time (Close→Open) Bypass 2", "open_time_close_to_open_bypass2"),

        # Remarks
        ("Remarks", "remarks"),
    ]

    pairs = []

    for label, name in FIXED_FIELDS:

        # Special handling for checkbox list:
        if name == "water_drying_technique":
            values = request.POST.getlist(name)  # returns list
            value = ", ".join(values)
        else:
            value = request.POST.get(name, "")

        pairs.append((_t(label, 50), _t(value)))

    return pairs


from django.db import transaction, connection
from django.utils import timezone
from django.contrib import messages

@transaction.atomic
def insert_master_actuator(request):
    valve_ser_no = request.POST.get("valve_serial_number", "").strip()
    remarks = request.POST.get("remarks", "")
    shift_name = get_latest_shift_name()
    cycle_complete = 1
    created_date = timezone.now()

    # Build label-value pairs from the POST data
    pairs = build_pairs_from_post(request)

    # Basic validation
    if not valve_ser_no:
        messages.error(request, "Valve serial number is missing; cannot save master_actuator.")
        print("[master_actuator DEBUG] Missing valve_ser_no. POST keys:", list(request.POST.keys()))
        return False

    # Debug info
    non_empty = [(lbl, val) for lbl, val in pairs if val]
    print(f"[DEBUG] Total pairs: {len(pairs)}")
    print(f"[DEBUG] Non-empty values: {len(non_empty)}")
    print(f"[DEBUG] Sample pairs: {pairs[:10]}")

    # -------- Get latest COUNT_ID from temp_pressure_analysis --------
    count_id = None
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT_ID
            FROM temp_pressure_analysis
            WHERE VALVE_SER_NO = %s
            ORDER BY CREATED_DATE DESC
            LIMIT 1
        """, [valve_ser_no])
        count_row = cursor.fetchone()
        if count_row:
            count_id = count_row[0]
            print(f"[DEBUG] Found COUNT_ID: {count_id} for valve {valve_ser_no}")
        else:
            print(f"[DEBUG] No COUNT_ID found for valve {valve_ser_no}")

    # -------- Check if record with VALVE_SER_NO and COUNT_ID already exists --------
    record_id = None
    if count_id is not None:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT ID
                FROM master_actuator
                WHERE VALVE_SER_NO = %s
                  AND COUNT_ID = %s
                LIMIT 1
            """, [valve_ser_no, count_id])
            existing = cursor.fetchone()
            if existing:
                record_id = existing[0]
                print(f"[DEBUG] Found existing record ID: {record_id}")

    # Prepare 50 name/value columns for the CC pairs
    name_cols = [f"CC_COL{i}_NAME" for i in range(1, 51)]
    value_cols = [f"CC_COL{i}_VALUE" for i in range(1, 51)]

    name_values = []
    value_values = []
    for i in range(50):
        if i < len(pairs):
            name_values.append(pairs[i][0])
            value_values.append(pairs[i][1])
        else:
            name_values.append("")
            value_values.append("")

    # -------- UPDATE existing record --------
    if record_id:
        all_cols = ["VALVE_SER_NO", "REMARKS"] + name_cols + value_cols + ["COUNT_ID"]
        all_values = [valve_ser_no, remarks] + name_values + value_values + [count_id]
        set_clause = ", ".join([f"{col} = %s" for col in all_cols])
        all_values.append(record_id)

        sql = f"""
            UPDATE master_actuator
            SET {set_clause}
            WHERE ID = %s
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, all_values)
            print(f"[master_actuator DEBUG] Updated existing record ID: {record_id}")
            # messages.success(request, f"Master actuator updated successfully for valve {valve_ser_no}")
            return True

        except Exception as e:
            print(f"[master_actuator UPDATE ERROR] {e}")
            messages.error(request, f"Update failed: {e}")
            return False

    # -------- INSERT new record --------
    else:
        base_cols = ["VALVE_SER_NO", "SHIFT", "CYCLE_COMPLETE", "CREATED_DATE", "REMARKS", "COUNT_ID"]
        base_values = [valve_ser_no, shift_name, cycle_complete, created_date, remarks, count_id]

        all_cols = base_cols + name_cols + value_cols
        all_values = base_values + name_values + value_values
        placeholders = ["%s"] * len(all_values)

        sql = f"""
            INSERT INTO master_actuator ({', '.join(all_cols)})
            VALUES ({', '.join(placeholders)})
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, all_values)
                try:
                    last_id = cursor.lastrowid
                    print(f"[master_actuator DEBUG] Inserted new record ID: {last_id}")
                except Exception:
                    last_id = None
            # messages.success(request, f"Master actuator saved successfully for valve {valve_ser_no}")
            return True

        except Exception as e:
            print(f"[master_actuator INSERT ERROR] {e}")
            messages.error(request, f"Insert failed: {e}")
            return False




def _apply_font_size(ws, size=12):
    try:
        max_row = ws.max_row or 0
        max_col = ws.max_column or 0
        if max_row == 0 or max_col == 0:
            return
        for row in ws.iter_rows(min_row=1, max_row=max_row, min_col=1, max_col=max_col):
            for cell in row:
                try:
                    if cell.value is not None:
                        cell.font = Font(name=(cell.font.name or 'Calibri'), size=size, bold=cell.font.bold, italic=cell.font.italic, underline=cell.font.underline, color=cell.font.color)
                except Exception:
                    continue
    except Exception:
        pass


@login_required
def cycle_complete_page(request):
    if request.method == 'POST':
        action = (request.POST.get('action') or '').strip().lower()
        if action in ('', 'save_station'):
            ok = insert_master_actuator(request)
            if ok:
                # Generate merged PDF silently to disk and update station flags
                try:
                    _generate_and_save_merged_pdf_to_disk()
                except Exception as _:
                    pass

            return redirect(request.path)
        elif action == 'generate_excel':
            # Generate a single Excel file with one sheet per active station (FBV + others).
            query = """
                SELECT ID, VALVE_SER_NO, TYPE_NAME
                FROM master_temp_data
                WHERE STATION_STATUS = 1
            """
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

            # Build combined workbook
            fbv_template_path = os.path.join(settings.BASE_DIR, "static", "templates", "floating ball valve report format.xlsx")
            tmbv_template_path = os.path.join(settings.BASE_DIR, "static", "templates", "tmbv report format.xlsx")
            fbv_template = load_workbook(fbv_template_path) if os.path.exists(fbv_template_path) else None
            tmbv_template = load_workbook(tmbv_template_path) if os.path.exists(tmbv_template_path) else None

            # Decide base by active station types
            types_lower = [((vtype or '').lower()) for (_sid, _serial, vtype) in rows]
            has_fbv = any(t in ("floating ball valve", "fbv") for t in types_lower)
            has_tmbv = any(t in ("tmbv", "trunnion mounted ball valve") for t in types_lower)

            if has_tmbv and not has_fbv and tmbv_template is not None:
                combined_wb = tmbv_template
                base_type = 'tmbv'
                template_ws = combined_wb.active
            elif has_fbv and not has_tmbv and fbv_template is not None:
                combined_wb = fbv_template
                base_type = 'fbv'
                template_ws = combined_wb.active
            else:
                # Mixed or missing templates: start with a blank workbook; we will add generic sheets
                combined_wb = Workbook()
                base_type = None
                template_ws = None

            # If no template workbook, ensure at least one sheet exists
            if not combined_wb.worksheets:
                combined_wb.create_sheet("Sheet1")

            # Helper to fill FBV sheet using template-like mapping
            def fill_fbv_sheet(ws, station_id):
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT ID, VALVE_SER_NO, TYPE_NAME
                        FROM master_temp_data
                        WHERE ID=%s
                    """, [station_id])
                    temp_row = cursor.fetchone()
                # Read actuator pairs by station id only
                pairs = _read_master_actuator_pairs_by_id(station_id)
                label_to_key = {
                    "Valve Type Name": "valve_type_name",
                    "Body to Ball: Measured Power (V)": "body_ball_power",
                    "Body to Stem/Shaft: Measured Power (V)": "body_stem_power",
                    "Actuator Timing (s) Close→Open": "timing_close_open",
                    "Actuator Timing (s) Open→Close": "timing_open_close",
                    "Actuator Torque Setting (%) Close→Open": "torque_close_open",
                    "Actuator Torque Setting (%) Open→Close": "torque_open_close",
                    "Run Torque @ Atmospheric (Nm)": "run_torque",
                    "Tightness of Gear Unit Position Stopper": "gear_unit_stopper",
                    "Measured Power (V)": "measured_power",
                    "Water Drying Technique (QM-7B)": "technique_result",
                    "Abnormal Sound During Operation": "check_sound",
                    "Water Draining After Testing": "draining_test",
                    "Torque Test (Nm) BTO at LH": "torque_lh",
                    "Torque Test (Nm) BTO at RH": "torque_rh",
                }
                kv = {}
                for label, val in pairs.items():
                    key = label_to_key.get(label)
                    if key:
                        kv[key] = val
                form_field_map = {
                    "body_ball_power": "A13",
                    "body_stem_power": "B13",
                    "timing_close_open": "U13",
                    "timing_open_close": "V13",
                    "torque_close_open": "W13",
                    "torque_open_close": "X13",
                    "torque_lh": "R13",
                    "torque_rh": "S13",
                    "run_torque": "T13",
                    "gear_unit_stopper": "X6",
                    "measured_power": "B10",
                    "check_sound": "C13",
                    "draining_test": "AA6",
                    "Water Drying Technique (QM-7B)":"Z16/Z7",
                    "Abnormal Sound During Operation":""
                }
                for k, cell in form_field_map.items():
                    if k in kv:
                        ws[cell] = kv[k]
                if temp_row:
                    _sid, _serial, _vtype = temp_row
                    ws["F13"] = _serial
                    ws["B4"] = _vtype

            # Helper to fill TMBV sheet using template-like mapping
            def fill_tmbv_sheet(ws, station_id):
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT ID, VALVE_SER_NO, TYPE_NAME
                        FROM master_temp_data
                        WHERE ID=%s
                    """, [station_id])
                    temp_row = cursor.fetchone()
                # Write header fields from pressure_analysis as per provided mapping
                valve_serial_for_query = None
                if temp_row:
                    valve_serial_for_query = temp_row[1]
                pa = None
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            SELECT valve_size, valve_class, shell_material,
                                   sales_order_no, sales_item_no, gad_no, valve_serial_number, valve_tag_no,
                                   tested_by, approved_by,
                                   gear_actuator, ma_gear_ratio, ga_drg_no,
                                   body_heat, body_mp, body_rt,
                                   connector_heat, connector_mp, connector_rt
                            FROM pressure_analysis
                            WHERE valve_serial_number = %s AND station = %s
                            ORDER BY id DESC
                            LIMIT 1
                        """, [valve_serial_for_query, station_id])
                        pa = cursor.fetchone()
                except OperationalError:
                    pa = None
                if pa:
                    pa_map = {
                        0: "K4",   # valve_size
                        1: "K5",   # valve_class
                        2: "K8",   # shell_material
                        3: "E4",   # sales_order_no
                        4: "E5",   # sales_item_no
                        5: "E6",   # gad_no
                        6: "K6",   # valve_serial_number
                        7: "L19",  # valve_tag_no
                        8: "L19",  # tested_by (note: same cell as tag per example)
                        9: "O19",  # approved_by
                        10: "K11", # gear_actuator
                        11: "K9",  # ma_gear_ratio
                        12: "K7",  # ga_drg_no
                        13: "A9",  # body_heat
                        14: "A9",  # body_mp
                        15: "A9",  # body_rt
                        16: "E9",  # connector_heat
                        17: "E9",  # connector_mp
                        18: "E9",  # connector_rt
                    }
                    for idx, cell_ref in pa_map.items():
                        try:
                            ws[cell_ref] = pa[idx]
                        except Exception:
                            pass
                pairs = _read_master_actuator_pairs_by_id(station_id)
                # Map saved keys to cells based on provided TMBV layout
                tmbv_map = {
                    "body_ball_power": "B16",
                    "body_ball_resistance": "C16",
                    "body_stem_power": "B17",
                    "body_stem_resistance": "C17",
                    "timing_close_open": "E20",
                    "timing_open_close": "F20",
                    "torque_close_open": "A20",
                    "torque_open_close": "C20",
                    "sizing_pressure": "G20",
                    "run_torque": "Q15",
                    "gear_unit_stopper": "R19",
                    "bto_dbb": "M15",
                    "bto_dbb_result": "M16",
                    "bto_connector_l": "N15",
                    "bto_connector_l_result": "N16",
                    "bto_connector_r": "O15",
                    "bto_connector_r_result": "O16",
                    "btc": "P15",
                    "btc_result": "P16",
                    "check_sound": "R26",
                    "draining_test": "T26",
                }
                for k, cell in tmbv_map.items():
                    if k in pairs:
                        ws[cell] = pairs[k]
                if temp_row:
                    _sid, _serial, _vtype = temp_row
                    # Ensure serial and station info are present
                    ws["K6"] = _serial
                    ws["L19"] = f"Station {_sid}"
                    ws["K4"] = _vtype

            # Helper to add a generic sheet for non-template stations
            def add_generic_sheet(wb, station_id, title):
                ws = wb.create_sheet(title)
                ws["A1"] = "Field"
                ws["B1"] = "Value"
                # Temp header
                with connection.cursor() as cursor:
                    cursor.execute("SELECT VALVE_SER_NO, TYPE_NAME FROM master_temp_data WHERE ID=%s", [station_id])
                    row = cursor.fetchone()
                if row:
                    ws["D1"] = "Serial"
                    ws["E1"] = row[0]
                    ws["D2"] = "Type"
                    ws["E2"] = row[1]
                pairs = _read_master_actuator_pairs_by_id(station_id)
                r = 2
                for name, value in pairs.items():
                    ws.cell(row=r, column=1, value=name)
                    ws.cell(row=r, column=2, value=value)
                    r += 1
                return ws

            # Build per-station sheets
            fbv_template_ws = template_ws if base_type == 'fbv' else None
            tmbv_template_ws = template_ws if base_type == 'tmbv' else None
            for sid, serial, vtype in rows:
                vtype_l = (vtype or '').lower()
                title = f"Station_{sid}"
                if vtype_l in ("floating ball valve", "fbv") and fbv_template_ws:
                    # Always copy from the untouched template sheet
                    ws = combined_wb.copy_worksheet(fbv_template_ws)
                    ws.title = title
                    fill_fbv_sheet(ws, sid)
                elif vtype_l in ("tmbv", "trunnion mounted ball valve") and tmbv_template_ws:
                    ws = combined_wb.copy_worksheet(tmbv_template_ws)
                    ws.title = title
                    fill_tmbv_sheet(ws, sid)
                else:
                    # No matching template in the combined workbook: fallback to generic
                    add_generic_sheet(combined_wb, sid, title)

            # Remove the original template sheet if it still exists and is unused
            if template_ws and template_ws in combined_wb.worksheets:
                try:
                    combined_wb.remove(template_ws)
                except Exception:
                    pass

            out = io.BytesIO()
            combined_wb.save(out)
            out.seek(0)
            # After generating Excel, update station flags
           
            resp = HttpResponse(out.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            resp['Content-Disposition'] = 'attachment; filename="active_station_reports.xlsx"'
            return resp

    query = """
        SELECT ID, VALVE_SER_NO, TYPE_NAME, COL7_VALUE, COL11_VALUE
        FROM master_temp_data
        WHERE STATION_STATUS = 1
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # ✅ Pass additional Yes/No fields to template
    stations = []
    for row in rows:
        serial_no = row[1]
        
        stations.append({
            'id': row[0],
            'valve_serial_number': serial_no,
            'valve_type': row[2],
            'col7_value': row[3],
            'col11_value': row[4],
        })
        with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE pressure_analysis
                    SET CYCLE_COMPLETE = %s
                    WHERE VALVE_SER_NO = %s
                    AND (CYCLE_COMPLETE IS NULL OR CYCLE_COMPLETE = '' OR CYCLE_COMPLETE != 'Not Completed')
                """, ["yes", serial_no])
        TesleadSmartsyncx.write_register(2000,0) # set pressure
        TesleadSmartsyncx.write_register(2001,0) # valve size
        TesleadSmartsyncx.write_register(2002,0) # valve class
        TesleadSmartsyncx.write_register(2003,0) # set time
        TesleadSmartsyncx.write_register(2004,0) # Test Type
        TesleadSmartsyncx.write_register(2101,0) # station 1 Enable/ Disable
        TesleadSmartsyncx.write_register(2102,0) # station 2 Enable/ Disable
        TesleadSmartsyncx.write_register(2103,0) # station 3 Enable/ Disable
        TesleadSmartsyncx.write_register(2104,0) # station 4 Enable/ Disable
        TesleadSmartsyncx.write_register(2006,0) # Actual time
        TesleadSmartsyncx.write_register(2011,0) # station 1 result
        TesleadSmartsyncx.write_register(2025,0) # station 2 result
        TesleadSmartsyncx.write_register(2026,0) # station 3 result
        TesleadSmartsyncx.write_register(2027,0) # station 4 result
        TesleadSmartsyncx.write_register(2105,0) # pressure unit

   
    return render(request, 'cycle_complete.html', {'stations': stations})


def _read_master_actuator_pairs_by_id(station_id):
    cols = []
    for i in range(1, 51):
        cols.append(f"CC_COL{i}_NAME")
        cols.append(f"CC_COL{i}_VALUE")
    sel = ", ".join(cols)
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {sel} FROM master_actuator WHERE ID=%s", [station_id])
        row = cursor.fetchone()
    result = {}
    if not row:
        return result
    # Build name->value dict ignoring empty names
    for i in range(0, len(cols), 2):
        name = row[i]
        value = row[i+1]
        if name and str(name).strip() != "":
            result[str(name).strip()] = value
    return result


def _read_master_actuator_pairs_by_serial(valve_serial_number):
    cols = []
    for i in range(1, 51):
        cols.append(f"CC_COL{i}_NAME")
        cols.append(f"CC_COL{i}_VALUE")
    sel = ", ".join(cols)
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {sel} FROM master_actuator WHERE VALVE_SER_NO=%s ORDER BY ID DESC LIMIT 1", [valve_serial_number])
        row = cursor.fetchone()
    result = {}
    if not row:
        return result
    for i in range(0, len(cols), 2):
        name = row[i]
        value = row[i+1]
        if name and str(name).strip() != "":
            result[str(name).strip()] = value
    return result

def _safe_set(ws, cell_ref, value):
    """Write value to cell, resolving merged cells to their top-left anchor."""
    try:
        cell = ws[cell_ref]
        # If cell_ref falls inside a merged range, write to top-left
        for rng in ws.merged_cells.ranges:
            if cell.coordinate in rng:
                top_left = f"{get_column_letter(rng.min_col)}{rng.min_row}"
                ws[top_left].value = value
                return
        cell.value = value
    except Exception:
        try:
            ws[cell_ref] = value
        except Exception:
            pass

import io, os, traceback
from openpyxl import load_workbook
from openpyxl.styles import Font
from django.db import connection
from django.conf import settings
from datetime import datetime

def _safe_set(ws, cell, value):
    """Safely write to Excel cell."""
    try:
        ws[cell] = "" if value is None else str(value)
        try:
            c = ws[cell]
            c.font = Font(
                name=(c.font.name or 'Calibri'),
                size=(c.font.size or 11),
                bold=c.font.bold,
                italic=c.font.italic,
                underline=c.font.underline,
                color="000000"
            )
        except Exception:
            pass
    except Exception:
        pass





import os
import io
from datetime import datetime
from openpyxl import load_workbook
from django.conf import settings
from django.db import connection
from openpyxl.styles import Font
import os
import io
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import Alignment
from django.conf import settings
from django.db import connection


def _safe_set(ws, cell, value):
    """Set Excel cell value safely."""
    try:
        ws[cell] = value if value is not None else "N/A"
    except Exception as e:
        print(f"Failed to set {cell}: {e}")

def _apply_font_size(ws, size=12):
    """Apply font size to all cells."""
    for row in ws.iter_rows():
        for cell in row:
            if cell.value is not None:
                cell.font = Font(size=size)


def export_fbv_report_from_master(station_id, valve_serial_number=None):
    # Load Excel Template
    template_path = os.path.join(settings.BASE_DIR, "static", "templates", "floating ball valve report format.xlsx")
    wb = load_workbook(template_path)
    ws = wb.active
    ws.title = "Raw Query Export"

    # 1️⃣ Fetch master_temp_data (if station_id is valid and not 0)
    temp = {}
    serial = valve_serial_number  # Use provided serial if available
    if station_id and station_id != 0:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM master_temp_data WHERE ID=%s", [station_id])
                trow = cursor.fetchone()
                tcols = [d[0].upper() for d in cursor.description] if cursor.description else []
                if trow:
                    temp = {tcols[i]: trow[i] for i in range(len(tcols))}
                    if not serial:  # Only use from master_temp_data if serial not provided
                        serial = temp.get("VALVE_SER_NO")
        except Exception:
            pass  # If master_temp_data doesn't exist or fails, continue with serial parameter

    # 2️⃣ Fetch latest pressure_analysis
    pa = {}
    with connection.cursor() as cpa:
        if serial:
            cpa.execute("SELECT * FROM pressure_analysis WHERE VALVE_SER_NO=%s ORDER BY ID DESC LIMIT 1", [serial])
        else:
            cpa.execute("SELECT * FROM pressure_analysis WHERE STATION_ID=%s ORDER BY ID DESC LIMIT 1", [station_id])
        prow = cpa.fetchone()
        pcols = [d[0].upper() for d in cpa.description] if cpa.description else []
        if prow:
            pa = {pcols[i]: prow[i] for i in range(len(pcols))}

    # 3️⃣ Fetch latest master_actuator
    act = {}
    with connection.cursor() as ca:
        if serial:
            ca.execute("SELECT * FROM master_actuator WHERE VALVE_SER_NO=%s ORDER BY ID DESC LIMIT 1", [serial])
        else:
            ca.execute("SELECT * FROM master_actuator WHERE STATION_ID=%s ORDER BY ID DESC LIMIT 1", [station_id])
        arow = ca.fetchone()
        acols = [d[0].upper() for d in ca.description] if ca.description else []
        if arow:
            act = {acols[i]: arow[i] for i in range(len(acols))}

    # 4️⃣ Fetch pressure_gauge_analysis
    pg_rows = []
    with connection.cursor() as cpg:
        if serial:
            cpg.execute("""
                SELECT INSTRUMENT_TYPE, CAL_DUE_DATE, CAL_DONE_DATE, INSTRUMENT_SER_NO, `RANGE`
                FROM pressure_gauge_analysis
                WHERE VALVE_SER_NO=%s
                ORDER BY ID ASC
            """, [serial])
        else:
            cpg.execute("""
                SELECT INSTRUMENT_TYPE, CAL_DUE_DATE, CAL_DONE_DATE, INSTRUMENT_SER_NO, `RANGE`
                FROM pressure_gauge_analysis
                WHERE STATION_ID=%s
                ORDER BY ID ASC
            """, [station_id])
        pg_rows = cpg.fetchall() or []

    # 5️⃣ Fill pressure_analysis & master_temp_data fields
    pa_map = {
        "COL1_VALUE": "D13", "COL2_VALUE": "E13", "COL8_VALUE": "D7", "COL13_VALUE": "G13",
        "COL14_VALUE": "H13", "COL15_VALUE": "I13", "COL16_VALUE": "J13", "COL17_VALUE": "K13",
        "COL18_VALUE": "L13", "VALVESIZE_NAME": "B4", "VALVECLASS_NAME": "B5", "VALVE_SER_NO": "F13",
        "COL5_VALUE": "B7", "SHELLMATERIAL_NAME": "B6", "COL12_VALUE": "D5", "COL7_VALUE": "D6",
        "COL10_VALUE": "Y13", "COL9_VALUE": "Z13", "COL6_VALUE": "D4",
    }
    for field, cell in pa_map.items():
        value = pa.get(field) or temp.get(field)
        _safe_set(ws, cell, value)

    # 6️⃣ Fill master_actuator fields
    act_map = {
        "CC_COL2_VALUE": "A13", "CC_COL4_VALUE": "B13", "CC_COL8_VALUE": "U13", "CC_COL9_VALUE": "V13",
        "CC_COL6_VALUE": "W13", "CC_COL7_VALUE": "X13", "CC_COL13_VALUE": "X6",
        "CC_COL16_VALUE": "C13", "CC_COL17_VALUE": "AA6", "CC_COL12_VALUE": "T13", "CC_COL27_VALUE": "AA13",
        "CC_COL10_VALUE": "R13", "CC_COL11_VALUE": "S13", "CC_COL14_VALUE": "B10",
        "CC_COL28_VALUE": "AA13", "CC_COL19_VALUE": "S6", "SHIFT": "AA3"
    }
    for field, cell in act_map.items():
        _safe_set(ws, cell, act.get(field))

    if act.get("CC_COL27_VALUE"):
        _safe_set(ws, "AA13", act.get("CC_COL27_VALUE"))

    # 6.1️⃣ FBV test-specific fields with pressure unit conversion
    try:
        with connection.cursor() as cx:
            if serial:
                cx.execute("""
                    SELECT TEST_NAME, SET_PRESSURE, SET_TIME, VALVE_STATUS, PRESSURE_UNIT
                    FROM pressure_analysis
                    WHERE VALVE_SER_NO=%s AND TEST_NAME<>'' ORDER BY ID DESC LIMIT 200
                """, [serial])
            else:
                cx.execute("""
                    SELECT TEST_NAME, SET_PRESSURE, SET_TIME, VALVE_STATUS, PRESSURE_UNIT
                    FROM pressure_analysis
                    WHERE STATION_ID=%s AND TEST_NAME<>'' ORDER BY ID DESC LIMIT 200
                """, [station_id])
            rows = cx.fetchall() or []

        def norm(s): return (str(s) if s else '').strip().lower()
        def is_fail(x): return norm(x) in ('fail', 'failed', 'not ok', 'ng')
        def conv_pressure(val, unit):
            try:
                val = float(val)
                if str(unit).strip().lower() == 'psi':
                    return round(val / 14.5038, 2)
                return val
            except Exception:
                return val

        shell_rows = [r for r in rows if 'shell' in norm(r[0]) and ('primary' in norm(r[0]) or 'hydro' in norm(r[0]))]
        hydro_seat_rows = [r for r in rows if 'hydro seat' in norm(r[0])]
        torque_rows = [r for r in rows if 'torque' in norm(r[0])]
        air_seat_rows = [r for r in rows if 'air seat' in norm(r[0])]

        # SHELL
        if shell_rows:
            _safe_set(ws, 'M6', conv_pressure(shell_rows[0][1], shell_rows[0][4]))
            _safe_set(ws, 'N12', shell_rows[0][2])
            _safe_set(ws, 'N13', 'FAIL' if any(is_fail(r[3]) for r in shell_rows) else 'PASS')
        else:
            _safe_set(ws, 'M6', 'N/A')
            _safe_set(ws, 'N12', 'N/A')
            _safe_set(ws, 'N13', 'N/A')

        # HYDRO SEAT
        if hydro_seat_rows:
            _safe_set(ws, 'O6', conv_pressure(hydro_seat_rows[0][1], hydro_seat_rows[0][4]))
            _safe_set(ws, 'O12', hydro_seat_rows[0][2])
            _safe_set(ws, 'O13', 'FAIL' if any(is_fail(r[3]) for r in hydro_seat_rows) else 'PASS')
        else:
            _safe_set(ws, 'O6', 'N/A')
            _safe_set(ws, 'O12', 'N/A')
            _safe_set(ws, 'O13', 'N/A')

        # TORQUE
        if torque_rows:
            _safe_set(ws, 'Q6', conv_pressure(torque_rows[0][1], torque_rows[0][4]))
            _safe_set(ws, 'Q13', 'FAIL' if any(is_fail(r[3]) for r in torque_rows) else 'PASS')
        else:
            _safe_set(ws, 'Q6', 'N/A')
            _safe_set(ws, 'Q13', 'N/A')

        # AIR SEAT
        if air_seat_rows:
            _safe_set(ws, 'U6', conv_pressure(air_seat_rows[0][1], air_seat_rows[0][4]))
            _safe_set(ws, 'P12', air_seat_rows[0][2])
            _safe_set(ws, 'P13', 'FAIL' if any(is_fail(r[3]) for r in air_seat_rows) else 'PASS')
        else:
            _safe_set(ws, 'U6', 'N/A')
            _safe_set(ws, 'P12', 'N/A')
            _safe_set(ws, 'P13', 'N/A')

        # OVERALL RESULT
        results = [str(ws[c].value).strip().upper() for c in ['N13', 'O13', 'P13'] if ws[c].value]
        if results:
            if any(r == 'PASS' for r in results) and all(r in ('PASS', 'N/A') for r in results):
                _safe_set(ws, 'Q13', 'PASS')
            else:
                _safe_set(ws, 'Q13', 'FAIL')
        else:
            _safe_set(ws, 'Q13', '')

    except Exception as e:
        print(f"Error in test-specific logic: {e}")

    # 7️⃣ Fill pressure_gauge_analysis
    if not pg_rows:
        _safe_set(ws, "G5", "N/A")
        _safe_set(ws, "K5", "N/A")
    else:
        valid_types = {"hydro", "air", "gas"}
        filtered_rows = [r for r in pg_rows if str(r[0]).strip().lower() in valid_types]

        if not filtered_rows:
            _safe_set(ws, "G5", "N/A")
            _safe_set(ws, "K5", "N/A")
        else:
            serial_lines = []
            due_lines = []
            for row in filtered_rows[:4]:
                itype, cal_due, _, serno, rng = row
                serial_lines.append(str(serno or "N/A"))
                due_lines.append(cal_due.strftime("%d-%m-%Y") if cal_due else "N/A")

            ws["G5"].value = "\n".join(serial_lines)
            ws["K5"].value = "\n".join(due_lines)

            align_center = Alignment(horizontal="center", vertical="center", wrapText=True)
            ws["G5"].alignment = align_center
            ws["K5"].alignment = align_center

        # Fill instrument details (unique types only, excluding Hydro, Air, Gas)
        cell_map = [
            ("A15", "E15", "J15"),
            ("A16", "E16", "J16"),
            ("N15", "T15", "Y15"),
            ("N16", "T16", "Y16"),
        ]
        excluded_types = {"hydro", "air", "gas"}

        unique_instruments = {}
        for row in pg_rows:
            itype, cal_due, _, serno, rng = row
            type_lower = str(itype).strip().lower()

            if type_lower in excluded_types or not itype:
                continue

            if type_lower not in unique_instruments:
                unique_instruments[type_lower] = row
            else:
                old_cal_due = unique_instruments[type_lower][1]
                if cal_due and (not old_cal_due or cal_due > old_cal_due):
                    unique_instruments[type_lower] = row

        sorted_unique = list(unique_instruments.values())[:4]
        for i, row in enumerate(sorted_unique):
            if i >= len(cell_map):
                break
            itype, cal_due, _, serno, rng = row
            combo = f"{serno or ''}/{rng or ''}".strip("/") or "N/A"
            cal_due_str = cal_due.strftime("%d-%m-%Y") if cal_due else "N/A"
            _safe_set(ws, cell_map[i][0], itype or "N/A")
            _safe_set(ws, cell_map[i][1], combo)
            _safe_set(ws, cell_map[i][2], cal_due_str)

    # 8️⃣ Current Date
    _safe_set(ws, "Y3", datetime.now().strftime("%d-%m-%Y"))

    align_center = Alignment(horizontal="center", vertical="center", wrapText=True)
    for row in ws.iter_rows():
        for cell in row:
            if cell.value is not None and str(cell.value).strip() != "":
                cell.alignment = align_center

    # 9️⃣ Save to BytesIO
    _apply_font_size(ws, size=13)
    out = io.BytesIO()
    wb.save(out)
    out.seek(0)
    return out



from django.db import connection, OperationalError


@login_required
def download_fbv_report(request, station_id):
    try:
        out = export_fbv_report_from_master(station_id)
    except Exception as e:
        return HttpResponse(f"Error generating report: {e}", status=500)

    resp = HttpResponse(
        out.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    resp['Content-Disposition'] = f'attachment; filename="FBV_station_{station_id}.xlsx"'
    return resp


@login_required
def download_active_fbv_reports(request):
    # Find all active stations across possible sources
    station_ids = []
    with connection.cursor() as cursor:
        # Primary source
        cursor.execute(
            """
            SELECT ID FROM master_temp_data WHERE STATION_STATUS = 1
            ORDER BY ID
            """
        )
        station_ids += [r[0] for r in cursor.fetchall()]

        # Alternative source (if used elsewhere in project)
        try:
            cursor.execute(
                """
                SELECT id FROM master_temp_data1 WHERE station_status = 'active'
                ORDER BY id
                """
            )
            station_ids += [r[0] for r in cursor.fetchall()]
        except Exception:
            pass

    # De-duplicate and sort
    station_ids = sorted(list({int(s) for s in station_ids}))

    if not station_ids:
        return HttpResponse("No active stations found", status=404)

    # Return an HTML page that sequentially triggers downloads for each station
    ids_js = ",".join(str(sid) for sid in station_ids)
    autostart = request.GET.get('autostart') in ('1', 'true', 'yes')
    autostart_js = "next();" if autostart else ""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset='utf-8'>
      <title>Downloading FBV Reports</title>
    </head>
    <body>
      <h4>Starting downloads for active stations: [{', '.join(str(s) for s in station_ids)}]</h4>
      <p>If your browser blocks multiple downloads, please allow them.</p>
      <button id="startBtn">Start Downloads</button>
      <div id="links" style="display:none;"></div>
      <script>
        (function() {{
          var ids = [{ids_js}];
          console.log('Active station IDs:', ids);
          var idx = 0;
          function next() {{
            if (idx >= ids.length) {{ console.log('All downloads triggered'); return; }}
            var sid = ids[idx++];
            console.log('Downloading station', sid);
            var a = document.createElement('a');
            var bust = Date.now() + '_' + sid;
            a.href = '/fbv-report/' + sid + '/?t=' + bust;
            a.download = 'FBV_station_' + sid + '.xlsx';
            a.style.display = 'none';
            document.getElementById('links').appendChild(a);
            a.click();
            setTimeout(next, 3000);
          }}
          document.getElementById('startBtn').addEventListener('click', function() {{
            next();
          }});
          {autostart_js}
        }})();
      </script>
    </body>
    </html>
    """
    return HttpResponse(html)

@login_required
def download_tmbv_report(request, station_id):
    try:
        out = export_tmbv_report_from_master(None, station_id)
    except Exception as e:
        return HttpResponse(f"Error generating TMBV report: {e}", status=500)

    resp = HttpResponse(
        out.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    resp['Content-Disposition'] = f'attachment; filename="TMBV_station_{station_id}.xlsx"'
    return resp


@login_required
def download_active_tmbv_reports(request):
    # Find all active stations across possible sources
    station_ids = []
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT ID FROM master_temp_data WHERE STATION_STATUS = 1
            ORDER BY ID
            """
        )
        station_ids += [r[0] for r in cursor.fetchall()]
        try:
            cursor.execute(
                """
                SELECT id FROM master_temp_data1 WHERE station_status = 'active'
                ORDER BY id
                """
            )
            station_ids += [r[0] for r in cursor.fetchall()]
        except Exception:
            pass

    station_ids = sorted(list({int(s) for s in station_ids}))
    if not station_ids:
        return HttpResponse("No active stations found", status=404)

    ids_js = ",".join(str(sid) for sid in station_ids)
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset='utf-8'>
      <title>Downloading TMBV Reports</title>
    </head>
    <body>
      <h4>Starting downloads for active stations: [{', '.join(str(s) for s in station_ids)}]</h4>
      <p>If your browser blocks multiple downloads, please allow them.</p>
      <button id=\"startBtn\">Start Downloads</button>
      <div id=\"links\" style=\"display:none;\"></div>
      <script>
        (function() {{
          var ids = [{ids_js}];
          console.log('Active station IDs:', ids);
          var idx = 0;
          function next() {{
            if (idx >= ids.length) {{ console.log('All downloads triggered'); return; }}
            var sid = ids[idx++];
            console.log('Downloading station', sid);
            var a = document.createElement('a');
            var bust = Date.now() + '_' + sid;
            a.href = '/tmbv-report/' + sid + '/?t=' + bust;
            a.download = 'TMBV_station_' + sid + '.xlsx';
            a.style.display = 'none';
            document.getElementById('links').appendChild(a);
            a.click();
            setTimeout(next, 3000);
          }}
          document.getElementById('startBtn').addEventListener('click', function() {{
            next();
          }});
        }})();
      </script>
    </body>
    </html>
    """
    return HttpResponse(html)



import os
import io
from datetime import datetime
from django.conf import settings
from django.db import connection
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
from openpyxl.cell.cell import MergedCell

# ================================================================
# Helper: Safe Excel Write (fixes MergedCell error)
# ================================================================
def _safe_set(ws, cell, value):
    """Safely set Excel cell value, even if it's part of a merged range."""
    try:
        target = ws[cell]
        if isinstance(target, MergedCell):
            # Find merged range and redirect to top-left cell
            for merged_range in ws.merged_cells.ranges:
                if cell in merged_range:
                    top_left = ws.cell(
                        row=merged_range.min_row,
                        column=merged_range.min_col
                    )
                    top_left.value = value if value is not None else "N/A"
                    return
            print(f"⚠️ Skipped merged cell {cell}: not found in merged ranges.")
        else:
            target.value = value if value is not None else "N/A"
    except Exception as e:
        print(f"❌ Failed to set {cell}: {e}")

# ================================================================
# Helper: Apply font size
# ================================================================
def _apply_font_size(ws, size=12):
    """Apply font size to all cells."""
    for row in ws.iter_rows():
        for cell in row:
            if cell.value is not None:
                cell.font = Font(size=size)
import os
import io
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font
from django.db import connection
from django.conf import settings
import os


def export_valve_report_from_master(station_id, valve_serial_number=None, count_id=None):
    # ---------------- Utility functions ----------------
    def _safe_set(ws, cell, value, append=False):
        """Safely set a cell value. If append=True, append with a comma."""
        try:
            if hasattr(ws[cell], 'value'):
                if append and ws[cell].value not in (None, ""):
                    ws[cell].value = f"{ws[cell].value}, {value}" if value not in (None, "") else ws[cell].value
                else:
                    ws[cell].value = value if value not in (None, "") else ""
        except Exception:
            pass

    def _apply_font_size(ws, size=10):
        for row in ws.iter_rows():
            for cell in row:
                if cell.value not in (None, ""):
                    cell.font = Font(size=size)

    # ---------------- Load Excel template ----------------
    template_path = os.path.join(settings.BASE_DIR, "static", "templates", "gcc report format.xlsx")
    wb = load_workbook(template_path)
    ws = wb.active
    ws.title = "Raw Query Export"

    # ---------------- Fetch master_temp_data ----------------
    temp = {}
    serial = valve_serial_number
    if station_id and station_id != 0:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM master_temp_data WHERE ID=%s", [station_id])
                trow = cursor.fetchone()
                tcols = [d[0].upper() for d in cursor.description] if cursor.description else []
                if trow:
                    temp = {tcols[i]: trow[i] for i in range(len(tcols))}
                    if not serial:
                        serial = temp.get("VALVE_SER_NO")
        except Exception:
            pass

    # ---------------- 🆕 Get COUNT_ID from pressure_analysis ----------------
    if count_id is None:
        count_id = None
        with connection.cursor() as cursor:
            if serial:
                cursor.execute("""
                    SELECT COUNT_ID FROM pressure_analysis 
                    WHERE VALVE_SER_NO=%s 
                    ORDER BY ID DESC LIMIT 1
                """, [serial])
            else:
                cursor.execute("""
                    SELECT COUNT_ID FROM pressure_analysis 
                    WHERE STATION_STATUS=%s 
                    ORDER BY ID DESC LIMIT 1
                """, [station_id])
            row = cursor.fetchone()
            count_id = row[0] if row else None
    
    print(f"📊 Generating report for Serial: {serial}, COUNT_ID: {count_id}")

    # ---------------- Fetch pressure_analysis BASED ON COUNT_ID ----------------
    pa = {}
    if count_id is not None:
        with connection.cursor() as cpa:
            if serial:
                cpa.execute("""
                    SELECT * FROM pressure_analysis 
                    WHERE VALVE_SER_NO=%s AND COUNT_ID=%s 
                    ORDER BY ID DESC LIMIT 1
                """, [serial, count_id])
            else:
                cpa.execute("""
                    SELECT * FROM pressure_analysis 
                    WHERE STATION_STATUS=%s AND COUNT_ID=%s 
                    ORDER BY ID DESC LIMIT 1
                """, [station_id, count_id])
            prow = cpa.fetchone()
            pcols = [d[0].upper() for d in cpa.description] if cpa.description else []
            if prow:
                pa = {pcols[i]: prow[i] for i in range(len(pcols))}
                print(f"✅ Found pressure_analysis data for COUNT_ID={count_id}")
    else:
        print("⚠️ No COUNT_ID found, using latest pressure_analysis data")
        with connection.cursor() as cpa:
            if serial:
                cpa.execute("""
                    SELECT * FROM pressure_analysis 
                    WHERE VALVE_SER_NO=%s 
                    ORDER BY ID DESC LIMIT 1
                """, [serial])
            else:
                cpa.execute("""
                    SELECT * FROM pressure_analysis 
                    WHERE STATION_STATUS=%s 
                    ORDER BY ID DESC LIMIT 1
                """, [station_id])
            prow = cpa.fetchone()
            pcols = [d[0].upper() for d in cpa.description] if cpa.description else []
            if prow:
                pa = {pcols[i]: prow[i] for i in range(len(pcols))}

    # ---------------- 🆕 Fetch latest SHIFT_NAME from shift table ----------------
    shift_name = None
    try:
        with connection.cursor() as cs:
            cs.execute("""
                SELECT SHIFT
                FROM pressure_gauge_analysis
                WHERE VALVE_SER_NO=%s AND COUNT_ID=%s
                ORDER BY ID DESC LIMIT 1
            """, [serial, count_id])

           
            shift_row = cs.fetchone()
            if shift_row:
                shift_name = shift_row[0]
                print(f"✅ Found shift: {shift_name}")
    except Exception as e:
        print(f"⚠️ Error fetching shift: {e}")

    # ---------------- Fetch master_actuator BASED ON COUNT_ID ----------------
    act = {}
    with connection.cursor() as ca:
        if serial and count_id is not None:
            ca.execute("""
                SELECT * FROM master_actuator 
                WHERE VALVE_SER_NO=%s AND COUNT_ID=%s
                ORDER BY ID DESC LIMIT 1
            """, [serial, count_id])
        elif serial:
            ca.execute("""
                SELECT * FROM master_actuator 
                WHERE VALVE_SER_NO=%s 
                ORDER BY ID DESC LIMIT 1
            """, [serial])
        else:
            ca.execute("""
                SELECT * FROM master_actuator 
                WHERE VALVE_SER_NO=%s 
                ORDER BY ID DESC LIMIT 1
            """, [serial])
        arow = ca.fetchone()
        acols = [d[0].upper() for d in ca.description] if ca.description else []
        if arow:
            act = {acols[i]: arow[i] for i in range(len(acols))}

    # ---------------- Fill master data & pressure_analysis ----------------
    pa_map_with_titles = {
        "COL8_VALUE": ("V9", "Heat No"),
        "COL9_VALUE": ("V10", "MP/DP No"),
        "COL10_VALUE": ("V11", "RT No"),
        "COL11_VALUE": ("W9", "Heat No"),
        "COL12_VALUE": ("W10", "MP/DP No"),
        "COL13_VALUE": ("W11", "RT No"),
        "COL14_VALUE": ("X9", "Heat No"),
        "COL15_VALUE": ("X10", "MP/DP No"),
        "COL16_VALUE": ("X11", "RT No"),
    }

    additional_pa_map = {
        "COL1_VALUE": "H9",
        "COL2_VALUE": "H9",
        "VALVESIZE_NAME": "B9",
        "VALVECLASS_NAME": "B9",
        "VALVE_SER_NO": "R9",
        "COL5_VALUE": "J9",
        "SHELLMATERIAL_NAME": "F9",
        "COL7_VALUE": "AG41",
        "COL6_VALUE": "AJ41",
        "COL4_VALUE": "M9",
        "VALVETYPE_NAME": "C9",
        "COL17_VALUE": "C9",
    }

    for key, (cell, title) in pa_map_with_titles.items():
        value = pa.get(key) or temp.get(key) or "N/A"
        _safe_set(ws, cell, f"{title}: {value}", append=False)
        ws[cell].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    for key, cell in additional_pa_map.items():
        if key not in pa_map_with_titles:
            value = pa.get(key) or temp.get(key) or "N/A"
            _safe_set(ws, cell, value, append=True)
            ws[cell].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # ---------------- Fill master_actuator fields ----------------
    act_map = {
        "CC_COL2_VALUE": "AF9","CC_COL3_VALUE":"AG9", "CC_COL4_VALUE": "AH9", "CC_COL6_VALUE": "AK9",
        "CC_COL7_VALUE":"Y9", "CC_COL8_VALUE": "AL9","CC_COL10_VALUE": "AJ28",
        "CC_COL11_VALUE": "Y28","CC_COL12_VALUE":"Y28","CC_COL13_VALUE":"Y28",
        "CC_COL14_VALUE": "Y32","CC_COL15_VALUE": "Y32","CC_COL16_VALUE":"Y32",
        "CC_COL17_VALUE": "AF28","CC_COL18_VALUE": "AF28","CC_COL19_VALUE": "AF28",
        "CC_COL20_VALUE": "AF32","CC_COL21_VALUE": "AF32","CC_COL22_VALUE":"AF32",
        "CC_COL23_VALUE": "AJ32","CC_COL24_VALUE": "AJ32","CC_COL25_VALUE": "AJ32",
        "REMARKS": "J47"
    }

    for field, cell in act_map.items():
        _safe_set(ws, cell, act.get(field), append=True)

    # ---------------- 🆕 Set SHIFT from shift table (NOT from master_actuator) ----------------
    if shift_name:
        _safe_set(ws, "AJ5", f"SHIFT: {shift_name}", append=False)
        ws["AJ5"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # ---------------- CC_COL5_VALUE checkbox logic for AI9 ----------------
    default_options = ["Comp Air", "Vacuum", "Heating In Oven", "Comp Hot Air"]
    db_val = act.get("CC_COL5_VALUE", "")
    selected = [x.strip() for x in db_val.split(",") if x.strip()]
    display = "\n".join([f"✔ {opt}" if opt in selected else f"☐ {opt}" for opt in default_options])
    _safe_set(ws, "AI9", display, append=False)
    ws["AI9"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # ---------------- REMARKS formatting ----------------
    remarks_val = act.get("REMARKS", "")
    _safe_set(ws, "J47", f"REMARKS: {remarks_val}", append=False)
    ws["J47"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

    # ---------------- 🆕 Pressure test results (filtered by COUNT_ID) ----------------
    try:
        with connection.cursor() as cx:
            if count_id is not None:
                # Get ALL test results for this COUNT_ID
                if serial:
                    cx.execute("""
                        SELECT TEST_NAME, SET_PRESSURE, RESULT_PRESSURE, SET_TIME, VALVE_STATUS, PRESSURE_UNIT
                        FROM pressure_analysis
                        WHERE VALVE_SER_NO=%s AND COUNT_ID=%s AND TEST_NAME<>'' 
                        ORDER BY ID DESC
                    """, [serial, count_id])
                else:
                    cx.execute("""
                        SELECT TEST_NAME, SET_PRESSURE, RESULT_PRESSURE, SET_TIME, VALVE_STATUS, PRESSURE_UNIT
                        FROM pressure_analysis
                        WHERE STATION_STATUS=%s AND COUNT_ID=%s AND TEST_NAME<>'' 
                        ORDER BY ID DESC
                    """, [station_id, count_id])
                print(f"🔍 Fetching test results for COUNT_ID={count_id}")
            else:
                # Fallback: get latest test results
                if serial:
                    cx.execute("""
                        SELECT TEST_NAME, SET_PRESSURE, RESULT_PRESSURE, SET_TIME, VALVE_STATUS, PRESSURE_UNIT
                        FROM pressure_analysis
                        WHERE VALVE_SER_NO=%s AND TEST_NAME<>'' 
                        ORDER BY ID DESC LIMIT 200
                    """, [serial])
                else:
                    cx.execute("""
                        SELECT TEST_NAME, SET_PRESSURE, RESULT_PRESSURE, SET_TIME, VALVE_STATUS, PRESSURE_UNIT
                        FROM pressure_analysis
                        WHERE STATION_STATUS=%s AND TEST_NAME<>'' 
                        ORDER BY ID DESC LIMIT 200
                    """, [station_id])
            
            test_rows = cx.fetchall() or []
            print(f"📋 Found {len(test_rows)} test result rows")

        # Helpers
        def norm(s): return (str(s) if s else '').strip().lower()
        def conv_pressure(val, unit):
            try:
                val = float(val)
                unit = str(unit).strip().lower()
                if unit == 'psi': return round(val, 2)
                if unit in ('bar', 'barg'): return round(val * 14.5, 2)
                return val
            except: return val
        def conv_time(sec):
            try: return round(float(sec) / 60, 2)
            except: return "N/A"

        # Known test names and mapping
        excel_map = {
            "primary shell": ('F13', 'F14', 'F15', 'N/A', 'N/A'),
            "secondary shell": ('J13', 'J14', 'J15', 'N/A', 'N/A'),
            "hydro seat a": ('V13', 'V14', 'V15', 'N/A', 'N/A'),
            "hydro seat b": ('Y13', 'Y14', 'Y15', 'N/A', 'N/A'),
            "air seat a": ('AC13', 'AC14', 'AC15', 'N/A', 'N/A'),
            "air seat b": ('AG13', 'AG14', 'AG15', 'N/A', 'N/A'),
            "back seat": ('M13', 'M14', 'M15', 'N/A', 'N/A'),
            "low pressure": ('AJ13', 'AJ14', 'AJ15', 'N/A', 'N/A')
        }

        inserted_tests = set()
        dynamic_row_start = 30
        dyn_index = 0

        for row in test_rows:
            test_name, set_press, result_press, set_time, valve_status, press_unit = row
            key = norm(test_name)
            if key in inserted_tests:
                continue
            inserted_tests.add(key)

            set_pressure = conv_pressure(set_press, press_unit)
            actual_pressure = conv_pressure(result_press, press_unit)
            actual_time_min = conv_time(set_time)
            valve_status_val = valve_status or "N/A"
            raw_time_sec = set_time

            if key in excel_map:
                press_set_col, press_actual_col, time_col, valve_col, raw_time_col = excel_map[key]
                _safe_set(ws, press_set_col, set_pressure)
                _safe_set(ws, press_actual_col, actual_pressure)
                _safe_set(ws, time_col, actual_time_min)
                _safe_set(ws, valve_col, valve_status_val)
                _safe_set(ws, raw_time_col, raw_time_sec)

        # Align cells
        align_center = Alignment(horizontal="center", vertical="center", wrapText=True)
        for cols in excel_map.values():
            for col in cols:
                if col != 'N/A':
                    ws[col].alignment = align_center
        for i in range(dynamic_row_start, dynamic_row_start + dyn_index):
            for col in ["A", "B", "C", "D", "E"]:
                ws[f"{col}{i}"].alignment = align_center

    except Exception as e:
        print("⚠️ Pressure Analysis Mapping Error:", e)

    # -----------------------------------------
    # PRESSURE GAUGE ANALYSIS
    # -----------------------------------------
    import re
    from datetime import datetime

    EMPTY = "N/A"

    fixed_map = {
        "hydro": [("D42", "G42"), ("D43", "G43")],
        "air":   [("D44", "G44"), ("D45", "G45")],
        "gas":   [("D46", "G46"), ("D47", "G47")],
    }

    instrument_map = {
        "torque wrench 1": ("J37", "U37"),
        "torque wrench 2": ("J38", "U38"),
        "torque wrench": ("J37", "U37"),
        "veriner caliper": ("J39", "U39"),
        "measuring tape": ("J39", "U39"),
        "lux meter": ("AE37", "AI37"),
        "stopwatch": ("AE38", "AI38"),
        "stop watch": ("AE38", "AI38"),
        "thermometer": ("AE39", "AI39"),
        "thermo meter": ("AE39", "AI39"),
        "air": ("D44", "G44"),
    }

    pg_rows = []
    with connection.cursor() as cpg:
        if serial:
            cpg.execute("""
                SELECT INSTRUMENT_TYPE, CAL_DUE_DATE, INSTRUMENT_SER_NO, `RANGE`
                FROM pressure_gauge_analysis
                WHERE VALVE_SER_NO=%s AND COUNT_ID=%s
                ORDER BY ID ASC
            """, [serial, count_id])
        else:
            cpg.execute("""
                SELECT INSTRUMENT_TYPE, CAL_DUE_DATE, INSTRUMENT_SER_NO, `RANGE`
                FROM pressure_gauge_analysis
                WHERE STATION_ID=%s
                ORDER BY ID ASC
            """, [station_id])
        pg_rows = cpg.fetchall() or []

    # Clear all cells
    for pairs in fixed_map.values():
        for serial_cell, due_cell in pairs:
            _safe_set(ws, serial_cell, EMPTY)
            _safe_set(ws, due_cell, EMPTY)

    for serial_cell, due_cell in instrument_map.values():
        _safe_set(ws, serial_cell, EMPTY)
        _safe_set(ws, due_cell, EMPTY)

    # Process PG rows
    inserted_serials = set()

    for row in pg_rows:
        if len(row) < 3:
            print(f"Skipping invalid row: {row}")
            continue

        row_extended = row + (None, None, None, None)
        itype, cal_due, serno, rng = row_extended[:4]

        if isinstance(itype, tuple):
            itype = itype[0]
        key = re.sub(r'\s+', ' ', str(itype or "").strip().lower())

        if serno and rng:
            serial_text = f"{serno}/{rng}"
        elif serno:
            serial_text = str(serno)
        elif rng:
            serial_text = str(rng)
        else:
            serial_text = EMPTY

        if serial_text != EMPTY and serial_text in inserted_serials:
            continue
        if serial_text != EMPTY:
            inserted_serials.add(serial_text)

        if cal_due:
            if isinstance(cal_due, datetime):
                due_text = cal_due.strftime("%d-%m-%Y")
            else:
                try:
                    cal_due_dt = datetime.strptime(str(cal_due), "%Y-%m-%d")
                    due_text = cal_due_dt.strftime("%d-%m-%Y")
                except ValueError:
                    due_text = str(cal_due)
        else:
            due_text = EMPTY

        if key in fixed_map:
            for serial_cell, due_cell in fixed_map[key]:
                if ws[serial_cell].value == EMPTY:
                    _safe_set(ws, serial_cell, serial_text)
                    _safe_set(ws, due_cell, due_text)
                    break
            continue

        if key in instrument_map:
            serial_cell, due_cell = instrument_map[key]
            _safe_set(ws, serial_cell, serial_text)
            _safe_set(ws, due_cell, due_text)

    # Align cells
    align_center = Alignment(horizontal="center", vertical="center", wrapText=True)

    for pairs in fixed_map.values():
        for serial_cell, due_cell in pairs:
            ws[serial_cell].alignment = align_center
            ws[due_cell].alignment = align_center

    for serial_cell, due_cell in instrument_map.values():
        ws[serial_cell].alignment = align_center
        ws[due_cell].alignment = align_center

    # -----------------------------------------
    # ✅ PASS/FAIL EVALUATION SECTION
    # -----------------------------------------
    try:
        print(f"\n🔍 DEBUG INFO:")
        print(f"  - temp dict has {len(temp)} keys")
        print(f"  - pa dict has {len(pa)} keys")
        print(f"  - VALVETYPE_NAME in temp: {'VALVETYPE_NAME' in temp}")
        print(f"  - VALVETYPE_NAME in pa: {'VALVETYPE_NAME' in pa}")
        
        valve_type_raw = temp.get("VALVETYPE_NAME") or pa.get("VALVETYPE_NAME")
        valve_type = (valve_type_raw or "").strip().lower()
        
        print(f"  - Raw Valve Type: '{valve_type_raw}'")
        print(f"  - Processed Valve Type: '{valve_type}'")
        print(f"  - Available test rows: {len(test_rows)}")

        test_dict = { (r[0] or "").strip().lower(): r for r in test_rows }
        print(f"  - Test dictionary keys: {list(test_dict.keys())}")

        def get_result(test_name):
            row = test_dict.get(test_name.lower())
            if not row:
                return None
            result = (row[4] or "").strip().lower()
            print(f"    → {test_name}: {result}")
            return result

        def evaluate_tests(test_list, cell_ref):
            results = []
            print(f"\n📊 Evaluating {cell_ref} for tests: {test_list}")

            for t in test_list:
                r = get_result(t)
                if r is not None:
                    results.append(r)

            if not results:
                _safe_set(ws, cell_ref, "N/A")
                print(f"  ✅ {cell_ref} = N/A (no tests found)")
                return

            if any(r != "pass" for r in results):
                _safe_set(ws, cell_ref, "FAIL")
                print(f"  ❌ {cell_ref} = FAIL")
            else:
                _safe_set(ws, cell_ref, "PASS")
                print(f"  ✅ {cell_ref} = PASS")

        # 1. SHELL TEST → Z9 (all valves)
        evaluate_tests(["primary shell", "secondary shell", "shell"], "Z9")

        # 2. HYDRO SEAT TESTS
        if valve_type == "gate":
            evaluate_tests(["hydro seat a", "hydro seat b"], "AA11")
            print("  📍 Gate valve: Hydro PASS/FAIL → AA11")
        elif valve_type in ("globe", "check"):
            evaluate_tests(["hydro seat a", "hydro seat b"], "AB9")
            print("  📍 Globe/Check valve: Hydro PASS/FAIL → AB9")
        else:
            evaluate_tests(["hydro seat a", "hydro seat b"], "AB9")
            print(f"  📍 Unknown valve type '{valve_type}': Hydro PASS/FAIL → AB9 (default)")

        # 3. BACK SEAT → AC9
        evaluate_tests(["back seat"], "AC9")

        # 4. AIR SEAT TESTS
        if valve_type == "gate":
            evaluate_tests(["air seat a", "air seat b"], "AD11")
            print("  📍 Gate valve: Air PASS/FAIL → AD11")
        elif valve_type in ("globe", "check"):
            evaluate_tests(["air seat a", "air seat b"], "AE9")
            print("  📍 Globe/Check valve: Air PASS/FAIL → AE9")
        else:
            evaluate_tests(["air seat a", "air seat b"], "AE9")
            print(f"  📍 Unknown valve type '{valve_type}': Air PASS/FAIL → AE9 (default)")

    except Exception as e:
        print(f"⚠️ Error in test evaluation: {e}")
        import traceback
        traceback.print_exc()

    # ---------------- 🆕 Add COUNT_ID to report header ----------------
    if count_id is not None:
        _safe_set(ws, "A1", f"Count: {count_id}")
        ws["A1"].font = Font(size=10, bold=True)

    # ---------------- Current Date ----------------
    _safe_set(ws, "AH5", f"Date: {datetime.now().strftime('%d-%m-%Y')}", append=False)

    # ---------------- Formatting ----------------
    align_center = Alignment(horizontal="center", vertical="center", wrapText=True)
    for row in ws.iter_rows():
        for cell in row:
            if cell.value not in (None, ""):
                cell.alignment = align_center
    _apply_font_size(ws, size=10)

    # ---------------- Save to memory ----------------
    out = io.BytesIO()
    wb.save(out)
    out.seek(0)
    
    print(f"✅ Report generated successfully for COUNT_ID={count_id}")
    return out

def save_active_gcc_reports_to_disk(request):
    save_dir = r"D:\\Reports\\GGCreports"
    os.makedirs(save_dir, exist_ok=True)

    station_ids = []
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT ID FROM master_temp_data WHERE STATION_STATUS = 1
            ORDER BY ID
            """
        )
        station_ids += [r[0] for r in cursor.fetchall()]
        try:
            cursor.execute(
                """
                SELECT id FROM master_temp_data1 WHERE station_status = 'active'
                ORDER BY id
                """
            )
            station_ids += [r[0] for r in cursor.fetchall()]
        except Exception:
            pass

    station_ids = sorted(list({int(s) for s in station_ids}))
    if not station_ids:
        return HttpResponse("No active stations found", status=404)

    ok, fails = [], []
    for sid in station_ids:
        try:
            out = export_valve_report_from_master(sid)
            # Build filename using valve serial and date
            with connection.cursor() as c2:
                c2.execute("SELECT VALVE_SER_NO FROM master_temp_data WHERE ID=%s", [sid])
                r = c2.fetchone()
                serial = (r[0] if r and r[0] else f"Station_{sid}")
            
                c2.execute("SELECT COUNT_ID FROM pressure_analysis WHERE VALVE_SER_NO=%s order by id desc limit 1", [serial])
                count_row = c2.fetchone()
                count_no = count_row[0] if count_row else 1
            
            safe_serial = ''.join(ch if ch.isalnum() or ch in ('-', '_') else '_' for ch in str(serial))
            date_str = timezone.now().strftime('%Y%m%d')
            base_name = f"L&T_{safe_serial}_{date_str}_count{count_no}.xlsx"
            filepath = os.path.join(save_dir, base_name)
            # Try writing; if file is locked/denied, append _2, _3 ... up to _10
            written = False
            for idx in range(1, 11):
                try:
                    target = filepath if idx == 1 else os.path.join(save_dir, f"L&T_{safe_serial}_{date_str}_{idx}.xlsx")
                    with open(target, 'wb') as f:
                        f.write(out.getvalue())
                    ok.append(target)
                    written = True
                    break
                except PermissionError as pe:
                    last_err = pe
                    continue
            if not written:
                raise last_err if 'last_err' in locals() else PermissionError("Permission denied for all candidate filenames")
            
            # --- SAP UPLOAD: Excel Report ---
            try:
                fname = os.path.basename(target)
                sap_upload_doc(f'GGCreports/{fname}', serial_no=serial)
            except Exception as e:
                print(f"⚠️ SAP Excel Upload failed for {sid}: {e}")
        except Exception as e:
            fails.append((sid, str(e)))

    # Also generate merged PDFs per active station to D:\LNTReports\merged
    try:
        merged_paths = _generate_and_save_merged_pdf_to_disk()
        merged_msg = f" Merged PDFs saved to D:\\Reports\\merged ({len(merged_paths)} files)."
        
        # --- SAP UPLOAD: PDF Reports ---
        if isinstance(merged_paths, list):
            for p, ser_no in merged_paths:
                try:
                    fname = os.path.basename(p)
                    sap_upload_doc(f'merged/{fname}', serial_no=ser_no)
                except Exception as e:
                    print(f"⚠️ SAP PDF Upload failed for {p}: {e}")
    except Exception as e:
        merged_msg = f" Merged PDF save skipped: {e}"
    messages.success(request, f"GGC reports saved Successfully")
    if fails:
        # Show brief failure details (up to 5) with station id and error
        brief = []
        for sid, err in fails[:5]:
            try:
                with connection.cursor() as c2:
                    c2.execute("SELECT VALVE_SER_NO FROM master_temp_data WHERE ID=%s", [sid])
                    r = c2.fetchone()
                serial = (r[0] if r and r[0] else f"Station_{sid}")
            except Exception:
                serial = f"Station_{sid}"
            brief.append(f"{serial} (ID {sid}): {err}")
        more = f" and {len(fails)-5} more..." if len(fails) > 5 else ""
        messages.error(request, "GCC failed stations: " + "; ".join(brief) + more)
    # After saving FBV reports, update active stations to completed
    # ✅ Update pressure_analysis STATUS based on VALVE_SER_NO of active stations,
# and then reset master_temp_data + truncate current_status_station tables

    try:
        with transaction.atomic():
            with connection.cursor() as cur:

                # Step 1️⃣: Fetch all active valve serials
                cur.execute("""
                    SELECT VALVE_SER_NO
                    FROM master_temp_data
                    WHERE STATION_STATUS = 1 AND VALVE_SER_NO IS NOT NULL
                """)
                serials = [r[0] for r in cur.fetchall()]

                # Step 2️⃣: Update pressure_analysis for each serial
                for serial in serials:
                    cur.execute("""
                        UPDATE pressure_analysis
                        SET STATUS = 0
                        WHERE VALVE_SER_NO = %s
                    """, [serial])
                    
                    
                    cur.execute("SELECT COUNT(*) FROM serial_tbl WHERE Serial_No = %s", [serial])
                    exists = cur.fetchone()[0]

                    if exists:
                        # 3️⃣ Update existing row
                        cur.execute("""
                            UPDATE serial_tbl
                            SET Count_No = Count_No + 1
                            WHERE Serial_No = %s
                        """, [serial])
                    else:
                        # 4️⃣ Insert new row
                        cur.execute("""
                            INSERT INTO serial_tbl (Serial_No, Count_No)
                            VALUES (%s, %s)
                        """, [serial, 1])
                        
                    cur.execute("update pressure_analysis set STATUS=%s",[0])
                        
                cur.execute("""
                    UPDATE master_temp_data
                    SET STATION_STATUS = %s,
                        CYCLE_COMPLETE = %s
                    WHERE STATION_STATUS = %s
                """, [0, 0, 1])
            
                

                # Step 4️⃣: Truncate all current_status_station tables
                for i in [1,2,3,4]:
                    cur.execute(f"TRUNCATE TABLE current_status_station{i}")
                    cur.execute(f"TRUNCATE TABLE temp_pressure_analysis")
                
                cur.execute("TRUNCATE TABLE temp_testing_data")

        print("✅ Station data and pressure_analysis successfully reset.")

    except DatabaseError as e:
        # Rollback happens automatically under transaction.atomic()
        print("❌ Database error while resetting stations:", str(e))
        messages.error(request, f"Database error while resetting stations: {str(e)}")

    except Exception as e:
        print("❌ Unexpected error while updating database:", str(e))
        messages.error(request, f"Unexpected error while updating database: {str(e)}")

    
    return redirect('dashboard')


# @login_required
# def save_active_fbv_reports_to_disk(request):
#     save_dir = r"D:\\LNT_Reports\\FBVReports"
#     os.makedirs(save_dir, exist_ok=True)

#     station_ids = []
#     with connection.cursor() as cursor:
#         cursor.execute(
#             """
#             SELECT ID FROM master_temp_data WHERE STATION_STATUS = 1
#             ORDER BY ID
#             """
#         )
#         station_ids += [r[0] for r in cursor.fetchall()]
#         try:
#             cursor.execute(
#                 """
#                 SELECT id FROM master_temp_data1 WHERE station_status = 'active'
#                 ORDER BY id
#                 """
#             )
#             station_ids += [r[0] for r in cursor.fetchall()]
#         except Exception:
#             pass

#     station_ids = sorted(list({int(s) for s in station_ids}))
#     if not station_ids:
#         return HttpResponse("No active stations found", status=404)

#     ok, fails = [], []
#     for sid in station_ids:
#         try:
#             out = export_fbv_report_from_master(sid)
#             # Build filename using valve serial and date
#             with connection.cursor() as c2:
#                 c2.execute("SELECT VALVE_SER_NO FROM master_temp_data WHERE ID=%s", [sid])
#                 r = c2.fetchone()
#             serial = (r[0] if r and r[0] else f"Station_{sid}")
#             safe_serial = ''.join(ch if ch.isalnum() or ch in ('-', '_') else '_' for ch in str(serial))
#             date_str = timezone.now().strftime('%Y%m%d')
#             base_name = f"L&T_{safe_serial}_{date_str}.xlsx"
#             filepath = os.path.join(save_dir, base_name)
#             # Try writing; if file is locked/denied, append _2, _3 ... up to _10
#             written = False
#             for idx in range(1, 11):
#                 try:
#                     target = filepath if idx == 1 else os.path.join(save_dir, f"L&T_{safe_serial}_{date_str}_{idx}.xlsx")
#                     with open(target, 'wb') as f:
#                         f.write(out.getvalue())
#                     ok.append(target)
#                     written = True
#                     break
#                 except PermissionError as pe:
#                     last_err = pe
#                     continue
#             if not written:
#                 raise last_err if 'last_err' in locals() else PermissionError("Permission denied for all candidate filenames")
#         except Exception as e:
#             fails.append((sid, str(e)))

#     # Also generate merged PDFs per active station to D:\LNTReports\merged
#     try:
#         merged_paths = _generate_and_save_merged_pdf_to_disk()
#         merged_msg = f" Merged PDFs saved to D:\\LNTReports\\merged ({len(merged_paths)} files)."
#     except Exception as e:
#         merged_msg = f" Merged PDF save skipped: {e}"
#     messages.success(request, f"FBV reports saved Successfully")
#     if fails:
#         # Show brief failure details (up to 5) with station id and error
#         brief = []
#         for sid, err in fails[:5]:
#             try:
#                 with connection.cursor() as c2:
#                     c2.execute("SELECT VALVE_SER_NO FROM master_temp_data WHERE ID=%s", [sid])
#                     r = c2.fetchone()
#                 serial = (r[0] if r and r[0] else f"Station_{sid}")
#             except Exception:
#                 serial = f"Station_{sid}"
#             brief.append(f"{serial} (ID {sid}): {err}")
#         more = f" and {len(fails)-5} more..." if len(fails) > 5 else ""
#         messages.error(request, "FBV failed stations: " + "; ".join(brief) + more)
#     # After saving FBV reports, update active stations to completed
#     try:
#         with transaction.atomic():
#             with connection.cursor() as cur:

#                 # Step 1️⃣: Fetch all active valve serials
#                 cur.execute("""
#                     SELECT VALVE_SER_NO
#                     FROM master_temp_data
#                     WHERE STATION_STATUS = 1 AND VALVE_SER_NO IS NOT NULL
#                 """)
#                 serials = [r[0] for r in cur.fetchall()]

#                 # Step 2️⃣: Update pressure_analysis for each serial
#                 for serial in serials:
#                     cur.execute("""
#                         UPDATE pressure_analysis
#                         SET STATUS = 0
#                         WHERE VALVE_SER_NO = %s
#                     """, [serial])
                    
                    
#                     cur.execute("SELECT COUNT(*) FROM serial_tbl WHERE Serial_No = %s", [serial])
#                     exists = cur.fetchone()[0]

#                     if exists:
#                         # 3️⃣ Update existing row
#                         cur.execute("""
#                             UPDATE serial_tbl
#                             SET Count_No = Count_No + 1
#                             WHERE Serial_No = %s
#                         """, [serial])
#                     else:
#                         # 4️⃣ Insert new row
#                         cur.execute("""
#                             INSERT INTO serial_tbl (Serial_No, Count_No)
#                             VALUES (%s, %s)
#                         """, [serial, 1])
                        
#                     cur.execute("update pressure_analysis set STATUS=%s",[0])
                        
#                 cur.execute("""
#                     UPDATE master_temp_data
#                     SET STATION_STATUS = %s,
#                         CYCLE_COMPLETE = %s
#                     WHERE STATION_STATUS = %s
#                 """, [0, 0, 1])
            
                

#                 # Step 4️⃣: Truncate all current_status_station tables
#                 for i in [1,2,3,4]:
#                     cur.execute(f"TRUNCATE TABLE current_status_station{i}")
#                     cur.execute(f"TRUNCATE TABLE temp_pressure_analysis")

#         print("✅ Station data and pressure_analysis successfully reset.")

#     except DatabaseError as e:
#         # Rollback happens automatically under transaction.atomic()
#         print("❌ Database error while resetting stations:", str(e))
#         messages.error(request, f"Database error while resetting stations: {str(e)}")

#     except Exception as e:
#         print("❌ Unexpected error while updating database:", str(e))
#         messages.error(request, f"Unexpected error while updating database: {str(e)}")
        
#     return redirect('dashboard')


# @login_required
# def save_active_tmbv_reports_to_disk(request):
#     save_dir = r"D:\\LNT_Reports\\TMBVReports"
#     os.makedirs(save_dir, exist_ok=True)

#     station_ids = []
#     with connection.cursor() as cursor:
#         cursor.execute(
#             """
#             SELECT ID FROM master_temp_data WHERE STATION_STATUS = 1
#             ORDER BY ID
#             """
#         )
#         station_ids += [r[0] for r in cursor.fetchall()]
#         try:
#             cursor.execute(
#                 """
#                 SELECT id FROM master_temp_data1 WHERE station_status = 'active'
#                 ORDER BY id
#                 """
#             )
#             station_ids += [r[0] for r in cursor.fetchall()]
#         except Exception:
#             pass

#     station_ids = sorted(list({int(s) for s in station_ids}))
#     if not station_ids:
#         return HttpResponse("No active stations found", status=404)

#     ok, fails = [], []
#     for sid in station_ids:
#         try:
#             out = export_tmbv_report_from_master(None, sid)
#             # Build filename using valve serial and date
#             with connection.cursor() as c2:
#                 c2.execute("SELECT VALVE_SER_NO FROM master_temp_data WHERE ID=%s", [sid])
#                 r = c2.fetchone()
#             serial = (r[0] if r and r[0] else f"Station_{sid}")
#             safe_serial = ''.join(ch if ch.isalnum() or ch in ('-', '_') else '_' for ch in str(serial))
#             date_str = timezone.now().strftime('%Y%m%d')
#             base_name = f"L&T_{safe_serial}_{date_str}.xlsx"
#             filepath = os.path.join(save_dir, base_name)
#             written = False
#             for idx in range(1, 11):
#                 try:
#                     target = filepath if idx == 1 else os.path.join(save_dir, f"L&T_{safe_serial}_{date_str}_{idx}.xlsx")
#                     with open(target, 'wb') as f:
#                         f.write(out.getvalue())
#                     ok.append(target)
#                     written = True
#                     break
#                 except PermissionError as pe:
#                     last_err = pe
#                     continue
#             if not written:
#                 raise last_err if 'last_err' in locals() else PermissionError("Permission denied for all candidate filenames")
#         except Exception as e:
#             fails.append((sid, str(e)))

#     # Also generate merged PDFs per active station to D:\LNTReports\merged
#     try:
#         _generate_and_save_merged_pdf_to_disk()
#         merged_msg = " Merged PDFs saved to D:\\LNTReports\\merged."
#     except Exception as e:
#         merged_msg = f" Merged PDF save skipped: {e}"
#     messages.success(request, f"TMBV reports saved Successfully")
#     if fails:
#         brief = []
#         for sid, err in fails[:5]:
#             try:
#                 with connection.cursor() as c2:
#                     c2.execute("SELECT VALVE_SER_NO FROM master_temp_data WHERE ID=%s", [sid])
#                     r = c2.fetchone()
#                 serial = (r[0] if r and r[0] else f"Station_{sid}")
#             except Exception:
#                 serial = f"Station_{sid}"
#             brief.append(f"{serial} (ID {sid}): {err}")
#         more = f" and {len(fails)-5} more..." if len(fails) > 5 else ""
#         messages.error(request, "TMBV failed stations: " + "; ".join(brief) + more)
#     # After saving TMBV reports, update active stations to completed
#     try:
#         with transaction.atomic():
#             with connection.cursor() as cur:

#                 # Step 1️⃣: Fetch all active valve serials
#                 cur.execute("""
#                     SELECT VALVE_SER_NO
#                     FROM master_temp_data
#                     WHERE STATION_STATUS = 1 AND VALVE_SER_NO IS NOT NULL
#                 """)
#                 serials = [r[0] for r in cur.fetchall()]

#                 # Step 2️⃣: Update pressure_analysis for each serial
#                 for serial in serials:
#                     cur.execute("""
#                         UPDATE pressure_analysis
#                         SET STATUS = 0
#                         WHERE VALVE_SER_NO = %s
#                     """, [serial])
                 

#                     cur.execute("SELECT COUNT(*) FROM serial_tbl WHERE Serial_No = %s", [serial])
#                     exists = cur.fetchone()[0]

#                     if exists:
#                         # 3️⃣ Update existing row
#                         cur.execute("""
#                             UPDATE serial_tbl
#                             SET Count_No = Count_No + 1
#                             WHERE Serial_No = %s
#                         """, [serial])
#                     else:
#                         # 4️⃣ Insert new row
#                         cur.execute("""
#                             INSERT INTO serial_tbl (Serial_No, Count_No)
#                             VALUES (%s, %s)
#                         """, [serial, 1])
                        
#                     cur.execute("update pressure_analysis set STATUS=%s",[0])
#                     # Step 3️⃣: Reset master_temp_data stations
#                 cur.execute("""
#                     UPDATE master_temp_data
#                     SET STATION_STATUS = %s,
#                         CYCLE_COMPLETE = %s
#                     WHERE STATION_STATUS = %s
#                 """, [0, 0, 1])
                    
#                 # cur.execute("insert into serial_tbl (Serial_No,Count_No) values (%s,%s)", [serial,1])

#                 # Step 4️⃣: Truncate all current_status_station tables
#                 for i in [1, 2, 3, 4]:
#                     cur.execute(f"TRUNCATE TABLE current_status_station{i}")
#                     cur.execute(f"TRUNCATE TABLE temp_pressure_analysis")

#         print("✅ Station data and pressure_analysis successfully reset.")

#     except DatabaseError as e:
#         # Rollback happens automatically under transaction.atomic()
#         print("❌ Database error while resetting stations:", str(e))
#         messages.error(request, f"Database error while resetting stations: {str(e)}")

#     except Exception as e:
#         print("❌ Unexpected error while updating database:", str(e))
#         messages.error(request, f"Unexpected error while updating database: {str(e)}")
    
#     return redirect('dashboard')


@login_required
def save_active_fbv_reports_to_disk_from_pressure_analysis(request):
    """Save FBV reports to disk based on serial numbers from pressure_analysis table"""
    save_dir = r"E:\LNT_Reports\FBVReports"
    os.makedirs(save_dir, exist_ok=True)

    # Get distinct serial numbers from pressure_analysis where STATION_STATUS = '1' or 'active'
    serial_numbers = []
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT DISTINCT VALVE_SER_NO 
            FROM pressure_analysis 
            WHERE (STATION_STATUS = '1' OR STATION_STATUS = 'active' OR STATION_STATUS = 1)
            AND VALVE_SER_NO IS NOT NULL 
            AND VALVE_SER_NO != ''
            ORDER BY VALVE_SER_NO
            """
        )
        serial_numbers = [r[0] for r in cursor.fetchall()]

    if not serial_numbers:
        return HttpResponse("No active serial numbers found in pressure_analysis", status=404)

    ok, fails = [], []
    for serial in serial_numbers:
        try:
            # Determine valve type from pressure_analysis
            valve_type = None
            station_id = None
            
            with connection.cursor() as c_type:
                c_type.execute("""
                    SELECT VALVETYPE_NAME 
                    FROM pressure_analysis 
                    WHERE VALVE_SER_NO = %s 
                    ORDER BY ID DESC LIMIT 1
                """, [serial])
                type_row = c_type.fetchone()
                if type_row and type_row[0]:
                    valve_type = str(type_row[0]).lower()
                
                # Try to get station_id from master_temp_data1 as fallback
                try:
                    c_type.execute("""
                        SELECT id FROM master_temp_data1 
                        WHERE valve_serial_no = %s 
                        ORDER BY id DESC LIMIT 1
                    """, [serial])
                    sid_row = c_type.fetchone()
                    if sid_row:
                        station_id = sid_row[0]
                except Exception:
                    pass

            # Check if it's FBV (Floating Ball Valve)
            if valve_type and ('float' in valve_type or 'floating' in valve_type or 'fbv' in valve_type):
                # Pass serial directly to export function, station_id is optional
                out = export_fbv_report_from_master(station_id if station_id else None, serial)
                
                safe_serial = ''.join(ch if ch.isalnum() or ch in ('-', '_') else '_' for ch in str(serial))
                date_str = timezone.now().strftime('%Y%m%d')
                base_name = f"L&T_{safe_serial}_{date_str}.xlsx"
                filepath = os.path.join(save_dir, base_name)
                
                # Try writing; if file is locked/denied, append _2, _3 ... up to _10
                written = False
                for idx in range(1, 11):
                    try:
                        target = filepath if idx == 1 else os.path.join(save_dir, f"L&T_{safe_serial}_{date_str}_{idx}.xlsx")
                        with open(target, 'wb') as f:
                            f.write(out.getvalue())
                        ok.append(target)
                        written = True
                        break
                    except PermissionError as pe:
                        last_err = pe
                        continue
                if not written:
                    raise last_err if 'last_err' in locals() else PermissionError("Permission denied for all candidate filenames")
        except Exception as e:
            fails.append((serial, str(e)))

    # Also generate merged PDFs per active station to D:\LNTReports\merged
    try:
        merged_paths = _generate_and_save_merged_pdf_to_disk()
        merged_msg = f" Merged PDFs saved to D:\\Reports\\merged ({len(merged_paths)} files)."
    except Exception as e:
        merged_msg = f" Merged PDF save skipped: {e}"
    
    messages.success(request, f"FBV reports saved Successfully from pressure_analysis")
    if fails:
        # Show brief failure details (up to 5) with serial number and error
        brief = []
        for serial, err in fails[:5]:
            brief.append(f"{serial}: {err}")
        more = f" and {len(fails)-5} more..." if len(fails) > 5 else ""
        messages.error(request, "FBV failed serials: " + "; ".join(brief) + more)
    
    return redirect('dashboard')


@login_required
def save_active_tmbv_reports_to_disk_from_pressure_analysis(request):
    """Save TMBV reports to disk based on serial numbers from pressure_analysis table"""
    save_dir = r"E:\\LNT_Reports\\TMBVReports"
    os.makedirs(save_dir, exist_ok=True)

    # Get distinct serial numbers from pressure_analysis where STATION_STATUS = '1' or 'active'
    serial_numbers = []
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT DISTINCT VALVE_SER_NO 
            FROM pressure_analysis 
            WHERE (STATION_STATUS = '1' OR STATION_STATUS = 'active' OR STATION_STATUS = 1)
            AND VALVE_SER_NO IS NOT NULL 
            AND VALVE_SER_NO != ''
            ORDER BY VALVE_SER_NO
            """
        )
        serial_numbers = [r[0] for r in cursor.fetchall()]

    if not serial_numbers:
        return HttpResponse("No active serial numbers found in pressure_analysis", status=404)

    ok, fails = [], []
    for serial in serial_numbers:
        try:
            # Determine valve type from pressure_analysis
            valve_type = None
            station_id = None
            
            with connection.cursor() as c_type:
                c_type.execute("""
                    SELECT VALVETYPE_NAME 
                    FROM pressure_analysis 
                    WHERE VALVE_SER_NO = %s 
                    ORDER BY ID DESC LIMIT 1
                """, [serial])
                type_row = c_type.fetchone()
                if type_row and type_row[0]:
                    valve_type = str(type_row[0]).lower()
                
                # Try to get station_id from master_temp_data1 as fallback
                try:
                    c_type.execute("""
                        SELECT id FROM master_temp_data1 
                        WHERE valve_serial_no = %s 
                        ORDER BY id DESC LIMIT 1
                    """, [serial])
                    sid_row = c_type.fetchone()
                    if sid_row:
                        station_id = sid_row[0]
                except Exception:
                    pass

            # Check if it's TMBV (Trunnion Mounted Ball Valve)
            if valve_type and ('trunnion' in valve_type or 'tmbv' in valve_type):
                # export_tmbv_report_from_master accepts serial and station_id
                out = export_tmbv_report_from_master(serial, station_id)
                
                safe_serial = ''.join(ch if ch.isalnum() or ch in ('-', '_') else '_' for ch in str(serial))
                date_str = timezone.now().strftime('%Y%m%d')
                base_name = f"L&T_{safe_serial}_{date_str}.xlsx"
                filepath = os.path.join(save_dir, base_name)
                
                written = False
                for idx in range(1, 11):
                    try:
                        target = filepath if idx == 1 else os.path.join(save_dir, f"L&T_{safe_serial}_{date_str}_{idx}.xlsx")
                        with open(target, 'wb') as f:
                            f.write(out.getvalue())
                        ok.append(target)
                        written = True
                        break
                    except PermissionError as pe:
                        last_err = pe
                        continue
                if not written:
                    raise last_err if 'last_err' in locals() else PermissionError("Permission denied for all candidate filenames")
        except Exception as e:
            fails.append((serial, str(e)))

    # Also generate merged PDFs per active station to D:\LNTReports\merged
    try:
        _generate_and_save_merged_pdf_to_disk()
        merged_msg = " Merged PDFs saved to D:\\Reports\\merged."
    except Exception as e:
        merged_msg = f" Merged PDF save skipped: {e}"
    
    messages.success(request, f"TMBV reports saved Successfully from pressure_analysis")
    if fails:
        brief = []
        for serial, err in fails[:5]:
            brief.append(f"{serial}: {err}")
        more = f" and {len(fails)-5} more..." if len(fails) > 5 else ""
        messages.error(request, "TMBV failed serials: " + "; ".join(brief) + more)
    
    return redirect('dashboard')


@login_required
def download_fbv_report_from_pressure_analysis(request):
    """Save single FBV report based on serial number from pressure_analysis to D:\FBVReports"""
    serial = request.GET.get('serial', '').strip()
    if not serial:
        messages.error(request, "Serial number is required")
        return redirect('dashboard')
    
    try:
        # Get station_id if available (optional)
        station_id = None
        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                    SELECT id FROM master_temp_data1 
                    WHERE valve_serial_no = %s 
                    ORDER BY id DESC LIMIT 1
                """, [serial])
                sid_row = cursor.fetchone()
                if sid_row:
                    station_id = sid_row[0]
            except Exception:
                pass
        
        # Generate report using serial from pressure_analysis
        out = export_fbv_report_from_master(station_id if station_id else None, serial)
        
        # Save to D:\FBVReports
        save_dir = r'D:\\LNT_Reports\\FBVReports'
        os.makedirs(save_dir, exist_ok=True)
        
        safe_serial = ''.join(ch if ch.isalnum() or ch in ('-', '_') else '_' for ch in str(serial))
        date_str = timezone.now().strftime('%Y%m%d')
        base_name = f"L&T_{safe_serial}_{date_str}.xlsx"
        filepath = os.path.join(save_dir, base_name)
        
        # Try to save file, if file exists, append number
        written = False
        last_err = None
        for idx in range(1, 11):
            try:
                target = filepath if idx == 1 else os.path.join(save_dir, f"L&T_{safe_serial}_{date_str}_{idx}.xlsx")
                with open(target, 'wb') as f:
                    f.write(out.getvalue())
                written = True
                messages.success(request, f"FBV report saved successfully")
                break
            except PermissionError as pe:
                last_err = pe
                continue
            except Exception as e:
                last_err = e
                continue
        
        if not written:
            error_msg = str(last_err) if last_err else "Unknown error occurred"
            messages.error(request, f"Error saving FBV report: {error_msg}")
    except Exception as e:
        messages.error(request, f"Error generating FBV report: {str(e)}")
    
    return redirect('dashboard')


@login_required
def download_tmbv_report_from_pressure_analysis(request):
    """Save single TMBV report based on serial number from pressure_analysis to D:\TMBVReports"""
    serial = request.GET.get('serial', '').strip()
    if not serial:
        messages.error(request, "Serial number is required")
        return redirect('dashboard')
    
    try:
        # Get station_id if available (optional)
        station_id = None
        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                    SELECT id FROM master_temp_data1 
                    WHERE valve_serial_no = %s 
                    ORDER BY id DESC LIMIT 1
                """, [serial])
                sid_row = cursor.fetchone()
                if sid_row:
                    station_id = sid_row[0]
            except Exception:
                pass
        
        # Generate report using serial from pressure_analysis
        out = export_tmbv_report_from_master(serial, station_id)
        
        # Save to D:\TMBVReports
        save_dir = r'D:\\LNT_Reports\\TMBVReports'
        os.makedirs(save_dir, exist_ok=True)
        
        safe_serial = ''.join(ch if ch.isalnum() or ch in ('-', '_') else '_' for ch in str(serial))
        date_str = timezone.now().strftime('%Y%m%d')
        base_name = f"L&T_{safe_serial}_{date_str}.xlsx"
        filepath = os.path.join(save_dir, base_name)
        
        # Try to save file, if file exists, append number
        written = False
        last_err = None
        for idx in range(1, 11):
            try:
                target = filepath if idx == 1 else os.path.join(save_dir, f"L&T_{safe_serial}_{date_str}_{idx}.xlsx")
                with open(target, 'wb') as f:
                    f.write(out.getvalue())
                written = True
                messages.success(request, f"TMBV report saved successfully")
                break
            except PermissionError as pe:
                last_err = pe
                continue
            except Exception as e:
                last_err = e
                continue
        
        if not written:
            error_msg = str(last_err) if last_err else "Unknown error occurred"
            messages.error(request, f"Error saving TMBV report: {error_msg}")
    except Exception as e:
        messages.error(request, f"Error generating TMBV report: {str(e)}")
    
    return redirect('dashboard')

def _safe_set(ws, cell, value):
    """Safely set a cell’s value and center-align it."""
    try:
        if value not in (None, ""):
            ws[cell] = value
            ws[cell].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    except Exception:
        pass


def _apply_font_size(ws, size=12):
    """Uniform font and center alignment across used range."""
    try:
        for row in ws.iter_rows():
            for cell in row:
                if cell.value not in (None, ""):
                    cell.font = Font(size=size)
                    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    except Exception:
        pass


def export_tmbv_report_from_master(valve_serial_number, station_id):
    # Load template
    template_path = os.path.join(settings.BASE_DIR, "static", "templates", "tmbv report format.xlsx")
    if not os.path.exists(template_path):
        wb = load_workbook(io.BytesIO())  # fallback will fail; template must exist
    wb = load_workbook(template_path)
    ws = wb.active
    ws.title = "Raw Query Export"

    # Fetch full master_temp_data row (primary source for header/basic cells)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM master_temp_data WHERE ID=%s", [station_id])
        temp_row = cursor.fetchone()
        temp_cols = [d[0] for d in cursor.description] if cursor.description else []
    temp = {str(temp_cols[i]).lower(): temp_row[i] for i in range(len(temp_cols))} if temp_row else {}

    # Helper to pick first non-empty among candidates from temp
    def _tget(*cands):
        for c in cands:
            v = temp.get(c.lower())
            if v not in (None, ""):
                return v
        return None

    # Write header/basic cells from master_temp_data if available
    _safe_set(ws, "K4", _tget("valve_size", "size", "size_name", "size_id"))
    _safe_set(ws, "K5", _tget("valve_class", "class", "class_name", "class_id"))
    _safe_set(ws, "K8", _tget("shell_material", "shell_material_name", "shell_material_id"))
    _safe_set(ws, "E4", _tget("sales_order_no", "salesorder_no", "so_no"))
    _safe_set(ws, "E5", _tget("sales_item_no", "salesitem_no", "so_item_no"))
    _safe_set(ws, "E6", _tget("gad_no", "gadnumber", "gad"))
    _safe_set(ws, "K6", _tget("valve_serial_number", "valve_ser_no", "serial_no"))
    _safe_set(ws, "L19", _tget("tested_by", "testedby"))
    _safe_set(ws, "O19", _tget("approved_by", "approvedby"))
    _safe_set(ws, "K11", _tget("gear_actuator", "gear_actuator_name", "gearactuator"))
    _safe_set(ws, "K9", _tget("ma_gear_ratio", "gear_ratio", "ma_gearratio"))
    _safe_set(ws, "K7", _tget("ga_drg_no", "ga_drawing_no", "ga_drg"))
    _safe_set(ws, "A9", _tget("body_heat"))
    _safe_set(ws, "A9", _tget("body_mp"))
    _safe_set(ws, "A9", _tget("body_rt"))
    # Connector right/left (concatenate heat/mp/rt)
    r_text = " / ".join([str(x) for x in [
        _tget("connector_r_heat", "connector_heat"),
        _tget("connector_r_mp", "connector_mp"),
        _tget("connector_r_rt", "connector_rt")
    ] if x not in (None, "")])
    l_text = " / ".join([str(x) for x in [
        _tget("connector_l_heat"),
        _tget("connector_l_mp"),
        _tget("connector_l_rt")
    ] if x not in (None, "")])
    if r_text:
        _safe_set(ws, "E9", r_text)
    if l_text:
        _safe_set(ws, "G9", l_text)

    # Header fields from pressure_analysis (latest by id)
    valve_serial_for_query = _tget("valve_serial_number", "valve_ser_no", "serial_no") or valve_serial_number
    pa = None
    try:
        with connection.cursor() as cursor:
            # Try detailed connector L/R columns first
            try:
                cursor.execute(
                    """
                    SELECT valve_size, valve_class, shell_material,
                           sales_order_no, sales_item_no, gad_no, valve_serial_number, valve_tag_no,
                           tested_by, approved_by,
                           gear_actuator, ma_gear_ratio, ga_drg_no,
                           body_heat, body_mp, body_rt,
                           connector_r_heat, connector_r_mp, connector_r_rt,
                           connector_l_heat, connector_l_mp, connector_l_rt
                    FROM pressure_analysis
                    WHERE valve_serial_number = %s AND station = %s
                    ORDER BY id DESC
                    LIMIT 1
                    """,
                    [valve_serial_for_query, station_id],
                )
                row = cursor.fetchone()
                if row is None:
                    # fallback: by serial only
                    cursor.execute(
                        """
                        SELECT valve_size, valve_class, shell_material,
                               sales_order_no, sales_item_no, gad_no, valve_serial_number, valve_tag_no,
                               tested_by, approved_by,
                               gear_actuator, ma_gear_ratio, ga_drg_no,
                               body_heat, body_mp, body_rt,
                               connector_r_heat, connector_r_mp, connector_r_rt,
                               connector_l_heat, connector_l_mp, connector_l_rt
                        FROM pressure_analysis
                        WHERE valve_serial_number = %s
                        ORDER BY id DESC
                        LIMIT 1
                        """,
                        [valve_serial_for_query],
                    )
                    row = cursor.fetchone()
                pa = (row, 'detailed')
            except Exception:
                cursor.execute(
                    """
                    SELECT valve_size, valve_class, shell_material,
                           sales_order_no, sales_item_no, gad_no, valve_serial_number, valve_tag_no,
                           tested_by, approved_by,
                           gear_actuator, ma_gear_ratio, ga_drg_no,
                           body_heat, body_mp, body_rt,
                           connector_heat, connector_mp, connector_rt
                    FROM pressure_analysis
                    WHERE valve_serial_number = %s AND station = %s
                    ORDER BY id DESC
                    LIMIT 1
                    """,
                    [valve_serial_for_query, station_id],
                )
                row = cursor.fetchone()
                if row is None:
                    # fallback: by serial only
                    cursor.execute(
                        """
                        SELECT valve_size, valve_class, shell_material,
                               sales_order_no, sales_item_no, gad_no, valve_serial_number, valve_tag_no,
                               tested_by, approved_by,
                               gear_actuator, ma_gear_ratio, ga_drg_no,
                               body_heat, body_mp, body_rt,
                               connector_heat, connector_mp, connector_rt
                        FROM pressure_analysis
                        WHERE valve_serial_number = %s
                        ORDER BY id DESC
                        LIMIT 1
                        """,
                        [valve_serial_for_query],
                    )
                    row = cursor.fetchone()
                pa = (row, 'generic')
    except OperationalError:
        pa = None
    if pa and pa[0]:
        row, mode = pa
        # Common indices
        _safe_set(ws, "K4", row[0])   # valve_size
        _safe_set(ws, "K5", row[1])   # valve_class
        _safe_set(ws, "K8", row[2])   # shell_material
        _safe_set(ws, "E4", row[3])   # sales_order_no
        _safe_set(ws, "E5", row[4])   # sales_item_no
        _safe_set(ws, "E6", row[5])   # gad_no
        _safe_set(ws, "K6", row[6])   # valve_serial_number
        # valve_tag_no not requested in final map, keeping available if needed
        _safe_set(ws, "L19", row[8])  # tested_by
        _safe_set(ws, "O19", row[9])  # approved_by
        _safe_set(ws, "K11", row[10]) # gear_actuator
        _safe_set(ws, "K9", row[11])  # ma_gear_ratio
        _safe_set(ws, "K7", row[12])  # ga_drg_no
        _safe_set(ws, "A9", row[13])  # body_heat
        _safe_set(ws, "A9", row[14])  # body_mp
        _safe_set(ws, "A9", row[15])  # body_rt
        if mode == 'detailed':
            # Right connector -> E9, Left connector -> G9 (concatenate heat/mp/rt)
            r_vals = [row[16], row[17], row[18]]
            l_vals = [row[19], row[20], row[21]]
            r_text = " / ".join([str(v) for v in r_vals if v not in (None, "")])
            l_text = " / ".join([str(v) for v in l_vals if v not in (None, "")])
            _safe_set(ws, "E9", r_text)
            _safe_set(ws, "G9", l_text)
        else:
            # Fallback: write generic connector_* concatenated to E9 (right)
            r_vals = [row[16], row[17], row[18]]
            r_text = " / ".join([str(v) for v in r_vals if v not in (None, "")])
            _safe_set(ws, "E9", r_text)

    # Read pairs from master_actuator using latest by serial; fallback to station_id
    serial_candidates = []
    if temp_row:
        serial_candidates = [temp_row[1]]  # VALVE_SER_NO from SELECT
    # Add alternative keys from pressure_analysis if available
    try:
        if pa:
            # pa[6] mapped as valve_serial_number in pressure_analysis query
            pa_serial = pa[6]
            if pa_serial:
                serial_candidates.append(pa_serial)
    except Exception:
        pass
    serial = next((s for s in serial_candidates if s not in (None, "")), None)
    if serial:
        pairs = _read_master_actuator_pairs_by_serial(serial)
    else:
        pairs = _read_master_actuator_pairs_by_id(station_id)

    # Map label -> canonical key as used in build_pairs_from_post
    label_to_key = {
        "Valve Type Name": "valve_type_name",
        "Body to Ball: Measured Power (V)": "body_ball_power",
        "Body to Ball: Measured Resistance (Ω)": "body_ball_resistance",
        "Body to Stem/Shaft: Measured Power (V)": "body_stem_power",
        "Body to Stem/Shaft: Measured Resistance (Ω)": "body_stem_resistance",
        "Actuator Timing (s) Close→Open": "timing_close_open",
        "Actuator Timing (s) Open→Close": "timing_open_close",
        "Actuator Torque Setting (%) Close→Open": "torque_close_open",
        "Actuator Torque Setting (%) Open→Close": "torque_open_close",
        "Actuator Sizing Pressure (psig)": "sizing_pressure",
        "Run Torque @ Atmospheric (Nm)": "run_torque",
        "Tightness of Gear Unit Position Stopper": "gear_unit_stopper",
        "Torque @ Rated Pressure (Nm) BTO (DBB)": "bto_dbb",
        "Torque @ Rated Pressure (Nm) BTO (DBB) Result": "bto_dbb_result",
        "Torque @ Rated Pressure (Nm) BTO Connector (L)": "bto_connector_l",
        "Torque @ Rated Pressure (Nm) BTO Connector (L) Result": "bto_connector_l_result",
        "Torque @ Rated Pressure (Nm) BTO Connector (R)": "bto_connector_r",
        "Torque @ Rated Pressure (Nm) BTO Connector (R) Result": "bto_connector_r_result",
        "Torque @ Rated Pressure (Nm) BTC": "btc",
        "Torque @ Rated Pressure (Nm) BTC Result": "btc_result",
        "Water Drying Technique (QM-7B)": "technique_result",
        "Abnormal Sound During Operation": "check_sound",
        "Water Draining After Testing": "draining_test",
        "Remarks": "remarks",
    }

    # Build key->value dict
    kv = {}
    for label, val in pairs.items():
        key = label_to_key.get(label)
        if key:
            kv[key] = val

    # Place values into cells (TMBV mapping)
    form_field_map = {
        "body_ball_power": "B16",
        "body_ball_resistance": "C16",
        "body_stem_power": "B17",
        "body_stem_resistance": "C17",
        "timing_close_open": "E20",
        "timing_open_close": "F20",
        "torque_close_open": "A20",
        "torque_open_close": "C20",
        "sizing_pressure": "G20",
        "run_torque": "Q15",
        "gear_unit_stopper": "R19",
        "bto_dbb": "M15",
        "bto_dbb_result": "M16",
        "bto_connector_l": "N15",
        "bto_connector_l_result": "N16",
        "bto_connector_r": "O15",
        "bto_connector_r_result": "O16",
        "btc": "P15",
        "btc_result": "P16",
        "result_drying": "P26",
        "check_sound": "R26",
        "draining_test": "T26",
        "remarks": "A25",
    }
    for k, cell in form_field_map.items():
        if k in kv:
            _safe_set(ws, cell, kv[k])

    # Pressure Gauge Analysis for TMBV
    try:
        pg_rows = []
        with connection.cursor() as cpg:
            # Prefer by serial if available in temp
            vserial = _tget("valve_serial_number", "valve_ser_no", "serial_no") or valve_serial_number
            if vserial:
                cpg.execute(
                    """
                    SELECT INSTRUMENT_TYPE, CAL_DUE_DATE, INSTRUMENT_SER_NO, `RANGE`
                    FROM pressure_gauge_analysis
                    WHERE VALVE_SER_NO=%s
                    ORDER BY ID ASC
                    """,
                    [vserial],
                )
            else:
                cpg.execute(
                    """
                    SELECT INSTRUMENT_TYPE, CAL_DUE_DATE, INSTRUMENT_SER_NO, `RANGE`
                    FROM pressure_gauge_analysis
                    WHERE STATION_ID=%s
                    ORDER BY ID ASC
                    """,
                    [station_id],
                )
            pg_rows = cpg.fetchall() or []

        # Header details 1 & 2
        if len(pg_rows) >= 1:
            _safe_set(ws, "O7", pg_rows[0][0])   # INSTRUMENT_TYPE
            _safe_set(ws, "T7", pg_rows[0][1])   # CAL_DUE_DATE
        if len(pg_rows) >= 2:
            _safe_set(ws, "O10", pg_rows[1][0])  # INSTRUMENT_TYPE
            _safe_set(ws, "T10", pg_rows[1][1])  # CAL_DUE_DATE

        # Instruments 1..4 grid
        grid = [
            ("A23", "D23", "G23"),  # inst, range/serial, due
            ("A24", "D24", "G24"),
            ("K23", "O23", "R23"),
            ("K24", "O24", "R24"),
        ]
        for i in range(min(4, len(pg_rows))):
            itype, due, serno, rng = pg_rows[i]
            c_inst, c_combo, c_due = grid[i]
            if itype not in (None, ""):
                _safe_set(ws, c_inst, itype)
            combo = None
            if serno and rng:
                combo = f"{serno}/{rng}"
            elif serno:
                combo = str(serno)
            elif rng:
                combo = str(rng)
            if combo:
                _safe_set(ws, c_combo, combo)
            if due not in (None, ""):
                _safe_set(ws, c_due, due)
    except Exception:
        pass

    # Write current date and shift, regardless
    try:
        _safe_set(ws, "T4", timezone.now().strftime("%d-%m-%Y"))
    except Exception:
        pass
    try:
        _safe_set(ws, "T5", get_latest_shift_name())
    except Exception:
        pass

    # ===== Apply provided mappings to TMBV sheet =====
    try:
        # PRESSURE_ANALYSIS latest by serial or station
        p = {}
        with connection.cursor() as cpx:
            if valve_serial_for_query:
                cpx.execute(
                    """
                    SELECT COL1_VALUE, COL2_VALUE, COL8_VALUE,
                           COL13_VALUE, COL14_VALUE, COL15_VALUE,
                           COL19_VALUE, COL20_VALUE, COL21_VALUE,
                           COL22_VALUE, COL23_VALUE, COL24_VALUE,
                           VALVESIZE_NAME, VALVECLASS_NAME, VALVE_SER_NO,
                           COL5_VALUE, SHELLMATERIAL_NAME,
                           COL12_VALUE, COL7_VALUE, COL9_VALUE, COL10_VALUE, COL4_VALUE
                    FROM pressure_analysis
                    WHERE VALVE_SER_NO = %s
                    ORDER BY id DESC LIMIT 1
                    """,
                    [valve_serial_for_query],
                )
            else:
                cpx.execute(
                    """
                    SELECT COL1_VALUE, COL2_VALUE, COL8_VALUE,
                           COL13_VALUE, COL14_VALUE, COL15_VALUE,
                           COL19_VALUE, COL20_VALUE, COL21_VALUE,
                           COL22_VALUE, COL23_VALUE, COL24_VALUE,
                           VALVESIZE_NAME, VALVECLASS_NAME, VALVE_SER_NO,
                           COL5_VALUE, SHELLMATERIAL_NAME,
                           COL12_VALUE, COL7_VALUE, COL9_VALUE, COL10_VALUE, COL4_VALUE
                    FROM pressure_analysis
                    WHERE STATION_STATUS = %s
                    ORDER BY id DESC LIMIT 1
                    """,
                    [station_id],
                )
            row = cpx.fetchone()
            if row:
                (COL1, COL2, COL8,
                 COL13, COL14, COL15,
                 COL19, COL20, COL21,
                 COL22, COL23, COL24,
                 VSIZE, VCLASS, VSER,
                 COL5, SMAT,
                 COL12, COL7, COL9, COL10, COL4) = row
                # Map to cells per table image
                _safe_set(ws, "E4", COL1)
                _safe_set(ws, "E5", COL2)
                _safe_set(ws, "E6", COL8)
                _safe_set(ws, "A9", COL13)
                _safe_set(ws, "A9", COL14)  # Body Mp/Dp No
                _safe_set(ws, "A9", COL15)  # Body Rt No (same merged cell in template)
                _safe_set(ws, "E9", COL21)  # Connector R Rt NO
                _safe_set(ws, "G9", COL24)  # Connector L Rt NO
                _safe_set(ws, "K4", VSIZE)
                _safe_set(ws, "K5", VCLASS)
                _safe_set(ws, "K6", VSER)
                _safe_set(ws, "K7", COL5)  # End Detail
                _safe_set(ws, "K8", SMAT)
                _safe_set(ws, "K9", COL12) # Gear Unit detail
                _safe_set(ws, "K11", COL7)  # Actuator Detail
                # Tested By (COL10) and Witnessed By (COL9)
                _safe_set(ws, "L19", COL10)
                _safe_set(ws, "O19", COL9)
                # Stem Position U19/U20 (template may use two cells)
                _safe_set(ws, "U19", COL4)
                _safe_set(ws, "U20", COL4)
    except Exception:
        pass

    try:
        # MASTER_ACTUATOR latest by serial or station
        with connection.cursor() as cam:
            if valve_serial_for_query:
                cam.execute(
                    """
                    SELECT CC_COL2_VALUE, CC_COL3_VALUE, CC_COL4_VALUE, CC_COL5_VALUE,
                           CC_COL8_VALUE, CC_COL9_VALUE, CC_COL6_VALUE, CC_COL7_VALUE,
                           CC_COL18_VALUE, CC_COL13_VALUE, CC_COL15_VALUE, CC_COL2_VALUE,
                           CC_COL16_VALUE, CC_COL17_VALUE,
                           CC_COL19_VALUE, CC_COL21_VALUE, CC_COL23_VALUE, CC_COL25_VALUE,
                           CC_COL20_VALUE, CC_COL22_VALUE, CC_COL24_VALUE, CC_COL26_VALUE,
                           CC_COL12_VALUE, CC_COL27_VALUE
                    FROM master_actuator
                    WHERE VALVE_SER_NO = %s
                    ORDER BY ID DESC LIMIT 1
                    """,
                    [valve_serial_for_query],
                )
            else:
                cam.execute(
                    """
                    SELECT CC_COL2_VALUE, CC_COL3_VALUE, CC_COL4_VALUE, CC_COL5_VALUE,
                           CC_COL8_VALUE, CC_COL9_VALUE, CC_COL6_VALUE, CC_COL7_VALUE,
                           CC_COL18_VALUE, CC_COL13_VALUE, CC_COL15_VALUE, CC_COL2_VALUE,
                           CC_COL16_VALUE, CC_COL17_VALUE,
                           CC_COL19_VALUE, CC_COL21_VALUE, CC_COL23_VALUE, CC_COL25_VALUE,
                           CC_COL20_VALUE, CC_COL22_VALUE, CC_COL24_VALUE, CC_COL26_VALUE,
                           CC_COL12_VALUE, CC_COL27_VALUE
                    FROM master_actuator
                    WHERE VALVE_SER_NO = %s
                    ORDER BY id DESC LIMIT 1
                    """,
                    [valve_serial_for_query],
                )
            a = cam.fetchone()
            if a:
                (CC2, CC3, CC4, CC5,
                 CC8, CC9, CC6, CC7,
                 CC18, CC13, CC15, CC2,
                 CC16, CC17,
                 CC19, CC21, CC23, CC25,
                 CC20, CC22, CC24, CC26,
                 CC12, CC27) = a
                # Cells per table image
                _safe_set(ws, "B16", CC2)   # Body to Ball Measured Power
                _safe_set(ws, "C16", CC3)   # Body to Ball Measured Resistance
                _safe_set(ws, "B17", CC4)   # Body to Stem/Shaft Measured Power
                _safe_set(ws, "C17", CC5)   # Body to Stem/Shaft Measured Resistance
                _safe_set(ws, "A20", CC8)   # Torque % Close to Open
                _safe_set(ws, "C20", CC9)   # Torque % Open to Close
                _safe_set(ws, "E20", CC6)   # Timing sec Close to Open
                _safe_set(ws, "F20", CC7)   # Timing sec Open to Close
                _safe_set(ws, "G20", CC18)  # Actuator Sizing Pressure
                _safe_set(ws, "R19", CC13)  # Tightness of Gear Unit Position Stopper
               
                _safe_set(ws, "P26", CC2)   # Result of drying
                _safe_set(ws, "R26", CC16)  # Check abnormal sound
                _safe_set(ws, "T26", CC17)  # Water draining after testing
                _safe_set(ws, "M15", CC19)  # Torque Nm @ Rated Pressure BTO (DBB)
                _safe_set(ws, "N15", CC21)  # Torque Nm ... (body/Connector L)
                _safe_set(ws, "O15", CC23)  # Torque Nm ... (Connector R)
                _safe_set(ws, "P15", CC25)  # Torque Nm ... BTC
                _safe_set(ws, "M16", CC20)  # Result DBB
                _safe_set(ws, "N16", CC22)  # Result body/Connector L
                _safe_set(ws, "O16", CC24)  # Result Connector R
                _safe_set(ws, "P16", CC26)  # Result BTC
                _safe_set(ws, "T13", CC12)  # Run Torque Nm @ Atmospheric
                _safe_set(ws, "A25", CC27)  # Remarks
    except Exception:
        pass

    try:
        # PRESSURE_GAUGE_ANALYSIS: fill as per table
        with connection.cursor() as cpg2:
            if valve_serial_for_query:
                cpg2.execute(
                    """
                    SELECT INSTRUMENT_TYPE, CAL_DUE_DATE, CAL_DONE_DATE, INSTRUMENT_SER_NO, `RANGE`
                    FROM pressure_gauge_analysis
                    WHERE VALVE_SER_NO= %s
                    ORDER BY id ASC
                    """,
                    [valve_serial_for_query],
                )
            else:
                cpg2.execute(
                    """
                    SELECT INSTRUMENT_TYPE, CAL_DUE_DATE, CAL_DONE_DATE, INSTRUMENT_SER_NO, `RANGE`
                    FROM pressure_gauge_analysis
                    WHERE STATION_STATUS = %s
                    ORDER BY id ASC
                    """,
                    [station_id],
                )
            rows = cpg2.fetchall() or []
        # Header details 1/2
        if len(rows) >= 1:
            _safe_set(ws, "O7", rows[0][0])
            _safe_set(ws, "T7", rows[0][1])
        if len(rows) >= 2:
            _safe_set(ws, "O10", rows[1][0])
            _safe_set(ws, "T10", rows[1][1])
        # Up to 4 instruments block rows
        grid = [
            ("A23", "D23", "G23"),
            ("A24", "D24", "G24"),
            ("K23", "O23", "R23"),
            ("K24", "O24", "R24"),
        ]
        for i in range(min(4, len(rows))):
            itype, cal_due, cal_done, serno, rng = rows[i]
            c_inst, c_combo, c_due = grid[i]
            _safe_set(ws, c_inst, itype)
            combo = f"{serno or ''}/{rng or ''}".strip("/")
            _safe_set(ws, c_combo, combo)
            _safe_set(ws, c_due, cal_due)
    except Exception:
        pass

    # Save to bytes (apply moderate font size first)
    try:
        _apply_font_size(ws, size=12)
    except Exception:
        pass
    out = io.BytesIO()
    wb.save(out)
    out.seek(0)
    return out

@login_required
def trunnion_mounted_ball_valve_form(request):
    # Render only the form HTML (not full page)
    return render(request, 'floating_ball_form.html')

@login_required
def floating_ball_valve_form(request):
    return render(request, 'tmpv_form.html')

  

@login_required
def sap_form_page(request):
    standards = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT STANDARD_NAME FROM standard ORDER BY STANDARD_NAME")
        standards = [row[0] for row in cursor.fetchall()]
    return render(request, 'sap_form.html', {"newapp_standard": standards})


@login_required
def get_valve_form(request):
    valve_type = request.GET.get('valve_type')

    if valve_type == "Floating Ball valve":
        html = render_to_string('floating_ball_valve_form.html')
    elif valve_type == "TMBV":
        html = render_to_string('trunnion_mounted_ball_valve_form.html')
    else:
        html = "<p>No form available for this valve type</p>"

    return JsonResponse({"html": html})



@permission_required("Employee")
def employee(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, employee_type, code, name, password, email, mobile, image
            FROM newapp_employee
            WHERE superuser = 0
            ORDER BY id
        """)
        rows = cursor.fetchall()
        employees = [
            {
                'id': r[0],
                'employee_type': r[1],
                'code': r[2],
                'name': r[3],
                'password': r[4],
                'email': r[5],
                'mobile': r[6],
                'image': r[7],
            }
            for r in rows
        ]

        cursor.execute("SELECT code FROM newapp_employee")
        existing_codes_raw = [r[0] for r in cursor.fetchall()]

    existing_employee_codes = json.dumps(existing_codes_raw, cls=DjangoJSONEncoder)

    return render(request, 'employee.html', {
        'employees': employees,


        'existing_employee_codes': existing_employee_codes,
    })


import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import connection
from django.shortcuts import redirect
from django.contrib import messages

@permission_required("Employee")
def employee_add(request):
    if request.method == 'POST':
        employee_type = request.POST.get('employee_type')
        code = request.POST.get('employee_code', '').strip()
        name = request.POST.get('employee_name', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '')
        mobile = request.POST.get('mobile', '')
        image = request.FILES.get('image')

        with connection.cursor() as cursor:
            # check duplicate code
            cursor.execute("SELECT COUNT(*) FROM newapp_employee WHERE code=%s", [code])
            if cursor.fetchone()[0] > 0:
                messages.error(request, 'This Employee Code already exists.')
                return redirect('employee')

            # Save image if uploaded
            filename = None
            if image:
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                filename = fs.save(image.name, image)  # file saved physically in /media/

            encryted_password = make_password(password)

            # Insert record
            cursor.execute("""
                INSERT INTO newapp_employee (employee_type, code, name, password, email, mobile, image)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, [employee_type, code, name, encryted_password, email, mobile, filename])

        messages.success(request, 'Employee added successfully.')
        return redirect('employee')


@permission_required("Employee")
def employee_edit(request, id):
    if request.method == 'POST':
        employee_type = request.POST.get('employee_type')
        new_code = request.POST.get('employee_code', '').strip()
        name = request.POST.get('employee_name', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '')
        mobile = request.POST.get('mobile', '')
        image = request.FILES.get('image')

        with connection.cursor() as cursor:
            # check duplicate code
            cursor.execute(
                "SELECT COUNT(*) FROM newapp_employee WHERE code=%s AND id != %s",
                [new_code, id]
            )
            if cursor.fetchone()[0] > 0:
                messages.error(request, 'This Employee Code already exists.')
                return redirect('employee')

            # Handle image save
            if image:
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                filename = fs.save(image.name, image)   # saves file into /media/
                # only save filename in DB
                cursor.execute("""
                    UPDATE newapp_employee
                    SET employee_type=%s, code=%s, name=%s, password=%s,
                        email=%s, mobile=%s, image=%s
                    WHERE id=%s
                """, [employee_type, new_code, name, password,
                      email, mobile, filename, id])
            else:
                cursor.execute("""
                    UPDATE newapp_employee
                    SET employee_type=%s, code=%s, name=%s, password=%s,
                        email=%s, mobile=%s
                    WHERE id=%s
                """, [employee_type, new_code, name, password, email, mobile, id])

        messages.success(request, 'Employee updated successfully.')
        return redirect('employee')

    # Fetch employee for edit form
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, employee_type, code, name, password, email, mobile, image
            FROM newapp_employee
            WHERE id=%s
        """, [id])
        row = cursor.fetchone()
        employee = {
            'id': row[0],
            'employee_type': row[1],
            'code': row[2],
            'name': row[3],
            'password': row[4],
            'email': row[5],
            'mobile': row[6],
            'image': row[7],
        }
        # Build correct media URL
        if employee['image']:
            employee['image_url'] = f"{settings.MEDIA_URL}{employee['image']}"
        else:
            employee['image_url'] = None

        cursor.execute("SELECT code FROM newapp_employee WHERE id != %s", [id])
        existing_codes = [r[0] for r in cursor.fetchall()]

    return render(request, 'employee_edit.html', {
        'employee': employee,
        'existing_employee_codes': existing_codes,
    })

@permission_required("Employee")
def employee_delete(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM newapp_employee WHERE id=%s", [id])

    messages.success(request, 'Employee deleted successfully.')
    return redirect('employee')


def dictfetchall(cursor):
    """Return all rows from cursor as dicts"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def dictfetchone(cursor):
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    if row:
        return dict(zip(columns, row))
    return None

@superuser_required(min_level=1)
def user_permissions_view(request):
    # Fetch non-superuser employees
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM newapp_employee WHERE superuser=0 ORDER BY name ASC")
        employees = dictfetchall(cursor)

    selected_employee = None
    selected_item_ids = []
    is_selected_superuser = False

    # Handle GET request for viewing permissions
    if request.method == 'GET' and 'user_id' in request.GET:
        employee_id = request.GET.get('user_id')
        if employee_id:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM newapp_employee WHERE id=%s", [employee_id])
                selected_employee = dictfetchone(cursor)

            if selected_employee and selected_employee['superuser']:
                messages.error(request, 'Cannot assign permissions to a superuser.')
                return redirect('user_permissions_view')

            # Fetch existing permissions
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT menu_item_id FROM newapp_usermenupermission
                    WHERE employee_id=%s
                """, [employee_id])
                selected_item_ids = [row['menu_item_id'] for row in dictfetchall(cursor)]

            is_selected_superuser = bool(selected_employee['superuser'])

    # Handle POST request for updating permissions
    if request.method == 'POST':
        employee_id = request.POST.get('user_id')
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM newapp_employee WHERE id=%s", [employee_id])
            selected_employee = dictfetchone(cursor)

        if selected_employee and selected_employee['superuser']:
            messages.error(request, 'Cannot assign permissions to a superuser.')
            return redirect('user_permissions_view')

        is_selected_superuser = bool(selected_employee['superuser'])

        selected_ids = request.POST.getlist('menu_items')

        # Delete existing permissions
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM newapp_usermenupermission WHERE employee_id=%s", [employee_id])

        # Insert new permissions
        with connection.cursor() as cursor:
            for item_id in selected_ids:
                if item_id:
                    cursor.execute("""
                        INSERT INTO newapp_usermenupermission (employee_id, menu_item_id)
                        VALUES (%s, %s)
                    """, [employee_id, item_id])

        messages.success(request, 'User permissions updated successfully!')
        return redirect('/user_permissions_view/')

    # Load menu items and group by section
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM newapp_menuitem")
        menu_items = dictfetchall(cursor)

    if selected_employee and not selected_employee['superuser']:
        menu_items = [
            item for item in menu_items
            if item['section'] != 'settings' and item['name'] != 'Category' and item['name'] != 'Test Type' and item['name'] != 'Instrument Type'
        ]


    # Group menu items by section
    menu_items_by_section = {}
    for item in menu_items:
        menu_items_by_section.setdefault(item['section'], []).append(item)

    context = {
        'users': employees,
        'selected_user': selected_employee,
        'selected_item_ids': list(map(int, selected_item_ids)),
        'menu_items_by_section': menu_items_by_section,
        'is_selected_superuser': is_selected_superuser,
    }

    return render(request, 'user_permissions.html', context)



from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime
from django.db import connection

from django.shortcuts import render
from django.db import connection
from datetime import datetime

@permission_required("Gauge Details")
def gauge_details(request):
    gauges = []
    validation_errors = []

    with connection.cursor() as cursor:
        # Fetch gauge data - Order by ACTIVE_STATUS DESC (Enable=1 first), then STATION_ID, then INSTRUMENT_ID
        cursor.execute("""
            SELECT INSTRUMENT_ID, INSTRUMENT_SER_NO, `RANGE`, INSTRUMENT_TYPE,
                   CAL_DUE_DATE, CAL_DONE_DATE,
                   ACTIVE_STATUS, STATION_ID, DUE_ALARM
            FROM gauge_details
            ORDER BY ACTIVE_STATUS DESC, STATION_ID, INSTRUMENT_ID
        """)
        rows = cursor.fetchall()

        # Fetch enabled instrument types
        cursor.execute("""
            SELECT INSTRUMENT_TYPE
            FROM instrument_categories
            WHERE INSTRUMENT_STATUS = 'ENABLE'
        """)
        instrument_types = [row[0] for row in cursor.fetchall()]

        for r in rows:
            cal_due_date = r[4]
            cal_done_date = r[5]
            errors = []

            # Strict validations
            if cal_due_date and cal_done_date:
                if cal_done_date > cal_due_date:
                    errors.append("Calibration done date cannot be after due date.")

            if cal_due_date:
                if cal_due_date < datetime.now().date():
                    errors.append("Calibration due date is in the past.")

            if not cal_done_date and cal_due_date:
                errors.append("Calibration done date is missing while due date exists.")

            # Build gauge dict
            gauges.append({
                'gauge_id': r[0],
                'gauge_ser_no': r[1],
                'range': r[2],
                'gauge_type': r[3],
                'cal_due_date': cal_due_date.strftime('%Y-%m-%d') if cal_due_date else '',
                'cal_done_date': cal_done_date.strftime('%Y-%m-%d') if cal_done_date else '',
                'active_status': r[6],
                'station_id': r[7],
                'due_alarm': r[8],
                'errors': errors,
            })

            if errors:
                validation_errors.append({
                    'gauge_id': r[0],
                    'errors': errors,
                })

    return render(request, 'gauge_details.html', {
        'gauges': gauges,
        'instrument_types': instrument_types,
        'validation_errors': validation_errors,
    })

def _parse_date_ymd(val):
    if not val:
        return None
    try:
        return datetime.strptime(val, "%Y-%m-%d").date()
    except Exception:
        try:
            return datetime.strptime(val, "%d-%m-%Y").date()
        except Exception:
            return None

from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import connection

@csrf_exempt
@permission_required("Gauge Details")
def gauge_save(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    try:
        # Extract all rows from form
        gauge_names = request.POST.getlist('station1_gauge_name[]')
        serials = request.POST.getlist('station1_serial[]')
        ranges = request.POST.getlist('station1_range[]')
        types = request.POST.getlist('station1_type[]')
        done_dates = request.POST.getlist('station1_done_date[]')
        due_dates = request.POST.getlist('station1_due_date[]')
        station_ids = request.POST.getlist('station1_id[]')
        statuses = request.POST.getlist('station1_status[]')
        instrument_ids = request.POST.getlist('station1_instrument_id[]')  # optional hidden field for updates

        now_ts = timezone.now()

        # First, validate for duplicate serial numbers within the form
        serial_map = {}
        for i in range(len(gauge_names)):
            serial = serials[i].strip()
            if serial:
                instrument_id = ''
                try:
                    instrument_id = instrument_ids[i].strip()
                except (IndexError, ValueError):
                    pass
                
                if serial in serial_map:
                    messages.error(request, f'Duplicate serial number "{serial}" detected. Please use unique serial numbers.')
                    return redirect('gauge_details')
                serial_map[serial] = (i, instrument_id)

        # Now validate against database for each serial number
        with connection.cursor() as cursor:
            for serial, (idx, current_id) in serial_map.items():
                if current_id:
                    # Check if another record has this serial number
                    cursor.execute(
                        "SELECT INSTRUMENT_ID FROM gauge_details WHERE INSTRUMENT_SER_NO=%s AND INSTRUMENT_ID != %s",
                        [serial, current_id]
                    )
                else:
                    # New record, check if serial already exists
                    cursor.execute(
                        "SELECT INSTRUMENT_ID FROM gauge_details WHERE INSTRUMENT_SER_NO=%s",
                        [serial]
                    )
                
                existing = cursor.fetchone()
                if existing:
                    messages.error(request, f'Serial number "{serial}" already exists in database. Please use a unique serial number.')
                    return redirect('gauge_details')

        # Check for empty new rows before processing
        for i in range(len(gauge_names)):
            try:
                instrument_id = instrument_ids[i].strip()
            except (IndexError, ValueError):
                instrument_id = ''
            
            # Skip validation for existing rows
            if instrument_id:
                continue
            
            # For new rows, check if they are empty
            serial = serials[i].strip() if i < len(serials) else ''
            rng = ranges[i].strip() if i < len(ranges) else ''
            gauge_type = types[i].strip() if i < len(types) else ''
            station_id = station_ids[i].strip() if i < len(station_ids) else ''
            
            # If all key fields are empty, show error
            if not (serial or rng or gauge_type or station_id):
                messages.error(request, 'Empty gauge details are not allowed. Please fill all required fields or remove empty rows.')
                return redirect('gauge_details')

        # Validate station-wise row count (max 10 ENABLED rows per station)
        station_counts = {}
        for i in range(len(gauge_names)):
            station_id_str = station_ids[i].strip() if i < len(station_ids) else ''
            status_str = statuses[i].strip().lower() if i < len(statuses) else ''
            
            # Only count if station is selected AND status is enable
            if station_id_str and status_str == 'enable':
                try:
                    station_id_int = int(station_id_str)
                    if station_id_int not in station_counts:
                        station_counts[station_id_int] = 0
                    station_counts[station_id_int] += 1
                except (ValueError, IndexError):
                    pass
        
        # Check if any station has more than 10 enabled rows
        for station_id_int, count in station_counts.items():
            if count > 10:
                station_name = f'Station {station_id_int}'
                messages.error(request, f'{station_name} has {count} enabled rows. Only 10 enabled rows are allowed per station.')
                return redirect('gauge_details')

        for i in range(len(gauge_names)):
            # Use existing INSTRUMENT_ID or generate new
            try:
                gauge_id = int(instrument_ids[i])
            except (IndexError, ValueError):
                with connection.cursor() as cursor:
                    cursor.execute("SELECT COALESCE(MAX(INSTRUMENT_ID), 0) + 1 FROM gauge_details")
                    gauge_id = cursor.fetchone()[0]

            gauge_name = gauge_names[i].strip()
            gauge_ser_no = serials[i].strip()
            rng = ranges[i].strip()
            gauge_type = types[i].strip()
            cal_done_date = _parse_date_ymd(done_dates[i])
            cal_due_date = _parse_date_ymd(due_dates[i])

            try:
                station_id = int(station_ids[i])
            except:
                station_id = 0

            active_status = 1 if statuses[i].strip().lower() == 'enable' else 0

            with connection.cursor() as cursor:
                # Check if the gauge exists
                cursor.execute("SELECT CAL_DUE_DATE FROM gauge_details WHERE INSTRUMENT_ID=%s", [gauge_id])
                row = cursor.fetchone()
                # prev_due = row[0] if row else None
                # due_alarm = 1 if (prev_due and cal_due_date and cal_due_date > prev_due) else 0

                if row:
                    # UPDATE existing
                    cursor.execute(
                        """
                        UPDATE gauge_details
                        SET INSTRUMENT_SER_NO=%s, `RANGE`=%s, INSTRUMENT_TYPE=%s,
                            CAL_DUE_DATE=%s, CAL_DONE_DATE=%s,
                            ACTIVE_STATUS=%s, STATION_ID=%s,
                            UPDATED_DATE=%s
                        WHERE INSTRUMENT_ID=%s
                        """,
                        [gauge_ser_no, rng, gauge_type,
                         cal_due_date, cal_done_date,
                         active_status, station_id,
                         now_ts, gauge_id]
                    )
                    
                    # Log UPDATE
                    cursor.execute(
                        """
                        INSERT INTO gauge_log_details (
                            INSTRUMENT_ID, INSTRUMENT_SER_NO, `RANGE`, INSTRUMENT_TYPE,
                            CAL_DUE_DATE, CAL_DONE_DATE,
                            STATION_ID, CREATED_DATE
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        [gauge_id, gauge_ser_no, rng, gauge_type,
                         cal_due_date, cal_done_date,
                         station_id, now_ts]
                    )
                else:
                    # INSERT new - skip empty rows
                    # Check if any required field has data
                    has_data = gauge_ser_no or rng or gauge_type or station_id
                    
                    if has_data:
                        cursor.execute(
                            """
                            INSERT INTO gauge_details (
                                INSTRUMENT_ID, INSTRUMENT_SER_NO, `RANGE`, INSTRUMENT_TYPE,
                                CAL_DUE_DATE, CAL_DONE_DATE,
                                ACTIVE_STATUS, STATION_ID,
                                CREATED_DATE, UPDATED_DATE
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                            [gauge_id, gauge_ser_no, rng, gauge_type,
                             cal_due_date, cal_done_date,
                             active_status, station_id,
                             now_ts, now_ts]
                        )

                        # Log
                        cursor.execute(
                            """
                            INSERT INTO gauge_log_details (
                                INSTRUMENT_ID, INSTRUMENT_SER_NO, `RANGE`, INSTRUMENT_TYPE,
                                CAL_DUE_DATE, CAL_DONE_DATE,
                                STATION_ID, CREATED_DATE
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                            [gauge_id, gauge_ser_no, rng, gauge_type,
                             cal_due_date, cal_done_date,
                             station_id, now_ts]
                        )
        messages.success(request, 'Gauge details saved successfully.')
        # Redirect back to the same page
        return redirect('gauge_details')

    except Exception as e:
        return redirect('gauge_details')
        

@csrf_exempt
@permission_required("Gauge Details")
def gauge_delete(request, instrument_id):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Invalid method'}, status=405)
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM gauge_details WHERE INSTRUMENT_ID=%s", [instrument_id])
        return JsonResponse({'ok': True})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)


@csrf_exempt
@login_required
def check_serial_exists(request):
    if request.method != 'GET':
        return JsonResponse({'exists': False}, status=405)
    
    serial = request.GET.get('serial', '').strip()
    exclude_id = request.GET.get('exclude_id', '').strip()
    
    if not serial:
        return JsonResponse({'exists': False})
    
    try:
        with connection.cursor() as cursor:
            if exclude_id:
                cursor.execute(
                    "SELECT COUNT(*) FROM gauge_details WHERE INSTRUMENT_SER_NO=%s AND INSTRUMENT_ID != %s",
                    [serial, exclude_id]
                )
            else:
                cursor.execute(
                    "SELECT COUNT(*) FROM gauge_details WHERE INSTRUMENT_SER_NO=%s",
                    [serial]
                )
            count = cursor.fetchone()[0]
            return JsonResponse({'exists': count > 0})
    except Exception as e:
        return JsonResponse({'exists': False, 'error': str(e)})


@permission_required("Instrument Type")
def instrument_type(request):
    # ✅ Fetch all instrument types - Order by INSTRUMENT_STATUS DESC (ENABLE first), then INSTRUMENT_TYPE_ID
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT INSTRUMENT_TYPE_ID, INSTRUMENT_TYPE, INSTRUMENT_STATUS
            FROM instrument_categories
            ORDER BY INSTRUMENT_STATUS DESC, INSTRUMENT_TYPE_ID
        """)
        instrument_types = cursor.fetchall()

    if request.method == "POST":
        instrument_ids = request.POST.getlist("instrument_id[]")
        instrument_names = request.POST.getlist("instrument_name[]")
        statuses = request.POST.getlist("status[]")

        # ✅ Process each record - Insert new or Update existing
        with connection.cursor() as cursor:
            for instrument_id, instrument_name, status in zip(instrument_ids, instrument_names, statuses):
                instrument_name = instrument_name.strip()
                status = status.strip()
                
                # Skip empty rows
                if not instrument_name:
                    continue
                
                if instrument_id and instrument_id.strip():
                    # Update existing record
                    cursor.execute("""
                        UPDATE instrument_categories
                        SET INSTRUMENT_TYPE = %s,
                            INSTRUMENT_STATUS = %s,
                            UPDATED_DATE = NOW()
                        WHERE INSTRUMENT_TYPE_ID = %s
                    """, [instrument_name, status, instrument_id])
                else:
                    # Insert new record - calculate next INSTRUMENT_TYPE_ID
                    cursor.execute("SELECT COALESCE(MAX(INSTRUMENT_TYPE_ID), 0) + 1 FROM instrument_categories")
                    next_instrument_type_id = cursor.fetchone()[0]
                    
                    cursor.execute("""
                        INSERT INTO instrument_categories 
                        (INSTRUMENT_TYPE_ID, INSTRUMENT_TYPE, INSTRUMENT_STATUS, CREATED_DATE, UPDATED_DATE)
                        VALUES (%s, %s, %s, NOW(), NOW())
                    """, [next_instrument_type_id, instrument_name, status])

        messages.success(request, "Instrument details saved successfully!")
        return redirect("instrument_type")  # Reload page after update

    # ✅ Prepare data for template
    data = [
        {
            "id": row[0],
            "instrument_name": row[1],
            "status": row[2],
        }
        for row in instrument_types
    ]

    return render(request, "instrument_type.html", {"instrument_types": data})


@csrf_exempt
@permission_required("Instrument Type")
def instrument_type_delete(request, instrument_type_id):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Invalid method'}, status=405)
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM instrument_categories WHERE INSTRUMENT_TYPE_ID=%s", [instrument_type_id])
        return JsonResponse({'ok': True})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.db import connection
import os
import traceback

@login_required
def graph(request):
    serial_numbers = []

    # ✅ Fetch distinct serial numbers from pressure_analysis
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT VALVE_SER_NO
                FROM pressure_analysis
                WHERE VALVE_SER_NO IS NOT NULL
                ORDER BY VALVE_SER_NO
            """)
            serial_numbers = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print(f"❌ Error fetching serial numbers: {e}")

    # ✅ Handle POST request for PDF download
    if request.method == 'POST':
        valve_serial = request.POST.get('valve_serial') or request.POST.get('valve_serial_input')
        count_id = request.POST.get('count_id')

        if not valve_serial:
            if request.POST.get('ajax'):
                return JsonResponse({'status': 'error', 'message': 'Please select a serial number.'}, status=400)
            messages.error(request, 'Please select a serial number.')
            return render(request, "graph.html", {'serial_numbers': serial_numbers})

        try:
            # Convert count_id if provided
            try:
                count_id_int = int(count_id) if count_id and count_id.strip().isdigit() else None
            except Exception:
                count_id_int = None
            if count_id_int == 0:
                count_id_int = None

            # ✅ Generate PDF for selected serial number
            pdf_result = _generate_and_save_merged_pdf_to_disk(serial_number=valve_serial, count_id=count_id_int)
            # Handle return list of tuples (path, serial)
            pdf_path = pdf_result[0][0] if pdf_result and isinstance(pdf_result, list) else ''

            if not pdf_path:
                # Check if serial exists in pressure_analysis
                with connection.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM pressure_analysis WHERE VALVE_SER_NO=%s", [valve_serial])
                    count = cursor.fetchone()[0] if cursor.fetchone() else 0

                if count == 0:
                    msg = f'No test data found for serial number: {valve_serial}. Please ensure tests have been completed for this valve.'
                    if request.POST.get('ajax'):
                        return JsonResponse({'status': 'error', 'message': msg}, status=400)
                    messages.error(request, msg)
                else:
                    charts_root = r"D:\LNT_Reports\Graphs"
                    if not os.path.exists(charts_root):
                        msg = f'Charts folder not found: {charts_root}. Please ensure the graphs folder exists.'
                        if request.POST.get('ajax'):
                            return JsonResponse({'status': 'error', 'message': msg}, status=500)
                        messages.error(request, msg)
                    else:
                        msg = f'Error generating PDF report for serial {valve_serial}. Please check server logs for details.'
                        if request.POST.get('ajax'):
                            return JsonResponse({'status': 'error', 'message': msg}, status=500)
                        messages.error(request, msg)

                if request.POST.get('ajax'):
                    return JsonResponse({'status': 'error', 'message': 'PDF generation failed'}, status=500)
                return render(request, "graph.html", {'serial_numbers': serial_numbers})

            if not os.path.exists(pdf_path):
                msg = f'Generated PDF file not found at: {pdf_path}. Please try again.'
                if request.POST.get('ajax'):
                    return JsonResponse({'status': 'error', 'message': msg}, status=500)
                messages.error(request, msg)
                return render(request, "graph.html", {'serial_numbers': serial_numbers})

            # ✅ If AJAX request, return path
            if request.POST.get('ajax'):
                return JsonResponse({'status': 'success', 'path': pdf_path})

            # ✅ Otherwise, serve as file download
            with open(pdf_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                safe_serial = ''.join(ch if str(ch).isalnum() or ch in ('-', '_') else '_' for ch in str(valve_serial))
                response['Content-Disposition'] = f'attachment; filename="merged_report_{safe_serial}.pdf"'
                return response

        except Exception as e:
            error_details = traceback.format_exc()
            print(f"❌ Error generating PDF: {error_details}")
            if request.POST.get('ajax'):
                return JsonResponse({'status': 'error', 'message': f'Error generating PDF: {str(e)}'}, status=500)
            messages.error(request, f'Error generating PDF: {str(e)}. Please check server logs for details.')
            return render(request, "graph.html", {'serial_numbers': serial_numbers})

    # ✅ Render page with serial list
    return render(request, "graph.html", {'serial_numbers': serial_numbers})



@csrf_exempt
@login_required
def vtr(request):
    # Handle POST request from downloadExcelReport() to check valve type
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            valve_serial_number = data.get('valve_serial_number', '').strip()
            
            if not valve_serial_number:
                return JsonResponse({'status': 'error', 'message': 'Valve serial number is required'})
            
            # Try to get valve type from pressure_analysis table
            valve_type = None
            with connection.cursor() as cursor:
                # First try pressure_analysis
                cursor.execute("""
                    SELECT VALVETYPE_NAME 
                    FROM pressure_analysis
                    WHERE VALVE_SER_NO = %s
                    ORDER BY ID DESC 
                    LIMIT 1
                """, [valve_serial_number])
                result = cursor.fetchone()
                
                if result and result[0]:
                    valve_type = result[0]
                else:
                    # Fallback to master_temp_data1
                    try:
                        cursor.execute("""
                            SELECT vt.name as valve_type_name
                            FROM master_temp_data1 mtd
                            JOIN newapp_valvetype vt ON mtd.type = vt.id
                            WHERE mtd.valve_serial_no = %s
                            ORDER BY mtd.id DESC 
                            LIMIT 1
                        """, [valve_serial_number])
                        result = cursor.fetchone()
                        if result and result[0]:
                            valve_type = result[0]
                    except Exception:
                        pass
            
            if valve_type:
                return JsonResponse({
                    'status': 'success', 
                    'valve_type': valve_type,
                    'message': 'Valve type determined successfully'
                })
            else:
                return JsonResponse({
                    'status': 'error', 
                    'message': f'Valve type not found for serial number {valve_serial_number}'
                })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    # Handle GET request - render the page
    # Fetch distinct VALVE_SER_NO from pressure_analysis table
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT VALVE_SER_NO FROM pressure_analysis WHERE VALVE_SER_NO IS NOT NULL AND VALVE_SER_NO != '' ORDER BY VALVE_SER_NO")
        valve_serial_numbers = [row[0] for row in cursor.fetchall()]
    
    return render(request, "vtr.html", {"valve_serial_numbers": valve_serial_numbers})

TesleadSmartsyncx = None

# def hmi_check_loop():
#     global hmi_connected, TesleadSmartsyncx
#     while True:
#         try:
#             TesleadSmartsyncx = ModbusTcpClient('127.0.0.1')
#             # TesleadSmartsyncx = ModbusTcpClient('192.168.1.66')
#             TesleadSmartsyncx.connect()
#             hmi_connected = TesleadSmartsyncx.connect()
#             print(TesleadSmartsyncx.connect())
#             if TesleadSmartsyncx.connect():
#                 print("✅ HMI connected.")
#             else:
#                 print("❌ HMI disconnected!")
#         except Exception as e:
#             print("❌ HMI connection error:", e)
#             hmi_connected = False
#         time.sleep(2)

# # Start the background thread once when views.py is loaded
# threading.Thread(target=hmi_check_loop, daemon=True).start()


def hmi_conn():
    try:
        global TesleadSmartsyncx
        TesleadSmartsyncx = ModbusTcpClient('10.21.94.203')
        # TesleadSmartsyncx = ModbusTcpClient('127.0.0.1')
        # TesleadSmartsyncx = ModbusTcpClient('192.168.1.106')
        # TesleadSmartsyncx = ModbusTcpClient('192.168.1.66')
        TesleadSmartsyncx.connect()
        # Check what parameters the method actually expects
    except Exception as e:
        print("Modbus connection error: >>>>", e)
hmi_conn()



@login_required
def livepage(request):
    # machine_mode = TesleadSmartsyncx.read_holding_registers(2017, 1).registers[0]
    machine_mode = TesleadSmartsyncx.read_holding_registers(2017, 1)

    if machine_mode.isError():
        raise Exception(f"Modbus error reading register 2017: {machine_mode}")

    machine_mode = machine_mode.registers[0]

    if machine_mode == 1:
        machine_mode = "Auto"
    else:
        machine_mode = "Manual"
    write_read(request)
    return render(request,'livepage.html',{'machinemode':machine_mode})

@login_required
def secondpage(request):
    return render(request,'new_live.html')

@login_required
def get_all_pressure_data(request):
    """Return pressure data for all 4 gauges"""
    try:
        serials = ['1234','456','789','0123']
        gauges = []
        with connection.cursor() as cursor:
            for idx, s in enumerate(serials, start=1):
                cursor.execute(
                    """
                    SELECT PRESSURE
                    FROM current_Status
                    WHERE VALVE_SERIAL_NO = %s
                    ORDER BY ID DESC
                    LIMIT 1
                    """,
                    [s],
                )
                row = cursor.fetchone()
                p = float(row[0]) if row and row[0] is not None else 0.0
                gauges.append({
                    'pressure': p,
                    'leak_status': 'No Leak Observed',
                    'name': f'Station {idx}',
                    'unit': 'bar'
                })

        return JsonResponse({'status': 'success','gauges': gauges})
            
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)


# Simple in-memory flags per station; consider persisting per Serial_number for robustness
previous_timer_by_station = {}




@login_required
def get_buttons(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT TEST_ID, TEST_NAME FROM temp_testing_data")
        results = cursor.fetchall()
        print('Results:', results)

        test_data = []
        for row in results:
            test_data.append({
                'test_id': row[0],
                'test_name': row[1]
            })
            
        cursor.execute("select VALVE_SER_NO from master_temp_data where STATION_STATUS=%s and CYCLE_COMPLETE=%s",[1,0])
        active_serial_no = cursor.fetchall()
        print('active serial number',active_serial_no)
        
        serial = []
        for test_serial in active_serial_no:
            serial.append({
                'active_sno':test_serial[0]
            })
        
        return JsonResponse({"status": "success", "data": test_data, "active_serialnumber":serial})

@login_required
def get_size_class(request):
    with connection.cursor() as cursor:

        # Get all active station IDs
        cursor.execute("SELECT ID FROM master_temp_data WHERE STATION_STATUS=%s", [1])
        active_station = cursor.fetchall()
        print("activestation", active_station)

        # Fetch only one fully filled row
        cursor.execute("""
            SELECT SIZE_NAME, CLASS_NAME, TYPE_NAME, SHELL_MATERIAL_NAME, PRESSURE_UNIT, COL7_VALUE, COL8_VALUE, COL11_VALUE,COL9_VALUE,COL12_VALUE
            FROM master_temp_data
            WHERE STATION_STATUS=%s
              AND SIZE_NAME IS NOT NULL
              AND CLASS_NAME IS NOT NULL
              AND TYPE_NAME IS NOT NULL
              AND SHELL_MATERIAL_NAME IS NOT NULL
              AND PRESSURE_UNIT IS NOT NULL
              AND COL7_VALUE IS NOT NULL
              AND COL8_VALUE IS NOT NULL
              AND COL11_VALUE IS NOT NULL
            ORDER BY ID DESC
            LIMIT 1
        """, [1])

        row = cursor.fetchone()

        if row:
            data = {
                'size_name': row[0],
                'class_name': row[1],
                'type_name': row[2],
                'shell_material_name': row[3],
                'pressure_unit': row[4],
                'col7_value': row[5],
                'col8_value': row[6],
                'col11_value': row[7],
                'COL9_VALUE':row[8],
                'COL12_VALUE':row[9],
            }

            # Default gauge range
            gauge_range = "0-2000"

            # Gauge range logic
            if row[4] in ["bar", "kg/cm2"]:
                if row[1] == "#150":
                    gauge_range = "0-250"
                elif row[1] == "#300":
                    gauge_range = "0-300"
                elif row[1] == "#600" and row[2] == "#900":
                    gauge_range = "0-1000"
                elif row[1] == "#1500":
                    gauge_range = "0-1000"
                elif row[1] == "#2500":
                    gauge_range = "0-1500"

            elif row[4] == "psi":
                if row[1] == "#150":
                    gauge_range = "0-1000"
                elif row[1] == "#300":
                    gauge_range = "0-3000"
                elif row[1] == "#600" and row[2] == "#900":
                    gauge_range = "0-6000"
                elif row[1] == "#1500":
                    gauge_range = "0-10000"
                elif row[1] == "#2500":
                    gauge_range = "0-15000"

            return JsonResponse({
                "status": "success",
                "data": data,
                "active_station": active_station,
                "gauge_range": gauge_range
            })

        else:
            return JsonResponse({"status": "failure", "message": "No fully filled data found"})


@login_required
def get_test_settings(request):
    test_id = request.GET.get('test_id')
   
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT TEST_ID, TEST_NAME, TESTING_PR_UNIT,
                   TESTING_PR_BAR, TESTING_PR_PSI,TESTING_PR_KGCM2, TESTING_DUR_SEC
            FROM temp_testing_data
            WHERE TEST_ID=%s
        """, [test_id])
       
        result = cursor.fetchone()
       
        if result:
            pressure_unit = result[2]
           
            if pressure_unit == 'bar':
                set_pressure = result[3]  # TESTING_PR_BAR
            elif pressure_unit == 'psi':
                set_pressure = result[4]  # TESTING_PR_PSI
            elif pressure_unit == 'kg/cm2':
                set_pressure = result[5]  # TESTING_PR_KGCM2
           
            data = {
                'test_id': result[0],
                'test_name': result[1],
                'pressure_unit': pressure_unit,
                'set_pressure': set_pressure,
                'set_time': result[6]
            }
            TesleadSmartsyncx.write_register(2004,result[0])

            set_pressure = None
            set_time = None
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT TESTING_PR_UNIT, TESTING_PR_BAR, TESTING_PR_PSI, TESTING_PR_KGCM2, TESTING_DUR_SEC
                        FROM temp_testing_data WHERE TEST_ID=%s
                        """,
                        [test_id]
                    )
                    trow = cursor.fetchone()
                    if trow:
                        unit = (trow[0] or '').lower()
                        set_pressure = (
                            trow[1] if unit == 'bar'
                            else trow[2] if unit == 'psi'
                            else trow[3] if unit == 'kg/cm2'
                            else None
                        )
                        set_time = trow[4]
                        cursor.execute("SELECT PRESSURE_UNIT FROM master_temp_data where STATION_STATUS=%s",[1])
                        pressure_unit = cursor.fetchone()[0]
                        if pressure_unit in ('bar', 'kg/cm2'):
                            TesleadSmartsyncx.write_register(2000, int(set_pressure * 10))
                            print('this is runned')
                        elif pressure_unit == 'psi':
                            TesleadSmartsyncx.write_register(2000, int(set_pressure))
                            print('else block runned')
                        TesleadSmartsyncx.write_register(2003, set_time)

                       
            except Exception:
                pass
           
            return JsonResponse({"status": "success", "data": data})
        else:
            return JsonResponse({"status": "failure", "message": "No data found"})


# Global flag to control background thread
_pressure_data_thread_running = False
_pressure_data_thread = None

def collect_pressure_data_background():
    """Background thread function to continuously collect pressure data"""
    global _pressure_data_thread_running
    _pressure_data_thread_running = True
   
    while _pressure_data_thread_running:
        try:
            # Wait for Modbus connection to be available
            if TesleadSmartsyncx is None:
               
                continue
               
            with connection.cursor() as cursor:
                # Get active stations
                cursor.execute("SELECT ID, VALVE_SER_NO FROM master_temp_data WHERE STATION_STATUS = %s", [1])
                active_data = cursor.fetchall()

                if not active_data:
                     # Wait before retrying if no active stations
                    continue

                # Create mapping: { station_id: valve_serial_no }
                active_stations = {row[0]: row[1] for row in active_data}

                # Get shared pressure unit
                cursor.execute("SELECT PRESSURE_UNIT FROM master_temp_data LIMIT 1")
                pressure_unit_result = cursor.fetchone()
                if not pressure_unit_result:
                   
                    continue
                pressure_unit = pressure_unit_result[0]

            # Define Modbus address mapping for all stations
            station_addresses = {
                1: 2008,
                2: 2020,
                3: 2021,
                4: 2022
            }

            # Loop through each active station
            for station_id, valve_serial_no in active_stations.items():
                try:
                    address = station_addresses.get(station_id)

                    if not address:
                        continue
                    # print("First Hi")
                    # Read pressure from Modbus
                    # raw_pressure = TesleadSmartsyncx.read_holding_registers(address, 1).registers[0]
                    response = TesleadSmartsyncx.read_holding_registers(address, 1)

                    if response.isError():
                        raise Exception(f"Modbus error reading register {address}: {response}")

                    raw_pressure = response.registers[0]
                    # print("Second Hi")

                    # Convert pressure based on unit
                    pressure = raw_pressure / 10 if pressure_unit.lower() in ["bar", "kg/cm2"] else raw_pressure

                    # Read other parameters
                    timer_status = TesleadSmartsyncx.read_holding_registers(2010, 1).registers[0]
                    actual_time = TesleadSmartsyncx.read_holding_registers(2006, 1).registers[0]
                    test_id = TesleadSmartsyncx.read_holding_registers(2004, 1).registers[0]
                   

                    # Fetch test metadata
                    test_name = None
                    set_pressure = None
                    set_time = None
                    try:
                        with connection.cursor() as cursor:
                            cursor.execute(
                                """
                                SELECT TEST_NAME, TESTING_PR_UNIT, TESTING_PR_BAR, TESTING_PR_PSI,TESTING_PR_KGCM2, TESTING_DUR_SEC
                                FROM temp_testing_data WHERE TEST_ID=%s
                                """,
                                [test_id]
                            )
                            trow = cursor.fetchone()
                            if trow:
                                test_name = trow[0]
                                unit = (trow[1] or '').lower()
                                set_pressure = (
                                    trow[2] if unit == 'bar'
                                    else trow[3] if unit == 'psi'
                                    else trow[4] if unit == 'kg/cm2'
                                    else None
                                )

                                set_time = trow[5]

                                # TesleadSmartsyncx.write_register(2000, int(set_pressure))  # Set Pressure
                                # TesleadSmartsyncx.write_register(2003, set_time)  # Set Time
                    except Exception:
                        pass

                    # Update pressure data in database
                    update_pressure_data(
                        station_id, valve_serial_no, pressure, timer_status, test_id, actual_time
                    )
                   
                except Exception as e:
                    print("First")
                    print(f"Error in background pressure collection for station {station_id}: {e}")
                    continue

            # Sleep before next iteration (2 seconds to match frontend polling)
            time.sleep(0.2)
           
        except Exception as e:
            print("Second")
            print(f"Error in background pressure data collection: {e}")
            time.sleep(0.2)  # Wait before retrying on error

def start_pressure_data_thread():
    """Start the background thread for continuous pressure data collection"""
    global _pressure_data_thread, _pressure_data_thread_running
   
    if _pressure_data_thread is None or not _pressure_data_thread.is_alive():
        _pressure_data_thread_running = True
        _pressure_data_thread = threading.Thread(target=collect_pressure_data_background, daemon=True)
        _pressure_data_thread.start()
        print("Background pressure data collection thread started")
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



@csrf_exempt
@login_required

def get_pressure_data(request):
    """
    Read-only endpoint to fetch pressure data from database.
    Data collection is handled by collect_pressure_data_background thread.
    """
    # Get test_id from request parameter (for filtering pressure history on page refresh)
    request_test_id = request.GET.get('test_id')
    if request_test_id:
        try:
            request_test_id = int(request_test_id)
        except (ValueError, TypeError):
            request_test_id = None
   
    with connection.cursor() as cursor:
        # Get active stations
        cursor.execute("SELECT ID, VALVE_SER_NO FROM master_temp_data WHERE STATION_STATUS = %s", [1])
        active_data = cursor.fetchall()

        if not active_data:
            return JsonResponse({"error": "No active stations found"}, status=404)

        # Create mapping: { station_id: valve_serial_no }
        active_stations = {row[0]: row[1] for row in active_data}

        # Get shared pressure unit
        cursor.execute("SELECT PRESSURE_UNIT FROM master_temp_data LIMIT 1")
        pressure_unit_row = cursor.fetchone()
        if not pressure_unit_row:
            return JsonResponse({"error": "No pressure unit found"}, status=404)
        pressure_unit = pressure_unit_row[0]

    station_results = []

    # Loop through each active station
    for station_id, valve_serial_no in active_stations.items():
        # Get the latest data from the station's current_status table
        station_tables = {
            1: "current_status_station1",
            2: "current_status_station2",
            3: "current_status_station3",
            4: "current_status_station4",
        }
       
        table_name = station_tables.get(station_id)
        if not table_name:
            station_results.append({
                "station_id": station_id,
                "error": "No table defined for station"
            })
            continue

        try:
            with connection.cursor() as cursor:
                # Get latest record for this station
                cursor.execute(
                    f"""
                    SELECT PRESSURE, TIMER_STATUS, TEST_ID, TEST_NAME, RESULT
                    FROM {table_name}
                    WHERE VALVE_SERIAL_NO=%s AND STATION=%s
                    ORDER BY ID DESC
                    LIMIT 1
                    """,
                    [valve_serial_no, station_id]
                )
                latest_row = cursor.fetchone()
               
                if not latest_row:
                    station_results.append({
                        "station_id": station_id,
                        "error": "No data available"
                    })
                    continue
               
                pressure = float(latest_row[0]) if latest_row[0] is not None else 0.0
                timer_status = latest_row[1]
                test_id = latest_row[2]
                test_name = latest_row[3]
                result_value = latest_row[4]

            # Fetch test metadata for restoring UI on refresh
            set_pressure = None
            set_time = None
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT TESTING_PR_UNIT, TESTING_PR_BAR, TESTING_PR_PSI, TESTING_PR_KGCM2, TESTING_DUR_SEC
                        FROM temp_testing_data WHERE TEST_ID=%s
                        """,
                        [test_id]
                    )
                    trow = cursor.fetchone()
                    if trow:
                        unit = (trow[0] or '').lower()
                        set_pressure = (
                            trow[1] if unit == 'bar'
                            else trow[2] if unit == 'psi'
                            else trow[3] if unit == 'kg/cm2'
                            else None
                        )
                        set_time = trow[4]
            except Exception:
                pass

            # Use filter test_id for reading history (page refresh scenario)
            filter_test_id = test_id
            actual_time = TesleadSmartsyncx.read_holding_registers(2006, 1).registers[0]
           
            # READ ONLY - fetch the data from database
            pressure_history, formatted_times, greenlinetime, redlinetime, result_value, actual_time = read_pressure_data(
                station_id, valve_serial_no, filter_test_id, actual_time
            )
           
            # Add frontend data
            latest_time = (formatted_times or [None])[-1]
            station_results.append({
                "station_id": station_id,
                "timer_status": timer_status,
                "test_id": test_id,
                "valve_serial_no": valve_serial_no,
                "pressure_unit": pressure_unit,
                "pressure_value": pressure,
                "test_name": test_name,
                "set_pressure": set_pressure,
                "set_time": set_time,
                "time": latest_time,
                "times": formatted_times,  
                "pressure_history": pressure_history,  
                'greenlinetime': greenlinetime,
                'redlinetime': redlinetime,
                'result_value': result_value,
                'actual_time' : actual_time
            })
           
        except Exception as e:
            print(f"Error reading data for station {station_id}: {e}")
            station_results.append({
                "station_id": station_id,
                "error": str(e)
            })
            continue

    # Return data for all active stations
    return JsonResponse({
        "status": "success",
        "stations": station_results
    })


def read_pressure_data(station_id, valve_serial_no, filter_test_id,actual_time):
    """
    Read pressure data without inserting - for display purposes only.
    This function only queries the database and returns formatted data.
    """
    station_tables = {
        1: "current_status_station1",
        2: "current_status_station2",
        3: "current_status_station3",
        4: "current_status_station4"
    }
   
    table_name = station_tables.get(station_id)
    if not table_name:
        print(f"Error: No table defined for station {station_id}")
        return None, None, None, None, None
   
    try:
        with connection.cursor() as cursor:
            # ? Fetch full history
            cursor.execute(
                f"""
                SELECT PRESSURE, DATE_TIME
                FROM {table_name}
                WHERE VALVE_SERIAL_NO=%s AND STATION=%s AND TEST_ID=%s
                ORDER BY ID ASC
                """,
                [valve_serial_no, station_id, filter_test_id]
            )
            rows = cursor.fetchall()
            pressure_history = [float(r[0]) if r[0] is not None else 0.0 for r in rows]
            formatted_times = [r[1].strftime("%I:%M:%S") for r in rows]

            # ? Fetch greenline time (first 'on' timer event)
            cursor.execute(
                f"""
                SELECT DATE_TIME FROM {table_name}
                WHERE VALVE_SERIAL_NO=%s AND STATION=%s AND TEST_ID=%s AND TIMER_ON_OFF='on'
                ORDER BY ID ASC LIMIT 1
                """,
                [valve_serial_no, station_id, filter_test_id]
            )
            first_on_time_row = cursor.fetchone()
            greenlinetime = first_on_time_row[0].strftime("%I:%M:%S") if first_on_time_row else None
           
            # ? Fetch redline time (first 'off' timer event)
            cursor.execute(
                f"""
                SELECT DATE_TIME FROM {table_name}
                WHERE VALVE_SERIAL_NO=%s AND STATION=%s AND TEST_ID=%s AND TIMER_ON_OFF='off'
                ORDER BY ID ASC LIMIT 1
                """,
                [valve_serial_no, station_id, filter_test_id]
            )
            first_off_time_row = cursor.fetchone()
            redlinetime = first_off_time_row[0].strftime("%I:%M:%S") if first_off_time_row else None
           
            # ? Fetch latest result value
            cursor.execute(
                f"""
                SELECT RESULT
                FROM {table_name}
                WHERE VALVE_SERIAL_NO=%s AND STATION=%s AND TEST_ID=%s AND RESULT IS NOT NULL
                ORDER BY ID DESC
                LIMIT 1
                """,
                [valve_serial_no, station_id, filter_test_id]
            )
            result_row = cursor.fetchone()
            result_value = result_row[0] if result_row else None
           
            return pressure_history, formatted_times, greenlinetime, redlinetime, result_value, actual_time
           
    except Exception as e:
        print(f"Error in read_pressure_data: {e}")
        return None, None, None, None, None
# Start the background thread when module loads (ensures continuous data collection)
start_pressure_data_thread()

previous_timer = 0

def update_pressure_data(station_id, valve_serial_no, pressure, timer_status, test_id,actual_time, filter_test_id=None):
    """
    Update pressure data for a station.
    test_id: Used for inserting new records (hardware state)
    filter_test_id: Used for filtering pressure history (for page refresh with specific test selected)
    """
    global previous_timer_by_station
   
    # Use filter_test_id for history if provided, otherwise use test_id
    history_test_id = filter_test_id if filter_test_id is not None else test_id
   
    station_tables = {
        1: "current_status_station1",
        2: "current_status_station2",
        3: "current_status_station3",
        4: "current_status_station4"
            }
   

    with connection.cursor() as cursor:
        cursor.execute("SELECT TEST_NAME FROM temp_testing_data WHERE TEST_ID=%s", [test_id])
        test_name_result = cursor.fetchone()
        # print("testname",test_name_result)
        test_name = test_name_result[0] if test_name_result else None
        print("secondtest",test_name)

    table_name = station_tables.get(station_id)
    if not table_name:
        print(f"Error: No table defined for station {station_id}")
        return None, None  

    try:
        with connection.cursor() as cursor:
            # Timer logic per station
            TIMER_ON_OFF = 'normal'
            test_completed = None

            prev = previous_timer_by_station.get(station_id, 0)

            if timer_status == 1 and prev == 0:
                TIMER_ON_OFF = 'on'
            elif timer_status == 0 and prev == 1:
                TIMER_ON_OFF = 'off'

            # Update memory for this station
            previous_timer_by_station[station_id] = timer_status
            # Always keep test_id and test_name once provided (button click writes Modbus register),
            # so they are persisted even before timer turns ON/OFF.
            # No-op here; we intentionally do not null them based on timer state.
               
            # RESULT should be saved only when timer goes OFF; otherwise retrieve from database
            result_addresses = {1: 2011, 2: 2025, 3: 2026, 4: 2027}
            result_value = None
            if TIMER_ON_OFF == 'off':
                # When timer transitions from ON to OFF, read result from Modbus
                try:
                    res_addr = result_addresses.get(station_id)
                    if res_addr is not None:
                        res = TesleadSmartsyncx.read_holding_registers(res_addr, 1)
                        if res and hasattr(res, 'registers') and res.registers:
                            code = res.registers[0]
                            print('code',code)
                            if code == 1:
                                result_value = 'PASS'
                            elif code == 0:
                                result_value = 'FAIL'
                            else:
                                # Unknown code on OFF; leave as NULL
                                result_value = None
                except Exception as _:
                    result_value = None
            elif timer_status == 0:
                # Timer is OFF but not transitioning - retrieve latest result from database
                try:
                    cursor.execute(
                        f"""
                        SELECT RESULT
                        FROM {table_name}
                        WHERE VALVE_SERIAL_NO=%s AND STATION=%s AND TEST_ID=%s AND RESULT IS NOT NULL
                        ORDER BY ID DESC
                        LIMIT 1
                        """,
                        [valve_serial_no, station_id, history_test_id]
                    )
                    result_row = cursor.fetchone()
                    if result_row and result_row[0]:
                        result_value = result_row[0]
                        print('try block')
                except Exception as _:
                    result_value = None
                    print("this statement is running")

            # ? Insert record
            query = f"""
                INSERT INTO {table_name} (VALVE_SERIAL_NO, STATION, PRESSURE, TIMER_STATUS, TEST_ID, TEST_NAME, TIMER_ON_OFF, RESULT)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, [valve_serial_no, station_id, pressure, timer_status, test_id, test_name, TIMER_ON_OFF, result_value])
            connection.commit()

            # ?? Sync to pressure_analysis based on timer events per active station
            try:
                if TIMER_ON_OFF == 'on' and test_id is not None:
                    # Set start pressure and start time on the latest matching row (created on test button click)
                    cursor.execute(
                        """
                        UPDATE pressure_analysis
                        SET START_PRESSURE=%s, `START`=NOW()
                        WHERE TEST_ID=%s AND STATION_STATUS=%s AND `START` IS NULL
                        ORDER BY ID DESC
                        LIMIT 1
                        """,
                        [pressure, test_id, station_id]
                    )
                    cursor.execute(
                        """
                        UPDATE temp_pressure_analysis
                        SET START_PRESSURE=%s, `START`=NOW()
                        WHERE TEST_ID=%s AND STATION_STATUS=%s AND `START` IS NULL
                        ORDER BY ID DESC
                        LIMIT 1
                        """,
                        [pressure, test_id, station_id]
                    )
                elif TIMER_ON_OFF == 'off' and test_id is not None:
                    # On OFF, set result/final pressures, end time, valve status, and leak pressure
                    cursor.execute(
                        """
                        UPDATE pressure_analysis
                        SET RESULT_PRESSURE=%s,
                            ACTUAL_PRESSURE=%s,
                            `END`=NOW(),
                            VALVE_STATUS=%s,
                            LEAK_PRESSURE=CASE WHEN START_PRESSURE IS NOT NULL THEN START_PRESSURE - %s ELSE NULL END
                        WHERE TEST_ID=%s AND STATION_STATUS=%s AND `END` IS NULL
                        ORDER BY ID DESC
                        LIMIT 1
                        """,
                        [pressure, pressure, result_value, pressure, test_id, station_id]
                    )
                   
                    cursor.execute(
                        """
                        UPDATE temp_pressure_analysis
                        SET RESULT_PRESSURE=%s,
                            ACTUAL_PRESSURE=%s,
                            `END`=NOW(),
                            VALVE_STATUS=%s,
                            LEAK_PRESSURE=CASE WHEN START_PRESSURE IS NOT NULL THEN START_PRESSURE - %s ELSE NULL END
                        WHERE TEST_ID=%s AND STATION_STATUS=%s AND `END` IS NULL
                        ORDER BY ID DESC
                        LIMIT 1
                        """,
                        [pressure, pressure, result_value, pressure, test_id, station_id]
                    )
                connection.commit()
            except Exception as _:
                # Do not fail the main flow if pressure_analysis update has an issue
                pass

            # ? Fetch full history and convert times to 12-hour format
            # Use history_test_id to filter by the selected test (for page refresh)
            cursor.execute(
                f"""
                SELECT PRESSURE, DATE_TIME
                FROM {table_name}
                WHERE VALVE_SERIAL_NO=%s AND STATION=%s AND TEST_ID=%s
                ORDER BY ID ASC
                """,
                [valve_serial_no, station_id, history_test_id]
            )
            rows = cursor.fetchall()
            pressure_history = [float(r[0]) if r[0] is not None else 0.0 for r in rows]
            formatted_times = [r[1].strftime("%I:%M:%S") for r in rows]


            cursor.execute(f"SELECT DATE_TIME FROM {table_name} WHERE VALVE_SERIAL_NO=%s AND STATION=%s AND TEST_ID=%s AND TIMER_ON_OFF='on' ORDER BY ID ASC LIMIT 1", [valve_serial_no, station_id, history_test_id])
            first_on_time_row = cursor.fetchone()
            greenlinetime = first_on_time_row[0].strftime("%I:%M:%S") if first_on_time_row else None
            # print('greenline time',greenlinetime)
           
            # ? Fetch redline time (first 'off' timer event)
            cursor.execute(f"SELECT DATE_TIME FROM {table_name} WHERE VALVE_SERIAL_NO=%s AND STATION=%s AND TEST_ID=%s AND TIMER_ON_OFF='off' ORDER BY ID ASC LIMIT 1", [valve_serial_no, station_id, history_test_id])
            first_off_time_row = cursor.fetchone()
            redlinetime = first_off_time_row[0].strftime("%I:%M:%S") if first_off_time_row else None
            # print('redline time',redlinetime)
           
            # ? Return arrays, greenline time, redline time, and actual_time
            return pressure_history, formatted_times, greenlinetime, redlinetime, result_value, actual_time

    except Exception as e:
        print(f"Error in update_pressure_data: {e}")
        return None, None, None, None, None, None  # ? Return Nones on error to match caller unpacking


@csrf_exempt
@login_required
def mark_test_completed(request):
    try:
        if request.method != 'POST':
            return JsonResponse({"status": "error", "message": "POST required"}, status=405)
        test_id = request.POST.get('test_id')
        if not test_id:
            return JsonResponse({"status": "error", "message": "test_id is required"}, status=400)

        tables = [
            'current_status_station1',
            'current_status_station2',
            'current_status_station3',
            'current_status_station4'
            
        ]
        with connection.cursor() as cursor:
            for t in tables:
                cursor.execute(f"UPDATE {t} SET CYCLE_COMPLETE=%s WHERE TEST_ID=%s and TIMER_ON_OFF=%s", [1, test_id,'off'])
            connection.commit()
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@login_required
def get_completed_tests(request):
    try:
        tables = [
            'current_status_station1',
            'current_status_station2',
            'current_status_station3',
            'current_status_station4'
        ]
        completed_ids = set()
        with connection.cursor() as cursor:
            for t in tables:
                cursor.execute(f"SELECT DISTINCT TEST_ID FROM {t} WHERE CYCLE_COMPLETE=%s", [1])
                rows = cursor.fetchall()
                for r in rows:
                    if r and r[0] is not None:
                        completed_ids.add(int(r[0]))
        return JsonResponse({"status": "success", "completed_test_ids": list(completed_ids)})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@csrf_exempt
@login_required
def reset_test_data(request):
    try:
        if request.method != 'POST':
            return JsonResponse({"status": "error", "message": "POST required"}, status=405)
        test_id = request.POST.get('test_id')
        active_serial_no = request.POST.get('active_serial_no')
        
        if not test_id or not active_serial_no:
            return JsonResponse({"status": "error", "message": "test_id is required"}, status=400)

        tables = [
            'current_status_station1',
            'current_status_station2',
            'current_status_station3',
            'current_status_station4'
        ]
        with connection.cursor() as cursor:
            for t in tables:
                cursor.execute(f"DELETE FROM {t} WHERE TEST_ID=%s", [test_id])

            # Also reset existing pressure_analysis rows for this test to reuse same row
            # Clear timing and result-related fields; keep metadata and COL values
            cursor.execute(
                """
                UPDATE pressure_analysis
                SET `START`=NULL,
                    `END`=NULL,
                    START_PRESSURE=NULL,
                    RESULT_PRESSURE=NULL,
                    LEAK_PRESSURE=NULL,
                    VALVE_STATUS=NULL,
                    STATUS=NULL,
                    CYCLE_START=NULL,
                    CYCLE_END=NULL,
                    ACTUAL_PRESSURE=NULL,
                    ACTUAL_TIME=NULL
                WHERE TEST_ID=%s
                """,
                [test_id]
            )
            cursor.execute(
                """
                UPDATE temp_pressure_analysis
                SET `START`=NULL,
                    `END`=NULL,
                    START_PRESSURE=NULL,
                    RESULT_PRESSURE=NULL,
                    LEAK_PRESSURE=NULL,
                    VALVE_STATUS=NULL,
                    STATUS=NULL,
                    CYCLE_START=NULL,
                    CYCLE_END=NULL,
                    ACTUAL_PRESSURE=NULL,
                    ACTUAL_TIME=NULL
                WHERE TEST_ID=%s
                """,
                [test_id]
            )
            
            
            # Set all other tests to STATUS=0 (deactivate them)
            cursor.execute("UPDATE pressure_analysis SET STATUS = 0 WHERE STATUS = 1")
            
            # Set the reset test to STATUS=1 (mark it as active)
            cursor.execute(
                "UPDATE pressure_analysis SET STATUS = 1 WHERE TEST_ID = %s AND VALVE_SER_NO = %s", 
                [test_id, active_serial_no]
            )
            
            
            connection.commit()
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@csrf_exempt
@login_required
def insert_pressure_analysis(request):
    try:
        if request.method != 'POST':
            return JsonResponse({"status": "error", "message": "POST required"}, status=405)

        test_id = request.POST.get('test_id')
        if not test_id:
            return JsonResponse({"status": "error", "message": "test_id is required"}, status=400)

        with connection.cursor() as cursor:
            # 🔹 Fetch all active stations
            cursor.execute("""
                SELECT ID, VALVE_SER_NO, PRESSURE_UNIT, STANDARD_NAME, SIZE_NAME, CLASS_NAME,
                       TYPE_NAME, SHELL_MATERIAL_NAME,
                       COL1_NAME,COL1_VALUE,COL2_NAME,COL2_VALUE,COL3_NAME,COL3_VALUE,COL4_NAME,COL4_VALUE,
                       COL5_NAME,COL5_VALUE,COL6_NAME,COL6_VALUE,COL7_NAME,COL7_VALUE,COL8_NAME,COL8_VALUE,
                       COL9_NAME,COL9_VALUE,COL10_NAME,COL10_VALUE,COL11_NAME,COL11_VALUE,COL12_NAME,COL12_VALUE,
                       COL13_NAME,COL13_VALUE,COL14_NAME,COL14_VALUE,COL15_NAME,COL15_VALUE,
                       COL16_NAME,COL16_VALUE,COL17_NAME,COL17_VALUE,COL18_NAME,COL18_VALUE,
                       COL19_NAME,COL19_VALUE,COL20_NAME,COL20_VALUE,COL21_NAME,COL21_VALUE,
                       COL22_NAME,COL22_VALUE,COL23_NAME,COL23_VALUE,COL24_NAME,COL24_VALUE
                FROM master_temp_data
                WHERE STATION_STATUS=%s
            """, [1])
            active_rows = cursor.fetchall()

            if not active_rows:
                return JsonResponse({"status": "error", "message": "No active stations found"}, status=404)

            # 🔹 Get test info
            cursor.execute("""
                SELECT TEST_ID, TEST_NAME, TESTING_PR_UNIT, TESTING_PR_BAR, TESTING_PR_PSI,
                       TESTING_PR_KGCM2, TESTING_DUR_SEC
                FROM temp_testing_data
                WHERE TEST_ID=%s
            """, [test_id])
            trow = cursor.fetchone()

            if not trow:
                return JsonResponse({"status": "error", "message": "Test not found"}, status=404)

            _tid, test_name, testing_unit, testing_pr_bar, testing_pr_psi, testing_pr_kgcm2, testing_dur_sec = trow

            testing_unit = (testing_unit or '').lower()
            set_pressure = (
                testing_pr_bar if testing_unit == 'bar'
                else testing_pr_kgcm2 if testing_unit in ['kg/cm2', 'kg/cm²']
                else testing_pr_psi if testing_unit == 'psi'
                else testing_pr_bar
            )
            set_time = testing_dur_sec
            set_time_unit = 'sec'

            # 🔹 Check if this is a cavity relief test and read connector values
            is_cavity_test = test_name and 'cavity relief' in test_name.lower()
            connector_values = {}
            if is_cavity_test:
                try:
                    s1_connector_l_raw = TesleadSmartsyncx.read_holding_registers(2203, 1).registers[0]
                    s1_connector_r_raw = TesleadSmartsyncx.read_holding_registers(2204, 1).registers[0]
                    s2_connector_l_raw = TesleadSmartsyncx.read_holding_registers(2205, 1).registers[0]
                    s2_connector_r_raw = TesleadSmartsyncx.read_holding_registers(2206, 1).registers[0]
                    connector_values = {
                        'COL31_NAME': 's1_connector_l_raw',
                        'COL31_VALUE': str(s1_connector_l_raw),
                        'COL32_NAME': 's1_connector_r_raw',
                        'COL32_VALUE': str(s1_connector_r_raw),
                        'COL33_NAME': 's2_connector_l_raw',
                        'COL33_VALUE': str(s2_connector_l_raw),
                        'COL34_NAME': 's2_connector_r_raw',
                        'COL34_VALUE': str(s2_connector_r_raw),
                    }
                except Exception as e:
                    print(f"Error reading cavity connector values: {e}")
                    connector_values = {
                        'COL31_NAME': 's1_connector_l_raw',
                        'COL31_VALUE': '0',
                        'COL32_NAME': 's1_connector_r_raw',
                        'COL32_VALUE': '0',
                        'COL33_NAME': 's2_connector_l_raw',
                        'COL33_VALUE': '0',
                        'COL34_NAME': 's2_connector_r_raw',
                        'COL34_VALUE': '0',
                    }

            # 🔹 Get latest shift name from shift table
            cursor.execute("""
                SELECT SHIFT_NAME 
                FROM shift 
                ORDER BY ID DESC 
                LIMIT 1
            """)
            shift_row = cursor.fetchone()
            shift_name = shift_row[0] if shift_row else None

            inserted, updated = 0, 0

            for row in active_rows:
                (
                    station_id, valve_ser_no, pressure_unit_master, standard_name, size_name,
                    class_name, type_name, shell_material_name, *col_pairs
                ) = row

                # 🔸 Check existing record for this test & station
                cursor.execute("""
                    SELECT ID, CYCLE_COMPLETE, COUNT_ID
                    FROM pressure_analysis
                    WHERE TEST_ID=%s AND STATION_STATUS=%s
                    ORDER BY ID DESC LIMIT 1
                """, [_tid, station_id])
                existing = cursor.fetchone()

                current_count_id = None  # Track the COUNT_ID for this operation
                should_update_gauge = False  # Flag to determine if we should update pressure_gauge_analysis

                if existing:
                    pa_id, cycle_complete, count_id = existing
                    current_count_id = count_id

                    # --- CASE 1: exists but cycle not complete → UPDATE
                    if not cycle_complete:
                        # Build connector columns for cavity test
                        connector_cols = ""
                        connector_params = []
                        if is_cavity_test:
                            connector_cols = ", " + ", ".join([f"{k}=%s" for k in ['COL31_NAME', 'COL31_VALUE', 'COL32_NAME', 'COL32_VALUE', 'COL33_NAME', 'COL33_VALUE', 'COL34_NAME', 'COL34_VALUE']])
                            connector_params = [connector_values['COL31_NAME'], connector_values['COL31_VALUE'],
                                               connector_values['COL32_NAME'], connector_values['COL32_VALUE'],
                                               connector_values['COL33_NAME'], connector_values['COL33_VALUE'],
                                               connector_values['COL34_NAME'], connector_values['COL34_VALUE']]
                        
                        update_sql = """
                            UPDATE pressure_analysis
                            SET VALVE_SER_NO=%s, TEST_NAME=%s, SET_PRESSURE=%s, PRESSURE_UNIT=%s,
                                SET_TIME=%s, SET_TIME_UNIT=%s, STANDARD_NAME=%s, VALVESIZE_NAME=%s,
                                VALVETYPE_NAME=%s, VALVECLASS_NAME=%s, SHELLMATERIAL_NAME=%s,
                                DATE_TIME=NOW(),
                        """ + ", ".join([f"COL{i}_NAME=%s, COL{i}_VALUE=%s" for i in range(1, 25)]) + connector_cols + """
                            WHERE ID=%s
                        """
                        params = [
                            valve_ser_no, test_name, set_pressure, (testing_unit or pressure_unit_master),
                            set_time, set_time_unit, standard_name, size_name, type_name,
                            class_name, shell_material_name,
                        ] + list(col_pairs) + connector_params + [pa_id]
                       
                        cursor.execute(update_sql, params)
                        # Ensure STATUS=1 for updated test
                        cursor.execute("UPDATE pressure_analysis SET STATUS = 1 WHERE ID = %s", [pa_id])
                        updated += 1
                        should_update_gauge = True  # Mark for gauge update

                        # 🆕 Insert into temp_pressure_analysis when updating
                        connector_cols_temp = ""
                        connector_params_temp = []
                        if is_cavity_test:
                            connector_cols_temp = ", " + ",".join(['COL31_NAME', 'COL31_VALUE', 'COL32_NAME', 'COL32_VALUE', 'COL33_NAME', 'COL33_VALUE', 'COL34_NAME', 'COL34_VALUE'])
                            connector_params_temp = [connector_values['COL31_NAME'], connector_values['COL31_VALUE'],
                                                    connector_values['COL32_NAME'], connector_values['COL32_VALUE'],
                                                    connector_values['COL33_NAME'], connector_values['COL33_VALUE'],
                                                    connector_values['COL34_NAME'], connector_values['COL34_VALUE']]
                        
                        insert_temp_sql = """
                            INSERT INTO temp_pressure_analysis (
                                VALVE_SER_NO, TEST_ID, TEST_NAME,
                                SET_PRESSURE, ACTUAL_PRESSURE, PRESSURE_UNIT,
                                SET_TIME, ACTUAL_TIME, SET_TIME_UNIT,
                                STANDARD_NAME, VALVESIZE_NAME, VALVETYPE_NAME,
                                VALVECLASS_NAME, SHELLMATERIAL_NAME,
                                STATION_STATUS, DATE_TIME, STATUS, COUNT_ID,
                        """ + ",".join([f"COL{i}_NAME, COL{i}_VALUE" for i in range(1, 25)]) + connector_cols_temp + """
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), 1, %s,
                        """ + ",".join(["%s, %s" for _ in range(1, 25)]) + (", " + ",".join(["%s" for _ in range(8)]) if is_cavity_test else "") + """
                            )
                        """
                        temp_params = [
                            valve_ser_no, _tid, test_name,
                            set_pressure, set_pressure,  # ACTUAL_PRESSURE = SET_PRESSURE initially
                            (testing_unit or pressure_unit_master),
                            set_time, 0,  # ACTUAL_TIME = 0 at start
                            set_time_unit,
                            standard_name, size_name, type_name,
                            class_name, shell_material_name,
                            station_id, count_id
                        ] + list(col_pairs) + connector_params_temp
                       
                        cursor.execute(insert_temp_sql, temp_params)

                    else:
                        # --- CASE 2: exists and cycle complete = 'Yes' → INSERT new record
                        cursor.execute("""
                            SELECT COUNT_ID
                            FROM pressure_analysis
                            WHERE VALVE_SER_NO=%s AND CYCLE_COMPLETE='Yes'
                            ORDER BY COUNT_ID DESC LIMIT 1
                        """, [valve_ser_no])
                        last_completed = cursor.fetchone()

                        if last_completed:
                            new_count_id = last_completed[0] + 1
                        else:
                            cursor.execute("""
                                SELECT COUNT_ID
                                FROM pressure_analysis
                                WHERE VALVE_SER_NO=%s
                                ORDER BY COUNT_ID DESC LIMIT 1
                            """, [valve_ser_no])
                            any_test = cursor.fetchone()
                            new_count_id = any_test[0] if any_test else 1

                        current_count_id = new_count_id

                        # Build connector columns for cavity test
                        connector_cols_insert = ""
                        connector_params_insert = []
                        if is_cavity_test:
                            connector_cols_insert = "," + ",".join(['COL31_NAME', 'COL31_VALUE', 'COL32_NAME', 'COL32_VALUE', 'COL33_NAME', 'COL33_VALUE', 'COL34_NAME', 'COL34_VALUE'])
                            connector_params_insert = [connector_values['COL31_NAME'], connector_values['COL31_VALUE'],
                                                      connector_values['COL32_NAME'], connector_values['COL32_VALUE'],
                                                      connector_values['COL33_NAME'], connector_values['COL33_VALUE'],
                                                      connector_values['COL34_NAME'], connector_values['COL34_VALUE']]
                        
                        insert_query = """
                            INSERT INTO pressure_analysis (
                                VALVE_SER_NO, TEST_ID, TEST_NAME, SET_PRESSURE, PRESSURE_UNIT,
                                SET_TIME, SET_TIME_UNIT, STANDARD_NAME, VALVESIZE_NAME,
                                VALVETYPE_NAME, VALVECLASS_NAME, SHELLMATERIAL_NAME,
                                STATION_STATUS, DATE_TIME,
                        """ + ",".join([f"COL{i}_NAME,COL{i}_VALUE" for i in range(1, 25)]) + connector_cols_insert + """,
                                STATUS, COUNT_ID
                            ) VALUES (
                                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),
                        """ + ",".join(["%s,%s" for _ in range(1, 25)]) + ("," + ",".join(["%s,%s" for _ in range(4)]) if is_cavity_test else "") + """,
                                1,%s
                            )
                        """
                        params = [
                            valve_ser_no, _tid, test_name, set_pressure,
                            (testing_unit or pressure_unit_master),
                            set_time, set_time_unit, standard_name, size_name,
                            type_name, class_name, shell_material_name, station_id
                        ] + list(col_pairs) + connector_params_insert + [new_count_id]
                       
                        cursor.execute(insert_query, params)
                        inserted += 1
                        should_update_gauge = True  # Mark for gauge update

                        # 🆕 Insert into temp_pressure_analysis for new record
                        connector_cols_temp2 = ""
                        connector_params_temp2 = []
                        if is_cavity_test:
                            connector_cols_temp2 = ", " + ",".join(['COL31_NAME', 'COL31_VALUE', 'COL32_NAME', 'COL32_VALUE', 'COL33_NAME', 'COL33_VALUE', 'COL34_NAME', 'COL34_VALUE'])
                            connector_params_temp2 = [connector_values['COL31_NAME'], connector_values['COL31_VALUE'],
                                                      connector_values['COL32_NAME'], connector_values['COL32_VALUE'],
                                                      connector_values['COL33_NAME'], connector_values['COL33_VALUE'],
                                                      connector_values['COL34_NAME'], connector_values['COL34_VALUE']]
                        
                        insert_temp_sql = """
                            INSERT INTO temp_pressure_analysis (
                                VALVE_SER_NO, TEST_ID, TEST_NAME,
                                SET_PRESSURE, ACTUAL_PRESSURE, PRESSURE_UNIT,
                                SET_TIME, ACTUAL_TIME, SET_TIME_UNIT,
                                STANDARD_NAME, VALVESIZE_NAME, VALVETYPE_NAME,
                                VALVECLASS_NAME, SHELLMATERIAL_NAME,
                                STATION_STATUS, DATE_TIME, STATUS, COUNT_ID,
                        """ + ",".join([f"COL{i}_NAME, COL{i}_VALUE" for i in range(1, 25)]) + connector_cols_temp2 + """
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), 1, %s,
                        """ + ",".join(["%s, %s" for _ in range(1, 25)]) + (", " + ",".join(["%s" for _ in range(8)]) if is_cavity_test else "") + """
                            )
                        """
                        temp_params = [
                            valve_ser_no, _tid, test_name,
                            set_pressure, set_pressure,
                            (testing_unit or pressure_unit_master),
                            set_time, 0, set_time_unit,
                            standard_name, size_name, type_name,
                            class_name, shell_material_name,
                            station_id, new_count_id
                        ] + list(col_pairs) + connector_params_temp2
                       
                        cursor.execute(insert_temp_sql, temp_params)

                else:
                    # --- CASE 3: No record at all → INSERT new
                    cursor.execute("""
                        SELECT COUNT_ID
                        FROM pressure_analysis
                        WHERE VALVE_SER_NO=%s AND CYCLE_COMPLETE='Yes' AND COUNT_ID > 0
                        ORDER BY COUNT_ID DESC LIMIT 1
                    """, [valve_ser_no])
                    last_completed = cursor.fetchone()
                    new_count_id = (last_completed[0] + 1) if last_completed else 1
                    current_count_id = new_count_id

                    # Build connector columns for cavity test
                    connector_cols_insert3 = ""
                    connector_params_insert3 = []
                    if is_cavity_test:
                        connector_cols_insert3 = "," + ",".join(['COL31_NAME', 'COL31_VALUE', 'COL32_NAME', 'COL32_VALUE', 'COL33_NAME', 'COL33_VALUE', 'COL34_NAME', 'COL34_VALUE'])
                        connector_params_insert3 = [connector_values['COL31_NAME'], connector_values['COL31_VALUE'],
                                                    connector_values['COL32_NAME'], connector_values['COL32_VALUE'],
                                                    connector_values['COL33_NAME'], connector_values['COL33_VALUE'],
                                                    connector_values['COL34_NAME'], connector_values['COL34_VALUE']]
                    
                    insert_query = """
                        INSERT INTO pressure_analysis (
                            VALVE_SER_NO, TEST_ID, TEST_NAME, SET_PRESSURE, PRESSURE_UNIT,
                            SET_TIME, SET_TIME_UNIT, STANDARD_NAME, VALVESIZE_NAME,
                            VALVETYPE_NAME, VALVECLASS_NAME, SHELLMATERIAL_NAME,
                            STATION_STATUS, DATE_TIME,
                    """ + ",".join([f"COL{i}_NAME,COL{i}_VALUE" for i in range(1, 25)]) + connector_cols_insert3 + """,
                            STATUS, COUNT_ID
                        ) VALUES (
                            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),
                    """ + ",".join(["%s,%s" for _ in range(1, 25)]) + ("," + ",".join(["%s,%s" for _ in range(4)]) if is_cavity_test else "") + """,
                            1,%s
                        )
                    """
                    params = [
                        valve_ser_no, _tid, test_name, set_pressure,
                        (testing_unit or pressure_unit_master),
                        set_time, set_time_unit, standard_name, size_name,
                        type_name, class_name, shell_material_name, station_id
                    ] + list(col_pairs) + connector_params_insert3 + [new_count_id]
                   
                    cursor.execute(insert_query, params)
                    inserted += 1
                    should_update_gauge = True  # Mark for gauge update

                    # 🆕 Insert into temp_pressure_analysis for new record
                    connector_cols_temp3 = ""
                    connector_params_temp3 = []
                    if is_cavity_test:
                        connector_cols_temp3 = ", " + ",".join(['COL31_NAME', 'COL31_VALUE', 'COL32_NAME', 'COL32_VALUE', 'COL33_NAME', 'COL33_VALUE', 'COL34_NAME', 'COL34_VALUE'])
                        connector_params_temp3 = [connector_values['COL31_NAME'], connector_values['COL31_VALUE'],
                                                  connector_values['COL32_NAME'], connector_values['COL32_VALUE'],
                                                  connector_values['COL33_NAME'], connector_values['COL33_VALUE'],
                                                  connector_values['COL34_NAME'], connector_values['COL34_VALUE']]
                    
                    insert_temp_sql = """
                        INSERT INTO temp_pressure_analysis (
                            VALVE_SER_NO, TEST_ID, TEST_NAME,
                            SET_PRESSURE, ACTUAL_PRESSURE, PRESSURE_UNIT,
                            SET_TIME, ACTUAL_TIME, SET_TIME_UNIT,
                            STANDARD_NAME, VALVESIZE_NAME, VALVETYPE_NAME,
                            VALVECLASS_NAME, SHELLMATERIAL_NAME,
                            STATION_STATUS, DATE_TIME, STATUS, COUNT_ID,
                    """ + ",".join([f"COL{i}_NAME, COL{i}_VALUE" for i in range(1, 25)]) + connector_cols_temp3 + """
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), 1, %s,
                    """ + ",".join(["%s, %s" for _ in range(1, 25)]) + (", " + ",".join(["%s" for _ in range(8)]) if is_cavity_test else "") + """
                        )
                    """
                    temp_params = [
                        valve_ser_no, _tid, test_name,
                        set_pressure, set_pressure,
                        (testing_unit or pressure_unit_master),
                        set_time, 0, set_time_unit,
                        standard_name, size_name, type_name,
                        class_name, shell_material_name,
                        station_id, new_count_id
                    ] + list(col_pairs) + connector_params_temp3
                   
                    cursor.execute(insert_temp_sql, temp_params)

                # 🆕 CRITICAL: Only update COUNT_ID and SHIFT if they are NULL/empty
                if should_update_gauge and current_count_id is not None:
                    # Check if COUNT_ID and SHIFT are already set for this valve
                    cursor.execute("""
                        SELECT COUNT_ID, SHIFT 
                        FROM pressure_gauge_analysis 
                        WHERE VALVE_SER_NO = %s AND STATION_ID = %s
                        ORDER BY ID DESC LIMIT 1
                    """, [valve_ser_no, station_id])
                    existing_gauge = cursor.fetchone()
                    
                    if existing_gauge:
                        existing_count_id = existing_gauge[0]
                        existing_shift = existing_gauge[1]
                        
                        # Only update if COUNT_ID or SHIFT is NULL/empty
                        if existing_count_id is None or existing_shift is None:
                            cursor.execute("""
                                UPDATE pressure_gauge_analysis 
                                SET COUNT_ID = %s, SHIFT = %s 
                                WHERE VALVE_SER_NO = %s AND STATION_ID = %s 
                                AND (COUNT_ID IS NULL OR SHIFT IS NULL)
                            """, [current_count_id, shift_name, valve_ser_no, station_id])
                            print(f"✅ Updated NULL COUNT_ID/SHIFT → COUNT_ID={current_count_id}, SHIFT={shift_name} for valve {valve_ser_no} in station {station_id}")
                        else:
                            print(f"⏭️ Skipped update - COUNT_ID={existing_count_id}, SHIFT={existing_shift} already exist for valve {valve_ser_no} in station {station_id}")
                    else:
                        print(f"⚠️ No gauge records found for valve {valve_ser_no} in station {station_id}")

            # 🔹 Deactivate all other tests and activate only the selected test
            cursor.execute("UPDATE pressure_analysis SET STATUS = 0 WHERE STATUS = 1 AND TEST_ID != %s", [_tid])
            cursor.execute("UPDATE pressure_analysis SET STATUS = 1 WHERE TEST_ID = %s", [_tid])
            
            connection.commit()

            return JsonResponse({
                "status": "success",
                "inserted": inserted,
                "updated": updated
            })

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


import csv
import io
import base64



@csrf_exempt
def export_current_status_csv(request):
    try:
        if request.method != 'POST':
            return JsonResponse({"status": "error", "message": "POST required"}, status=405)

        tables = [
            'current_status_station1',
            'current_status_station2',
            'current_status_station3',
            'current_status_station4'         
        ]
        with connection.cursor() as cursor:
            cursor.execute("select PRESSURE_UNIT from temp_pressure_analysis")
            pressure_unit = cursor.fetchone()[0]

        # Resolve Desktop path (Windows/Linux/Mac)
        target_folder = r'D:\LNT_Reports'
        csv_folder = os.path.join(target_folder, 'csv_Reports')
        images_folder = os.path.join(target_folder, 'Graphs')
        # os.makedirs(target_folder, exist_ok=True)
        os.makedirs(csv_folder, exist_ok=True)
        os.makedirs(images_folder, exist_ok=True)
        ts = datetime.now().strftime('%Y%m%d_%H%M')

        saved_files = []
        saved_images = []
        with connection.cursor() as cursor:
            for t in tables:
                # Get distinct serial numbers in this table
                cursor.execute(f"SELECT DISTINCT VALVE_SERIAL_NO FROM {t}")
                serial_rows = cursor.fetchall()
                serials = [r[0] for r in serial_rows if r and r[0] is not None]

                for serial in serials:
                    # Fetch all rows for this serial
                    cursor.execute(f"SELECT * FROM {t} WHERE VALVE_SERIAL_NO=%s ORDER BY ID ASC", [serial])
                    rows = cursor.fetchall()
                    headers = [col[0] for col in cursor.description]
                    

                    # Build filename as <serial>_station<no>.csv based on table name
                    # Get the COUNT_ID from the pressure_analysis table based on serial number
                    cursor.execute(
                        "SELECT COUNT_ID FROM pressure_analysis WHERE VALVE_SER_NO=%s ORDER BY ID DESC LIMIT 1",
                        [serial]
                    )
                    count_row = cursor.fetchone()
                    count = count_row[0] if count_row and count_row[0] is not None else 1
                   
                    try:
                        station_no = ''.join([ch for ch in t if ch.isdigit()]) or 'unknown'
                    except Exception:
                        station_no = 'unknown'
                    base_name = f"{serial}_station{station_no}_count{count}.csv"
                    filepath = os.path.join(csv_folder, base_name)

                    with open(filepath, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        # Write header with S.No first
                        writer.writerow(['S.No'] + headers)
                        for idx, row in enumerate(rows, start=1):
                            writer.writerow([idx] + list(row))

                    saved_files.append(filepath)

                    # Also build graphs per TEST_NAME for this serial - READ FROM CSV
                    try:
                        import matplotlib
                        matplotlib.use('Agg')  # Headless backend to avoid Tk/TkAgg
                        from matplotlib import pyplot as plt
                        import matplotlib.dates as mdates
                        from datetime import datetime as dt
                    except Exception:
                        # If matplotlib is not available, skip graph generation
                        continue

                    # Read data from the CSV file we just created
                    tests = {}
                    try:
                        with open(filepath, 'r', encoding='utf-8') as csvfile:
                            csv_reader = csv.DictReader(csvfile)
                            for row in csv_reader:
                                test_id_val = row.get('TEST_ID')
                                test_name = row.get('TEST_NAME')
                                dt_str = row.get('DATE_TIME')
                                pressure_val = row.get('PRESSURE')
                                timer_status_val = row.get('TIMER_STATUS')
                                onoff = row.get('TIMER_ON_OFF', '')
                                
                                # Skip rows without test info
                                if not test_id_val and not test_name:
                                    continue
                                
                                # Parse datetime
                                try:
                                    dt_val = dt.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
                                except Exception:
                                    try:
                                        dt_val = dt.fromisoformat(dt_str)
                                    except Exception:
                                        continue
                                
                                # Parse pressure
                                try:
                                    pressure_float = float(pressure_val or 0.0)
                                except Exception:
                                    pressure_float = 0.0
                                
                                # Parse timer status
                                try:
                                    timer_status_int = int(timer_status_val or 0)
                                except Exception:
                                    timer_status_int = 0
                                
                                # Group by TEST_ID (fallback to TEST_NAME if TEST_ID is None/empty)
                                key = test_id_val if test_id_val else (test_name or 'UNKNOWN_TEST')
                                tests.setdefault((key, test_name), []).append((dt_val, pressure_float, timer_status_int, (onoff or '').lower()))
                    except Exception as csv_err:
                        # If CSV reading fails, skip graph generation for this file
                        continue

                    for (test_key, test_name), series in tests.items():
                        if not series:
                            continue
                        times = [r[0] for r in series]
                        pressures = [r[1] for r in series]
                        timer_states = [r[2] for r in series]
                        onoff_states = [r[3] for r in series]

                        # Determine all ON/OFF transitions for this test
                        # 1) Prefer edge detection on TIMER_STATUS (0->1 is ON, 1->0 is OFF)
                        on_indices = []
                        off_indices = []
                        try:
                            for i in range(1, len(timer_states)):
                                prev_s = int(timer_states[i - 1])
                                cur_s = int(timer_states[i])
                                if prev_s == 0 and cur_s == 1:
                                    on_indices.append(i)
                                elif prev_s == 1 and cur_s == 0:
                                    off_indices.append(i)
                        except Exception:
                            # Best-effort; ignore if conversion fails
                            pass

                        # 2) Also include any explicit TIMER_ON_OFF markers if present in data
                        try:
                            for i in range(len(onoff_states)):
                                st = (onoff_states[i] or '').lower()
                                if st == 'on' and i not in on_indices:
                                    on_indices.append(i)
                                elif st == 'off' and i not in off_indices:
                                    off_indices.append(i)
                        except Exception:
                            pass

                        # Skip generating graph if there are no ON or OFF transitions at all
                        if not on_indices and not off_indices:
                            continue

                        # Get station number from table name for color selection
                        station_num = 1
                        try:
                            station_num = int(''.join([ch for ch in t if ch.isdigit()]) or '1')
                        except Exception:
                            station_num = 1

                        # Station colors matching frontend
                        station_colors = {
                            1: (75/255, 192/255, 192/255),    # Teal
                            2: (255/255, 99/255, 132/255),    # Red
                         
                        }
                        line_color = station_colors.get(station_num, (75/255, 192/255, 192/255))

                        # Plot with dark background matching frontend
                        plt.figure(figsize=(8, 3), facecolor='white')
                        ax = plt.gca()
                        ax.set_facecolor('white')
                       
                        # Plot line with station-specific color (no label to hide legend)
                        plt.plot(times, pressures, color=line_color, linewidth=2, marker='', markersize=0)
                       
                        # Style matching frontend
                        plt.title(f'{serial} - {test_name}', color='black', fontsize=4, fontweight='bold')
                        plt.xlabel('Time', color='black', fontsize=10)
                        plt.ylabel(f'Pressure({pressure_unit})', color='black', fontsize=10)
                       
                        # Grid with light white color (matching frontend rgba(255,255,255,0.1))
                        ax.grid(True, color='black', alpha=0.1, linestyle='-', linewidth=0.5)
                        ax.set_axisbelow(True)  # Grid behind plot
                       
                        # Format x-axis time as %I:%M (without seconds)
                        ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M'))
                        plt.xticks(rotation=45, ha='right', color='black', fontsize=9)
                        plt.yticks(color='black', fontsize=9)
                       
                        # Style axis spines to match dark theme
                        for spine in ax.spines.values():
                            spine.set_color('black')
                            spine.set_alpha(0.3)
                        # Set Y-axis max based on actual pressure data with 20% headroom
                        if pressures:
                            max_actual_pressure = max(pressures)
                            if max_actual_pressure > 0:
                                ax.set_ylim(bottom=0, top=max_actual_pressure * 1.2)
                            else:
                                ax.set_ylim(bottom=0)
                        else:
                            ax.set_ylim(bottom=0)
                       
                        # Set X-axis limits to extend slightly beyond data to connect with chart borders
                        if times:
                            time_min = min(times)
                            time_max = max(times)
                            time_range = time_max - time_min
                            # Add small padding (2% of range) to both sides to connect with borders
                            padding = time_range * 0.01 if time_range.total_seconds() > 0 else timedelta(seconds=1)
                            ax.set_xlim(left=time_min - padding, right=time_max + padding)

                        # Prepare helpers for label placement on vertical lines
                        yl = ax.get_ylim()
                        try:
                            yrange = (yl[1] - yl[0]) if isinstance(yl, tuple) else None
                        except Exception:
                            yrange = None
                        def local_value(idx):
                            try:
                                return pressures[idx]
                            except Exception:
                                try:
                                    return yl[0] + 0.9 * (yl[1] - yl[0])
                                except Exception:
                                    return 0

                        # Draw only the FIRST ON transition (green) and FIRST OFF transition (red)
                        # Get first ON and OFF indices
                        first_on_idx = None
                        first_off_idx = None
                        
                        if on_indices:
                            first_on_idx = min(on_indices)
                        if off_indices:
                            first_off_idx = min(off_indices)
                        
                        # Draw first ON line (green)
                        if first_on_idx is not None and first_on_idx < len(times):
                            dtv = times[first_on_idx]
                            plt.axvline(dtv, color='#00ff00', linestyle='-', linewidth=2)
                            try:
                                y_here = local_value(first_on_idx)
                                y_here = y_here + (0.02 * yrange if yrange else 0)
                                time_str = dtv.strftime('%I:%M')
                                plt.text(dtv, y_here, f"{time_str} - Start", color="#155715", rotation=90,
                                         va='top', ha='right', fontsize=8, fontweight='bold')
                            except Exception:
                                pass

                        # Draw first OFF line (red)
                        if first_off_idx is not None and first_off_idx < len(times):
                            dtv = times[first_off_idx]
                            plt.axvline(dtv, color='red', linestyle='-', linewidth=2)
                            try:
                                y_here_off = local_value(first_off_idx)
                                y_here_off = y_here_off + (0.02 * yrange if yrange else 0)
                                time_str = dtv.strftime('%I:%M')
                                plt.text(dtv, y_here_off, f"{time_str} - End", color='red', rotation=90,
                                         va='top', ha='right', fontsize=8, fontweight='bold')
                            except Exception:
                                pass

                        # No legend (removed as per user request)
                        plt.tight_layout()
                        # Sanitize filename
                        safe_test = ''.join(c for c in str(test_name) if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
                        img_path = os.path.join(images_folder, f"{serial}_{safe_test}_count{count}.png")

                        try:
                            # Save with dark background preserved
                            plt.savefig(img_path, dpi=150, facecolor='white', edgecolor='none', bbox_inches='tight')
                            saved_images.append(img_path)
                        finally:
                            plt.close()

                   

        return JsonResponse({
            "status": "success",
            "folder": target_folder,
            "files": saved_files,
            "images": saved_images,
            "images_folder": images_folder
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)







@login_required
def merged_report(request):
    return render(request, 'report.html')


@login_required
def download_merged_pdf(request):
    try:
        # Determine completed tests
        tables = [
            'current_status_station1',
            'current_status_station2',
            'current_status_station3',
            'current_status_station4'
        ]
        completed = set()
        with connection.cursor() as cursor:
            for t in tables:
                try:
                    cursor.execute(f"SELECT DISTINCT TEST_ID FROM {t} WHERE CYCLE_COMPLETE=%s", [1])
                    completed.update([r[0] for r in cursor.fetchall() if r and r[0] is not None])
                except Exception:
                    continue

        # Active stations and serials
        with connection.cursor() as cursor:
            cursor.execute("SELECT ID, VALVE_SER_NO FROM master_temp_data WHERE STATION_STATUS=%s", [1])
            active = cursor.fetchall() or []

        # Fallback: if no completed IDs via current_status tables, try pressure_analysis rows with END set
        if not completed:
            try:
                active_serials = [row[1] for row in active if row and row[1]]
                with connection.cursor() as cursor:
                    if active_serials:
                        placeholders = ",".join(["%s"] * len(active_serials))
                        cursor.execute(
                            f"""
                            SELECT DISTINCT TEST_ID FROM pressure_analysis
                            WHERE `END` IS NOT NULL AND TEST_ID IS NOT NULL AND VALVE_SER_NO IN ({placeholders})
                            """,
                            active_serials
                        )
                    else:
                        cursor.execute(
                            """
                            SELECT DISTINCT TEST_ID FROM pressure_analysis
                            WHERE `END` IS NOT NULL AND TEST_ID IS NOT NULL
                            """
                        )
                    completed.update([r[0] for r in cursor.fetchall() if r and r[0] is not None])
            except Exception:
                pass

        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        charts_root = os.path.join(desktop, 'LNT_Reports', 'Graphs')
        # Resolve and embed logo as base64 for WeasyPrint rendering
        logo_b64 = None
        try:
            logo_path = finders.find('images/lnt-logo.png')
            if not logo_path:
                alt_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'lnt-logo.png')
                logo_path = alt_path if os.path.exists(alt_path) else None
            if logo_path:
                with open(logo_path, 'rb') as lf:
                    logo_b64 = 'data:image/png;base64,' + base64.b64encode(lf.read()).decode('utf-8')
        except Exception:
            logo_b64 = None
        rendered_sections = []
        def _resolve_chart_path(root, sid, tid, serial, test_name):
            try:
                # Check if root directory exists
                if not os.path.exists(root):
                    print(f"⚠️ Charts root directory does not exist: {root}")
                    return None
               
                serial_str = str(serial).lower() if serial else ""
                safe_test = ''.join(c for c in str(test_name or '') if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
               
                # Collect all PNG files with their metadata
                all_files = []
                for fn in os.listdir(root):
                    if fn.lower().endswith('.png'):
                        full_path = os.path.join(root, fn)
                        all_files.append({
                            'path': full_path,
                            'name': fn,
                            'lower': fn.lower(),
                            'mtime': os.path.getmtime(full_path)
                        })
               
                if not all_files:
                    print(f"⚠️ No PNG files found in {root}")
                    return None
               
                # Priority 1: Match by BOTH serial number AND test name (highest priority)
                serial_and_test_matches = []
                if serial_str and safe_test:
                    for f in all_files:
                        if serial_str in f['lower'] and safe_test.lower() in f['lower']:
                            serial_and_test_matches.append(f)
               
                # Priority 2: Match by serial number only
                serial_matches = []
                if serial_str:
                    for f in all_files:
                        if serial_str in f['lower']:
                            serial_matches.append(f)
               
                # Priority 3: Match by test name only
                test_matches = []
                if safe_test:
                    for f in all_files:
                        if safe_test.lower() in f['lower']:
                            test_matches.append(f)
               
                # Priority 4: Match by station and test ID pattern
                pattern_matches = []
                pattern = f"station{sid}_test{tid}.png"
                for f in all_files:
                    if f['name'] == pattern:
                        pattern_matches.append(f)
               
                # Select best match: prioritize serial+test, then serial, then test name, then pattern
                # Always select the LATEST file (highest mtime) from the best category
                best_matches = serial_and_test_matches or serial_matches or test_matches or pattern_matches
               
                if best_matches:
                    # Sort by modification time (latest first)
                    best_matches.sort(key=lambda x: x['mtime'], reverse=True)
                    selected = best_matches[0]
                    match_type = "serial+test" if serial_and_test_matches else ("serial" if serial_matches else ("test_name" if test_matches else "pattern"))
                    print(f"✅ Found chart for station {sid}, test {tid} (matched by {match_type}, latest): {selected['name']}")
                    return selected['path']
               
                print(f"⚠️ No chart found for station {sid}, test {tid}, serial {serial}, test_name {test_name}")
            except Exception as e:
                print(f"❌ Error resolving chart path: {e}")
            return None

        for sid, serial in active:
            with connection.cursor() as cur:
                for tid in sorted(completed):
                    cur.execute(
                        """
                        SELECT TEST_NAME, SET_PRESSURE, ACTUAL_PRESSURE, PRESSURE_UNIT,
                               SET_TIME, ACTUAL_TIME, START_PRESSURE, RESULT_PRESSURE,
                               LEAK_PRESSURE, VALVE_STATUS, DATE_TIME
                        FROM pressure_analysis
                        WHERE STATION_STATUS=%s AND VALVE_SER_NO=%s AND TEST_ID=%s
                        ORDER BY ID DESC LIMIT 1
                        """,
                        [sid, serial, tid],
                    )
                    row = cur.fetchone()
                    if not row:
                        continue
                    test_name, set_p, act_p, unit, set_t, act_t, start_p, res_p, leak_p, vstatus, dt = row

                    img_path = _resolve_chart_path(charts_root, sid, tid, serial, test_name)
                    chart_b64 = None
                    if img_path and os.path.exists(img_path):
                        try:
                            with open(img_path, 'rb') as fimg:
                                chart_b64 = 'data:image/png;base64,' + base64.b64encode(fimg.read()).decode('utf-8')
                        except Exception:
                            chart_b64 = None

                    # Try to fetch extended header fields from pressure_analysis (best-effort)
                    ext = {
                        'valve_type': '', 'valve_size': '', 'valve_class': '', 'shell_material': '',
                        'tested_by': '', 'valve_tag_no': '', 'body_mp': ''
                    }
                    try:
                        cur.execute(
                            """
                            SELECT VALVETYPE_NAME, VALVESIZE_NAME, VALVECLASS_NAME, SHELLMATERIAL_NAME,
                                   TESTED_BY, NULL as valve_tag_no, NULL as body_mp
                            FROM pressure_analysis
                            WHERE STATION_STATUS=%s AND VALVE_SER_NO=%s
                            ORDER BY ID DESC LIMIT 1
                            """,
                            [sid, serial],
                        )
                        erow = cur.fetchone()
                        if erow:
                            ext['valve_type'] = erow[0] or ''
                            ext['valve_size'] = erow[1] or ''
                            ext['valve_class'] = erow[2] or ''
                            ext['shell_material'] = erow[3] or ''
                            ext['tested_by'] = erow[4] or ''
                            ext['valve_tag_no'] = erow[5] or ''
                            ext['body_mp'] = ''
                    except Exception:
                        pass

                    ctx = {
                        'type': ext['valve_type'] or 'Merged Valve Test Report',
                        'date': timezone.now().strftime('%Y-%m-%d'),
                        'size': ext['valve_size'],
                        'class': ext['valve_class'] or (unit or ''),
                        'tested_by': ext['tested_by'],
                        'shell_material': ext['shell_material'],
                        'body_mp': ext['body_mp'],
                        'serial_number': serial or '',
                        'valve_tag_no': ext['valve_tag_no'],
                        'test_name': test_name or '',
                        'set_time': set_t or '',
                        'set_pressure': set_p or '',
                        'stop_pressure': res_p or '',
                        'result_pressure': res_p or '',
                        'valve_status': vstatus or '',
                        'start_time_str': (dt.strftime('%H:%M:%S') if dt else '00:00:00'),
                        'test_duration_minutes': int((act_t or 0)) if isinstance(act_t, (int, float)) else 1,
                        'chart_image_base64': chart_b64,
                        'chart_image_url': None,
                        'chart_image_absolute_path': img_path if (img_path and os.path.exists(img_path)) else None,
                        'logo_base64': logo_b64,
                    }
                    html_part = render_to_string('report.html', ctx)
                    try:
                        body_start = html_part.lower().find('<body')
                        if body_start != -1:
                            body_start = html_part.find('>', body_start) + 1
                            body_end = html_part.lower().rfind('</body>')
                            content = html_part[body_start:body_end]
                        else:
                            content = html_part
                    except Exception:
                        content = html_part
                    rendered_sections.append(f"<section style=\"page-break-after: always;\">{content}</section>")

        # Secondary fallback: if still no sections, render directly from latest pressure_analysis rows
        if not rendered_sections and completed:
            try:
                with connection.cursor() as cur:
                    for tid in sorted(completed):
                        cur.execute(
                            """
                            SELECT STATION_STATUS, VALVE_SER_NO, TEST_NAME, SET_PRESSURE, ACTUAL_PRESSURE, PRESSURE_UNIT,
                                   SET_TIME, ACTUAL_TIME, START_PRESSURE, RESULT_PRESSURE, LEAK_PRESSURE, VALVE_STATUS, DATE_TIME
                            FROM pressure_analysis
                            WHERE TEST_ID=%s AND `END` IS NOT NULL
                            ORDER BY ID DESC
                            LIMIT 4
                            """,
                            [tid]
                        )
                        rows = cur.fetchall() or []
                        for (sid, serial, test_name, set_p, act_p, unit, set_t, act_t, start_p, res_p, leak_p, vstatus, dt) in rows:
                            img_path = _resolve_chart_path(charts_root, sid, tid, serial, test_name)
                            chart_b64 = None
                            if img_path and os.path.exists(img_path):
                                try:
                                    with open(img_path, 'rb') as fimg:
                                        chart_b64 = 'data:image/png;base64,' + base64.b64encode(fimg.read()).decode('utf-8')
                                except Exception:
                                    chart_b64 = None
                            ctx = {
                                'type': 'Merged Valve Test Report',
                                'date': timezone.now().strftime('%Y-%m-%d'),
                                'size': '',
                                'class': (unit or ''),
                                'tested_by': '',
                                'shell_material': '',
                                'body_mp': '',
                                'serial_number': serial or '',
                                'valve_tag_no': '',
                                'test_name': test_name or '',
                                'set_time': set_t or '',
                                'set_pressure': set_p or '',
                                'stop_pressure': res_p or '',
                                'result_pressure': res_p or '',
                                'valve_status': vstatus or '',
                                'start_time_str': (dt.strftime('%H:%M:%S') if dt else '00:00:00'),
                                'test_duration_minutes': int((act_t or 0)) if isinstance(act_t, (int, float)) else 1,
                                'chart_image_base64': chart_b64,
                                'chart_image_url': None,
                                'chart_image_absolute_path': img_path if (img_path and os.path.exists(img_path)) else None,
                                'logo_base64': logo_b64,
                            }
                            html_part = render_to_string('report.html', ctx)
                            try:
                                body_start = html_part.lower().find('<body')
                                if body_start != -1:
                                    body_start = html_part.find('>', body_start) + 1
                                    body_end = html_part.lower().rfind('</body>')
                                    content = html_part[body_start:body_end]
                                else:
                                    content = html_part
                            except Exception:
                                content = html_part
                            rendered_sections.append(f"<section style=\"page-break-after: always;\">{content}</section>")
            except Exception:
                pass

        # If nothing was rendered, include a simple placeholder page to avoid empty PDF
        if not rendered_sections:
            rendered_sections.append(
                "<section><h2 style='font-family: Arial, sans-serif;'>No completed tests found</h2>"
                "<p style='font-family: Arial, sans-serif;'>There are no completed test cycles to include in the merged report."
                " Ensure the test is marked completed and try again.</p></section>"
            )

        # Load inline styles from report.html to preserve exact formatting
        try:
            template_path = os.path.join(settings.BASE_DIR, 'templates', 'report.html')
            with open(template_path, 'r', encoding='utf-8') as tf:
                tpl = tf.read()
            st_idx = tpl.lower().find('<style>')
            en_idx = tpl.lower().find('</style>')
            styles = tpl[st_idx + 7:en_idx] if st_idx != -1 and en_idx != -1 else ''
        except Exception:
            styles = '@page { size: A4 landscape; margin: 1cm; } body { font-family: Arial, sans-serif; }'

        # If nothing was rendered, include a simple placeholder page to avoid empty PDF
        if not rendered_sections:
            rendered_sections.append(
                "<section><h2 style='font-family: Arial, sans-serif;'>No completed tests found</h2>"
                "<p style='font-family: Arial, sans-serif;'>There are no completed test cycles to include in the merged report."
                " Ensure the test is marked completed and try again.</p></section>"
            )

        sections_html = "\n".join(rendered_sections)
        combined_html = f"""
        <html>
          <head>
            <meta charset=\"utf-8\">
            <style>
              {styles}
            </style>
          </head>
          <body>
            {sections_html}
          </body>
        </html>
        """
        pdf = HTML(string=combined_html, base_url=str(settings.BASE_DIR)).write_pdf()
        # After generating merged PDF, update station flags
       
        resp = HttpResponse(pdf, content_type='application/pdf')
        resp['Content-Disposition'] = 'attachment; filename="merged_report.pdf"'
        return resp
    except Exception as e:
        return HttpResponse(f"PDF generation error: {e}", status=500)
    
def _generate_and_save_merged_pdf_to_disk(serial_number=None, count_id=None):
    """
    Generate merged PDF report from CSV data and pressure_analysis
    Returns a list of tuples (path, serial_no) to generated PDFs.
    """
    print(f"\n{'='*60}")
    print(f"🚀 Starting PDF generation")
    print(f"   Serial: {serial_number}, Count ID: {count_id}")
    print(f"{'='*60}\n")
    
    # --- Step 1: Fetch active station + serial numbers ---
    try:
        if serial_number:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT ID, VALVE_SER_NO FROM master_temp_data WHERE STATION_STATUS=%s AND VALVE_SER_NO=%s", 
                    [1, serial_number]
                )
                active = cursor.fetchall() or []
            
            if not active:
                print(f"   ⚠️ Serial {serial_number} not in active stations, checking pressure_analysis...")
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT DISTINCT VALVE_SER_NO FROM pressure_analysis WHERE VALVE_SER_NO=%s LIMIT 1", 
                        [serial_number]
                    )
                    result = cursor.fetchone()
                    if result and result[0]:
                        active = [(0, serial_number)]
                        print(f"   ✅ Found serial {serial_number} in pressure_analysis")
                    else:
                        print(f"   ❌ Serial {serial_number} not found anywhere")
                        return ''
        else:
            with connection.cursor() as cursor:
                cursor.execute("SELECT ID, VALVE_SER_NO FROM master_temp_data WHERE STATION_STATUS=%s", [1])
                active = cursor.fetchall() or []

        if not active:
            print("❌ No active valves found.")
            return ''
        
        print(f"✅ Found {len(active)} active valve(s): {[s[1] for s in active]}")
    except Exception as e:
        print(f"❌ Error fetching active valves: {e}")
        import traceback
        traceback.print_exc()
        return ''

    # --- Step 2: CSV directory for reading data ---
    csv_folder = r"D:\LNT_Reports\csv_Reports"
    if not os.path.exists(csv_folder):
        print(f"❌ CSV folder not found: {csv_folder}")
        return ''
    print(f"✅ Using CSV folder: {csv_folder}")

    # --- Step 3: Output folder ---
    out_dir = r"D:\Reports\merged"
    try:
        os.makedirs(out_dir, exist_ok=True)
        print(f"✅ Output directory ready: {out_dir}")
    except Exception as e:
        print(f"❌ Cannot create output directory: {e}")
        return ''

    # --- Step 4: Load inline CSS from template ---
    styles = '@page { size: A4 landscape; margin: 1cm; } body { font-family: Arial, sans-serif; }'
    try:
        template_path = os.path.join(settings.BASE_DIR, 'templates', 'report.html')
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as tf:
                tpl = tf.read()
            st_idx = tpl.lower().find('<style>')
            en_idx = tpl.lower().find('</style>')
            if st_idx != -1 and en_idx != -1:
                styles = tpl[st_idx + 7:en_idx]
                print("✅ Loaded CSS from template")
    except Exception as e:
        print(f"⚠️ Using default CSS (template error: {e})")

    # --- Step 5: Load logo as base64 ---
    logo_b64 = None
    try:
        logo_path = finders.find('images/lnt-logo.png')
        if not logo_path:
            alt_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'lnt-logo.png')
            logo_path = alt_path if os.path.exists(alt_path) else None
        
        if logo_path and os.path.exists(logo_path):
            with open(logo_path, 'rb') as lf:
                logo_b64 = 'data:image/png;base64,' + base64.b64encode(lf.read()).decode('utf-8')
            print("✅ Logo loaded successfully")
    except Exception as e:
        print(f"⚠️ Logo loading failed: {e}")

    # --- Helper: Generate chart from CSV data ---
    def _generate_chart_from_csv(csv_folder, serial, test_name, count_id, pressure_unit):
        """Generate chart image from CSV data and return as base64"""
        try:
            import matplotlib
            matplotlib.use('Agg')
            from matplotlib import pyplot as plt
            import matplotlib.dates as mdates
            from datetime import datetime as dt, timedelta
            
            print(f"\n   📊 Generating chart for: {test_name}")
            print(f"      Serial: {serial}, Count: {count_id}")
            
            # Find matching CSV file
            station_num = None
            csv_file = None
            for station in [1, 2, 3, 4]:
                filename = f"{serial}_station{station}_count{count_id}.csv"
                filepath = os.path.join(csv_folder, filename)
                
                if os.path.exists(filepath):
                    csv_file = filepath
                    station_num = station
                    print(f"      ✅ Found CSV: {filename}")
                    break
            
            if not csv_file:
                print(f"      ❌ CSV not found for count {count_id}")
                # Try to list available files
                try:
                    all_files = [f for f in os.listdir(csv_folder) if serial in f and f.endswith('.csv')]
                    print(f"      📋 Available CSV files for {serial}: {all_files[:3]}")
                except:
                    pass
                return None
            def wait_for_file_ready(path, timeout=5.0, min_size=20):
                start = time.time()
                while time.time() - start < timeout:
                    try:
                        if os.path.exists(path) and os.path.getsize(path) >= min_size:
                            return True
                    except Exception:
                        pass
                    time.sleep(0.1)
                return False

            if not wait_for_file_ready(csv_file, timeout=8.0, min_size=20):
                print(f" ❌ CSV found but incomplete or empty (timeout): {csv_file}")
                return None

            # Read CSV and filter for this test
            times = []
            pressures = []
            timer_states = []
            onoff_states = []
            
            all_test_names = set()
            row_count = 0
            matched_rows = 0
            
            with open(csv_file, 'r', encoding='utf-8') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                for row in csv_reader:
                    row_count += 1
                    row_test_name = row.get('TEST_NAME', '')
                    all_test_names.add(row_test_name)
                    
                    # Match test name (case-insensitive and strip whitespace)
                    if row_test_name.strip().lower() != test_name.strip().lower():
                        continue
                    
                    matched_rows += 1
                    dt_str = row.get('DATE_TIME')
                    pressure_val = row.get('PRESSURE')
                    timer_status_val = row.get('TIMER_STATUS')
                    onoff = row.get('TIMER_ON_OFF', '')
                    
                    # Parse datetime
                    try:
                        dt_val = dt.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
                    except Exception:
                        try:
                            dt_val = dt.fromisoformat(dt_str)
                        except Exception:
                            continue
                    
                    # Parse pressure
                    try:
                        pressure_float = float(pressure_val or 0.0)
                    except Exception:
                        pressure_float = 0.0
                    
                    # Parse timer status
                    try:
                        timer_status_int = int(timer_status_val or 0)
                    except Exception:
                        timer_status_int = 0
                    
                    times.append(dt_val)
                    pressures.append(pressure_float)
                    timer_states.append(timer_status_int)
                    onoff_states.append((onoff or '').lower())
            
            if not times:
                print(f"      ❌ No data rows matched test '{test_name}'")
                return None
            
            print(f"      ✅ Found {matched_rows} data points")
            
            # Detect ON/OFF transitions
            on_indices = []
            off_indices = []
            
            # Edge detection on TIMER_STATUS
            for i in range(1, len(timer_states)):
                prev_s = int(timer_states[i - 1])
                cur_s = int(timer_states[i])
                if prev_s == 0 and cur_s == 1:
                    on_indices.append(i)
                elif prev_s == 1 and cur_s == 0:
                    off_indices.append(i)
            
            # Also check explicit TIMER_ON_OFF markers
            for i in range(len(onoff_states)):
                st = onoff_states[i]
                if st == 'on' and i not in on_indices:
                    on_indices.append(i)
                elif st == 'off' and i not in off_indices:
                    off_indices.append(i)
            
            # Station colors
            station_colors = {
                1: (75/255, 192/255, 192/255),
                2: (255/255, 99/255, 132/255),
                3: (54/255, 162/255, 235/255),
                4: (255/255, 206/255, 86/255)
            }
            line_color = station_colors.get(station_num, (75/255, 192/255, 192/255))
            
            # Create plot
            plt.figure(figsize=(8, 3), facecolor='white')
            ax = plt.gca()
            ax.set_facecolor('white')
            
            plt.plot(times, pressures, color=line_color, linewidth=2, marker='', markersize=0)
            
            plt.title(f'{serial} - {test_name}', color='black', fontsize=12, fontweight='bold')
            plt.xlabel('Time', color='black', fontsize=10)
            plt.ylabel(f'Pressure({pressure_unit})', color='black', fontsize=10)
            
            ax.grid(True, color='black', alpha=0.1, linestyle='-', linewidth=0.5)
            ax.set_axisbelow(True)
            
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M'))
            plt.xticks(rotation=45, ha='right', color='black', fontsize=9)
            plt.yticks(color='black', fontsize=9)
            
            for spine in ax.spines.values():
                spine.set_color('black')
                spine.set_alpha(0.3)
            
            # Set Y-axis limits
            if pressures:
                max_actual_pressure = max(pressures)
                if max_actual_pressure > 0:
                    ax.set_ylim(bottom=0, top=max_actual_pressure * 1.2)
                else:
                    ax.set_ylim(bottom=0, top=10)
            
            # Set X-axis limits
            if times:
                time_min = min(times)
                time_max = max(times)
                time_range = time_max - time_min
                padding = time_range * 0.01 if time_range.total_seconds() > 0 else timedelta(seconds=1)
                ax.set_xlim(left=time_min - padding, right=time_max + padding)
            
            # Draw first ON and OFF lines
            yl = ax.get_ylim()
            yrange = (yl[1] - yl[0]) if isinstance(yl, tuple) else None
            
            def local_value(idx):
                try:
                    return pressures[idx]
                except Exception:
                    return yl[0] + 0.9 * (yl[1] - yl[0]) if yrange else 0
            
            first_on_idx = min(on_indices) if on_indices else None
            first_off_idx = min(off_indices) if off_indices else None
            
            if first_on_idx is not None and first_on_idx < len(times):
                dtv = times[first_on_idx]
                plt.axvline(dtv, color='#00ff00', linestyle='-', linewidth=2)
                y_here = local_value(first_on_idx) + (0.02 * yrange if yrange else 0)
                time_str = dtv.strftime('%I:%M')
                plt.text(dtv, y_here, f"{time_str} - Start", color="#155715", rotation=90,
                         va='top', ha='right', fontsize=8, fontweight='bold')
            
            if first_off_idx is not None and first_off_idx < len(times):
                dtv = times[first_off_idx]
                plt.axvline(dtv, color='red', linestyle='-', linewidth=2)
                y_here_off = local_value(first_off_idx) + (0.02 * yrange if yrange else 0)
                time_str = dtv.strftime('%I:%M')
                plt.text(dtv, y_here_off, f"{time_str} - End", color='red', rotation=90,
                         va='top', ha='right', fontsize=8, fontweight='bold')
            
            plt.tight_layout()
            
            # Save to BytesIO and convert to base64
            buf = BytesIO()
            plt.savefig(buf, format='png', dpi=150, facecolor='white', edgecolor='none', bbox_inches='tight')
            plt.close()
            buf.seek(0)
            
            img_b64 = 'data:image/png;base64,' + base64.b64encode(buf.read()).decode('utf-8')
            print(f"      ✅ Chart generated successfully")
            return img_b64
            
        except Exception as e:
            print(f"      ❌ Chart generation error: {e}")
            import traceback
            traceback.print_exc()
            return None

    # --- Step 6: Generate PDF per valve ---
    output_paths = []

    for sid, serial in active:
        if not serial:
            continue

        print(f"\n{'─'*60}")
        print(f"📄 Processing serial: {serial}")
        print(f"{'─'*60}")

        # *** CRITICAL FIX: Determine COUNT_ID first ***
        try:
            if count_id is not None:
                target_count_id = count_id
                print(f"   Using specified count_id: {target_count_id}")
            else:
                # Get the latest COUNT_ID for this serial
                with connection.cursor() as cur:
                    cur.execute("""
                        SELECT COUNT_ID 
                        FROM pressure_analysis 
                        WHERE VALVE_SER_NO=%s AND CYCLE_COMPLETE='yes'
                        ORDER BY ID DESC LIMIT 1
                    """, [serial])
                    count_row = cur.fetchone()
                    target_count_id = count_row[0] if count_row and count_row[0] else None
                    
                    if target_count_id is None:
                        # Fallback: get any latest COUNT_ID
                        cur.execute("""
                            SELECT COUNT_ID 
                            FROM pressure_analysis 
                            WHERE VALVE_SER_NO=%s
                            ORDER BY ID DESC LIMIT 1
                        """, [serial])
                        count_row = cur.fetchone()
                        target_count_id = count_row[0] if count_row and count_row[0] else 1
                    
                    print(f"   Using latest count_id: {target_count_id}")
            
            # *** CRITICAL FIX: Fetch test IDs ONLY for this specific COUNT_ID ***
            with connection.cursor() as cur:
                cur.execute("""
                    SELECT DISTINCT TEST_ID 
                    FROM pressure_analysis 
                    WHERE VALVE_SER_NO=%s 
                      AND COUNT_ID=%s 
                      AND TEST_ID IS NOT NULL 
                    ORDER BY TEST_ID
                """, [serial, target_count_id])
                test_ids = [r[0] for r in cur.fetchall() if r and r[0]]
                
        except Exception as e:
            print(f"❌ Error fetching test IDs: {e}")
            import traceback
            traceback.print_exc()
            continue

        if not test_ids:
            print(f"⚠️ No test data found for serial {serial} with count_id {target_count_id}")
            continue

        print(f"✅ Found {len(test_ids)} test(s): {test_ids}")

        rendered_sections = []

        # Process each test
        with connection.cursor() as cur:
            for tid in test_ids:
                try:
                    # Fetch test data for the specific COUNT_ID
                    cur.execute("""
                        SELECT TEST_NAME, SET_PRESSURE, ACTUAL_PRESSURE, PRESSURE_UNIT,
                               SET_TIME, ACTUAL_TIME, START_PRESSURE, RESULT_PRESSURE,
                               LEAK_PRESSURE, VALVE_STATUS, DATE_TIME,
                               VALVETYPE_NAME, VALVESIZE_NAME, VALVECLASS_NAME,
                               SHELLMATERIAL_NAME, COL7_VALUE, COL6_VALUE, COL14_VALUE,
                               COL8_VALUE, COL9_VALUE, COL11_VALUE, COL12_VALUE
                        FROM pressure_analysis
                        WHERE VALVE_SER_NO=%s AND TEST_ID=%s AND COUNT_ID=%s
                        ORDER BY ID DESC LIMIT 1
                    """, [serial, tid, target_count_id])
                    
                    row = cur.fetchone()
                    if not row:
                        print(f"   ⚠️ No data for test ID {tid}")
                        continue

                    # Unpack row data
                    (test_name, set_p, act_p, unit, set_t, act_t,
                     start_p, res_p, leak_p, vstatus, dt,
                     vtype, vsize, vclass, shell, tested_by, tag_no, body_mp,
                     body_heat, body_mpdp, bonnet_heat, bonnet_mp) = row

                    print(f"   📝 Test: {test_name} (ID: {tid}, Count: {target_count_id})")

                    # Generate chart
                    chart_b64 = _generate_chart_from_csv(csv_folder, serial, test_name, target_count_id, unit or 'bar')

                    # Prepare context
                    ctx = {
                        'type': vtype or 'Merged Valve Test Report',
                        'date': timezone.now().strftime('%Y-%m-%d'),
                        'size': vsize or '',
                        'class': vclass or (unit or ''),
                        'tested_by': tested_by or '',
                        'shell_material': shell or '',
                        'Body_heat': body_heat or '',
                        'Body_mp': body_mpdp or '',
                        'bonnet_heat': bonnet_heat or '',
                        'bonnet_mp': bonnet_mp or '',
                        'unit': unit or 'bar',
                        'serial_number': serial,
                        'valve_tag_no': tag_no or '',
                        'test_name': test_name or '',
                        'set_time': set_t or '',
                        'set_pressure': set_p or '',
                        'start_pressure': start_p or '',
                        'stop_pressure': res_p or '',
                        'result_pressure': res_p or '',
                        'valve_status': vstatus or '',
                        'start_time_str': dt.strftime('%H:%M:%S') if dt else '00:00:00',
                        'test_duration_minutes': int(act_t or 0) if isinstance(act_t, (int, float)) else 1,
                        'chart_image_base64': chart_b64,
                        'logo_base64': logo_b64,
                    }

                    # Render HTML section
                    html_part = render_to_string('report.html', ctx)
                    
                    # Extract body content
                    try:
                        body_start = html_part.lower().find('<body')
                        if body_start != -1:
                            body_start = html_part.find('>', body_start) + 1
                            body_end = html_part.lower().rfind('</body>')
                            content = html_part[body_start:body_end]
                        else:
                            content = html_part
                    except:
                        content = html_part

                    rendered_sections.append(f"<section style='page-break-after: always;'>{content}</section>")
                    print(f"   ✅ Section rendered for {test_name}")

                except Exception as e:
                    print(f"   ❌ Error processing test {tid}: {e}")
                    import traceback
                    traceback.print_exc()
                    continue

        if not rendered_sections:
            print(f"⚠️ No sections rendered for {serial}. Skipping PDF.")
            continue

        # Combine HTML
        combined_html = f"""
        <html>
          <head>
            <meta charset='utf-8'>
            <style>{styles}</style>
          </head>
          <body>{''.join(rendered_sections)}</body>
        </html>
        """

        # Generate PDF
        try:
            print(f"\n   🔨 Generating PDF...")
            pdf_bytes = HTML(string=combined_html, base_url=str(settings.BASE_DIR)).write_pdf()

            # Determine output filename
            safe_serial = ''.join(ch if str(ch).isalnum() or ch in ('-', '_') else '_' for ch in str(serial))
            
            out_filename = f"L&T_{safe_serial}_count{target_count_id}.pdf"
            out_path = os.path.join(out_dir, out_filename)

            # Save PDF
            with open(out_path, 'wb') as f:
                f.write(pdf_bytes)

            output_paths.append((out_path, serial))
            print(f"   ✅ PDF saved: {out_filename}")
            print(f"   📁 Full path: {out_path}")

        except Exception as e:
            print(f"   ❌ PDF generation error: {e}")
            import traceback
            traceback.print_exc()
            continue

    print(f"\n{'='*60}")
    if output_paths:
        print(f"✅ PDF generation complete! {len(output_paths)} file(s) generated.")
    else:
        print(f"❌ No PDFs were generated")
    print(f"{'='*60}\n")

    return output_paths

@csrf_exempt
def get_serial_counts(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'GET required'}, status=405)
    serial = (request.GET.get('serial') or '').strip()
    if not serial:
        return JsonResponse({'status': 'error', 'message': 'serial query param required'}, status=400)
    try:
        with connection.cursor() as cur:
            cur.execute(
                """
                SELECT COUNT_ID, MAX(DATE_TIME) AS latest_dt
                FROM pressure_analysis
                WHERE VALVE_SER_NO=%s AND COUNT_ID IS NOT NULL AND CYCLE_COMPLETE='yes'
                GROUP BY COUNT_ID
                ORDER BY latest_dt DESC
                """,
                [serial]
            )
            rows = cur.fetchall() or []
            counts = []
            for r in rows:
                cid = r[0]
                dt = r[1]
                counts.append({
                    'count_id': int(cid) if cid is not None else None,
                    'latest_date': (dt.strftime('%Y-%m-%d %H:%M:%S') if hasattr(dt, 'strftime') else (str(dt) if dt is not None else ''))
                })
        return JsonResponse({'status': 'success', 'counts': counts})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)





@csrf_exempt
@login_required
def check_category_data(request):
    """Check if enabled categories have missing pressure or duration data"""
    if request.method not in ("GET", "POST"):
        return JsonResponse({"status": "error", "message": "Unsupported method"}, status=405)
    
    try:
        with connection.cursor() as cursor:
            # Get all enabled categories
            cursor.execute("""
                SELECT CATEGORY_ID, CATEGORY_NAME, PRESSURE_COLUMN_NAME, DURATION_COLUMN_NAME
                FROM category
                WHERE STATUS = 'ENABLE'
                ORDER BY CATEGORY_ID
            """)
            enabled_categories = cursor.fetchall()
            
            missing_data = []
            
            for cat_id, cat_name, pre_col, dur_col in enabled_categories:
                if not pre_col or not dur_col:
                    continue
                
                # Check pressure data - find ALL shell materials with missing/empty/0 values
                # Note: FLOAT columns can only be NULL or numeric (not empty strings)
                cursor.execute(f"""
                    SELECT DISTINCT 
                        mpd.SHELLMATERIAL_ID,
                        sm.SHELL_MATERIAL_NAME,
                        mpd.VALVECLASS_ID,
                        vc.CLASS_NAME
                    FROM master_pressure_data mpd
                    LEFT JOIN shell_material sm ON mpd.SHELLMATERIAL_ID = sm.ID
                    LEFT JOIN valveclass vc ON mpd.VALVECLASS_ID = vc.CLASS_ID
                    WHERE (mpd.{pre_col} IS NULL OR mpd.{pre_col} = 0)
                """)
                pressure_issues = cursor.fetchall()
                
                # Check duration data - find ALL valve sizes with missing/empty/0 values
                # Note: INT columns can only be NULL or numeric (not empty strings)
                cursor.execute(f"""
                    SELECT DISTINCT 
                        mdd.SIZE_ID,
                        vs.SIZE_NAME,
                        mdd.STANDARD_ID,
                        std.STANDARD_NAME
                    FROM master_duration_data mdd
                    LEFT JOIN valvesize vs ON mdd.SIZE_ID = vs.SIZE_ID
                    LEFT JOIN standard std ON mdd.STANDARD_ID = std.STANDARD_ID
                    WHERE (mdd.{dur_col} IS NULL OR mdd.{dur_col} = 0)
                """)
                duration_issues = cursor.fetchall()
                
                # Add all pressure issues for this category
                for pressure_issue in pressure_issues:
                    missing_data.append({
                        'category_id': cat_id,
                        'category_name': cat_name,
                        'issue_type': 'pressure',
                        'shell_material_id': pressure_issue[0],
                        'shell_material_name': pressure_issue[1] or f"ID: {pressure_issue[0]}",
                        'valve_class_id': pressure_issue[2],
                        'valve_class_name': pressure_issue[3] or f"ID: {pressure_issue[2]}",
                        'redirect_url': '/shell_material/'
                    })
                
                # Add all duration issues for this category
                for duration_issue in duration_issues:
                    missing_data.append({
                        'category_id': cat_id,
                        'category_name': cat_name,
                        'issue_type': 'duration',
                        'valve_size_id': duration_issue[0],
                        'valve_size_name': duration_issue[1] or f"ID: {duration_issue[0]}",
                        'standard_id': duration_issue[2],
                        'standard_name': duration_issue[3] or f"ID: {duration_issue[2]}",
                        'redirect_url': '/valve_size/'
                    })
            
            if missing_data:
                return JsonResponse({
                    "status": "error",
                    "has_missing_data": True,
                    "missing_data": missing_data  # Return all issues, not just first one
                })
            
            return JsonResponse({
                "status": "success",
                "has_missing_data": False
            })
            
    except Exception as e:
        import traceback
        print(f"Error in check_category_data: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

@csrf_exempt
@login_required
def check_cycle_status(request):
    if request.method not in ("GET", "POST"):
        return JsonResponse({"status": "failure", "message": "Unsupported method"}, status=405)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT VALVE_SER_NO
                FROM master_temp_data
                WHERE STATION_STATUS = %s
                  AND VALVE_SER_NO IS NOT NULL
                ORDER BY ID
                """,
                [1]
            )
            rows = cursor.fetchall() or []
            print('rows',rows)
            serials = [str(r[0]) for r in rows if r and r[0] is not None]
            if serials:
                # Backward-compatible single value + full list
                return JsonResponse({
                    "status": "success",
                    "incomplete_serialno": serials[0],
                    "incomplete_serialnos": serials,
                    "count": len(serials),
                })
            return JsonResponse({"status": "failure", "incomplete_serialnos": [], "count": 0})
    except Exception as e:
        return JsonResponse({"status": "failure", "message": str(e)}, status=500)

@csrf_exempt
@login_required
def delete_test(request, serialno):
    serial_list = [s.strip() for s in serialno.split(',') if s.strip()]

    if not serial_list:
        return JsonResponse({'error': 'No serial numbers provided'}, status=400)
    try:
        tables = [
            'current_status_station1',
            'current_status_station2',
            'current_status_station3',
            # 'current_status_station4'
           
        ]
       
        with connection.cursor() as cursor:
            # Update master_temp_data
            cursor.execute(
                "UPDATE master_temp_data SET STATION_STATUS = %s",
                [0]
            )
            for sn in serial_list:
                # Get the latest count_id for this serial number
                cursor.execute("""
                    SELECT COUNT_ID FROM pressure_analysis
                    WHERE VALVE_SER_NO=%s
                    ORDER BY ID DESC
                    LIMIT 1
                """, [sn])
                row = cursor.fetchone()
                count_id = row[0] if row and row[0] else 0
                print('count_id',count_id)
                cursor.execute("""DELETE FROM pressure_analysis
                                 WHERE VALVE_SER_NO=%s AND COUNT_ID=%s""",[sn,count_id])
            

           
            # Delete from all tables
            for table in tables:
                cursor.execute(f"TRUNCATE TABLE {table}")      
                cursor.execute("update pressure_analysis set STATUS=%s",[0])
                cursor.execute("TRUNCATE TABLE temp_pressure_analysis")
                cursor.execute("TRUNCATE TABLE temp_testing_data")
               
                TesleadSmartsyncx.write_register(2000,0) # set pressure
                TesleadSmartsyncx.write_register(2001,0) # valve size
                TesleadSmartsyncx.write_register(2002,0) # valve class
                TesleadSmartsyncx.write_register(2003,0) # set time
                TesleadSmartsyncx.write_register(2004,0) # Test Type
                TesleadSmartsyncx.write_register(2101,0) # station 1 Enable/ Disable
                TesleadSmartsyncx.write_register(2102,0) # station 2 Enable/ Disable
                TesleadSmartsyncx.write_register(2103,0) # station 3 Enable/ Disable
                TesleadSmartsyncx.write_register(2104,0) # station 4 Enable/ Disable
                TesleadSmartsyncx.write_register(2006,0) # Actual time
                TesleadSmartsyncx.write_register(2011,0) # station 1 result
                TesleadSmartsyncx.write_register(2025,0) # station 2 result
                TesleadSmartsyncx.write_register(2026,0) # station 3 result
                TesleadSmartsyncx.write_register(2027,0) # station 4 result
                TesleadSmartsyncx.write_register(2105,0) # pressure unit
           
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "failure", "message": str(e)}, status=500)
   
       
       
   
       
    
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
@login_required
def set_active_test(request):
    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "POST required"}, status=405)
    data = json.loads(request.body or "{}")
    test_id = data.get("test_id")
    if not test_id:
        return JsonResponse({"status": "error", "message": "test_id required"}, status=400)

    with connection.cursor() as cursor:
        # Reset previous active
        cursor.execute("UPDATE pressure_analysis SET `STATUS` = 0 WHERE `STATUS` = 1")
        # Mark clicked test active
        cursor.execute("UPDATE pressure_analysis SET `STATUS` = 1 WHERE TEST_ID = %s", [test_id])

    return JsonResponse({"status": "success"})


from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def get_load_data(request):
    """
    Returns currently active test info from pressure_analysis where STATUS=1
    """

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT TEST_ID, TEST_NAME, SET_PRESSURE, PRESSURE_UNIT, SET_TIME
            FROM pressure_analysis
            WHERE STATUS = 1
            ORDER BY ID DESC
            LIMIT 1
        """)
        arow = cursor.fetchone()

    if arow:
        active_test_id, active_test_name, active_set_pressure, active_pressure_unit, active_set_time = arow
        return JsonResponse({
            "status": "success",
            "active_test_id": active_test_id,
            "active_test_name": active_test_name,
            "active_set_pressure": int(active_set_pressure),
            
            "active_set_time": active_set_time,
        })
    else:
        return JsonResponse({"status": "no_active_test"})

        
        
def download_valve_report_from_pressure_analysis(request):
    """Save single GGC report based on serial number from pressure_analysis to D:\LNT_Reports\GGC_Reports"""
    serial = request.GET.get('serial', '').strip()
    count_id = request.GET.get('count_id', '').strip()  # 🆕 Get count_id from request
    
    print(f'Generating GGC report for serial: {serial}, count_id: {count_id}')  # 🆕 Debug log
    
    if not serial:
        messages.error(request, "Serial number is required")
        return redirect('dashboard')
    
    try:
        # Just to check if serial exists in pressure_analysis (no need for STATION_ID)
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM pressure_analysis 
                WHERE VALVE_SER_NO = %s
            """, [serial])
            count_row = cursor.fetchone()
            if not count_row or count_row[0] == 0:
                messages.error(request, f"No data found for serial {serial} in pressure_analysis")
                return redirect('dashboard')

        # ✅ Generate report directly from serial with count_id
        out = export_valve_report_from_master(
            station_id=None, 
            valve_serial_number=serial,
            count_id=count_id if count_id else None  # 🆕 Pass count_id parameter
        )

        # ✅ Save to folder
        save_dir = r'D:\\Reports\\GGCreports'
        os.makedirs(save_dir, exist_ok=True)

        safe_serial = ''.join(ch if ch.isalnum() or ch in ('-', '_') else '_' for ch in str(serial))
        date_str = timezone.now().strftime('%Y%m%d')
        
        # 🆕 Include count_id in filename if provided
        if count_id:
            base_name = f"L&T_{safe_serial}_{date_str}_count{count_id}.xlsx"
        else:
            base_name = f"L&T_{safe_serial}_{date_str}.xlsx"
        
        filepath = os.path.join(save_dir, base_name)

        # ✅ Try writing with up to 10 attempts
        written = False
        last_err = None
        for idx in range(1, 11):
            try:
                if idx == 1:
                    target = filepath
                else:
                    # 🆕 Include count_id in numbered versions too
                    if count_id:
                        target = os.path.join(save_dir, f"L&T_{safe_serial}_{date_str}_count{count_id}_{idx}.xlsx")
                    else:
                        target = os.path.join(save_dir, f"L&T_{safe_serial}_{date_str}_{idx}.xlsx")
                
                with open(target, 'wb') as f:
                    f.write(out.getvalue())
                written = True
                messages.success(request, f"GGC report saved successfully")  # 🆕 Added saved path info
                print(f"✅ Report saved to: {target}")  # 🆕 Debug log
                break
            except PermissionError as pe:
                last_err = pe
                continue
            except Exception as e:
                last_err = e
                continue

        if not written:
            error_msg = str(last_err) if last_err else "Unknown error occurred"
            messages.error(request, f"Error saving GGC report: {error_msg}")

    except Exception as e:
        messages.error(request, f"Error generating GGC report: {str(e)}")
        print(f"❌ Error: {str(e)}")  # 🆕 Debug log

    return redirect('dashboard')


def write_read(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT PRESSURE_UNIT FROM master_temp_data where STATION_STATUS=%s",[1])
        _pu_row = cursor.fetchone()
        if not _pu_row:
            return JsonResponse({"error": "No active station found"}, status=404)
        pressure_unit = _pu_row[0]
        if pressure_unit:
            if pressure_unit == "psi":
                TesleadSmartsyncx.write_register(2105,1)
            elif pressure_unit == "bar":
                TesleadSmartsyncx.write_register(2105,2)
            elif pressure_unit == "kg/cm2":
                TesleadSmartsyncx.write_register(2105,3)

        with connection.cursor() as cursor:
            cursor.execute("select SIZE_NAME,CLASS_NAME from master_temp_data where STATION_STATUS=%s", ["1"])
            fetched_data = cursor.fetchone()

            print("fetched_data >>>>", fetched_data)
           
            if fetched_data:
                size_name = fetched_data[0]
                class_name = fetched_data[1]
               
                with connection.cursor() as cursor:
                    cursor.execute("select SIZE_ID from valvesize where SIZE_NAME=%s", [size_name])
                    _size_row = cursor.fetchone()
                    if not _size_row:
                        return JsonResponse({"error": f"Size '{size_name}' not found in valvesize table"}, status=404)
                    size_id = _size_row[0]
               
                    split_class_name = class_name.replace("#", "")
                
                    TesleadSmartsyncx.write_register(2002, int(split_class_name))
                    TesleadSmartsyncx.write_register(2001, size_id)
                
                    print("class_name >>>>>> ", class_name)
            
                    cursor.execute("select CLASS_ID from valveclass where CLASS_NAME=%s", [class_name])
                    _class_row = cursor.fetchone()
                    if not _class_row:
                        return JsonResponse({"error": f"Class '{class_name}' not found in valveclass table"}, status=404)
                    class_id = _class_row[0]
                   
                split_class_name = class_name.replace("#", "")
            
                TesleadSmartsyncx.write_register(2002, class_id)
                TesleadSmartsyncx.write_register(2001, size_id)
                
                station_addresses = {
                    1: 2008,
                    2: 2020,
                    3: 2021,
                    4: 2022
                }
                station_id_addresses = {
                    1: 2101,
                    2: 2102,
                    3: 2103,
                    4: 2104
                }
                with connection.cursor() as cursor:
                    cursor.execute("SELECT ID, VALVE_SER_NO FROM master_temp_data WHERE STATION_STATUS = %s", [1])
                    active_data = cursor.fetchall()

                    if not active_data:
                        return JsonResponse({"error": "No active stations found"}, status=404)
                    active_stations = {row[0]: row[1] for row in active_data}
                   
                    for station_id, valve_serial_no in active_stations.items():
                        address = station_addresses.get(station_id)
                        id_address = station_id_addresses.get(station_id)
                        result = TesleadSmartsyncx.write_register(id_address,1)
                           
                return JsonResponse({"status":"success"})
        return JsonResponse({"status":"failure"})

def get_drained_status(request):
    pressure_drain = TesleadSmartsyncx.read_holding_registers(2200, 1).registers[0]
    return JsonResponse({"pressure_drain": pressure_drain})



def sap_upload_doc(file=None, serial_no=None):
    print(f"--- SAP 'UPLOAD' Integration (File: {file}) ---")
    
    wsdl_path = os.path.join(settings.BASE_DIR, 'landtapp', 'wdsl', 'z_qm_upl_vtr_doc_frm_test_macbinding.wsdl')
    
    if not os.path.exists(wsdl_path):
        print(f"❌ SAP configuration error: WSDL file not found at {wsdl_path}")
        return

    try:
        # Initialize Client
        # Note: XML huge tree enabled for large SOAP responses
        soap_settings = Settings(strict=False, xml_huge_tree=True)
        client = Client(wsdl=wsdl_path, settings=soap_settings)
        print(f"[OK] WSDL Loaded: {os.path.basename(wsdl_path)}")

        if not file or not serial_no:
            print("❌ File name or Serial Number is required for SAP upload")
            return

        # Data for UPLOAD request
        # The SAP service expects IpFilePath in a specific format
        upload_data = {
            'IpFilePath': f'//LTVLCD29338/Reports/{file}',
            'IpUsn': serial_no
        }

        print(f"Attempting to UPLOAD Report: {file}")
        print(f"SAP Path: {upload_data['IpFilePath']}")
        
        # Calling the service
        # Note: We use IpFilePath as the primary identifier for SAP to fetch/store the file
        response = client.service.ZQmUplVtrDocFrmTestMac(**upload_data)
        
        print(f"--- RAW SAP RESPONSE ---")
        print(response)

        # Success/Error logic based on SAP response fields
        success_code = getattr(response, 'EpSuccess', '1')
        exc_msg = getattr(response, 'EpExcmsg', '')

        if success_code == '0':
            print(f"✅ SUCCESS: {file} has been uploaded to SAP.")
        elif "CMS 057" in str(exc_msg):
             print(f"❌ SAP SERVER ERROR (CMS 057) for {file}:")
             print("The SAP Server is trying to start 'sapftp' to reach your PC but it is being blocked.")
             print("FIX: You MUST move the file to a folder the SAP server can see directly (AL11 path).")
        else:
            reason = exc_msg if exc_msg else "Unknown SAP Error (Status 1)"
            print(f"❌ FAILED to upload {file}: {reason}")

    except Exception as e:
        print(f"❌ SAP Connection failed for {file}: {str(e)}")
