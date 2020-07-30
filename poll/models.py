from django.db import models
from django.contrib.auth.models import User
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

class Question(AbstractModel):
    status=models.CharField(default='inactive',max_length=100)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    start_date=models.DateTimeField(null=True)
    end_date=models.DateTimeField(null=True)

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

    def __str__(self):
        return self.user.first_name+"-"+self.choice.title
    