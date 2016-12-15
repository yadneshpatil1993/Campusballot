from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,get_object_or_404
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect,Http404,JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from random import random, randint
from django.core.urlresolvers import reverse
from json import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from django.contrib.auth.models import User
from group.models import *

##########################################################################################################

state = ''

#################### LOGIN #########################
def login_user(request):
    state = username = password = ''
    if request.user.is_authenticated():
        return g_admin_home(request)        
    else:    
        if request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return g_admin_home(request)
                else:
                    state = "Your account is not active, please contact the site admin."
            else:
                state = "Your username and/or password were incorrect."

    return render(request,'home/index.html',{'state':state, 'username': username, 'login':True})


###################### SIGN UP #######################
def signup_user(request):
    state=username=email=password=''
    mail_send    = False
    if request.POST:
        username = request.POST.get('username')
        email    = request.POST.get('email')
        #password = request.POST.get('password')

        if not email_present(email):
            if not username_present(username):
                password = User.objects.make_random_password()
                #send_mail('Reset password campusballot', 'Thank you for contacting campusballot, here is your new password ', 'campusballot@example.com',[email], fail_silently=False)
                user = User.objects.create_user(username, email,password)
                user.save()
                mail_send = True
                state = "You are successfully signed up and your password is send to your email id."
            else:
                state = "This user name is already taken try different username"
        else:
            state = "This email id is already registerd Please try to login/ use new email id"

    return render(request,'home/index.html',{'state':state,'username':username,'email':email,'signup':True,'mail_send':mail_send})


###################### LOG OUT ###############################    
def logout_user(request):
    logout(request)
    # state = "You're successfully logged out!"
    # return render(request,'group/auth.html',{'state':state})
    return HttpResponseRedirect("/")


###################### RESET PASSWORD ########################
def reset_password(request):
    state = email = ''
    if request.POST:
        email        = request.POST.get('email')
        if email_present(email):
            state    = "your new password is mailed to your registerd email id."
            user     = User.objects.get(email=email)
            password = User.objects.make_random_password()
            #user.set_password(password)
            #send_mail('Reset password campusballot', 'Thank you for contacting campusballot, here is your new password ', 'campusballot@example.com',[email], fail_silently=False)
        else:
            state = "This email id is not registerd Please write correct email id"

    return render(request,'home/index.html',{'state':state,'email':email,'reset_password':True})


##################### CHECK EXIST OR NOT ######################
def username_present(username):
    if User.objects.filter(username=username).count():
        return True

    return False

def email_present(email):
    if User.objects.filter(email=email).count():
        return True

    return False    


############# load Organization Ajax############
@csrf_exempt
def load_organization(request):
    search_result=''
    if request.is_ajax():
        name = request.POST['input']
        if name:
            search_result = Group.objects.filter(Q(group_name__contains=name) | Q(org_name__contains=name))
            
    return render(request,'home/explore_result.html',{'search_result':search_result})


############################################ GROUP ADMIN ###############################################
@login_required(login_url='/')
def verify_group_user(request,group_id):
    user               =  request.user
    group = get_object_or_404(Group, pk=group_id)
    if group.u_id == user:
        return True

    return False

@login_required(login_url='/')
def change_password(request):
    user            =  request.user
    state           =  ''
    if request.POST:
        newpass     = request.POST.get('new_password')
        cinpass     = request.POST.get('confirm_password')
        if not newpass == cinpass:
            state = "Passwords are not same. Please write again"
            return render(request,'group/index.html',{'changepassword':True,'username':user,'state':state})        
        
        user.set_password(newpass)
        user.save()
        state = "password changed successfully."
            
    return render(request,'group/index.html',{'changepassword':True,'username':user,'state':state})


############ DISPLAY GROUPS ##################
@login_required(login_url='/')
def g_admin_home(request):
    user            =  request.user
    u_details       =  User.objects.get(username=user)
    group_list      =  Group.objects.filter(u_id=user) 
    return render(request,'group/index.html',{'groups':True,'username':u_details.username,'group_list':group_list})



######################## CREATE/DELETE/EDIT/DISABLE GROUP (OPERATIONS)  ##################

