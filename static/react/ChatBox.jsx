import React from 'react';
import UIkit from 'uikit';
import Icons from 'uikit/dist/js/uikit-icons';
import ChatForm from './ChatForm';
import withMessages from './withMessages';

UIkit.use(Icons);

class ChatBox extends React.Component {
  constructor(props) {
    super(props);
    this.messagesEndRef = React.createRef();
    this.closeChatBox = this.closeChatBox.bind(this);
  }

  waitForSocketConnection() {
    this.props.waitForSocketConnection();
  }

  scrollToBottom = () => {
    this.messagesEndRef.current.scrollIntoView({behavior: 'smooth'});
  }

  componentDidMount() {
    this.props.waitForSocketConnection(() => {
      this.props.ws.bindCallbacks(this.props.setMessages, this.props.addMessage);
      this.props.ws.fetchMessages();
    });
    this.scrollToBottom();
  }

  componentDidUpdate() {
    this.scrollToBottom();
  }

  closeChatBox() {
    this.props.closeChatBox();
  }

  render() {
    const connected = this.props.connected;
    const message = this.props.message;
    const messages = this.props.messages;
    const methods = {
      messageChangeHandler: this.props.messageChangeHandler,
      sendMessageHandler: this.props.sendMessageHandler
    };
    const currentChatUser = this.props.currentChatUser;
    const limit = JSON.parse(document.querySelector('#chat-limit').textContent)['chat-limit'];
    return (
      <div className="chat-box uk-background-secondary uk-grid uk-width-1-2@s uk-width-1-4@m uk-margin uk-animation-slide-bottom uk-box-shadow-large">
        <div className="close-chat">
          <button type="button" uk-icon="icon: close" className="uk-align-right uk-margin-remove" onClick={this.closeChatBox}/>
        </div>
        <div className="chat-container">
          <div className="uk-align-center">
            { connected ?
                ( this.props.renderConnectionMessage(limit) ) : ( this.props.renderLoader() )
            }
            <ul>
              { messages && this.props.renderMessages(messages, currentChatUser) }
            </ul>
          </div>
          <div ref={this.messagesEndRef}/>
        </div>
        <ChatForm
          inline={true}
          formClass={'uk-light'}
          message={message}
          {...methods}
        />
      </div>
    )
  }
}

export default withMessages(ChatBox);
