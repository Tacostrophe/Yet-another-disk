import uuid

from django.db import models


def calc_folder_size(item):
    children = Item.objects.filter(parent=item)
    size = 0
    # Проверка для удаления
    if children.exists():
        size = children.aggregate(sum_size=models.Sum('size'))['sum_size']
    item.size = size
    item.save()
    # if item.parent:
    #     calc_folder_size(item.parent)


class Item(models.Model):
    '''Модель файла/папкИ'''
    class Types(models.TextChoices):
        FILE = 'FILE'
        FOLDER = 'FOLDER'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        null=False,
        unique=True,
    )
    type = models.CharField(
        max_length=6,
        choices=Types.choices,
        # editable=False,
    )
    url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    date = models.DateTimeField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='folder',
        null=True,
        blank=True,
        default=None,
        # validators=(validate_parent,)
    )
    size = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if self.size is None:
            self.size = 0
        super(Item, self).save(*args, **kwargs)
        if self.parent:
            self.parent.date = self.date
            calc_folder_size(self.parent)

    def delete(self, *args, **kwargs):
        parent = self.parent
        super(Item, self).delete(*args, **kwargs)
        if parent:
            calc_folder_size(parent)

    def __str__(self):
        return f'{self.type} - {self.id}'