@login_required(login_url='/')
def create_group(request):
    user            =  request.user
    state = group_name = org_name = ''
    if request.POST:
        group_name  = request.POST.get('group_name')
        org_name    = request.POST.get('org_name')    
        if not group_name_present(group_name):
            group   = Group(u_id=user,group_name=group_name,org_name=org_name,is_active=True)  
            group.save()
            return render(request,'group/index.html',{'addmembers':True,'username':user,'group':group})
        else:
            state   = "This group name is already taken Please try some different name"
            
    return render(request,'group/index.html',{'creategroup':True,'username':user,'group_name':group_name,'org_name':org_name,'state':state})
                
def group_name_present(group_name):
    if Group.objects.filter(group_name=group_name).count():
        return True

    return False    

@login_required(login_url='/')
def view_group(request,group_id):
    user                =  request.user
    group = get_object_or_404(Group, pk=group_id)
    if not verify_group_user(request,group_id):
        return HttpResponseRedirect("/")
    members     = Members.objects.filter(group_id=group)
    questionset = GroupQn.objects.filter(group_id=group)
    membercount = group.female_count+group.male_count
    return render(request,'group/index.html',{'viewgroup':True,'state':state,'username':user,'group':group,'members_list':members,'questionset':questionset,'membercount':membercount})

@login_required(login_url='/')
def edit_group(request,group_id):
    user                =  request.user
    group = get_object_or_404(Group, pk=group_id)
    state=''
    if not verify_group_user(request,group_id):
        return HttpResponseRedirect("/")
    if request.POST:
        groupname    = request.POST.get('group_name')
        orgname      = request.POST.get('org_name')
        if not group_name_present(groupname):
            Group.objects.filter(pk=group_id).update(group_name=groupname,org_name=orgname)     
            state    = "Group updated successfully"    
            url      = reverse('group:view_group', kwargs={'group_id':group_id})
            return HttpResponseRedirect(url)    

        state="Group name already exist, please try another name" 
    return render(request,'group/index.html',{'editgroup':True,'username':user,'group':group,'state':state})

@login_required(login_url='/')
def disable_group(request,group_id):
    user                =  request.user
    group = get_object_or_404(Group, pk=group_id)
    state=''
    if not verify_group_user(request,group_id):
        return HttpResponseRedirect("/")
    Group.objects.filter(pk=group_id).update(is_active=not group.is_active)     
    state = ""    
    url      = reverse('group:view_group', kwargs={'group_id':group_id})
    return HttpResponseRedirect(url)    

@login_required(login_url='/')
def delete_group(request,group_id):
    user                =  request.user
    group = get_object_or_404(Group, pk=group_id)
    state=''
    if not verify_group_user(request,group_id):
        return HttpResponseRedirect("/")
    Group.objects.filter(pk=group_id).delete()     
    state = "Group Deleted successfully."    
    #return g_admin_home(request)
    return HttpResponseRedirect("/")



#################################### ADD/EDIT/DELETE GROUP MEMBERS (OPERATIONS) ##################

@login_required(login_url='/')
def add_members(request,group_id):
    user               =  request.user
    group = get_object_or_404(Group, pk=group_id)
    state =''
    if not verify_group_user(request,group_id):
        return HttpResponseRedirect("/")

    if request.POST:
        female_list    = request.POST.get('female_list')
        male_list      = request.POST.get('male_list')    
        female_list    = female_list.split('\r\n')
        male_list      = male_list.split('\r\n')
        totallen       = len(female_list)+len(male_list)
        if not male_list[0] and not female_list[0] and totallen is 2:
            state="Please Enter the members names" 
        elif group.male_count+group.female_count+totallen > 500:
            state="Your group's members limit reached you can add maximum 500 members in a group. Please create new group to add more members."
        # elif totallen > 200:
        #     state="You can add only 200 group members at a time. You can add more group members after group creation."
        else:
            countf      = 0
            for i in female_list:
                if i:
                    member      = Members(group_id=group,name=i,gender=0)  
                    member.save()
                    countf     += 1
            countm      = 0     
            for i in male_list:
                if i:
                    member      = Members(group_id=group,name=i,gender=1)  
                    member.save()
                    countm     += 1
            
            countf           += group.female_count
            countm           += group.male_count 
            Group.objects.filter(pk=group_id).update(female_count=countf,male_count=countm)
            questions_all    = Questions.objects.filter(gender=0,is_groupspecifc=False)
            questions_female = Questions.objects.filter(gender=1,is_groupspecifc=False)
            questions_male   = Questions.objects.filter(gender=2,is_groupspecifc=False)
            questionset      = GroupQn.objects.filter(group_id=group)
            groupq           = Questions.objects.filter(is_groupspecifc=True)
            groupquestions   = GroupQn.objects.filter(group_id=groupq) ###fetch the list of groupspecifc qns
            qset =[]
            for i in questionset:
                qset.append(i.qn_id.id)
            
            state            = "members added successfully"   
            return render(request,'group/index.html',{'addqn':True,'username':user,'state':state,'group':group,'questions_male':questions_male,'questions_female':questions_female,'questions_all':questions_all,'qset':qset,'groupquestions':groupquestions})

    return render(request,'group/index.html',{'addmembers':True,'username':user,'group':group,'state':state})


