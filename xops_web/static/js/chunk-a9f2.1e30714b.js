(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-a9f2","chunk-4b02"],{"3ADX":function(e,t,n){"use strict";var i=n("14Xm"),a=n.n(i),r=n("4d7F"),l=n.n(r),s=n("D3Ub"),u=n.n(s),o=n("t3Un");function c(e,t,n){return Object(o.a)({url:e,method:"get",params:t,isMock:n})}var d=n("LvDl"),p=n.n(d);t.a={data:function(){return{loading:!0,rawData:[],data:[],page:1,size:10,total:0,url:"",params:{},query:{},time:170}},methods:{init:p.a.throttle(function(){var e=u()(a.a.mark(function e(){var t=this,n=arguments.length>0&&void 0!==arguments[0]&&arguments[0];return a.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,this.beforeInit();case 2:if(e.sent){e.next=4;break}return e.abrupt("return");case 4:return e.abrupt("return",new l.a(function(e,i){t.loading=!0,c(t.url,t.params,n).then(function(n){t.total=n.count,t.rawData=n.results,t.data=t.afterInit?t.afterInit(n.results):t.rawData,setTimeout(function(){t.loading=!1},t.time),e(n)}).catch(function(e){t.loading=!1,i(e)})}));case 5:case"end":return e.stop()}},e,this)}));return function(){return e.apply(this,arguments)}}(),1e3),beforeInit:function(){return!0},pageChange:function(e){this.page=e,this.init()},sizeChange:function(e){this.page=1,this.size=e,this.init()}}}},"41Be":function(e,t,n){"use strict";n.d(t,"a",function(){return a});var i=n("Q2AE");function a(e){if(e&&e instanceof Array&&e.length>0){var t=e;return!!(i.a.getters&&i.a.getters.roles).some(function(e){return t.includes(e)})}return console.error("need roles! Like v-permission=\"['admin','editor']\""),!1}},"5W6J":function(e,t,n){"use strict";n.r(t);var i=n("4d7F"),a=n.n(i),r=n("41Be"),l=n("3ADX"),s=n("qpgI"),u=n("7Qib"),o={components:{eHeader:n("AgHX").default},mixins:[l.a],data:function(){return{delLoading:!1,sup_this:this,allSelect:!1}},created:function(){var e=this;this.$nextTick(function(){e.init()})},methods:{parseTime:u.b,checkPermission:r.a,beforeInit:function(){this.url="api/devices/";var e=this.query,t=e.value,n=e.status,i=e.groups,a=e.labels,r=e.businesses,l=e.device_type,s=e.os_type;return this.params={page:this.page,size:this.size,ordering:"id"},""!==n&&null!==n&&(this.params.status=n),""!==i&&null!==i&&(this.params.groups=i),""!==a&&null!==a&&(this.params.labels=a),""!==r&&null!==r&&(this.params.businesses=r),""!==s&&null!==s&&(this.params.os_type=s),""!==l&&null!==l&&(this.params.device_type=l),t&&(this.params.search=t),!0},subDelete:function(e){var t=this;this.delLoading=!0,Object(s.a)(e).then(function(n){t.delLoading=!1,t.$refs[e].doClose(),t.init(),t.$message({showClose:!0,type:"success",message:"删除成功!",duration:2500})}).catch(function(n){t.delLoading=!1,t.$refs[e].doClose(),console.log(n)})},toggleSelection:function(e){var t=this;e&&(e.forEach(function(e){t.$refs.table.toggleRowSelection(e,!t.allSelect)}),this.allSelect=!this.allSelect)},handleSelectionChange:function(e){this.multipleSelection=e},doSelectionDel:function(){var e=this,t=[];this.multipleSelection.forEach(function(e,n){var i=Object(s.a)(e.id).catch(function(e){console.log(e)});t.push(i)}),a.a.all(t).then(function(t){e.init()})},toDetail:function(e){this.$router.push({path:"devices/detail",query:{id:e}})},handleNodeClick:function(e){console.log(e)}}},c=(n("e4N4"),n("KHd+")),d=Object(c.a)(o,function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"app-container"},[n("eHeader",{attrs:{query:e.query}}),e._v(" "),n("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],ref:"table",staticStyle:{width:"100%"},attrs:{data:e.data,size:"small",border:""},on:{"selection-change":e.handleSelectionChange}},[n("el-table-column",{attrs:{type:"selection",width:"55",align:"center"}}),e._v(" "),n("el-table-column",{attrs:{label:"序号",width:"60",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[n("div",[e._v(e._s(t.$index+1))])]}}])}),e._v(" "),n("el-table-column",{attrs:{prop:"hostname",label:"IP/域名",width:"120"}}),e._v(" "),n("el-table-column",{attrs:{label:"业务类型",width:"120"},scopedSlots:e._u([{key:"default",fn:function(t){return e._l(t.row.businesses,function(t){return n("el-tag",{key:t.id,staticStyle:{display:"inline-block",margin:"0px 2px"},attrs:{size:"small"}},[e._v(e._s(t.name))])})}}])}),e._v(" "),n("el-table-column",{attrs:{label:"设备标签"},scopedSlots:e._u([{key:"default",fn:function(t){return e._l(t.row.labels,function(t){return n("el-tag",{key:t.id,staticStyle:{display:"inline-block",margin:"0px 2px"},attrs:{size:"small"}},[e._v(e._s(t.name))])})}}])}),e._v(" "),n("el-table-column",{attrs:{prop:"os_version",label:"系统版本"}}),e._v(" "),n("el-table-column",{attrs:{label:"状态",width:"100"},scopedSlots:e._u([{key:"default",fn:function(t){return["online"==t.row.status?n("span",{staticStyle:{color:"#00CC00"}},[e._v("在线")]):n("span",{staticStyle:{color:"red"}},[e._v("下线")])]}}])}),e._v(" "),n("el-table-column",{attrs:{label:"操作",width:"150px",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[e.checkPermission(["admin","device_all","device_list"])?n("el-button",{attrs:{size:"mini",type:"primary"},on:{click:function(n){e.toDetail(t.row.id)}}},[e._v("详情")]):e._e(),e._v(" "),e.checkPermission(["admin","device_all","device_delete"])?n("el-popover",{ref:t.row.id,attrs:{placement:"top",width:"180"}},[n("p",[e._v("确定删除本条数据吗？")]),e._v(" "),n("div",{staticStyle:{"text-align":"right",margin:"0"}},[n("el-button",{attrs:{size:"mini",type:"text"},on:{click:function(n){e.$refs[t.row.id].doClose()}}},[e._v("取消")]),e._v(" "),n("el-button",{attrs:{loading:e.delLoading,type:"primary",size:"mini"},on:{click:function(n){e.subDelete(t.row.id)}}},[e._v("确定")])],1),e._v(" "),n("el-button",{attrs:{slot:"reference",type:"danger",size:"mini"},slot:"reference"},[e._v("删除")])],1):e._e()]}}])})],1),e._v(" "),n("el-pagination",{staticStyle:{"margin-top":"8px"},attrs:{total:e.total,layout:"total, prev, pager, next, sizes"},on:{"size-change":e.sizeChange,"current-change":e.pageChange}})],1)},[],!1,null,"7666e88d",null);d.options.__file="index.vue";t.default=d.exports},AgHX:function(e,t,n){"use strict";n.r(t);var i=n("41Be"),a=n("K22w"),r=n("I7qB"),l=n("NM0R"),s=n("twU4"),u={props:{query:{type:Object,required:!0}},data:function(){return{delLoading:!1,updateLoading:!1,status_list:[{value:"online",label:"在线"},{value:"offline",label:"下线"}],group_list:[],label_list:[],business_list:[],device_types:[],os_types:[{value:"Linux",label:"Linux系统"},{value:"Windows",label:"Windows系统"},{value:"Other",label:"其他系统"}]}},created:function(){var e=this;this.$nextTick(function(){e.getAllBusiness(),e.getAllGroup(),e.getAllLable(),e.getAllDeviceType()})},methods:{checkPermission:i.a,toQuery:function(){this.$parent.page=1,this.$parent.init()},to:function(){this.$refs.form.dialog=!0},getPtoggleSelect:function(){this.$parent.toggleSelection(this.$parent.data)},deleteSelect:function(){var e=this;if(this.$parent.multipleSelection){var t=this.$parent.multipleSelection.length;this.$confirm("此操作将删除"+t+"条数据, 是否继续?","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){e.$parent.doSelectionDel(),e.$message({type:"success",message:"删除成功!"})}).catch(function(){e.$message({type:"info",message:"已取消删除"})})}else this.$message({type:"info",message:"请先选择数据"})},refresh:function(){this.$parent.init()},getAllGroup:function(){var e=this;Array.isArray(this.group_list)&&0===this.group_list.length&&Object(r.d)().then(function(t){e.group_list=t.results})},getAllLable:function(){var e=this;Array.isArray(this.label_list)&&0===this.label_list.length&&Object(l.d)().then(function(t){e.label_list=t.results})},getAllBusiness:function(){var e=this;Array.isArray(this.business_list)&&0===this.business_list.length&&Object(a.d)().then(function(t){e.business_list=t.results})},getAllDeviceType:function(){var e=this;Array.isArray(this.business_list)&&0===this.business_list.length&&Object(s.e)("DEVICE_TYPE").then(function(t){e.device_types=t[0].DEVICE_TYPE})},formatJson:function(e,t){return t.map(function(t){return e.map(function(e){return"Succeed"===e?t[e]?"成功":"失败":t[e]})})}}},o=n("KHd+"),c=Object(o.a)(u,function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"head-container"},[n("el-input",{staticClass:"filter-item",staticStyle:{width:"192px"},attrs:{clearable:"",placeholder:"输入IP/域名搜索"},nativeOn:{keyup:function(t){return"button"in t||!e._k(t.keyCode,"enter",13,t.key,"Enter")?e.toQuery(t):null}},model:{value:e.query.value,callback:function(t){e.$set(e.query,"value",t)},expression:"query.value"}}),e._v(" "),n("el-button",{staticClass:"filter-item",attrs:{size:"mini",type:"primary",icon:"el-icon-search"},on:{click:e.toQuery}},[e._v("搜索")]),e._v(" "),n("div",{staticStyle:{display:"inline-block",margin:"0px 2px"}},[n("el-button-group",[e.checkPermission(["admin","device_all","device_delete"])?n("el-button",{staticClass:"filter-item",attrs:{size:"mini",type:"primary"},on:{click:e.getPtoggleSelect}},[e._v("全选")]):e._e(),e._v(" "),e.checkPermission(["admin","device_all","device_delete"])?n("el-button",{staticClass:"filter-item",attrs:{size:"mini",type:"danger"},on:{click:e.deleteSelect}},[e._v("删除")]):e._e(),e._v(" "),n("el-button",{staticClass:"filter-item",attrs:{size:"mini",type:"primary"},on:{click:e.refresh}},[e._v("刷新")])],1)],1),e._v(" "),n("div",{staticStyle:{display:"inline-block",margin:"0px 8px",float:"right"}},[e.checkPermission(["admin","device_all"])?n("el-button-group",[n("el-button",{staticClass:"filter-item",attrs:{loading:e.updateLoading,size:"mini",type:"warning",icon:"el-icon-plus"}},[e._v("全部更新")])],1):e._e()],1),e._v(" "),n("br"),e._v(" "),n("el-select",{staticClass:"filter-item",staticStyle:{width:"192px"},attrs:{clearable:"",placeholder:"设备组"},on:{change:e.toQuery},model:{value:e.query.groups,callback:function(t){e.$set(e.query,"groups",t)},expression:"query.groups"}},e._l(e.group_list,function(e){return n("el-option",{key:e.id,attrs:{label:e.name,value:e.id}})})),e._v(" "),n("el-select",{staticClass:"filter-item",staticStyle:{width:"192px"},attrs:{clearable:"",placeholder:"业务类型"},on:{change:e.toQuery},model:{value:e.query.businesses,callback:function(t){e.$set(e.query,"businesses",t)},expression:"query.businesses"}},e._l(e.business_list,function(e){return n("el-option",{key:e.id,attrs:{label:e.name,value:e.id}})})),e._v(" "),n("el-select",{staticClass:"filter-item",staticStyle:{width:"192px"},attrs:{clearable:"",placeholder:"标签"},on:{change:e.toQuery},model:{value:e.query.labels,callback:function(t){e.$set(e.query,"labels",t)},expression:"query.labels"}},e._l(e.label_list,function(e){return n("el-option",{key:e.id,attrs:{label:e.name,value:e.id}})})),e._v(" "),n("el-select",{staticClass:"filter-item",staticStyle:{width:"192px"},attrs:{clearable:"",placeholder:"设备类型"},on:{change:e.toQuery},model:{value:e.query.device_type,callback:function(t){e.$set(e.query,"device_type",t)},expression:"query.device_type"}},e._l(e.device_types,function(e){return n("el-option",{key:e.key,attrs:{label:e.value,value:e.key}})})),e._v(" "),n("el-select",{staticClass:"filter-item",staticStyle:{width:"192px"},attrs:{clearable:"",placeholder:"操作系统"},on:{change:e.toQuery},model:{value:e.query.os_type,callback:function(t){e.$set(e.query,"os_type",t)},expression:"query.os_type"}},e._l(e.os_types,function(e){return n("el-option",{key:e.value,attrs:{label:e.label,value:e.value}})})),e._v(" "),n("el-select",{staticClass:"filter-item",staticStyle:{width:"100px"},attrs:{clearable:"",placeholder:"状态"},on:{change:e.toQuery},model:{value:e.query.status,callback:function(t){e.$set(e.query,"status",t)},expression:"query.status"}},e._l(e.status_list,function(e){return n("el-option",{key:e.value,attrs:{label:e.label,value:e.value}})}))],1)},[],!1,null,null,null);c.options.__file="header.vue";t.default=c.exports},I7qB:function(e,t,n){"use strict";n.d(t,"d",function(){return a}),n.d(t,"a",function(){return r}),n.d(t,"b",function(){return l}),n.d(t,"e",function(){return s}),n.d(t,"c",function(){return u}),n.d(t,"f",function(){return o});var i=n("t3Un");function a(){return Object(i.a)({url:"api/groups/",method:"get"})}function r(e){return Object(i.a)({url:"api/groups/",method:"post",data:e})}function l(e){return Object(i.a)({url:"api/groups/"+e+"/",method:"delete"})}function s(e){return Object(i.a)({url:"api/groups/"+e+"/",method:"get"})}function u(e,t){return Object(i.a)({url:"api/groups/"+e+"/",method:"put",data:t})}function o(e,t){return Object(i.a)({url:"api/groups/"+e+"/",method:"patch",data:t})}},JqMZ:function(e,t,n){},K22w:function(e,t,n){"use strict";n.d(t,"d",function(){return a}),n.d(t,"a",function(){return r}),n.d(t,"b",function(){return l}),n.d(t,"e",function(){return s}),n.d(t,"c",function(){return u}),n.d(t,"f",function(){return o});var i=n("t3Un");function a(){return Object(i.a)({url:"api/businesses/",method:"get"})}function r(e){return Object(i.a)({url:"api/businesses/",method:"post",data:e})}function l(e){return Object(i.a)({url:"api/businesses/"+e+"/",method:"delete"})}function s(e){return Object(i.a)({url:"api/businesses/"+e+"/",method:"get"})}function u(e,t){return Object(i.a)({url:"api/businesses/"+e+"/",method:"put",data:t})}function o(e,t){return Object(i.a)({url:"api/businesses/"+e+"/",method:"patch",data:t})}},NM0R:function(e,t,n){"use strict";n.d(t,"d",function(){return a}),n.d(t,"a",function(){return r}),n.d(t,"b",function(){return l}),n.d(t,"e",function(){return s}),n.d(t,"c",function(){return u}),n.d(t,"f",function(){return o});var i=n("t3Un");function a(){return Object(i.a)({url:"api/labels/",method:"get"})}function r(e){return Object(i.a)({url:"api/labels/",method:"post",data:e})}function l(e){return Object(i.a)({url:"api/labels/"+e+"/",method:"delete"})}function s(e){return Object(i.a)({url:"api/labels/"+e+"/",method:"get"})}function u(e,t){return Object(i.a)({url:"api/labels/"+e+"/",method:"put",data:t})}function o(e,t){return Object(i.a)({url:"api/labels/"+e+"/",method:"patch",data:t})}},e4N4:function(e,t,n){"use strict";var i=n("JqMZ");n.n(i).a},qpgI:function(e,t,n){"use strict";n.d(t,"c",function(){return a}),n.d(t,"d",function(){return r}),n.d(t,"a",function(){return l}),n.d(t,"b",function(){return s});var i=n("t3Un");function a(e){return e?Object(i.a)({url:"api/device/list/?os_type="+e,method:"get"}):Object(i.a)({url:"api/device/list/",method:"get"})}function r(e){return Object(i.a)({url:"api/devices/"+e+"/",method:"get"})}function l(e){return Object(i.a)({url:"api/devices/"+e+"/",method:"delete"})}function s(e,t){return Object(i.a)({url:"api/devices/"+e+"/",method:"put",data:t})}},twU4:function(e,t,n){"use strict";n.d(t,"d",function(){return a}),n.d(t,"a",function(){return r}),n.d(t,"b",function(){return l}),n.d(t,"c",function(){return s}),n.d(t,"e",function(){return u});var i=n("t3Un");function a(){return Object(i.a)({url:"api/dict/tree/",method:"get"})}function r(e){return Object(i.a)({url:"api/dicts/",method:"post",data:e})}function l(e){return Object(i.a)({url:"api/dicts/"+e+"/",method:"delete"})}function s(e,t){return Object(i.a)({url:"api/dicts/"+e+"/",method:"put",data:t})}function u(){for(var e=arguments.length,t=Array(e),n=0;n<e;n++)t[n]=arguments[n];return Object(i.a)({url:"api/dicts/?&key="+t,method:"get"})}}}]);