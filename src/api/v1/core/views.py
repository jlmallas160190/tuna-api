# apps/navigation/views.py

from collections import defaultdict

from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Menu, Translation

from .serializers import MenuSerializer


class UserMenuView(APIView):

    def get(self, request):
        language = request.GET.get("lang", "es")

        menus = Menu.objects.filter(
            parent__isnull=True, is_active=True
        ).prefetch_related("translations", "children__translations")

        serializer = MenuSerializer(menus, many=True, context={"language": language})

        return Response(serializer.data)


class TranslationListView(APIView):

    def get(self, request):
        result = defaultdict(dict)
        for t in Translation.objects.all():
            result[t.language][t.key] = t.text
        return Response(result)
