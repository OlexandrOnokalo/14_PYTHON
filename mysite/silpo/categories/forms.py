from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        label='Назва категорії',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg border border-gray-700 bg-gray-900 px-4 py-3 text-white placeholder-gray-500 focus:border-indigo-500 focus:outline-none',
            'placeholder': 'Назва категорії ...',
        })
    )

    description = forms.CharField(
        label='Oпис',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full rounded-lg border border-gray-700 bg-gray-900 px-4 py-3 text-white placeholder-gray-500 focus:border-indigo-500 focus:outline-none',
            'rows': '3',
            'placeholder': 'Короткий опис ...',
        })
    )

    slug = forms.SlugField(
        label='Slug',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg border border-gray-700 bg-gray-900 px-4 py-3 text-white placeholder-gray-500 focus:border-indigo-500 focus:outline-none',
            'placeholder': 'category-name',
        })
    )

    image = forms.ImageField(
        label='Зображення',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-gray-400 '
                     'file:mr-4 file:py-2 file:px-4 '
                     'file:rounded-lg file:border-0 '
                     'file:text-sm file:font-semibold '
                     'file:bg-indigo-600 file:text-white '
                     'hover:file:bg-indigo-500 '
                     'cursor-pointer',
            'accept': 'image/*',
        }),
    )

    class Meta:
        model = Category
        fields = ('name', 'description', 'slug', 'image')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        gs = Category.objects.filter(name=name)
        if self.instance.pk:
            gs = gs.exclude(pk=self.instance.pk)
        if gs.exists():
            raise forms.ValidationError("Категорія з такою назвою існує.")
        return name