@login_required(login_url='/')
def edit_members(request,group_id,member_id):
    if not verify_group_user(request,group_id):
        return HttpResponseRedirect("/")

    user   = request.user
    group  = get_object_or_404(Group, pk=group_id)
    member = get_object_or_404(Members, pk=member_id)
    state  = ''
    
    if request.POST:
        membername    = request.POST.get('name')
        gender        = request.POST.get('gender') 
        if gender == 'male':
            Members.objects.filter(pk=member_id).update(name=membername,gender=1)     
        else:
            Members.objects.filter(pk=member_id).update(name=membername,gender=0)

        state = "Member edited successfully"    
        url      = reverse('group:view_group', kwargs={'group_id':group_id})
        return HttpResponseRedirect(url)    

    return render(request,'group/index.html',{'editmembers':True,'username':user,'group':group,'member':member})


@login_required(login_url='/')
def delete_members(request,group_id,member_id):
    if not verify_group_user(request,group_id):
        return HttpResponseRedirect("/")

    user   = request.user
    group = get_object_or_404(Group,pk=group_id)
    if group.female_count+group.male_count<=5:
        state="You can't further delete members, Because there should be atleast 5 members in the group."
        members = Members.objects.filter(group_id=group)
        return render(request,'group/index.html',{'viewgroup':True,'state':state,'username':user,'group':group,'members_list':members})
    
    member=Members.objects.get(pk=member_id)    
    Members.objects.filter(pk=member_id).delete()
    if member.gender=="0":
        Group.objects.filter(pk=group_id).update(female_count=group.female_count-1)     
    else:
        Group.objects.filter(pk=group_id).update(male_count=group.male_count-1)
    state = "Member deleted successfully"    
    url      = reverse('group:view_group', kwargs={'group_id':group_id})
    return HttpResponseRedirect(url)    



#################################### ADD GROUP QUESTIONS ##############################

