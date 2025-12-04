from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

User = get_user_model()

@receiver(post_migrate)
def crear_superusuario_automatico(sender, **kwargs):
    if sender.name != "auth" and sender.name != settings.AUTH_USER_MODEL.split(".")[0]:
        return

    admin_username = settings.ADMIN_USERNAME
    admin_email = settings.ADMIN_EMAIL
    admin_password = settings.ADMIN_PASSWORD

    if not User.objects.filter(username=admin_username).exists():
        print("⚠️ Creando superusuario automático en Render...")
        User.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password
        )
        print("✅ Superusuario creado.")
    else:
        print("ℹ️ Superusuario ya existe.")
