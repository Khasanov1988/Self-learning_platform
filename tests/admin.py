from django.contrib import admin

from tests.models import *


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_filter = ('title',)


@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_filter = ('title',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_filter = ('text',)


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_filter = ('text',)
