<template>
    <div class="fater-body-show">
        <Card>
            <template #title>
				信息查询
			</template>
			<div>
				<Form :model="qryForm" inline>
					<FormItem>
						<Input type="text" v-model="qryForm.examName" placeholder="考试名称……"></Input>
					</FormItem>
					<FormItem>
						<Select style="width:200px;" v-model="qryForm.gradeId" placeholder="选择班级……">
                            <Option value="">查看全部</Option>
                            <Option v-for="(item, index) in grades" 
                                :key="index" :value="String(item.id)" :label="String(item.name)">{{ item.name }}</Option>
                        </Select>
					</FormItem>
					<FormItem>
						<Select style="width:200px;" v-model="qryForm.projectId" placeholder="选择科目……">
                            <Option value="">查看全部</Option>
                            <Option v-for="(item, index) in projects" 
                                :key="index" :value="String(item.id)" :label="String(item.name)">{{ item.name }}</Option>
                        </Select>
					</FormItem>
					<FormItem>
						<Button type="primary" @click="getPageInfo()">
							<Icon type="ios-search" />
						</Button>
					</FormItem>
				</Form>
			</div>
		</Card>

        <Card>
			<div>
				<Table border :columns="columns" :loading="loading" :data="pageInfos">
					<template #action="{ row }">
                        <Tag v-if="row.status == 0" type="border" color="primary">考试中</Tag>
						<Button v-else-if="row.status == 1"
                                size="small" type="warning" @click="putScore(row)">公布成绩</Button>
                        <span v-else>处理完毕(得分{{ row.score }})</span>
					</template>
					<template #action1="{ row }">
						<Button v-if="row.status == 1"
                                size="small" type="success" @click="showAuditWin_1(row)">审核</Button>
                        <Button v-else
                                size="small" type="info" disabled>审核</Button>
					</template>
					<template #action2="{ row }">
						<Button v-if="row.status == 1"
                                size="small" type="success" @click="showAuditWin_2(row)">审核</Button>
                        <Button v-else
                                size="small" type="info" disabled>审核</Button>
					</template>
				</Table>
				<Page style="margin-top: 15px;" v-if="pageTotal > 1" :current="pageIndex"
					@on-change="handleCurrentChange" :total="totalInfo" show-total/>
			</div>
		</Card>

        <Modal fullscreen="true" v-model="showAuditFlag_1" footer-hide="true" title="填空题审核">
            <Table border :columns="pracCols1" :data="ansers_1">
                <template #action="{ row }">
                    <Button v-if="row.status==0" size="small" style="margin-right: 5px;"
                                    type="success" @click="auditLog(row.id, 1, 0)">正确</Button>
                    <Button v-if="row.status==1" size="small" disabled
                             style="margin-right: 5px;" type="success">正确</Button>
                    <Button v-if="row.status==0" size="small" type="error" @click="auditLog(row.id, 1, 1)">错误</Button>
                    <Button v-if="row.status==1" size="small" type="error" disabled>错误</Button>
                </template>
                <template #score="{ row }">
                    <Tag v-if="row.status==0" type="border" color="green">待审</Tag>
                    <span v-if="row.status==1" >{{ row.score }}</span>
                </template>
                <template #action1="{ row }">
                    <span v-if="row.answer">{{ row.answer }}</span>
                    <span v-else>未作答</span>
                </template>
            </Table>
        </Modal>
        
        <Modal fullscreen="true" v-model="showAuditFlag_2" footer-hide="true" title="编程题审核">
            <Table border :columns="pracCols2" :data="ansers_2">
                <template #practiseAnswer="{ row }">
                    <Input v-model="row.practiseAnswer" type="textarea" :rows="6" :border="false"/>    
                </template>
                <template #answer="{ row }">
                    <Input v-if="row.answer" v-model="row.answer" type="textarea" :rows="6" :border="false"/>   
                    <span v-else>未作答</span> 
                </template>
                <template #score="{ row }">
                    <Tag v-if="row.status==0" type="border" color="green">待审</Tag>
                    <span v-if="row.status==1" >{{ row.score }}</span>
                </template>
                <template #action="{ row }">
                    <Button v-if="row.status==0" size="small" style="margin-right: 5px;"
                                    type="success" @click="auditLog(row.id, 3, 0)">正确</Button>
                    <Button v-if="row.status==1" size="small" disabled
                             style="margin-right: 5px;" type="success">正确</Button>
                    <Button v-if="row.status==0" size="small" type="error" @click="auditLog(row.id, 3, 1)">错误</Button>
                    <Button v-if="row.status==1" size="small" type="error" disabled>错误</Button>
                </template>                
            </Table>
        </Modal>
    </div>
</template>

<style>
/* 提升表头与单元格可读性 */
.ivu-table th, .ivu-table td {
    color: #333;
}
.ivu-table th {
    background-color: #f6f7fb;
    font-weight: 600;
}
/* 审核弹窗中的表格字体颜色 */
.ivu-modal .ivu-table th, .ivu-modal .ivu-table td {
    color: #333;
}
/* 输入框里的文字颜色、自动换行 */
.ivu-input, .ivu-input textarea {
    color: #333 !important;
}
.ivu-table .ivu-table-cell {
    white-space: normal;
    line-height: 1.6;
}
/* 空数据提示颜色更清晰 */
.ivu-table-tip {
    color: #666;
}
</style>

