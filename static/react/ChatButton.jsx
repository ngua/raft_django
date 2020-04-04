import React from 'react';
import UIkit from 'uikit';
import Icons from 'uikit/dist/js/uikit-icons';

UIkit.use(Icons);

class ChatButton extends React.Component {
  constructor(props) {
    super(props);
    this.openChatBox = this.openChatBox.bind(this);
  }
  openChatBox() {
    const sessionUid = JSON.parse(document.querySelector('#session-uid').textContent);
    const uid = sessionUid['chat-uid'];
    this.props.openChatBox(uid);
  }
  render() {
    return (
      <button
        className="uk-align-right uk-button uk-button-primary uk-light uk-margin-right uk-animation-slide-bottom"
        onClick={this.openChatBox}
      >
        <span uk-icon="icon: commenting" className="uk-margin-right"></span>
        Chat Now
      </button>
    )
  }
}

export default ChatButton;
