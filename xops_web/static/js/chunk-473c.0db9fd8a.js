(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-473c","chunk-6525"],{"+Jyj":function(t,e,i){},"41Be":function(t,e,i){"use strict";i.d(e,"a",function(){return a});var r=i("Q2AE");function a(t){if(t&&t instanceof Array&&t.length>0){var e=t;return!!(r.a.getters&&r.a.getters.roles).some(function(t){return e.includes(t)})}return console.error("need roles! Like v-permission=\"['admin','editor']\""),!1}},"623q":function(t,e,i){"use strict";var r=i("pMCq");i.n(r).a},DgwL:function(t,e,i){"use strict";i.r(e);var r={components:{eForm:i("IGqm").default},props:{data:{type:Object,required:!0},sup_this:{type:Object,required:!0},disabled:{type:Boolean,default:!1}},data:function(){return{project_id:""}},methods:{to:function(){var t=this.$refs.form;t.form={id:this.data.id,name:this.data.name,type:this.data.task_type?this.data.task_type.id:"",priority:this.data.task_priority?this.data.task_priority.id:"",quality:this.data.task_quality?this.data.task_quality.id:"",points:this.data.points,period:[this.data.begin_time,this.data.end_time],receiver_id:this.data.receiver?this.data.receiver.id:"",receiver_name:this.data.receiver?this.data.receiver.name:"",files:this.data.files,content:this.data.content,memo:this.data.memo,project_id:this.data.project?this.data.project.id:""},t.dialog=!0,this.project_id=this.data.project?this.data.project.id:""}}},a=(i("623q"),i("KHd+")),s=Object(a.a)(r,function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",[i("el-button",{attrs:{disabled:t.disabled,size:"mini",type:"success"},on:{click:function(e){return e.stopPropagation(),t.to(e)}}},[t._v("编辑\n  ")]),t._v(" "),i("eForm",{ref:"form",attrs:{sup_this:t.sup_this,"is-add":!1,project_id:t.project_id}})],1)},[],!1,null,"56d0fa90",null);s.options.__file="edit.vue";e.default=s.exports},IGqm:function(t,e,i){"use strict";i.r(e);var r=i("41Be"),a=i("yUYn"),s=i("dMq6"),o=i("lYL8"),l=i("qpJb"),n={components:{Feedback:i("KglX").a},props:{isAdd:{type:Boolean,required:!0},sup_this:{type:Object,default:null},project_id:{type:[Number,String],required:!0}},data:function(){return{activeNames:[],dialogTableVisible:!1,task_type:[],taskType:[{id:0,value:"角色原画",text:"角色原画"},{id:1,value:"场景原画",text:"场景原画"},{id:2,value:"3D模型",text:"3D模型"},{id:3,value:"动作(2D3D)",text:"动作(2D3D)"},{id:4,value:"特效(2D3D)",text:"特效(2D3D)"},{id:5,value:"修图",text:"修图"},{id:6,value:"视频剪辑",text:"视频剪辑"},{id:7,value:"UI",text:"UI"},{id:8,value:"平面设计",text:"平面设计"}],task_priorities:[],taskPriority:[{id:0,value:"特急"},{id:1,value:"紧急"},{id:2,value:"急"},{id:3,value:"普通"}],task_qualities:[],taskQuality:[{id:0,value:"A+"},{id:1,value:"A"},{id:2,value:"B+"},{id:3,value:"B"},{id:4,value:"C+"},{id:5,value:"C"}],managers:[],loading:!1,dialog:!1,taskStatus:[{value:"未安排任务负责人",text:"未安排任务负责人"},{value:"已安排任务负责人",text:"已安排任务负责人"},{value:"等待接手",text:"等待接手"},{value:"已接手",text:"已接手"},{value:"已完成",text:"已完成"},{value:"已拒接",text:"已拒接"}],form:{name:"",type:"",priority:"",quality:"",points:0,period:[],receiver_id:"",receiver_name:"",files:[],content:"",memo:""},rules:{name:[{required:!0,message:"请输入任务名称",trigger:"blur"}],type:[{required:!0,message:"请输入任务类型",trigger:"blur"}],priority:[{required:!0,message:"请选择任务优先级",trigger:"blur"}],quality:[{required:!0,message:"请选择任务品质要求",trigger:"blur"}],manager:[{required:!0,message:"请选择任务负责人",trigger:"blur"}],period:[{required:!0,message:"请输入任务完成时间范围",trigger:"blur"}]}}},methods:{getFileType:function(t){t&&(this.form.type=t)},getFiles:function(t){console.log("val",t),t&&(this.form.files=t)},getRTEContent:function(t){t&&(this.form.content=t)},filterHandler:function(t,e,i){return e[i.property]===t},checkPermission:r.a,cancel:function(){this.resetForm()},doSubmit:function(){var t=this;this.$refs.form.validate(function(e){if(!e)return!1;t.loading=!0,t.isAdd?t.doAdd():t.doEdit()})},doAdd:function(){var t=this,e={name:this.form.name,task_type:this.form.type,task_priority:this.form.priority,points:this.form.points,task_quality:this.form.quality,receiver:this.form.receiver_id,content:this.form.content,type:this.form.type,memo:this.form.memo,begin_time:this.form.period[0],end_time:this.form.period[1],project:this.project_id};e.files=this.form.files.map(function(t){return t.url=t.raw_url||t.url,t}),Object(a.a)(e).then(function(e){t.resetForm(),t.$message({showClose:!0,type:"success",message:"添加成功!",duration:2500}),t.loading=!1,t.sup_this.init(),t.$refs.feedback.init()}).catch(function(e){t.loading=!1,console.log(e)})},doEdit:function(){var t=this,e={name:this.form.name,task_type:this.form.type,task_priority:this.form.priority,points:this.form.points,task_quality:this.form.quality,receiver:this.form.receiver_id,content:this.form.content,type:this.form.type,memo:this.form.memo,begin_time:this.form.period[0],end_time:this.form.period[1],project:this.form.project_id};e.files=this.form.files.map(function(t){return t.url=t.raw_url||t.url,t}),Object(a.c)(this.form.id,e).then(function(e){t.resetForm(),t.$message({showClose:!0,type:"success",message:"修改成功!",duration:2500}),t.loading=!1,t.sup_this.init(),t.$refs.feedback.init()}).catch(function(e){t.loading=!1,console.log(e)})},resetForm:function(){this.dialog=!1,this.$refs.form.resetFields(),this.form={name:""},this.form.type=this.task_type[0].id,this.form.priority=this.task_priorities[0].id,this.form.quality=this.task_qualities[0].id,this.form.files=[]},getAllTaskManagers:function(){var t=this;Object(a.d)().then(function(e){t.managers=e.detail,t.managers.length>0&&t.managers.forEach(function(e){e.name=e.name||"-",e.task_type=e.task_type||"-",e.task_name=e.task_name||"-",e.progress=0===e.task_progress?"0%":e.task_progress?e.task_progress+"%":"-",e.end_time=e.end_time||"-",e.left_days=""!==e.leftdays?e.leftdays:"-",e.task_status=""!==e.receive_status?t.taskStatus[e.receive_status]:"-"})})},open:function(){console.log("this.form",this.form),this.getAllTaskManagers()},selectTaskReceiver:function(t){t&&(this.form.receiver_name=t.name||"-",this.form.receiver_id=t.user_id||"-",this.dialogTableVisible=!1)},getTaskTypes:function(){var t=this;Object(s.b)().then(function(e){e&&e.length>0?(t.task_type=e,t.form.type=e[0].id):t.task_type=[]}).catch(function(e){console.log(e),t.task_type=[]})},getTaskPriorities:function(){var t=this;Object(o.d)().then(function(e){e&&e.length>0?(t.task_priorities=e,t.form.priority=e[0].id):t.task_priorities=[]}).catch(function(e){console.log(e),t.task_priorities=[]})},getTaskQualities:function(){var t=this;Object(l.d)().then(function(e){e&&e.length>0?(t.task_qualities=e,t.form.quality=e[0].id):t.task_qualities=[]}).catch(function(e){console.log(e),t.task_qualities=[]})},init:function(){this.getTaskTypes(),this.getTaskPriorities(),this.getTaskQualities()}},created:function(){this.init()}},d=(i("REHs"),i("KHd+")),c=Object(d.a)(n,function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("el-dialog",{attrs:{width:"70%","append-to-body":!0,visible:t.dialog,title:t.isAdd?"新增任务":"编辑任务"},on:{"update:visible":function(e){t.dialog=e},open:t.open}},[i("el-form",{ref:"form",attrs:{size:"small","label-width":"96px",model:t.form,rules:t.rules}},[i("el-row",[i("el-col",{attrs:{span:12}},[i("el-form-item",{attrs:{label:"任务名称",prop:"name"}},[i("el-input",{staticStyle:{width:"338px"},model:{value:t.form.name,callback:function(e){t.$set(t.form,"name",e)},expression:"form.name"}})],1),t._v(" "),i("el-form-item",{attrs:{label:"类型",prop:"type"}},[i("el-select",{staticStyle:{width:"338px"},attrs:{placeholder:"请选择",value:""},model:{value:t.form.type,callback:function(e){t.$set(t.form,"type",e)},expression:"form.type"}},t._l(t.task_type,function(t){return i("el-option",{key:t.id,attrs:{label:t.name,value:t.id}})}))],1),t._v(" "),i("el-form-item",{attrs:{label:"优先级",prop:"priority"}},[i("el-select",{staticStyle:{width:"338px"},attrs:{placeholder:"请选择",value:""},model:{value:t.form.priority,callback:function(e){t.$set(t.form,"priority",e)},expression:"form.priority"}},t._l(t.task_priorities,function(t){return i("el-option",{key:t.id,attrs:{label:t.name,value:t.id}})}))],1),t._v(" "),i("el-form-item",{attrs:{label:"品质要求",prop:"quality"}},[i("el-select",{staticStyle:{width:"338px"},attrs:{placeholder:"请选择",value:""},model:{value:t.form.quality,callback:function(e){t.$set(t.form,"quality",e)},expression:"form.quality"}},t._l(t.task_qualities,function(t){return i("el-option",{key:t.id,attrs:{label:t.name,value:t.id}})}))],1),t._v(" "),t.checkPermission(["admin","task_all","task_points_view","task_points_edit"])?i("el-form-item",{attrs:{label:"积分",prop:"points"}},[i("el-input",{staticStyle:{width:"338px"},model:{value:t.form.points,callback:function(e){t.$set(t.form,"points",e)},expression:"form.points"}})],1):t._e(),t._v(" "),i("el-form-item",{attrs:{label:"时间范围",prop:"period"}},[i("el-date-picker",{staticStyle:{width:"338px"},attrs:{type:"daterange","range-separator":"至","start-placeholder":"开始日期","end-placeholder":"结束日期","value-format":"yyyy-MM-dd"},model:{value:t.form.period,callback:function(e){t.$set(t.form,"period",e)},expression:"form.period"}})],1),t._v(" "),i("el-form-item",{attrs:{label:"任务负责人"}},[i("el-input",{staticStyle:{width:"338px"},attrs:{disabled:"",placeholder:"请选择任务负责人"},model:{value:t.form.receiver_name,callback:function(e){t.$set(t.form,"receiver_name",e)},expression:"form.receiver_name"}},[i("el-button",{attrs:{slot:"append"},on:{click:function(e){t.dialogTableVisible=!0}},slot:"append"},[t._v("...")])],1)],1),t._v(" "),i("el-form-item",{attrs:{label:"备注",prop:"memo"}},[i("el-input",{staticStyle:{width:"338px"},attrs:{type:"textarea"},model:{value:t.form.memo,callback:function(e){t.$set(t.form,"memo",e)},expression:"form.memo"}})],1)],1),t._v(" "),i("el-col",{attrs:{span:12}},[i("Feedback",{ref:"feedback",attrs:{files:t.form.files,content:t.form.content},on:{getFiles:t.getFiles,getRTEContent:t.getRTEContent,getFileType:t.getFileType}})],1)],1)],1),t._v(" "),i("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[i("el-button",{attrs:{type:"text"},on:{click:t.cancel}},[t._v("取消")]),t._v(" "),i("el-button",{attrs:{loading:t.loading,type:"primary"},on:{click:t.doSubmit}},[t._v("确认")])],1),t._v(" "),i("el-dialog",{attrs:{visible:t.dialogTableVisible,"append-to-body":""},on:{"update:visible":function(e){t.dialogTableVisible=e}}},[i("el-table",{attrs:{"highlight-current-row":"",data:t.managers},on:{"row-dblclick":t.selectTaskReceiver}},[i("el-table-column",{attrs:{property:"name",label:"姓名","show-overflow-tooltip":!0}}),t._v(" "),i("el-table-column",{attrs:{property:"task_type",label:"任务类型",filters:t.taskType,"filter-method":t.filterHandler}}),t._v(" "),i("el-table-column",{attrs:{property:"task_name",label:"任务名称"}}),t._v(" "),i("el-table-column",{attrs:{property:"end_time",sortable:"",label:"结束时间"}}),t._v(" "),i("el-table-column",{attrs:{property:"left_days",sortable:"",label:"剩余天数"}}),t._v(" "),i("el-table-column",{attrs:{property:"progress",sortable:"",label:"进度",width:"80"}}),t._v(" "),i("el-table-column",{attrs:{property:"task_status",label:"任务状态",filters:t.taskStatus,"filter-method":t.filterHandler,"show-overflow-tooltip":!0}}),t._v(" "),i("el-table-column",{attrs:{fixed:"right",label:"操作",width:"100"},scopedSlots:t._u([{key:"default",fn:function(e){return[i("el-button",{attrs:{type:"primary",size:"small"},on:{click:function(i){t.selectTaskReceiver(e.row)}}},[t._v("选择")])]}}])})],1)],1)],1)},[],!1,null,"17f13b54",null);c.options.__file="form.vue";e.default=c.exports},REHs:function(t,e,i){"use strict";var r=i("+Jyj");i.n(r).a},pMCq:function(t,e,i){}}]);