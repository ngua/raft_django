import React from 'react';

class AdminRoomList extends React.Component {
  render() {
    const rooms = this.props.rooms;
    const roomListStyle = {
      listStyleType: 'none'
    };
    return (
      rooms.map((room) => {
        return (
          <li key={room.id} style={roomListStyle} className={room === this.props.currentRoom ? 'uk-active' : ''}>
            <a onClick={() => this.props.selectRoom(room)} href="#">{room.pk}</a>
          </li>
        )
      })
    )
  }
}

export default AdminRoomList;
