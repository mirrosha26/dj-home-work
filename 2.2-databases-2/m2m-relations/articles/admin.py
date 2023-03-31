from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag
class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        counter = 0
        check_tag_list = []
        for form in self.forms:
            tag = form.cleaned_data.get('tag')
            if tag in check_tag_list:
                    raise ValidationError('Теги не должны повторяться ')
                    
            if form.cleaned_data.get('is_main'):
                if not form.cleaned_data.get('DELETE'):
                    counter += 1
                    check_tag_list.append(tag)
                if counter > 1:
                    raise ValidationError('Основным может быть только один тег')
                
        if counter == 0:
            raise ValidationError('Укажите основной тег')


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 0



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_at']
    inlines = [ScopeInline, ]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']




