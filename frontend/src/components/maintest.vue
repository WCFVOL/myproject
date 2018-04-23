<template lang="html">
  <el-container style="overflow: hidden;position: absolute;top: 0;right: 0;bottom: 0;left: 0;min-width: 1103px;_width: 100%;_height: 630px;">
    <el-header style="height:10%">
      <img class="image" :src="src" alt="头像" width="70" height="70"/>
      <div class="nickname">
        <p style="display: inline-block;margin:0">欢迎{{ this.$parent.nickname }}!</p>
        <a style="display: inline-block;text-decoration:none"href="#" @click="quit()">登出</a>
      </div>
    </el-header>
    <el-container>
      <el-aside width="200px"style="background-color: rgb(255, 255, 255)">
        <div style="height:50%;width:100%">
          <el-row class="tac"style="width:99.5%;">
              <el-menu default-active="3" class="el-menu-vertical-demo">
                <el-menu-item index="1">
                  <i class="el-icon-menu"></i>
                  <span slot="title">全部文件</span>
                </el-menu-item>
                <el-menu-item index="2">
                  <i class="el-icon-picture"></i>
                  <span slot="title">图片</span>
                </el-menu-item>
                <el-menu-item index="3">
                  <i class="el-icon-service"></i>
                  <span slot="title">音乐</span>
                </el-menu-item>
              </el-menu>
          </el-row>
        </div>
        <div style="height:50%">

        </div>
      </el-aside>
      <el-main hegith="120px">
        <el-container >
          <el-header style="height:70px;padding: 0px;margin : 0;">
            <ul style="width:1000px;list-style: none;padding: 0px;margin : 0;">
              <li style="float:left;display: inline;width:270px;list-style: none;padding: 0px;margin : 0;">
                <a href="javascript:void(0)" style="display: inline-block;text-decoration:none" @click="NewFolder">
                  <el-button style="display: inline;postion:absolute;left:0;"type="primary" icon="el-icon-edit">新建文件夹</el-button>
                </a>
                <a href="javascript:void(0)" style="display: inline-block;" @click="Uploadstart">
                  <el-button type="primary">上传<i class="el-icon-upload el-icon--right"></i></el-button>
                  <span class="text">{{progress}}</span>
                </a>
              </li>
            </ul>
          </el-header>
          <el-main style="width: 100%;padding: 0px;margin : 0;">
          <div style="position: absolute;height:82%;width:87.5%">
            <div id = "layoutList-head">
              <ul id="layoutList-ul-head">
                <li class="headli" style="width:60%">
                  <span class="text" >文件名</span>
                </li>
                <li class="headli" style="width:16%">
                  <span class="text" >文件大小</span>
                </li>
                <li class="headli" style="width:23%">
                  <span class="text">更新日期</span>
                </li>
              </ul>
            </div>
            <div id="layoutList-head" style="overflow:auto;height:90%">
              <ul id="layoutList-ul" v-for="e in all" :key="e.size">
                <li style="width:60%">
                  <div v-if = "e.ok === true">
                      <input class='text' type="text" v-model="e.list">
                      <button type="button" name="button" @click="NewFolderSubmit()">确认</button>
                      <button type="button" name="button" @click="NewFolderCancel()">取消</button>
                  </div>
                  <div v-else-if = "e.size === -1">
                    <router-link :to="{path: '/maintest/', query: {id: e.listid}}" class="a-folder text">{{ e.list }}</router-link>
                  </div>
                  <div v-else>
                    <span class="text">{{ e.list }}</span>
                  </div>
                </li>
                <li style="width:16%">
                  <span class="text" v-if="e.size !== -1">{{ e.size }}</span>
                  <span class="text" v-else>-</span>
                </li>
                <li style="width:23%">
                  <span class="text">{{ e.update }}</span>
                  <el-button type="primary" icon="el-icon-download" name="button" v-if="e.size !== -1" @click="Download(e.listid, e.list)">下载</el-button>
                </li>
              </ul>
            </div>
          </div>
          </el-main>
        </el-container>
      </el-main>
    </el-container>
    <input type="file" ref="btn_file" style="display:none" @change="Uploadend">
  </el-container>
