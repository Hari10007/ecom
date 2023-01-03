from django.shortcuts import redirect

def user_is_admin(function=None, redirect_url='/'):

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_staff:
                return redirect(redirect_url)
                
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator