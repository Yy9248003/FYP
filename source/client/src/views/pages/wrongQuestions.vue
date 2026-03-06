<template>
  <div class="wrong-questions-container">
    <div class="page-header">
      <h2>错题本</h2>
      <div class="header-actions">
        <Input
          v-model="searchKeyword"
          placeholder="搜索题目或学科"
          style="width: 180px"
          @on-enter="handleSearch"
        />
        <Select
          v-model="filterProjectId"
          placeholder="学科"
          style="width: 140px"
          clearable
        >
          <Option v-for="p in projects" :key="p.id" :value="p.id">
            {{ p.name }}
          </Option>
        </Select>
        <Select
          v-model="filterType"
          placeholder="题型"
          style="width: 120px"
          clearable
        >
          <Option value="0">选择题</Option>
          <Option value="1">填空题</Option>
          <Option value="2">判断题</Option>
          <Option value="3">编程题</Option>
        </Select>
        <Select
          v-model="filterReviewStatus"
          placeholder="复习状态"
          style="width: 120px"
          clearable
        >
          <Option value="reviewed">已复习</Option>
          <Option value="unreviewed">待复习</Option>
        </Select>
        <DatePicker
          v-model="filterDateRange"
          type="daterange"
          placeholder="时间范围"
          style="width: 220px"
          format="yyyy-MM-dd"
        />
        <Button type="primary" @click="handleSearch">搜索</Button>
        <Button @click="handleReset">重置</Button>
        <Button type="success" @click="goToWrongPractice">
          基于错题生成练习
        </Button>
      </div>
    </div>

    <div class="content-area">
      <div class="stats-cards">
        <Card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ totalCount }}</div>
            <div class="stat-label">总错题数</div>
          </div>
        </Card>
        <Card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ reviewedCount }}</div>
            <div class="stat-label">已复习</div>
          </div>
        </Card>
        <Card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ unreviewedCount }}</div>
            <div class="stat-label">待复习</div>
          </div>
        </Card>
      </div>

      <Card class="wrong-questions-list">
        <div slot="title">
          <span>错题列表</span>
          <Tag v-if="filteredList.length > 0" color="blue">{{ filteredList.length }}题</Tag>
        </div>
        
        <div v-if="loading" class="loading-container">
          <Spin size="large">
            <Icon type="ios-loading" size="18" class="spin-icon-load"></Icon>
            <div class="spin-text">加载中...</div>
          </Spin>
        </div>

        <div v-else-if="filteredList.length === 0" class="empty-container">
          <Icon type="ios-document-outline" size="48" color="#ccc" />
          <p>暂无错题记录</p>
        </div>

        <div v-else class="questions-container">
          <div
            v-for="question in filteredList"
            :key="question.id"
            class="question-item"
            :class="{ 'reviewed': question.isReviewed }"
          >
            <div class="question-header">
              <div class="question-title">
                <span class="question-type">{{ getQuestionTypeName(question.type) }}</span>
                <span class="question-text">{{ question.title }}</span>
              </div>
              <div class="question-actions">
                <Button
                  size="small"
                  type="primary"
                  @click="handleReview(question)"
                >
                  复习
                </Button>
                <Button
                  size="small"
                  @click="handleViewDetail(question)"
                >
                  详情
                </Button>
                <Button
                  size="small"
                  type="error"
                  @click="handleDelete(question)"
                >
                  删除
                </Button>
              </div>
            </div>
            
            <div class="question-info">
              <Tag color="green">{{ question.project }}</Tag>
              <Tag v-if="question.isReviewed" color="blue">已复习</Tag>
              <Tag v-else color="orange">待复习</Tag>
              <span class="review-count">复习{{ question.reviewCount }}次</span>
              <span class="create-time">{{ question.createTime }}</span>
            </div>
          </div>
        </div>

        <div v-if="total > pageSize" class="pagination-container">
          <Page
            :total="total"
            :current="currentPage"
            :page-size="pageSize"
            show-total
            show-elevator
            @on-change="handlePageChange"
          />
        </div>
      </Card>
    </div>

    <!-- 复习弹窗 -->
    <Modal
      v-model="reviewModalVisible"
      title="错题复习"
      width="800px"
      :mask-closable="false"
    >
      <div v-if="currentQuestion" class="review-content">
        <div class="question-display">
          <h3>{{ currentQuestion.title }}</h3>
          <div class="question-type-tag">
            <Tag>{{ getQuestionTypeName(currentQuestion.type) }}</Tag>
          </div>
          
          <div v-if="currentQuestion.type === 0" class="options-list">
            <RadioGroup v-model="reviewAnswer" :disabled="reviewSubmitted">
              <div
                v-for="(option, idx) in currentQuestion.options"
                :key="'opt-' + (currentQuestion && currentQuestion.id) + '-' + idx"
                class="option-item"
              >
                <Radio :label="String.fromCharCode(65 + idx)">
                  {{ String.fromCharCode(65 + idx) }}. {{ option.name }}
                </Radio>
              </div>
            </RadioGroup>
          </div>
          
          <div v-else-if="currentQuestion.type === 1" class="fill-blank">
            <Input
              v-model="reviewAnswer"
              type="textarea"
              placeholder="请输入答案"
              :disabled="reviewSubmitted"
              :rows="3"
            />
          </div>
          
          <div v-else-if="currentQuestion.type === 2" class="judgment">
            <RadioGroup v-model="reviewAnswer" :disabled="reviewSubmitted">
              <Radio label="true">正确</Radio>
              <Radio label="false">错误</Radio>
            </RadioGroup>
          </div>
          
          <div v-else-if="currentQuestion.type === 3" class="programming">
            <Input
              v-model="reviewAnswer"
              type="textarea"
              placeholder="请输入代码答案"
              :disabled="reviewSubmitted"
              :rows="6"
            />
          </div>
        </div>
        
        <div class="answer-analysis">
          <Divider>参考答案</Divider>
          <div class="correct-answer">
            <strong>正确答案：</strong>{{ currentQuestion.correctAnswer }}
          </div>
          <div class="analysis">
            <strong>题目分析：</strong>{{ currentQuestion.analysis }}
          </div>
        </div>
        
        <div class="review-notes">
          <Input
            v-model="reviewNotes"
            type="textarea"
            placeholder="复习笔记（可选）"
            :disabled="reviewSubmitted"
            :rows="3"
          />
        </div>
      </div>
      
      <div slot="footer">
        <Button @click="reviewModalVisible = false">取消</Button>
        <Button
          type="primary"
          :disabled="!reviewAnswer || reviewSubmitted"
          @click="submitReview"
        >
          提交复习
        </Button>
      </div>
    </Modal>

    <!-- 详情弹窗 -->
    <Modal
      v-model="detailModalVisible"
      title="错题详情"
      width="900px"
    >
      <div v-if="currentQuestion" class="detail-content">
        <div class="question-detail">
          <h3>{{ currentQuestion.title }}</h3>
          <div class="detail-info">
            <Tag>{{ getQuestionTypeName(currentQuestion.type) }}</Tag>
            <Tag color="green">{{ currentQuestion.project }}</Tag>
            <span class="create-time">创建时间：{{ currentQuestion.createTime }}</span>
          </div>
          
          <div class="answer-details">
            <div class="answer-item">
              <strong>你的答案：</strong>
              <span class="wrong-answer">{{ currentQuestion.wrongAnswer }}</span>
            </div>
            <div class="answer-item">
              <strong>正确答案：</strong>
              <span class="correct-answer">{{ currentQuestion.correctAnswer }}</span>
            </div>
          </div>
          
          <div class="analysis-detail">
            <strong>题目分析：</strong>
            <p>{{ currentQuestion.analysis }}</p>
          </div>

          <div class="analysis-detail">
            <Divider>AI 错因分析</Divider>
            <div v-if="aiLoading">
              <Spin size="small" />
              <span style="margin-left: 8px;">AI 正在分析这道错题，请稍候...</span>
            </div>
            <div v-else-if="aiAnalysis">
              <p>{{ aiAnalysis }}</p>
            </div>
            <div v-else>
              <Button type="primary" @click="generateAIAnalysis">
                使用 AI 分析这道错题
              </Button>
            </div>
          </div>
        </div>
        
        <Divider>复习历史</Divider>
        <div class="review-history">
          <div
            v-for="review in reviewHistory"
            :key="review.id"
            class="review-item"
          >
            <div class="review-header">
              <span class="review-time">{{ review.reviewTime }}</span>
              <Tag :color="review.isCorrect ? 'success' : 'error'">
                {{ review.isCorrect ? '正确' : '错误' }}
              </Tag>
            </div>
            <div class="review-answer">
              <strong>复习答案：</strong>{{ review.reviewAnswer }}
            </div>
            <div v-if="review.notes" class="review-notes">
              <strong>笔记：</strong>{{ review.notes }}
            </div>
          </div>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script>
