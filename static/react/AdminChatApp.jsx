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
      ws: null,
      active: false
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

  setRooms() {
    this.fetchRooms()
      .then(
        (result) => {
          this.setState({rooms: result.rooms}, () => {
            if (this.state.rooms.length !== 0 ) {
              this.selectRoom(result.rooms[0]);
            }
          });
        },
        (error) => {
          console.log(`Error: ${error}`);
        }
      )
  }

  componentDidMount() {
    this.setRooms();
  }

  selectRoom = (room) => {
    this.setState((state) => {
      return {
        currentRoom: room,
        active: !state.active
      }
    }, () => {
      const path = `ws://${window.location.host}/ws/chat/admin/${this.state.currentRoom.id}/`
      const ws = new WebSocketService(path);
      this.setState({ ws: ws, active: true }, () => {
        this.state.ws.connect();
      })
    });
  }

  render() {
    const rooms = this.state.rooms;
    const roomListStyle = {
      listStyleType: 'none'
    };
    return (
      <>
        { this.state.active? (
          <div uk-grid="true">
            <div className="uk-width-1-5@m">
              <div>
                <ul className="uk-tab-left" uk-tab="">
                  <AdminRoomList
                    {...this.state}
                    selectRoom={this.selectRoom}
                  />
                </ul>
              </div>
            </div>
            <div className="uk-width-expand@m">
              <div className="">
                <AdminChatPanel {...this.state} currentChatUser={'admin'} />
              </div>
            </div>
          </div>
        ) : (
          <section className={'uk-section uk-section-muted uk-section-large'}>
            <div className="uk-container">
              <h1>No active rooms</h1>
              <div className="uk-width-1-1@m">
                <p>No chat rooms are currently active.</p>
              </div>
            </div>
          </section>
        )}
      </>
    )
  }
}

export default AdminChatApp;
