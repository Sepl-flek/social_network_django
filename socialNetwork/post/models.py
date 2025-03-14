from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    header = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    likes = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='my_post')
    data = models.DateTimeField(auto_now_add=True)

    readers = models.ManyToManyField(User, through='UserPostRelation', related_name='posts')

    def update_likes(self):
        """Пересчитывает количество лайков"""
        self.likes = self.user_post_relations.filter(is_like=True).count()
        self.save()

    def __str__(self):
        if self.header is not None:
            return f'{self.header} id:{self.pk}'
        return f'id: {self.pk}'


class UserPostRelation(models.Model):
    rating_choice = (
        (1, 'Bad'),
        (2, 'Nice'),
        (3, 'Good'),
        (4, 'Perfect'),
        (5, 'Amazing'),
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='user_post_relations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=False)
    is_bookmark = models.BooleanField(default=False)
    rating = models.SmallIntegerField(choices=rating_choice, null=True)

    def __str__(self):
        return f'{self.user}, {self.post}'