@login_required(login_url='/')
def add_questions(request,group_id):
    user                =  request.user
    group = get_object_or_404(Group, pk=group_id)
    state = ''
    if not verify_group_user(request,group_id):
        return HttpResponseRedirect("/")
    
    if request.POST:
        q_all    = request.POST.getlist('q_all')
        q_f      = request.POST.getlist('q_f')    
        q_m      = request.POST.getlist('q_m')
        q_g      = request.POST.getlist('q_g')
        q        = ''

        
        totallen = len(q_all)+len(q_f)+len(q_m)
        if totallen < 1:
            state="Please select atleast 1 question."
        elif totallen > 50:
            state="You can select atmost 50 questions."
        elif q_f and group.female_count<4:
            state="You need to add atleast 5 female members to select female category questions."    
        elif q_m and group.male_count<4:
            state="You need to add atleast 5 male members to select male category questions."
        elif group.male_count + group.female_count <4:
            state="Please add atleast 5 members to select any question"
        else:
            deleteq = GroupQn.objects.filter(group_id=group).delete() #### Delete whole list of group-qn to fill new list
            for i in q_all:
                if i:
                    q  = Questions.objects.get(pk=i)
                    gq = GroupQn(group_id=group,qn_id=q)
                    gq.save()
                
            for i in q_m:
                if i:
                    q  = Questions.objects.get(pk=i)
                    gq = GroupQn(group_id=group,qn_id=q)
                    gq.save()
            
            for i in q_f:
                if i:
                    q  = Questions.objects.get(pk=i)
                    gq = GroupQn(group_id=group,qn_id=q)
                    gq.save()
            
            for i in q_g:
                if i:
                    q  = Questions.objects.get(pk=i)
                    gq = GroupQn(group_id=group,qn_id=q)
                    gq.save()
            
            state = ""    
            url      = reverse('group:view_group', kwargs={'group_id':group_id})
            return HttpResponseRedirect(url)    

    questions_all       = Questions.objects.filter(gender='0',is_groupspecifc=False)
    questions_female    = Questions.objects.filter(gender='1',is_groupspecifc=False)
    questions_male      = Questions.objects.filter(gender='2',is_groupspecifc=False)
    questionset         = GroupQn.objects.filter(group_id=group)
    q                   = Questions.objects.filter(is_groupspecifc=True)
    groupquestions      = GroupQn.objects.filter(qn_id=q,group_id=group) ###fetch the list of groupspecifc qns
    qset =[]
    for i in questionset:
        qset.append(i.qn_id.id)
    return render(request,'group/index.html',{'addqn':True,'username':user,'state':state,'group':group,'questions_male':questions_male,'questions_female':questions_female,'questions_all':questions_all,'qset':qset,'groupquestions':groupquestions})


@login_required(login_url='/')
def suggest_questions(request):
    user       = request.user
    group_list = Group.objects.filter(u_id=user)
    state=''  
    if request.POST:
        suggestion      = request.POST.get('qn')
        gender          = request.POST.get('genderq')
        group_id        = request.POST.get('group')
        if group_id and gender:
            group = get_object_or_404(Group,pk=group_id)
            q = Suggested_questions.objects.filter(suggestion=suggestion,group_id=group,gender=gender)
            if q:
                state = "Same Question is already suggested."
            else:
                q = Suggested_questions(group_id=group,suggestion=suggestion,gender=gender,is_accepted=True)                    
                q.save()
                state = "Question Suggested successfully !" 
        else:
            state="Select the Question category and Group."    
            
    return render(request,'group/index.html',{'suggestquestions':True,'username':user,'state':state,'group_list':group_list})


@login_required(login_url='/')
def suggestions_load(request):   
    user                 = request.user
    group                = Group.objects.filter(u_id=user)
    suggested_questions  = Suggested_questions.objects.filter(group_id=group,is_accepted=False)
    suggested_members    = Suggested_members.objects.filter(group_id=group)
    return render(request,'group/index.html',{'suggestions':True,'username':user,'suggested_questions':suggested_questions,'suggested_members':suggested_members})

@login_required(login_url='/')
def delete_suggested_qn(request,s_id):
    user                = request.user
    Suggested_questions.objects.filter(pk=s_id).delete()
    url = reverse('group:suggestions_load', kwargs={})
    return HttpResponseRedirect(url)    

@login_required(login_url='/')
def approve_suggested_qn(request,s_id):
    user                = request.user
    Suggested_questions.objects.filter(pk=s_id).update(is_accepted=True)
    url = reverse('group:suggestions_load', kwargs={})
    return HttpResponseRedirect(url)

@login_required(login_url='/')
def delete_suggested_member(request,s_id):
    user                = request.user
    Suggested_members.objects.filter(pk=s_id).delete()
    url = reverse('group:suggestions_load', kwargs={})
    return HttpResponseRedirect(url)    

