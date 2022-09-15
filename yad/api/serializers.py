from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    '''Сериализватор элемента для наследования'''
    type = serializers.ChoiceField(
        choices=[Item.Types.FILE, Item.Types.FOLDER],
        required=True,
    )
    id = serializers.UUIDField(
        required=True,
    )
    url = serializers.CharField(
        required=False,
    )
    size = serializers.IntegerField(
        required=False,
    )
    date = serializers.DateTimeField()

    class Meta:
        fields = ('type', 'id', 'parentId', 'url', 'size', 'date')
        model = Item


class ItemRepresentSerializer(ItemSerializer):
    '''Сериализватор отображения элемента'''
    parentId = serializers.SerializerMethodField()

    def get_parentId(self, obj):
        if obj.parent:
            return obj.parent.id
        else:
            return obj.parent


class ItemCreateSerializer(ItemSerializer):
    '''Сериализватор создания элемента'''
    parentId = serializers.UUIDField(
        # queryset=Item.objects.all(),
        allow_null=True,
        required=True,
    )

    def validate(self, data):
        type = data.get('type')
        url = data.get('url')
        size = data.get('size')
        error_message = {}
        if type == Item.Types.FOLDER:
            # Поле url при импорте папки всегда должно быть равно null
            if url is not None:
                error_message['url'] = 'Should be null for folder'
            # Поле size при импорте папки всегда должно быть равно null
            if size is not None:
                error_message['size'] = 'Should be null for folder'
        elif type == Item.Types.FILE:
            # Поле size для файлов всегда должно быть больше 0
            if size <= 0:
                error_message['size'] = 'Should be greater than 0 for file'
        if error_message:
            raise ValidationError(error_message)
        return data


class ImportsSerializer(serializers.Serializer):
    '''Сериализатор импортирования элементов'''
    items = ItemCreateSerializer(many=True)
    updateDate = serializers.DateTimeField()

    class Meta:
        fields = ('items', 'updateDate')

    @atomic
    def create(self, validated_data):
        items = validated_data.get('items')
        date = validated_data.get('updateDate')
        id_list = []
        for item_data in items:
            item_id = item_data.pop('id')
            # В одном запросе не может быть двух элементов с одинаковым id
            if item_id in id_list:
                raise ValidationError(
                    'One request cannot have two elements with the same id'
                )
            parent_id = item_data.pop('parentId')
            if parent_id:
                parent = Item.objects.filter(id=parent_id)
                if not parent.exists():
                    raise ValidationError(
                        {'parentId': 'Folder with such id doesn\'t exist'}
                    )
                parent = parent[0]
                # Родителем элемента может быть только папка
                if parent.type != Item.Types.FOLDER:
                    raise ValidationError(
                        {'parentId': 'Only folder can be parent'}
                    )
            else:
                parent = None
            Item.objects.update_or_create(
                defaults={
                    'type': item_data.get('type'),
                    'url': item_data.get('url'),
                    'size': item_data.get('size'),
                    'date': item_data.get('date'),
                    'parent': parent,
                },
                id=item_id,
            )
            id_list.append(item_id)
        queryset = Item.objects.filter(id__in=id_list)
        serializer = ItemRepresentSerializer(queryset, many=True)
        return {'items': serializer.data, 'updateDate': date}


class NodesSerializer(serializers.ModelSerializer):
    '''Сериализатор получения элемента'''
    type = serializers.CharField()
    id = serializers.UUIDField()
    size = serializers.IntegerField()
    url = serializers.CharField()
    parentId = serializers.SerializerMethodField()
    date = serializers.DateTimeField()
    children = serializers.SerializerMethodField()

    def get_parentId(self, obj):
        if obj.parent:
            return obj.parent.id
        else:
            return obj.parent

    def get_children(self, obj):
        if obj.type == Item.Types.FILE:
            return None
        else:
            children = Item.objects.filter(parent=obj)
            if children.exists():
                serializer = NodesSerializer(
                    instance=children,
                    many=True
                )
                return serializer.data
            return []

    class Meta:
        fields = (
            'type', 'id', 'size', 'url', 'parentId', 'date', 'children'
        )
        model = Item
