from django.contrib import admin
from .models import Genre, Movie, MovieFrame, UserProfile, WatchLater


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')
    search_fields = ('name',)


class MovieFrameInline(admin.TabularInline):

    model = MovieFrame
    extra = 0
    max_num = 6
    validate_max = True


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'year', 'genre')
    list_filter = ('genre', 'year')
    search_fields = ('title',)

    inlines = [MovieFrameInline]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = ('id', 'full_name', 'user')

    search_fields = (
        'full_name',
        'user__username',
        'user__email'
    )


@admin.register(WatchLater)
class WatchLaterAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'movie',
        'status',
        'rating',
        'added_at'
    )

    list_filter = ('status', 'added_at')

    list_editable = ('status', 'rating')

    search_fields = (
        'user__username',
        'user__email',
        'movie__title'
    )

    readonly_fields = ('added_at',)