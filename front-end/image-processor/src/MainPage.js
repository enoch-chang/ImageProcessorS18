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
import Select from 'material-ui/Select';
import Input, { InputLabel } from 'material-ui/Input';
import ReactDOM from 'react-dom';

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

class MainPage extends React.Component {
    constructor() {
        super();
        this.state = {
            "email": ["Enter your e-mail"],
            "name": ["Enter your name"],
            "logged_in": 2,
            "images": [['Frozen yoghurt', 159, 6.0, 24, 4.0], ['Ice cream sandwich', 237, 9.0, 37, 4.3],['Eclair', 262, 16.0, 45, 6.0]],
            "disp_images": [],
            "disp": "original",
            "current_image":[],
            "processed_images":[['Cupcake', 305, 3.7, 24, 4.3],['Gingerbread', 356, 16.0, 49, 3.9]],
            "current_image_processed":[],
            "process":[],
            "tab":0,
            "id":""
        };

    }

    TypeInputEmail = (event) => {
        console.log(this.email);
        this.setState({"email": event.target.value});
    }

    TypeInputName = (event) => {
        console.log(this.name);
        this.setState({"name": event.target.value});
    }

    resetUser = (event) => {
        this.setState({
            "email": ["Enter your e-mail"],
            "name": ["Enter your name"],
            "logged_in": 0,
            "images": [],
            "disp_images": [],
            "disp": "original",
            "current_image": [],
            "processed_images": [],
            "current_image_processed": []
        })
        console.log(this.state)

    }

    logIn = (event) => {
        var URL = "http://vcm-3608.vm.duke.edu:5000/api/images/".concat(this.state.email)

        axios.get(URL).then((response) => {
            console.log(response);
            console.log(response.status);

            if (this.state.logged_in == 2){
                this.setState({
                    "name": response.data["name"],
                    "images": response.data["images"],
                    "logged_in": response.data["success"],
                    "processed_images": response.data["processed_images"],
                });
            }

            if (response.data["success"] == 1) {

                this.setState({
                    "name": response.data["name"],
                    "images": response.data["images"],
                    "logged_in": response.data["success"],
                    "processed_images": response.data["processed_images"],
                    "disp_images": response.data["images"],
                    "logged_in": 2
                });
            }
            else {
                this.setState({"logged_in":1});

            }



            console.log(this.state)
        })
    }

    createUser = (event) => {
        var URL = "http://vcm-3608.vm.duke.edu:5000/api/images/create"
        axios.post(URL,
               {"name":this.state.name,
               "email":this.state.email})
        this.logIn()
    }

    onFileLoad = (e, files) => {

    var files = e.target.result;

        for (var i=0; i<files.length; i++){
            this.uploadPOST(files[i])
        }

        this.setState({"current_image":e.target.result});

        // const reader = new FileReader()
        // const file = files[0]
        // reader.readAsDataURL(file);
        // reader.onloadend = () => {
        //     console.log(reader.result);
        //     this.setState({"current_image": reader.result})
        // }
    }

    uploadPOST = (file) => {
        var URL = "http://vcm-3608.vm.duke.edu:5000/api/images/"
        axios.post(URL,
            {"image":file,
                "email":this.state.email})

        this.logIn()

    }


    processPOST = () => {
        var URL = "http://vcm-3608.vm.duke.edu:5000/api/images/upload".concat(this.state.email)
            .concat("/").concat(this.state.current_image[0]).concat("/").concat(this.state.process) //change to ID

        axios.post(URL,{"image_id":this.state.current_image[0], "process":this.state.process}) //change to ID

        this.logIn()
        this.setState({"current_image_processed":(this.processed_images)[(this.processed_images).length-1]});

    }

    onListClick1 = (id, image) => { //holds original image array

        this.setState({"current_image_id":id,
                       "current_image":image}); // set to index of image
        var temp_image_list = [];

        for (var i = 0; i < (this.state.processed_images).length; i++){
            if (this.state.processed_images[i][3] == id){
                temp_image_list.push(this.state.processed_images[i])
            }
        }

        this.setState({"disp_images":temp_image_list,
                       "disp":"processed"});

        console.log(this.state)

    }

    onListClick2 = (image) => { //holds processed image array

        this.setState({"current_image_processed":image}); // set to index of image
        console.log(this.state)


    }

    onListBack = () => {

        this.setState({
            "disp_images":this.state.images,
            "disp":"original",
        });

    }

    viewProcessed = () => {

    }

    // Tabs

    handleChange = (event, value) => {
        this.setState({ "tab":value });
    };

    handleChangeIndex = index => {
        this.setState({ "tab": index });
    };

    // Select

    selectProcess = event => {
        this.setState({ "process": event.target.value });
    };


