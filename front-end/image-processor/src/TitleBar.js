import React from 'react';
import Toolbar from 'material-ui/Toolbar'
import Typography from 'material-ui/Typography'
import AppBar from 'material-ui/AppBar';


class TitleBar extends React.Component {
    render() {
            return (
                < div >
                < AppBar position = "static" color = "secondary" >
            < Toolbar >
            < Typography variant = "title" color = "inherit">
                Image Processor
                < /Typography>
        < /Toolbar>
        < /AppBar>
        < /div>
    );
        }
}

export default TitleBar;