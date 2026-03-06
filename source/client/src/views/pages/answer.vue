<template>
    <div class="fater-answer-panle">
        <div class="fater-answer-left">
            <div class="fater-answer-time">
                倒计时  {{ countDown.text }}
            </div>
            <div class="fater-answer-select-list">
                <Divider>选择题</Divider>
                <Row class="fater-answer-select-item" :gutter="15">
                    <Col v-for="(item, index) in p_list_0" :key="index" span="6">
                        <Button @click="getItem(item.id, item.no)" type="primary">{{ item.no }}</Button>
                    </Col>
                </Row>
                <Divider>填空题</Divider>
                <Row class="fater-answer-select-item" :gutter="15">
                    <Col v-for="(item, index) in p_list_1" :key="index" span="6">
                        <Button @click="getItem(item.id, item.no)" type="primary">{{ item.no }}</Button>
                    </Col>
                </Row>
                <Divider>判断题</Divider>
                <Row class="fater-answer-select-item" :gutter="15">
                    <Col v-for="(item, index) in p_list_2" :key="index" span="6">
                        <Button @click="getItem(item.id, item.no)" type="primary">{{ item.no }}</Button>
                    </Col>
                </Row>
                <Divider>编程题</Divider>
                <Row class="fater-answer-select-item" :gutter="15">
                    <Col v-for="(item, index) in p_list_3" :key="index" span="6">
                        <Button @click="getItem(item.id, item.no)" type="primary">{{ item.no }}</Button>
                    </Col>
                </Row>
            </div>
            <div class="fater-answer-flag">
                仔细阅读，认真答题，遵守考试纪律
            </div>
        </div>
        <div class="fater-answer-right">
            <div class="fater-answer-info">
                <div class="fater-answer-info-item">
                    <span>学生学号：</span>
                    <span>{{ userInfo.id }}</span>
                </div>
                <div class="fater-answer-info-item">
                    <span>学生姓名：</span>
                    <span>{{ userInfo.name }}</span>
                </div>
                <div class="fater-answer-info-item">
                    <span>学生性别：</span>
                    <span>{{ userInfo.gender }}</span>
                </div>
                <div class="fater-answer-info-item">
                    <span>所属学院：</span>
                    <span>{{ userInfo.collegeName }}</span>
                </div>
                <div class="fater-answer-info-item">
                    <span>所在班级：</span>
                    <span>{{ userInfo.gradeName }}</span>
                </div>
            </div>
            <div class="fater-answer-body">
                <div class="fater-answer-practise" v-if="practise && practise.id">
                    {{ practise.no }}. {{ practise.name }}
                </div>
                <div class="fater-answer-input">
                    <RadioGroup v-if="practise.type==0" v-model="practise.answer" vertical>
                        <Radio v-for="(item, index) in practise.options" 
                                :key="index" :label="item.id">{{ item.name }}</Radio>
                    </RadioGroup>
                    <Input v-else-if="practise.type==1" 
                            v-model="practise.answer" placeholder="输入正确答案..."/>
                    <RadioGroup v-else-if="practise.type==2" v-model="practise.answer">
                        <Radio label="正确">正确</Radio>
                        <Radio label="错误">错误</Radio>
                    </RadioGroup>
                    <Input v-else-if="practise.type==3" type="textarea" 
                           :rows="15" v-model="practise.answer" placeholder="输入正确答案..."/>
                    <div v-else class="empty-tip">暂无题目，请联系老师或管理员补充题库</div>
                </div>
            </div>
            <div class="fater-answer-foot">
                <div class="fater-answer-foot-desc">
                    本次针对{{ examInfo.gradeName }}{{ examInfo.projectName }}考试, 其中选择题10道(每道2分), 填空题10道(每道2分),
                    判断题10道(每道2分), 编程题2道(每道20分), 考试时间120分钟, 满分100分
                </div>
                <div class="fater-answer-foot-subbtn">
                    <Button @click="subAnswers()" type="primary">交卷</Button>
                </div>
            </div>
        </div>
        <div style="clear:both"></div>
    </div>
</template>

<style>

</style>

