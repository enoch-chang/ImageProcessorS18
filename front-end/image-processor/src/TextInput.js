import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import TextField from 'material-ui/TextField';
import axios from 'axios';
import Button from 'material-ui/Button';
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table';
import Paper from 'material-ui/Paper';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';
import Upload from 'material-ui-next-upload/Upload';
import List, { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import Card, { CardActions, CardContent, CardMedia } from 'material-ui/Card';
import Typography from 'material-ui/Typography';
import Tabs, { Tab } from 'material-ui/Tabs';
import AppBar from 'material-ui/AppBar';
import SwipeableViews from 'react-swipeable-views';
import Menu, { MenuItem } from 'material-ui/Menu';


function TabContainer({ children, dir }) {
    return (
        <Typography component="div" dir={dir} style={{ padding: 8 * 3 }}>
            {children}
        </Typography>
    );
}

var styles = {
    "blockStyle": {
        "padding": "20px",
        "marginLeft": "auto",
        "marginRight": "auto",
        "marginTop": "20px",
        }
}

class GetInfo extends React.Component{
    constructor(){
        super();
        this.state = {
            "email":["Enter patient e-mail"],
            "hr": ["Nothing yet"],
            "hr_times": ["Nothing yet"],
            "id": [],
            "data": [['Frozen yoghurt', 159, 6.0, 24, 4.0], ['Ice cream sandwich', 237, 9.0, 37, 4.3]],
            "test":"Rich",
            "process":"",
            "tab_test":"0",
            "id":"",
        };

    }

    onFileLoad = (e, file) => console.log(e.target.result, file.name);

    // Tabs

    handleChange = (event, value) => {
        this.setState({ value });
    };

    handleChangeIndex = index => {
        this.setState({ value: index });
    };

    // Menu

    handleClick = event => {
        this.setState({ anchorEl: event.currentTarget });
    };

    handleClose = () => {
        this.setState({ anchorEl: null });
    };


    TypeInput = (event) => {
        console.log(this.email);
        this.setState({"email": event.target.value});
        }

    getAllFiles = () => {
        var URL = "http://vcm-3608.vm.duke.edu:5000/api/heart_rate/".concat(this.state.email)
        axios.get(URL).then( (response) => {
            console.log(response);
            console.log(response.status);
            var list = [];
            for (var i = 0; i <= (response.data["heart_rate"]).length-1; i++) {
                list.push(i);
            }
            this.setState({"hr": response.data["heart_rate"],
                           "hr_times": response.data["times"],
                            "id": list});
            console.log(this.state)
        })
    }

    onListClick = (event) => {
        this.setState({"test":"Zhiwei"})
    }


    onButtonClick = (event) => {
        console.log(this.state.email)
        this.getData()
    }

    render () {

        const { anchorEl } = this.state;

        // if this.state.tab_test == 2 {}


        return(

            <div>
                <Paper style = {{"width":"600px", "margin": "auto"}} >
                <div style={styles.blockStyle}>
                <TextField id="email"
                          label="E-mail"
                          value={this.state.email}
                          onChange = {this.TypeInput}
                          color="secondary"

               />
                <Button variant="raised" onClick={this.onButtonClick}
                        style={{"float":"right"}}
                        color="secondary">
                    LOG IN
                </Button>
                </div >
                </Paper>

        <Paper style = {{"width":"600px", "margin": "auto"}} >
    <div style={styles.blockStyle}>
    <Upload label="Add" onFileLoad={this.onFileLoad}/>
        <Button variant="raised" onClick={this.onButtonClick}
        style={{"marginLeft":"220px"}}
        color="secondary">
            Upload
            </Button>
        {/* Refresh the table below*/}
        </div>
        </Paper>

                <div style={styles.blockStyle}>

                <Paper style = {{"width":"600px", "margin": "auto"}} >

                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell style={{"textAlign":"left"}}>Filename</TableCell>
                                <TableCell numeric style={{"textAlign":"left"}}>Date Added</TableCell>
                            </TableRow>
                        </TableHead>
                    </Table>

                    <List component="nav">

                            {(this.state.data).map(n => {         {/* Should probably (this.state.images)*/}
                                return (
                                    <ListItem button component="a" href="#simple-list" onClick={this.onListClick}>
                                        <ListItemText primary={n[1]}  style={{"textAlign":"left"}}/>
                                        <ListItemText primary={n[2]}  style={{"textAlign":"left"}}/>
                                    </ListItem>

                                );
                            })}

                    </List>
                    Hello {this.state.test}

                </Paper>
                </div>


                <div style={styles.blockStyle}>
                    <Paper style = {{"width":"600px", "margin": "auto"}} >
                    <img src="images/paris.jpg" style={{"width":"550px", "marginLeft":"20px", "marginTop":"20px", "marginRight":"20px"}} alt="Paris"/>


                        <AppBar position="static" color="default">
                            <Tabs
                                value={this.state.value}
                                onChange={this.handleChange}
                                indicatorColor="primary"
                                textColor="primary"
                                fullWidth
                            >
                                <Tab label="Original" />
                                <Tab label="Processed"/>
                            </Tabs>
                        </AppBar>
                        <SwipeableViews
                            index={this.state.value}
                            onChangeIndex={this.handleChangeIndex}
                        >
                            <TabContainer>

                                <LineChart width={550} height={200}
                                           data={(this.state.id).map(n => {
                                               return (
                                                   {name: this.state.hr_times[n], value: this.state.hr[n]}
                                               );
                                           })}
                                           margin={{ top: 15, right: 5, bottom: 5, left: 5 }}>
                                    <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                                    <XAxis dataKey="name" />
                                    <YAxis />
                                    <Tooltip />
                                    <Line type="monotone" dataKey="value" stroke="#8884d8" activeDot={{r: 8}} />
                                </LineChart>

                                <Card>
                                    <CardContent>
                                        <Typography gutterBottom variant="headline" component="h2">
                                            Lizard
                                        </Typography>
                                        <Typography component="p">
                                            Lizards are a widespread group of squamate reptiles, with over 6,000 species, ranging
                                            across all continents except Antarctica
                                        </Typography>
                                    </CardContent>
                                </Card>

                            </TabContainer>
                            <TabContainer>
                                <LineChart width={550} height={200}
                                           data={(this.state.id).map(n => {
                                               return (
                                                   {name: this.state.hr_times[n], value: this.state.hr[n]}
                                               );
                                           })}
                                           margin={{ top: 15, right: 5, bottom: 5, left: 5 }}>
                                    <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                                    <XAxis dataKey="name" />
                                    <YAxis />
                                    <Tooltip />
                                    <Line type="monotone" dataKey="value" stroke="#8884d8" activeDot={{r: 8}} />
                                </LineChart>

                                <Card>
                                    <CardContent>
                                        <Typography gutterBottom variant="headline" component="h2">
                                            Dogs
                                        </Typography>
                                        <Typography component="p">
                                            Dogs are a widespread group of squamate reptiles, with over 6,000 species, ranging
                                            across all continents except Antarctica
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </TabContainer>
                        </SwipeableViews>
                    </Paper>
            </div>

                <div style={styles.blockStyle}>

                <Paper style = {{"width":"600px", "margin": "auto", "marginBottom":"50px"}} >

                    <Button
                        aria-owns={anchorEl ? 'simple-menu' : null}
                        aria-haspopup="true"
                        onClick={this.handleClick}
                    >
                        Open Menu
                    </Button>
                    <Menu
                        id="simple-menu"
                        anchorEl={anchorEl}
                        open={Boolean(anchorEl)}
                        onClose={this.handleClose}
                    >
                        <MenuItem onClick={this.handleClose}>Profile</MenuItem>
                        <MenuItem onClick={this.handleClose}>My account</MenuItem>
                        <MenuItem onClick={this.handleClose}>Logout</MenuItem>
                    </Menu>

                </Paper>
                </div>
            </div>

            );
            }

    }
export default GetInfo;