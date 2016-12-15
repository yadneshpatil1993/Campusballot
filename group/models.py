from django.db import models
from django.contrib.auth import authenticate
from django.core.context_processors import csrf
from django.contrib.auth.models import *

import datetime


#################################### GROUP DETAILS ####################################################

class Group(models.Model):
    u_id                = models.ForeignKey(User)
    group_name          = models.CharField(max_length=50,unique=True)
    org_name            = models.CharField(max_length=50)
    male_count          = models.IntegerField(default=0)
    female_count        = models.IntegerField(default=0)
    vote_count          = models.IntegerField(default=0)
    created_on          = models.DateTimeField(auto_now_add=True)
    updated_on          = models.DateTimeField(auto_now=True)
    is_active           = models.BooleanField(default=False)
    def __str__(self):              # __unicode__ on Python 2
        return self.group_name + " " + self.org_name

#################################### QUESTION DETAILS ####################################################

class Questions(models.Model):
    question = models.CharField(max_length=200,unique=True)
    GENDER_CHOICES  =   (
                            ('0', 'All')
                            ,('1', 'Female')
                            ,('2', 'Male')
                        )
    gender          = models.CharField(max_length=1,choices = GENDER_CHOICES,default = False )
    is_groupspecifc = models.BooleanField(default=False)
    def __str__(self):              # __unicode__ on Python 2
        return self.question + " " + self.gender

################################# SCORE TABLE ##########################################################

class Members(models.Model):
    group_id             = models.ForeignKey(Group)
    name                 = models.CharField(max_length=60)
    GENDER_CHOICES       =   (
                                ('0', 'Female')
                                ,('1', 'Male')
                            )
    gender               = models.CharField(max_length=1,choices = GENDER_CHOICES,default = False )
    def __str__(self):              # __unicode__ on Python 2
        return self.name + " " + self.gender

class Ratings(models.Model):
    member_id            = models.ForeignKey(Members)
    question             = models.ForeignKey(Questions) 
    rating               = models.DecimalField(max_digits=20,decimal_places=2,null=True,blank=True)
    
class GroupQn(models.Model):
    group_id             = models.ForeignKey(Group)
    qn_id                = models.ForeignKey(Questions)     

####################################### SUGGESIONS #######################################

class Suggested_members(models.Model):
    group_id             = models.ForeignKey(Group)
    suggestion           = models.CharField(max_length=50)
    GENDER_CHOICES       =   (
                                ('0', 'Female')
                                ,('1', 'Male')
                            )
    gender               = models.CharField(max_length=1,choices = GENDER_CHOICES,default = False )
    def __str__(self):              # __unicode__ on Python 2
        return self.group_id.group_name + " " + self.suggestion

class Suggested_questions(models.Model):
    group_id             = models.ForeignKey(Group)
    suggestion           = models.CharField(max_length=50)
    GENDER_CHOICES  =   (
                            ('0', 'All')
                            ,('1', 'Female')
                            ,('2', 'Male')
                        )
    gender          = models.CharField(max_length=1,choices = GENDER_CHOICES,default = False )
    is_accepted          = models.BooleanField(default=False)
    def __str__(self):              # __unicode__ on Python 2
        return self.group_id.group_name + " " + self.suggestion
    