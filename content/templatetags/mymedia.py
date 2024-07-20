from django import template

register = template.Library()


@register.simple_tag()
def mymedia(data):
    """
    Тег для направления пути к медиа файлам
    """

    if data:
        return f'/media/{data}'
    return '/media/content/null.jpg'
