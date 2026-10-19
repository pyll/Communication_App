<template>
  <div id="app">
    <input type="button" @click="getMsg" value="get" />
    <div>
      <p>用户名</p>
      <p>{{username}}</p>
      <p>性别</p>
      <p>{{gender}}</p>
      <p>学校</p>
      <p>{{school}}</p>
      <p></p>
    </div>
    
    <textarea id="chat-log" cols="100" rows="20" v-model="comemessage"></textarea><br/>
    <input id="chat-message-input" v-model="content" type="text" size="100"/><br/>
    <!--<input id="chat-message-submit" type="button" value="Send"/>-->

    <input id="chat-message-submit" value="send" type="button" @click="websocketsend"/>

  </div>
</template>

<script>
import Axios from 'axios'
export default {
  name: 'app',
  data () {
    return {
      username: 'orz',
      gender: '',
      school: '',
      to_user: 'lol',
      content: '',
      comemessage: '',
    }
  },
  computed: {
    room_name: function(){
      return this.username + '_' + this.to_user;
    }
  },

  created() {
    Axios.post("http://127.0.0.1:8000/user/getUserInfo?token=7ddf3a2e42f243ad5a9c377752e94f46")
    .then(function (response) {
      console.log('getMsg');
      this.username = response.data.info.username;
      this.gender = response.data.info.gender;
      this.school = response.data.info.school;
    });
    setTimeout(this.initWebSocket(), 10000);
  },
  methods: {
    initWebSocket(){
      const wsuri = `ws://127.0.0.1:8000/talk/websocketLink/${this.room_name}`;
      console.log('wsuri: ', wsuri);
      //alert(`地址：${wsuri}`)
      this.websock = new WebSocket(wsuri);
      this.websock.onmessage = this.websocketonmessage;
      this.websock.onopen = this.websocketonopen;
      this.websock.onerror = this.websocketonerror;
      this.websock.onclose = this.websocketclose;
    },
    //连接建立  
    websocketonopen(){ 
      console.log('WebSocket连接成功')
    },
    //连接建立失败重连
    websocketonerror(e){
      console.log(`连接失败的信息：${e}`);
      setTimeout("this.initWebSocket()", 3000);
    },
    //数据接收
    websocketonmessage(e){ 
      console.log('message: ' + e.data);//打印服务端返回的数据
      var data = JSON.parse(e.data);
      this.comemessage += 'from: ' + data['from_user'] + '\nto: ' + data['to_user'] + '\nsend: ' + data['content'] + '\ntime: ' + data['time'] + '\n\n';
      // var data = e.data
      // var message = data['message'];
      // document.querySelector('#chat-log').value += (message + '\n');
    },
    websocketclose(e){ 
      if(this.websock)
        console.log('websocketclose断开连接',e);
        this.websock.close()
    },

    websocketsend(){
      if(!this.websock){
        console.log("Please connect server.");
      }
      this.websock.send(JSON.stringify({'roomname': this.room_name, 'from_user': this.username, 'to_user': this.to_user, 'content': this.content}));//发送json数据类型
      this.content = '';
    },
    getMsg(){
      Axios.post("http://120.78.91.11:8000/user/getUserInfo?token=7ddf3a2e42f243ad5a9c377752e94f46")
      .then(function (response) {
        console.log('getMsg');
        this.username = response.data.info.username;
        this.gender = response.data.info.gender;
        this.school = response.data.info.school;
      });
    },
  },
  mounted () { 
  },
  destroyed() {
    //关闭websocket连接
    console.log('destroying')
    this.websock.close()
  },
}
</script>

<style>

</style>
