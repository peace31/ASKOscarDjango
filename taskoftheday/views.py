from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Guide, Step, Task, UserTaskHistory
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.views import generic
import analytics
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from analytics.models import Profile
import datetime
import operator
from django.db.models import F


# Create your views here.


@login_required(login_url='/login/')
@csrf_exempt
def taskoftheday(request):
    guide = {}
    try:
        if not request.POST and not request.POST.get('sb_start', False):
            guide = Guide.objects.get(pk=8)
            profile = Profile.objects.filter(user_id=request.user.id).first()
            return render(request, 'taskoftheday/taskoftheday.html', {'guide': guide, 'profile': profile})
        else:
            # code to figureout current working task.
            profile = Profile.objects.filter(user_id=request.user.id).first()
            return redirect('../%s/%s/%s/' % (request.POST.get('sb_start', False),
                                              profile.current_step_id.sequence_number if profile and profile.current_step_id else 1,
                                              profile.current_task_id.sequence_number if profile and profile.current_task_id else 1))
    except Guide.DoesNotExist:
        raise Http404("Guide does not exist")


@login_required(login_url='/login/')
@csrf_exempt
def detail_taskoftheday(request, guide_id, step_id, task_id=1):
    user = User.objects.get(id=request.user.id)  # GET CURRENT USER

    guide = Guide.objects.get(pk=guide_id)
    steps = Step.objects.filter(guide=guide_id).order_by('sequence_number')  # ALL STEPS IN A GUIDE
    step = Step.objects.filter(sequence_number=step_id, guide=guide_id).first()  # CURRENT STEP
    tasks = Task.objects.filter(step=step.id).order_by('sequence_number')  # ALL TASKS IN A STEP
    task = Task.objects.filter(sequence_number=task_id, step=step.id).first()  # CURRENT TASK IN A STEP

    profile = Profile.objects.filter(user_id=request.user.id).first()

    next = ""
    if int(task_id) < len(tasks):
        next = "/taskoftheday/%s/%s/%s/" % (guide_id, step_id, int(task_id) + 1)
    elif int(task_id) == len(tasks) and int(step_id) < len(steps):
        next = "/taskoftheday/%s/%s/%s/" % (guide_id, int(step_id) + 1, 1)
    elif int(task_id) == len(tasks) and int(step_id) == len(steps):
        next = "/taskoftheday/start"

    if request.POST:
        id1 = int(task_id) - 1
        id2 = int(step_id) - 1
        task1 = Task.objects.filter(sequence_number=id1, step=step.id).first()
        step1 = Step.objects.filter(sequence_number=id2, guide=guide_id).first()
        if 'buttoncheck' in request.POST.keys():
            user_history = UserTaskHistory.objects.filter(user=user, step=step.id, task=task.id).first()
            # CHECK IF ALREADY TASK COMPLETED, DON'T CREATE NEW TASK HISTORY 
            if not user_history:
                task_history = UserTaskHistory.objects.create(user=user,
                                                              guide=Guide.objects.get(pk=request.POST.get('guide_id')),
                                                              step=step,
                                                              task=task,
                                                              is_complete=True,
                                                              completion_datetime=datetime.datetime.now()
                                                              )
                task_history.save()

        if 'nextstep' in request.POST:
            # if not usertasks:
            #     task_history = UserTaskHistory.objects.create(user = user,
            #                                                   guide = Guide.objects.get(pk=request.POST.get('guide_id')),
            #                                                   step = step,
            #                                                   task = task,
            #                                                   completion_datetime = datetime.datetime.now()
            #                             )
            #     task_history.save()
            return redirect(request.POST.get('next'))

    # GET USER'S COMPLETED TASKS HISTORY, PICK ONLY ONE | FRIST
    usertasks = UserTaskHistory.objects.filter(user=request.user.id, step=step.id).order_by('-id').first()
    current_step = int(usertasks.step.sequence_number) if usertasks and usertasks.step else 0
    current_task = int(usertasks.task.sequence_number) if usertasks and usertasks.step and usertasks.task else 0

    if int(step_id) == 1:
        previous_task = int(current_task) + 1 if usertasks and usertasks.step else 1
    elif int(step_id) > 1:
        previous_step_id = int(step_id) - 1
        step = Step.objects.filter(sequence_number=previous_step_id, guide=guide_id).first()
        usertasks = UserTaskHistory.objects.filter(user=request.user.id, step=step.id).last()
        tasks = Task.objects.filter(step=step.id).order_by('sequence_number')
        if usertasks and int(usertasks.task.sequence_number) == len(tasks):
            previous_task = int(current_task) + 1 if usertasks and usertasks.step else 1
        else:
            previous_task = 0

    # if int(task_id) < len(tasks) :
    #     next = "/taskoftheday/%s/%s/%s/"%(guide_id, step_id, int(task_id)+1)
    #     if not usertasks:
    #         current_profile = Profile.objects.filter(user_id = request.user.id).update(current_guide_id = guide.id,
    #                                                                                    current_step_id = step.id,
    #                                                                                    current_task_id = task.id
    #             )

    if int(task_id) <= len(tasks) and int(step_id) <= len(steps):
        next = "/taskoftheday/%s/%s/%s/" % (guide_id, int(step_id) + 1, 1)
        if not usertasks:
            current_profile = Profile.objects.filter(user_id=request.user.id).update(current_guide_id=guide.id,
                                                                                     current_step_id=step.id,
                                                                                     current_task_id=task.id
                                                                                     )

    if int(task_id) <= len(tasks) and int(step_id) == len(steps):
        next = "/taskoftheday/start"
        # current_profile = Profile.objects.filter(user_id = request.user.id).update(current_guide_id = '',
        #                                                                            current_step_id = '',
        #                                                                            current_task_id = ''
        #     )
    # lists = list(zip(tasks, usertasks))
    return render(request, 'taskoftheday/detail_taskoftheday.html', {
        'steps': steps,
        'stepslist': range(len(steps)),
        'tasks': tasks,
        'taskslist': range(len(tasks)),
        'guide_id': int(guide_id), 'step_id': int(step_id), 'task_id': int(task_id),
        'task': task,
        'next': next,
        'usertasks': usertasks,
        'current_step': current_step,
        'current_task': current_task,
        'previous_task': previous_task,
        # 'lists':lists
    })
