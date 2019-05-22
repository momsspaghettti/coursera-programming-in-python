from django.http import HttpResponse, JsonResponse
from django.views import View
from django import forms
import json
from somemart.models import Item, Review
from django.contrib.auth.mixins import LoginRequiredMixin


class ItemForm(forms.Form):
    title = forms.CharField(min_length=1, max_length=64)
    description = forms.CharField(min_length=1, max_length=1024)
    price = forms.IntegerField(min_value=1, max_value=1000000)


class ReviewForm(forms.Form):
    text = forms.CharField(min_length=1, max_length=1024)
    grade = forms.IntegerField(min_value=1, max_value=10)


class AddItemView(LoginRequiredMixin, View):
    """View для создания товара."""

    def post(self, request):
        form = ItemForm(request.POST)

        if form.is_valid():
            context = form.cleaned_data
            item = Item(title=context['title'], description=context['description'], price=context['price'])
            item.save()
            data = {'id': item.pk}
            return JsonResponse(data, status=201)
        else:
            return HttpResponse(status=400)


class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        form = ReviewForm(request.POST)
        data = {'id': item_id}

        if form.is_valid():
            context = form.cleaned_data
            try:
                item = Item.objects.get(pk=item_id)
                review = Review(text=context['text'], grade=context['grade'], item=item)
                review.save()
                return JsonResponse(data, status=201)
            except Item.DoesNotExist:
                return HttpResponse(status=404)
        else:
            return HttpResponse(status=400)


class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
            reviews = [
                {
                    'id': review.pk,
                    'text': review.text,
                    'grade': review.grade
                }
                for review in Review.objects.filter(item=item).order_by('-pk')
            ]

            data = {
                'id': item.pk,
                'title': item.title,
                'description': item.description,
                'price': item.price,
                'reviews': reviews[-5:]
            }
            return JsonResponse(data, status=200)
        except (Item.DoesNotExist, json.JSONDecodeError):
            return HttpResponse(status=404)



