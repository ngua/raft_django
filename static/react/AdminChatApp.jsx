import React from 'react';
import AdminRoomList from './AdminRoomList';
import AdminChatPanel from './AdminChatPanel';
import WebSocketInstance from './WebSocket';


class AdminChatApp extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      rooms: [],
      currentRoom: ''
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
          this.setState({rooms: result.rooms})
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
      WebSocketInstance.connect(path);
    });
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
        <div className="uk-width-expand@m">
          { WebSocketInstance.socketRef != null && <AdminChatPanel {...this.state} /> }
        </div>
      </div>
    )
  }
}

export default AdminChatApp;
