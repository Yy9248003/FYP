<template>
  <div class="admin-practice-papers">
    <div class="page-header">
      <h2>练习试卷管理</h2>
      <div>
        <Button type="primary" @click="reload" style="margin-right:8px">刷新</Button>
        <Button :disabled="!selectedRow" @click="openCreateExam" type="success">从选中试卷创建考试</Button>
      </div>
    </div>

    <div class="search-section">
      <Form :model="filters" inline>
        <FormItem>
          <Input v-model="filters.title" placeholder="标题关键词" style="width: 220px" />
        </FormItem>
        <FormItem>
          <Select v-model="filters.projectId" placeholder="所属学科" clearable style="width: 180px" transfer>
            <Option value="">全部学科</Option>
            <Option v-for="p in projects" :key="p.id" :value="String(p.id)" :label="String(p.name)">{{ p.name }}</Option>
          </Select>
        </FormItem>
        <FormItem>
          <Select v-model="filters.difficulty" placeholder="难度" clearable style="width: 150px" transfer>
            <Option value="">全部难度</Option>
            <Option value="easy">简单</Option>
            <Option value="medium">中等</Option>
            <Option value="hard">困难</Option>
          </Select>
        </FormItem>
        <FormItem>
          <Select v-model="filters.type" placeholder="类型" clearable style="width: 150px" transfer>
            <Option value="">全部类型</Option>
            <Option value="fixed">固定试卷</Option>
            <Option value="timed">时段试卷</Option>
          </Select>
        </FormItem>
        <FormItem>
          <Button type="primary" @click="onSearch">搜索</Button>
          <Button style="margin-left:8px" @click="onReset">重置</Button>
        </FormItem>
      </Form>
    </div>

    <Table :columns="columns" :data="list" :loading="loading" :pagination="pagination"
           @on-page-change="onPageChange" @on-page-size-change="onPageSizeChange"
           @on-current-change="onCurrentChange">
      <template #action="{ row }">
        <Button size="small" @click="openDetail(row)" style="margin-right:8px">详情</Button>
        <Button size="small" type="success" @click="openCreateExam(row)">创建考试</Button>
      </template>
    </Table>

    <Modal v-model="detail.visible" title="试卷详情" width="800">
      <div v-if="detail.info">
        <h3 style="margin-bottom:8px">{{ detail.info.title }}</h3>
        <p style="color:#666">{{ detail.info.description }}</p>
        <div class="info-grid">
          <div><b>学科：</b>{{ detail.info.projectName }}</div>
          <div><b>难度：</b>{{ dict.difficulty[detail.info.difficulty] || detail.info.difficulty }}</div>
          <div><b>类型：</b>{{ dict.type[detail.info.type] || detail.info.type }}</div>
          <div><b>时长：</b>{{ detail.info.duration }} 分钟</div>
          <div><b>总分：</b>{{ detail.info.totalScore }}</div>
          <div><b>题量：</b>{{ detail.info.questionCount }}</div>
          <div><b>创建时间：</b>{{ detail.info.createTime }}</div>
        </div>
        <Divider>题目列表</Divider>
        <Table :columns="qColumns" :data="detail.questions" size="small" :loading="detail.loading">
          <template #options="{ row }">
            <div v-if="row.options && row.options.length">
              <ol style="margin:0;padding-left:18px">
                <li v-for="(opt, i) in row.options" :key="i">{{ String.fromCharCode(65+i) }}. {{ opt }}</li>
              </ol>
            </div>
            <span v-else>-</span>
          </template>
        </Table>
      </div>
    </Modal>

    <Modal v-model="createExam.visible" title="从练习试卷创建考试" @on-ok="submitCreateExam">
      <Form :label-width="100">
        <FormItem label="考试名称">
          <Input v-model="createExam.form.name" placeholder="未填则使用 试卷标题-考试" />
        </FormItem>
        <FormItem label="教师工号">
          <Select v-model="createExam.form.teacherId" filterable placeholder="选择教师" transfer>
            <Option v-for="t in teachers" :key="t.id" :value="String(t.id)">{{ t.id }}（{{ t.name }}）</Option>
          </Select>
        </FormItem>
        <FormItem label="年级">
          <Select v-model="createExam.form.gradeId" filterable placeholder="选择年级" transfer>
            <Option v-for="g in grades" :key="g.id" :value="String(g.id)">{{ g.name }}</Option>
          </Select>
        </FormItem>
        <FormItem label="开始时间">
          <DatePicker v-model="createExam.form.startTime" type="datetime" placeholder="可选：开始时间" style="width:100%" transfer />
        </FormItem>
        <FormItem label="结束时间">
          <DatePicker v-model="createExam.form.endTime" type="datetime" placeholder="可选：结束时间" style="width:100%" transfer />
        </FormItem>
      </Form>
    </Modal>
  </div>
</template>

<script>
import { getAdminPracticePapers, getPracticePaperInfo, getPracticePaperQuestions, getAllProjects, listTeachers, listGrades } from '@/api'
import http from '@/utils/http'

