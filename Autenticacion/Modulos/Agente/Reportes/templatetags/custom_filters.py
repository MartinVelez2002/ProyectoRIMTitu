from django import template

register = template.Library()

@register.filter
def is_image(file_url):
    """Devuelve True si el archivo es una imagen basada en su extensión."""
    return file_url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))

@register.filter
def is_video(file_url):
    """Devuelve True si el archivo es un video basado en su extensión."""
    return file_url.lower().endswith(('.mp4', '.webm', '.avi'))