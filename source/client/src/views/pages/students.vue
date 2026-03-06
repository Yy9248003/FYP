<template>
	<div class="fater-body-show">
        <div class="page-header animate-fade-in-up">
            <div class="header-content">
                <Icon type="ios-people" class="header-icon" />
                <div class="header-text">
                    <h2>学生管理</h2>
                    <p>管理系统中的所有学生信息</p>
                </div>
            </div>
            <div class="header-stats">
                <div class="stat-item">
                    <div class="stat-number">{{ totalInfo }}</div>
                    <div class="stat-label">总学生数</div>
                </div>
            </div>
        </div>

        <Card class="search-card animate-fade-in-up delay-100">
            <template #title>
                <div class="card-title">
                    <Icon type="ios-search" class="title-icon" />
                    <span>信息查询</span>
                </div>
            </template>
			<div class="search-form">
				<Form :model="qryForm" inline class="modern-form">
					<FormItem class="form-item">
						<Input 
                            type="text" 
                            v-model="qryForm.name" 
                            placeholder="学生姓名……"
                            class="modern-input"
                            prefix="ios-person">
                        </Input>
					</FormItem>
					<FormItem class="form-item">
                        <Select 
                            style="width:200px;" 
                            v-model="qryForm.gradeId" 
                            placeholder="选择班级……"
                            class="modern-select" transfer>
                            <Option value="">查看全部</Option>
                            <Option v-for="(item, index) in grades" 
                                :key="index" :value="String(item.id)" :label="String(item.name)">{{ item.name }}</Option>
                        </Select>
					</FormItem>
					<FormItem class="form-item">
                        <Select 
                            style="width:200px;" 
                            v-model="qryForm.collegeId" 
                            placeholder="选择学院……"
                            class="modern-select" transfer>
                            <Option value="">查看全部</Option>
                            <Option v-for="(item, index) in colleges" 
                                :key="index" :value="String(item.id)" :label="String(item.name)">{{ item.name }}</Option>
                        </Select>
					</FormItem>
					<FormItem class="form-item">
						<Button 
                            type="primary" 
                            @click="getPageInfo()"
                            class="search-btn btn-ripple">
							<Icon type="ios-search" />
							搜索
						</Button>
					</FormItem>
				</Form>
			</div>
		</Card>

        <Card class="data-card animate-fade-in-up delay-200">
			<template #title>
				<div class="card-title">
                    <Icon type="ios-list" class="title-icon" />
                    <span>学生列表</span>
                    <Button 
                        @click="showAddWin()" 
                        type="primary"
                        class="add-btn btn-ripple">
						<Icon type="md-add" />
						添加学生
					</Button>
                </div>
			</template>
			<div class="table-container">
				<Table 
                    border 
                    :columns="columns" 
                    :loading="loading" 
                    :data="pageInfos"
                    class="modern-table">
					<template #action="{ row }">
						<div class="action-buttons">
                            <Button 
                                size="small" 
                                type="info" 
                                icon="md-create" 
                                @click="showUpdWin(row)"
                                class="action-btn edit-btn">
                                编辑
                            </Button>
							<Button 
                                size="small" 
                                type="warning" 
                                icon="ios-trash" 
                                @click="delInfo(row.id)"
                                class="action-btn delete-btn">
                                删除
                            </Button>
						</div>
					</template>
				</Table>
				<div class="pagination-container">
					<Page 
                        v-if="pageTotal > 1" 
                        :current="pageIndex"
						@on-change="handleCurrentChange" 
                        :total="totalInfo" 
                        show-total
                        class="modern-pagination"/>
				</div>
			</div>
		</Card>

        <Modal 
            width="700" 
            v-model="showAddFlag"
			title="添加学生" 
            ok-text="提交" 
            cancel-text="取消" 
            @on-ok="addInfo()"
            class="modern-modal">
            <Form :label-width="80" :model="studentForm" class="modal-form">
                <FormItem label="学生学号">
                    <Input 
                        v-model="studentForm.id" 
                        placeholder="请输入学生学号..."
                        class="modern-input">
                    </Input>
                </FormItem>
                <Row :gutter="15">
                    <Col span="12">
                        <FormItem label="学生账号">
                            <Input 
                                v-model="studentForm.userName" 
                                placeholder="请输入学生账号..."
                                class="modern-input">
                            </Input>
                        </FormItem>
                    </Col>
                    <Col span="12">
                        <FormItem label="学生姓名">
                            <Input 
                                v-model="studentForm.name" 
                                placeholder="请输入学生姓名..."
                                class="modern-input">
                            </Input>
                        </FormItem>
                    </Col>
                </Row>
                <Row :gutter="15">
                    <Col span="12">
                        <FormItem label="学生性别">
                            <RadioGroup v-model="studentForm.gender" class="gender-group">
                                <Radio label="男" class="gender-radio">男</Radio>
                                <Radio label="女" class="gender-radio">女</Radio>
                            </RadioGroup>
                        </FormItem>
                    </Col>
                    <Col span="12">
                        <FormItem label="学生年龄">
                            <Input 
                                v-model="studentForm.age" 
                                placeholder="请输入学生年龄..."
                                class="modern-input">
                            </Input>
                        </FormItem>
                    </Col>
                </Row>
                <Row :gutter="15">
                    <Col span="12">
                        <FormItem label="所属学院">
                            <Select 
                                v-model="studentForm.collegeId" 
                                placeholder="选择学院……"
                                class="modern-select" transfer>
                                <Option v-for="(item, index) in colleges" 
                                    :key="index" :value="String(item.id)" :label="String(item.name)">{{ item.name }}</Option>
                            </Select>
                        </FormItem>
                    </Col>
                    <Col span="12">
                        <FormItem label="所属班级">
                            <Select 
                                v-model="studentForm.gradeId" 
                                placeholder="选择班级……"
                                class="modern-select" transfer>
                                <Option v-for="(item, index) in grades" 
                                    :key="index" :value="String(item.id)" :label="String(item.name)">{{ item.name }}</Option>
                            </Select>
                        </FormItem>
                    </Col>
                </Row>
            </Form>
		</Modal>

        <Modal 
            v-model="showUpdFlag"
			title="编辑学生信息" 
            ok-text="提交" 
            cancel-text="取消" 
            @on-ok="updInfo()"
            class="modern-modal">
			<Form :label-width="80" :model="studentForm" class="modal-form">
                <FormItem label="所属学院">
                    <Select 
                        v-model="studentForm.collegeId" 
                        placeholder="选择学院……"
                        class="modern-select" transfer>
                        <Option v-for="(item, index) in colleges" 
                            :key="index" :value="String(item.id)" :label="String(item.name)">{{ item.name }}</Option>
                    </Select>
                </FormItem>
                <FormItem label="所属班级">
                    <Select 
                        v-model="studentForm.gradeId" 
                        placeholder="选择班级……"
                        class="modern-select" transfer>
                        <Option v-for="(item, index) in grades" 
                            :key="index" :value="String(item.id)" :label="String(item.name)">{{ item.name }}</Option>
                    </Select>
                </FormItem>
			</Form>
		</Modal>
    </div>
