import React from 'react';
import WebSocketInstance from './WebSocket';

const withMessages = (WrappedComponent) => {
  return class extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        connected: false,
        message: '',
        messages: []
      };
    }

    waitForSocketConnection = (callback) => {
      setTimeout(() => {
        if (WebSocketInstance.state() === 1) {
          console.log('Connected');
          this.setState({
            connected: true
          })
          callback();
          return;
        } else {
          this.setState({
            connected: false
          })
          console.log('Attempting connection...');
          this.waitForSocketConnection(callback);
        }
      }, 1);
    }

    setMessages = (messages) => {
      this.setState({
        messages : messages.reverse()
      });
    }

    messageChangeHandler = (e) => {
      this.setState({
        message : e.target.value
      });
    }

    sendMessageHandler = (e, message) => {
      const messageObject = {
        text: message
      };
      WebSocketInstance.newChatMessage(messageObject);
      this.setState({
        message : ''
      });
      e.preventDefault();
    }

    addMessage = (message) => {
      this.setState({
        messages : [...this.state.messages, message]
      });
    }

    renderLoader() {
      return (
        <div className="loader" uk-spinner="ratio: 1"/>
      )
    }

    renderConnectionMessage(limit = 20) {
      return (
        <div className="connection-message">
          <small>
            {`You're connected! Displaying the last ${limit} messages.`}
          </small>
          <hr/>
        </div>
      )
    }

    renderMessages(messages, currentChatUser, self, other) {
      return messages.map((message, i) => {
        const userClass = message.author === currentChatUser ? self : other;
        return (
          <li key={i} className="chat-messages uk-animation-fade">
            <div className={userClass}>
              <p> {message.text} </p>
              <small>{message.time}</small>
            </div>
          </li>
        )
      });
    }

    render() {
      const methods = {
        renderConnectionMessage: this.renderConnectionMessage,
        renderMessages: this.renderMessages,
        renderLoader: this.renderLoader,
        waitForSocketConnection: this.waitForSocketConnection,
        sendMessageHandler: this.sendMessageHandler,
        messageChangeHandler: this.messageChangeHandler,
        addMessage: this.addMessage,
        setMessages: this.setMessages
      }
      return (
        <>
          <WrappedComponent
            {...methods}
            {...this.props}
            connected={this.state.connected}
            messages={this.state.messages}
            message={this.state.message}
          />
        </>
      )
    }
  }
}

export default withMessages;
