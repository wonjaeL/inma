from django.contrib import admin

from .models import Course


class CourseInLine(admin.TabularInline):
    model = Course
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_valid']
    inlines = [
    ]
