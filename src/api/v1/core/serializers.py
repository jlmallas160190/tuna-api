# apps/navigation/serializers.py

from rest_framework import serializers

from core.models import Menu, Translation


class MenuSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ["id", "key", "label", "icon", "url", "children"]

    def get_label(self, obj):
        language = self.context.get("language", "es")
        translation = obj.translations.filter(language_code=language).first()
        return translation.label if translation else obj.key

    def get_children(self, obj):
        children = obj.children.filter(is_active=True)
        return MenuSerializer(children, many=True).data


class TranslationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ["key", "text"]


class TranslationSerializer(serializers.Serializer):
    language = serializers.CharField(max_length=10)
    items = TranslationModelSerializer(many=True)

    # class Meta:
    #     model = Translation
    #     fields = ["key", "text"]
