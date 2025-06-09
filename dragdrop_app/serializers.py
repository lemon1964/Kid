from rest_framework import serializers
from .models import DragDropTask, DragDropName, DragDropType, Container, Item
from quiz_app.serializers import ImageSerializer, MusicSerializer

class DragDropTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DragDropType
        fields = ['id', 'type', 'slug']
        

class DragDropNameSerializer(serializers.ModelSerializer):
    type = DragDropTypeSerializer(read_only=True)

    class Meta:
        model = DragDropName
        fields = ['id', 'name', 'slug', 'type']

class ContainerSerializer(serializers.ModelSerializer):
    image_url = ImageSerializer(read_only=True)

    class Meta:
        model = Container
        fields = ['id', 'title', 'condition', 'image_url', 'visibility_text', 'alt_text']

class ItemSerializer(serializers.ModelSerializer):
    image_url = ImageSerializer(read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'text', 'condition', 'image_url', 'visibility_text', 'alt_text']

class DragDropTaskSerializer(serializers.ModelSerializer):
    name = DragDropNameSerializer(read_only=True)
    music = MusicSerializer(read_only=True)
    containers = ContainerSerializer(many=True, read_only=True)
    items = ItemSerializer(many=True, read_only=True)
    background_image = serializers.SerializerMethodField()
    next_task = serializers.SerializerMethodField()

    class Meta:
        model = DragDropTask
        fields = ['id', 'name', 'description', 'replacement', 'background_image', 'music', 'containers', 'items', 'slug', 'next_task']
        
    def get_background_image(self, obj):
        """Возвращает file_url, если фон существует"""
        if obj.background_image:
            return obj.background_image.file.url
        return None
    
    def get_next_task(self, obj):
        """
        Возвращает список задач, связанных как "следующая задача".
        Теперь включает `type`, `name` и `slug` для корректных переходов.
        """
        return [
            {
                "id": task.id,
                "type": task.name.type.slug,
                "name": task.name.slug,
                "slug": task.slug
            }
            for task in obj.next_task.all()
        ]
    