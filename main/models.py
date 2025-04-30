from django.db import models
from django.contrib.auth.hashers import make_password
from urllib.parse import urlparse, parse_qs

class Users(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_sha256$"):  # Check if password is not hashed
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username

class Ertaklar(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    order = models.PositiveIntegerField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.order:
            last_video = Ertaklar.objects.order_by('-order').first()
            self.order = (last_video.order + 1) if last_video else 1
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title}"

    def embed_video(self):
        """YouTube URL'dan video ID ni ajratib olib, iframe uchun URL hosil qiladi."""
        parsed_url = urlparse(self.video_url)
        video_id = None

        if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
            query_params = parse_qs(parsed_url.query)
            video_id = query_params.get("v", [None])[0]
        elif parsed_url.hostname in ["youtu.be"]:
            video_id = parsed_url.path.lstrip("/")

        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return None

class WatchedVideo(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    video = models.ForeignKey(Ertaklar, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    watched_at = models.DateTimeField(auto_now=True)
    watch_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        status = "Ko'rilgan" if self.watched else "Ko'rilmagan"
        return f"{self.user.username} - {self.video.title} ({status})"

    class Meta:
        unique_together = ('user', 'video')

class Multfilmlar(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    order = models.PositiveIntegerField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.order:
            last_video = Multfilmlar.objects.order_by('-order').first()
            self.order = (last_video.order + 1) if last_video else 1
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title}"

    def embed_video(self):
        """YouTube URL'dan video ID ni ajratib olib, iframe uchun URL hosil qiladi."""
        parsed_url = urlparse(self.video_url)
        video_id = None

        if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
            query_params = parse_qs(parsed_url.query)
            video_id = query_params.get("v", [None])[0]
        elif parsed_url.hostname in ["youtu.be"]:
            video_id = parsed_url.path.lstrip("/")

        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return None

class WatchedMultfilm(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    video = models.ForeignKey(Multfilmlar, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    watched_at = models.DateTimeField(auto_now=True)
    watch_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        status = "Ko'rilgan" if self.watched else "Ko'rilmagan"
        return f"{self.user.username} - {self.video.title} ({status})"

    class Meta:
        unique_together = ('user', 'video')

class Qoshiqlar(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    order = models.PositiveIntegerField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.order:
            last_video = Qoshiqlar.objects.order_by('-order').first()
            self.order = (last_video.order + 1) if last_video else 1
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title}"

    def embed_video(self):
        """YouTube URL'dan video ID ni ajratib olib, iframe uchun URL hosil qiladi."""
        parsed_url = urlparse(self.video_url)
        video_id = None

        if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
            query_params = parse_qs(parsed_url.query)
            video_id = query_params.get("v", [None])[0]
        elif parsed_url.hostname in ["youtu.be"]:
            video_id = parsed_url.path.lstrip("/")

        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return None

class WatchedQoshiqlar(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    video = models.ForeignKey(Qoshiqlar, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    watched_at = models.DateTimeField(auto_now=True)
    watch_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        status = "Ko'rilgan" if self.watched else "Ko'rilmagan"
        return f"{self.user.username} - {self.video.title} ({status})"

    class Meta:
        unique_together = ('user', 'video')

class Qiziqari_Matematika(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    order = models.PositiveIntegerField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.order:
            last_video = Qiziqari_Matematika.objects.order_by('-order').first()
            self.order = (last_video.order + 1) if last_video else 1
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title}"

    def embed_video(self):
        """YouTube URL'dan video ID ni ajratib olib, iframe uchun URL hosil qiladi."""
        parsed_url = urlparse(self.video_url)
        video_id = None

        if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
            query_params = parse_qs(parsed_url.query)
            video_id = query_params.get("v", [None])[0]
        elif parsed_url.hostname in ["youtu.be"]:
            video_id = parsed_url.path.lstrip("/")

        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return None

class WatchedMatematika(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    video = models.ForeignKey(Qiziqari_Matematika, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    watched_at = models.DateTimeField(auto_now=True)
    watch_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        status = "Ko'rilgan" if self.watched else "Ko'rilmagan"
        return f"{self.user.username} - {self.video.title} ({status})"

    class Meta:
        unique_together = ('user', 'video')

class Ingliztili(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    order = models.PositiveIntegerField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.order:
            last_video = Ingliztili.objects.order_by('-order').first()
            self.order = (last_video.order + 1) if last_video else 1
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title}"

    def embed_video(self):
        """YouTube URL'dan video ID ni ajratib olib, iframe uchun URL hosil qiladi."""
        parsed_url = urlparse(self.video_url)
        video_id = None

        if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
            query_params = parse_qs(parsed_url.query)
            video_id = query_params.get("v", [None])[0]
        elif parsed_url.hostname in ["youtu.be"]:
            video_id = parsed_url.path.lstrip("/")

        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return None

class WatchedIngliztili(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    video = models.ForeignKey(Ingliztili, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    watched_at = models.DateTimeField(auto_now=True)
    watch_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        status = "Ko'rilgan" if self.watched else "Ko'rilmagan"
        return f"{self.user.username} - {self.video.title} ({status})"

    class Meta:
        unique_together = ('user', 'video')

class Badantarbiya(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    order = models.PositiveIntegerField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.order:
            last_video = Badantarbiya.objects.order_by('-order').first()
            self.order = (last_video.order + 1) if last_video else 1
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title}"

    def embed_video(self):
        """YouTube URL'dan video ID ni ajratib olib, iframe uchun URL hosil qiladi."""
        parsed_url = urlparse(self.video_url)
        video_id = None

        if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
            query_params = parse_qs(parsed_url.query)
            video_id = query_params.get("v", [None])[0]
        elif parsed_url.hostname in ["youtu.be"]:
            video_id = parsed_url.path.lstrip("/")

        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return None

class WatchedBadantarbiya(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    video = models.ForeignKey(Badantarbiya, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    watched_at = models.DateTimeField(auto_now=True)
    watch_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        status = "Ko'rilgan" if self.watched else "Ko'rilmagan"
        return f"{self.user.username} - {self.video.title} ({status})"

    class Meta:
        unique_together = ('user', 'video')

class Rasmlar(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    order = models.PositiveIntegerField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.order:
            last_video = Rasmlar.objects.order_by('-order').first()
            self.order = (last_video.order + 1) if last_video else 1
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title}"

    def embed_video(self):
        """YouTube URL'dan video ID ni ajratib olib, iframe uchun URL hosil qiladi."""
        parsed_url = urlparse(self.video_url)
        video_id = None

        if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
            query_params = parse_qs(parsed_url.query)
            video_id = query_params.get("v", [None])[0]
        elif parsed_url.hostname in ["youtu.be"]:
            video_id = parsed_url.path.lstrip("/")

        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return None

class WatchedRasmlar(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    video = models.ForeignKey(Rasmlar, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    watched_at = models.DateTimeField(auto_now=True)
    watch_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        status = "Ko'rilgan" if self.watched else "Ko'rilmagan"
        return f"{self.user.username} - {self.video.title} ({status})"

    class Meta:
        unique_together = ('user', 'video')

class Ariza(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class TestQuestion(models.Model):
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.IntegerField(choices=[(1, "A"), (2, "B"), (3, "C"), (4, "D")])

    def __str__(self):
        return self.question_text

class TestResult(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"{username} - {self.score}/{self.total_questions}"