@login_required(login_url='/')
def approve_suggested_member(request,s_id):
    user                = request.user
    member              = Suggested_members.objects.get(pk=s_id)
    state =''
    if membername_present(member.suggestion,member.group_id,member.gender):
        Suggested_members.objects.filter(pk=s_id).delete()
        url = reverse('group:suggestions_load', kwargs={})
        return HttpResponseRedirect(url)
    if member.group_id.female_count+member.group_id.male_count<500:
        addmember           = Members(group_id=member.group_id,name=member.suggestion,gender=member.gender)
        addmember.save()
        if member.gender == "0":
            newcount            = member.group_id.female_count+1
            Group.objects.filter(pk=member.group_id.id).update(female_count=newcount)
        else :
            newcount            = member.group_id.male_count+1
            Group.objects.filter(pk=member.group_id.id).update(male_count=newcount)
        Suggested_members.objects.filter(pk=s_id).delete()
    else :
        state= "Group member limit exceeded, Delete some members to add new, or Create new group."    
    
    suggested_questions  = Suggested_questions.objects.filter(group_id=member.group_id,is_accepted=False)
    suggested_members    = Suggested_members.objects.filter(group_id=member.group_id)
    return render(request,'group/index.html',{'suggestions':True,'username':user,'state':state,'suggested_questions':suggested_questions,'suggested_members':suggested_members})

def membername_present(name,group,gender):
    if Members.objects.filter(name=name,group_id=group,gender=gender).count():
        return True

    return False

########################################## VOTING PAGE (BALLOT) #############################################

def ballot_home(request,group_id):
    group               = get_object_or_404(Group, pk=group_id)
    if not group.is_active:
        state = 'This Group is Disabled by group admin'
        return render(request,'ballot/index.html',{'question':True,'group':group,'state':state})    
    questionset         = GroupQn.objects.filter(group_id=group)
    o1=o2=o3=o4=options     = ''
    
    if not questionset:
        return HttpResponseRedirect("/")
    
    qset =[]
    for i in questionset:
        qset.append(i.qn_id.id)
    
    q                       = randint(0,len(qset)-1)
    q                       = qset[q]
    qn                      = Questions.objects.get(pk=q)
    if qn.gender == '0':
        options             = Members.objects.filter(group_id=group)
    elif qn.gender == '1':
        options             = Members.objects.filter(group_id=group,gender=0)
    else:
        options             = Members.objects.filter(group_id=group,gender=1)
    if len(options)>3:
        o1                  = randint(0,len(options)-1)
        o4=o2=o3=o1
        while o2==o1:
            o2              = randint(0,len(options)-1)
        while o3==o1 or o3==o2:
            o3              = randint(0,len(options)-1)
        while o4==o1 or o4==o2 or o4==o3:
            o4              = randint(0,len(options)-1)
        
        o1                  = options[o1]
        o2                  = options[o2]
        o3                  = options[o3]
        o4                  = options[o4]    
        request.session['o1'] = o1.id
        request.session['o2'] = o2.id
        request.session['o3'] = o3.id
        request.session['o4'] = o4.id
        request.session['group_id'] = group_id
        request.session['q_id']     = qn.id

    else:
        if qn.gender=='0':
            return HttpResponseRedirect("/")
        else:
            url      = reverse('group:ballot_home', kwargs={'group_id':group_id})
            return HttpResponseRedirect(url)    
    if request.is_ajax():
        return render(request,'ballot/question_load.html',{'group':group,'q':qn,'o1':o1,'o2':o2,'o3':o3,'o4':o4})

    return render(request,'ballot/index.html',{'question':True,'group':group,'q':qn,'o1':o1,'o2':o2,'o3':o3,'o4':o4})

