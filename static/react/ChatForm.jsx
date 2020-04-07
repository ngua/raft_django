import React from 'react';

class ChatForm extends React.Component {
  render() {
    const message = this.props.message;
    const textareaStyle = {
      resize: 'none',
      maxWidth: '80%'
    };
    return (
      <>
        <fieldset className={`uk-fieldset uk-text-center ${this.props.formClass}`}>
          <form className="uk-form" onSubmit={(e) => {this.props.sendMessageHandler(e, message)}}>
            <textarea
              type="text"
              className="uk-textarea"
              placeholder="..."
              rows="2"
              style={textareaStyle}
              value={message}
              onChange={this.props.messageChangeHandler}
            />
            <div className={`${this.props.inline ? 'uk-inline' : ''} uk-padding-small uk-padding-remove-horizontal`}>
              <button type="submit" className="uk-button uk-button-default" value="submit"> Send</button>
            </div>
          </form>
        </fieldset>
      </>
    )
  }
}

export default ChatForm;
