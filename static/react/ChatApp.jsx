import React from 'react';
import ChatButton from './ChatButton';
import ChatBox from './ChatBox';


class ChatApp extends React.Component {
    constructor(props) {
        super(props);
        this.clickHandler = this.clickHandler.bind(this);
        this.state = {
            clicked: false
        };
    }
    clickHandler() {
        this.setState({
            clicked: true
        });
    }
    render() {
        return <div onClick={this.clickHandler} className="">
            { this.state.clicked ? (
                <ChatBox />
            ) : (
                <ChatButton />
            )}
        </div>
    }
}

export default ChatApp;
