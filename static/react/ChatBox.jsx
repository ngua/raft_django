import React from 'react';
import UIkit from 'uikit';
import Icons from 'uikit/dist/js/uikit-icons';
import WebSocketInstance from './WebSocket'

UIkit.use(Icons);

class ChatBox extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      connected: false,
      message: '',
      messages: []
    };
    this.waitForSocketConnection(() => {
      WebSocketInstance.bindCallbacks(this.setMessages.bind(this), this.addMessage.bind(this));
      WebSocketInstance.fetchMessages();
    });
    this.closeChatBox = this.closeChatBox.bind(this);
  }

  waitForSocketConnection(callback) {
    const component = this;
    setTimeout(
      () => {
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
          console.log("Attempting connection...");
          component.waitForSocketConnection(callback);
        }
      }, 100);
  }

  addMessage(message) {
    this.setState({
      messages : [...this.state.messages, message]
    });
  }

  setMessages(messages) {
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
      from: this.props.currentChatUser,
      text: message
    };
    WebSocketInstance.newChatMessage(messageObject);

    this.setState({
      message : ''
    });

    e.preventDefault();
  }

  scrollToBottom = () => {
    this.messagesEnd.scrollIntoView({behavior: 'smooth'});
  }

  componentDidMount() {
    this.scrollToBottom();
  }

  componentDidUpdate() {
    this.scrollToBottom();
  }

  componentDidCatch(error, info) {
    this.setState({
      connected: false
    });
  }


  renderConnectionMessage() {
    const limit = JSON.parse(document.querySelector('#chat-limit').textContent)['chat-limit']
    return (
      <div className="connection-message">
        <small>
          {`You're connected! Displaying the last ${limit} messages.`}
        </small>
        <hr/>
      </div>
    )
  }

  renderErrorMessage() {
    return (
      <div className="error-message">
        <h4>
          Looks like something went wrong! Trying to reconnect...
        </h4>
      </div>
    )
  }

  renderMessages(messages) {
    const currentChatUser = this.props.currentChatUser;
    return messages.map((message, i) => {
      const time = message.time;
      const userClass = message.author === currentChatUser ? "user" : "admin";
      return (
        <li key={i} className="chat-messages uk-animation-fade">
          <div className={`${userClass}`}>
            <p> {message.text} </p>
            <small>{time}</small>
          </div>
        </li>
      )
    })
  }

  closeChatBox() {
    this.props.closeChatBox();
  }

  render() {
    const messages = this.state.messages;
    const textareaStyle = {
      resize: 'none',
      maxWidth: '80%'
    };
    return (
      <div className="chat-box uk-background-secondary uk-grid uk-width-1-2@s uk-width-1-4@m uk-margin uk-animation-slide-bottom uk-box-shadow-large">
        <div className="close-chat">
          <button
            type="button" uk-icon="icon: close" className="uk-align-right uk-margin-remove"
            onClick={this.closeChatBox}
          >
          </button>
        </div>
        <div className="chat-container">
          <div className="uk-align-center">
            { this.state.connected ?
                ( this.renderConnectionMessage() ) : ( this.renderErrorMessage() )
            }
            <ul>
              { messages && this.renderMessages(messages) }
            </ul>
          </div>
          <div ref={(el) => {this.messagesEnd = el;}}></div>
        </div>
        <fieldset className="uk-fieldset uk-text-center uk-light">
          <form className="uk-form" onSubmit={(e) => {this.sendMessageHandler(e, this.state.message)}}>
            <textarea
              type="text"
              className="uk-textarea"
              placeholder="..."
              rows="2"
              style={textareaStyle}
              value={this.state.message}
              onChange={this.messageChangeHandler}
            />
            <div className="uk-inline uk-padding-small uk-padding-remove-horizontal">
              <button type="submit" className="uk-button uk-button-default" value="submit"> Send</button>
            </div>
          </form>
        </fieldset>
      </div>
    )
  }
}

export default ChatBox;