export default {
  name: 'AdminPracticePapers',
  data() {
    return {
      loading: false,
      list: [],
      projects: [],
      filters: { title: '', projectId: '', difficulty: '', type: '' },
      pagination: {
        current: 1,
        pageSize: 10,
        total: 0,
        showSizeChanger: true,
        showQuickJumper: true,
        showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条，共 ${total} 条`
      },
      columns: [
        { title: 'ID', key: 'id', width: 80 },
        { title: '标题', key: 'title', minWidth: 220 },
        { title: '学科', key: 'projectName', width: 130 },
        { title: '难度', key: 'difficulty', width: 90, render: (h, p) => h('Tag', { props:{ color: p.row.difficulty==='easy'?'success':p.row.difficulty==='medium'?'warning':'error' } }, this.dict.difficulty[p.row.difficulty] || p.row.difficulty) },
        { title: '类型', key: 'type', width: 90, render: (h, p) => h('Tag', { props:{ color: p.row.type==='fixed'?'success':'warning' } }, this.dict.type[p.row.type] || p.row.type) },
        { title: '时长', key: 'duration', width: 80 },
        { title: '总分', key: 'totalScore', width: 80 },
        { title: '题量', key: 'questionCount', width: 80 },
        { title: '创建时间', key: 'createTime', width: 160 },
        { title: '操作', slot: 'action', width: 120, fixed: 'right' }
      ],
      qColumns: [
        { title: '#', key: 'questionOrder', width: 60 },
        { title: '类型', key: 'type', width: 90, render: (h,p)=> h('Tag', { props:{ color: ['blue','purple','orange','red'][p.row.type] } }, this.dict.qType[p.row.type] || p.row.type) },
        { title: '分值', key: 'score', width: 80 },
        { title: '题目', key: 'content', minWidth: 300 },
        { title: '选项', slot: 'options', minWidth: 240 }
      ],
      detail: { visible: false, info: null, questions: [], loading: false },
      selectedRow: null,
      createExam: { visible: false, form: { name: '', teacherId: '', gradeId: '', examTime: '', startTime: '', endTime: '' } },
      teachers: [],
      grades: [],
      dict: {
        difficulty: { easy: '简单', medium: '中等', hard: '困难' },
        type: { fixed: '固定试卷', timed: '时段试卷' },
        qType: { 0: '选择题', 1: '填空题', 2: '判断题', 3: '编程题' }
      }
    }
  },
  methods: {
    async loadProjects(){
      try { const resp = await getAllProjects(); if (resp.code === 0) this.projects = resp.data; } catch(e) { /* ignore */ }
    },
    async loadTeachers(){ try{ const resp = await listTeachers(); if (resp.code===0) this.teachers = resp.data?.data || [] }catch(_){} },
    async loadGrades(){ try{ const resp = await listGrades(); if (resp.code===0) this.grades = resp.data?.data || [] }catch(_){} },
    async loadList(){
      this.loading = true
      try{
        const params = {
          pageIndex: this.pagination.current,
          pageSize: this.pagination.pageSize,
          title: this.filters.title || '',
          projectId: this.filters.projectId || '',
          difficulty: this.filters.difficulty || '',
          type: this.filters.type || ''
        }
        const resp = await getAdminPracticePapers(params)
        if (resp.code === 0){
          const page = resp.data
          this.list = page.data || []
          this.pagination.total = page.count || 0
        } else {
          this.$Message.error(resp.msg || '加载失败')
        }
      }catch(e){
        console.error(e)
        this.$Message.error('加载失败')
      }finally{
        this.loading = false
      }
    },
    onPageChange(p){ this.pagination.current = p; this.loadList() },
    onPageSizeChange(s){ this.pagination.pageSize = s; this.pagination.current = 1; this.loadList() },
    onSearch(){ this.pagination.current = 1; this.loadList() },
    onReset(){ this.filters = { title:'', projectId:'', difficulty:'', type:'' }; this.pagination.current = 1; this.loadList() },
    reload(){ this.loadList() },
    async openDetail(row){
      this.detail.visible = true
      this.detail.info = null
      this.detail.questions = []
      this.detail.loading = true
      try{
        const info = await getPracticePaperInfo(row.id)
        if (info.code === 0) this.detail.info = info.data
        const qs = await getPracticePaperQuestions(row.id)
        if (qs.code === 0) this.detail.questions = qs.data
      }catch(e){
        console.error(e)
        this.$Message.error('加载详情失败')
      }finally{
        this.detail.loading = false
      }
    },
    onCurrentChange(current){ this.selectedRow = current },
    openCreateExam(row){
      if (row) this.selectedRow = row
      if (!this.selectedRow) { this.$Message.warning('请先选择一条试卷'); return }
      this.createExam.visible = true
      // 尝试自动填充教师工号（从本地登录信息）
      try {
        const token = this.$store.state.token || sessionStorage.getItem('token')
        if (token) {
          // 简化处理：若系统里教师ID即为 token->userId，可在后端提供接口获取，这里留空由用户填写
        }
      } catch(_) {}
    },
    async submitCreateExam(){
      try{
        const f = this.createExam.form
        if (!f.teacherId || !f.gradeId){ this.$Message.warning('请填写教师工号与年级ID'); return }
        const resp = await http.post('/exams/create_from_practice_paper/', {
          paperId: this.selectedRow.id,
          name: f.name,
          teacherId: f.teacherId,
          gradeId: f.gradeId,
          examTime: f.examTime ? f.examTime : '',
          startTime: f.startTime ? f.startTime : '',
          endTime: f.endTime ? f.endTime : ''
        })
        if (resp.code === 0){
          this.$Message.success('考试创建成功')
          this.createExam.visible = false
        } else {
          this.$Message.error(resp.msg || '创建失败')
        }
      }catch(e){
        console.error(e)
        this.$Message.error('创建失败')
      }
    }
  },
  async mounted(){
    await this.loadProjects()
    await this.loadTeachers()
    await this.loadGrades()
    await this.loadList()
  }
}
</script>

<style scoped>
.admin-practice-papers { padding: 24px; }
.page-header { display:flex; justify-content:space-between; align-items:center; margin-bottom: 16px; }
.search-section { margin-bottom: 16px; background:#f8f9fa; padding: 12px; border-radius: 6px; }
.info-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:8px; margin: 12px 0; }
</style>


