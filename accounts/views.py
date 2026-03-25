import json
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import User


@method_decorator(csrf_exempt, name='dispatch')
class SignupView(View):
    def post(self, request):
        try:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)

            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            if not username or not email or not password:
                return JsonResponse({"error": "All fields required"}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already exists"}, status=400)

            hashed_password = make_password(password)

            User.objects.create(
                username=username,
                email=email,
                password=hashed_password
            )

            return JsonResponse({"message": "User created successfully"}, status=201)

        except Exception:
            return JsonResponse({"error": "Something went wrong"}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        try:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)

            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return JsonResponse({"error": "All fields required"}, status=400)

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=404)

            if not check_password(password, user.password):
                return JsonResponse({"error": "Invalid password"}, status=400)

            return JsonResponse({"message": "Login successful"}, status=200)

        except Exception:
            return JsonResponse({"error": "Something went wrong"}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class GetUsersView(View):
    def get(self, request):
        try:
            users = User.objects.all()

            data = [
                {
                    "username": user.username,
                    "email": user.email
                }
                for user in users
            ]

            return JsonResponse(data, safe=False)

        except Exception:
            return JsonResponse({"error": "Something went wrong"}, status=500)