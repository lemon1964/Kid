from rest_framework import serializers
from .models import PixiTaskType, PixiTask, PixiObject, PixiSVG, PixiImage
from quiz_app.serializers import ImageSerializer, MusicSerializer


class PixiTaskTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PixiTaskType
        fields = ["id", "type", "slug"]


class PixiObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PixiObject
        fields = ["id", "color", "shape", "is_correct"]


class PixiSVGSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = PixiSVG
        fields = ["id", "title", "file_url"]

    def get_file_url(self, obj):
        return obj.file.url if obj.file else None


class PixiImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PixiImage
        fields = ["id", "image_url", "is_correct"]

    def get_image_url(self, obj):
        return obj.image.file.url if obj.image and obj.image.file else None


class PixiTaskSerializer(serializers.ModelSerializer):
    type = PixiTaskTypeSerializer(read_only=True)
    objects = PixiObjectSerializer(many=True, read_only=True)
    svg_images = PixiSVGSerializer(many=True, read_only=True)
    pixi_images = PixiImageSerializer(many=True, read_only=True)
    music = MusicSerializer(read_only=True)
    page_background = serializers.SerializerMethodField()
    pixi_background = serializers.SerializerMethodField()

    class Meta:
        model = PixiTask
        fields = ["id", "title", "description", "task_mode", "slug", "type", "objects", "svg_images", "pixi_images", 'music', "animation","page_background", "pixi_background"]
        
    def get_page_background(self, obj):
        """Возвращает file_url, если фон существует"""
        if obj.page_background:
            return obj.page_background.file.url
        return None

    def get_pixi_background(self, obj):
        """Возвращает file_url, если фон существует"""
        if obj.pixi_background:
            return obj.pixi_background.file.url
        return None