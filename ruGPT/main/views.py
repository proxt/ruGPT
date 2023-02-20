from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class MyLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'
    pk_url_kwarg = 'pk'
    pk_field = 'id'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subscription = Subscription.objects.filter(user=self.request.user).first()
        context['subscription'] = subscription
        return context



def home(request):
    return render(request, 'home.html')

def chat(request):
    return render(request, 'chat.html')



@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        openai.api_key = "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"
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"Hello, I am a chatbot. {message}",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        answer = response.choices[0].text.strip()
        return JsonResponse({'answer': answer})
    else:
        return JsonResponse({'error': 'Invalid request method'})


