import React from 'react';

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
    data.append('filename', this.fileName.value);
    data.append('percentage', this.percentage.value)

    fetch('http://localhost:5000/upload_file', {
      method: 'POST',
      body: data,
    }).then((response) => {
      console.log(response)
      response.json().then((body) => {
        this.setState({ vidPath: `http://localhost:5000/${body.file}` });
      });
    });
  }

  render() {
    return (
      <div>
        <form onSubmit={this.handleUploadImage}>
          <div>
            <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
          </div>
          //<div>
          //  <input ref={(ref) => { this.fileName = ref; }} type="text" placeholder="Enter the desired name of file" />
          //</div>
          <br />
          <div>
            <button>Upload</button>
          </div>
        </form>
        <div>
          <Player path={this.state.vidPath} />
        </div>
      </div>
    );
  }
}

export default Main;
