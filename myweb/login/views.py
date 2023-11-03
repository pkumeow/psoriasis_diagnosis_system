from django.shortcuts import render,HttpResponse
import os,json
import login.handle.begin as begin
# Create your views here.
def index(request):
    return render(request,'index.html')


def quest(request):
    #if request.method == 'POST':
        #chart_list.append(request.POST.get('age'))
        #username = request.POST.get('username')
        #password = request.POST.get('password')
    #    print(request.POST.getlist("reason"))
    #return render(request, 'index.html')

    if request.method == 'POST':
        chart_list=[]
        chart_list.append(request.POST.get('gender'))
        chart_list.append(request.POST.get('age'))
        chart_list.append(request.POST.get("again"))
        chart_list.append(request.POST.get("freq") if request.POST.get("again")=='1' else '0')
        chart_list.append(request.POST.get("month"))
        chart_list.append(request.POST.get("relative"))
        
        reason = request.POST.getlist("reason")
        chart_list.extend(('1' if str(i) in reason else '0' for i in range(10)))
        chart_list.append(request.POST.get("season"))


        place = request.POST.getlist("place")
        chart_list.extend(('1' if str(i) in place else '0' for i in range(6)))
        if '0' in place:
            # chart_list.append(request.POST.get("hair") if request.POST.get("hair")!=None else '0')
            chart_list.append(request.POST.get("hair"))
            chart_list.append(request.POST.get("head"))
        else:
            chart_list.extend(('0', '0'))
        

        chart_list.append(request.POST.get("skin"))
        if request.POST.get("skin")=='1':
            chart_list.append(request.POST.get("scales") if request.POST.get("scales")!=None else '0')
            chart_list.append(request.POST.get("thick") if request.POST.get("thick")!=None else '0')
            chart_list.append(request.POST.get("peel") if request.POST.get("peel")!=None else '0')
            chart_list.append(request.POST.get("flim") if request.POST.get("flim")!=None else '0')
            chart_list.append(request.POST.get("blood") if request.POST.get("blood")!=None else '0')
        else:
            chart_list.extend(('0', '0', '0', '0', '0'))

        
        nail = request.POST.getlist("nail")
        chart_list.extend(('1' if str(i) in nail else '0' for i in range(3)))
        chart_list.append(request.POST.get("joint"))
        symptom = request.POST.getlist("symptom")
        chart_list.extend(('1' if str(i) in symptom else '0' for i in range(2)))
        image=request.FILES.get('photo')
        print(os.getcwd())
        print(image)

        
        return render(request,'result.html', context=begin.start(chart_list,image))


    return render(request,'quest.html')