<script>
import {
    getPractiseInfo,
    makeExams,
    getExamInfo,
    getLoginUser,
    addAnswerLog
} from '../../api/index.js';
import {
    countDown,
    formatCountDown,
    contrastCountDown,
    formatDate
} from '../../utils/date.js';
export default{
    data(){
        return {
            userInfo: {},
            p_list_0: [],
            p_list_1: [],
            p_list_2: [],
            p_list_3: [],
            examInfo: {},
            countDown: {
                text: "",
                startTime: "",
                endTime: ""
            },
            practise: {
                no: 1,
                id: "",
                name: "",
                answer: null,
                type: "",
                options: [],
            }
        }
    },
    methods: {
        
        getAnswerIsNull(){

            let resl = [];

            this.p_list_0.forEach(item =>{

                if(item.answer){

                }else{
                    resl.push(item.no);
                }
            });
            this.p_list_1.forEach(item =>{

                if(item.answer){

                }else{
                    resl.push(item.no);
                }
            });
            this.p_list_2.forEach(item =>{

                if(item.answer){

                }else{
                    resl.push(item.no);
                }
            });
            this.p_list_3.forEach(item =>{

                if(item.answer){

                }else{
                    resl.push(item.no);
                }
            });

            return resl;
        },
        subAnswers(){

            let answersIsNull = this.getAnswerIsNull();

            if(answersIsNull.length==0){

                let answers=[], nos=[], practiseIds=[];
                this.p_list_0.forEach(item =>{

                    answers.push(item.answer);
                    nos.push(item.no);
                    practiseIds.push(item.id);
                });
                this.p_list_1.forEach(item =>{

                    answers.push(item.answer);
                    nos.push(item.no);
                    practiseIds.push(item.id);
                });
                this.p_list_2.forEach(item =>{

                    answers.push(item.answer);
                    nos.push(item.no);
                    practiseIds.push(item.id);
                });
                this.p_list_3.forEach(item =>{

                    answers.push(item.answer);
                    nos.push(item.no);
                    practiseIds.push(item.id);
                });

                addAnswerLog({
                    token: this.$store.state.token || sessionStorage.getItem('token'),
                    examId: this.$route.query.id,
                    answers: answers,
                    nos: nos,
                    practiseIds: practiseIds
                }).then(resp =>{

                    this.$Notice.success({
                        title: '系统提示',
                        desc: '提交成功，请耐心等待教师审核结果'
                    });
                    this.$router.push('/welcome');
                }).catch(err => {
                    const msg = (err && err.msg) ? err.msg : '提交失败，请稍后重试';
                    this.$Message.error(msg);
                });
            }else{

                this.$Notice.warning({
                    title: '系统提示',
                    desc: '题目 ' + answersIsNull.join(', ') + ' 尚未完成, 请填写完整之后再提交'
                });
            }
        },
        getItem(id, no){

            getPractiseInfo(id).then(resp =>{

                if(resp.data.type == 0){

                    let temp = this.p_list_0[no-1];
                    this.practise = {
                        token: this.$store.state.token || sessionStorage.getItem('token'),
                        examId: this.$route.query.id,
                        no: no,
                        id: resp.data.id,
                        name: resp.data.name,
                        answer: temp.answer ? temp.answer : null,
                        type: resp.data.type,
                        options: resp.data.options,
                    }
                }else if(resp.data.type == 1){
                    
                    let temp = this.p_list_1[no-1-10];
                    this.practise = {
                        token: this.$store.state.token || sessionStorage.getItem('token'),
                        examId: this.$route.query.id,
                        no: no,
                        id: resp.data.id,
                        name: resp.data.name,
                        answer: temp.answer ? temp.answer : null,
                        type: resp.data.type
                    }
                }else if(resp.data.type == 2){
                    
                    let temp = this.p_list_2[no-1-20];
                    this.practise = {
                        token: this.$store.state.token || sessionStorage.getItem('token'),
                        examId: this.$route.query.id,
                        no: no,
                        id: resp.data.id,
                        name: resp.data.name,
                        answer: temp.answer ? temp.answer : null,
                        type: resp.data.type
                    }
                }else if(resp.data.type == 3){
                    
                    let temp = this.p_list_3[no-1-30];
                    this.practise = {
                        token: this.$store.state.token || sessionStorage.getItem('token'),
                        examId: this.$route.query.id,
                        no: no,
                        id: resp.data.id,
                        name: resp.data.name,
                        answer: temp.answer ? temp.answer : null,
                        type: resp.data.type
                    }
                }
            });
        },
        initCountDown(){
            
            let temp1 = new Date();
            this.countDown.startTime = formatDate(temp1);
            let temp2 = new Date();
            temp1.setTime(temp2.getTime() + 1000*60*60*2);
            this.countDown.endTime = formatDate(temp1);
        }
    },
    watch: {

        practise(newVal, oldVal){

            if(oldVal.type == 0){

                (this.p_list_0[oldVal.no-1])['answer'] = oldVal['answer'] ? oldVal['answer'] : null;
            }else if(oldVal.type == 1){

                (this.p_list_1[oldVal.no-1-10])['answer'] = oldVal['answer'] ? oldVal['answer'] : null;
            }else if(oldVal.type == 2){

                (this.p_list_2[oldVal.no-1-20])['answer'] = oldVal['answer'] ? oldVal['answer'] : null;
            }else if(oldVal.type == 3){

                (this.p_list_3[oldVal.no-1-30])['answer'] = oldVal['answer'] ? oldVal['answer'] : null;
            }
        }
    },
    mounted(){

        getLoginUser(this.$store.state.token || sessionStorage.getItem('token')).then(resp =>{

            this.userInfo = resp.data;
        }).catch(()=>{});
        getExamInfo(this.$route.query.id).then(resp =>{

            this.examInfo = resp.data;

            // 若设置了开始/结束时间，进行校验；只要未过期即可继续
            try {
                const hasStart = !!this.examInfo.startTime;
                const hasEnd = !!this.examInfo.endTime;
                if (hasStart || hasEnd) {
                    const now = new Date();
                    const s = hasStart ? new Date(String(this.examInfo.startTime).replace(/-/g,'/')) : null;
                    const e = hasEnd ? new Date(String(this.examInfo.endTime).replace(/-/g,'/')) : null;
                    if (s && now < s) {
                        this.$Message.warning('考试未开始（当前允许进入用于测试）');
                    }
                    if (e && now > e) {
                        this.$Message.warning('考试已结束（当前允许进入用于测试）');
                    }
                }
            } catch(_) {}

            makeExams(this.examInfo.projectId).then(res =>{

                const item0 = res.data.item_0 || []
                const item1 = res.data.item_1 || []
                const item2 = res.data.item_2 || []
                const item3 = res.data.item_3 || []

                item0.forEach((item, index) =>{

                    if(index == 0){
                        getPractiseInfo(item).then(re =>{

                            this.practise = {
                                no: index+1,
                                id: re.data.id,
                                name: re.data.name,
                                answer: null,
                                type: 0,
                                options: re.data.options,
                            }
                        }).catch(()=>{
                            // 没有取到题目时，保持空白提示
                        });
                    }

                    this.p_list_0.push({
                        no: index+1,
                        id: item,
                        answer: "",
                        type: 0
                    });
                });
                item1.forEach((item, index) =>{

                    this.p_list_1.push({
                        no: index+1+10,
                        id: item,
                        answer: "",
                        type: 1
                    });
                });
                item2.forEach((item, index) =>{

                    this.p_list_2.push({
                        no: index+1+20,
                        id: item,
                        answer: "",
                        type: 2
                    });
                });
                item3.forEach((item, index) =>{

                    this.p_list_3.push({
                        no: index+1+30,
                        id: item,
                        answer: "",
                        type: 3
                    });
                });
                // 若四类题目都为空，给出提示
                if (!item0.length && !item1.length && !item2.length && !item3.length) {
                    this.$Message.warning('该学科题库题量不足，请先在题库中补充题目后再开始考试');
                }
            }).catch((err)=>{
                this.$Message.error((err && err.msg) ? err.msg : '无法生成试卷，请先补充题库');
            });
        }).catch((err)=>{
            this.$Message.error((err && err.msg) ? err.msg : '无法获取考试信息');
        });
        
        this.initCountDown();
        let timer = setInterval(() =>{

            let temp = countDown(this.countDown.startTime, this.countDown.endTime);
            if(contrastCountDown(temp.h, temp.m, temp.s)){

                this.$Modal.warning({
                    title: '系统提示',
                    content: '考试时间已到，请交卷',
                    onOk: () => {
                        let answers=[], nos=[], practiseIds=[];
                        this.p_list_0.forEach(item =>{

                            answers.push(item.answer ? item.answer : '');
                            nos.push(item.no);
                            practiseIds.push(item.id);
                        });
                        this.p_list_1.forEach(item =>{

                            answers.push(item.answer ? item.answer : '');
                            nos.push(item.no);
                            practiseIds.push(item.id);
                        });
                        this.p_list_2.forEach(item =>{

                            answers.push(item.answer ? item.answer : '');
                            nos.push(item.no);
                            practiseIds.push(item.id);
                        });
                        this.p_list_3.forEach(item =>{

                            answers.push(item.answer ? item.answer : '');
                            nos.push(item.no);
                            practiseIds.push(item.id);
                        });

                        addAnswerLog({

                            token: this.$store.state.token || sessionStorage.getItem('token'),
                            examId: this.$route.query.id,
                            answers: answers,
                            nos: nos,
                            practiseIds: practiseIds
                        }).then(resp =>{

                            this.$Notice.success({
                                title: '系统提示',
                                desc: '提交成功，请耐心等待教师审核结果'
                            });
                            this.$router.push('/welcome');
                            clearInterval(timer);
                        });
                    },
                });
            }else{

                this.countDown.text = formatCountDown(temp.h, temp.m, temp.s);
                this.countDown.startTime = formatDate(new Date());
            }
        }, 1000);
    }
}
</script>
