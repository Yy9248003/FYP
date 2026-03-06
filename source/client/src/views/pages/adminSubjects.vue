<template>
  <div class="admin-subjects">
    <div class="page-header">
      <h2>学科管理</h2>
      <Button type="primary" @click="showAddModal">创建学科</Button>
    </div>

    <div class="search-section">
      <Input 
        v-model="searchKeyword" 
        placeholder="请输入学科名称或描述" 
        style="width: 300px; margin-right: 16px;"
        @on-enter="handleSearch"
      />
      <Button type="primary" @click="handleSearch">搜索</Button>
      <Button @click="resetSearch" style="margin-left: 8px;">重置</Button>
    </div>

    <Table 
      :columns="columns" 
      :data="subjects" 
      :loading="loading"
      :pagination="pagination"
      @on-page-change="handlePageChange"
      @on-page-size-change="handlePageSizeChange"
    >
      <template #action="{ row }">
        <Button type="primary" size="small" @click="editSubject(row)" style="margin-right: 8px;">编辑</Button>
        <Button type="error" size="small" @click="deleteSubject(row)">删除</Button>
      </template>
    </Table>

    <!-- 添加/编辑学科模态框 -->
    <Modal 
      v-model="showModal" 
      :title="isEdit ? '编辑学科' : '创建学科'"
      @on-ok="handleSubmit"
      @on-cancel="handleCancel"
    >
      <Form ref="formRef" :model="formData" :rules="formRules" :label-width="80">
        <FormItem label="学科名称" prop="name">
          <Input v-model="formData.name" placeholder="请输入学科名称" />
        </FormItem>
        <FormItem label="学科描述" prop="description">
          <Input 
            v-model="formData.description" 
            type="textarea" 
            :rows="3"
            placeholder="请输入学科描述" 
          />
        </FormItem>
        <FormItem label="学科代码" prop="code">
          <Input v-model="formData.code" placeholder="请输入学科代码" />
        </FormItem>
        <FormItem label="是否启用" prop="isActive">
          <Switch v-model="formData.isActive" />
        </FormItem>
      </Form>
    </Modal>

    <!-- 删除确认模态框 -->
    <Modal v-model="showDeleteModal" title="确认删除" @on-ok="confirmDelete">
      <p>确定要删除学科 "{{ subjectToDelete.name }}" 吗？此操作不可恢复。</p>
    </Modal>
  </div>
</template>

<script>
import { getAdminSubjects, addAdminSubject, updateAdminSubject, deleteAdminSubject } from '@/api'

export default {
  name: 'AdminSubjects',
  data() {
    return {
      loading: false,
      searchKeyword: '',
      subjects: [],
      columns: [
        { title: 'ID', key: 'id', width: 80 },
        { title: '学科名称', key: 'name', minWidth: 150 },
        { title: '学科代码', key: 'code', width: 120 },
        { title: '学科描述', key: 'description', minWidth: 200 },
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
        { title: '操作', slot: 'action', width: 150, fixed: 'right' }
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
        name: '',
        description: '',
        code: '',
        isActive: true
      },
      formRules: {
        name: [
          { required: true, message: '请输入学科名称', trigger: 'blur' }
        ],
        code: [
          { required: true, message: '请输入学科代码', trigger: 'blur' }
        ]
      },
      showDeleteModal: false,
      subjectToDelete: {}
    }
  },
  mounted() {
    this.loadSubjects()
  },
  methods: {
    async loadSubjects() {
      this.loading = true
      try {
        const response = await getAdminSubjects({
          page: this.pagination.current,
          pageSize: this.pagination.pageSize,
          keyword: this.searchKeyword
        })
        if (response.code === 0) {
          this.subjects = response.data.list
          this.pagination.total = response.data.total
        } else {
          this.$Message.error(response.msg || '加载学科列表失败')
        }
      } catch (error) {
        console.error('加载学科列表失败:', error)
        this.$Message.error('加载学科列表失败')
      } finally {
        this.loading = false
      }
    },

    handleSearch() {
      this.pagination.current = 1
      this.loadSubjects()
    },

    resetSearch() {
      this.searchKeyword = ''
      this.pagination.current = 1
      this.loadSubjects()
    },

    handlePageChange(page) {
      this.pagination.current = page
      this.loadSubjects()
    },

    handlePageSizeChange(pageSize) {
      this.pagination.pageSize = pageSize
      this.pagination.current = 1
      this.loadSubjects()
    },

    showAddModal() {
      this.isEdit = false
      this.formData = {
        name: '',
        description: '',
        code: '',
        isActive: true
      }
      this.showModal = true
    },

    editSubject(subject) {
      this.isEdit = true
      this.formData = { ...subject }
      this.showModal = true
    },

    async handleSubmit() {
      try {
        const valid = await this.$refs.formRef.validate()
        if (!valid) return

        let response
        if (this.isEdit) {
          response = await updateAdminSubject(this.formData)
        } else {
          response = await addAdminSubject(this.formData)
        }

        if (response.code === 0) {
          this.$Message.success(this.isEdit ? '编辑成功' : '创建成功')
          this.showModal = false
          this.loadSubjects()
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

    deleteSubject(subject) {
      this.subjectToDelete = subject
      this.showDeleteModal = true
    },

    async confirmDelete() {
      try {
        const response = await deleteAdminSubject(this.subjectToDelete.id)
        if (response.code === 0) {
          this.$Message.success('删除成功')
          this.loadSubjects()
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
.admin-subjects {
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

.search-section .ivu-input {
  margin-right: 16px;
}
</style>
