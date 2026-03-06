import { createRouter, createWebHashHistory } from 'vue-router'

// 路由懒加载 - 代码分割优化
const Login = () => import(/* webpackChunkName: "login" */ "../views/login.vue")
const Home = () => import(/* webpackChunkName: "home" */ "../views/home.vue")
const Welcome = () => import(/* webpackChunkName: "welcome" */ "../views/pages/welcome.vue")

const routes = [
  {
    path: '/',
    name: 'login',
    component: Login
  },
  {
    path: '/home',
    name: 'home',
    component: Home,
    children: [
      {
        path: '',
        name: 'welcome',
        component: require("../views/pages/welcome.vue").default
      },
      {
        path: 'studentRegister',
        name: 'studentRegister',
        component: require("../views/pages/studentRegister.vue").default
      },
      {
        path: 'taskCenter',
        name: 'taskCenter',
        component: require("../views/pages/taskCenter.vue").default
      },
      {
        path: 'exams',
        name: 'exams',
        component: require("../views/pages/exams.vue").default
      },
      {
        path: 'practises',
        name: 'practises',
        component: require("../views/pages/practises.vue").default
      },
      {
        path: 'studentExamLogs',
        name: 'studentExamLogs',
        component: require("../views/pages/studentExamLogs.vue").default
      },
      {
        path: 'wrongQuestions',
        name: 'wrongQuestions',
        component: require("../views/pages/wrongQuestions.vue").default
      },
      {
        path: 'studentProfile',
        name: 'studentProfile',
        component: require("../views/pages/studentProfile.vue").default
      },
      {
        path: 'personalDynamics',
        name: 'personalDynamics',
        component: require("../views/pages/personalDynamics.vue").default
      },
      {
        path: 'messageCenter',
        name: 'messageCenter',
        component: require("../views/pages/messageCenter.vue").default
      },
      {
        path: '/home/answer',
        name: 'answer',
        component: require("../views/pages/answer.vue").default
      },
      {
        path: 'practiceResult',
        name: 'practiceResult',
        component: require("../views/pages/practiceResult.vue").default
      },
      {
        path: 'taskResult',
        name: 'taskResult',
        component: require("../views/pages/taskResult.vue").default
      },
      {
        path: 'aiScoring',
        name: 'aiScoring',
        component: require("../views/pages/aiScoring.vue").default
      },
      {
        path: 'aiQuestionGenerator',
        name: 'aiQuestionGenerator',
        component: require("../views/pages/aiQuestionGenerator.vue").default
      }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// 兼容从任意位置跳到 '/home/answer' 的写法
router.addRoute('home', {
  path: '/home/answer',
  name: 'answerAlias',
  component: require('../views/pages/answer.vue').default
})

export default router
