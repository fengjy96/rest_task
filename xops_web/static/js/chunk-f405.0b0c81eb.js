(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-f405","chunk-d767"],{"4t+H":function(e,t,n){"use strict";n.r(t);var a=n("PL5b"),i=n("g8L3"),l={name:"step_file_preview",props:{file:{type:Object,required:!0}},components:{image_preview:a.a,rte_preview:i.a},data:function(){return{}},watch:{file:{deep:!0,handler:function(){}}},methods:{handleDownload:function(){}},created:function(){}},o=(n("aJMq"),n("KHd+")),r=Object(o.a)(l,function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"step-file-preview"},[n("el-button",{staticClass:"download",attrs:{type:"text",size:"mini"},on:{click:function(t){return t.stopPropagation(),e.handleDownload(t)}}},[1===e.file.type?n("a",{attrs:{target:"_blank",href:e.file.path,download:e.file.name}},[e._v("下载\n    ")]):e._e()]),e._v(" "),n("div",[1===e.file.type?n("image_preview",{attrs:{src:e.file.path}}):n("rte_preview",{attrs:{content:e.file.content}})],1)],1)},[],!1,null,"0fa7e686",null);r.options.__file="file_preview.vue";t.default=r.exports},"57ZV":function(e,t,n){},VmOs:function(e,t,n){"use strict";n.r(t);var a=n("4t+H"),i=n("PL5b"),l=n("g8L3"),o={name:"step_file_table",components:{image_preview:i.a,rte_preview:l.a,file_preview:a.default},props:{files:{type:Array,default:function(){return[]}}},data:function(){return{expands:[],src:"",type:"",content:"",file:""}},methods:{handlePreview:function(e){var t=window.open("","预览","width=500, height=300");1===e.type?t.document.write('<img src="'+e.path+'" alt=""/>'):0===e.type&&t.document.write(e.content)},getRowKeys:function(e){return e.name+e.id},handleExpandChange:function(e,t){var n=this;t.length>1&&this.files.forEach(function(t){t.id!==e.id&&n.$refs.tables.toggleRowExpansion(t,!1)})},handleRowClick:function(e,t,n){this.$refs.tables.toggleRowExpansion(e)}}},r=(n("zD9V"),n("KHd+")),s=Object(r.a)(o,function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("el-table",{ref:"tables",staticStyle:{width:"100%"},attrs:{data:e.files,border:"","highlight-current-row":"",size:"small",fit:"","expand-row-keys":e.expands,"row-key":e.getRowKeys},on:{"expand-change":e.handleExpandChange,"row-click":e.handleRowClick}},[n("el-table-column",{attrs:{type:"expand"},scopedSlots:e._u([{key:"default",fn:function(e){return[n("div",[n("file_preview",{attrs:{file:e.row}})],1)]}}])}),e._v(" "),n("el-table-column",{attrs:{prop:"name",label:"文件名"}}),e._v(" "),n("el-table-column",{attrs:{prop:"type_name",label:"类型"}}),e._v(" "),n("el-table-column",{attrs:{prop:"add_time",label:"提交时间"}}),e._v(" "),n("el-table-column",{attrs:{label:"操作"},scopedSlots:e._u([{key:"default",fn:function(t){return[n("el-button",{attrs:{type:"text",size:"small"},on:{click:function(n){n.stopPropagation(),e.handlePreview(t.row)}}},[e._v("预览")])]}}])})],1)],1)},[],!1,null,"44646d6b",null);s.options.__file="file_table.vue";t.default=s.exports},XK0V:function(e,t,n){},aJMq:function(e,t,n){"use strict";var a=n("XK0V");n.n(a).a},zD9V:function(e,t,n){"use strict";var a=n("57ZV");n.n(a).a}}]);