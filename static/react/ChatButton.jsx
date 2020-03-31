import React from 'react';
import UIkit from 'uikit';
import Icons from 'uikit/dist/js/uikit-icons';

UIkit.use(Icons);

class ChatButton extends React.Component {
    render() {
        return <button className="uk-align-right uk-button uk-button-primary uk-light uk-margin-right">
            <span uk-icon="icon: commenting" className="uk-margin-right"></span>
            Chat Now
        </button>
    }
}

export default ChatButton;
