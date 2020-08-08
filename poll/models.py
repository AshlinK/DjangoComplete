from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation

# Create your models here.
class AbstractModel(models.Model):
    title=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract=True
        managed=False
        ordering=['created_at']

class QuestionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='active')

    def all_objects(self):
        return super().get_queryset()

    def inactive(self):
        self.all_objects().filter(status='inactive')

class Comment(models.Model):
    text=models.TextField(null=False,blank=False)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')

    def __str__(self):
        return self.text[:10]



class Question(AbstractModel):
    status=models.CharField(default='inactive',max_length=100)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    start_date=models.DateTimeField(null=True)
    end_date=models.DateTimeField(null=True)
    comments=GenericRelation(Comment,related_query_name="question")

    objects=QuestionManager()

    class Meta:
        verbose_name_plural="questions"

    @property
    def choices(self):
        return self.choice_set.all()   

class Choice(AbstractModel):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural="choices"

    @property
    def vote_counts(self):
        return self.answer_set.count()


class Answer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    choice=models.ForeignKey(Choice,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    comments=GenericRelation(Comment,related_query_name="answer")

    def __str__(self):
        return self.user.first_name+"-"+self.choice.title



    