    render() {

        if (this.state.logged_in == 0) { // logged out state
            return (
                <div>
                    <Paper style={{"width": "600px", "margin": "auto"}}>
                        <div style={styles.blockStyle}>
                            <TextField id="email"
                                       label="E-mail"
                                       value={this.state.email}
                                       onChange={this.TypeInputEmail}
                                       color="secondary"

                            />
                            <Button variant="raised" onClick={this.logIn}
                                    style={{"float": "right"}}
                                    color="secondary">
                                LOG IN
                            </Button>
                        </div>
                    </Paper>

                </div>
            );
        }

        if (this.state.logged_in == 1) { // create new user
            return (
                <div>
                    <Paper style={{"width": "600px", "margin": "auto"}}>
                        <div style={styles.blockStyle}>

                            <TextField id="email"
                                       label="E-mail"
                                       value={this.state.email}
                                       onChange={this.TypeInputEmail}
                                       color="secondary"

                            />
                            <TextField id="name"
                                       label="Name"
                                       value={this.state.name}
                                       onChange={this.TypeInputName}
                                       color="secondary"

                            />
                            <Button variant="raised" onClick={this.createUser}
                                    style={{"float": "right"}}
                                    color="secondary">
                                CREATE NEW USER
                            </Button>
                            <Button variant="raised" onClick={this.resetUser}
                                    style={{"float": "right"}}
                                    color="secondary">
                                BACK
                            </Button>
                        </div>
                    </Paper>

                </div>
            );
        }

        if (this.state.logged_in == 2) { // logged in


            return (
                <div>
                    <Paper style={{"width": "600px", "margin": "auto"}}>
                        <div style={styles.blockStyle}>

                            Hello {this.state.name} !

                            <Button variant="raised" onClick={this.resetUser}
                                    style={{"float": "right"}}
                                    color="secondary">
                                CHANGE USER
                            </Button>
                        </div>
                    </Paper>

                    <Paper style = {{"width":"600px", "margin": "auto"}} >
                        <div style={styles.blockStyle}>
                            <Upload label="Add"  onFileLoad={this.onFileLoad}/>
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

                                {(this.state.disp_images).map(n => {

                                    if (this.state.disp == "original") {

                                        return (
                                            <ListItem button component="a"
                                                      href="#simple-list"
                                                      onClick={() => this.onListClick1(n[3], n[0])}> {/* CHANGE TO IMAGE ID AND FILE*/}
                                                <ListItemText primary={n[1]}
                                                              style={{"textAlign": "left"}}/> {/* CHANGE TO FILENAME*/}
                                                <ListItemText primary={n[2]}
                                                              style={{"textAlign": "left"}}/> {/* CHANGE TO TIMESTAMP*/}
                                            </ListItem>
                                        );
                                    }

                                    if (this.state.disp == "processed"){
                                        {
                                            return (
                                                <ListItem button component="a"
                                                          href="#simple-list"
                                                          onClick={() => this.onListClick2(n[3])}> {/* CHANGE TO FILE*/}
                                                    <ListItemText primary={n[1]}
                                                                  style={{"textAlign": "left"}}/> {/* CHANGE TO FILENAME*/}
                                                    <ListItemText primary={n[2]}
                                                                  style={{"textAlign": "left"}}/> {/* CHANGE TO TIMESTAMP*/}
                                                </ListItem>
                                            );
                                        }

                                    }

                                })}
                            </List>
                            <Button variant="raised" onClick={this.onListBack}
                                    style={{"marginLeft":"180px", "marginBottom":"10px"}}
                                    color="secondary">
                                View all original images
                            </Button>
                        </Paper>
                    </div>

                    <div style={styles.blockStyle}>
                        <Paper style = {{"width":"600px", "margin": "auto"}} >
                            <img src={this.state.current_image} style={{"width":"550px", "marginLeft":"20px", "marginTop":"20px", "marginRight":"20px"}} />


                            <AppBar position="static" color="default">
                                <Tabs
                                    value={this.state.tab}
                                    onChange={this.handleChange}
                                    indicatorColor="primary"
                                    textColor="primary"
                                    centered
                                >
                                    <Tab label="Original" />
                                    <Tab label="Processed"/>
                                </Tabs>
                            </AppBar>
                            <SwipeableViews
                                index={this.state.tab}
                                onChangeIndex={this.handleChangeIndex}
                            >
                                <TabContainer>
                                    <LineChart width={550} height={200}
                                               data={(this.state.images).map(n => {
                                                   return (
                                                       {name: "", value: ""}
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
                                               data={(this.state.images).map(n => {
                                                   return (
                                                       {name: "", value: ""}
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
                        <Paper style = {{"width":"600px", "margin": "auto"}} >
                        Select image processing technique:
                        <Select
                            value={this.state.process}
                            onChange={this.selectProcess}
                            input={<Input name="age" id="age-helper"
                            />}
                            style={{"marginTop":"20px", "marginBottom":"20px"}}
                        >
                            <MenuItem value={"histogram"}>Histogram Equalization</MenuItem>
                            <MenuItem value={"contrast"}>Contrast Stretching</MenuItem>
                            <MenuItem value={"log"}>Log Compression</MenuItem>
                            <MenuItem value={"reverse"}>Reverse Video</MenuItem>
                        </Select>

                            <Button variant="raised" onClick={this.resetUser}
                                    style={{"float": "right", "marginTop":"20px", "marginBottom":"20px", "marginRight":"20px"}}
                                    color="secondary">
                                GO!
                            </Button>

                        </Paper>
                        </div>

                </div>
            );
        }

    }
}
export default MainPage;