import React from 'react';
import UIkit from 'uikit';
import Icons from 'uikit/dist/js/uikit-icons';

UIkit.use(Icons);

class ChatBox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            message: '',
            messages : []
        };
        this.messageHandler = this.messageHandler.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    messageHandler(e) {
        this.setState({
            message: e.target.value
        });
    }
    handleSubmit(e) {
        console.log(this.state.messages);
        e.preventDefault();
    }
    render() {
        return (
          <div className="uk-grid uk-width-1-4@m uk-align-right">
            <fieldset className="uk-fieldset uk-light">
              <form className="uk-form uk-align-right">
                <div className="uk-inline">
                  <input
                    type="text"
                    className="uk-input"
                    placeholder="..."
                    value={this.state.message}
                    onChange={this.messageHandler}
                    onSubmit={this.handleSubmit}
                  />
                </div>
                <div className="uk-inline">
                  <button type="submit" className="uk-button uk-button-default" value="submit">Send</button>
                  <span className="uk-form-icon uk-dark" uk-icon="icon: reply"></span>
                </div>
              </form>
            </fieldset>
          </div>
        )

    }
}

export default ChatBox;
