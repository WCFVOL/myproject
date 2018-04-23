<template>
  <div class="">
    <a href="javascript:void(0)" @click="testt()">123</a>
    <el-table :data="all" style="width: 100%;padding: 0px;margin : 0;">
      <el-table-column
        prop="list"
        label="文件名"
        width="1000">
      </el-table-column>
      <el-table-column
        prop="size"
        label="文件大小"
        width="300">
      </el-table-column>
      <el-table-column
      prop="update"
        label="更新日期">
      </el-table-column>
    </el-table>
  </div>
</template>
<script type="text/javascript">
import axios from 'axios'
axios.defaults.headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}
export default{
  methods: {
    deleteRow(index, rows) {
      rows.splice(index, 1);
    },
    testt() {
      this.all.push({'list':'list'})
    }
  },
  data() {
    return {
      all: [{'list':'123'}], // 上述属性的字典形式
      progress: '',
      path: [], // 路径
      listid: [], // 列表id
      test:[],
      nowid: this.$route.query.id, // 当前文件夹的listid
      list: [], // 文件列表名称
      size: [], // 文件大小
      update: [], // 更新时间
      table: [{'list':'list'}],
      debug: '', // 调试bug使用
      src: BASE_URL + '/media/' + this.$parent.image // 头像src
    }
  }
}
</script>
<style media="screen">
@import url("//unpkg.com/element-ui@2.3.6/lib/theme-chalk/index.css");

</style>
