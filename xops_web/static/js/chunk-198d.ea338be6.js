(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-198d"],{"41Be":function(e,t,s){"use strict";s.d(t,"a",function(){return i});var n=s("Q2AE");function i(e){if(e&&e instanceof Array&&e.length>0){var t=e;return!!(n.a.getters&&n.a.getters.roles).some(function(e){return t.includes(e)})}return console.error("need roles! Like v-permission=\"['admin','editor']\""),!1}},iWqs:function(e,t,s){"use strict";s.r(t);var n=s("41Be"),i=s("/veO"),a={components:{eForm:s("fBsd").default},props:{query:{type:Object,required:!0}},data:function(){return{delLoading:!1,inboundLoading:!1,scanLoading:!1,statusOptions:[{key:"Succeed",display_name:"成功"},{key:"Failed",display_name:"失败"}],settings:{net_address:"",auth_type:"",ssh_username:"",ssh_password:"",ssh_port:"",ssh_private_key:"",commands:""},status:""}},mounted:function(){this.getSettings()},methods:{checkPermission:n.a,toQuery:function(){this.$parent.page=1,this.$parent.init()},to:function(){var e=this.$refs.form;e.form={net_address:String(this.settings.net_address),auth_type:this.settings.auth_type,ssh_username:this.settings.ssh_username,ssh_password:this.settings.ssh_password,ssh_port:this.settings.ssh_port,ssh_private_key:this.settings.ssh_private_key,commands:this.settings.commands},e.dialog=!0},getSettings:function(){var e=this;this.$nextTick(function(){Object(i.d)().then(function(t){e.settings=t.hosts})})},excuScan:function(){var e=this;this.scanLoading=!0,this.$nextTick(function(){Object(i.a)({excu:"scan"}).then(function(t){200===t.code?e.$message({showClose:!0,type:"success",message:t.detail,duration:3e3}):e.$message({showClose:!0,type:"error",message:t.detail,duration:3e3}),e.scanLoading=!1})})},excuInbound:function(){var e=this;this.$confirm("是否将扫描成功的设备入库?","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){e.inboundLoading=!0,Object(i.a)({excu:"inbound"}).then(function(t){200===t.code?e.$message({showClose:!0,type:"success",message:t.detail,duration:3e3}):e.$message({showClose:!0,type:"error",message:t.detail,duration:3e3}),e.inboundLoading=!1,e.$parent.init()})}).catch(function(){e.$message({type:"info",message:"取消操作"})})},getPtoggleSelect:function(){this.$parent.toggleSelection(this.$parent.data)},deleteSelect:function(){var e=this;if(this.$parent.multipleSelection){var t=this.$parent.multipleSelection.length;this.$confirm("此操作将删除"+t+"条数据, 是否继续?","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){e.$parent.doSelectionDel(),e.$message({type:"success",message:"删除成功!"})}).catch(function(){e.$message({type:"info",message:"已取消删除"})})}else this.$message({type:"info",message:"请先选择数据"})},refresh:function(){this.$parent.init()},formatJson:function(e,t){return t.map(function(t){return e.map(function(e){return"Succeed"===e?t[e]?"成功":"失败":t[e]})})}}},o=s("KHd+"),r=Object(o.a)(a,function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",{staticClass:"head-container"},[s("el-input",{staticClass:"filter-item",staticStyle:{width:"200px"},attrs:{clearable:"",placeholder:"输入主机名/IP/域名搜索"},nativeOn:{keyup:function(t){return"button"in t||!e._k(t.keyCode,"enter",13,t.key,"Enter")?e.toQuery(t):null}},model:{value:e.query.value,callback:function(t){e.$set(e.query,"value",t)},expression:"query.value"}}),e._v(" "),s("el-select",{staticClass:"filter-item",staticStyle:{width:"90px"},attrs:{clearable:"",placeholder:"状态",value:""},on:{change:e.toQuery},model:{value:e.query.status,callback:function(t){e.$set(e.query,"status",t)},expression:"query.status"}},e._l(e.statusOptions,function(e){return s("el-option",{key:e.key,attrs:{label:e.display_name,value:e.key}})})),e._v(" "),s("el-button",{staticClass:"filter-item",attrs:{size:"mini",type:"primary",icon:"el-icon-search"},on:{click:e.toQuery}},[e._v("搜索\n  ")]),e._v(" "),s("div",{staticStyle:{display:"inline-block",margin:"0 2px"}},[e.checkPermission(["admin","scan_all"])?s("el-button-group",[s("el-button",{staticClass:"filter-item",attrs:{size:"mini",type:"primary"},on:{click:e.getPtoggleSelect}},[e._v("全选")]),e._v(" "),s("el-button",{staticClass:"filter-item",attrs:{size:"mini",type:"danger"},on:{click:e.deleteSelect}},[e._v("删除")]),e._v(" "),s("el-button",{staticClass:"filter-item",attrs:{size:"mini",type:"primary"},on:{click:e.refresh}},[e._v("刷新")])],1):e._e()],1),e._v(" "),s("div",{staticStyle:{display:"inline-block",margin:"0 0",float:"right"}},[e.checkPermission(["admin","scan_all"])?s("el-button-group",[s("el-button",{staticClass:"filter-item",attrs:{size:"mini",type:"primary",icon:"el-icon-plus"},on:{click:e.to}},[e._v("扫描设置\n      ")]),e._v(" "),s("el-button",{staticClass:"filter-item",attrs:{loading:e.inboundLoading,size:"mini",type:"success",icon:"el-icon-plus"},on:{click:e.excuInbound}},[e._v("全部入库\n      ")]),e._v(" "),s("el-button",{staticClass:"filter-item",attrs:{loading:e.scanLoading,size:"mini",type:"warning",icon:"el-icon-plus"},on:{click:e.excuScan}},[e._v("执行扫描\n      ")])],1):e._e(),e._v(" "),s("eForm",{ref:"form"})],1)],1)},[],!1,null,null,null);r.options.__file="header.vue";t.default=r.exports}}]);