import {
  getPageWrongQuestions,
  getWrongQuestionDetail,
  getReviewHistory,
  addReview,
  markAsReviewed,
  deleteWrongQuestion
} from '@/api/index.js'

export default {
  name: 'WrongQuestions',
  data() {
    return {
      loading: false,
      searchKeyword: '',
      // 筛选条件
      filterProjectId: '',
      filterType: '',
      filterReviewStatus: '',
      filterDateRange: [],
      currentPage: 1,
      pageSize: 10,
      total: 0,
      wrongQuestionsList: [],
      filteredList: [],
      projects: [],
      
      // 复习弹窗
      reviewModalVisible: false,
      currentQuestion: null,
      reviewAnswer: '',
      reviewNotes: '',
      reviewSubmitted: false,
      
      // 详情弹窗
      detailModalVisible: false,
      reviewHistory: [],
      // AI 错题分析
      aiLoading: false,
      aiAnalysis: '',
      // 基于错题练习相关
      generatingPractice: false
    }
  },
  
  computed: {
    totalCount() {
      return this.wrongQuestionsList.length
    },
    reviewedCount() {
      return this.wrongQuestionsList.filter(q => q.isReviewed).length
    },
    unreviewedCount() {
      return this.wrongQuestionsList.filter(q => !q.isReviewed).length
    }
  },
  
  mounted() {
    this.loadProjects()
    this.loadWrongQuestions()
  },
  
  methods: {
    async loadProjects() {
      try {
        const { getAllProjects } = await import('@/api/index.js')
        const res = await getAllProjects()
        if (res.code === 0) {
          this.projects = res.data || res || []
        }
      } catch (e) {
        // 忽略项目加载失败，不影响错题本使用
      }
    },

    async loadWrongQuestions() {
      try {
        this.loading = true
        const token = this.$store.state.token || sessionStorage.getItem('token')
        const { getPageWrongQuestions } = await import('@/api/index.js')
        const filters = {
          projectId: this.filterProjectId || '',
          type: this.filterType,
          reviewStatus: this.filterReviewStatus,
          startDate: this.filterDateRange[0] || '',
          endDate: this.filterDateRange[1] || ''
        }
        const response = await getPageWrongQuestions(
          this.currentPage,
          this.pageSize,
          '', // studentId 通过 token 自动识别
          this.searchKeyword,
          filters
        )
        
        if (response.code === 0) {
          const list = response.data.list || response.data || []
          const total = response.data.total || list.length || 0
          this.wrongQuestionsList = list
          this.filteredList = list
          this.total = total
        } else {
          this.$Message.error(response.msg || '加载错题失败')
        }
      } catch (error) {
        console.error('加载错题失败:', error)
        this.$Message.error('加载错题失败')
      } finally {
        this.loading = false
      }
    },
    
    handleSearch() {
      this.currentPage = 1
      this.loadWrongQuestions()
    },
    
    handleReset() {
      this.searchKeyword = ''
      this.filterProjectId = ''
      this.filterType = ''
      this.filterReviewStatus = ''
      this.filterDateRange = []
      this.currentPage = 1
      this.loadWrongQuestions()
    },
    
    handlePageChange(page) {
      this.currentPage = page
      this.loadWrongQuestions()
    },
    
    async handleReview(question) {
      try {
        this.currentQuestion = question
        this.aiAnalysis = ''
        this.reviewAnswer = ''
        this.reviewNotes = ''
        this.reviewSubmitted = false
        
        // 获取题目详情
        const response = await getWrongQuestionDetail(question.id)
        if (response.code === 0) {
          this.currentQuestion = response.data
        }
        
        this.reviewModalVisible = true
      } catch (error) {
        console.error('获取题目详情失败:', error)
        this.$Message.error('获取题目详情失败')
      }
    },
    
    async submitReview() {
      if (!this.reviewAnswer) {
        this.$Message.warning('请先输入答案')
        return
      }
      
      try {
        this.reviewSubmitted = true
        
        const params = {
          wrongQuestionId: this.currentQuestion.id,
          reviewAnswer: this.reviewAnswer,
          isCorrect: this.checkAnswer(),
          notes: this.reviewNotes
        }
        
        const response = await addReview(params)
        if (response.code === 0) {
          if (params.isCorrect) {
            this.$Message.success('复习正确，已标记为已复习')
            try {
              await markAsReviewed(this.currentQuestion.id)
              this.currentQuestion.isReviewed = true
              this.currentQuestion.reviewCount = (this.currentQuestion.reviewCount || 0) + 1
              const idx = this.wrongQuestionsList.findIndex(q => q.id === this.currentQuestion.id)
              if (idx !== -1) {
                this.wrongQuestionsList[idx].isReviewed = true
                this.wrongQuestionsList[idx].reviewCount = (this.wrongQuestionsList[idx].reviewCount || 0) + 1
              }
              const fidx = this.filteredList.findIndex(q => q.id === this.currentQuestion.id)
              if (fidx !== -1) {
                this.filteredList[fidx].isReviewed = true
                this.filteredList[fidx].reviewCount = (this.filteredList[fidx].reviewCount || 0) + 1
              }
            } catch (e) {}
          } else {
            this.$Message.warning('答案不正确，已记录复习，请继续练习')
          }
          // 刷新列表
          this.loadWrongQuestions()
          this.reviewModalVisible = false
        } else {
          this.$Message.error(response.msg || '复习提交失败')
        }
      } catch (error) {
        console.error('复习提交失败:', error)
        this.$Message.error('复习提交失败')
      } finally {
        this.reviewSubmitted = false
      }
    },
    
    checkAnswer() {
      if (!this.currentQuestion || this.reviewAnswer === undefined || this.reviewAnswer === null) return false
      const correctAnswerRaw = (this.currentQuestion.correctAnswer || '').toString().trim()
      const reviewAnswerRaw = (this.reviewAnswer || '').toString().trim()
      const type = this.currentQuestion.type

      const extractLetter = (s) => {
        if (!s) return ''
        const u = s.toString().trim().toUpperCase()
        let m = u.match(/^[A-D]$/)
        if (m) return m[0]
        m = u.match(/选项([A-D])/)
        if (m) return m[1]
        m = u.match(/^([A-D])[\\.．、，\s]/)
        if (m) return m[1]
        return u
      }
      const toBool = (s) => {
        const v = (s || '').toString().trim().toLowerCase()
        if (['true', 't', '1', 'y', 'yes', '是', '对', '正确'].includes(v)) return true
        if (['false', 'f', '0', 'n', 'no', '否', '错', '错误'].includes(v)) return false
        return v === 'true'
      }

      switch (type) {
        case 0: {
          // 选择题：兼容 “D”、“选项D”、“D. 文本”
          return extractLetter(reviewAnswerRaw) === extractLetter(correctAnswerRaw)
        }
        case 1: {
          // 填空题：忽略大小写与空白
          const norm = (s) => s.replace(/\s+/g, '').toLowerCase()
          return norm(reviewAnswerRaw) === norm(correctAnswerRaw)
        }
        case 2: {
          // 判断题：兼容 true/false、正确/错误
          return toBool(reviewAnswerRaw) === toBool(correctAnswerRaw)
        }
        case 3: {
          // 编程题：简单去首尾空白
          return reviewAnswerRaw.trim() === correctAnswerRaw.trim()
        }
        default:
          return false
      }
    },
    
    async handleViewDetail(question) {
      try {
        this.currentQuestion = question
        this.aiAnalysis = ''
        
        // 获取复习历史
        const response = await getReviewHistory(question.id)
        if (response.code === 0) {
          this.reviewHistory = response.data
        }
        
        this.detailModalVisible = true
      } catch (error) {
        console.error('获取复习历史失败:', error)
        this.$Message.error('获取复习历史失败')
      }
    },
    
    async handleDelete(question) {
      this.$Modal.confirm({
        title: '确认删除',
        content: `确定要删除错题"${question.title}"吗？删除后无法恢复。`,
        onOk: async () => {
          try {
            const response = await deleteWrongQuestion(question.id)
            if (response.code === 0) {
              this.$Message.success('删除成功')
              this.loadWrongQuestions()
            } else {
              this.$Message.error(response.msg || '删除失败')
            }
          } catch (error) {
            console.error('删除失败:', error)
            this.$Message.error('删除失败')
          }
        }
      })
    },
    
    async generateAIAnalysis() {
      if (!this.currentQuestion) return
      try {
        this.aiLoading = true
        const { analyzeWrongAnswer } = await import('@/api/index.js')
        const res = await analyzeWrongAnswer({
          questionContent: this.currentQuestion.title,
          correctAnswer: this.currentQuestion.correctAnswer || '',
          wrongAnswer: this.currentQuestion.wrongAnswer || '',
          questionType: this.currentQuestion.type || 0
        })
        if (res.code === 0) {
          this.aiAnalysis = res.data.analysis || res.data.explanation || 'AI 已返回结果，但未包含详细解析。'
        } else {
          this.$Message.error(res.msg || 'AI 分析失败')
        }
      } catch (e) {
        console.error('AI 分析失败:', e)
        this.$Message.error('AI 分析失败，请稍后重试')
      } finally {
        this.aiLoading = false
      }
    },

    goToWrongPractice() {
      // 跳转到练习试卷页，并打开“错题专项”对话框
      this.$router.push({ name: 'practises', query: { from: 'wrongQuestions', wrongPractice: '1' } });
    },
    
    getQuestionTypeName(type) {
      const typeMap = {
        0: '选择题',
        1: '填空题',
        2: '判断题',
        3: '编程题'
      }
      return typeMap[type] || '未知类型'
    }
  }
}
</script>

