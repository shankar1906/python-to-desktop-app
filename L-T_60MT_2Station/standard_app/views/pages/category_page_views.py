from django.shortcuts import render, redirect
from standard_app.decorators import permission_required
from django.db import connection


@permission_required("Category")
def category(request):
    # Get superuser level from session
    superuser_level = request.session.get('superuser', 0)
    try:
        superuser_level = int(superuser_level)
    except (ValueError, TypeError):
        superuser_level = 0
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT TEST_CATEGORY_ID, TEST_CATEGORY_NAME, CATEGORY_STATUS
            FROM category
            ORDER BY CATEGORY_STATUS DESC, TEST_CATEGORY_ID
        """)
        categories = cursor.fetchall()

        data = [
        {
            "id": row[0],
            "category_name": row[1],
            "status": row[2],
        }
        for row in categories
        ]
    return render(request, "category.html", {
        "categories": data,
        "superuser_level": superuser_level
    })






