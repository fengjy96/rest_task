(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-4333","chunk-9ad0","chunk-1d00","chunk-db1d"],{"278r":function(t,e,n){"use strict";var i=n("8YkG");n.n(i).a},"2sDi":function(t,e,n){"use strict";var i=n("JQpr");n.n(i).a},"3ADX":function(t,e,n){"use strict";var i=n("14Xm"),a=n.n(i),r=n("4d7F"),o=n.n(r),s=n("D3Ub"),l=n.n(s),c=n("t3Un");function u(t,e,n){return Object(c.a)({url:t,method:"get",params:e,isMock:n})}var d=n("LvDl"),p=n.n(d);e.a={data:function(){return{loading:!0,rawData:[],data:[],page:1,size:10,total:0,url:"",params:{},query:{},time:170}},methods:{init:p.a.throttle(function(){var t=l()(a.a.mark(function t(){var e=this,n=arguments.length>0&&void 0!==arguments[0]&&arguments[0];return a.a.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,this.beforeInit();case 2:if(t.sent){t.next=4;break}return t.abrupt("return");case 4:return t.abrupt("return",new o.a(function(t,i){e.loading=!0,u(e.url,e.params,n).then(function(n){e.total=n.count,e.rawData=n.results,e.data=e.afterInit?e.afterInit(n.results):e.rawData,setTimeout(function(){e.loading=!1},e.time),t(n)}).catch(function(t){e.loading=!1,i(t)})}));case 5:case"end":return t.stop()}},t,this)}));return function(){return t.apply(this,arguments)}}(),1e3),beforeInit:function(){return!0},pageChange:function(t){this.page=t,this.init()},sizeChange:function(t){this.page=1,this.size=t,this.init()}}}},"41Be":function(t,e,n){"use strict";n.d(e,"a",function(){return a});var i=n("Q2AE");function a(t){if(t&&t instanceof Array&&t.length>0){var e=t;return!!(i.a.getters&&i.a.getters.roles).some(function(t){return e.includes(t)})}return console.error("need roles! Like v-permission=\"['admin','editor']\""),!1}},"6pS9":function(t,e,n){"use strict";n.d(e,"a",function(){return a}),n.d(e,"d",function(){return r}),n.d(e,"b",function(){return o}),n.d(e,"c",function(){return s});var i=n("t3Un");function a(t){return Object(i.a)({url:"api/connections/",method:"post",data:t})}function r(t){return Object(i.a)({url:"api/connections/"+t+"/",method:"get"})}function o(t){return Object(i.a)({url:"api/connections/"+t+"/",method:"delete"})}function s(t,e){return Object(i.a)({url:"api/connections/"+t+"/",method:"put",data:e})}},"8YkG":function(t,e,n){},DZVM:function(t,e,n){"use strict";n.r(e);var i={components:{eForm:n("JdTb").default},props:{data:{type:Object,required:!0},sup_this:{type:Object,required:!0},service_types:{type:Array,default:null}},methods:{to:function(){var t=this.$refs.form;t.form={id:this.data.id,hostname:this.data.hostname,auth_type:this.data.auth_type,username:this.data.username,password:this.data.password,is_public:this.data.is_public.toString(),port:this.data.port,desc:this.data.desc},t.dialog=!0}}},a=(n("2sDi"),n("KHd+")),r=Object(a.a)(i,function(){var t=this.$createElement,e=this._self._c||t;return e("div",[e("el-button",{attrs:{size:"mini",type:"success"},on:{click:this.to}},[this._v("编辑")]),this._v(" "),e("eForm",{ref:"form",attrs:{"is-add":!1,sup_this:this.sup_this,service_types:this.service_types}})],1)},[],!1,null,"6038eb2c",null);r.options.__file="edit.vue";e.default=r.exports},JQpr:function(t,e,n){},JdTb:function(t,e,n){"use strict";n.r(e);var i=n("6pS9"),a={props:{isAdd:{type:Boolean,required:!0},sup_this:{type:Object,default:null},service_types:{type:Array,default:null}},data:function(){return{loading:!1,dialog:!1,form:{id:"",hostname:"",auth_type:null,username:"",password:"",is_public:"false",port:0,desc:""},rules:{hostname:[{required:!0,message:"请输入IP/URL地址",trigger:"blur"}],auth_type:[{required:!0,message:"请选择服务类型",trigger:"blur"}],username:[{required:!0,message:"请输入用户名",trigger:"blur"}],password:[{required:!0,message:"请输入密码",trigger:"blur"}],is_public:[{required:!0,message:"是否要公开该密码",trigger:"blur"}]}}},methods:{cancel:function(){this.resetForm()},doSubmit:function(){var t=this;this.$refs.form.validate(function(e){if(!e)return!1;t.loading=!0,t.isAdd?t.doAdd():t.doEdit()})},doAdd:function(){var t=this;Object(i.a)(this.form).then(function(e){t.resetForm(),t.$message({showClose:!0,type:"success",message:"添加成功!",duration:2500}),t.loading=!1,t.$parent.$parent.init()}).catch(function(e){t.loading=!1,console.log(e)})},doEdit:function(){var t=this;Object(i.c)(this.form.id,this.form).then(function(e){t.resetForm(),t.$message({showClose:!0,type:"success",message:"修改成功!",duration:2500}),t.loading=!1,t.sup_this.init()}).catch(function(e){t.loading=!1,console.log(e)})},resetForm:function(){this.dialog=!1,this.$refs.form.resetFields(),this.form={hostname:"",auth_type:null,username:"",password:"",is_public:"false",port:0,desc:""}}}},r=(n("q3Lm"),n("KHd+")),o=Object(r.a)(a,function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("el-dialog",{attrs:{width:"550px","append-to-body":!0,visible:t.dialog,title:t.isAdd?"新增密码":"编辑密码"},on:{"update:visible":function(e){t.dialog=e}}},[n("el-form",{ref:"form",attrs:{model:t.form,rules:t.rules,size:"small","label-width":"100px"}},[n("el-form-item",{attrs:{label:"IP/URL",prop:"hostname"}},[n("el-input",{staticStyle:{width:"370px"},model:{value:t.form.hostname,callback:function(e){t.$set(t.form,"hostname",e)},expression:"form.hostname"}})],1),t._v(" "),n("el-form-item",{attrs:{label:"服务类型",prop:"auth_type"}},[n("el-select",{staticStyle:{width:"370px"},attrs:{placeholder:"请选择认证类型",value:""},model:{value:t.form.auth_type,callback:function(e){t.$set(t.form,"auth_type",e)},expression:"form.auth_type"}},t._l(t.service_types,function(t){return n("el-option",{key:t.key,attrs:{label:t.value,value:t.key}})}))],1),t._v(" "),n("el-form-item",{attrs:{label:"用户名",prop:"username"}},[n("el-input",{staticStyle:{width:"370px"},model:{value:t.form.username,callback:function(e){t.$set(t.form,"username",e)},expression:"form.username"}})],1),t._v(" "),n("el-form-item",{attrs:{label:"密码/KEY",prop:"password"}},[n("el-input",{staticStyle:{width:"370px"},model:{value:t.form.password,callback:function(e){t.$set(t.form,"password",e)},expression:"form.password"}})],1),t._v(" "),n("el-form-item",{attrs:{label:"是否公开",prop:"is_public"}},[n("el-radio",{attrs:{label:"true"},model:{value:t.form.is_public,callback:function(e){t.$set(t.form,"is_public",e)},expression:"form.is_public"}},[t._v("是")]),t._v(" "),n("el-radio",{attrs:{label:"false"},model:{value:t.form.is_public,callback:function(e){t.$set(t.form,"is_public",e)},expression:"form.is_public"}},[t._v("否")])],1),t._v(" "),n("el-form-item",{attrs:{label:"端口",prop:"port"}},[n("el-input",{staticStyle:{width:"370px"},model:{value:t.form.port,callback:function(e){t.$set(t.form,"port",e)},expression:"form.port"}})],1),t._v(" "),n("el-form-item",{attrs:{label:"备注"}},[n("el-input",{staticStyle:{width:"370px"},attrs:{rows:"4",type:"textarea"},model:{value:t.form.desc,callback:function(e){t.$set(t.form,"desc",e)},expression:"form.desc"}})],1)],1),t._v(" "),n("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[n("el-button",{attrs:{type:"text"},on:{click:t.cancel}},[t._v("取消")]),t._v(" "),n("el-button",{attrs:{loading:t.loading,type:"primary"},on:{click:t.doSubmit}},[t._v("确认")])],1)],1)},[],!1,null,"1ab9b83c",null);o.options.__file="form.vue";e.default=o.exports},PID8:function(t,e,n){"use strict";n.r(e);var i=n("4d7F"),a=n.n(i),r=n("41Be"),o=n("3ADX"),s=n("twU4"),l=n("6pS9"),c=n("Zg1K"),u=n("DZVM"),d={components:{eHeader:c.default,edit:u.default},mixins:[o.a],data:function(){return{delLoading:!1,sup_this:this,service_types:[]}},created:function(){var t=this;this.$nextTick(function(){t.init(Object(s.e)("SERVICE_TYPE").then(function(e){t.service_types=e[0].SERVICE_TYPE}))})},methods:{checkPermission:r.a,beforeInit:function(){this.url="api/connections/";var t=this.query.value;return this.params={page:this.page,size:this.size,ordering:"id"},t&&(this.params.search=t),!0},toggleSelection:function(t){var e=this;t&&(t.forEach(function(t){e.$refs.table.toggleRowSelection(t,!e.allSelect)}),this.allSelect=!this.allSelect)},handleSelectionChange:function(t){this.multipleSelection=t},doSelectionDel:function(){var t=this,e=[];this.multipleSelection.forEach(function(t,n){var i=Object(l.b)(t.id).catch(function(t){console.log(t)});e.push(i)}),a.a.all(e).then(function(e){t.init()})},subDelete:function(t){var e=this;this.delLoading=!0,Object(l.b)(t).then(function(n){e.delLoading=!1,e.$refs[t].doClose(),e.init(),e.$message({showClose:!0,type:"success",message:"删除成功!",duration:2500})}).catch(function(n){e.delLoading=!1,e.$refs[t].doClose(),console.log(n)})}}},p=(n("278r"),n("KHd+")),f=Object(p.a)(d,function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"app-container"},[n("eHeader",{attrs:{query:t.query,service_types:t.service_types}}),t._v(" "),n("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.loading,expression:"loading"}],ref:"table",staticStyle:{width:"100%"},attrs:{size:"small",border:"",data:t.data},on:{"selection-change":t.handleSelectionChange}},[n("el-table-column",{attrs:{type:"selection",width:"55",align:"center"}}),t._v(" "),n("el-table-column",{attrs:{label:"序号",width:"60",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[n("div",[t._v(t._s(e.$index+1))])]}}])}),t._v(" "),n("el-table-column",{attrs:{prop:"hostname",label:"IP/URL",width:"200"}}),t._v(" "),n("el-table-column",{attrs:{prop:"auth_type",label:"认证类型",width:"100"}}),t._v(" "),n("el-table-column",{attrs:{prop:"username",label:"用户名",width:"100"}}),t._v(" "),n("el-table-column",{attrs:{prop:"password",label:"密码"}}),t._v(" "),n("el-table-column",{attrs:{prop:"port",label:"端口",width:"80"}}),t._v(" "),n("el-table-column",{attrs:{prop:"uid_name",label:"所有者"}}),t._v(" "),n("el-table-column",{attrs:{label:"操作",width:"150px",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[t.checkPermission(["admin","connection_all","connection_edit"])?n("edit",{attrs:{data:e.row,sup_this:t.sup_this,service_types:t.service_types}}):t._e(),t._v(" "),t.checkPermission(["admin","connection_all","connection_delete"])?n("el-popover",{ref:e.row.id,attrs:{placement:"top",width:"180"}},[n("p",[t._v("确定删除本条数据吗？")]),t._v(" "),n("div",{staticStyle:{"text-align":"right",margin:"0"}},[n("el-button",{attrs:{size:"mini",type:"text"},on:{click:function(n){t.$refs[e.row.id].doClose()}}},[t._v("取消\n            ")]),t._v(" "),n("el-button",{attrs:{type:"primary",size:"mini",loading:t.delLoading},on:{click:function(n){t.subDelete(e.row.id)}}},[t._v("确定\n            ")])],1),t._v(" "),n("el-button",{attrs:{slot:"reference",type:"danger",size:"mini"},slot:"reference"},[t._v("删除")])],1):t._e()]}}])})],1),t._v(" "),n("el-pagination",{staticStyle:{"margin-top":"8px"},attrs:{layout:"total, prev, pager, next, sizes",total:t.total},on:{"size-change":t.sizeChange,"current-change":t.pageChange}})],1)},[],!1,null,"06300fbd",null);f.options.__file="index.vue";e.default=f.exports},Zg1K:function(t,e,n){"use strict";n.r(e);var i=n("41Be"),a={components:{eForm:n("JdTb").default},props:{query:{type:Object,required:!0},service_types:{type:Array,default:null}},data:function(){return{downloadLoading:!1}},methods:{checkPermission:i.a,toQuery:function(){this.$parent.page=1,this.$parent.init()},add:function(){this.$refs.form.dialog=!0},getPtoggleSelect:function(){this.$parent.toggleSelection(this.$parent.data)},deleteSelect:function(){var t=this;if(this.$parent.multipleSelection){var e=this.$parent.multipleSelection.length;this.$confirm("此操作将删除"+e+"条数据, 是否继续?","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){t.$parent.doSelectionDel(),t.$message({type:"success",message:"删除成功!"})}).catch(function(){t.$message({type:"info",message:"已取消删除"})})}else this.$message({type:"info",message:"请先选择数据"})},download:function(){var t=this;this.downloadLoading=!0,Promise.all([n.e("chunk-ef4a"),n.e("chunk-54ca")]).then(n.bind(null,"S/jZ")).then(function(e){var n=t.formatJson(["id","hostname","auth_type","username","password","port","user_name","desc","is_public"],t.$parent.data);e.export_json_to_excel({header:["ID","IP/URL","认证类型","用户名","密码","端口","备注"],data:n,filename:"table-list"}),t.downloadLoading=!1})},formatJson:function(t,e){return e.map(function(e){return t.map(function(t){return e[t]})})}}},r=n("KHd+"),o=Object(r.a)(a,function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"head-container"},[n("el-input",{staticClass:"filter-item",staticStyle:{width:"200px"},attrs:{clearable:"",placeholder:"输入名称搜索"},nativeOn:{keyup:function(e){return"button"in e||!t._k(e.keyCode,"enter",13,e.key,"Enter")?t.toQuery(e):null}},model:{value:t.query.value,callback:function(e){t.$set(t.query,"value",e)},expression:"query.value"}}),t._v(" "),n("el-button",{staticClass:"filter-item",attrs:{size:"mini",type:"primary",icon:"el-icon-search"},on:{click:t.toQuery}},[t._v("搜索\n  ")]),t._v(" "),n("div",{staticStyle:{display:"inline-block",margin:"10px 2px"}},[n("el-button-group",[t.checkPermission(["admin","connection_all","connection_delete"])?n("el-button",{staticClass:"filter-item",attrs:{size:"mini",type:"primary"},on:{click:t.getPtoggleSelect}},[t._v("全选\n      ")]):t._e(),t._v(" "),t.checkPermission(["admin","connection_all","connection_delete"])?n("el-button",{staticClass:"filter-item",attrs:{size:"mini",type:"danger"},on:{click:t.deleteSelect}},[t._v("删除\n      ")]):t._e(),t._v(" "),t.checkPermission(["admin","connection_all","connection_create"])?n("el-button",{staticClass:"filter-item",attrs:{size:"mini",type:"primary"},on:{click:t.add}},[t._v("创建\n      ")]):t._e()],1),t._v(" "),n("eForm",{ref:"form",attrs:{"is-add":!0,service_types:t.service_types}})],1),t._v(" "),t.checkPermission(["admin"])?n("el-button",{staticClass:"filter-item",staticStyle:{display:"inline-block",margin:"0 20px",float:"right"},attrs:{loading:t.downloadLoading,size:"mini",type:"primary",icon:"el-icon-download"},on:{click:t.download}},[t._v("导出\n  ")]):t._e()],1)},[],!1,null,null,null);o.options.__file="header.vue";e.default=o.exports},q3Lm:function(t,e,n){"use strict";var i=n("sCTt");n.n(i).a},sCTt:function(t,e,n){},twU4:function(t,e,n){"use strict";n.d(e,"d",function(){return a}),n.d(e,"a",function(){return r}),n.d(e,"b",function(){return o}),n.d(e,"c",function(){return s}),n.d(e,"e",function(){return l});var i=n("t3Un");function a(){return Object(i.a)({url:"api/dict/tree/",method:"get"})}function r(t){return Object(i.a)({url:"api/dicts/",method:"post",data:t})}function o(t){return Object(i.a)({url:"api/dicts/"+t+"/",method:"delete"})}function s(t,e){return Object(i.a)({url:"api/dicts/"+t+"/",method:"put",data:e})}function l(){for(var t=arguments.length,e=Array(t),n=0;n<t;n++)e[n]=arguments[n];return Object(i.a)({url:"api/dicts/?&key="+e,method:"get"})}}}]);