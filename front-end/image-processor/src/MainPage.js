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
import Toolbar from 'material-ui/Toolbar'
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

        var histogram_x = []
        for (var i=0; i<=255; i++){
            histogram_x.push(i)
        }

        this.state = {
            "email": ["Enter your e-mail"],
            "name": ["Enter your name"],
            "logged_in": 0,
            "images": [],
            // // [image, filename, image_id, filetype, time_stamp, image_size, histogram]
            // [   0  ,    1   ,    2    ,    3    ,     4     ,      5    ,    6     ]
            "disp_images": [],
            "disp": "original",
            "current_image":['', "No file selected.", "", "--", "--", ["--","--"], [["0 0 0"],["0 0 0"],["0 0 0"]]],
            "pro_images": [],
            // [proc_image, filename, image_id, proc_type, time_stamp, time_duration, histogram]
            // [     0    ,     1   ,     2   ,     3    ,     4     ,       5      ,      6   ]
            "current_image_processed":['', "No file selected.", "", "--", "--", "--", ""],
            "process":[],
            "tab":0,
            "id":"",
            "to_upload":[],
            "to_upload_names":[],
            "histogram_x": histogram_x,
            "histogram_ori":[[],[],[]],
            "histogram_test": [["3","63","65","73"],[93,62,54,34],[28,64,76,34],[2, 4, 6, 8],[0, 1, 2, 3]],
            "histogram_pro":[[],[],[]]
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

            if (this.state.logged_in == 2 && response.status == 200){ // ALREADY LOGGED-IN/REFRESH
                this.setState({
                    "name": response.data["name"],
                    "images": response.data["images"],
                    "pro_images": response.data["pro_images"],
                });
                if ((this.state.images).length>0) {
                    this.setState({"current_image": this.state.images[((this.state.images).length) - 1]});
                }

                if ((this.state.pro_images).length>0) {
                    this.setState({"current_image_processed": this.state.pro_images[((this.state.pro_images).length) - 1]});
                }

                if (this.state.disp == "original"){
                    this.setState({"disp_images": response.data["images"]});
                }

            }

            if (response.data["success"] == 1 && this.state.logged_in != 2 && response.status == 200) { // SUCCESSFUL LOG-IN

                this.setState({
                    "name": response.data["name"],
                    "images": response.data["images"],
                    "logged_in": 2,
                    "pro_images": response.data["pro_images"],
                    "disp_images": response.data["images"],
                });
            }

            if (response.data["success"] == 0 && response.status == 200) { // USER DOES NOT EXIST YET
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
                  //     this.setState({"success": 2});
                       this.logIn()
                   }
        })
    }

    onFileLoad = (e, files) => {
        var file_list = e.target.result;
        this.setState({"to_upload":file_list,"to_upload_names":files.name});

    }

    uploadPOST = (event) => {
            var URL = "http://vcm-3608.vm.duke.edu:5000/api/images/upload"

        axios.post(URL,
            {"images":this.state.to_upload,
                "email":this.state.email,
                "filename": this.state.to_upload_names
            })
            console.log(this.state)
    }


    processPOST = () => {
        var URL = "http://vcm-3608.vm.duke.edu:5000/api/images/".concat(this.state.email)
            .concat("/").concat(this.state.current_image[1]).concat("/process") //change to ID

        this.setState({"to_upload":this.state.current_image[0]});
        console.log(this.state)

        axios.post(URL,{"images":this.state.to_upload,
                        "process":this.state.process}).then((response) => { //change to ID

            if (response.status == 200) {

            this.logIn()
            }

        })

    }

    parseHistogram = (image) => {

        var r = (image[6][0]).split(" ");
        var g = (image[6][1]).split(" ");
        var b = (image[6][2]).split(" ");


        var r_mod = []

        for (var i = 1; i < r.length-1; i++) {
            if (r[i]) {
                r_mod.push(r[i]);
            }
        }

        var g_mod = []

        for (var i = 1; i < g.length-1; i++) {
            if (g[i]) {
                g_mod.push(g[i]);
            }
        }


        var b_mod = []

        for (var i = 1; i < b.length-1; i++) {
            if (b[i]) {
                b_mod.push(b[i]);
            }
        }


        var temp_max = 0;

        for (var i=0; i< r.length; i++){
            if (Number(r_mod[i]) > temp_max){
                temp_max = Number(r_mod[i]);}
            if (Number(g_mod[i]) > temp_max){
                temp_max = Number(g_mod[i]);}
            if (Number(b_mod[i]) > temp_max){
                temp_max = Number(b_mod[i]);}
        }

            return [r_mod, g_mod, b_mod, temp_max]

    }


    onListClick1 = (image) => { //holds original image array

        this.setState({"current_image":image});
        this.setState({"histogram_ori":this.parseHistogram(image)});
        var temp_image_list = [[]];
        console.log(image)
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
        this.setState({"histogram_pro":this.parseHistogram(image)});
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

                            /> {' '}
                        <TextField id="name"
                                       label="Name"
                                       value={this.state.name}
                                       onChange={this.TypeInputName}
                                       color="secondary"
                                       style = {{"marginLeft":"50px"}}
                            />
                        </div>
                            <div style={{"margin":"auto", "textAlign":"center"}}>
                            <Button variant="raised" onClick={this.createUser}
                                    style={{ "margin": "5px","marginBottom":"20px"}}
                                    color="secondary">
                                CREATE NEW USER
                            </Button> {' '}
                            <Button variant="raised" onClick={this.resetUser}
                                    style={{"margin": "5px","marginBottom":"20px"}}
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
                    <Paper style={{"width": "600px", "height":"100px","margin": "auto"}}>
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

                    <Paper style = {{"width":"600px", "height":"100px", "margin": "auto"}} >
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

                                    <LineChart width={550} height={300}
                                               data={(this.state.histogram_x).map(n => {
                                                   return (
                                                       {name: n,
                                                           r: this.state.histogram_ori[0][n],
                                                           g: this.state.histogram_ori[1][n],
                                                           b: this.state.histogram_ori[2][n]}
                                                   );
                                               })}
                                               margin={{ top: 15, right: 5, bottom: 5, left: 5 }}>
                                        <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                                        <XAxis dataKey="name" />
                                        <YAxis  type="number" domain={[0, this.state.histogram_ori[3] + 50]} />
                                        <Tooltip />
                                        <Line type="monotone" dataKey="r" stroke="#cc0000" activeDot={{r: 8}} />
                                        <Line type="monotone" dataKey="g" stroke="#006600" activeDot={{r: 8}} />
                                        <Line type="monotone" dataKey="b" stroke="#003399" activeDot={{r: 8}} />

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
                                    <img src={"data:image/jpeg;base64,".concat(this.state.current_image_processed[0])} style={{"width":"550px", "marginLeft":"20px", "marginTop":"20px", "marginRight":"20px"}} />
                                    <LineChart width={550} height={300}
                                               data={(this.state.histogram_x).map(n => {
                                                   return (
                                                       {name: n,
                                                           r: this.state.histogram_pro[0][n],
                                                           g: this.state.histogram_pro[1][n],
                                                           b: this.state.histogram_pro[2][n]}
                                                   );
                                               })}
                                               margin={{ top: 15, right: 5, bottom: 5, left: 5 }}>
                                        <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                                        <XAxis dataKey="name" />
                                        <YAxis  type="number" domain={[0, this.state.histogram_pro[3] + 50]} />
                                        <Tooltip />
                                        <Line type="monotone" dataKey="r" stroke="#cc0000" activeDot={{r: 8}} />
                                        <Line type="monotone" dataKey="g" stroke="#006600" activeDot={{r: 8}} />
                                        <Line type="monotone" dataKey="b" stroke="#003399" activeDot={{r: 8}} />

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
                            <MenuItem value={"Histogram Equalization"}><Typography component="p">
                                Histogram Equalization </Typography></MenuItem>
                            <MenuItem value={"Contrast Stretching"}><Typography component="p">Contrast Stretching</Typography></MenuItem>
                            <MenuItem value={"Log Compression"}><Typography component="p">Log Compression</Typography></MenuItem>
                            <MenuItem value={"Reverse Video"}><Typography component="p">Reverse Video</Typography></MenuItem>

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