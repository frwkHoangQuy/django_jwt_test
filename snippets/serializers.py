from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers

from User.serializers import UserSerializer
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField()
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
    user = UserSerializer(read_only=True)
    image = serializers.ImageField(required=False)
    thumbnail = serializers.ImageField(read_only=True)

    def create(self, validated_data):
        original_image = validated_data.get('image', None)

        if original_image:
            try:
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
                        len(img_io.getvalue()),
                        None
                    )
                    validated_data['thumbnail'] = thumbnail_file
            except Exception as e:
                raise serializers.ValidationError(f"Error processing image: {e}")

        request = self.context.get('request')
        return Snippet.objects.create(**validated_data, user=request.user)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)

        image = validated_data.get('image', None)
        if image:
            instance.image = image

        instance.save()
        return instance
