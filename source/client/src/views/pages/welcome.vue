<template>
	<div class="fater-body-show">
        <Row :gutter="20">
            <Col span="8">
                <div class="fater-calendar-panel">
                    <div class="calendar-header">
                        <Icon type="ios-calendar" class="calendar-icon" />
                        <span class="calendar-title">今日日历</span>
                    </div>
                    <Calendar cell-height="40" class="custom-calendar"/>
                </div>
            </Col>
            <Col span="16">
                <Card style="margin-top:16px;">
                    <template #title>
                        <div class="card-title">
                            <Icon type="ios-stats" class="title-icon" />
                            <span>系统概览</span>
                        </div>
                    </template>
                    <Row :gutter="12">
                        <Col span="4"><div class="stat-card"><div class="stat-value">{{ today.todayNewQuestions }}</div><div class="stat-label">今日新增题目</div></div></Col>
                        <Col span="4"><div class="stat-card"><div class="stat-value">{{ today.todayNewPractices }}</div><div class="stat-label">今日新增练习</div></div></Col>
                        <Col span="4"><div class="stat-card"><div class="stat-value">{{ today.todayNewExams }}</div><div class="stat-label">今日新增考试</div></div></Col>
                        <Col span="4"><div class="stat-card"><div class="stat-value">{{ trend.activeUsers7d }}</div><div class="stat-label">近7天活跃用户</div></div></Col>
                        <Col span="4"><div class="stat-card"><div class="stat-value">{{ trend.passRate7d }}%</div><div class="stat-label">近7天通过率</div></div></Col>
                        <Col span="4"><div class="stat-card"><div class="stat-value">{{ trend.avgScore7d }}</div><div class="stat-label">近7天平均分</div></div></Col>
                    </Row>
                    <Row :gutter="12" style="margin-top:12px;">
                        <Col span="4"><div class="stat-card warn"><div class="stat-value">{{ review.pendingReviews }}</div><div class="stat-label">待人工覆核数</div></div></Col>
                    </Row>
                </Card>
            </Col>
        </Row>

        <Card style="margin-top:16px;">
            <template #title>
                <div class="card-title">
                    <Icon type="ios-trending-up" class="title-icon" />
                    <span>趋势图表</span>
                </div>
            </template>
            <Row :gutter="12">
                <Col span="12">
                    <div style="height:300px;" ref="chartQuestions"></div>
                </Col>
                <Col span="12">
                    <div style="height:300px;" ref="chartActive"></div>
                </Col>
            </Row>
            <Row :gutter="12" style="margin-top:12px;">
                <Col span="24">
                    <div style="height:300px;" ref="chartDone"></div>
                </Col>
            </Row>
        </Card>

        
    </div>
</template>

<style>
.fater-body-show {
	padding: 20px;
}

.calendar-header {
	display: flex;
	align-items: center;
	gap: 10px;
	margin-bottom: 15px;
	padding-bottom: 10px;
	border-bottom: 2px solid #f0f0f0;
}

.calendar-icon {
	font-size: 20px;
	color: #667eea;
}

.calendar-title {
	font-size: 16px;
	font-weight: 600;
	color: #333;
}

.custom-calendar {
	border-radius: 8px;
	overflow: hidden;
}

.system-info-card {
	border-radius: 12px;
	box-shadow: 0 4px 20px rgba(0,0,0,0.08);
	border: none;
}

.card-title {
	display: flex;
	align-items: center;
	gap: 8px;
	font-size: 16px;
	font-weight: 600;
	color: #333;
}

.title-icon {
	font-size: 18px;
	color: #667eea;
}

.info-icon {
	font-size: 16px;
	color: #667eea;
	margin-right: 8px;
}

.welcome-content {
	position: relative;
	z-index: 2;
	text-align: center;
	padding: 40px;
}

