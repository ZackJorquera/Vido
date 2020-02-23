import React from 'react';
import { Player } from 'video-react';
import "node_modules/video-react/dist/video-react.css"; // import css

export default props => {
  return (
    <Player
      playsInline
      src={props.path}
    />
  );
};
