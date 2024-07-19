from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView

from content.forms import ContentForm
from content.models import Content
from users.models import User


class MainView(TemplateView):
    """
    Отображение главной страницы с подсчетом статистики.
    Доступно всем пользователям
    """

    template_name = "content/main.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['total_content'] = Content.objects.all().count()
        context_data['premium_content'] = Content.objects.filter(is_premium='True').count()
        context_data['all_users'] = User.objects.all().count()
        context_data['premium_user'] = User.objects.filter(is_premium='True').count()
        return context_data


class ContentCreateView(LoginRequiredMixin, CreateView):
    """
    Отображение создания публикации на основе формы.
    Доступно только зарегистрированным пользователям
    """

    model = Content
    form_class = ContentForm
    success_url = reverse_lazy('content:list')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ContentListView(LoginRequiredMixin, ListView):
    """
    Отображение списка публкаций пользователя.
    Доступно только зарегистрированным пользователям
    """

    model = Content
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Content.objects.all()
        else:
            return Content.objects.filter(author=self.request.user)


class ContentDetailView(DetailView):
    """
    Отображение детальной информации публикации.
    Доступно всем пользователям
    """

    model = Content
    login_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class ContentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Отображение изменения публкации на основе формы.
    Доступно только авторам публикации или суперпользователю
    """

    model = Content
    form_class = ContentForm
    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse('content:view', args=[self.kwargs.get('pk')])

    def test_func(self):
        content = self.get_object()
        return self.request.user.is_superuser or self.request.user == content.author

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ContentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Отображение удаления публкации на основе формы.
    Доступно только авторам публикации или суперпользователю
    """

    model = Content
    success_url = reverse_lazy('content:list')
    login_url = reverse_lazy('users:login')

    def test_func(self):
        content = self.get_object()
        return self.request.user.is_superuser or self.request.user == content.author


class ReaderListView(ListView):
    """
    Отображение списка всех доступных публкаций.
    Доступно всем пользователям
    Если пользователь оплатил подписку, то он может смотреть все записи,
    если нет или он вовсе не зарегистрирован, то только бесплатные
    """

    model = Content
    template_name = "content/reader_list.html"

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_premium:
            return Content.objects.all()
        else:
            return Content.objects.exclude(is_premium=True)
