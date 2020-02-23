import React from 'react';
import Player from './Player'

class Main extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      vidPath: '',
      fileUploaded: false,
    };

    this.handleUploadImage = this.handleUploadImage.bind(this);
  }

  handleUploadImage(ev) {
    ev.preventDefault();

    const data = new FormData();
    data.append('file', this.uploadInput.files[0]);
  {/*  data.append('filename', this.fileName.value); */}
  {/*  data.append('percentage', this.percentage.value) */}

    fetch('http://localhost:5000/upload_file', {
      method: 'POST',
      body: data,
    }).then((response) => {
      {console.log(response)}
      response.json().then((body) => {
        {console.log(body)}
        this.setState({ vidPath: `http://localhost:5000/${body.out_file}` });
      });
    });
  }
  render() {
    return (
      <div style={{
        display: 'flex',
        backgroundColor: "#ffffff",
        textAign: 'center',
        justifyContent: 'center',
        fontFamily: 'Gill Sans',
      }}>
      <div style={{flexDirection: 'row'}}>
        <h1 style={{fontSize: 50, fontWeight: 700}}>Vido</h1>
        <br></br>
        <form onSubmit={this.handleUploadImage}>
          <div>
            <label style={{
              color: "9048cf",
              display: 'inline-block',
              overflow: 'hidden',
              size: '0',
            }} class="button">
              <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
            </label>
          </div>
          {/*
          <div>
            <input ref={(ref) => { this.fileName = ref; }} type="text" placeholder="Enter the desired name of file" />
          </div>
        */}
          <br />
          <div>
            <button>Upload</button>
          </div>
        </form>
        </div>
        <div style={{flexDirection: 'row', lex:0.8, borderWidth:1}}>
          <Player path={this.state.vidPath} />
        </div>
      </div>
    );
  }
}

export default Main;
