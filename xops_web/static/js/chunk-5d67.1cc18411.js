(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-5d67","chunk-2d8d","chunk-4b92","chunk-38d6","chunk-8d2c"],{"/xFh":function(e,t,r){},"02iu":function(e,t,r){"use strict";r.d(t,"d",function(){return a}),r.d(t,"e",function(){return n}),r.d(t,"a",function(){return s}),r.d(t,"b",function(){return o}),r.d(t,"c",function(){return l});var i=r("t3Un");function a(){return Object(i.a)({url:"api/organization/tree/",method:"get"})}function n(){return Object(i.a)({url:"api/organization/user/tree/",method:"get"})}function s(e){return Object(i.a)({url:"api/organizations/",method:"post",data:e})}function o(e){return Object(i.a)({url:"api/organizations/"+e+"/",method:"delete"})}function l(e,t){return Object(i.a)({url:"api/organizations/"+e+"/",method:"put",data:t})}},"25vb":function(e,t,r){"use strict";var i=r("e8rh");r.n(i).a},"2Bqp":function(e,t,r){"use strict";var i=r("/xFh");r.n(i).a},"2KYm":function(e,t,r){"use strict";var i=r("EYJg");r.n(i).a},"3ADX":function(e,t,r){"use strict";var i=r("14Xm"),a=r.n(i),n=r("4d7F"),s=r.n(n),o=r("D3Ub"),l=r.n(o),u=r("t3Un");function c(e,t,r){return Object(u.a)({url:e,method:"get",params:t,isMock:r})}var d=r("LvDl"),p=r.n(d);t.a={data:function(){return{loading:!0,rawData:[],data:[],page:1,size:10,total:0,url:"",params:{},query:{},time:170}},methods:{init:p.a.throttle(function(){var e=l()(a.a.mark(function e(){var t=this,r=arguments.length>0&&void 0!==arguments[0]&&arguments[0];return a.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,this.beforeInit();case 2:if(e.sent){e.next=4;break}return e.abrupt("return");case 4:return e.abrupt("return",new s.a(function(e,i){t.loading=!0,c(t.url,t.params,r).then(function(r){t.total=r.count,t.rawData=r.results,t.data=t.afterInit?t.afterInit(r.results):t.rawData,setTimeout(function(){t.loading=!1},t.time),e(r)}).catch(function(e){t.loading=!1,i(e)})}));case 5:case"end":return e.stop()}},e,this)}));return function(){return e.apply(this,arguments)}}(),1e3),beforeInit:function(){return!0},pageChange:function(e){this.page=e,this.init()},sizeChange:function(e){this.page=1,this.size=e,this.init()}}}},"41Be":function(e,t,r){"use strict";r.d(t,"a",function(){return a});var i=r("Q2AE");function a(e){if(e&&e instanceof Array&&e.length>0){var t=e;return!!(i.a.getters&&i.a.getters.roles).some(function(e){return t.includes(e)})}return console.error("need roles! Like v-permission=\"['admin','editor']\""),!1}},EYJg:function(e,t,r){},Gqlf:function(e,t,r){},HzRm:function(e,t,r){"use strict";r.r(t);var i=r("QbLZ"),a=r.n(i),n=r("41Be"),s=r("3ADX"),o=r("wk8/"),l=r("zF5t"),u=r("02iu"),c=r("7Qib"),d=r("iM05"),p=r("YOUW"),m=r("fhgi"),f={components:{eHeader:d.default,edit:p.default,updatePass:m.default},mixins:[s.a],data:function(){return{roles:[],organizations:[],delLoading:!1,sup_this:this}},methods:{parseTime:c.b,checkPermission:n.a,beforeInit:function(){this.url="api/users/";var e=this.query,t=e.value,r=e.is_active;return this.params={page:this.page,size:this.size,ordering:"id"},""!==r&&null!==r&&(this.params.is_active=r),t&&(this.params.search=t),!0},subDelete:function(e){var t=this;this.delLoading=!0,Object(o.b)(e).then(function(r){t.delLoading=!1,t.$refs[e].doClose(),t.init(),t.$message({showClose:!0,type:"success",message:"删除成功!",duration:2500})}).catch(function(r){t.delLoading=!1,t.$refs[e].doClose(),console.log(r)})},getOrganizations:function(){var e=this;Object(u.d)().then(function(t){e.organizations=t.detail})},getRoleALL:function(){var e=this;Object(l.d)().then(function(t){e.roles=t.results.map(function(e){return a()({},e,{label:e.name})})})}},created:function(){var e=this;this.getRoleALL(),this.getOrganizations(),this.$nextTick(function(){e.init()})}},h=(r("2KYm"),r("KHd+")),b=Object(h.a)(f,function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"app-container"},[r("eHeader",{attrs:{roles:e.roles,organizations:e.organizations,query:e.query}}),e._v(" "),r("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],staticStyle:{width:"100%"},attrs:{size:"small",border:"",data:e.data}},[r("el-table-column",{attrs:{label:"头像",width:"50px"},scopedSlots:e._u([{key:"default",fn:function(e){return[r("img",{staticClass:"el-avatar",attrs:{alt:"",src:e.row.image}})]}}])}),e._v(" "),r("el-table-column",{attrs:{prop:"username",label:"用户名",width:"150px","show-overflow-tooltip":!0}}),e._v(" "),r("el-table-column",{attrs:{prop:"name",label:"姓名",width:"150px","show-overflow-tooltip":!0}}),e._v(" "),r("el-table-column",{attrs:{prop:"email",label:"邮箱"}}),e._v(" "),r("el-table-column",{attrs:{prop:"mobile",label:"手机号码",width:"100px"}}),e._v(" "),r("el-table-column",{attrs:{prop:"department.name",label:"部门",width:"100px"}}),e._v(" "),r("el-table-column",{attrs:{prop:"position",label:"职位",width:"100px"}}),e._v(" "),r("el-table-column",{attrs:{label:"状态",width:"50px"},scopedSlots:e._u([{key:"default",fn:function(t){return[r("span",[e._v(e._s(t.row.is_active?"激活":"锁定"))])]}}])}),e._v(" "),r("el-table-column",{attrs:{label:"操作",width:"220px",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[e.checkPermission(["admin","user_all","user_edit"])?r("edit",{attrs:{data:t.row,roles:e.roles,organizations:e.organizations,sup_this:e.sup_this}}):e._e(),e._v(" "),e.checkPermission(["admin","user_all"])?r("updatePass",{attrs:{data:t.row,sup_this:e.sup_this}}):e._e(),e._v(" "),e.checkPermission(["admin","user_all","user_delete"])?r("el-popover",{ref:t.row.id,attrs:{placement:"top",width:"180"}},[r("p",[e._v("确定删除本条数据吗？所有关联的数据将会被清除")]),e._v(" "),r("div",{staticStyle:{"text-align":"right",margin:"0"}},[r("el-button",{attrs:{size:"mini",type:"text"},on:{click:function(r){e.$refs[t.row.id].doClose()}}},[e._v("取消\n            ")]),e._v(" "),r("el-button",{attrs:{type:"primary",size:"mini",loading:e.delLoading},on:{click:function(r){e.subDelete(t.row.id)}}},[e._v("确定\n            ")])],1),e._v(" "),r("el-button",{attrs:{slot:"reference",type:"danger",size:"mini",disabled:1===t.row.id},slot:"reference"},[e._v("删除\n          ")])],1):e._e()]}}])})],1),e._v(" "),r("el-pagination",{staticStyle:{"margin-top":"8px"},attrs:{total:e.total,layout:"total, prev, pager, next, sizes"},on:{"size-change":e.sizeChange,"current-change":e.pageChange}})],1)},[],!1,null,"9650ea9a",null);b.options.__file="index.vue";t.default=b.exports},T4hH:function(e,t,r){"use strict";var i=r("Gqlf");r.n(i).a},YOUW:function(e,t,r){"use strict";r.r(t);var i=r("fIwS"),a=r("02iu"),n={components:{eForm:i.default},props:{organizations:{type:Array,required:!0},roles:{type:Array,required:!0},data:{type:Object,required:!0},sup_this:{type:Object,required:!0}},data:function(){return{orgusers:[]}},methods:{to:function(){var e=this,t=this.$refs.form;t.roleIds=[],t.skillIds=[];var r=null;null!==this.data.department&&(r=this.data.department.id);var i=null;null!==this.data.superior&&(i=this.data.superior.id),t.form={id:this.data.id,username:this.data.username,name:this.data.name,email:this.data.email,mobile:this.data.mobile,is_active:this.data.is_active.toString(),department:r,superior:i,position:this.data.position,roles:[],skills:[],base_salary:0},this.data.skills.forEach(function(e,r){t.skillIds.push(e.id)}),this.data.roles.forEach(function(e,r){t.roleIds.push(e.id)}),t.dialog=!0,Object(a.e)().then(function(t){e.orgusers=t.detail})}}},s=(r("25vb"),r("KHd+")),o=Object(s.a)(n,function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",[r("el-button",{attrs:{disabled:1===e.data.id,size:"mini",type:"success"},on:{click:e.to}},[e._v("编辑")]),e._v(" "),r("eForm",{ref:"form",attrs:{roles:e.roles,organizations:e.organizations,orgusers:e.orgusers,sup_this:e.sup_this,"is-add":!1}})],1)},[],!1,null,"faa441a4",null);o.options.__file="edit.vue";t.default=o.exports},Yfch:function(e,t,r){"use strict";function i(e){return/^1[3|4|5|7|8][0-9]\d{8}$/.test(e)}function a(e){return/^[a-zA-Z0-9_]+$/g.test(e)}r.d(t,"b",function(){return i}),r.d(t,"a",function(){return a})},e8rh:function(e,t,r){},fIwS:function(e,t,r){"use strict";r.r(t);var i=r("QbLZ"),a=r.n(i),n=r("wk8/"),s=r("cCY5"),o=r.n(s),l=(r("VCwm"),r("Yfch")),u=function(e,t,r){t?Object(l.b)(t)?r():r(new Error("请输入正确的11位手机号码")):r(new Error("请输入手机号码"))},c={name:"Form",components:{Treeselect:o.a},props:{organizations:{type:Array,required:!0},orgusers:{type:Array,required:!0},roles:{type:Array,required:!0},isAdd:{type:Boolean,required:!0},sup_this:{type:Object,default:null}},data:function(){return{dialog:!1,loading:!1,form:{username:"",name:"",mobile:"",department:null,superior:null,position:"",email:"",is_active:"false",roles:[],skills:[],base_salary:0},roleIds:[],skills:[],skillIds:[],rules:{username:[{required:!0,message:"请输入用户名",trigger:"blur"},{min:3,max:20,message:"长度在 3 到 20 个字符",trigger:"blur"}],name:[{required:!0,message:"姓名不能为空",trigger:"blur"}],email:[{message:"请输入邮箱地址",trigger:"blur",required:!0},{type:"email",message:"请输入正确的邮箱地址",trigger:"blur"}],mobile:[{required:!0,trigger:"blur",validator:u}],is_active:[{required:!0,message:"状态不能为空",trigger:"blur"}],base_salary:[]}}},methods:{cancel:function(){this.resetForm()},doSubmit:function(){var e=this;this.$refs.form.validate(function(t){if(!t)return!1;e.loading=!0,e.form.roles=[];var r=e;e.roleIds.forEach(function(e,t){r.form.roles.push(e)}),e.skillIds.forEach(function(e){r.form.skills.push(e)}),e.isAdd?e.doAdd():e.doEdit()})},doAdd:function(){var e=this;Object(n.a)(this.form).then(function(t){e.resetForm(),e.$message({showClose:!0,type:"success",message:"添加成功!默认密码123456!",duration:2500}),e.loading=!1,e.$parent.$parent.init()}).catch(function(t){e.loading=!1,console.log(t)})},doEdit:function(){var e=this;Object(n.c)(this.form.id,this.form).then(function(t){e.resetForm(),e.$message({showClose:!0,type:"success",message:"修改成功!",duration:2500}),e.loading=!1,e.sup_this.init()}).catch(function(t){e.loading=!1,console.log(t)})},resetForm:function(){this.dialog=!1,this.$refs.form.resetFields(),this.roleIds=[],this.skillIds=[],this.form={username:"",name:"",mobile:"",department:null,superior:null,position:"",email:"",is_active:"false",roles:[],skills:[],base_salary:0}},init:function(){this.getSkills()},getSkills:function(){var e=this.$store.state.task.types||[];this.skills=e.map(function(e){return a()({},e,{label:e.name})})}},created:function(){var e=this;this.$nextTick(function(){e.init()})}},d=(r("2Bqp"),r("KHd+")),p=Object(d.a)(c,function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("el-dialog",{attrs:{width:"850px","append-to-body":!0,visible:e.dialog,title:e.isAdd?"新增用户":"编辑用户"},on:{"update:visible":function(t){e.dialog=t}}},[r("el-form",{ref:"form",attrs:{model:e.form,rules:e.rules,size:"small","label-width":"80px"}},[r("el-row",[r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"用户名",prop:"username"}},[r("el-input",{staticStyle:{width:"300px"},attrs:{disabled:!1===e.isAdd},model:{value:e.form.username,callback:function(t){e.$set(e.form,"username",t)},expression:"form.username"}})],1)],1),e._v(" "),r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"姓名",prop:"name"}},[r("el-input",{staticStyle:{width:"300px"},model:{value:e.form.name,callback:function(t){e.$set(e.form,"name",t)},expression:"form.name"}})],1)],1)],1),e._v(" "),r("el-row",[r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"邮箱",prop:"email"}},[r("el-input",{staticStyle:{width:"300px"},model:{value:e.form.email,callback:function(t){e.$set(e.form,"email",t)},expression:"form.email"}})],1)],1),e._v(" "),r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"手机",prop:"mobile"}},[r("el-input",{staticStyle:{width:"300px"},model:{value:e.form.mobile,callback:function(t){e.$set(e.form,"mobile",t)},expression:"form.mobile"}})],1)],1)],1),e._v(" "),r("el-row",[r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"状态",prop:"is_active"}},[r("el-radio",{attrs:{label:"true"},model:{value:e.form.is_active,callback:function(t){e.$set(e.form,"is_active",t)},expression:"form.is_active"}},[e._v("激活")]),e._v(" "),r("el-radio",{attrs:{label:"false"},model:{value:e.form.is_active,callback:function(t){e.$set(e.form,"is_active",t)},expression:"form.is_active"}},[e._v("锁定")])],1)],1),e._v(" "),r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"部门"}},[r("treeselect",{staticStyle:{width:"300px"},attrs:{placeholder:"请选择部门",options:e.organizations},model:{value:e.form.department,callback:function(t){e.$set(e.form,"department",t)},expression:"form.department"}})],1)],1)],1),e._v(" "),r("el-row",[r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"职位",prop:"position"}},[r("el-input",{staticStyle:{width:"300px"},model:{value:e.form.position,callback:function(t){e.$set(e.form,"position",t)},expression:"form.position"}})],1)],1),e._v(" "),r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"上级主管"}},[r("treeselect",{staticStyle:{width:"300px"},attrs:{options:e.orgusers,"disable-branch-nodes":!0,placeholder:"请选择上级主管"},model:{value:e.form.superior,callback:function(t){e.$set(e.form,"superior",t)},expression:"form.superior"}})],1)],1)],1),e._v(" "),r("el-row",[r("el-col",{attrs:{span:12}},[r("el-form-item",{staticStyle:{"margin-bottom":"0"},attrs:{label:"基本工资"}},[r("el-input",{staticStyle:{width:"300px"},model:{value:e.form.base_salary,callback:function(t){e.$set(e.form,"base_salary",e._n(t))},expression:"form.base_salary"}})],1)],1),e._v(" "),r("el-col",{attrs:{span:12}},[r("el-form-item",{staticStyle:{"margin-bottom":"0"},attrs:{label:"角色"}},[r("treeselect",{staticStyle:{width:"300px"},attrs:{multiple:!0,options:e.roles,placeholder:"请选择角色"},model:{value:e.roleIds,callback:function(t){e.roleIds=t},expression:"roleIds"}})],1)],1)],1),e._v(" "),r("el-row",[r("el-col",{attrs:{span:12}},[r("el-form-item",{staticStyle:{"margin-bottom":"0"},attrs:{label:"技能"}},[r("treeselect",{staticStyle:{width:"300px"},attrs:{multiple:!0,options:e.skills,placeholder:"请选择技能"},model:{value:e.skillIds,callback:function(t){e.skillIds=t},expression:"skillIds"}})],1)],1)],1)],1),e._v(" "),r("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[r("el-button",{attrs:{type:"text"},on:{click:e.cancel}},[e._v("取消")]),e._v(" "),r("el-button",{attrs:{loading:e.loading,type:"primary"},on:{click:e.doSubmit}},[e._v("确认")])],1)],1)},[],!1,null,"02d7ea3a",null);p.options.__file="form.vue";t.default=p.exports},fhgi:function(e,t,r){"use strict";r.r(t);var i=r("wk8/"),a={props:{data:{type:Object,required:!0},sup_this:{type:Object,required:!0}},data:function(){var e=this;return{loading:!1,dialog:!1,title:"修改密码",form:{new_password1:"",new_password2:""},rules:{new_password1:[{required:!0,message:"请输入新密码",trigger:"blur"},{min:6,max:20,message:"长度在 6 到 20 个字符",trigger:"blur"}],new_password2:[{required:!0,validator:function(t,r,i){e.form.new_password1!==r?i(new Error("两次输入的密码不一致")):i()},trigger:"blur"}]}}},methods:{cancel:function(){this.resetForm()},doSubmit:function(){var e=this;this.$refs.form.validate(function(t){if(!t)return!1;e.loading=!0,Object(i.f)(e.data.id,e.form).then(function(t){e.resetForm(),e.$message({showClose:!0,type:"success",message:"密码修改成功!请重新登录!",duration:2500}),e.sup_this.init()}).catch(function(t){e.loading=!1,console.log(t)})})},resetForm:function(){this.dialog=!1,this.$refs.form.resetFields(),this.form={new_password1:"",new_password2:""}}}},n=(r("T4hH"),r("KHd+")),s=Object(n.a)(a,function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticStyle:{display:"inline-block"}},[r("el-button",{staticClass:"button",attrs:{size:"mini",type:"primary",disabled:1===e.data.id},on:{click:function(t){e.dialog=!0}}},[e._v("密码\n  ")]),e._v(" "),r("el-dialog",{attrs:{width:"500px",visible:e.dialog,title:e.title},on:{"update:visible":function(t){e.dialog=t},close:e.cancel}},[r("el-form",{ref:"form",attrs:{size:"small","label-width":"88px",model:e.form,rules:e.rules}},[r("el-form-item",{attrs:{label:"新密码",prop:"new_password1"}},[r("el-input",{staticStyle:{width:"370px"},attrs:{type:"password","auto-complete":"on"},model:{value:e.form.new_password1,callback:function(t){e.$set(e.form,"new_password1",t)},expression:"form.new_password1"}})],1),e._v(" "),r("el-form-item",{attrs:{label:"确认密码",prop:"new_password2"}},[r("el-input",{staticStyle:{width:"370px"},attrs:{type:"password","auto-complete":"on"},model:{value:e.form.new_password2,callback:function(t){e.$set(e.form,"new_password2",t)},expression:"form.new_password2"}})],1)],1),e._v(" "),r("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[r("el-button",{attrs:{type:"text"},on:{click:e.cancel}},[e._v("取消")]),e._v(" "),r("el-button",{attrs:{loading:e.loading,type:"primary"},on:{click:e.doSubmit}},[e._v("确认")])],1)],1)],1)},[],!1,null,"23cec52a",null);s.options.__file="updatePass.vue";t.default=s.exports},iM05:function(e,t,r){"use strict";r.r(t);var i=r("41Be"),a=r("02iu"),n={components:{eForm:r("fIwS").default},props:{organizations:{type:Array,required:!0},roles:{type:Array,required:!0},query:{type:Object,required:!0}},data:function(){return{orgusers:[],downloadLoading:!1,enabledTypeOptions:[{key:"true",display_name:"激活"},{key:"false",display_name:"锁定"}]}},methods:{checkPermission:i.a,toQuery:function(){this.$parent.page=1,this.$parent.init()},getOrgUserTree:function(){var e=this;Object(a.e)().then(function(t){e.orgusers=t.detail})},download:function(){var e=this;this.downloadLoading=!0,Promise.all([r.e("chunk-ef4a"),r.e("chunk-54ca")]).then(r.bind(null,"S/jZ")).then(function(t){var r=e.formatJson(["id","username","email","avatar","is_active","createTime","lastPasswordResetTime"],e.$parent.data);t.export_json_to_excel({header:["ID","用户名","邮箱","头像地址","状态","注册日期","最后修改密码日期"],data:r,filename:"table-list"}),e.downloadLoading=!1})},formatJson:function(e,t){return t.map(function(t){return e.map(function(e){return"is_active"===e?t[e]?"启用":"禁用":t[e]})})}}},s=r("KHd+"),o=Object(s.a)(n,function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"head-container"},[r("el-input",{staticClass:"filter-item",staticStyle:{width:"200px"},attrs:{clearable:"",placeholder:"输入关键字搜索"},nativeOn:{keyup:function(t){return"button"in t||!e._k(t.keyCode,"enter",13,t.key,"Enter")?e.toQuery(t):null}},model:{value:e.query.value,callback:function(t){e.$set(e.query,"value",t)},expression:"query.value"}}),e._v(" "),r("el-select",{staticClass:"filter-item",staticStyle:{width:"90px"},attrs:{placeholder:"状态",value:"",clearable:""},on:{change:e.toQuery},model:{value:e.query.is_active,callback:function(t){e.$set(e.query,"is_active",t)},expression:"query.is_active"}},e._l(e.enabledTypeOptions,function(e){return r("el-option",{key:e.key,attrs:{label:e.display_name,value:e.key}})})),e._v(" "),r("el-button",{staticClass:"filter-item",attrs:{size:"mini",type:"primary",icon:"el-icon-search"},on:{click:e.toQuery}},[e._v("搜索\n  ")]),e._v(" "),r("div",{staticStyle:{display:"inline-block",margin:"0 2px"}},[e.checkPermission(["admin","user_all","user_create"])?r("el-button",{staticClass:"filter-item",attrs:{size:"mini",type:"primary",icon:"el-icon-plus"},on:{click:function(t){e.$refs.form.dialog=!0,e.getOrgUserTree()}}},[e._v("新增\n    ")]):e._e(),e._v(" "),r("eForm",{ref:"form",attrs:{roles:e.roles,organizations:e.organizations,orgusers:e.orgusers,"is-add":!0}})],1),e._v(" "),e.checkPermission(["admin","user_all"])?r("el-button",{staticClass:"filter-item",attrs:{size:"mini",type:"primary",icon:"el-icon-download",loading:e.downloadLoading},on:{click:e.download}},[e._v("导出\n  ")]):e._e()],1)},[],!1,null,null,null);o.options.__file="header.vue";t.default=o.exports},"wk8/":function(e,t,r){"use strict";r.d(t,"a",function(){return a}),r.d(t,"b",function(){return n}),r.d(t,"c",function(){return s}),r.d(t,"f",function(){return o}),r.d(t,"d",function(){return l}),r.d(t,"e",function(){return u});var i=r("t3Un");function a(e){return Object(i.a)({url:"api/users/",method:"post",data:e})}function n(e){return Object(i.a)({url:"api/users/"+e+"/",method:"delete"})}function s(e,t){return Object(i.a)({url:"api/users/"+e+"/",method:"put",data:t})}function o(e,t){return Object(i.a)({url:"api/users/"+e+"/change-passwd/",method:"post",data:t})}function l(e){return e?Object(i.a)({url:"api/user/list/?name="+e,method:"get"}):Object(i.a)({url:"api/user/list/",method:"get"})}function u(){return Object(i.a)({url:"api/v1/points",method:"get"})}},zF5t:function(e,t,r){"use strict";r.d(t,"d",function(){return a}),r.d(t,"a",function(){return n}),r.d(t,"b",function(){return s}),r.d(t,"c",function(){return o}),r.d(t,"e",function(){return l}),r.d(t,"f",function(){return u});var i=r("t3Un");function a(){return Object(i.a)({url:"api/roles/",method:"get"})}function n(e){return Object(i.a)({url:"api/roles/",method:"post",data:e})}function s(e){return Object(i.a)({url:"api/roles/"+e+"/",method:"delete"})}function o(e,t){return Object(i.a)({url:"api/roles/"+e+"/",method:"put",data:t})}function l(e){return Object(i.a)({url:"api/roles/"+e+"/",method:"get"})}function u(e,t){return Object(i.a)({url:"api/roles/"+e+"/",method:"patch",data:t})}}}]);