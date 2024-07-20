import random
import string

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from smsaero import SmsAeroException

from users.forms import UserRegisterForm, UserForm
from users.models import User
from users.servicies import send_sms, create_session


class RegisterView(CreateView):
    """
    Отображение регистрационной формы пользователя.
    После отправки на телефон приходит СМС с кодом.
    Доступно всем пользователям
    """

    model = User
    form_class = UserRegisterForm
    template_name = "users/user_register_form.html"
    success_url = reverse_lazy('users:phone_verify')

    def form_valid(self, form):
        self.object = form.save()
        phone = int(self.object.phone.as_e164[1:])
        token = ''.join(random.choice(string.digits) for i in range(6))
        self.object.token = token
        self.object.save()
        try:
            send_sms(phone=phone, message=f'Код подтверждения {token}')
            print('Сообщение отправлено')
        except SmsAeroException as e:
            print(f"An error occurred: {e}")
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    Отображение изменения профиля пользователя.
    Доступно только зарегистрированым пользователям
    """

    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')
    login_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def payment_create(request):
    """
    Отображение страницы для прехода на ссылку для оплаты.
    Доступно только зарегистрированым пользователям
    """

    user = request.user
    user.payment_session_id, link = create_session()
    user.save()
    context_data = {'link': link}
    return render(request, 'users/payment_create.html', context_data)


@login_required
def payment_success(request):
    """
    Отображение страницы при успешной оплате
    """

    user = request.user
    user.is_premium = True
    user.save()

    return render(request, 'users/payment_success.html')


@login_required
def payment_cancel(request):
    """
    Отображение страницы при отмены оплаты
    """
    return render(request, 'users/payment_cancel.html')


def phone_verification(request):
    """
    Отображение формы для верификации номера телефона через код из СМС.
    На страницуу переходит после регистрации пользователя
    """
    if request.method == 'POST':
        entered_token = request.POST.get('token', '')
        nick_name = request.POST.get('nick_name', '')
        user = get_object_or_404(User, nick_name=nick_name)
        if str(user.token) == str(entered_token):
            user.is_active = True
            user.save()
            return redirect('users:profile')
        else:
            return HttpResponse("Код подтверждения неверный. Попробуйте еще раз.")
    return render(request, 'users/phone_verify.html')


def generate_new_password(request):
    """
    Создане нового пароля и отправка его по СМС
    """

    user = request.user
    characters = string.ascii_letters + string.digits
    new_password = ''.join(random.choice(characters) for i in range(12))
    phone = int(user.phone.as_e164[1:])
    try:
        send_sms(phone=phone, message=f'Новый пароль {new_password}')
    except SmsAeroException as e:
        print(f"An error occurred: {e}")
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('content:main'))