@csrf_exempt
def ballot_update(request):
    winner=loser1=loser2=loser3=search_result=''
    if request.is_ajax():
        vote            = request.POST['vote']
        group_id        = request.POST['group_id']
        q_id            = request.POST['q']
        if 'q_id' in request.session:
            q_id            = request.session['q_id']
        if 'group_id' in request.session:
            group_id        = request.session['group_id']
        if vote=="1":
            if 'o1' in request.session:
                winner  = request.session['o1']
                loser1  = request.session['o2']
                loser2  = request.session['o3']
                loser3  = request.session['o4']
        elif vote=="2":
            if 'o2' in request.session:
                winner  = request.session['o2']
                loser1  = request.session['o1']
                loser2  = request.session['o3']
                loser3  = request.session['o4']
        elif vote=="3":
            if 'o3' in request.session:
                winner  = request.session['o3']
                loser1  = request.session['o1']
                loser2  = request.session['o2']
                loser3  = request.session['o4']
        elif vote=="4":
            if 'o3' in request.session:
                winner  = request.session['o4']
                loser1  = request.session['o1']
                loser2  = request.session['o2']
                loser3  = request.session['o3']                
        else:
            return ballot_home(request,group_id)

        ## RATING ALGORITHM ##
        group           = get_object_or_404(Group, pk=group_id)
        qn              = get_object_or_404(Questions, pk=q_id)

        if winner and loser1 and loser2 and loser3:
            w           = get_object_or_404(Members, pk=winner)    
            l1          = get_object_or_404(Members, pk=loser1)    
            l2          = get_object_or_404(Members, pk=loser2)    
            l3          = get_object_or_404(Members, pk=loser3)            
        else:
            return ballot_home(request,group_id)

        Q = float(GroupQn.objects.filter(group_id=group).count())    
        N = float(group.female_count+group.male_count) 
          
        #intializing    
        lower_limit = 100.00
        base_score = 1000.00
        wining_score = Q/3 + N/15 + 8
        l1_score=l2_score=l3_score=w_score=base_score

        if Ratings.objects.filter(member_id=w,question=qn).count():
            w1           = Ratings.objects.get(member_id=w,question=qn)
            w_score     = float(w1.rating)
        else:
            rate        = Ratings(member_id=w,question=qn,rating=base_score)
            rate.save()
        
        if Ratings.objects.filter(member_id=l1,question=qn).count():
            l11          = Ratings.objects.get(member_id=l1,question=qn)
            l1_score    = float(l11.rating)
        else:
            rate        = Ratings(member_id=l1,question=qn,rating=base_score)
            rate.save()        
                
        if Ratings.objects.filter(member_id=l2,question=qn).count():
            l21          = Ratings.objects.get(member_id=l2,question=qn)
            l2_score    = float(l21.rating)
        else:
            rate        = Ratings(member_id=l2,question=qn,rating=base_score)
            rate.save()
        
        if Ratings.objects.filter(member_id=l3,question=qn).count():
            l31          = Ratings.objects.get(member_id=l3,question=qn)
            l3_score    = float(l31.rating)         
        else:
            rate        = Ratings(member_id=l3,question=qn,rating=base_score)
            rate.save()
        
        d1=d2=d3=0.0

        if l1_score>lower_limit:
            d1=l1_score - lower_limit
        if l2_score>lower_limit:
            d2=l2_score - lower_limit
        if l3_score>lower_limit:
            d3=l3_score - lower_limit 
        
        if d1>0:
            l1_score -= wining_score*d1/(d1+d2+d3)    
            Ratings.objects.filter(member_id=l1).update(rating=l1_score)
        if d2>0:
            l2_score -= wining_score*d2/(d1+d2+d3)    
            Ratings.objects.filter(member_id=l2).update(rating=l2_score)
        if d3>0:
            l3_score -= wining_score*d3/(d1+d2+d3)    
            Ratings.objects.filter(member_id=l3).update(rating=l3_score)
        
        w_score += wining_score 
        Ratings.objects.filter(member_id=w).update(rating=w_score) 
        
        
        Group.objects.filter(id=group_id).update(vote_count=group.vote_count+1)
    return ballot_home(request,group_id)
    #url = reverse('group:ballot_home', kwargs={'group_id': group.id })
    #return HttpResponseRedirect(url)    

def ballot_leaderboard(request,group_id):
    group               = get_object_or_404(Group, pk=group_id)
    members             = Members.objects.filter(group_id=group)
    questionset         = GroupQn.objects.filter(group_id=group)
    return render(request,'ballot/index.html',{'leaderboard':True,'group':group,'allqn':questionset})

@csrf_exempt
def load_leaderboard(request):
    search_result=''
    if request.is_ajax():
        q_id     = request.POST['q_id']
        group_id = request.POST['group_id']
        if q_id and group_id:
            group               = get_object_or_404(Group, pk=group_id)
            qn                  = Questions.objects.get(pk=q_id)
            members             = Members.objects.filter(group_id=group)
            leaderboard_list    = Ratings.objects.filter(member_id=members,question=qn).order_by('-rating')    
               
    return render(request,'ballot/leaderboard_load.html',{'leaderboard_list':leaderboard_list,'q':qn})


