from django.shortcuts import render
from .auth_page_views import _require_session_auth

def livepage_page_view(request):
    """
    A demo view to test UI developments.
    """
    # Optional: protect with session auth
    # guard = _require_session_auth(request)
    # if guard:
    #     return guard
    
    context = {
        "header_title": "Live Page",
        "username": request.session.get("username", "Guest"),
    }
    return render(request, "livepage.html", context)
