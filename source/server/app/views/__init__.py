"""
视图模块
按功能模块组织的视图类
优先使用拆分后的视图，如果不存在则从旧views.py导入
"""
# 导入已拆分的视图
from .sys_view import SysView

# 为了避免循环导入，使用importlib动态导入旧视图模块
# 注意：不能直接 import app.views，因为那会导入这个包本身
import sys
import importlib.util
import os

# 获取旧views.py的路径（相对于当前文件）
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
_views_py_path = os.path.join(_parent_dir, 'views.py')

# 动态加载旧视图模块
if os.path.exists(_views_py_path):
    spec = importlib.util.spec_from_file_location("app_views_old", _views_py_path)
    old_views_module = importlib.util.module_from_spec(spec)
    # 使用一个唯一的模块名避免冲突
    sys.modules['app_views_old'] = old_views_module
    spec.loader.exec_module(old_views_module)
    
    # 从旧视图导入所有类
    CollegesView = old_views_module.CollegesView
    GradesView = old_views_module.GradesView
    ProjectsView = old_views_module.ProjectsView
    TeachersView = old_views_module.TeachersView
    StudentsView = old_views_module.StudentsView
    PractisesView = old_views_module.PractisesView
    ExamsView = old_views_module.ExamsView
    ExamLogsView = old_views_module.ExamLogsView
    PracticePapersView = old_views_module.PracticePapersView
    TasksView = old_views_module.TasksView
    WrongQuestionsView = old_views_module.WrongQuestionsView
    AdminView = old_views_module.AdminView
    AIView = old_views_module.AIView
    OptionsView = old_views_module.OptionsView
    AnswerLogsView = old_views_module.AnswerLogsView
    StudentPracticeView = old_views_module.StudentPracticeView
else:
    # 如果views.py不存在，抛出错误
    raise ImportError(f"Cannot find app/views.py file at {_views_py_path}")

__all__ = [
    'SysView',
    'CollegesView',
    'GradesView',
    'ProjectsView',
    'TeachersView',
    'StudentsView',
    'PractisesView',
    'ExamsView',
    'ExamLogsView',
    'PracticePapersView',
    'TasksView',
    'WrongQuestionsView',
    'AdminView',
    'AIView',
    'OptionsView',
    'AnswerLogsView',
    'StudentPracticeView',
]
