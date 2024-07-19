from django import forms

from content.models import Content


class StyleForMixin:
    """
    Миксин класс для отображения форм
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ContentForm(StyleForMixin, forms.ModelForm):
    """
    Класс для отображения формы модели публикации
    """

    class Meta:
        model = Content
        exclude = ['created_at', 'views_count', 'author']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        if not self.user.is_premium:
            del self.fields['is_premium']
