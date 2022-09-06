from distutils.command.upload import upload
from django.db import models

# Create your models here.
# pqsl - происходит авторицация  Model - связывает с бд, автризует

class Category(models.Model):
    name=models.CharField(max_length=255)
    # blank=True,null=True  - необяз заполнять
    parent=models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True,null=True)

    def __str__(self):
        return f'{self.name} -> {self.parent}' if self.parent else self.name


class Post(models.Model):
    # related_name - вместо join
    # models.PROTECT   SET_NULL   SET_DEFAULT
    title=models.CharField(max_length=255, unique=True, verbose_name='Название')
    body=models.TextField(blank=True)
    owner=models.ForeignKey('auth.User',related_name='posts', on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,related_name='posts',null=True)
    preview=models.ImageField(upload_to='images/',null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f'{self.owner} -> {self.title}'

    class Meta:
        # если не запятая подумает что строка
        ordering=('created_at',)
        verbose_name='Посты'
        verbose_name_plural='Пост'
        
class PostImages(models.Model):
    title=models.CharField(max_length=150,blank=True)
    image=models.ImageField(upload_to='images/')
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')

    @staticmethod
    def generate_name():
        from random import randint
        return 'image'+str(randint(100000,999999))

    def save(self,*args,**kwargs):
        self.title=self.generate_name()
        return super(PostImages, self).save(*args,**kwargs)

class Comment(models.Model):
    owner=models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    post=models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} -> {self.post} -> {self.created_at}'

class Like(models.Model):
    owner=models.ForeignKey('auth.User', related_name='liked', on_delete=models.CASCADE)
    post=models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    
    class Meta:
        unique_together=['post','owner']

class Favourites (models.Model):
    owner=models.ForeignKey('auth.User', related_name='favourites', on_delete=models.CASCADE)
    post=models.ForeignKey(Post, related_name='favourites', on_delete=models.CASCADE)
    class Meta:
        unique_together=['post','owner']
