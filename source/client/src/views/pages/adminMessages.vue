<template>
  <div class="admin-messages">
    <div class="page-header">
      <h2>消息管理</h2>
      <Button type="primary" @click="openSendModal">发送消息</Button>
    </div>

    <div class="search-section">
      <Input 
        v-model="searchKeyword" 
        placeholder="请输入消息标题或内容" 
        style="width: 300px; margin-right: 16px;"
        @on-enter="handleSearch"
      />
      <Select 
        v-model="searchType" 
        placeholder="消息类型" 
        style="width: 150px; margin-right: 16px;"
        clearable
      >
        <Option value="notice">通知公告</Option>
        <Option value="task">任务提醒</Option>
        <Option value="exam">考试提醒</Option>
        <Option value="system">系统消息</Option>
      </Select>
      <Button type="primary" @click="handleSearch">搜索</Button>
      <Button @click="resetSearch" style="margin-left: 8px;">重置</Button>
    </div>

    <Table 
      :columns="columns" 
      :data="messages" 
      :loading="loading"
      :pagination="pagination"
      @on-page-change="handlePageChange"
      @on-page-size-change="handlePageSizeChange"
    >
      <template #action="{ row }">
        <Button type="primary" size="small" @click="viewMessage(row)" style="margin-right: 8px;">查看</Button>
        <Button type="success" size="small" @click="viewReaders(row)" style="margin-right: 8px;">已读情况</Button>
        <Button type="error" size="small" @click="deleteMessage(row)">删除</Button>
      </template>
    </Table>

    <!-- 发送消息模态框 -->
    <Modal 
      v-model="showSendModal" 
      title="发送消息"
      width="800"
      @on-ok="handleSendMessage"
      @on-cancel="handleCancel"
    >
      <Form ref="formRef" :model="formData" :rules="formRules" :label-width="100">
        <Row :gutter="16">
          <Col span="12">
            <FormItem label="消息标题" prop="title">
              <Input v-model="formData.title" placeholder="请输入消息标题" />
            </FormItem>
          </Col>
          <Col span="12">
            <FormItem label="消息类型" prop="type">
              <Select v-model="formData.type" placeholder="请选择消息类型">
                <Option value="notice">通知公告</Option>
                <Option value="task">任务提醒</Option>
                <Option value="exam">考试提醒</Option>
                <Option value="system">系统消息</Option>
              </Select>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="16">
          <Col span="12">
            <FormItem label="接收用户类型" prop="userType">
              <Select v-model="formData.userType" placeholder="请选择接收用户类型" @on-change="onUserTypeChange">
                <Option value="all">所有用户</Option>
                <Option value="student">学生</Option>
                <Option value="teacher">教师</Option>
                <Option value="admin">管理员</Option>
                <Option value="custom">自定义选择</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="12">
            <FormItem label="优先级" prop="priority">
              <Select v-model="formData.priority" placeholder="请选择优先级">
                <Option value="low">低</Option>
                <Option value="medium">中</Option>
                <Option value="high">高</Option>
                <Option value="urgent">紧急</Option>
              </Select>
            </FormItem>
          </Col>
        </Row>
        
        <!-- 自定义选择用户 -->
        <div v-if="formData.userType === 'custom'">
          <FormItem label="选择用户">
            <div class="user-selection">
              <div class="user-type-tabs">
                <Tabs v-model="activeUserTab">
                  <TabPane label="按年级选择" name="grade">
                    <div class="grade-selection">
                      <div v-for="grade in grades" :key="grade.id" class="grade-item">
                        <Checkbox 
                          v-model="selectedGrades" 
                          :value="grade.id"
                          @on-change="updateSelectedUsers"
                        >
                          {{ grade.name }}
                        </Checkbox>
                      </div>
                    </div>
                  </TabPane>
                  <TabPane label="按学院选择" name="college">
                    <div class="college-selection">
                      <div v-for="college in colleges" :key="college.id" class="college-item">
                        <Checkbox 
                          v-model="selectedColleges" 
                          :value="college.id"
                          @on-change="updateSelectedUsers"
                        >
                          {{ college.name }}
                        </Checkbox>
                      </div>
                    </div>
                  </TabPane>
                  <TabPane label="手动选择" name="manual">
                    <div class="manual-selection">
                      <Input 
                        v-model="searchUser" 
                        placeholder="搜索用户名或姓名" 
                        style="margin-bottom: 16px;"
                        @on-enter="searchUsers"
                      />
                      <div class="user-list">
                        <div v-for="user in filteredUsers" :key="user.id" class="user-item">
                          <Checkbox 
                            v-model="selectedUsers" 
                            :value="user.id"
                          >
                            {{ user.userName }} ({{ user.realName }})
                          </Checkbox>
                        </div>
                      </div>
                    </div>
                  </TabPane>
                </Tabs>
              </div>
            </div>
          </FormItem>
        </div>

        <FormItem label="消息内容" prop="content">
          <Input 
            v-model="formData.content" 
            type="textarea" 
            :rows="4"
            placeholder="请输入消息内容" 
          />
        </FormItem>
        
        <FormItem label="是否置顶" prop="isTop">
          <Switch v-model="formData.isTop" />
        </FormItem>
      </Form>
    </Modal>

    <!-- 查看消息详情模态框 -->
    <Modal v-model="showViewModal" title="消息详情" width="600">
      <div class="message-detail">
        <div class="detail-item">
          <label>消息标题：</label>
          <span>{{ currentMessage.title }}</span>
        </div>
        <div class="detail-item">
          <label>消息类型：</label>
          <Tag :color="getTypeColor(currentMessage.type)">
            {{ getTypeName(currentMessage.type) }}
          </Tag>
        </div>
        <div class="detail-item">
          <label>优先级：</label>
          <Tag :color="getPriorityColor(currentMessage.priority)">
            {{ getPriorityName(currentMessage.priority) }}
          </Tag>
        </div>
        <div class="detail-item">
          <label>发送时间：</label>
          <span>{{ currentMessage.createTime }}</span>
        </div>
        <div class="detail-item">
          <label>消息内容：</label>
          <div class="message-content">{{ currentMessage.content }}</div>
        </div>
      </div>
    </Modal>

    <!-- 查看已读情况模态框 -->
    <Modal v-model="showReadersModal" title="已读情况" width="800">
      <div class="readers-info">
        <div class="stats-row">
          <div class="stat-item">
            <span class="stat-label">总接收人数：</span>
            <span class="stat-value">{{ readersInfo.totalCount }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">已读人数：</span>
            <span class="stat-value success">{{ readersInfo.readCount }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">未读人数：</span>
            <span class="stat-value warning">{{ readersInfo.unreadCount }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">已读率：</span>
            <span class="stat-value">{{ readersInfo.readRate }}%</span>
          </div>
        </div>
        <Table 
          :columns="readersColumns" 
          :data="readersInfo.readers" 
          :loading="readersLoading"
          :pagination="readersPagination"
          @on-page-change="handleReadersPageChange"
        />
      </div>
    </Modal>

    <!-- 删除确认模态框 -->
    <Modal v-model="showDeleteModal" title="确认删除" @on-ok="confirmDelete">
      <p>确定要删除这条消息吗？此操作不可恢复。</p>
    </Modal>
  </div>
</template>

<script>
import { 
  getAdminMessages, 
  sendAdminMessage, 
  deleteAdminMessage, 
  getMessageReaders,
  getAllGrades,
  getAllColleges,
  getAllUsers
} from '@/api'

export default {
  name: 'AdminMessages',
  data() {
    return {
      loading: false,
      searchKeyword: '',
      searchType: '',
      messages: [],
      columns: [
        { title: 'ID', key: 'id', width: 80 },
        { title: '消息标题', key: 'title', minWidth: 200 },
        { title: '消息类型', key: 'type', width: 120,
          render: (h, params) => {
            return h('Tag', {
              props: {
                color: this.getTypeColor(params.row.type)
              }
            }, this.getTypeName(params.row.type))
          }
        },
        { title: '优先级', key: 'priority', width: 100,
          render: (h, params) => {
            return h('Tag', {
              props: {
                color: this.getPriorityColor(params.row.priority)
              }
            }, this.getPriorityName(params.row.priority))
          }
        },
        { title: '接收人数', key: 'receiverCount', width: 100 },
        { title: '已读人数', key: 'readCount', width: 100 },
        { title: '已读率', key: 'readRate', width: 100,
          render: (h, params) => {
            const rate = params.row.readRate || 0
            return h('span', {
              style: {
                color: rate >= 80 ? '#19be6b' : rate >= 50 ? '#ff9900' : '#ed4014'
              }
            }, `${rate}%`)
          }
        },
        { title: '是否置顶', key: 'isTop', width: 100,
          render: (h, params) => {
            return h('Tag', {
              props: {
                color: params.row.isTop ? 'red' : 'default'
              }
            }, params.row.isTop ? '是' : '否')
          }
        },
        { title: '发送时间', key: 'createTime', width: 150 },
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
      showSendModal: false,
      showViewModal: false,
      showReadersModal: false,
      showDeleteModal: false,
      formData: {
        title: '',
        type: 'notice',
        userType: 'all',
        priority: 'medium',
        content: '',
        isTop: false,
        selectedUsers: []
      },
      formRules: {
        title: [
          { required: true, message: '请输入消息标题', trigger: 'blur' }
        ],
        type: [
          { required: true, message: '请选择消息类型', trigger: 'change' }
        ],
        userType: [
          { required: true, message: '请选择接收用户类型', trigger: 'change' }
        ],
        content: [
          { required: true, message: '请输入消息内容', trigger: 'blur' }
        ]
      },
      currentMessage: {},
      readersInfo: {
        totalCount: 0,
        readCount: 0,
        unreadCount: 0,
        readRate: 0,
        readers: []
      },
      readersLoading: false,
      readersPagination: {
        current: 1,
        pageSize: 10,
        total: 0
      },
      readersColumns: [
        { title: '用户名', key: 'userName', width: 120 },
        { title: '真实姓名', key: 'realName', width: 120 },
        { title: '用户类型', key: 'userType', width: 100,
          render: (h, params) => {
            const typeMap = { 0: '管理员', 1: '教师', 2: '学生' }
            return h('Tag', {
              props: {
                color: params.row.userType === 0 ? 'red' : params.row.userType === 1 ? 'blue' : 'green'
              }
            }, typeMap[params.row.userType] || '未知')
          }
        },
        { title: '阅读时间', key: 'readTime', width: 150 },
        { title: '状态', key: 'isRead', width: 100,
          render: (h, params) => {
            return h('Tag', {
              props: {
                color: params.row.isRead ? 'success' : 'default'
              }
            }, params.row.isRead ? '已读' : '未读')
          }
        }
      ],
      grades: [],
      colleges: [],
      users: [],
      selectedGrades: [],
      selectedColleges: [],
      selectedUsers: [],
      activeUserTab: 'grade',
      searchUser: '',
      messageToDelete: {}
    }
  },
  computed: {
    filteredUsers() {
      if (!this.searchUser) return this.users
      return this.users.filter(user => 
        user.userName.includes(this.searchUser) || 
        user.realName.includes(this.searchUser)
      )
    }
  },
  mounted() {
    this.loadMessages()
    this.loadGrades()
    this.loadColleges()
    this.loadUsers()
  },
  methods: {
    getTypeColor(type) {
      const colorMap = {
        'notice': 'blue',
        'task': 'green',
        'exam': 'orange',
        'system': 'red'
      }
      return colorMap[type] || 'default'
    },

    getTypeName(type) {
      const nameMap = {
        'notice': '通知公告',
        'task': '任务提醒',
        'exam': '考试提醒',
        'system': '系统消息'
      }
      return nameMap[type] || type
    },

    getPriorityColor(priority) {
      const colorMap = {
        'low': 'default',
        'medium': 'blue',
        'high': 'orange',
        'urgent': 'red'
      }
      return colorMap[priority] || 'default'
    },

    getPriorityName(priority) {
      const nameMap = {
        'low': '低',
        'medium': '中',
        'high': '高',
        'urgent': '紧急'
      }
      return nameMap[priority] || priority
    },

    async loadMessages() {
      this.loading = true
      try {
        const response = await getAdminMessages({
          page: this.pagination.current,
          pageSize: this.pagination.pageSize,
          keyword: this.searchKeyword,
          type: this.searchType
        })
        if (response.code === 0) {
          this.messages = (response.data.list || []).map(m => {
            const total = m.totalRecipients != null ? m.totalRecipients : (m.receiverCount || 0)
            const read = m.readCount || 0
            const rate = total > 0 ? Math.round((read / total) * 100) : 0
            return {
              ...m,
              receiverCount: total,
              readCount: read,
              readRate: rate
            }
          })
          this.pagination.total = response.data.total
        } else {
          this.$Message.error(response.msg || '加载消息列表失败')
        }
      } catch (error) {
        console.error('加载消息列表失败:', error)
        this.$Message.error('加载消息列表失败')
      } finally {
        this.loading = false
      }
    },

    async loadGrades() {
      try {
        const response = await getAllGrades()
        if (response.code === 0) {
          this.grades = response.data
        }
      } catch (error) {
        console.error('加载年级列表失败:', error)
      }
    },

    async loadColleges() {
      try {
        const response = await getAllColleges()
        if (response.code === 0) {
          this.colleges = response.data
        }
      } catch (error) {
        console.error('加载学院列表失败:', error)
      }
    },

    async loadUsers() {
      try {
        const response = await getAllUsers()
        if (response.code === 0) {
          this.users = response.data
        }
      } catch (error) {
        console.error('加载用户列表失败:', error)
      }
    },

    handleSearch() {
      this.pagination.current = 1
      this.loadMessages()
    },

    resetSearch() {
      this.searchKeyword = ''
      this.searchType = ''
      this.pagination.current = 1
      this.loadMessages()
    },

    handlePageChange(page) {
      this.pagination.current = page
      this.loadMessages()
    },

    handlePageSizeChange(pageSize) {
      this.pagination.pageSize = pageSize
      this.pagination.current = 1
      this.loadMessages()
    },

    openSendModal() {
      this.formData = {
        title: '',
        type: 'notice',
        userType: 'all',
        priority: 'medium',
        content: '',
        isTop: false,
        selectedUsers: []
      }
      this.selectedGrades = []
      this.selectedColleges = []
      this.selectedUsers = []
      this.showSendModal = true
    },

    onUserTypeChange(userType) {
      if (userType !== 'custom') {
        this.selectedGrades = []
        this.selectedColleges = []
        this.selectedUsers = []
      }
    },

    updateSelectedUsers() {
      // 根据选择的年级和学院更新选中的用户
      this.selectedUsers = []
      
      if (this.selectedGrades.length > 0) {
        const gradeUsers = this.users.filter(user => 
          user.userType === 2 && this.selectedGrades.includes(user.grade)
        )
        this.selectedUsers.push(...gradeUsers.map(u => u.id))
      }
      
      if (this.selectedColleges.length > 0) {
        const collegeUsers = this.users.filter(user => 
          user.userType === 2 && this.selectedColleges.includes(user.college)
        )
        this.selectedUsers.push(...collegeUsers.map(u => u.id))
      }
      
      // 去重
      this.selectedUsers = [...new Set(this.selectedUsers)]
    },

    searchUsers() {
      // 搜索用户的逻辑已在computed中实现
    },

    async handleSendMessage() {
      try {
        const valid = await this.$refs.formRef.validate()
        if (!valid) return

        const token = this.$store.state.token || sessionStorage.getItem('token')
        if (!token) {
          this.$Message.error('未登录，无法发送消息')
          return
        }

        // 仅在自定义模式下需要显式选择接收者
        let recipientIds = []
        if (this.formData.userType === 'custom') {
          recipientIds = [...this.selectedUsers]
          if (!recipientIds.length) {
            this.$Message.warning('未选择任何接收者')
            return
          }
        }

        // 使用 FormData 以兼容后端的 recipientIds[]
        const formData = new FormData()
        formData.append('token', token)
        formData.append('action', 'send')
        formData.append('title', this.formData.title)
        formData.append('content', this.formData.content)
        formData.append('type', this.formData.type)
        formData.append('priority', this.formData.priority)
        formData.append('userType', this.formData.userType)
        recipientIds.forEach(id => formData.append('recipientIds[]', id))

        const response = await sendAdminMessage(formData)
        if (response.code === 0) {
          this.$Message.success('发送成功')
          this.showSendModal = false
          this.loadMessages()
        } else {
          this.$Message.error(response.msg || '发送失败')
        }
      } catch (error) {
        console.error('发送失败:', error)
        this.$Message.error('发送失败')
      }
    },

    handleCancel() {
      this.showSendModal = false
      this.$refs.formRef.resetFields()
    },

    viewMessage(message) {
      this.currentMessage = message
      this.showViewModal = true
    },

    async viewReaders(message) {
      this.currentMessage = message
      this.showReadersModal = true
      this.readersPagination.current = 1
      await this.loadMessageReaders()
    },

    async loadMessageReaders() {
      this.readersLoading = true
      try {
        const response = await getMessageReaders({
          messageId: this.currentMessage.id,
          page: this.readersPagination.current,
          pageSize: this.readersPagination.pageSize
        })
        if (response.code === 0) {
          this.readersInfo = response.data
          this.readersPagination.total = response.data.total
        } else {
          this.$Message.error(response.msg || '加载已读情况失败')
        }
      } catch (error) {
        console.error('加载已读情况失败:', error)
        this.$Message.error('加载已读情况失败')
      } finally {
        this.readersLoading = false
      }
    },

    handleReadersPageChange(page) {
      this.readersPagination.current = page
      this.loadMessageReaders()
    },

    deleteMessage(message) {
      this.messageToDelete = message
      this.showDeleteModal = true
    },

    async confirmDelete() {
      try {
        const response = await deleteAdminMessage(this.messageToDelete.id)
        if (response.code === 0) {
          this.$Message.success('删除成功')
          this.loadMessages()
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
.admin-messages {
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

.user-selection {
  border: 1px solid #e8eaec;
  border-radius: 4px;
  padding: 16px;
}

.grade-selection,
.college-selection {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
}

.grade-item,
.college-item {
  padding: 8px;
  border: 1px solid #e8eaec;
  border-radius: 4px;
  background: #fafafa;
}

.manual-selection {
  max-height: 300px;
  overflow-y: auto;
}

.user-list {
  max-height: 200px;
  overflow-y: auto;
}

.user-item {
  padding: 8px;
  border-bottom: 1px solid #f0f0f0;
}

.user-item:last-child {
  border-bottom: none;
}

.message-detail {
  padding: 16px;
}

.detail-item {
  margin-bottom: 16px;
  display: flex;
  align-items: flex-start;
}

.detail-item label {
  font-weight: bold;
  width: 100px;
  flex-shrink: 0;
}

.message-content {
  margin-top: 8px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 4px;
  white-space: pre-wrap;
  line-height: 1.6;
}

.readers-info {
  padding: 16px;
}

.stats-row {
  display: flex;
  justify-content: space-around;
  margin-bottom: 24px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 6px;
}

.stat-item {
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #999;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 18px;
  font-weight: bold;
  color: #17233d;
}

.stat-value.success {
  color: #19be6b;
}

.stat-value.warning {
  color: #ff9900;
}
</style>
