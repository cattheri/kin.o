from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название жанра'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Movie(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название фильма'
    )

    description = models.TextField(
        verbose_name='Описание'
    )

    year = models.PositiveIntegerField(
        verbose_name='Год выпуска'
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name='Оценка'
    )

    poster = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Путь к постеру'
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT,
        related_name='movies',
        verbose_name='Жанр'
    )

    def __str__(self):
        return self.title

    @property
    def poster_path(self):
        posters = {
            'Грязные деньги': 'assets/image 14.png',
            'Майкл': 'assets/image 15.png',
            'Интерстеллар': 'assets/image 16.png',
            'Ограбить Лондон': 'assets/image 17.png',
            'Закулисье': 'assets/image 18.png',
            'Обсессия': 'assets/image 19.png',
            'Зеленая миля': 'assets/image 20.png',
            'Властелин колец': 'assets/image 21.png',
            'Остров проклятых': 'assets/image 22.png',
            'Форрест Гамп': 'assets/image 23.png',
            'Титаник': 'assets/image 24.png',
            'Экипаж': 'assets/image 25.png',
            'Армагеддон': 'assets/image 26.png',
            'Выжить': 'assets/image 27.png',
            'Послезавтра': 'assets/image 28.png',
            'День независимости': 'assets/image 29.png',
            'К-19': 'assets/image 30.png',
            'Идеальный шторм': 'assets/image 31.png',
            'Пекло': 'assets/image 32.png',
            'Смерч': 'assets/image 33.png',
        }

        return posters.get(self.title, self.poster)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

class MovieFrame(models.Model):

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='frames',
        verbose_name='Фильм'
    )

    image = models.ImageField(
        upload_to='movie_frames/',
        verbose_name='Кадр из фильма'
    )

    def __str__(self):
        return f'Кадр: {self.movie.title}'

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильмов'

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )

    full_name = models.CharField(
        max_length=200,
        verbose_name='ФИО'
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


class WatchLater(models.Model):

    STATUS_CHOICES = [
        ('want', 'Хочу посмотреть'),
        ('watching', 'Смотрю'),
        ('watched', 'Просмотрено'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='watchlater_items',
        verbose_name='Пользователь'
    )

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='watchlater_items',
        verbose_name='Фильм'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='want',
        verbose_name='Статус просмотра'
    )

    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Моя оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    def __str__(self):
        return f'{self.user.username} — {self.movie.title}'

    class Meta:
        verbose_name = 'Запись списка просмотра'
        verbose_name_plural = 'Списки просмотра'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'movie'],
                name='unique_user_movie'
            )
        ]