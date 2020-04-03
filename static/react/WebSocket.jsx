import config from './config';


class WebSocketService {
  static instance = null;
  callbacks = {};

  static getInstance() {
    if (!WebSocketService.instance) {
      WebSocketService.instance = new WebSocketService();
    }
    return WebSocketService.instance;
  }

  constructor() {
    this.socketRef = null;
  }

  connect(uid) {
    const path = config.API_PATH + uid + '/'
    console.log(path)
    this.socketRef = new WebSocket(path);

    this.socketRef.onmessage = e => {
      this.socketNewMessage(e.data);
    };

    this.socketRef.onerror = e => {
      console.log(e.message);
    };

    this.socketRef.onclose = () => {
      this.connect(uid);
    };

  }
  socketNewMessage(data){
    const parsedData = JSON.parse(data);
    const command = parsedData.command;

    if (Object.keys(this.callbacks).length === 0){
      return;
    }

    if (command === 'list_messages') {
      this.callbacks[command](parsedData.messages);
    } else if (command === 'new_message') {
      this.callbacks[command](parsedData.message);
    }

  }

  fetchMessages(uid) {
    this.sendMessage({command: 'list_messages', uid: uid});
  }

  newChatMessage(message) {
    this.sendMessage({command: 'new_message', from: message.from, text: message.text});
  }

  bindCallbacks(messagesCallback, newMessageCallback) {
    this.callbacks['messages'] = messagesCallback;
    this.callbacks['new_message'] = newMessageCallback;
  }

  sendMessage(data) {
    try {
      this.socketRef.send(JSON.stringify({...data}))
    }
    catch(error){
      console.log(`Error: ${error}`);
    }
  }

  state() {
    return this.socketRef.readyState;
  }

  waitForSocketConnection(callback) {
    const socket = this.socketRef;
    const recursion = this.waitForSocketConnection;
    setTimeout(
      () => {
        if(socket.readyState === 1){
          console.log("Connection");
          if(callback != null){
            callback();
          }
          return;
        }
        else{
          console.log("Wait for connection..");
          recursion(callback);
        }
      }, 1);
  }

}

let WebSocketInstance = WebSocketService.getInstance();

export default WebSocketInstance;
