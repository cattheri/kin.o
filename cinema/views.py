from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Movie, WatchLater, UserProfile
from .forms import RegistrationForm, LoginForm, WatchLaterForm


# =========================
# ГЛАВНАЯ СТРАНИЦА
# =========================

def home(request):
    return render(request, 'index.html')


# =========================
# КАТАЛОГ ФИЛЬМОВ
# =========================

def showcase(request):

    movies = Movie.objects.all()

    saved_movie_ids = []

    if request.user.is_authenticated:
        saved_movie_ids = list(
            request.user.watchlater_items.values_list(
                'movie_id',
                flat=True
            )
        )

    return render(request, 'showcase.html', {
        'movies': movies,
        'saved_movie_ids': saved_movie_ids
    })


# =========================
# РЕГИСТРАЦИЯ
# =========================

def registration(request):

    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            pass
        else:
            return redirect('profile')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                'Регистрация прошла успешно!'
            )

            return redirect('profile')

    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {
        'form': form
    })


# =========================
# АВТОРИЗАЦИЯ
# =========================

def auth(request):

    if request.user.is_authenticated:

        if request.user.is_staff or request.user.is_superuser:
            pass
        else:
            return redirect('profile')

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():

            identifier = form.cleaned_data['login']
            password = form.cleaned_data['password']

            user_by_identifier = User.objects.filter(
                username__iexact=identifier
            ).first()

            if user_by_identifier is None:
                user_by_identifier = User.objects.filter(
                    email__iexact=identifier
                ).first()

            if user_by_identifier is not None:

                user = authenticate(
                    request,
                    username=user_by_identifier.username,
                    password=password
                )

                if user is not None:

                    if user.is_staff or user.is_superuser:
                        form.add_error(
                            None,
                            'Администратор должен входить через панель управления.'
                        )

                    else:
                        login(request, user)

                        messages.success(
                            request,
                            'Вы успешно вошли в аккаунт!'
                        )

                        return redirect('profile')

                else:
                    form.add_error(
                        None,
                        'Неверный логин, email или пароль.'
                    )

            else:
                form.add_error(
                    None,
                    'Неверный логин, email или пароль.'
                )

    else:
        form = LoginForm()

    return render(request, 'auth.html', {
        'form': form
    })

# =========================
# ВЫХОД ИЗ АККАУНТА
# =========================

@require_POST
def logout_view(request):

    logout(request)

    messages.success(
        request,
        'Вы вышли из аккаунта.'
    )

    return redirect('home')


# =========================
# СТРАНИЦА ОТДЕЛЬНОГО ФИЛЬМА
# =========================

def movie_detail(request, movie_id):

    movie = get_object_or_404(
        Movie,
        id=movie_id
    )

    movie_in_watchlater = False

    if request.user.is_authenticated:

        movie_in_watchlater = WatchLater.objects.filter(
            user=request.user,
            movie=movie
        ).exists()

    movie_frames = movie.frames.all()

    return render(request, 'movie_detail.html', {
        'movie': movie,
        'movie_in_watchlater': movie_in_watchlater,
        'movie_frames': movie_frames
    })


# =========================
# ПОЛУЧЕНИЕ ФИЛЬМА ЧЕРЕЗ GET
# =========================

def movie_by_get(request):

    movie_id = request.GET.get('id')

    if not movie_id or not movie_id.isdigit():

        return render(
            request,
            'movie_not_found.html',
            status=404
        )

    movie = Movie.objects.filter(
        id=movie_id
    ).first()

    if movie is None:

        return render(
            request,
            'movie_not_found.html',
            status=404
        )

    return redirect(
        'movie_detail',
        movie_id=movie.id
    )


# =========================
# ЛИЧНЫЙ ПРОФИЛЬ
# =========================

def profile(request):

    # Если пользователь не авторизован или это администратор,
    # открываем страницу входа
    if not request.user.is_authenticated:
        return redirect('auth')

    if request.user.is_staff or request.user.is_superuser:
        return redirect('auth')

    watchlater_items = WatchLater.objects.filter(
        user=request.user
    ).select_related(
        'movie',
        'movie__genre'
    ).order_by('-added_at')

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if user_profile:
        display_name = user_profile.full_name
    else:
        display_name = request.user.get_full_name() or request.user.username

    return render(request, 'profile.html', {
        'watchlater_items': watchlater_items,
        'display_name': display_name
    })


# =========================
# ДОБАВЛЕНИЕ ФИЛЬМА В СПИСОК
# =========================

@login_required
@require_POST
def watchlater_add(request, movie_id):

    movie = get_object_or_404(
        Movie,
        id=movie_id
    )

    item, created = WatchLater.objects.get_or_create(
        user=request.user,
        movie=movie
    )

    return redirect(request.META.get('HTTP_REFERER', 'showcase'))


# =========================
# РЕДАКТИРОВАНИЕ ЗАПИСИ
# =========================

@login_required
def watchlater_edit(request, item_id):

    item = get_object_or_404(
        WatchLater,
        id=item_id,
        user=request.user
    )

    if request.method == 'POST':

        form = WatchLaterForm(
            request.POST,
            instance=item
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Статус просмотра обновлён.'
            )

            return redirect('profile')

    else:

        form = WatchLaterForm(
            instance=item
        )

    return render(request, 'watchlater_edit.html', {
        'form': form,
        'item': item
    })


# =========================
# УДАЛЕНИЕ ИЗ ЛИЧНОГО СПИСКА
# =========================

@login_required
@require_POST
def watchlater_delete(request, item_id):

    item = get_object_or_404(
        WatchLater,
        id=item_id,
        user=request.user
    )

    item.delete()

    messages.success(
        request,
        'Фильм удалён из вашего списка.'
    )

    return redirect('profile')
