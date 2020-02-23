import React from 'react';
import { Player } from 'video-react';

export default props => {
  return (
    <Player
      playsInline
      src={props.path}
    />
  );
};