def ballot_suggestions(request,group_id):
    group               = get_object_or_404(Group, pk=group_id)
    state=''
    if request.POST:
        s_type          = request.POST.get('type')        
        
        if s_type == "1":
            suggestion      = request.POST.get('qn')
            gender          = request.POST.get('genderq')
            if gender:
                q = Suggested_questions.objects.filter(suggestion=suggestion,group_id=group,gender=gender)
                if q:
                    state = "Same Question is already exists."
                else:
                    q = Suggested_questions(group_id=group,suggestion=suggestion,gender=gender)
                    q.save()
                    state = "Question Suggested successfully !" 
            else:
                state = " Please select the category of question."
        else:
            suggestion      = request.POST.get('name')
            gender          = request.POST.get('genderf')
            if gender:
                q = Suggested_members.objects.filter(suggestion=suggestion,group_id=group,gender=gender)
                if q:
                    state = "Friend of same name is already exists."    
                else:
                    q = Suggested_members(group_id=group,suggestion=suggestion,gender=gender)
                    q.save()
                    state = "Friend name Suggested successfully !" 
            else:
                state = " Please select gender."      
            
    return render(request,'ballot/index.html',{'suggestion':True,'group':group,'state':state})




########################################## ONLY FOR SUPER ADMIN #################################

@user_passes_test(lambda u: u.is_staff)
def question_entry(request):
    user               =  request.user
    if request.POST:
        q_all    = request.POST.get('q_all')
        q_f      = request.POST.get('q_f')    
        q_m      = request.POST.get('q_m')    
        
        q_all    = q_all.split('\r\n')
        q_m      = q_m.split('\r\n')
        q_f      = q_f.split('\r\n')
        
        for i in q_all:
            if i:
                q      = Questions(question=i,gender=0)  
                q.save()
        
        for i in q_f:
            if i:
                q      = Questions(question=i,gender=1)  
                q.save()
        
        for i in q_m:
            if i:
                q      = Questions(question=i,gender=2)  
                q.save()
         
        questions_all    = Questions.objects.filter(gender=0)
        questions_female = Questions.objects.filter(gender=1)
        questions_male   = Questions.objects.filter(gender=2)    
        return render(request,'group/index.html',{'seeqn':True,'username':user,'questions_male':questions_male,'questions_female':questions_female,'questions_all':questions_all})

    return render(request,'group/index.html',{'question_entry':True,'username':user})

@user_passes_test(lambda u: u.is_staff)
def seeqn(request):
    user               =  request.user
    questions_all    = Questions.objects.filter(gender=0)
    questions_female = Questions.objects.filter(gender=1)
    questions_male   = Questions.objects.filter(gender=2)    
    return render(request,'group/index.html',{'seeqn':True,'username':user,'questions_male':questions_male,'questions_female':questions_female,'questions_all':questions_all})

@user_passes_test(lambda u: u.is_staff)
def seesuggestions(request):
    user             =  request.user
    seesuggestions_list = Suggested_questions.objects.filter(is_accepted=True)
    return render(request,'group/index.html',{'seesuggestions':True,'username':user,'seesuggestions_list':seesuggestions_list})

@user_passes_test(lambda u: u.is_staff)
def admin_approvesuggestedquestion(request,s_id):
    user                = request.user
    s = Suggested_questions.objects.get(pk=s_id)
    q = Questions(question=s.suggestion,gender=s.gender,is_groupspecifc=True)
    q.save()
    # q = Questions.objects.get(question=s.suggestion,gender=s.gender,is_groupspecifc=True)
    q = GroupQn(group_id=s.group_id,qn_id=q)
    q.save()
    Suggested_questions.objects.filter(pk=s_id).delete()
    url = reverse('group:seesuggestions', kwargs={})
    return HttpResponseRedirect(url)

@login_required(login_url='/')
def admin_deletesuggestedquestion(request,s_id):
    user                = request.user
    Suggested_questions.objects.filter(pk=s_id).delete()
    url = reverse('group:seesuggestions', kwargs={})
    return HttpResponseRedirect(url)    