</template>

<style>
.page-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    padding: 30px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #fff;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.header-content {
    display: flex;
    align-items: center;
    gap: 15px;
}

.header-icon {
    font-size: 40px;
    color: #fff;
}

.header-text h2 {
    font-size: 28px;
    font-weight: 600;
    margin: 0 0 5px 0;
}

.header-text p {
    font-size: 14px;
    opacity: 0.9;
    margin: 0;
}

.header-stats {
    display: flex;
    gap: 20px;
}

.stat-item {
    text-align: center;
    padding: 15px 25px;
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    backdrop-filter: blur(10px);
}

.stat-number {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 5px;
}

.stat-label {
    font-size: 12px;
    opacity: 0.8;
}

.search-card, .data-card {
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    border: none;
    margin-bottom: 20px;
}

.card-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 16px;
    font-weight: 600;
    color: #333;
}

.title-icon {
    font-size: 18px;
    color: #667eea;
}

.search-form {
    padding: 10px 0;
}

.modern-form {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    align-items: center;
}

.form-item {
    margin-bottom: 0;
}

.modern-input {
    border-radius: 8px;
    border: 1px solid #e8eaec;
    transition: all 0.3s ease;
}

.modern-input:hover {
    border-color: #667eea;
}

.modern-input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
}

.modern-select {
    border-radius: 8px;
}

.search-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.search-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.add-btn {
    background: linear-gradient(135deg, #19be6b 0%, #2db7f5 100%);
    border: none;
    border-radius: 8px;
    margin-left: auto;
    font-weight: 500;
    transition: all 0.3s ease;
}

.add-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(25, 190, 107, 0.3);
}

.table-container {
    padding: 10px 0;
}

.modern-table {
    border-radius: 8px;
    overflow: hidden;
}

.modern-table .ivu-table th {
    background: #f8f9fa;
    font-weight: 600;
    color: #333;
}

.modern-table .ivu-table td {
    transition: background-color 0.3s ease;
}

.modern-table .ivu-table tr:hover td {
    background-color: rgba(102, 126, 234, 0.05) !important;
}

.action-buttons {
    display: flex;
    gap: 8px;
    justify-content: center;
}

.action-btn {
    border-radius: 6px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.edit-btn {
    background: linear-gradient(135deg, #2db7f5 0%, #19be6b 100%);
    border: none;
}

.edit-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(45, 183, 245, 0.3);
}

.delete-btn {
    background: linear-gradient(135deg, #ed4014 0%, #ff9900 100%);
    border: none;
}

.delete-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(237, 64, 20, 0.3);
}

.pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: center;
}

.modern-pagination .ivu-page-item {
    border-radius: 6px;
    transition: all 0.3s ease;
}

.modern-pagination .ivu-page-item:hover {
    background: #667eea;
    color: #fff;
}

