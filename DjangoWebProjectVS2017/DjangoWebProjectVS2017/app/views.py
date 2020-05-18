"""
Definition of views.
"""

from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http.response import HttpResponse, Http404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Question,Choice,User
from django.template import loader
from django.core.urlresolvers import reverse
from app.forms import QuestionForm, ChoiceForm,UserForm
from django.shortcuts import redirect
from django.contrib import messages
import json


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Autor de la web',
            'message':'Datos de contacto',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def index(request):
    try :
        tema=request.POST['tema']
    except:
        tema='none'
    latest_question_list = Question.objects.order_by('-pub_date')
    temas = Question.objects.values_list('tema',flat=True).distinct()
    template = loader.get_template('polls/index.html')
    context = {'title':'Lista de preguntas de la encuesta', 'latest_question_list': latest_question_list,'temas':temas,'tema_elegido':tema}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
     question = get_object_or_404(Question, pk=question_id)
     return render(request, 'polls/detail.html', {'title':'Respuestas asociadas a la pregunta:','question': question})

def results(request, question_id, choice_id):
    question = get_object_or_404(Question, pk=question_id)
    choice= get_object_or_404(Choice, pk=choice_id)
    correct=''
    wrong=''
    if(choice.Correcta==True):
        correct='Respuesta correcta, has acertado Crack!!!'
    else:
        wrong='Has fallado, vuelve a intentarlo'
    return render(request, 'polls/results.html', {'title':'Resultados de la pregunta:','question': question,'acertar':correct,'fallar':wrong})

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Vuelve a mostrar el form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "ERROR: No se ha seleccionado una opcion",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Siempre devolver un HttpResponseRedirect despues de procesar
        # exitosamente el POST de un form. Esto evita que los datos se
        # puedan postear dos veces si el usuario vuelve atras en su browser.
        return HttpResponseRedirect(reverse('results', args=(p.id,selected_choice.id,)))

def question_new(request): 
        msg=''
        msg_er=''
        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.pub_date=datetime.now()
                question.save()
                msg='Pregunta añadida correctamente'
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = QuestionForm()
        return render(request, 'polls/question_new.html', {'form': form,'message':msg})

def choice_add(request, question_id):
        pregunta = Question.objects.get(id = question_id)
        respuestas=Choice.objects.filter(question=pregunta)
        msg_er=''
        msg=''
        Correcta=False
        numrespuestas=0
        for respuesta in respuestas :
            numrespuestas+=1
            if respuesta.Correcta==True :
                Correcta=True
        if request.method =='POST' and numrespuestas<4 :
            form = ChoiceForm(request.POST)
            if form.is_valid():
                choice = form.save(commit = False)
                choice.question = pregunta
                choice.vote = 0
                if numrespuestas<3 :
                    if not(choice.Correcta==True and Correcta==True) :
                        choice.save()
                        msg='Respuesta introducida correctamente'
                    else :
                        msg_er='Solo puede haber una respuesta correcta'
                else:
                    if (choice.Correcta==True and Correcta==False or choice.Correcta==False and Correcta==True):
                        choice.save()
                        msg='Respuesta introducida correctamente'
                    else:
                        if Correcta==False :
                            msg_er='Tiene que haber al menos una respuesta correcta'
                        else:
                            msg_er='Solo puede haber una respuesta correcta'
                #form.save()
        else: 
            if numrespuestas>=4 :
                msg_er='Se ha alcanzado el número máximo de respuestas'
               
            form = ChoiceForm()
        #return render_to_response ('choice_new.html', {'form': form, 'poll_id': poll_id,}, context_instance = RequestContext(request),)
        return render(request, 'polls/choice_new.html', {'title':'Pregunta:'+ pregunta.question_text,'form': form,'error_msg': msg_er,'message':msg})

def chart(request, question_id):
    q=Question.objects.get(id = question_id)
    qs = Choice.objects.filter(question=q)
    dates = [obj.choice_text for obj in qs]
    counts = [obj.votes for obj in qs]
    context = {
        'dates': json.dumps(dates),
        'counts': json.dumps(counts),
    }

    return render(request, 'polls/grafico.html', context)

def user_new(request):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = UserForm()
        return render(request, 'polls/user_new.html', {'form': form})

def users_detail(request):
    latest_user_list = User.objects.order_by('email')
    template = loader.get_template('polls/users.html')
    context = {
                'title':'Lista de usuarios',
                'latest_user_list': latest_user_list,
              }
    return render(request, 'polls/users.html', context)

