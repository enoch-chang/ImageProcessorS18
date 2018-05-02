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
            "logged_in": 0,
            "images": [],

            //["No images", "No images", "No images", "No images", "No images", [0, 0], [[0, 0], [0, 0], [0, 0]]],

            //     [['image64_1', "cat_1.jpg", "001", ".jpg", "15:05 04/20/2018",[1200,1600], [[23,14,15,18], [1, 2, 3, 4],
            //     [63,75,54,35], [1, 2, 3, 4], [45,35,34,12], [1, 2, 3, 4]]],
            //     ['image64_2', "dog_1.jpg", "002", ".jpg", "15:28 04/20/2018",[1200,1600], [[24,63,56,26], [1, 2, 3, 4],
            //         [3,63,65,73], [1, 2, 3, 4], [28,64,76,34], [1, 2, 3, 4]]],
            //         ['image64_3', "cat_2.png", "003", ".png", "16:20 04/20/2018",[1200,1600], [[87,47,83,25], [1, 2, 3, 4],
            //             [93,62,54,34], [1, 2, 3, 4], [22,63,23,46], [1, 2, 3, 4]]]], // test data
            // // [image, filename, image_id, filetype, time_stamp, image_size, histogram]
            // [   0  ,    1   ,    2    ,    3    ,     4     ,      5    ,    6     ]
            "disp_images": [],
            "disp": "original",
            "current_image":['', "No file selected.", "", "--", "--", ["--","--"], ""],
            "pro_images": [],
            //     [['image64_3', "cat_1_histogram.jpg", "001", "histogram", "16:52 04/20/2018", "4", [1200,1600], [[87,47,83,25], [1, 2, 3, 4],
            // [93,62,54,34], [1, 2, 3, 4], [22,63,23,46], [1, 2, 3, 4]]],
            // ['image64_4', "cat_2_reverse.png", "003", "reverse", "16.55 04/20/2018", "2.3", [[23,14,15,18], [1, 2, 3, 4],
            //     [63,75,54,35], [1, 2, 3, 4], [45,35,34,12], [1, 2, 3, 4]]]],
            // [proc_image, filename, image_id, proc_type, time_stamp, time_duration, histogram]
            // [     0    ,     1   ,     2   ,     3    ,     4     ,       5      ,      6   ]
            "current_image_processed":['', "No file selected.", "", "--", "--", "--", ""],
            "process":[],
            "tab":0,
            "id":"",
            "to_upload":[],
            "to_upload_names":[],
            "histogram_test": [[3,63,65,73],[93,62,54,34],[28,64,76,34],[2, 4, 6, 8],[0, 1, 2, 3]]
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
            "current_image":['', "No file selected.", "", "--", "--", ["--","--"], ""],
            "pro_images": [],
            "current_image_processed":['', "No file selected.", "", "--", "--", "--", ""],
            "tab":0,
        })
        console.log(this.state)

    }

    logIn = (event) => {
        var URL = "http://vcm-3608.vm.duke.edu:5000/api/images/".concat(this.state.email)

        axios.get(URL).then((response) => {
            console.log(response);
            console.log(response.status);

            if (this.state.logged_in == 2 && response.status == 200){
                this.setState({
                    "name": response.data["name"],
                    "images": response.data["images"],
                    "pro_images": response.data["pro_images"],
                });
            }

            if (response.data["success"] == 1 && response.status == 200) {

                this.setState({
                    "name": response.data["name"],
                    "images": response.data["images"],
                    "logged_in": 2,
                    "pro_images": response.data["pro_images"],
                    "disp_images": response.data["images"],
                });
            }
            if (response.data["success"] == 0 && response.status == 200) {
                this.setState({"logged_in":1});
            }

            console.log(this.state)
        })
    }

    createUser = (event) => {
        var URL = "http://vcm-3608.vm.duke.edu:5000/api/images/create"
        axios.post(URL,
               {"name":this.state.name,
               "email":this.state.email}).then((response) => {
                   if (response.status == 200) {
                       this.setState({"logged_in": 2});
                       this.logIn()
                   }
        })
    }

    onFileLoad = (e, files) => {
        var file_list = e.target.result;

        // for (var i=0; i<files.length; i++){
        //     var file = file_list[i]
        //     this.uploadPOST("", file, files[i].name)
        // }


        //var base64result = file_list.split(',')[1];

        this.setState({"to_upload":file_list,"to_upload_names":files.name});

        // this.setState({"current_image":e.target.result}); // Given that uploadPOST works

        // const reader = new FileReader()
        // const file = files[0]
        // reader.readAsDataURL(file);
        // reader.onloadend = () => {
        //     console.log(reader.result);
        //     this.setState({"current_image": reader.result})
        // }
    }

    uploadPOST = (event) => {
        console.log("fuck")
//for (var i=0; i<(this.state.to_upload).length; i++){

            var URL = "http://vcm-3608.vm.duke.edu:5000/api/images/upload"
            // axios.post(URL,
            //     {"images":this.state.to_upload[i],
            //      "email":this.state.email,
            //      "filename": this.state.to_upload_names[i]
            //     })

        axios.post(URL,
            {"images":this.state.to_upload,
                "email":this.state.email,
                "filename": this.state.to_upload_names
            }).then((response) => {

            if (response.status == 200) {
                this.logIn()
                this.setState({"current_image": this.state.images[(this.state.images).length - 1]});
            }
        })
            console.log(this.state)
       // }
    }


    processPOST = () => {
        var URL = "http://vcm-3608.vm.duke.edu:5000/api/images/upload".concat(this.state.email)
            .concat("/").concat(this.state.current_image[1]).concat("/").concat(this.state.process) //change to ID

        axios.post(URL,{"image_id":this.state.current_image[1], "process":this.state.process}).then((response) => { //change to ID

            if (response.status == 200) {

            this.logIn()
            this.setState({"current_image_processed": (this.pro_images)[(this.pro_images).length - 1]});
            }

        })

    }

    onListClick1 = (image) => { //holds original image array

        this.setState({"current_image":image});
        var temp_image_list = [];

        for (var i = 0; i < (this.state.pro_images).length; i++){
            if (this.state.pro_images[i][2] == image[2]){
                temp_image_list.push(this.state.pro_images[i])
            }
        }

        this.setState({"disp_images":temp_image_list,
                       "disp":"processed",
                       "current_image_processed":[]});

        console.log(this.state)
        this.handleChange("",0)

    }

    onListClick2 = (image) => { //holds processed image array

        this.setState({"current_image_processed":image}); // set to index of image
        console.log(this.state)
        this.handleChange("",1)


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
                        </div>
                        <div style={{"padding": "20px",
                            "marginLeft": "auto",
                            "marginRight": "auto"}}>

                        <TextField id="name"
                                       label="Name"
                                       value={this.state.name}
                                       onChange={this.TypeInputName}
                                       color="secondary"
                            />
                            <Button variant="raised" onClick={this.createUser}
                                    style={{"padding": "20px",
                                        "marginLeft": "auto",
                                        "marginRight": "auto",}}
                                    color="secondary">
                                CREATE NEW USER
                            </Button>
                            <Button variant="raised" onClick={this.resetUser}
                                    style={{"padding": "20px",
                                        "marginLeft": "auto",
                                        "marginRight": "auto",}}
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

                            <Typography component="p">

                            Hello {this.state.name} !

                            </Typography>


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
                            <Button variant="raised" onClick={this.uploadPOST}
                                    style={{"float": "right"}}
                                    color="secondary">
                                UPLOAD
                            </Button>
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
                                                      onClick={() => this.onListClick1(n)}> {/* CHANGE TO IMAGE ID AND FILE*/}
                                                    <ListItemText primary={n[1]}
                                                              style={{"textAlign": "left"}}/> {/* CHANGE TO FILENAME*/}
                                                <ListItemText primary={n[4]}
                                                              style={{"textAlign": "left"}}/> {/* CHANGE TO TIMESTAMP*/}
                                            </ListItem>


                                                );
                                    }

                                    if (this.state.disp == "processed"){
                                            return (
                                                <ListItem button component="a"
                                                          href="#simple-list"
                                                          onClick={() => this.onListClick2(n)}> {/* CHANGE TO FILE*/}
                                                    <ListItemText primary={n[1]}
                                                                  style={{"textAlign": "left"}}/> {/* CHANGE TO FILENAME*/}
                                                    <ListItemText primary={n[4]}
                                                                  style={{"textAlign": "left"}}/> {/* CHANGE TO TIMESTAMP*/}
                                                </ListItem>
                                            );

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
                                    <img src={this.state.current_image[0]} style={{"width":"550px", "marginLeft":"20px", "marginTop":"20px", "marginRight":"20px"}} />

                                    <LineChart width={550} height={200}
                                               data={(this.state.histogram_test[4]).map(n => {
                                                   return (
                                                       {name: this.state.histogram_test[3][n],
                                                           r: this.state.histogram_test[0][n],
                                                           g: this.state.histogram_test[1][n],
                                                           b: this.state.histogram_test[2][n]}
                                                   );
                                               })}
                                               margin={{ top: 15, right: 5, bottom: 5, left: 5 }}>
                                        <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                                        <XAxis dataKey="name" />
                                        <YAxis />
                                        <Tooltip />
                                        <Line type="monotone" dataKey="r" stroke="#8884d8" activeDot={{r: 8}} />
                                        <Line type="monotone" dataKey="g" stroke="#8884d8" activeDot={{r: 8}} />
                                        <Line type="monotone" dataKey="b" stroke="#8884d8" activeDot={{r: 8}} />

                                    </LineChart>

                                    <Card>
                                        <CardContent>
                                            <Typography gutterBottom variant="headline" component="h2">
                                                {this.state.current_image[1]}
                                            </Typography>
                                            <Typography component="p">
                                                Date Uploaded: {this.state.current_image[4]}
                                                <div>
                                                    Image Size: {this.state.current_image[5][0]} x {this.state.current_image[5][1]}
                                                </div>
                                                <div>
                                                    Filetype: {this.state.current_image[3]}
                                                </div>
                                            </Typography>
                                        </CardContent>
                                    </Card>
                                </TabContainer>
                                <TabContainer>
                                    <img src={this.state.current_image_processed[0]} style={{"width":"550px", "marginLeft":"20px", "marginTop":"20px", "marginRight":"20px"}} />
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
                                                {this.state.current_image_processed[1]}
                                            </Typography>
                                            <Typography component="p">
                                                Date Uploaded: {this.state.current_image_processed[4]}
                                                <div>
                                                    Process Type: {this.state.current_image_processed[3]}
                                                </div>
                                                <div>
                                                    Time for Processing: {this.state.current_image_processed[5]}
                                                </div>
                                            </Typography>
                                        </CardContent>
                                    </Card>
                                </TabContainer>
                            </SwipeableViews>
                        </Paper>
                    </div>

                    <div style={styles.blockStyle}>
                        <Paper style = {{"width":"600px", "margin": "auto"}} >
                            <Card>
                            <CardContent>
                            <Typography component="p">
                            Select image processing technique:
                            </Typography>
                        <Select
                            value={this.state.process}
                            onChange={this.selectProcess}
                            input={<Input name="age" id="age-helper"
                            />}
                            style={{"marginTop":"20px", "marginBottom":"20px"}}
                        >
                            <MenuItem value={"histogram eq"}><Typography component="p">
                                Histogram Equalization </Typography></MenuItem>
                            <MenuItem value={"contrast stretching"}><Typography component="p">Contrast Stretching</Typography></MenuItem>
                            <MenuItem value={"log compression"}><Typography component="p">Log Compression</Typography></MenuItem>
                            <MenuItem value={"reverse video"}><Typography component="p">Reverse Video</Typography></MenuItem>

                        </Select>

                            <Button variant="raised" onClick={this.processPOST}
                                    style={{"float": "right", "marginTop":"20px", "marginBottom":"20px", "marginRight":"20px"}}
                                    color="secondary">
                                GO!
                            </Button>
                                </CardContent>
                                </Card>
                        </Paper>
                        </div>

                </div>
            );
        }

    }
}
export default MainPage;