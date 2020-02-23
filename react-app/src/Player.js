import React from 'react';
import { Player, LoadingSpinner, ControlBar, PlayToggle } from 'video-react';

export default props => {
  return (
    <div>
    <Player
      playsInline
      src={props.path}
      style={{display: 'flex', flexDirecton: 'row', fluid: false, width: 0}}
      >

      <LoadingSpinner />
      <ControlBar disabled>
        <PlayToggle disabled/>
      </ControlBar>
    </Player>
    </div>
  );
};
