from django.db import models
from model_utils.models import TimeStampedModel

class Task(TimeStampedModel):
    title = models.CharField('Título', max_length=150,blank = False,null = False)
    description = models.TextField('Descripción',blank = False,null = False)
    datetime = models.DateTimeField(verbose_name="fecha y hora",blank = False,null = False)
    done = models.BooleanField(default=False, verbose_name="Finalizada",blank = False,null = False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE,blank = False,null = False)

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'

    def __str__(self):
        return self.title