</template>
<script type="text/javascript">
import axios from 'axios'
axios.defaults.headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}
export default {
  data () {
    return {
      all: [], // 上述属性的字典形式
      progress: '',
      path: [], // 路径
      listid: [], // 列表id
      nowid: this.$route.query.id, // 当前文件夹的listid
      list: [], // 文件列表名称
      size: [], // 文件大小
      update: [], // 更新时间
      debug: '', // 调试bug使用
      src: BASE_URL + '/media/' + this.$parent.image // 头像src
    }
  },
  beforeCreate () {
    if (this.$parent.nickname === undefined) {
      this.$router.push({path: '/'})
    }
  },
  beforeRouteUpdate (to, from, next) {
  // just use `this`
  this.nowid = to.query.id
  if (this.$parent.nickname === undefined) {
    this.$router.push({path: '/'})
  }
  // alert(this.nowid)
  let data = {'userID': this.$parent.userID, 'nowid': this.nowid}
  this.path.push('/')
  axios.post('/vueapi/list', data).then((res) => {
    // console.log(res)
    if (res.data['data'] === 'ok') {
      this.all = []
      this.list = res.data['list']
      this.listid = res.data['listid']
      this.size = res.data['size']
      this.update = res.data['update']
      for (var i = 0; i < this.list.length; i++) {
        this.all.push({'list': this.list[i], 'listid': this.listid[i], 'size': this.size[i], 'update': this.update[i], 'ok': false})
      }
    } else {
      this.debug = res.data['data']
    }
  })
  next()
  },
  created () {
    if (this.$parent.nickname === undefined) {
      this.$router.push({path: '/'})
    }
    this.refresh()
  },
  methods: {
    quit () {
      this.$router.push({path: '/'})
    },
    refresh () {
      if (this.$parent.nickname === undefined) {
        this.$router.push({path: '/'})
      }
      // alert(this.nowid)
      let data = {'userID': this.$parent.userID, 'nowid': this.nowid}
      axios.post('/vueapi/list', data).then((res) => {
        // console.log(res)
        if (res.data['data'] === 'ok') {
          this.all = []
          this.list = res.data['list']
          this.listid = res.data['listid']
          this.size = res.data['size']
          this.update = res.data['update']
          for (var i = 0; i < res.data.list.length; i++) {
            this.all.push({'list': this.list[i], 'listid': this.listid[i], 'size': this.size[i], 'update': this.update[i], 'ok': false})
          }
        } else {
          this.debug = res.data['data']
        }
      })
    },
    Download (id, name) {
      let url = BASE_URL + '/vueapi/download?fileid=' + id + '&filename=' + name
      window.open(url)
    },
    Uploadstart () {
      this.$refs.btn_file.click()
    },
    Uploadend () {
      var data = new FormData()
      data.append('userID', this.$parent.userID)
      data.append('nowid', this.nowid)
      data.append('file', this.$refs.btn_file.files[0])
      var config = {
        onUploadProgress: progressEvent => {
          var complete = ((progressEvent.loaded / progressEvent.total * 100) - 1 | 0) + '%'
          this.progress = complete
        },
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      axios.post('/vueapi/upload', data, config).then((res) => {
        console.log(res)
        if (res.data['data'] === 'ok') {
          this.progress = '100%'
          alert('上传成功')
          this.progress = ''
          this.$refs.btn_file.files = []
          this.refresh()
        } else {
          alert('上传失败')
        }
      })
    },
    NewFolder () {
      this.list.unshift('新建文件夹')
      this.all.unshift({'list': this.list[0], 'listid': this.listid[0], 'size': this.size[0], 'update': this.update[0], 'ok': true})
    },
    judgename (name) {
      for (var i = 1; i < this.list.length; i++) {
        if (this.list[i] === name) {
          return false
        }
      }
      return true
    },
    NewFolderSubmit () {
      var name = this.all[0].list
      if (this.judgename(name) === false) {
        for (var i = 1; i < 10; i++) {
          name = this.all[0].list
          name = name + '(' + i + ')'
          if (this.judgename(name) === true) break
        }
      }
      this.all[0].list = name
      this.list[0] = this.all[0].list
      let data = {'userID': this.$parent.userID, 'nowid': this.nowid, 'foldername': name}
      axios.post('/vueapi/newfolder', data).then((res) => {
        // console.log(res)
        if (res.data['data'] === 'ok') {
          this.all[0].ok = false
          this.listid[0] = res.data['listid']
          this.update[0] = res.data['update']
          this.all[0].listid = this.listid[0]
          this.all[0].update = this.update[0]
          this.refresh()
        } else {
          this.debug = res.data['data']
          this.list.shift()
          this.all.shift()
        }
      })
    },
    NewFolderCancel () {
      this.list.shift()
      this.all.shift()
    }
  }
}

</script>

<style>
.frame-all {
    background: #eff4f8;
}
.frame-main {
    background: #fff;
}
.nickname{color:#000000;float:right;height: 60px;}
.image{ float: right}
.text{
  float:left;
  font: 12px/2.5 "Microsoft YaHei", arial, SimSun, 宋体;
}
.g-button-right {
    position: relative;
    right: -1px;
    display: block;
    height: 29px;
    padding-right: 15px;
    line-height: 29px;
    text-align: center;
    cursor: pointer;
}
.a-folder {
    color: #666;
    text-decoration: none;
}
.g-button {
    position: relative;
    display: inline-block;
    height: 30px;
    margin: 0 5px;
    padding-left: 15px;
    font-size: 12px;
    line-height: 30px;
    vertical-align: top;
    white-space: nowrap;
    text-decoration: none;
    border: 1px solid #d4d4d4;
    color: #666;
    outline: 0;
    border-radius: 2px;
}
div{
  display: block;
}
ul{
  display: block;
  width:100%;/*这里设置为确定的值也可以*/
  height:30px;
}
li{
  cursor: pointer;
  float: left;
  display: inline-block;
  list-style: none;
  text-align: -webkit-match-parent;
  height:30px;
}
.headli{
  cursor: pointer;
  float: left;
  display: inline-block;
  list-style: none;
  text-align: -webkit-match-parent;
  height:30px;
}
.headli:hover{
  cursor: pointer;
  float: left;
  display: inline-block;
  list-style: none;
  text-align: -webkit-match-parent;
  height:30px;
  background-color: #EAFFFF;
}
#layoutApp {
    overflow: hidden;
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    min-width: 1103px;
    _width: 100%;
    _height: 630px;
}
#layoutMain {
    border-top:  1px solid #d8dfea;
    border-left: 1px solid #d8dfea;
    border-right: 1px solid #d8dfea;
    margin-left: -1px;
}
#layoutMain {
    top: 13%;
    left: 7%;
    bottom: 2%;
    right: 1%;
    z-index: 1;
    background: #fff;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    position: absolute;
}
#layoutList {
    border-top: 1px solid #d8dfea;
    border-left: 1px solid #d8dfea;
    border-right: 1px solid #d8dfea;
    margin-left: -1px;
}
#layoutList {
    top: 70px;
    left: 0px;
    bottom: 1px;
    right: 0px;
    z-index: 1;
    background: #fff;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    position: absolute;
}
#layoutList-path {
  padding-left: 16px;
  background-color: #fff;
  height: 16px;
  line-height: 16px;
  margin-bottom: 5px;
}
#layoutList-but {
  padding-left: 16px;
  background-color: #fff;
  height: 70px;
  line-height: 16px;
  margin-bottom: 5px;
}
#layoutList-head {
  padding-left: 16px;
  background-color: #fff;
  height: 30px;
  line-height: 16px;
  margin-bottom: 5px;
}
#layoutList-ul-head{
  padding-left: 0px;
  background-color: #fff;
  height: 30px;
  line-height: 16px;
  margin-bottom: 5px;
}
#layoutList-ul {
  padding-left: 0px;
  background-color: #fff;
  height: 30px;
  line-height: 16px;
  margin-bottom: 5px;
}
#layoutList-ul:hover {
  padding-left: 0px;
  background-color: #EAFFFF;
  height: 30px;
  line-height: 16px;
  margin-bottom: 5px;
}
  .el-header, .el-footer {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
  }

  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }

  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 160px;
  }

  body > .el-container {
    margin-bottom: 40px;
  }

  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }

  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
</style>
