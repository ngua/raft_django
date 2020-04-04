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
    const path = `ws://${window.location.host}/ws/chat/${uid}/`
    this.socketRef = new WebSocket(path);

    this.socketRef.onmessage = e => {
      this.socketNewMessage(e.data);
    };

    this.socketRef.onerror = e => {
      console.log(e);
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

    if (command === 'messages') {
      this.callbacks[command](parsedData.messages);
    } else if (command === 'new-message') {
      this.callbacks[command](parsedData.message);
    }

  }

  fetchMessages() {
    this.sendMessage({command: 'list-messages'});
  }

  newChatMessage(message) {
    this.sendMessage({command: 'new-message', from: message.from, text: message.text});
  }

  bindCallbacks(setMessages, addMessage) {
    this.callbacks['messages'] = setMessages;
    this.callbacks['new-message'] = addMessage;
  }

  sendMessage(data) {
    try {
      this.socketRef.send(JSON.stringify({...data}))
    }
    catch(error) {
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
          console.log("Connected");
          if(callback != null){
            callback();
          }
          return;
        } else {
          console.log("Waiting to connect...");
        }
      }, 100);
  }

}

let WebSocketInstance = WebSocketService.getInstance();

export default WebSocketInstance;
