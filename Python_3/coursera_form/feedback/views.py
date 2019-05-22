from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import Feedback
from django.views.generic.list import ListView


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    fields = [
        'text',
        'grade',
        'subject'
    ]
    success_url = '/feedback/add'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class FeedbackListView(LoginRequiredMixin, ListView):
    model = Feedback

    def get_queryset(self):
        if self.request.user.is_staff:
            return Feedback.objects.all().order_by('author')
        else:
            return Feedback.objects.filter(author=self.request.user).order_by('author')