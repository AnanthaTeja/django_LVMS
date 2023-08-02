from django.shortcuts import render, redirect
from .forms import AusForm, UsuserForm, UpForm, UspForm, TchprForm, StpForm, LeaveForm
from django.contrib import messages
from .models import User, TchProfile, StProfile, Leave


# Create your views here.
def home(request):
    return render(request, "html/home.html")


def about(request):
    return render(request, "html/about.html")


def contact(request):
    return render(request, "html/contact.html")


def register(request):
    if request.method == "POST":
        f = UsuserForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, "User Created Successfully")
            return redirect("/lgn")
    else:
        f = UsuserForm()
    return render(request, "html/register.html", {"g": f})


def userlist(request):
    c = User.objects.all()
    n, m = {}, {}
    if request.method == "POST":
        s = AusForm(request.POST)
        if s.is_valid():
            s.save()
            messages.success(request, "User created Successfully")
            return redirect("/usrlst")
        else:
            n[s] = s.errors
    for j in n.values():
        for v in j.items():
            m[v[0]] = v[1]
    print(m)
    s = AusForm()
    return render(request, "html/userlist.html", {"w": s, "p": m.items(), "k": c})


def profile(request):
    return render(request, "html/profile.html")


def userupdate(request, h):
    t = User.objects.get(id=h)
    if request.method == "POST":
        z = UpForm(request.POST, instance=t)
        if z.is_valid():
            z.save()
            return redirect("/usrlst")
    z = UpForm(instance=t)
    return render(request, "html/userupd.html", {"s": z})


def userdelete(request, d):
    n = User.objects.get(id=d)
    if request.method == "POST":
        n1 = UpForm(request.POST, instance=n)
        n.delete()
        return redirect("/usrlst")
    n1 = UpForm(instance=n)
    return render(request, "html/userdel.html", {"a": n1})


def updprofile(request):
    k = User.objects.get(id=request.user.id)

    if request.user.role_type == "2":
        t = TchProfile.objects.all()
        m = []
        for i in t:
            m.append(i.tc_id)
        if request.user.id not in m:
            if request.method == "POST":
                h = UspForm(request.POST, request.FILES, instance=k)
                y = TchprForm(request.POST)
                if h.is_valid() and y.is_valid():
                    h.save()
                    b = y.save(commit=False)
                    b.tc_id = request.user.id
                    b.tstatus = 1
                    b.save()
                    return redirect("/pfle")
            y = TchprForm()
            h = UspForm(instance=k)
            return render(request, "html/updateprofile.html", {"e": h, "t": y})
        else:
            p = TchProfile.objects.get(tc_id=request.user.id)
            if request.method == "POST":
                h = UspForm(request.POST, request.FILES, instance=k)
                y = TchprForm(request.POST, instance=p)
                if h.is_valid() and y.is_valid():
                    h.save()
                    y.save()
                    return redirect("/pfle")
            y = TchprForm(instance=p)
            h = UspForm(instance=k)
            return render(request, "html/updateprofile.html", {"e": h, "t": y})
    elif request.user.role_type == "1":
        j = StProfile.objects.all()
        s = []
        for i in j:
            s.append(i.sc_id)
        if request.user.id not in s:
            if request.method == "POST":
                h = UspForm(request.POST, request.FILES, instance=k)
                n = StpForm(request.POST)
                if h.is_valid() and n.is_valid:
                    h.save()
                    z = n.save(commit=False)
                    z.sc_id = request.user.id
                    z.sstatus = 1
                    z.save()
                    return redirect("/pfle")
            h = UspForm(instance=k)
            n = StpForm()
            return render(request, "html/updateprofile.html", {"e": h, "a": n})
        else:
            v = StProfile.objects.get(sc_id=request.user.id)
            if request.method == "POST":
                h = UspForm(request.POST, request.FILES, instance=k)
                n = StpForm(request.POST, instance=v)
                if h.is_valid() and n.is_valid():
                    h.save()
                    n.save()
                    return redirect("/pfle")
            h = UspForm(instance=k)
            return render(request, "html/updateprofile.html", {"e": h, "a": n})
    else:
        if request.method == "POST":
            h = UspForm(request.POST, request.FILES, instance=k)
            if h.is_valid():
                h.save()
                return redirect("/pfle")
        h = UspForm(instance=k)
        return render(request, "html/updateprofile.html", {"e": h})


def leavelist(request):
    p = Leave.objects.filter(st_id=request.user.id)
    if request.method == "POST":
        d = LeaveForm(request.POST, request.FILES)
        if d.is_valid():
            w = d.save(commit=False)
            w.st_id = request.user.id
            w.save()
            return redirect("/lvst")
    d = LeaveForm()
    return render(request, "html/leavelist.html", {"z": d, "h": p})


def tchlevlst(request):
    y = User.objects.filter(role_type="1")
    f = TchProfile.objects.get(tc_id=request.user.id)
    r, p, m = {}, {}, {}
    for i in y:
        r[i.id] = i.username
    k = StProfile.objects.all()
    for j in k:
        if j.sc_id in r and j.sbranch == f.tchbrnch:
            p[j.sc_id] = j.syear, r[i.id][0]

    # q = Leave.ob jects.all()
    for z in p:
        q = Leave.objects.all()
        for v in q:
            m[v.id] = v.leavetype, v.appldate, v.leavestatus, p[q.id][1], p[q.id][0]

    return render(request, "html/teacherlist.html")
