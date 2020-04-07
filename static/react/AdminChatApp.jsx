import React from 'react';
import AdminRoomList from './AdminRoomList';
import AdminChatPanel from './AdminChatPanel';
import WebSocketService from './WebSocket';


class AdminChatApp extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      rooms: [],
      currentRoom: '',
      ws: null
    };
  }

  fetchRooms = async () => {
    const path = `http://${window.location.host}/chat/rooms/`
    const response = await fetch(path, {
      method: 'POST',
    });
    const result = await response.json();
    return result;
  }

  componentDidMount() {
    this.fetchRooms()
      .then(
        (result) => {
          this.setState({rooms: result.rooms});
        },
        (error) => {
          console.log(`Error: ${error}`);
        }
      )
  }

  selectRoom = (room) => {
    this.setState((state) => {
      return {
        currentRoom: room !== state.currentRoom ? room : state.currentRoom
      }
    }, () => {
      const path = `ws://${window.location.host}/ws/chat/admin/${this.state.currentRoom.id}/`
      const ws = new WebSocketService(path);
      this.setState({ ws: ws }, () => {
        this.state.ws.connect(path);
      })
    });
  }

  renderChat() {
    return (
      <div className="uk-width-expand@m">
        { <AdminChatPanel {...this.state} /> }
      </div>
    )
  }

  render() {
    const rooms = this.state.rooms;
    const roomListStyle = {
      listStyleType: 'none'
    };
    return (
      <div uk-grid="true">
        <div className="uk-width-auto@m">
          <ul className="uk-tab-left" uk-tab="">
            <AdminRoomList
              {...this.state}
              selectRoom={this.selectRoom}
            />
          </ul>
        </div>
        {this.state.currentRoom && this.renderChat()}
      </div>
    )
  }
}

export default AdminChatApp;
