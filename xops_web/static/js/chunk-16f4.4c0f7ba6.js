(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-16f4","chunk-4d81","chunk-73b2","chunk-29bb","chunk-5c9a"],{"30h1":function(e,t,a){"use strict";var n=a("Y+P3");a.n(n).a},"41Be":function(e,t,a){"use strict";a.d(t,"a",function(){return i});var n=a("Q2AE");function i(e){if(e&&e instanceof Array&&e.length>0){var t=e;return!!(n.a.getters&&n.a.getters.roles).some(function(e){return t.includes(e)})}return console.error("need roles! Like v-permission=\"['admin','editor']\""),!1}},"6U1x":function(e,t,a){"use strict";var n=a("HK8/");a.n(n).a},"8KlD":function(e,t,a){"use strict";var n=a("NluS");a.n(n).a},ASsF:function(e,t,a){},FplJ:function(e,t,a){"use strict";a.r(t);var n=a("41Be"),i=a("qc7c"),l=a("PL5b"),s=a("g8L3"),r=a("m6M2"),c=(a("ySi6"),{name:"step_file_preview",inheritAttrs:!1,props:{file:{type:Object,required:!0},actives:{type:Array,default:function(){return["1"]}},feedbacks:{type:Array,default:function(){return[]}}},components:{step_feedback_form:i.default,image_preview:l.a,rte_preview:s.a,step_file_feedback_log:r.default},data:function(){return{activeNames:["1"]}},watch:{actives:function(){this.activeNames=this.actives},file:{deep:!0,handler:function(){}}},methods:{checkPermission:n.a,handleDownload:function(){},init:function(){this.feedbacks=[]}},created:function(){this.activeNames=this.actives}}),o=(a("6U1x"),a("KHd+")),f=Object(o.a)(c,function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"step-file-preview"},[a("el-collapse",{model:{value:e.activeNames,callback:function(t){e.activeNames=t},expression:"activeNames"}},[a("el-collapse-item",{staticClass:"preview",attrs:{name:"1"}},[a("template",{slot:"title"},[e._v("\n        预览\n        "),a("el-button",{staticClass:"download",attrs:{type:"text",size:"mini"},on:{click:function(t){return t.stopPropagation(),e.handleDownload(t)}}},[1===e.file.type?a("a",{attrs:{target:"_blank",href:e.file.path,download:e.file.name}},[e._v("下载\n          ")]):e._e()])],1),e._v(" "),a("div",[e.file.path?a("image_preview",{attrs:{src:e.file.path}}):e._e(),e._v(" "),e.file.content?a("rte_preview",{attrs:{content:e.file.content}}):e._e()],1)],2),e._v(" "),e.checkPermission(["admin","step_all","step_feedback_submit"])?a("el-collapse-item",{attrs:{name:"2"}},[a("template",{slot:"title"},[e._v("\n        提交反馈\n      ")]),e._v(" "),a("div",{staticClass:"feedback"},[a("step_feedback_form",e._g({attrs:{file:e.file,file_id:e.file.id}},e.$listeners))],1)],2):e._e(),e._v(" "),a("el-collapse-item",{attrs:{name:"3"}},[a("template",{slot:"title"},[e._v("\n        反馈历史"),a("i",{staticClass:"header-icon el-icon-info"})]),e._v(" "),a("div",{staticClass:"feedback"},[a("step_file_feedback_log",{attrs:{feedbacks:e.feedbacks}})],1)],2)],1)],1)},[],!1,null,"7409586b",null);f.options.__file="step_file_preview.vue";t.default=f.exports},"HK8/":function(e,t,a){},NluS:function(e,t,a){},NrYw:function(e,t,a){},SuGE:function(e,t,a){"use strict";var n=a("NrYw");a.n(n).a},UmRJ:function(e,t,a){"use strict";a.r(t);var n=a("PL5b"),i=a("g8L3"),l={name:"step_file_feedback_preview",props:{file:{type:Object,required:!0}},components:{image_preview:n.a,rte_preview:i.a},data:function(){return{feedbacks:[]}},watch:{file:{deep:!0,handler:function(){}}},methods:{handleDownload:function(){}},created:function(){}},s=(a("30h1"),a("KHd+")),r=Object(s.a)(l,function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"step-file-preview"},[a("el-button",{staticClass:"download",attrs:{type:"text",size:"mini"},on:{click:function(t){return t.stopPropagation(),e.handleDownload(t)}}},[1===e.file.type?a("a",{attrs:{target:"_blank",href:e.file.path,download:e.file.name}},[e._v("下载\n    ")]):e._e()]),e._v(" "),a("div",[1===e.file.type?a("image_preview",{attrs:{src:e.file.path}}):a("rte_preview",{attrs:{content:e.file.content}})],1)],1)},[],!1,null,"60514e96",null);r.options.__file="step_file_feedback_preview.vue";t.default=r.exports},"Y+P3":function(e,t,a){},Zdsn:function(e,t,a){"use strict";var n=a("ASsF");a.n(n).a},m6M2:function(e,t,a){"use strict";a.r(t);var n={name:"step_file_feedback_log",components:{step_feedback_file_table:a("xtGO").default},props:{feedbacks:{type:Array,default:function(){return[]}}},data:function(){return{activeNames:["1","2"]}},methods:{handleChange:function(){}}},i=(a("8KlD"),a("KHd+")),l=Object(i.a)(n,function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"block"},[a("div",{staticClass:"feedback-log"},[a("el-timeline",{staticClass:"feedback-timeline"},e._l(e.feedbacks,function(t,n){return a("el-timeline-item",{key:t.id,staticClass:"log-item",attrs:{timestamp:t.add_time,placement:"top",type:0===n?"primary":""}},[a("el-collapse",{on:{change:e.handleChange}},[a("el-card",[a("el-collapse",{staticClass:"outer-el-collapse",attrs:{accordion:""}},[a("el-collapse-item",{staticClass:"step-el-collapse-item"},[a("template",{staticClass:"log-item-detail",slot:"title"},[a("h4",[e._v(e._s(t.title)),a("i",{staticClass:"header-icon el-icon-info"})]),e._v(" "),a("p",{staticClass:"desc"},[e._v(" 提交于 "+e._s(t.add_time))])]),e._v(" "),a("el-collapse",{staticClass:"inter-el-collapse",on:{change:e.handleChange},model:{value:e.activeNames,callback:function(t){e.activeNames=t},expression:"activeNames"}},[a("el-collapse-item",{attrs:{title:"文件",name:"1"}},[a("step_feedback_file_table",{attrs:{files:t.files}})],1),e._v(" "),a("el-collapse-item",{attrs:{title:"备注",name:"2"}},[a("div",[e._v(e._s(t.memo))])])],1)],2)],1)],1)],1)],1)}))],1)])},[],!1,null,"309412ec",null);l.options.__file="step_file_feedback_log.vue";t.default=l.exports},qc7c:function(e,t,a){"use strict";a.r(t);var n=a("KglX"),i=a("ySi6"),l={name:"step_feedback_form",components:{Feedback:n.a},props:{file:{type:Object,required:!0}},data:function(){return{feedbackUpdateForm:{title:"",type:0,files:[],content:"",memo:""},feedbackUpdateRuleForm:{title:[{required:!0,message:"请输入标题",trigger:"blur"},{min:2,max:20,message:"长度在 2 到 20 个字符",trigger:"blur"}]}}},methods:{getFiles:function(e){e&&(this.feedbackUpdateForm.files=e)},getRTEContent:function(e){e&&(this.feedbackUpdateForm.content=e)},getFileType:function(e){e&&(this.feedbackUpdateForm.type=e)},handleCancelFeedback:function(){var e=this;this.$confirm("此操作将会重置当前表单并删除已上传的文件, 是否继续?","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){e.$message({type:"success",message:"已重置当前表单"})}).catch(function(){})},handleSubmitFeedback:function(){var e=this,t={};t.title=this.feedbackUpdateForm.title,t.type=this.file.type,t.memo=this.feedbackUpdateForm.memo,t.step_log_file_id=this.file.id,this.feedbackUpdateForm.files&&this.feedbackUpdateForm.files.length>0&&(t.files=this.feedbackUpdateForm.files.map(function(e){return e.url=e.raw_url||e.url,e})),this.feedbackUpdateForm.content&&(t.content=this.feedbackUpdateForm.content),this.$refs.feedbackUpdateValidateForm.validate(function(a){if(!a)return!1;Object(i.f)(t).then(function(t){200===t.code?(e.$message.success("反馈提交成功"),e.$refs.feedbackUpdateValidateForm.resetFields(),e.$listeners.getFeedbackLog(e.file),e.$refs.feedback.init()):console.log(t)}).catch(function(e){console.log(e)})})}}},s=(a("SuGE"),a("KHd+")),r=Object(s.a)(l,function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("el-form",{ref:"feedbackUpdateValidateForm",attrs:{model:e.feedbackUpdateForm,rules:e.feedbackUpdateRuleForm}},[a("el-form-item",{attrs:{prop:"title",label:"标题","label-width":"80px"}},[a("el-input",{attrs:{type:"text",placeholder:""},model:{value:e.feedbackUpdateForm.title,callback:function(t){e.$set(e.feedbackUpdateForm,"title",t)},expression:"feedbackUpdateForm.title"}})],1),e._v(" "),a("el-form-item",{attrs:{prop:"",label:"上传文件","label-width":"80px"}},[a("Feedback",{ref:"feedback",attrs:{files:e.feedbackUpdateForm.files,content:e.feedbackUpdateForm.content},on:{getFiles:e.getFiles,getRTEContent:e.getRTEContent,getFileType:e.getFileType}})],1),e._v(" "),a("el-form-item",{attrs:{prop:"memo",label:"备注","label-width":"80px"}},[a("el-input",{attrs:{type:"textarea",rows:1,placeholder:"备注"},model:{value:e.feedbackUpdateForm.memo,callback:function(t){e.$set(e.feedbackUpdateForm,"memo",t)},expression:"feedbackUpdateForm.memo"}})],1),e._v(" "),a("div",{staticClass:"footer"},[a("el-button",{on:{click:e.handleCancelFeedback}},[e._v("取 消")]),e._v(" "),a("el-button",{attrs:{type:"primary"},on:{click:e.handleSubmitFeedback}},[e._v("提 交")])],1)],1)},[],!1,null,"a22c0402",null);r.options.__file="step_feedback_form.vue";t.default=r.exports},xtGO:function(e,t,a){"use strict";a.r(t);var n=a("UmRJ"),i=a("KglX"),l=a("PL5b"),s=a("g8L3"),r={name:"step_feedback_file_table",components:{Feedback:i.a,image_preview:l.a,rte_preview:s.a,step_file_feedback_preview:n.default},props:{files:{type:Array,default:function(){return[]}}},data:function(){return{expands:[],src:"",type:"",content:"",file:""}},methods:{handlePreview:function(e){var t=window.open("","预览","width=500, height=300");1===e.type?t.document.write('<img src="'+e.path+'" alt=""/>'):0===e.type&&t.document.write(e.content)},getRowKeys:function(e){return e.name+e.id},handleExpandChange:function(e,t){var a=this;t.length>1&&this.files.forEach(function(t){t.id!==e.id&&a.$refs.tables.toggleRowExpansion(t,!1)})},handleRowClick:function(e,t,a){this.$refs.tables.toggleRowExpansion(e)}}},c=(a("Zdsn"),a("KHd+")),o=Object(c.a)(r,function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("el-table",{ref:"tables",staticStyle:{width:"100%"},attrs:{data:e.files,border:"","highlight-current-row":"",size:"small",fit:"","expand-row-keys":e.expands,"row-key":e.getRowKeys},on:{"expand-change":e.handleExpandChange,"row-click":e.handleRowClick}},[a("el-table-column",{attrs:{type:"expand"},scopedSlots:e._u([{key:"default",fn:function(e){return[a("div",[a("step_file_feedback_preview",{attrs:{file:e.row}})],1)]}}])}),e._v(" "),a("el-table-column",{attrs:{prop:"name",label:"文件名"}}),e._v(" "),a("el-table-column",{attrs:{prop:"type_name",label:"类型"}}),e._v(" "),a("el-table-column",{attrs:{prop:"add_time",label:"提交时间"}}),e._v(" "),a("el-table-column",{attrs:{label:"操作"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-button",{attrs:{type:"text",size:"small"},on:{click:function(a){a.stopPropagation(),e.handlePreview(t.row)}}},[e._v("预览")])]}}])})],1)],1)},[],!1,null,"40284880",null);o.options.__file="step_feedback_file_table.vue";t.default=o.exports},ySi6:function(e,t,a){"use strict";a.d(t,"a",function(){return i}),a.d(t,"b",function(){return l}),a.d(t,"c",function(){return s}),a.d(t,"g",function(){return r}),a.d(t,"e",function(){return c}),a.d(t,"d",function(){return o}),a.d(t,"f",function(){return f});var n=a("t3Un");function i(e){return Object(n.a)({url:"api/v1/steps/",method:"post",data:e})}function l(e){return Object(n.a)({url:"api/v1/steps/"+e+"/",method:"delete"})}function s(e,t){return Object(n.a)({url:"api/v1/steps/"+e+"/",method:"put",data:t})}function r(e){return Object(n.a)({url:"api/v1/step/progress/update",method:"post",data:e})}function c(e){return Object(n.a)({url:"api/v1/step/progress/log",method:"get",params:e})}function o(e){return Object(n.a)({url:"api/v1/step/file/feedback/log",method:"get",params:e})}function f(e){return Object(n.a)({url:"api/v1/step/file/feedback/submit",method:"post",data:e})}}}]);