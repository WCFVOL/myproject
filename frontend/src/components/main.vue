<template lang="html">
  <div class="frame-all" id="layoutApp">
    <p class="nickname">欢迎{{ this.$parent.nickname }}!</p>
    <img class="image" :src="src" alt="头像" width="70" height="70"/>
    <div class="frame-main" id="layoutMain">
      <!-- 新建文件夹等按钮 -->
      <div id="layoutList-but" style="position: absolute; top: 0px; padding-top: 18px; line-height: normal; padding-left: 0px; width: auto; visibility: visible;">
        <a class="g-button" href="javascript:void(0)" style="display: inline-block;" @click="NewFolder">
          <span class="g-button-right">新建文件夹</span>
        </a>
        <a class="g-button" href="javascript:void(0)" style="display: inline-block;" @click="Uploadstart">
          <span class="g-button-right">上传文件</span>
          <span class="text">{{progress}}</span>
        </a>
      </div>
      <!-- 显示块 -->
      <div id="layoutList">
        <!-- 第一层，显示路径 -->
        <div id= "layoutList-path">
            <!--返回上一级| 全部文件 path -->
        </div>
        <!-- 第二层，显示文件名，文件大小，更新日期 -->
        <div id="layoutList-head">
          <ul id="layoutList-head">
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
        <!-- 第三层，显示文件列表 -->
        <div id="layoutList-head" style="overflow:auto;height:437px">
          <ul id="layoutList-ul" v-for="e in all" :key="e.size">
            <li style="width:60%">
              <div v-if = "e.ok === true">
                  <input class='text' type="text" v-model="e.list">
                  <button type="button" name="button" @click="NewFolderSubmit()">确认</button>
                  <button type="button" name="button" @click="NewFolderCancel()">取消</button>
              </div>
              <div v-else-if = "e.size === -1">
                <router-link :to="{path: '/main/', query: {id: e.listid}}" class="a-folder text">{{ e.list }}</router-link>
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
              <button type="button" name="button" @click="Download(e.listid, e.list)">下载</button>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <!-- 按钮 -->
    <input type="file" ref="btn_file" style="display:none" @change="Uploadend">
  </div>

</template>

<script>
import axios from 'axios'
axios.defaults.headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}
export default {
  name: 'app',
  data () {
    return {
      progress: '',
      path: [], // 路径
      listid: [], // 列表id
      nowid: this.$route.query.id, // 当前文件夹的listid
      list: [], // 文件列表名称
      size: [], // 文件大小
      update: [], // 更新时间
      all: [], // 上述属性的字典形式
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
        for (var i = 0; i < this.list.length; i++) {
          this.all.push({'list': this.list[i], 'listid': this.listid[i], 'size': this.size[i], 'update': this.update[i], 'ok': false})
        }
      } else {
        this.debug = res.data['data']
      }
    })
  },
  methods: {
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
          for (var i = 0; i < this.list.length; i++) {
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

<style scoped>
@import './../static/css/main.css'
</style>
