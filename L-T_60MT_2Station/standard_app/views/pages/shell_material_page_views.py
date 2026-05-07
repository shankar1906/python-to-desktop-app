from django.shortcuts import render
from standard_app.decorators import permission_required


@permission_required("Shell Material")
def shell_material_page(request):
    return render(request, "shell_material.html")
