<template>
  <div class="fater-body-show">
    <div class="page-header animate-fade-in-up">
      <div class="header-content">
        <Icon type="ios-analytics" class="header-icon" />
        <div class="header-text">
          <h2>数据可视化</h2>
          <p>查看您的学习数据统计和分析</p>
        </div>
      </div>
    </div>

    <Row :gutter="24" class="charts-row">
      <Col span="24">
        <StudentProgressChart />
      </Col>
    </Row>

    <Row :gutter="24" class="charts-row">
      <Col span="24">
        <ScoreTrendChart />
      </Col>
    </Row>

    <Row :gutter="24" class="charts-row">
      <Col span="24">
        <WrongQuestionStatsChart />
      </Col>
    </Row>
  </div>
</template>

<script>
import StudentProgressChart from '@/components/StudentProgressChart.vue'
import ScoreTrendChart from '@/components/ScoreTrendChart.vue'
import WrongQuestionStatsChart from '@/components/WrongQuestionStatsChart.vue'

export default {
  name: 'DataVisualization',
  components: {
    StudentProgressChart,
    ScoreTrendChart,
    WrongQuestionStatsChart
  }
}
</script>

<style scoped>
.fater-body-show {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 30px;
  border-radius: 15px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content {
  display: flex;
  align-items: center;
}

.header-icon {
  font-size: 48px;
  margin-right: 20px;
  opacity: 0.9;
}

.header-text h2 {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 600;
}

.header-text p {
  margin: 0;
  font-size: 16px;
  opacity: 0.9;
}

.charts-row {
  margin-bottom: 24px;
}

.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

