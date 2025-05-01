# 📁 views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Min
from django.views.generic import TemplateView
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from .models import *
from .forms import ArizaForm, TestForm, LoginForm, RegisterForm

# 📌 Video kategoriyalarini lug'at ko'rinishida belgilaymiz
VIDEO_CATEGORIES = {
    "ertaklar": (Ertaklar, WatchedVideo),
    "multfilmlar": (Multfilmlar, WatchedMultfilm),
    "qoshiqlar": (Qoshiqlar, WatchedQoshiqlar),
    "matematika": (Qiziqari_Matematika, WatchedMatematika),
    "ingliztili": (Ingliztili, WatchedIngliztili),
    "badantarbiya": (Badantarbiya, WatchedBadantarbiya),
    "rasmlar": (Rasmlar, WatchedRasmlar),
}

# 🔐 Login required decorator
def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

# 👤 Login view
def login_view(request):
    if 'user_id' in request.session:
        return redirect('dashboard')
        
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                user = Users.objects.get(username=username)
                if check_password(password, user.password):
                    # Login successful
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    request.session['is_admin'] = user.is_admin
                    return redirect('dashboard')
                else:
                    form.add_error('password', 'Noto\'g\'ri parol')
            except Users.DoesNotExist:
                form.add_error('username', 'Bunday foydalanuvchi mavjud emas')
    else:
        form = LoginForm()
    
    return render(request, "login.html", {"form": form})

# 📝 Register view
def register_view(request):
    if 'user_id' in request.session:
        return redirect('dashboard')
        
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto login after registration
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['is_admin'] = user.is_admin
            return redirect('dashboard')
    else:
        form = RegisterForm()
    
    return render(request, "register.html", {"form": form})

# 🚪 Logout view
def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        del request.session['username']
        if 'is_admin' in request.session:
            del request.session['is_admin']
    return redirect('home')

# 🏠 Bosh sahifa (kategoriya ro'yxati bilan)
@login_required
@cache_page(60 * 5)  # Cache for 5 minutes
def dashboard(request):
    user_id = request.session.get("user_id")
    context = {"video_categories": VIDEO_CATEGORIES}
    return render(request, "dashboard.html", context)

# 📺 Videolar ro'yxati (kategoriya bo'yicha ko'rilgan holatini aniqlash)
@login_required
@cache_page(60 * 5)  # Cache for 5 minutes
def video_list(request, category):
    VideoModel, WatchedModel = VIDEO_CATEGORIES.get(category, (None, None))
    if not VideoModel or not WatchedModel:
        return redirect("dashboard")

    user_id = request.session.get('user_id')
    user = get_object_or_404(Users, id=user_id)

    # Use cache for watched IDs
    cache_key = f'watched_ids_{category}_{user_id}'
    korilgan_idlar = cache.get(cache_key)
    
    if korilgan_idlar is None:
        # Faqat video_id'larni olamiz (ko'rilganlar)
        korilgan_idlar = list(
            WatchedModel.objects.filter(user=user, watched=True).values_list("video_id", flat=True)
        )
        cache.set(cache_key, korilgan_idlar, 300)  # Cache for 5 minutes

    # Use select_related to reduce database queries
    videolar = VideoModel.objects.all().select_related()
    min_order = VideoModel.objects.aggregate(min_order=Min("order"))["min_order"]

    # Prepare a dictionary of watched videos for faster lookup
    watched_dict = {}
    if korilgan_idlar:
        watched_videos = WatchedModel.objects.filter(
            user=user, 
            video_id__in=[v.id for v in videolar]
        ).select_related('video')
        
        for watched in watched_videos:
            watched_dict[watched.video_id] = {
                'watch_count': watched.watch_count,
                'watched': watched.watched
            }

    # Har bir video uchun "ko'rish mumkin" flagini belgilaymiz
    for video in videolar:
        video.can_watch = video.order == min_order or video.order - 1 in [
            v.order for v in VideoModel.objects.filter(id__in=korilgan_idlar)
        ]
        # Add watch count for each video from our dictionary
        if video.id in watched_dict:
            video.watch_count = watched_dict[video.id]['watch_count']
            video.watched = watched_dict[video.id]['watched']
        else:
            video.watch_count = 0
            video.watched = False

    context = {"videos": videolar, "category": category}
    return render(request, "video_list.html", context)

