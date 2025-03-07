from django.core import serializers
from django.contrib.auth import get_user_model
import json

User = get_user_model()
users = User.objects.all()

# Сериализуем данные с отступами
users_json = serializers.serialize('json', users, indent=4)

# Убедитесь, что папка scripts_data существует
with open('scripts_data/users_export.json', 'w') as f:
    f.write(users_json)
