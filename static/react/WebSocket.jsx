class WebSocketService {
  callbacks = {};
  constructor(path) {
    this.connect(path);
  }

  connect(path) {
    this.socketRef = new WebSocket(path);

    this.socketRef.onmessage = e => {
      this.socketNewMessage(e.data);
    };

    this.socketRef.onerror = e => {
      console.log(e);
    };

    this.socketRef.onclose = () => {
      this.connect(path);
    };

  }

  close() {
    this.socketRef.close();
  }

  socketNewMessage(data){
    console.log('called');
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

  bindCallbacks = (setMessages, addMessage) => {
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

}

export default WebSocketService;