<style scoped>
.wrong-questions-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #17233d;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.content-area {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  text-align: center;
}

.stat-content {
  padding: 20px;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #2d8cf0;
  margin-bottom: 8px;
}

.stat-label {
  color: #808695;
  font-size: 14px;
}

.wrong-questions-list {
  min-height: 400px;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.spin-text {
  margin-top: 10px;
  color: #808695;
}

.empty-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 200px;
  color: #808695;
}

.empty-container p {
  margin-top: 10px;
}

.questions-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.question-item {
  border: 1px solid #e8eaec;
  border-radius: 6px;
  padding: 15px;
  transition: all 0.3s ease;
}

.question-item:hover {
  border-color: #2d8cf0;
  box-shadow: 0 2px 8px rgba(45, 140, 240, 0.1);
}

.question-item.reviewed {
  background-color: #f8f9fa;
  border-color: #19be6b;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.question-title {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
}

.question-type {
  background-color: #2d8cf0;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
}

.question-text {
  font-weight: 500;
  color: #17233d;
  line-height: 1.4;
}

.question-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.question-info {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.review-count {
  color: #808695;
  font-size: 12px;
}

.create-time {
  color: #808695;
  font-size: 12px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.review-content {
  max-height: 500px;
  overflow-y: auto;
}

.question-display {
  margin-bottom: 20px;
}

.question-display h3 {
  margin-bottom: 15px;
  color: #17233d;
}

.question-type-tag {
  margin-bottom: 15px;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-item {
  padding: 8px 12px;
  border: 1px solid #e8eaec;
  border-radius: 4px;
}

.fill-blank,
.programming {
  margin: 15px 0;
}

.judgment {
  margin: 15px 0;
}

.answer-analysis {
  margin: 20px 0;
}

.correct-answer,
.analysis {
  margin: 10px 0;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.review-notes {
  margin-top: 20px;
}

.detail-content {
  max-height: 600px;
  overflow-y: auto;
}

.question-detail h3 {
  margin-bottom: 15px;
  color: #17233d;
}

.detail-info {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.answer-details {
  margin: 20px 0;
}

.answer-item {
  margin: 10px 0;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.wrong-answer {
  color: #ed4014;
}

.correct-answer {
  color: #19be6b;
}

.analysis-detail {
  margin: 20px 0;
}

.analysis-detail p {
  margin: 10px 0;
  line-height: 1.6;
}

.review-history {
  max-height: 300px;
  overflow-y: auto;
}

.review-item {
  border: 1px solid #e8eaec;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 10px;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.review-time {
  color: #808695;
  font-size: 12px;
}

.review-answer,
.review-notes {
  margin: 8px 0;
  line-height: 1.4;
}
</style>
