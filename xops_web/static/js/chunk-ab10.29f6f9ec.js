(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-ab10"],{"6oA6":function(t,e,r){},OSA2:function(t,e,r){"use strict";var n=r("6oA6");r.n(n).a},l9Yl:function(t,e,r){"use strict";r.d(e,"a",function(){return o}),r.d(e,"e",function(){return a}),r.d(e,"g",function(){return i}),r.d(e,"n",function(){return u}),r.d(e,"j",function(){return c}),r.d(e,"s",function(){return s}),r.d(e,"r",function(){return l}),r.d(e,"q",function(){return d}),r.d(e,"p",function(){return m}),r.d(e,"v",function(){return p}),r.d(e,"u",function(){return f}),r.d(e,"t",function(){return h}),r.d(e,"w",function(){return b}),r.d(e,"m",function(){return g}),r.d(e,"f",function(){return v}),r.d(e,"i",function(){return j}),r.d(e,"b",function(){return y}),r.d(e,"k",function(){return O}),r.d(e,"l",function(){return _}),r.d(e,"d",function(){return k}),r.d(e,"c",function(){return w}),r.d(e,"h",function(){return x}),r.d(e,"o",function(){return A});var n=r("t3Un");function o(t){return Object(n.a)({url:"api/v1/art_projects/",method:"post",data:t})}function a(t){return Object(n.a)({url:"api/v1/art_projects/"+t+"/",method:"delete"})}function i(t,e){return Object(n.a)({url:"api/v1/art_projects/"+t+"/",method:"put",data:e})}function u(){return Object(n.a)({url:"api/v1/project/receivers",method:"get"})}function c(){return Object(n.a)({url:"api/v1/project/auditors",method:"get"})}function s(t){return Object(n.a)({url:"api/v1/project/audit/submit",method:"post",data:t})}function l(t){return Object(n.a)({url:"api/v1/project/audit/reject",method:"post",data:t})}function d(t){return Object(n.a)({url:"api/v1/project/audit/pass",method:"post",data:t})}function m(t){return Object(n.a)({url:"api/v1/project/accept",method:"post",data:t})}function p(t){return Object(n.a)({url:"api/v1/project/check/submit",method:"post",data:t})}function f(t){return Object(n.a)({url:"api/v1/project/check/reject",method:"post",data:t})}function h(t){return Object(n.a)({url:"api/v1/project/check/pass",method:"post",data:t})}function b(t){return Object(n.a)({url:"api/v1/project/reject",method:"post",data:t})}function g(t){return Object(n.a)({url:"/api/v1/project_fee",method:"get",params:t})}function v(t){return Object(n.a)({url:"/api/v1/project_fee/"+t+"/",method:"delete"})}function j(t,e){return Object(n.a)({url:"/api/v1/project_fee/"+t+"/",method:"put",data:e})}function y(t){return Object(n.a)({url:"/api/v1/project_fee/",method:"post",data:t})}function O(t){return Object(n.a)({url:"/api/v1/project/cost/analysis",method:"get",params:t})}function _(t){return Object(n.a)({url:"/api/v1/project/fee/cost/analysis",method:"get",params:t})}function k(t){return Object(n.a)({url:"api/v1/project/cost/analysis/finished",method:"post",data:t})}function w(t){return Object(n.a)({url:"api/v1/points/assignment",method:"post",data:t})}function x(t,e){return Object(n.a)({url:"/points/"+t+"/",method:"put",data:e,isMock:!0})}function A(){return Object(n.a)({url:"/api/v1/project_statuses",method:"get"})}},"u/rA":function(t,e,r){"use strict";r.r(e);var n=r("l9Yl"),o={props:{isAdd:{type:Boolean,required:!0},sup_this:{type:Object,default:null},data:{type:Object,default:null}},data:function(){return{managers:[],loading:!1,dialog:!1,form:{name:"",style:"",customer:"",manager:null,period:[]},rules:{name:[{required:!0,message:"请输入项目名称",trigger:"blur"}],style:[{required:!0,message:"请输入项目风格",trigger:"blur"}],customer:[{required:!0,message:"请输入客户名称",trigger:"blur"}],period:[{required:!0,message:"请输入项目完成时间范围",trigger:"blur"}]}}},methods:{cancel:function(){this.resetForm()},doSubmit:function(){var t=this;this.$refs.form.validate(function(e){if(!e)return!1;t.loading=!0,t.isAdd?t.doAdd():t.doEdit()})},doAdd:function(){var t=this,e={name:this.form.name,style:this.form.style,customer:this.form.customer,begin_time:this.form.period[0],end_time:this.form.period[1],receiver:this.form.manager};Object(n.a)(e).then(function(e){t.resetForm(),t.$message({showClose:!0,type:"success",message:"添加成功!",duration:2500}),t.loading=!1,t.$parent.$parent.init()}).catch(function(e){t.loading=!1,console.log(e)})},doEdit:function(){var t=this,e={name:this.form.name,style:this.form.style,customer:this.form.customer,begin_time:this.form.period[0],end_time:this.form.period[1],receiver:this.form.manager};this.data&&this.data.receiver&&this.form.manager===this.data.receiver.name&&(e.receiver=this.data.receiver.id),Object(n.g)(this.form.id,e).then(function(e){t.resetForm(),t.$message({showClose:!0,type:"success",message:"修改成功!",duration:2500}),t.loading=!1,t.sup_this.init()}).catch(function(e){t.loading=!1,console.log(e)})},resetForm:function(){this.dialog=!1,this.$refs.form.resetFields(),this.form={}},getAllProjectManagers:function(){var t=this;Object(n.n)().then(function(e){t.managers=e})},open:function(){this.getAllProjectManagers()}}},a=(r("OSA2"),r("KHd+")),i=Object(a.a)(o,function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("el-dialog",{attrs:{width:"480px","append-to-body":!0,visible:t.dialog,title:t.isAdd?"新增项目":"编辑项目"},on:{"update:visible":function(e){t.dialog=e},open:t.open}},[r("el-form",{ref:"form",attrs:{size:"small","label-width":"96px",model:t.form,rules:t.rules}},[r("el-form-item",{attrs:{label:"项目名称",prop:"name"}},[r("el-input",{staticStyle:{width:"338px"},model:{value:t.form.name,callback:function(e){t.$set(t.form,"name",e)},expression:"form.name"}})],1),t._v(" "),r("el-form-item",{attrs:{label:"风格",prop:"style"}},[r("el-input",{staticStyle:{width:"338px"},model:{value:t.form.style,callback:function(e){t.$set(t.form,"style",e)},expression:"form.style"}})],1),t._v(" "),r("el-form-item",{attrs:{label:"客户",prop:"customer"}},[r("el-input",{staticStyle:{width:"338px"},model:{value:t.form.customer,callback:function(e){t.$set(t.form,"customer",e)},expression:"form.customer"}})],1),t._v(" "),r("el-form-item",{attrs:{label:"项目负责人",prop:"manager"}},[r("el-select",{staticStyle:{width:"338px"},attrs:{placeholder:"请选择",clearable:"",value:""},model:{value:t.form.manager,callback:function(e){t.$set(t.form,"manager",e)},expression:"form.manager"}},t._l(t.managers,function(t){return r("el-option",{key:t.id,attrs:{label:t.name,value:t.id}})}))],1),t._v(" "),r("el-form-item",{attrs:{label:"时间范围",prop:"period"}},[r("el-date-picker",{staticStyle:{width:"338px"},attrs:{type:"daterange","range-separator":"至","start-placeholder":"开始日期","end-placeholder":"结束日期","value-format":"yyyy-MM-dd"},model:{value:t.form.period,callback:function(e){t.$set(t.form,"period",e)},expression:"form.period"}})],1)],1),t._v(" "),r("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[r("el-button",{attrs:{type:"text"},on:{click:t.cancel}},[t._v("取消")]),t._v(" "),r("el-button",{attrs:{loading:t.loading,type:"primary"},on:{click:t.doSubmit}},[t._v("确认")])],1)],1)},[],!1,null,"8d80409c",null);i.options.__file="form.vue";e.default=i.exports}}]);