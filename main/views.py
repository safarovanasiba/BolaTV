from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Min
from django.views.generic import  TemplateView

from .forms import ArizaForm, TestForm
from .models import Users, Ertaklar, WatchedVideo, Multfilmlar, WatchedMultfilm, Qoshiqlar, WatchedQoshiqlar, \
    Qiziqari_Matematika, WatchedMatematika, Ingliztili, WatchedIngliztili, Badantarbiya, WatchedBadantarbiya, \
    Rasmlar, WatchedRasmlar, TestQuestion, TestResult

# 📌 Kategoriyalarni umumiy qilib yozamiz
VIDEO_CATEGORIES = {
    "ertaklar": (Ertaklar, WatchedVideo),
    "multfilmlar": (Multfilmlar, WatchedMultfilm),
    "qoshiqlar": (Qoshiqlar, WatchedQoshiqlar),
    "matematika": (Qiziqari_Matematika, WatchedMatematika),
    "ingliztili": (Ingliztili, WatchedIngliztili),
    "badantarbiya": (Badantarbiya, WatchedBadantarbiya),
    "rasmlar": (Rasmlar, WatchedRasmlar),
}


# ✅ Foydalanuvchini tekshirish
def is_authenticated(request):
    return request.session.get("user_id") is not None


# ✅ Login qilish
def UsersViews(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = Users.objects.filter(username=username).first()

        if user and check_password(password, user.password):
            request.session["user_id"] = user.id
            return redirect("dashboard")

        return render(request, "login.html", {"error": "Username yoki parol noto‘g‘ri!"})

    return render(request, "login.html")


def dashboard(request):
    user = None
    if is_authenticated(request):
        user = Users.objects.get(id=request.session["user_id"])
    return render(request, "dashboard.html", {"user": user, "video_categories": VIDEO_CATEGORIES})


# ✅ Videolarni ro‘yxatini chiqarish (Barcha kategoriyalar uchun)
def video_list(request, category):
    # if not is_authenticated(request):
    #     return redirect("user")

    user = Users.objects.get(id=request.session["user_id"])

    # Model va ko‘rilgan videolarni aniqlash
    VideoModel, WatchedModel = VIDEO_CATEGORIES.get(category, (None, None))
    if not VideoModel:
        return redirect("dashboard")

    # Foydalanuvchi ko‘rgan videolar
    watched_videos = list(WatchedModel.objects.filter(user=user, watched=True).values_list("video__order", flat=True))

    # Eng birinchi video har doim ochiq bo‘lishi kerak
    min_order = VideoModel.objects.aggregate(min_order=Min("order"))["min_order"]

    # Hamma videolar
    videos = VideoModel.objects.all()

    for video in videos:
        video.can_watch = video.order == min_order or video.order - 1 in watched_videos

    return render(request, "video_list.html", {"videos": videos, "category": category})


# ✅ Videoni ko‘rish (Barcha kategoriyalar uchun)
def watch_video(request, video_id, category):
    # if not is_authenticated(request):
    #     return redirect("user")

    user = Users.objects.get(id=request.session["user_id"])

    # Model va ko‘rilgan videolarni aniqlash
    VideoModel, WatchedModel = VIDEO_CATEGORIES.get(category, (None, None))
    if not VideoModel:
        return redirect("dashboard")

    video = get_object_or_404(VideoModel, id=video_id)

    watched_videos = list(WatchedModel.objects.filter(user=user, watched=True).values_list("video__order", flat=True))

    if video.order == 1 or video.order - 1 in watched_videos:
        WatchedModel.objects.get_or_create(user=user, video=video, watched=True)
        return render(request, "watch_video.html", {"video": video, "category": category})

    return render(request, "video_list.html",
                  {"error": "Avvalgi videoni ko‘rmagansiz!", "videos": VideoModel.objects.all(), "category": category})


# ✅ Logout qilish
def user_logout(request):
    request.session.flush()
    return redirect("user")


def ariza_qoldirish(request):
    if request.method == "POST":
        form = ArizaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ariza_tashlandi")
    else:
        form = ArizaForm()

    return render(request, "ariza_qoldirish.html", {"form": form})


def ariza_tashlandi(request):
    return render(request, "ariza_tashlandi.html")


def test_view(request):
    if not request.session.get("user_id"):
        return redirect("user")

    user = Users.objects.get(id=request.session["user_id"])
    questions = TestQuestion.objects.all()

    if request.method == "POST":
        form = TestForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            for question in questions:
                user_answer = int(form.cleaned_data[f"question_{question.id}"])
                if user_answer == question.correct_option:
                    score += 1

            TestResult.objects.create(user=user, score=score, total_questions=len(questions))
            return redirect("test_result")
    else:
        form = TestForm(questions=questions)

    return render(request, "test.html", {"form": form})


def test_result(request):
    if not request.session.get("user_id"):
        return redirect("user")

    user = Users.objects.get(id=request.session["user_id"])
    result = TestResult.objects.filter(user=user).order_by("-created_at").first()

    return render(request, "test_result.html", {"result": result})

class Home(TemplateView):
    template_name = 'home.html'
