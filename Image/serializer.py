import sys
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers

from .models import UploadImageTest


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadImageTest
        fields = '__all__'

    def create(self, validated_data):
        original_image = validated_data.get('image')

        size = (100, 100)
        with Image.open(original_image) as img:
            img_resized = img.resize(size, Image.NEAREST)

            img_io = BytesIO()
            img_resized.save(img_io, format=img.format)
            img_io.seek(0)

            thumbnail_file = InMemoryUploadedFile(
                img_io,
                'ImageField',
                original_image.name,
                original_image.content_type,
                sys.getsizeof(img_io),
                None
            )

            validated_data['thumbnail'] = thumbnail_file

        return super().create(validated_data)
