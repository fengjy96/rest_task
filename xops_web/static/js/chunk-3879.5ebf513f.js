(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-3879","chunk-6a42"],{"41Be":function(e,t,r){"use strict";r.d(t,"a",function(){return i});var o=r("Q2AE");function i(e){if(e&&e instanceof Array&&e.length>0){var t=e;return!!(o.a.getters&&o.a.getters.roles).some(function(e){return t.includes(e)})}return console.error("need roles! Like v-permission=\"['admin','editor']\""),!1}},"4cRZ":function(e,t,r){},"5ZET":function(e,t,r){"use strict";r.r(t);var o=r("41Be"),i={components:{eForm:r("gAlZ").default},props:{query:{type:Object,required:!0},menus:{type:Array,required:!0}},data:function(){return{downloadLoading:!1}},methods:{checkPermission:o.a,toQuery:function(){console.log(this.query),this.$parent.page=1,this.$parent.init()}}},s=r("KHd+"),n=Object(s.a)(i,function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"head-container"},[r("el-input",{staticClass:"filter-item",staticStyle:{width:"200px"},attrs:{placeholder:"输入名称搜索",clearable:""},nativeOn:{keyup:function(t){return"button"in t||!e._k(t.keyCode,"enter",13,t.key,"Enter")?e.toQuery(t):null}},model:{value:e.query.value,callback:function(t){e.$set(e.query,"value",t)},expression:"query.value"}}),e._v(" "),r("el-button",{staticClass:"filter-item",attrs:{size:"mini",type:"primary",icon:"el-icon-search"},on:{click:e.toQuery}},[e._v("搜索\n  ")]),e._v(" "),r("div",{staticStyle:{display:"inline-block",margin:"0 2px"}},[e.checkPermission(["admin","menu_all","menu_create"])?r("el-button",{staticClass:"filter-item",attrs:{size:"mini",type:"primary",icon:"el-icon-plus"},on:{click:function(t){e.$refs.form.dialog=!0}}},[e._v("新增\n    ")]):e._e(),e._v(" "),r("eForm",{ref:"form",attrs:{menus:e.menus,"is-add":!0}})],1)],1)},[],!1,null,null,null);n.options.__file="header.vue";t.default=n.exports},Hycs:function(e,t,r){"use strict";r.d(t,"d",function(){return i}),r.d(t,"a",function(){return s}),r.d(t,"b",function(){return n}),r.d(t,"c",function(){return a});var o=r("t3Un");function i(){return Object(o.a)({url:"api/menu/tree/",method:"get"})}function s(e){return Object(o.a)({url:"api/menus/",method:"post",data:e})}function n(e){return Object(o.a)({url:"api/menus/"+e+"/",method:"delete"})}function a(e,t){return Object(o.a)({url:"api/menus/"+e+"/",method:"put",data:t})}},gAlZ:function(e,t,r){"use strict";r.r(t);var o=r("Hycs"),i=r("cCY5"),s=r.n(i),n=r("Wu6X"),a=(r("VCwm"),{components:{Treeselect:s.a,IconSelect:n.a},props:{menus:{type:Array,required:!0},isAdd:{type:Boolean,required:!0},sup_this:{type:Object,default:null}},data:function(){return{loading:!1,dialog:!1,form:{name:"",sort:999,path:"",component:"",is_show:"true",is_frame:"false",pid:null,icon:""},rules:{is_show:[{required:!0,message:"是否在导航栏显示",trigger:"blur"}],name:[{required:!0,message:"请输入名称",trigger:"blur"}],sort:[{required:!0,message:"请输入序号",trigger:"blur",type:"number"}],is_frame:[{required:!0,message:"请选择菜单类型",trigger:"blur"}]}}},methods:{cancel:function(){this.resetForm()},doSubmit:function(){var e=this;this.$refs.form.validate(function(t){if(!t)return!1;e.loading=!0,e.isAdd?e.doAdd():e.doEdit()})},doAdd:function(){var e=this;Object(o.a)(this.form).then(function(t){e.resetForm(),e.$message({showClose:!0,type:"success",message:"添加成功!",duration:2500}),e.loading=!1,e.$parent.$parent.init(),e.$parent.$parent.getMenus()}).catch(function(t){e.loading=!1,console.log(t)})},doEdit:function(){var e=this;Object(o.c)(this.form.id,this.form).then(function(t){e.resetForm(),e.$message({showClose:!0,type:"success",message:"修改成功!",duration:2500}),e.loading=!1,e.sup_this.init(),e.sup_this.getMenus()}).catch(function(t){e.loading=!1,console.log(t)})},resetForm:function(){this.dialog=!1,this.$refs.form.resetFields(),this.form={name:"",sort:999,path:"",component:"",is_show:"true",is_frame:"false",pid:null,icon:""}},selected:function(e){this.form.icon=e}}}),l=(r("nZPr"),r("KHd+")),c=Object(l.a)(a,function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("el-dialog",{attrs:{width:"600px","append-to-body":!0,visible:e.dialog,title:e.isAdd?"新增菜单":"编辑菜单"},on:{"update:visible":function(t){e.dialog=t}}},[r("el-form",{ref:"form",attrs:{size:"small","label-width":"80px",model:e.form,rules:e.rules}},[r("el-form-item",{attrs:{label:"是否显示",prop:"is_show"}},[r("el-radio",{attrs:{label:"true"},model:{value:e.form.is_show,callback:function(t){e.$set(e.form,"is_show",t)},expression:"form.is_show"}},[e._v("是")]),e._v(" "),r("el-radio",{attrs:{label:"false"},model:{value:e.form.is_show,callback:function(t){e.$set(e.form,"is_show",t)},expression:"form.is_show"}},[e._v("否")])],1),e._v(" "),"true"===e.form.is_show?r("el-form-item",{attrs:{prop:"icon",label:"菜单图标"}},[r("el-popover",{attrs:{placement:"bottom-start",width:"460",trigger:"click"},on:{show:function(t){e.$refs.iconSelect.reset()}}},[r("IconSelect",{ref:"iconSelect",on:{selected:e.selected}}),e._v(" "),r("el-input",{staticStyle:{width:"460px"},attrs:{slot:"reference",placeholder:"点击选择图标",readonly:""},slot:"reference",model:{value:e.form.icon,callback:function(t){e.$set(e.form,"icon",t)},expression:"form.icon"}},[e.form.icon?r("svg-icon",{staticClass:"el-input__icon",staticStyle:{height:"32px",width:"16px"},attrs:{slot:"prefix","icon-class":e.form.icon},slot:"prefix"}):r("i",{staticClass:"el-icon-search el-input__icon",attrs:{slot:"prefix"},slot:"prefix"})],1)],1)],1):e._e(),e._v(" "),r("el-form-item",{attrs:{label:"菜单名称",prop:"name"}},[r("el-input",{staticStyle:{width:"460px"},attrs:{placeholder:"名称"},model:{value:e.form.name,callback:function(t){e.$set(e.form,"name",t)},expression:"form.name"}})],1),e._v(" "),r("el-form-item",{attrs:{label:"菜单排序",prop:"sort"}},[r("el-input",{staticStyle:{width:"460px"},attrs:{placeholder:"序号越小越靠前"},model:{value:e.form.sort,callback:function(t){e.$set(e.form,"sort",e._n(t))},expression:"form.sort"}})],1),e._v(" "),r("el-form-item",{attrs:{label:"内部菜单",prop:"is_frame"}},[r("el-radio",{attrs:{label:"false"},model:{value:e.form.is_frame,callback:function(t){e.$set(e.form,"is_frame",t)},expression:"form.is_frame"}},[e._v("是")]),e._v(" "),r("el-radio",{attrs:{label:"true"},model:{value:e.form.is_frame,callback:function(t){e.$set(e.form,"is_frame",t)},expression:"form.is_frame"}},[e._v("否")])],1),e._v(" "),r("el-form-item",{attrs:{label:"链接地址"}},[r("el-input",{staticStyle:{width:"460px"},attrs:{placeholder:"菜单路径"},model:{value:e.form.path,callback:function(t){e.$set(e.form,"path",t)},expression:"form.path"}})],1),e._v(" "),"false"===e.form.is_frame?r("el-form-item",{attrs:{label:"组件路径"}},[r("el-input",{staticStyle:{width:"460px"},attrs:{placeholder:"组件路径"},model:{value:e.form.component,callback:function(t){e.$set(e.form,"component",t)},expression:"form.component"}})],1):e._e(),e._v(" "),r("el-form-item",{attrs:{label:"父级菜单"}},[r("treeselect",{staticStyle:{width:"460px"},attrs:{options:e.menus,placeholder:"请选择父级菜单"},model:{value:e.form.pid,callback:function(t){e.$set(e.form,"pid",t)},expression:"form.pid"}})],1)],1),e._v(" "),r("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[r("el-button",{attrs:{type:"text"},on:{click:e.cancel}},[e._v("取消")]),e._v(" "),r("el-button",{attrs:{loading:e.loading,type:"primary"},on:{click:e.doSubmit}},[e._v("确认")])],1)],1)},[],!1,null,"0f2805a8",null);c.options.__file="form.vue";t.default=c.exports},nZPr:function(e,t,r){"use strict";var o=r("4cRZ");r.n(o).a}}]);