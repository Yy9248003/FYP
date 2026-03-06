<template>
  <div class="admin-exams">
    <div class="page-header">
      <h2>试卷管理</h2>
      <Button type="primary" @click="showAddModal">创建试卷</Button>
    </div>

    <div class="search-section">
      <Input 
        v-model="searchKeyword" 
        placeholder="请输入试卷标题或描述" 
        style="width: 300px; margin-right: 16px;"
        @on-enter="handleSearch"
      />
      <Select 
        v-model="searchType" 
        placeholder="试卷类型" 
        style="width: 150px; margin-right: 16px;"
        clearable
      >
        <Option value="fixed">固定试卷</Option>
        <Option value="timed">时段试卷</Option>
        <Option value="task">任务试卷</Option>
      </Select>
      <Button type="primary" @click="handleSearch">搜索</Button>
      <Button @click="resetSearch" style="margin-left: 8px;">重置</Button>
    </div>

    <Table 
      :columns="columns" 
      :data="exams" 
      :loading="loading"
      :pagination="pagination"
      @on-page-change="handlePageChange"
      @on-page-size-change="handlePageSizeChange"
    >
      <template #action="{ row }">
        <Button type="primary" size="small" @click="editExam(row)" style="margin-right: 8px;">编辑</Button>
        <Button type="success" size="small" @click="manageQuestions(row)" style="margin-right: 8px;">题目管理</Button>
        <Button type="error" size="small" @click="deleteExam(row)">删除</Button>
      </template>
    </Table>

    <!-- 添加/编辑试卷模态框 -->
    <Modal 
      v-model="showModal" 
      :title="isEdit ? '编辑试卷' : '创建试卷'"
      width="800"
      @on-ok="handleSubmit"
      @on-cancel="handleCancel"
    >
      <Form ref="formRef" :model="formData" :rules="formRules" :label-width="100">
        <Row :gutter="16">
          <Col span="12">
            <FormItem label="试卷标题" prop="title">
              <Input v-model="formData.title" placeholder="请输入试卷标题" />
            </FormItem>
          </Col>
          <Col span="12">
            <FormItem label="试卷类型" prop="type">
              <Select v-model="formData.type" placeholder="请选择试卷类型">
                <Option value="fixed">固定试卷</Option>
                <Option value="timed">时段试卷</Option>
                <Option value="task">任务试卷</Option>
              </Select>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="16">
          <Col span="12">
            <FormItem label="所属学科" prop="project">
              <Select v-model="formData.project" placeholder="请选择学科" filterable>
                <Option 
                  v-for="project in projects" 
                  :key="project.id" 
                  :value="String(project.id)"
                  :label="String(project.name)"
                >
                  {{ project.name }}
                </Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="12">
            <FormItem label="难度等级" prop="difficulty">
              <Select v-model="formData.difficulty" placeholder="请选择难度">
                <Option value="easy">简单</Option>
                <Option value="medium">中等</Option>
                <Option value="hard">困难</Option>
              </Select>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="16">
          <Col span="12">
            <FormItem label="考试时长(分钟)" prop="duration">
              <InputNumber v-model="formData.duration" :min="1" :max="480" style="width: 100%" />
            </FormItem>
          </Col>
          <Col span="12">
            <FormItem label="总分" prop="totalScore">
              <InputNumber v-model="formData.totalScore" :min="1" :max="200" style="width: 100%" />
            </FormItem>
          </Col>
        </Row>
        <FormItem label="试卷描述" prop="description">
          <Input 
            v-model="formData.description" 
            type="textarea" 
            :rows="3"
            placeholder="请输入试卷描述" 
          />
        </FormItem>
        <Row :gutter="16">
          <Col span="12">
            <FormItem label="开始时间" prop="startTime" v-if="formData.type === 'timed'">
              <DatePicker 
                v-model="formData.startTime" 
                type="datetime" 
                placeholder="选择开始时间"
                style="width: 100%"
              />
            </FormItem>
          </Col>
          <Col span="12">
            <FormItem label="结束时间" prop="endTime" v-if="formData.type === 'timed'">
              <DatePicker 
                v-model="formData.endTime" 
                type="datetime" 
                placeholder="选择结束时间"
                style="width: 100%"
              />
            </FormItem>
          </Col>
        </Row>
        <FormItem label="是否启用" prop="isActive">
          <Switch v-model="formData.isActive" />
        </FormItem>
      </Form>
    </Modal>

    <!-- 删除确认模态框 -->
    <Modal v-model="showDeleteModal" title="确认删除" @on-ok="confirmDelete">
      <p>确定要删除试卷 "{{ examToDelete.title }}" 吗？此操作不可恢复。</p>
    </Modal>
  </div>
</template>

<script>
import { getAdminExams, addAdminExam, updateAdminExam, deleteAdminExam, getAllProjects } from '@/api'