<script>
import {
    getPageTeacherExamLogs,
    getLoginUser,
    getAllProjects,
    getAllGrades,
    getAnswers,
    checkAnswers,
    aduitAnswerLog,
    putExamLog
} from '../../api/index.js';
export default{
		
    data(){
        return {
            grades: [],
            projects: [],
            userInfo: {},
            pageInfos: [],
            ansers_1: [],
            ansers_2: [],
            showAuditFlag_1: false,
            showAuditFlag_2: false,
            pageInfos: [],
            pageIndex: 1,
            pageSize: 10,
            pageTotal: 0,
            totalInfo: 0,
            loading: true,
            qryForm: {
                examName: "",
                token: this.$store.state.token,
                gradeId: "",
                projectId: "",
            },
            answersForm: {
                studentId: "",
                type: "",
                examId: "",
                flag: "",
                score: ""
            },
            columns: [
                {title: '序号', type: 'index', width: 70, align: 'center'},
                {title: '考试名称', key: 'examName', align: 'center'},
                {title: '考试班级', key: 'gradeName', align: 'center'},
                {title: '考核科目', key: 'projectName', align: 'center'},
                {title: '参考学生', key: 'studentName', align: 'center'},
                {title: '填空审核', slot: 'action1', width: 150, align: 'center'},
                {title: '编程审核', slot: 'action2', width: 150, align: 'center'},
                {title: '操作', slot: 'action', align: 'center'}
            ],
            pracCols1: [
                {title: '序号', type: 'index', width: 70, align: 'center'},
                {title: '考试题目', key: 'practiseName', width: 620, align: 'left'},
                {title: '参考答案', key: 'practiseAnswer', align: 'left'},
                {title: '考生提交', slot: 'action1', align: 'left'},
                {title: '审核结果', slot: 'score', width: 120, align: 'center'},
                {title: '操作', slot: 'action', width: 300, align: 'center'}
            ],
            pracCols2: [
                {title: '序号', type: 'index', width: 70, align: 'center'},
                {title: '考试题目', key: 'practiseName', width: 580, align: 'left'},
                {title: '参考答案', slot: 'practiseAnswer', align: 'left'},
                {title: '考生提交', slot: 'answer', align: 'left'},
                {title: '审核结果', slot: 'score', width: 120, align: 'center'},
                {title: '操作', slot: 'action', width: 180, align: 'center'}
            ]
        }
    },
    methods: {

        showAuditWin_1(row){

            this.answersForm = {
                studentId: row.studentId,
                type: 1,
                examId: row.examId,
            }
            getAnswers(row.studentId, 
                    1, row.examId).then(resp =>{
                
                this.ansers_1 = resp.data;
                this.showAuditFlag_1 = true;
            });
        },
        showAuditWin_2(row){

            this.answersForm = {
                studentId: row.studentId,
                type: 3,
                examId: row.examId,
            }
            getAnswers(row.studentId, 
                    3, row.examId).then(resp =>{
                
                this.ansers_2 = resp.data;
                this.showAuditFlag_2 = true;
            });
        },
        putScore(row){

            checkAnswers(row.studentId, row.examId).then(resp =>{
                
                if(resp.data.flag){

                    this.$Notice.warning({
                        duration: 3,
                        title: "系统提示",
                        desc: "填空或者编程类型题目未完全审核，不能发布成绩"
                    });
                }else{
                    this.$Modal.confirm({
                        title: '系统提示',
                        content: '成绩发布之后, 结果将无法修改, 是否继续?',
                        onOk: () => {

                            putExamLog({
                                studentId: row.studentId,
                                examId: row.examId
                            }).then(res =>{

                                this.getPageInfo(1, this.pageSize);
                                this.$Notice.success({
                                    duration: 3,
                                    title: "发布成绩成功"
                                });
                            });
                        }
                    });
                }
            })
             
        },
        auditLog(id, type, flag){

             this.$Modal.confirm({
                title: '系统提示',
                content: '提交之后, 结果将无法修改, 是否继续?',
                onOk: () => {
                    aduitAnswerLog({
                        id: id,
                        type: type,
                        flag: flag
                    }).then(resp =>{

                        getAnswers(this.answersForm.studentId, 
                                this.answersForm.type, 
                                this.answersForm.examId).then(resp =>{
                            
                            if(type == 1){

                                this.ansers_1 = resp.data;
                            }else{

                                this.ansers_2 = resp.data;
                            }
                        });
                        this.$Notice.success({
                            duration: 3,
                            title: resp.msg
                        });
                    });
                },
            });
        },
        getPageInfo(pageIndex, pageSize) {
			
            getPageTeacherExamLogs(pageIndex, pageSize,
                this.qryForm.examName, this.qryForm.token,
                this.qryForm.gradeId, this.qryForm.projectId).then(resp => {
                const page = resp.data || {};
                this.pageInfos = page.data || [];
                this.pageIndex = page.pageIndex || 1;
                this.pageSize = page.pageSize || 10;
                this.pageTotal = page.pageTotal || 0;
                this.totalInfo = page.count || (this.pageInfos.length);
                this.loading = false;
            }).catch(() => {
                this.pageInfos = [];
                this.loading = false;
            });
        },
        handleCurrentChange(pageIndex) {
        
            this.getPageInfo(pageIndex, this.pageSize);
        },
    },
    mounted(){
        
        getAllProjects().then(resp =>{

            this.projects = resp.data;
        });
        getAllGrades().then(resp =>{

            this.grades = resp.data;
        });
        getLoginUser(this.$store.state.token).then(resp =>{

            this.userInfo = resp.data;
        });
        this.getPageInfo(1, this.pageSize);
    }
}
</script>