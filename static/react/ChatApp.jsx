import React from 'react';
import { v4 as uuidv4 } from 'uuid';
import ChatButton from './ChatButton';
import ChatBox from './ChatBox';
import WebSocketInstance from './WebSocket';


class ChatApp extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      active: false,
      uid: ''
    };
    this.handleOpen = this.handleOpen.bind(this);
    this.handleClose = this.handleClose.bind(this);
  }

  handleOpen(uid) {
    this.setState((state) => {
      return {
        active: true, uid: state.uid === '' ? uid : state.uid}
    },() => {
      WebSocketInstance.connect();
      console.log(this.state);
    });
  }

  handleClose() {
    this.setState({
      active: false
    })
    console.log(this.state.uid);
  }

  render() {
    const uid = this.state.uid;
    return (
      <div className="uk-animation-slide-top">
        { this.state.active ? (
          <ChatBox
            closeChatBox={this.handleClose}
            currentChatUser={uid}
          />
        ) : (
          <ChatButton
            openChatBox={this.handleOpen}
          />
        )}
      </div>
    )
  }

}

export default ChatApp;
