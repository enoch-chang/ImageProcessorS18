import React from 'react';
import TitleBar from './TitleBar.js';
import GetInfo from './TextInput.js';
import MainPage from './MainPage.js';
import { withStyles } from 'material-ui/styles';


const styles = {
    root: {
        flexGrow: 1,
    },
    flex: {
        flex: 1,
    },
}

class App extends React.Component {
    // One thing every component must do:
    // define the render method
    // (this defines the view of the component)
    render() {
        return (
            <div>
                <TitleBar />
                <MainPage />
            </div>
    );
    }
}

export default App;