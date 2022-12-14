from django.shortcuts import render

# Create your views here.
from QUAN.serializers import UserSerializer,QuestionSerializer,AnswerSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from QUAN.models import Questions,Answers
from rest_framework import permissions,authentication
from rest_framework.decorators import action
class UserView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()
class QuestionsView(ModelViewSet):
    serializer_class = QuestionSerializer
    queryset =Questions.objects.all()
    authentication_classes =[authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    #localhost:8000/questions/my_questions/
    @action(methods=["GET"],detail=False)
    def my_questions(self,request,*arg,**kw):
        qs=request.user.questions_set.all()
        serializer=QuestionSerializer(qs,many=True)
        return Response(data=serializer.data)

    #localhost:8000/questions/add_answer/  
    @action(methods=["POST"],detail=True)
    def add_answer(self,request,*args,**kw):
        id=kw.get("pk")
        ques=Questions.objects.get(id=id)
        usr=request.user
        serializer=AnswerSerializer(data=request.data,context={"question":ques,"user":usr})
        if serializer.is_valid():
          serializer.save()
          return Response(data=serializer.data)
        else:
          return Response(data=serializer.errors)

     #localhost:8000/questions/LIST_answers/       
    @action(methods=["GET"],detail=True)     
    def list_answers(self,request,*args,**kw):
        id=kw.get("pk")
        ques=Questions.objects.get(id=id)
        qs=ques.answers_set.all()
        serializer =AnswerSerializer(qs,many=True)
        return Response(data=serializer.data)

class AnswerView(ModelViewSet):
    serializer_class = AnswerSerializer
    queryset =Answers.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    @action(methods=["get"],detail=True)      
    def upvote(self,request,*arg,**kw):
        ans=self.get_object()
        usr=request.user
        ans.upvote.add(usr)
        return Response(data="created")

    


 