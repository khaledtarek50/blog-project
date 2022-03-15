from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    followers = models.ManyToManyField(
        "User", blank=True, symmetrical=False, related_name="following"
    )

    def follow(self, user):
        self.following.add(user)

    def unfollow(self, user):
        self.following.remove(user)

    def count_followers(self):
        return self.followers.count()

    def count_following(self):
        return self.following.count()


# followers > user.followers.all()

# following > user.following.all()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self) -> str:
        return f"{self.user.username} Profile"
