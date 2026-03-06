# 从新的模块化视图导入（包括已拆分和未拆分的）
from app.views import (
    SysView, CollegesView, GradesView, ProjectsView,
    TeachersView, StudentsView, PractisesView, ExamsView,
    ExamLogsView, PracticePapersView, TasksView, WrongQuestionsView,
    AdminView, AIView, OptionsView, AnswerLogsView, StudentPracticeView
)

from django.urls import path

urlpatterns = [
    path('<str:module>/', SysView.as_view()),
    path('colleges/<str:module>/', CollegesView.as_view()),
    path('grades/<str:module>/', GradesView.as_view()),
    path('projects/<str:module>/', ProjectsView.as_view()),
    path('students/<str:module>/', StudentsView.as_view()),
    path('teachers/<str:module>/', TeachersView.as_view()),
    path('practises/<str:module>/', PractisesView.as_view()),
    path('options/<str:module>/', OptionsView.as_view()),
    path('exams/<str:module>/', ExamsView.as_view()),
    path('examlogs/<str:module>/', ExamLogsView.as_view()),
    path('answerlogs/<str:module>/', AnswerLogsView.as_view()),
    path('practicepapers/<str:module>/', PracticePapersView.as_view()),
    path('studentpractice/<str:module>/', StudentPracticeView.as_view()),
    path('tasks/<str:module>/', TasksView.as_view()),
    path('wrongquestions/<str:module>/', WrongQuestionsView.as_view()),
    path('admin/<str:module>/', AdminView.as_view()),
    path('ai/<str:module>/', AIView.as_view()),
]