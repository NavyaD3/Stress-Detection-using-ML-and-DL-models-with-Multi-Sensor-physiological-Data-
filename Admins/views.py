from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages



def adminhome(request):
    users = User.objects.filter(is_staff=False, is_superuser=False) 
    return render(request, "Admin/adminhome.html", {"users": users})

def admin_update_userstatus(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        
        # Toggle the is_active status
        user.is_active = not user.is_active
        user.save()

        # Display message based on the action
        if user.is_active:
            messages.success(request, f"User {user.username} has been activated.")
        else:
            messages.success(request, f"User {user.username} has been deactivated.")
        
        return redirect('adminhome')  # Redirect back to the admin home page
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('adminhome')
    



from Users.models import PredictionHistory


from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test



@user_passes_test(lambda u: u.is_superuser)
def reports(request):
    """
    Admin view to display all user stress prediction reports.
    Shows user details, input values, prediction results, and contributing factors.
    """
    # Fetch all prediction records with related user info
    all_predictions = PredictionHistory.objects.select_related("user").order_by("-created_at")

    # Optional: Split contributing factors into a list for easier rendering in template
    for p in all_predictions:
        p.factors_list = [f.strip() for f in p.contributing_factors.split(",") if f.strip()]

    return render(request, "Admin/reports.html", {"predictions": all_predictions})


    
def admin_proposed(request):
    return render(request, "Admin/admin_proposed.html")