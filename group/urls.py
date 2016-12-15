from django.conf.urls import patterns, url

from group import views

urlpatterns = patterns('',
    # login/
    url(r'^$', views.login_user , name='login'),
    url(r'^signup$', views.signup_user , name='signup'),
    url(r'^logout$', views.logout_user, name='logout'),
    url(r'^reset_password$', views.reset_password, name='reset_password'),
    url(r'^change_password$', views.change_password, name='change_password'),
    url(r'^load_organization$', views.load_organization, name='load_organization'),
    
    #suggestions
    url(r'^suggestions_load$', views.suggestions_load, name='suggestions_load'),
    url(r'^delete_suggested_qn/(?P<s_id>\d+)$', views.delete_suggested_qn, name='delete_suggested_qn'),
    url(r'^approve_suggested_qn/(?P<s_id>\d+)$', views.approve_suggested_qn, name='approve_suggested_qn'),
    url(r'^delete_suggested_member/(?P<s_id>\d+)$', views.delete_suggested_member, name='delete_suggested_member'),
    url(r'^approve_suggested_member/(?P<s_id>\d+)$', views.approve_suggested_member, name='approve_suggested_member'),
    
    #voting page
    url(r'^gfdhjxv83brk3pfo3(?P<group_id>\d+)hjkz3bcveh$', views.ballot_home, name='ballot_home'),
    url(r'^ballot_update$', views.ballot_update, name='ballot_update'),
    url(r'^ballot_leaderboard/(?P<group_id>\d+)$', views.ballot_leaderboard, name='ballot_leaderboard'),
    url(r'^ballot_suggestions/(?P<group_id>\d+)$', views.ballot_suggestions, name='ballot_suggestions'),
    url(r'^load_leaderboard$', views.load_leaderboard, name='load_leaderboard'),
    
    #admin
    url(r'^create_group$', views.create_group, name='create_group'),
    url(r'^view_group/(?P<group_id>\d+)$', views.view_group, name='view_group'),
    url(r'^edit_group/(?P<group_id>\d+)$', views.edit_group, name='edit_group'),
    url(r'^disable_group/(?P<group_id>\d+)$', views.disable_group, name='disable_group'),
    url(r'^delete_group/(?P<group_id>\d+)$', views.delete_group, name='delete_group'),
    url(r'^add_members/(?P<group_id>\d+)$', views.add_members, name='add_members'),
    url(r'^edit_members/(?P<group_id>\d+)/(?P<member_id>\d+)$', views.edit_members, name='edit_members'),
    url(r'^delete_members/(?P<group_id>\d+)/(?P<member_id>\d+)$', views.delete_members, name='delete_members'),
    url(r'^add_questions/(?P<group_id>\d+)$', views.add_questions, name='add_questions'),
    url(r'^suggest_questions$', views.suggest_questions, name='suggest_questions'),
    #superadmin
    url(r'^question_entry$', views.question_entry, name='question_entry'),
    url(r'^seeqn$', views.seeqn, name='seeqn'),
    url(r'^seesug$', views.seesuggestions, name='seesuggestions'),
    url(r'^admin_approve_suggested_qn/(?P<s_id>\d+)$', views.admin_approvesuggestedquestion, name='admin_approve_suggested_qn'),
    url(r'^admin_delete_suggested_qn/(?P<s_id>\d+)$', views.admin_deletesuggestedquestion, name='admin_delete_suggested_qn'),
    # ex: /polls/5/
 	#url(r'^(?P<group_id>\d+)/group/$', views.groupview, name='groupview'),
       
)