export default {
  name: 'AdminExams',
  data() {
    return {
      loading: false,
      searchKeyword: '',
      searchType: '',
      exams: [],
      projects: [],
      columns: [
        { title: 'ID', key: 'id', width: 80 },
        { title: '试卷标题', key: 'title', minWidth: 200 },
        { title: '试卷类型', key: 'type', width: 120,
          render: (h, params) => {
            const typeMap = {
              'fixed': '固定试卷',
              'timed': '时段试卷',
              'task': '任务试卷'
            }
            return h('Tag', {
              props: {
                color: params.row.type === 'fixed' ? 'blue' : params.row.type === 'timed' ? 'green' : 'orange'
              }
            }, typeMap[params.row.type] || params.row.type)
          }
        },
        { title: '学科', key: 'projectName', width: 120 },
        { title: '难度', key: 'difficulty', width: 100,
          render: (h, params) => {
            const difficultyMap = {
              'easy': '简单',
              'medium': '中等',
              'hard': '困难'
            }
            return h('Tag', {
              props: {
                color: params.row.difficulty === 'easy' ? 'success' : params.row.difficulty === 'medium' ? 'warning' : 'error'
              }
            }, difficultyMap[params.row.difficulty] || params.row.difficulty)
          }
        },
        { title: '时长(分钟)', key: 'duration', width: 100 },
        { title: '总分', key: 'totalScore', width: 80 },
        { title: '状态', key: 'isActive', width: 100,
          render: (h, params) => {
            return h('Tag', {
              props: {
                color: params.row.isActive ? 'success' : 'default'
              }
            }, params.row.isActive ? '启用' : '禁用')
          }
        },
        { title: '创建时间', key: 'createTime', width: 150 },
        { title: '操作', slot: 'action', width: 200, fixed: 'right' }
      ],
      pagination: {
        current: 1,
        pageSize: 10,
        total: 0,
        showSizeChanger: true,
        showQuickJumper: true,
        showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条，共 ${total} 条`
      },
      showModal: false,
      isEdit: false,
      formData: {
        title: '',
        description: '',
        type: 'fixed',
        difficulty: 'medium',
        duration: 60,
        totalScore: 100,
        project: null,
        startTime: null,
        endTime: null,
        isActive: true
      },
      formRules: {
        title: [
          { required: true, message: '请输入试卷标题', trigger: 'blur' }
        ],
        type: [
          { required: true, message: '请选择试卷类型', trigger: 'change' }
        ],
        project: [
          { required: true, message: '请选择学科', trigger: 'change' }
        ],
        difficulty: [
          { required: true, message: '请选择难度等级', trigger: 'change' }
        ],
        duration: [
          { required: true, message: '请输入考试时长', trigger: 'blur' }
        ],
        totalScore: [
          { required: true, message: '请输入总分', trigger: 'blur' }
        ]
      },
      showDeleteModal: false,
      examToDelete: {}
    }
  },
  mounted() {
    this.loadExams()
    this.loadProjects()
  },
  methods: {
    async loadExams() {
      this.loading = true
      try {
        const response = await getAdminExams({
          page: this.pagination.current,
          pageSize: this.pagination.pageSize,
          keyword: this.searchKeyword,
          type: this.searchType
        })
        if (response.code === 0) {
          this.exams = response.data.list
          this.pagination.total = response.data.total
        } else {
          this.$Message.error(response.msg || '加载试卷列表失败')
        }
      } catch (error) {
        console.error('加载试卷列表失败:', error)
        this.$Message.error('加载试卷列表失败')
      } finally {
        this.loading = false
      }
    },

    async loadProjects() {
      try {
        const response = await getAllProjects()
        if (response.code === 0) {
          this.projects = response.data
        }
      } catch (error) {
        console.error('加载学科列表失败:', error)
      }
    },

    handleSearch() {
      this.pagination.current = 1
      this.loadExams()
    },

    resetSearch() {
      this.searchKeyword = ''
      this.searchType = ''
      this.pagination.current = 1
      this.loadExams()
    },

    handlePageChange(page) {
      this.pagination.current = page
      this.loadExams()
    },

    handlePageSizeChange(pageSize) {
      this.pagination.pageSize = pageSize
      this.pagination.current = 1
      this.loadExams()
    },

    showAddModal() {
      this.isEdit = false
      this.formData = {
        title: '',
        description: '',
        type: 'fixed',
        difficulty: 'medium',
        duration: 60,
        totalScore: 100,
        project: null,
        startTime: null,
        endTime: null,
        isActive: true
      }
      this.showModal = true
    },

    editExam(exam) {
      this.isEdit = true
      this.formData = { ...exam }
      this.showModal = true
    },

    manageQuestions(exam) {
      // 跳转到题目管理页面
      this.$router.push(`/admin/questions?examId=${exam.id}`)
    },

    async handleSubmit() {
      try {
        const valid = await this.$refs.formRef.validate()
        if (!valid) return

        let response
        if (this.isEdit) {
          response = await updateAdminExam(this.formData)
        } else {
          response = await addAdminExam(this.formData)
        }

        if (response.code === 0) {
          this.$Message.success(this.isEdit ? '编辑成功' : '创建成功')
          this.showModal = false
          this.loadExams()
        } else {
          this.$Message.error(response.msg || '操作失败')
        }
      } catch (error) {
        console.error('操作失败:', error)
        this.$Message.error('操作失败')
      }
    },

    handleCancel() {
      this.showModal = false
      this.$refs.formRef.resetFields()
    },

    deleteExam(exam) {
      this.examToDelete = exam
      this.showDeleteModal = true
    },

    async confirmDelete() {
      try {
        const response = await deleteAdminExam(this.examToDelete.id)
        if (response.code === 0) {
          this.$Message.success('删除成功')
          this.loadExams()
        } else {
          this.$Message.error(response.msg || '删除失败')
        }
      } catch (error) {
        console.error('删除失败:', error)
        this.$Message.error('删除失败')
      } finally {
        this.showDeleteModal = false
      }
    }
  }
}
</script>

<style scoped>
.admin-exams {
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h2 {
  margin: 0;
  color: #17233d;
}

.search-section {
  margin-bottom: 24px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 6px;
}

.search-section .ivu-input,
.search-section .ivu-select {
  margin-right: 16px;
}
</style>
