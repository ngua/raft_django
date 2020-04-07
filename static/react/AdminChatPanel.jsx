import React from 'react';
import WebSocketInstance from './WebSocket';
import ChatForm from './ChatForm';
import withMessages from './withMessages';

class AdminChatPanel extends React.Component {
  constructor(props) {
    super(props);

    this.messagesEndRef = React.createRef();
  }

  waitForSocketConnection() {
    this.props.waitForSocketConnection();
  }

  componentDidMount() {
    this.props.waitForSocketConnection(() => {
      WebSocketInstance.bindCallbacks(this.props.setMessages, this.props.addMessage);
      WebSocketInstance.fetchMessages();
    });
    this.scrollToBottom();
  }

  componentDidUpdate() {
    this.scrollToBottom();
  }

  scrollToBottom = () => {
    this.messagesEndRef.current.scrollIntoView({behavior: 'smooth'});
  }

  render() {
    const message = this.props.message;
    const messages = this.props.messages;
    const currentChatUser = 'admin';
    const methods = {
      messageChangeHandler: this.props.messageChangeHandler,
      sendMessageHandler: this.props.sendMessageHandler
    };
    return (
      <div>
        { this.props.currentRoom ? (this.props.renderConnectionMessage()) : ( this.props.renderLoader())}
        <hr/>
        <ul>
          { messages && this.props.renderMessages(messages, currentChatUser, 'user', 'admin') }
        </ul>
        <div ref={this.messagesEndRef}/>
        <ChatForm
          formClass={'uk-dark'}
          message={message}
          {...methods}
        />
      </div>
    )
  }
}

export default withMessages(AdminChatPanel);
