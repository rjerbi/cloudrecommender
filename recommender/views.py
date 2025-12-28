import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, RecommendationForm, CustomPasswordResetForm
from .models import Recommendation
from django.core.exceptions import ValidationError
from django.contrib.admin.views.decorators import staff_member_required

def cover(request):
    return render(request, 'recommender/cover.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You have successfully signed up! You can now login.")
            return redirect('login') 
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegisterForm()
    return render(request, 'recommender/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
       
            if not request.session.get('admin_user', False):
                messages.success(request, "Successfully logged in!", extra_tags='login')
                return redirect('recommendation_form')
          
            request.session.pop('admin_user', None)
    else:
        form = LoginForm()
    return render(request, 'recommender/login.html', {'form': form})


def custom_password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, "Password reset successfully! You can now login with your new password.")
                return redirect('login')
            except ValidationError as e:
                messages.error(request, str(e))
    else:
        form = CustomPasswordResetForm()
    
    return render(request, 'recommender/password_reset.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('cover')

@login_required
def recommendation_form(request):
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            try:
                user_input = form.cleaned_data
                df = pd.read_csv('recommender/data/cloud_data_10000.csv')
                
                encryption_value = 1 if user_input['supports_encryption'] else 0
                filtered_df = df[df['Activity_Field'] == user_input['activity_field']]
                
                if len(filtered_df) == 0:
                    messages.warning(request, f"No providers found for {user_input['activity_field']}. Showing recommendations across all industries.")
                    filtered_df = df
                
                X = filtered_df[["Storage_Needs", "Supports_Encryption", "CPU_Speed", "Price_Per_Hour", "Service_Model_Score"]]
                y = filtered_df["Provider"]

                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)
                model = NearestNeighbors(n_neighbors=1)
                model.fit(X_scaled)

                user_df = pd.DataFrame([{
                    "Storage_Needs": user_input['storage_needs'],
                    "Supports_Encryption": encryption_value,
                    "CPU_Speed": user_input['cpu_speed'],
                    "Price_Per_Hour": user_input['price_per_hour'],
                    "Service_Model_Score": user_input['service_model_score']
                }])

                user_input_scaled = scaler.transform(user_df)
                distance, index = model.kneighbors(user_input_scaled)

                recommended_provider = filtered_df.iloc[index[0][0]]["Provider"]
                provider_details = filtered_df.iloc[index[0][0]].to_dict()
                
               
                recommendation = Recommendation(
                    user=request.user,
                    name=user_input['name'],  # Use the name from form
                    activity_field=user_input['activity_field'],
                    storage_needs=user_input['storage_needs'],
                    supports_encryption=bool(encryption_value),
                    cpu_speed=user_input['cpu_speed'],
                    price_per_hour=user_input['price_per_hour'],
                    service_model_score=user_input['service_model_score'],
                    recommended_provider=recommended_provider,
                    provider_details=provider_details
                )
                recommendation.save()
                
                return render(request, 'recommender/recommendation_result.html', {
                    'user_input': {
                        'Name': user_input['name'], 
                        'Storage_Needs': user_input['storage_needs'],
                        'Supports_Encryption': 'Yes' if encryption_value else 'No',
                        'CPU_Speed': user_input['cpu_speed'],
                        'Price_Per_Hour': user_input['price_per_hour'],
                        'Service_Model_Score': user_input['service_model_score'],
                        'Activity_Field': user_input['activity_field']
                    },
                    'recommended_provider': recommended_provider,
                    'provider_details': provider_details
                })
                
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('recommendation_form')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RecommendationForm()
    
    return render(request, 'recommender/recommendation_form.html', {'form': form})


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
    
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_superuser:
                login(request, user)
             
                request.session['admin_user'] = True  
                return redirect('dashboard')
            else:
                messages.error(request, "Admin privileges required")
        else:
            messages.error(request, "Invalid credentials")
        return redirect('cover')
    return redirect('cover')

@staff_member_required
def dashboard(request):
    if not request.user.is_superuser:  # Extra security layer
        return redirect('cover')
    recommendations = Recommendation.objects.all().order_by('-created_at')
    
    if request.method == 'POST' and 'delete_id' in request.POST:
        try:
            rec = Recommendation.objects.get(id=request.POST['delete_id'])
            rec.delete()
            messages.success(request, "Recommendation deleted successfully")
        except Recommendation.DoesNotExist:
            messages.error(request, "Recommendation not found")
        return redirect('dashboard')
    
    return render(request, 'recommender/dashboard.html', {
        'recommendations': recommendations
    })