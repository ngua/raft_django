import React from 'react';
import ChatButton from './ChatButton';
import ChatBox from './ChatBox';
import WebSocketInstance from './WebSocket';

class ChatApp extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      active: false,
      chatUid: ''
    };
    this.handleOpen = this.handleOpen.bind(this);
    this.handleClose = this.handleClose.bind(this);
  }

  handleOpen(chatUid) {
    this.setState((state) => {
      return {
        active: true,
        chatUid: state.chatUid === '' ? chatUid : state.chatUid
      }
    },() => {
      const path = `ws://${window.location.host}/ws/chat/${chatUid}/`
      WebSocketInstance.connect(path);
    });
  }

  handleClose() {
    this.setState({
      active: false
    })
  }

  render() {
    const {active, chatUid} = this.state;
    return (
      <div className="uk-animation-slide-top">
        { active ? (
          <ChatBox
            closeChatBox={this.handleClose}
            currentChatUser={chatUid}
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
