from typing import ContextManager
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import QuizMst
from .models import StudentMst


def mainpage(request):
    return render(request, "Quiz.html")


def loginpage(request):
    if request.method=="POST":
        return render(request, "loginpage.html")
    return redirect("http://127.0.0.1:8000")


def gettest(request):
    '''
    context_dict={"ques":"HOW ARE YOU","op1":"GOOD","op2":"FINE","op3":"SAD","op4":"NOT FINE","qid":"q1"}
    context_dict2={"ques":"HOW ARE YOU DOING","op1":"GOOD","op2":"FINE","op3":"SAD","op4":"NOT FINE","qid":"q2"}
    di={"l":[context_dict,context_dict2]}
    return render(request,'page1.html',context=di)'''
    # print(request.method)

    if request.method == "POST":
        pwd = request.POST.get("password", None)

        if pwd != None:
            if request.POST.get("password") != "@#$%":
                l = [("Incorrect Password", "PLEASE ENTER CORRECT PASSWORD")]
                return render(request, "loginpage.html", context={"message": l})

            else:
                q = QuizMst.objects.values("subject").distinct()
                l = []
                for key in q:
                    l.append(key.get("subject").title())
                context = {"name": request.POST.get(
                    "st_details"), "testnames": l}

                r = render(request, "testselection.html", context=context)
                r.set_cookie(key="name", value=request.POST.get("st_details"))

                return r
                '''
                list_ques=[]
                q=QuizMst.objects.all()
                l=[]
                for i in q:
                    l.append(i.qid)
                for i in q:
                    list_ques.append(i)
                dict_ques={"l":list_ques,"nm":"English","st_details":request.POST.get("st_details")}
                r=render(request,'page1.html',context=dict_ques)
                r.set_cookie(key="name",value=request.POST.get("st_details"))
                r.set_cookie(key="keys",value=l)
                return r
                '''

        elif pwd == None:
            l = [("No Password", "PLEASE ENTER PASSWORD")]
            return render(request, "loginpage.html", context={"message": l})

    return redirect("http://127.0.0.1:8000")


def evaluate(request):

    if request.method == "POST":
        keys = eval(request.COOKIES.get('keys'))
        # print(eval(keys))
        totalmarks = len(keys)
        m = 0
        l = request.POST.copy()
        l.pop("csrfmiddlewaretoken")

        for i, j in l.items():
            # print(i)
            q = QuizMst.objects.get(qid=i)
            crt = q.correct_op
            # print(j,crt)
            if crt == j:
                m += 1
        # print(m)

        # SAVING DATA IN STUDENT MASTER
        student = StudentMst()
        student.student_name = request.COOKIES["name"]
        student.correct_ans = m
        student.wrong_ans = totalmarks-m
        student.subject = request.COOKIES.get("testname")
        student.total_marks = m*5-(totalmarks)*2
        student.save()

        # RENDERING FINAL RESULT PAGE
        context = {"name": request.COOKIES["name"], "marks": m, "tmarks": totalmarks,
                   'tname': request.COOKIES.get("testname"), 'tm': "27mins"}
        return render(request, "Result.html", context)

    # if DIRECTLY GET REQUEST IS MADE THEN REDIRECT THEM TO LOGIN PAGE
    return redirect("http://127.0.0.1:8000")


def getquestions(request):

    if request.method == 'POST':
        tname = request.POST.get("testname", None)
        list_ques = []
        q = QuizMst.objects.filter(subject=tname)
        l = []
        for i in q:
            l.append(i.qid)
        for i in q:
            list_ques.append(i)
        dict_ques = {"l": list_ques, "nm": tname,
                     "st_details": request.COOKIES.get("name"),"totalques":len(l),"totalmarks":len(l)*5}
        r = render(request, 'testattempt.html', context=dict_ques)
        r.set_cookie(key="testname", value=tname)
        r.set_cookie(key="keys", value=l)
        return r

    # IF DIRECT GET REQUEST IS MADE THEN REDIRECT TO LOGIN PAGE
    return redirect("http://127.0.0.1:8000")


# Create your views here.
