(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-67f0","chunk-6525"],{"+Jyj":function(e,t,i){},"41Be":function(e,t,i){"use strict";i.d(t,"a",function(){return a});var s=i("Q2AE");function a(e){if(e&&e instanceof Array&&e.length>0){var t=e;return!!(s.a.getters&&s.a.getters.roles).some(function(e){return t.includes(e)})}return console.error("need roles! Like v-permission=\"['admin','editor']\""),!1}},EM0K:function(e,t,i){},IGqm:function(e,t,i){"use strict";i.r(t);var s=i("41Be"),a=i("yUYn"),r=i("dMq6"),o=i("lYL8"),l=i("qpJb"),n={components:{Feedback:i("KglX").a},props:{isAdd:{type:Boolean,required:!0},sup_this:{type:Object,default:null},project_id:{type:[Number,String],required:!0}},data:function(){return{activeNames:[],dialogTableVisible:!1,task_type:[],taskType:[{id:0,value:"角色原画",text:"角色原画"},{id:1,value:"场景原画",text:"场景原画"},{id:2,value:"3D模型",text:"3D模型"},{id:3,value:"动作(2D3D)",text:"动作(2D3D)"},{id:4,value:"特效(2D3D)",text:"特效(2D3D)"},{id:5,value:"修图",text:"修图"},{id:6,value:"视频剪辑",text:"视频剪辑"},{id:7,value:"UI",text:"UI"},{id:8,value:"平面设计",text:"平面设计"}],task_priorities:[],taskPriority:[{id:0,value:"特急"},{id:1,value:"紧急"},{id:2,value:"急"},{id:3,value:"普通"}],task_qualities:[],taskQuality:[{id:0,value:"A+"},{id:1,value:"A"},{id:2,value:"B+"},{id:3,value:"B"},{id:4,value:"C+"},{id:5,value:"C"}],managers:[],loading:!1,dialog:!1,taskStatus:[{value:"未安排任务负责人",text:"未安排任务负责人"},{value:"已安排任务负责人",text:"已安排任务负责人"},{value:"等待接手",text:"等待接手"},{value:"已接手",text:"已接手"},{value:"已完成",text:"已完成"},{value:"已拒接",text:"已拒接"}],form:{name:"",type:"",priority:"",quality:"",points:0,period:[],receiver_id:"",receiver_name:"",files:[],content:"",memo:""},rules:{name:[{required:!0,message:"请输入任务名称",trigger:"blur"}],type:[{required:!0,message:"请输入任务类型",trigger:"blur"}],priority:[{required:!0,message:"请选择任务优先级",trigger:"blur"}],quality:[{required:!0,message:"请选择任务品质要求",trigger:"blur"}],manager:[{required:!0,message:"请选择任务负责人",trigger:"blur"}],period:[{required:!0,message:"请输入任务完成时间范围",trigger:"blur"}]}}},methods:{getFileType:function(e){e&&(this.form.type=e)},getFiles:function(e){console.log("val",e),e&&(this.form.files=e)},getRTEContent:function(e){e&&(this.form.content=e)},filterHandler:function(e,t,i){return t[i.property]===e},checkPermission:s.a,cancel:function(){this.resetForm()},doSubmit:function(){var e=this;this.$refs.form.validate(function(t){if(!t)return!1;e.loading=!0,e.isAdd?e.doAdd():e.doEdit()})},doAdd:function(){var e=this,t={name:this.form.name,task_type:this.form.type,task_priority:this.form.priority,points:this.form.points,task_quality:this.form.quality,receiver:this.form.receiver_id,content:this.form.content,type:this.form.type,memo:this.form.memo,begin_time:this.form.period[0],end_time:this.form.period[1],project:this.project_id};t.files=this.form.files.map(function(e){return e.url=e.raw_url||e.url,e}),Object(a.a)(t).then(function(t){e.resetForm(),e.$message({showClose:!0,type:"success",message:"添加成功!",duration:2500}),e.loading=!1,e.sup_this.init(),e.$refs.feedback.init()}).catch(function(t){e.loading=!1,console.log(t)})},doEdit:function(){var e=this,t={name:this.form.name,task_type:this.form.type,task_priority:this.form.priority,points:this.form.points,task_quality:this.form.quality,receiver:this.form.receiver_id,content:this.form.content,type:this.form.type,memo:this.form.memo,begin_time:this.form.period[0],end_time:this.form.period[1],project:this.form.project_id};t.files=this.form.files.map(function(e){return e.url=e.raw_url||e.url,e}),Object(a.c)(this.form.id,t).then(function(t){e.resetForm(),e.$message({showClose:!0,type:"success",message:"修改成功!",duration:2500}),e.loading=!1,e.sup_this.init(),e.$refs.feedback.init()}).catch(function(t){e.loading=!1,console.log(t)})},resetForm:function(){this.dialog=!1,this.$refs.form.resetFields(),this.form={name:""},this.form.type=this.task_type[0].id,this.form.priority=this.task_priorities[0].id,this.form.quality=this.task_qualities[0].id,this.form.files=[]},getAllTaskManagers:function(){var e=this;Object(a.d)().then(function(t){e.managers=t.detail,e.managers.length>0&&e.managers.forEach(function(t){t.name=t.name||"-",t.task_type=t.task_type||"-",t.task_name=t.task_name||"-",t.progress=0===t.task_progress?"0%":t.task_progress?t.task_progress+"%":"-",t.end_time=t.end_time||"-",t.left_days=""!==t.leftdays?t.leftdays:"-",t.task_status=""!==t.receive_status?e.taskStatus[t.receive_status]:"-"})})},open:function(){console.log("this.form",this.form),this.getAllTaskManagers()},selectTaskReceiver:function(e){e&&(this.form.receiver_name=e.name||"-",this.form.receiver_id=e.user_id||"-",this.dialogTableVisible=!1)},getTaskTypes:function(){var e=this;Object(r.b)().then(function(t){t&&t.length>0?(e.task_type=t,e.form.type=t[0].id):e.task_type=[]}).catch(function(t){console.log(t),e.task_type=[]})},getTaskPriorities:function(){var e=this;Object(o.d)().then(function(t){t&&t.length>0?(e.task_priorities=t,e.form.priority=t[0].id):e.task_priorities=[]}).catch(function(t){console.log(t),e.task_priorities=[]})},getTaskQualities:function(){var e=this;Object(l.d)().then(function(t){t&&t.length>0?(e.task_qualities=t,e.form.quality=t[0].id):e.task_qualities=[]}).catch(function(t){console.log(t),e.task_qualities=[]})},init:function(){this.getTaskTypes(),this.getTaskPriorities(),this.getTaskQualities()}},created:function(){this.init()}},c=(i("REHs"),i("KHd+")),u=Object(c.a)(n,function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("el-dialog",{attrs:{width:"70%","append-to-body":!0,visible:e.dialog,title:e.isAdd?"新增任务":"编辑任务"},on:{"update:visible":function(t){e.dialog=t},open:e.open}},[i("el-form",{ref:"form",attrs:{size:"small","label-width":"96px",model:e.form,rules:e.rules}},[i("el-row",[i("el-col",{attrs:{span:12}},[i("el-form-item",{attrs:{label:"任务名称",prop:"name"}},[i("el-input",{staticStyle:{width:"338px"},model:{value:e.form.name,callback:function(t){e.$set(e.form,"name",t)},expression:"form.name"}})],1),e._v(" "),i("el-form-item",{attrs:{label:"类型",prop:"type"}},[i("el-select",{staticStyle:{width:"338px"},attrs:{placeholder:"请选择",value:""},model:{value:e.form.type,callback:function(t){e.$set(e.form,"type",t)},expression:"form.type"}},e._l(e.task_type,function(e){return i("el-option",{key:e.id,attrs:{label:e.name,value:e.id}})}))],1),e._v(" "),i("el-form-item",{attrs:{label:"优先级",prop:"priority"}},[i("el-select",{staticStyle:{width:"338px"},attrs:{placeholder:"请选择",value:""},model:{value:e.form.priority,callback:function(t){e.$set(e.form,"priority",t)},expression:"form.priority"}},e._l(e.task_priorities,function(e){return i("el-option",{key:e.id,attrs:{label:e.name,value:e.id}})}))],1),e._v(" "),i("el-form-item",{attrs:{label:"品质要求",prop:"quality"}},[i("el-select",{staticStyle:{width:"338px"},attrs:{placeholder:"请选择",value:""},model:{value:e.form.quality,callback:function(t){e.$set(e.form,"quality",t)},expression:"form.quality"}},e._l(e.task_qualities,function(e){return i("el-option",{key:e.id,attrs:{label:e.name,value:e.id}})}))],1),e._v(" "),e.checkPermission(["admin","task_all","task_points_view","task_points_edit"])?i("el-form-item",{attrs:{label:"积分",prop:"points"}},[i("el-input",{staticStyle:{width:"338px"},model:{value:e.form.points,callback:function(t){e.$set(e.form,"points",t)},expression:"form.points"}})],1):e._e(),e._v(" "),i("el-form-item",{attrs:{label:"时间范围",prop:"period"}},[i("el-date-picker",{staticStyle:{width:"338px"},attrs:{type:"daterange","range-separator":"至","start-placeholder":"开始日期","end-placeholder":"结束日期","value-format":"yyyy-MM-dd"},model:{value:e.form.period,callback:function(t){e.$set(e.form,"period",t)},expression:"form.period"}})],1),e._v(" "),i("el-form-item",{attrs:{label:"任务负责人"}},[i("el-input",{staticStyle:{width:"338px"},attrs:{disabled:"",placeholder:"请选择任务负责人"},model:{value:e.form.receiver_name,callback:function(t){e.$set(e.form,"receiver_name",t)},expression:"form.receiver_name"}},[i("el-button",{attrs:{slot:"append"},on:{click:function(t){e.dialogTableVisible=!0}},slot:"append"},[e._v("...")])],1)],1),e._v(" "),i("el-form-item",{attrs:{label:"备注",prop:"memo"}},[i("el-input",{staticStyle:{width:"338px"},attrs:{type:"textarea"},model:{value:e.form.memo,callback:function(t){e.$set(e.form,"memo",t)},expression:"form.memo"}})],1)],1),e._v(" "),i("el-col",{attrs:{span:12}},[i("Feedback",{ref:"feedback",attrs:{files:e.form.files,content:e.form.content},on:{getFiles:e.getFiles,getRTEContent:e.getRTEContent,getFileType:e.getFileType}})],1)],1)],1),e._v(" "),i("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[i("el-button",{attrs:{type:"text"},on:{click:e.cancel}},[e._v("取消")]),e._v(" "),i("el-button",{attrs:{loading:e.loading,type:"primary"},on:{click:e.doSubmit}},[e._v("确认")])],1),e._v(" "),i("el-dialog",{attrs:{visible:e.dialogTableVisible,"append-to-body":""},on:{"update:visible":function(t){e.dialogTableVisible=t}}},[i("el-table",{attrs:{"highlight-current-row":"",data:e.managers},on:{"row-dblclick":e.selectTaskReceiver}},[i("el-table-column",{attrs:{property:"name",label:"姓名","show-overflow-tooltip":!0}}),e._v(" "),i("el-table-column",{attrs:{property:"task_type",label:"任务类型",filters:e.taskType,"filter-method":e.filterHandler}}),e._v(" "),i("el-table-column",{attrs:{property:"task_name",label:"任务名称"}}),e._v(" "),i("el-table-column",{attrs:{property:"end_time",sortable:"",label:"结束时间"}}),e._v(" "),i("el-table-column",{attrs:{property:"left_days",sortable:"",label:"剩余天数"}}),e._v(" "),i("el-table-column",{attrs:{property:"progress",sortable:"",label:"进度",width:"80"}}),e._v(" "),i("el-table-column",{attrs:{property:"task_status",label:"任务状态",filters:e.taskStatus,"filter-method":e.filterHandler,"show-overflow-tooltip":!0}}),e._v(" "),i("el-table-column",{attrs:{fixed:"right",label:"操作",width:"100"},scopedSlots:e._u([{key:"default",fn:function(t){return[i("el-button",{attrs:{type:"primary",size:"small"},on:{click:function(i){e.selectTaskReceiver(t.row)}}},[e._v("选择")])]}}])})],1)],1)],1)},[],!1,null,"17f13b54",null);u.options.__file="form.vue";t.default=u.exports},IfqL:function(e,t,i){"use strict";var s=i("EM0K");i.n(s).a},REHs:function(e,t,i){"use strict";var s=i("+Jyj");i.n(s).a},lrNY:function(e,t,i){"use strict";i.r(t);var s=i("41Be"),a={components:{eForm:i("IGqm").default},props:{query:{type:Object,required:!0},sup_this:{type:Object,default:null}},data:function(){return{taskTypes:[],taskQualities:[],taskPriorities:[],checkedTaskTypeIds:[],checkedTaskPriorityIds:[],checkedTaskQualityIds:[],skills:[]}},created:function(){this.init()},watch:{checkedTaskTypeIds:function(){this.handleCheckedTaskTypesChange(this.checkedTaskTypeIds)}},methods:{checkPermission:s.a,toQuery:function(){this.sup_this.page=1,this.sup_this.init()},init:function(){this.taskTypes=this.$store.state.task.types||[],this.taskPriorities=this.$store.state.task.priorities||[],this.taskQualities=this.$store.state.task.qualities||[],this.skills=this.$store.state.user.skills||[],this.checkedTaskTypeIds=this.skills.map(function(e){return e.id}),this.handleCheckedTaskTypesChange(this.checkedTaskTypeIds)},refresh:function(){this.sup_this.init()},handleCheckedTaskTypesChange:function(e){e&&(this.query.task_type_ids=e.join()),this.toQuery()},handleCheckedTaskPrioritiesChange:function(e){e&&(this.query.task_priority_ids=e.join()),this.toQuery()},handleCheckedTaskQualitiesChange:function(e){e&&(this.query.task_quality_ids=e.join()),this.toQuery()}}},r=(i("IfqL"),i("KHd+")),o=Object(r.a)(a,function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{staticClass:"head-container"},[i("el-form",{attrs:{"label-position":"right","label-width":"100px"}},[i("el-form-item",{attrs:{label:"任务类型："}},[i("el-checkbox-group",{attrs:{size:"mini"},on:{change:e.handleCheckedTaskTypesChange},model:{value:e.checkedTaskTypeIds,callback:function(t){e.checkedTaskTypeIds=t},expression:"checkedTaskTypeIds"}},e._l(e.taskTypes,function(t){return i("el-checkbox-button",{key:t.id,attrs:{label:t.id}},[e._v(e._s(t.name)+"\n        ")])}))],1),e._v(" "),i("el-form-item",{attrs:{label:"优先级："}},[i("el-checkbox-group",{attrs:{size:"mini"},on:{change:e.handleCheckedTaskPrioritiesChange},model:{value:e.checkedTaskPriorityIds,callback:function(t){e.checkedTaskPriorityIds=t},expression:"checkedTaskPriorityIds"}},e._l(e.taskPriorities,function(t){return i("el-checkbox-button",{key:t.id,attrs:{label:t.id}},[e._v(e._s(t.name)+"\n        ")])}))],1),e._v(" "),i("el-form-item",{attrs:{label:"品质要求："}},[i("el-checkbox-group",{attrs:{size:"mini"},on:{change:e.handleCheckedTaskQualitiesChange},model:{value:e.checkedTaskQualityIds,callback:function(t){e.checkedTaskQualityIds=t},expression:"checkedTaskQualityIds"}},e._l(e.taskQualities,function(t){return i("el-checkbox-button",{key:t.id,attrs:{label:t.id}},[e._v(e._s(t.name)+"\n        ")])}))],1)],1),e._v(" "),i("div",{staticClass:"btn_wrapper"},[i("el-button",{staticClass:"refresh",attrs:{type:"primary"},on:{click:e.refresh}},[e._v("刷新\n    ")])],1)],1)},[],!1,null,"3f1a571d",null);o.options.__file="header.vue";t.default=o.exports}}]);