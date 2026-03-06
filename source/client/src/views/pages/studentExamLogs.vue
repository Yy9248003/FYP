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
						<Tag v-else-if="row.status == 1"
                                type="border" color="blue">等待审核</Tag>
                        <span v-else>{{ row.score }}</span>
					</template>
				</Table>
				<Page style="margin-top: 15px;" v-if="pageTotal > 1" :current="pageIndex"
					@on-change="handleCurrentChange" :total="totalInfo" show-total/>
			</div>
		</Card>
    </div>
</template>

<style>
</style>

<script>
import {
    getPageStudentExamLogs,
    getLoginUser,
    getAllProjects,
} from '../../api/index.js';
export default{
		
    data(){
        return {
            projects: [],
            userInfo: {},
            pageInfos: [],
            pageInfos: [],
            pageIndex: 1,
            pageSize: 10,
            pageTotal: 0,
            totalInfo: 0,
            loading: true,
            qryForm: {
                examName: "",
                studentId: "",
                projectId: "",
            },
            columns: [
                {title: '序号', type: 'index', width: 70, align: 'center'},
                {title: '考试名称', key: 'examName', align: 'center'},
                {title: '考核科目', key: 'projectName', align: 'center'},
                {title: '审核教师', key: 'teacherName', align: 'center'},
                {title: '考试时间', key: 'createTime', align: 'center'},
                {title: '考试结果', slot: 'action', align: 'center'}
            ]
        }
    },
    methods: {

        getPageInfo(pageIndex, pageSize) {
			
            getPageStudentExamLogs(pageIndex, pageSize,
                this.qryForm.examName, this.qryForm.studentId, this.qryForm.projectId).then(resp => {
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
        getLoginUser(this.$store.state.token).then(resp =>{

            this.userInfo = resp.data;
            this.qryForm.studentId = resp.data.id;
            this.getPageInfo(1, this.pageSize);
        });
        
    }
}
</script>