.modern-pagination .ivu-page-item-active {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-color: #667eea;
}

.modern-modal .ivu-modal-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
    border-radius: 8px 8px 0 0;
}

.modern-modal .ivu-modal-header-inner {
    color: #fff;
    font-weight: 600;
}

.modal-form {
    padding: 20px 0;
}

.gender-group {
    display: flex;
    gap: 20px;
}

.gender-radio {
    margin-right: 0;
}

.gender-radio .ivu-radio-inner {
    border-radius: 50%;
    border: 2px solid #e8eaec;
    transition: all 0.3s ease;
}

.gender-radio .ivu-radio-checked .ivu-radio-inner {
    border-color: #667eea;
    background: #667eea;
}

.gender-radio .ivu-radio-checked .ivu-radio-inner::after {
    background: #fff;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .page-header {
        flex-direction: column;
        gap: 20px;
        text-align: center;
    }
    
    .header-content {
        flex-direction: column;
        gap: 10px;
    }
    
    .header-stats {
        justify-content: center;
    }
    
    .modern-form {
        flex-direction: column;
        align-items: stretch;
    }
    
    .form-item {
        width: 100%;
    }
    
    .action-buttons {
        flex-direction: column;
        gap: 5px;
    }
}
</style>

<script>
import {
    getAllColleges,
    getAllGrades,
    getPageStudents,
    addStudents,
    updStudents,
    delStudents,
} from '../../api/index.js';
export default{
		
    data(){
        return {
            colleges: [],
            grades: [],
            pageInfos: [],
            pageIndex: 1,
            pageSize: 10,
            pageTotal: 0,
            totalInfo: 0,
            loading: true,
            showAddFlag: false,
            showUpdFlag: false,
            qryForm: {
                name: "",
                collegeId: "",
                gradeId: ""
            },
            studentForm: {
                id: "",
                userName: "",
                name: "",
                gender: "",
                age: "",
                collegeId: "",
                gradeId: ""
            },
            columns: [
                {title: '学生学号', key: 'id', align: 'center'},
                {title: '学生账号', key: 'userName', align: 'center'},
                {title: '学生姓名', key: 'name', align: 'center'},
                {title: '学生性别', key: 'gender', align: 'center'},
                {title: '学生年龄', key: 'age', align: 'center'},
                {title: '所属学院', key: 'collegeName', align: 'center'},
                {title: '所属班级', key: 'gradeName', align: 'center'},
                {title: '操作', slot: 'action', align: 'center'}
            ]
        }
    },
    methods:{
			
		getPageInfo(pageIndex, pageSize) {
			
            getPageStudents(pageIndex, pageSize, 
                    this.qryForm.name, this.qryForm.collegeId, this.qryForm.gradeId).then(resp => {
                
                this.pageInfos = resp.data.data;
                this.pageIndex = resp.data.pageIndex;
                this.pageSize = resp.data.pageSize;
                this.pageTotal = resp.data.pageTotal;
                this.totalInfo = resp.data.count;
        
                this.loading = false;
            });
        },
        handleCurrentChange(pageIndex) {
        
            this.getPageInfo(pageIndex, this.pageSize);
        },
        showAddWin(){

            this.studentForm = {
                id: "",
                userName: "",
                name: "",
                gender: "",
                age: "",
                collegeId: "",
                gradeId: ""
            };
            this.showAddFlag = true;
        },	
        showUpdWin(row) {
			
            this.studentForm = row;
            this.showUpdFlag = true;
        },
        addInfo() {
			
            addStudents(this.studentForm).then(resp => {
                
                if(resp.code == 0){

                    this.$Notice.success({
                        duration: 3,
                        title: resp.msg
                    });
                    
                    this.getPageInfo(1, this.pageSize);
                    
                    this.showAddFlag = false;
                }else{

                    this.$Notice.warning({
                        duration: 3,
                        title: resp.msg
                    });
                }
            });
        },
        updInfo() {
        
            updStudents(this.studentForm).then(resp => {
        
                this.$Notice.success({
                    duration: 3,
                    title: resp.msg
                });
        
                this.getPageInfo(1, this.pageSize);
        
                this.showUpdFlag = false;
            });
        },
        delInfo(id){

            this.$Modal.confirm({
                title: '系统提示',
                content: '即将删除相关信息, 是否继续?',
                onOk: () => {
                    delStudents(id).then(resp =>{
                        
                        if(resp.code == 0){
                            this.$Notice.success({
                                duration: 3,
                                title: resp.msg
                            });
                            
                            this.getPageInfo(1, this.pageSize);
                        }else{
                            
                            this.$Notice.warning({
                                duration: 3,
                                title: resp.msg
                            });
                        }
                    });
                },
            });
        }	
    },
    mounted(){

        getAllColleges().then(resp =>{

            this.colleges = resp.data;
        });
        getAllGrades().then(resp =>{

            this.grades = resp.data;
        });
        this.getPageInfo(1, this.pageSize);
    }
}
</script>