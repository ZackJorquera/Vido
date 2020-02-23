import React from 'react';
import Player from './Player'
import logo from './Logo.png'
import Loading from './Loading'

class Main extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      vidPath: '',
      finUpload: false,
      loading: false,
      youtube: '',
    };

    this.handleUpload = this.handleUpload.bind(this);
  }

  handleUpload(ev) {
      ev.preventDefault();

    const data = new FormData();
    data.append('file', this.uploadInput.files[0]);
    data.append('youtube_url', this.youtube.value);
    this.setState({
      loading: true,
    });

    fetch('http://localhost:5000/upload_file', {
      method: 'POST',
      body: data,
    }).then((response) => {
      {console.log(response)}
      {console.log(this.state.loading)}
      response.json().then((body) => {
        {console.log(body)}
        this.setState({
          vidPath: `http://localhost:5000/${body.out_file}` ,
          finUpload: true,
          loading: false,
          });
        {console.log(this.state.loading)}
      });
    });
  }
  render() {
    return (
      <div id='mainContainer' style={{display: 'flex',flexDirection: 'column', justifyContent: 'center', alignItems: 'center'}}>

        <div style={{ display: 'flex', flexDirection: 'row'}}>

          <img src={logo} style={{height: 75, marginTop: 25}}/>
          <h1 style={{fontSize: 75, fontWeight: 700, paddingTop: 15,  paddingRight: 15, paddingBottom: 15, fontFamily: 'Roboto'}}>Vido</h1>


          <form
          style={{
            marginTop: 35,
          }}
          onSubmit={this.handleUpload}>
                <input
                style={{
                  color: "9048cf",
                  margin: 10,
                  width: 300,
                }} class="button button-outline"
                ref={(ref) => { this.uploadInput = ref; }} type="file" />
            <div>
              <input style={{
                color: "9048cf",
                width: 300,
                marginLeft: 10,
              }} class="button button-outline" ref={(ref) => { this.youtube = ref; }} type="text" name="youtube_url" placeholder="Or enter Youtube Video" />
            </div>
              <button
              style={{
                marginLeft: 10,
              }}
              class = "button"
              >Upload</button>
          </form>
          </div>
      { this.state.loading ?
        <div>
          <Loading />
        </div>
      : null }
        { this.state.finUpload ?
        <div
          style={{position: 'absolute', marginHorizontal: 200, top: 200, left: 50, height: 0, width: 0}}
        >
          <Player path={this.state.vidPath} />
        </div>
         : null }
      </div>
    );
  }
}

export default Main;