.welcome-text h1 {
	font-size: 48px;
	font-weight: 300;
	margin-bottom: 10px;
	color: #fff;
	text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.welcome-text h2 {
	font-size: 36px;
	font-weight: 600;
	margin-bottom: 20px;
	color: #fff;
	text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.welcome-text p {
	font-size: 18px;
	color: rgba(255,255,255,0.9);
	margin-bottom: 40px;
	text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

.welcome-features {
	display: flex;
	justify-content: center;
	flex-wrap: wrap;
	gap: 30px;
	margin-top: 40px;
}

.feature-item {
	display: flex;
	align-items: center;
	gap: 10px;
	background: rgba(255,255,255,0.1);
	padding: 15px 25px;
	border-radius: 25px;
	backdrop-filter: blur(10px);
	border: 1px solid rgba(255,255,255,0.2);
	transition: all 0.3s ease;
}

.feature-item:hover {
	background: rgba(255,255,255,0.2);
	transform: translateY(-2px);
	box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}

.feature-icon {
	font-size: 20px;
	color: #fff;
}

.feature-item span {
	color: #fff;
	font-weight: 500;
	font-size: 14px;
}

.voice-section {
	margin-top: 30px;
}

/* 响应式设计 */
@media (max-width: 768px) {
	.fater-body-show {
		padding: 15px;
	}
	
	.welcome-text h1 {
		font-size: 32px;
	}
	
	.welcome-text h2 {
		font-size: 24px;
	}
	
	.welcome-text p {
		font-size: 16px;
	}
	
	.welcome-features {
		gap: 15px;
	}
	
	.feature-item {
		padding: 12px 20px;
	}
}
</style>

<script>
import * as echarts from 'echarts/core'
import { BarChart, LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
echarts.use([BarChart, LineChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

export default{
    data(){
        return {
            today: { todayNewQuestions: 0, todayNewPractices: 0, todayNewExams: 0 },
            trend: { activeUsers7d: 0, passRate7d: 0, avgScore7d: 0 },
            review: { pendingReviews: 0 }

        }
    },
    methods:{
        async loadDashboard(){
            try{
                const api = await import('../../utils/http.js')
                const resp = await api.default.get('/admin/dashboard_cards/')
                if(resp.code === 0){
                    const d = resp.data || {}
                    this.today = { todayNewQuestions: d.todayNewQuestions || 0, todayNewPractices: d.todayNewPractices || 0, todayNewExams: d.todayNewExams || 0 }
                    this.trend = { activeUsers7d: d.activeUsers7d || 0, passRate7d: d.passRate7d || 0, avgScore7d: d.avgScore7d || 0 }
                    this.review = { pendingReviews: d.pendingReviews || 0 }
                }
            }catch(e){
                // ignore
            }
        }
        ,
        async loadTrends(){
            try{
                const api = await import('../../utils/http.js')
                const resp = await api.default.get('/admin/trends/')
                if(resp.code === 0){
                    const d = resp.data || {}
                    // 题目月度新增（柱状）
                    const chartQuestions = echarts.init(this.$refs.chartQuestions)
                    chartQuestions.setOption({
                        tooltip: { trigger: 'axis' },
                        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
                        xAxis: { type: 'category', data: d.months || [] },
                        yAxis: { type: 'value' },
                        series: [{ name: '题目数', type: 'bar', data: d.questionsByMonth || [], barWidth: '50%' }]
                    })
                    // 活跃用户（折线）
                    const chartActive = echarts.init(this.$refs.chartActive)
                    chartActive.setOption({
                        tooltip: { trigger: 'axis' },
                        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
                        xAxis: { type: 'category', data: d.days || [], boundaryGap: false },
                        yAxis: { type: 'value' },
                        series: [{ name: '活跃用户', type: 'line', smooth: true, data: d.activeUsersDaily || [] }]
                    })
                    // 练习/任务完成（堆叠柱状）
                    const chartDone = echarts.init(this.$refs.chartDone)
                    chartDone.setOption({
                        tooltip: { trigger: 'axis' },
                        legend: { data: ['练习完成', '任务完成'] },
                        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
                        xAxis: { type: 'category', data: d.days || [] },
                        yAxis: { type: 'value' },
                        series: [
                            { name: '练习完成', type: 'bar', stack: 'total', data: d.practiceDoneDaily || [] },
                            { name: '任务完成', type: 'bar', stack: 'total', data: d.taskDoneDaily || [] }
                        ]
                    })
                }
            }catch(e){
                // ignore
            }
        }
    },
    mounted(){
        this.loadDashboard()
        this.$nextTick(() => this.loadTrends())
    }
}
</script>