# ▶️ Video ko'rish (va uni "ko'rilgan" deb belgilash)
@login_required
def watch_video(request, video_id, category):
    VideoModel, WatchedModel = VIDEO_CATEGORIES.get(category, (None, None))
    if not VideoModel or not WatchedModel:
        return redirect("dashboard")

    user_id = request.session.get('user_id')
    user = get_object_or_404(Users, id=user_id)
    video = get_object_or_404(VideoModel, id=video_id)

    # Clear cache for this user's video list to ensure fresh data
    cache_key = f'video_list_{category}_{user_id}'
    cache.delete(cache_key)

    # Avvalgi videoni ko'rganmi yoki bu birinchi video ekanligini tekshiramiz
    korilgan_orderlar = list(
        VideoModel.objects.filter(
            id__in=WatchedModel.objects.filter(user=user, watched=True).values_list("video_id", flat=True)
        ).values_list("order", flat=True)
    )

    # Always allow watching the video, but only mark as watched if conditions are met
    watched_entry, created = WatchedModel.objects.get_or_create(user=user, video=video)
    
    # Increment watch count regardless of whether it's marked as watched
    watched_entry.watch_count += 1
    
    # Mark as watched only if it's the first video or previous one was watched
    if video.order == 1 or (video.order - 1 in korilgan_orderlar):
        watched_entry.watched = True
    
    # Always save to update the watch_count and watched_at timestamp
    watched_entry.save()
    
    return render(request, "watch_video.html", {
        "video": video, 
        "category": category,
        "watch_count": watched_entry.watch_count,
        "watched": watched_entry.watched
    })

# 📝 Ariza formasi
@login_required
def ariza_qoldirish(request):
    if request.method == "POST":
        form = ArizaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ariza_tashlandi")
    else:
        form = ArizaForm()

    return render(request, "ariza_qoldirish.html", {"form": form})

# ✅ Ariza yuborilgan sahifa
@login_required
def ariza_tashlandi(request):
    return render(request, "ariza_tashlandi.html")

# 🧠 Test sahifasi
@login_required
def test_view(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(Users, id=user_id)
    savollar = TestQuestion.objects.all()

    if request.method == "POST":
        form = TestForm(request.POST, questions=savollar)
        if form.is_valid():
            baho = 0
            for savol in savollar:
                javob = int(form.cleaned_data[f"question_{savol.id}"])
                if javob == savol.correct_option:
                    baho += 1

            TestResult.objects.create(
                user=user,
                score=baho, 
                total_questions=len(savollar)
            )
            return redirect("test_result")
    else:
        form = TestForm(questions=savollar)

    return render(request, "test.html", {"form": form})

# ✅ Test natijalari sahifasi
@login_required
def test_result(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(Users, id=user_id)
    natija = TestResult.objects.filter(user=user).order_by("-created_at").first()
    return render(request, "test_result.html", {"result": natija})

# 🏠 Home sahifa (class-based view)
class Home(TemplateView):
    template_name = 'home.html'
    
    def dispatch(self, request, *args, **kwargs):
        if 'user_id' in request.session:
            return HttpResponseRedirect(reverse('dashboard'))
        return super().dispatch(request, *args, **kwargs)

@cache_page(60 * 15)  # Cache for 15 minutes
def index(request):
    """Main homepage view"""
    return render(request, 'index.html')

@cache_page(60 * 60)  # Cache for 1 hour
def simple_text_response(request):
    """A simple text response that doesn't require templates"""
    return HttpResponse("BolaTV is running. Visit /admin/ for administration.", content_type="text/plain")
