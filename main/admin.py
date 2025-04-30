from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db.models import Count, Sum
from .models import (
    Users, Ertaklar, WatchedVideo, Multfilmlar, WatchedMultfilm,
    Qoshiqlar, WatchedQoshiqlar, Qiziqari_Matematika, WatchedMatematika,
    Ingliztili, WatchedIngliztili, Badantarbiya, WatchedBadantarbiya,
    Rasmlar, WatchedRasmlar, Ariza, TestQuestion, TestResult
)

# 📌 Hamma video turlari uchun umumiy kategoriya
VIDEO_CATEGORIES = {
    "ertaklar": (Ertaklar, WatchedVideo),
    "multfilmlar": (Multfilmlar, WatchedMultfilm),
    "qoshiqlar": (Qoshiqlar, WatchedQoshiqlar),
    "matematika": (Qiziqari_Matematika, WatchedMatematika),
    "ingliztili": (Ingliztili, WatchedIngliztili),
    "badantarbiya": (Badantarbiya, WatchedBadantarbiya),
    "rasmlar": (Rasmlar, WatchedRasmlar),
}

# ✅ **Foydalanuvchi admin paneli (ko'rilgan videolar foizi bilan)**
class UsersAdmin(admin.ModelAdmin):
    list_display = ["username", "is_admin", "created_at", "total_watched_percent"]
    list_filter = ["is_admin", "created_at"]
    search_fields = ["username"]

    def _generate_watched_percent(model, watched_model):
        def watched_percent(self, obj):
            total_videos = model.objects.count()
            watched_videos = watched_model.objects.filter(user=obj, watched=True).count()
            if total_videos == 0:
                return "0%"
            percent = (watched_videos / total_videos) * 100
            return f"{percent:.2f}%"

        return watched_percent

    # Generate watched percentage methods for each category
    for key, (VideoModel, WatchedModel) in VIDEO_CATEGORIES.items():
        func_name = f"watched_{key}_percent"
        locals()[func_name] = _generate_watched_percent(VideoModel, WatchedModel)
        locals()[func_name].short_description = f"{key.capitalize()} (%)"
        list_display.append(func_name)

    # ✅ **Umumiy ko'rilgan videolar foizi**
    def total_watched_percent(self, obj):
        total_percent = 0
        category_count = 0

        for key, (VideoModel, WatchedModel) in VIDEO_CATEGORIES.items():
            total_videos = VideoModel.objects.count()
            watched_videos = WatchedModel.objects.filter(user=obj, watched=True).count()

            if total_videos > 0:
                total_percent += (watched_videos / total_videos) * 100
                category_count += 1

        if category_count == 0:
            return "0%"

        return f"{(total_percent / category_count):.2f}%"

    total_watched_percent.short_description = "Umumiy Ko'rilgan (%)"

# ✅ **Videolar admin paneli (iframe preview bilan)**
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "video_preview", "total_views")
    search_fields = ["title"]
    list_filter = ["order"]

    def video_preview(self, obj):
        """YouTube video previewni admin panelda ko'rsatish"""
        if obj.embed_video():
            return mark_safe(
                f'<iframe width="200" height="100" src="{obj.embed_video()}" frameborder="0" allowfullscreen></iframe>')
        return "No Video"

    video_preview.short_description = "Video Preview"
    
    def get_watched_model(self, obj):
        for key, (VideoModel, WatchedModel) in VIDEO_CATEGORIES.items():
            if isinstance(obj, VideoModel):
                return WatchedModel
        return None
    
    def total_views(self, obj):
        watched_model = self.get_watched_model(obj)
        if watched_model:
            return watched_model.objects.filter(video=obj).aggregate(total=Sum('watch_count'))['total'] or 0
        return 0
    
    total_views.short_description = "Total Views"

# ✅ **Ko'rilgan videolar admin paneli**
class WatchedVideoAdmin(admin.ModelAdmin):
    list_display = ("user", "video", "watched", "watch_count", "watched_at")
    list_filter = ["watched", "watched_at", "user"]
    search_fields = ["user__username", "video__title"]
    raw_id_fields = ["user", "video"]

# 📌 **Admin panelga hamma modellarni ro'yxatdan o'tkazamiz**
admin.site.register(Users, UsersAdmin)

# Register video models
for key, (VideoModel, _) in VIDEO_CATEGORIES.items():
    admin.site.register(VideoModel, VideoAdmin)

# Register watched video models
for _, (_, WatchedModel) in VIDEO_CATEGORIES.items():
    admin.site.register(WatchedModel, WatchedVideoAdmin)

class ArizaAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone_number", "created_at")
    search_fields = ("full_name", "phone_number")
    list_filter = ("created_at",)

class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "correct_option")

class TestResultAdmin(admin.ModelAdmin):
    list_display = ("user", "score", "total_questions", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username",)

admin.site.register(TestQuestion, TestQuestionAdmin)
admin.site.register(TestResult, TestResultAdmin)
admin.site.register(Ariza, ArizaAdmin)