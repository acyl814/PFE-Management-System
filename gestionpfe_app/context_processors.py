from . import views 


def user_type_context(request):
    context = {
        'is_admin': views.is_admin(request.user) if request.user.is_authenticated else False,
        'is_teacher': views.is_teacher(request.user) if request.user.is_authenticated else False,
        'is_company': views.is_company(request.user) if request.user.is_authenticated else False,
        'is_student': views.is_student(request.user) if request.user.is_authenticated else False,
    }
    return context