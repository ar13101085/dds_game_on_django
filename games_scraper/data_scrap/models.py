import datetime

from django.db import models


# Create your models here.

class Genre(models.Model):
    id = models.AutoField(primary_key=True);
    name = models.CharField(max_length=100,unique=True);
    def __str__(self):
        return str(self.id)+" "+self.name;


class Game(models.Model):
    id = models.CharField(primary_key=True, max_length=100);
    icon = models.CharField(max_length=300);
    title = models.CharField(max_length=200);
    description = models.CharField(max_length=200);
    genre = models.ManyToManyField(Genre, blank=True);
    def __str__(self):
        return str(self.id);
class GameUser(models.Model):
    id=models.AutoField(primary_key=True)
    userName=models.CharField(max_length=100)
    userPhoto=models.ImageField()
    time=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    def __str__(self):
        return str(self.id)+" "+self.userName+" "+self.userPhoto.url;
class Review(models.Model):
    id=models.AutoField(primary_key=True);
    comment=models.TextField(default='');
    rating=models.IntegerField(default=0);
    game=models.ForeignKey(Game,blank=True,null=True);
    user=models.ForeignKey(GameUser,default=None);
    time=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    def __str__(self):
        return str(self.id)+" "+self.user.userName+" "+self.comment+" "+str(self.rating)
class Play(models.Model):
    id=models.AutoField(primary_key=True);
    user=models.ForeignKey(GameUser,blank=True)
    game=models.ForeignKey(Game,blank=True,null=True)
    time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    def __str__(self):
        return str(self.id)+" "+self.user.userName+" "+self.game.title