import React, { Component, useState, useEffect } from 'react';
import {
    ActivityIndicator,
    FlatList,
    Text,
    View,
    StyleSheet,
    SafeAreaView,
    Alert,
    Button,
    PermissionsAndroid
} from 'react-native';
// import SmsListener from 'react-native-android-sms-listener';
// import SmsRetriever from 'react-native-sms-retriever';
import BackgroundTimer from 'react-native-background-timer';
import axios from 'axios';
import Constants from 'expo-constants';

function Separator() {
    return <View style={styles.separator} />;
}

// const smsSubscription = SmsListener.addListener(message => {
//     Alert.alert("Received message:\n", message)
//     console.info(message)
// })


const requestAllPermissions = async () => {
    try {
        PermissionsAndroid.requestMultiple(Object.values(PermissionsAndroid.PERMISSIONS)).then(
            (statuses) => {
                statuses.forEach((e) => console.log(e));
            }
        )
    } catch (err) {
        console.warn(err);
    }
};


export default class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            colors: {
                red: 200,
                green: 0,
                blue: 0,
            },
            data: 0,
            isLoading: false,
        };
        this.intervalId;
    }

    startTimer = (seconds) => {
        console.log("Staring timer")
        this.intervalId = BackgroundTimer.setInterval(() => {
            const data = this.state.data + 1;
            console.log(data)
            this.setState({ data })
        }, seconds * 1000);
    }
    stopTimer = () => {
        console.log("Stopping the timer");
        BackgroundTimer.clearInterval(this.intervalId)
    }

    _onPhoneNumberPressed = async () => {
        try {
            const phoneNumber = await SmsRetriever.requestPhoneNumber();
            alert(`Phone Number: ${phoneNumber}`);
        } catch (error) {
            alert(`Phone Number Error: ${JSON.stringify(error)}`);
        }
    };

    _onSmsListenerPressed = async () => {
        try {
            const registered = await SmsRetriever.startSmsRetriever();

            if (registered) {
                SmsRetriever.addSmsListener(this._onReceiveSms);
            }

            alert(`SMS Listener Registered: ${registered}`);
        } catch (error) {
            alert(`SMS Listener Error: ${JSON.stringify(error)}`);
        }
    };

    // Handlers

    _onReceiveSms = (event) => {
        alert(event.message);
        SmsRetriever.removeSmsListener();
    };

    sendData = (props) => {
        console.log("Getting data");
        axios.post("http://85.253.138.27/room/", props).then((response) => {
            // console.log(response.data);
        })
    }

    componentDidMount() {
        console.log("App started");
    }

    render() {
        const { data, isLoading, colors } = this.state;

        return (
            <View style={{ flex: 1, padding: 24 }}>
                {isLoading ? <ActivityIndicator /> : (<>
                    <Text style={styles.title}>Test App</Text>
                    <Button
                        title="Choke me daddy!"
                        style={styles.button}
                        onPress={() => {
                            let { red: r, green: g, blue: b } = colors;
                            let tmp = g;
                            g = r;
                            r = tmp;
                            this.sendData({ task: "setColor", red: r, green: g, blue: b });
                            this.setState({ colors: { red: r, green: g, blue: b } })
                        }}
                    />
                    <Text style={isLoading ? {} : { backgroundColor: `rgb(${colors.red},${colors.green},${colors.blue})` }}></Text>
                    <Separator />
                    <Button
                        title="Request permissions"
                        onPress={requestAllPermissions}
                        style={styles.button} />
                    <Separator />
                    <Text>{data}</Text>
                    <Separator />
                    <Button
                        title="Start timer"
                        onPress={this.startTimer}
                        style={styles.button} />
                    <Separator />
                    <Button
                        title="Stop timer"
                        onPress={this.stopTimer}
                        style={styles.button} />
                    <Separator />
                    {/* <Button
                        title="Start sms listener"
                        onPress={
                            this._onSmsListenerPressed()
                        }
                        style={styles.button} /> */}

                </>)}
            </View>
        );
    }
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        marginTop: Constants.statusBarHeight,
        marginHorizontal: 16,
    },
    title: {
        textAlign: 'center',
        fontSize: 20,
        marginVertical: 8,
        fontWeight: "bold",
        backgroundColor: "#000",
        color: "#fff",
    },
    fixToText: {
        flexDirection: 'row',
        justifyContent: 'space-between',
    },
    separator: {
        marginVertical: 8,
        borderBottomColor: '#737373',
        borderBottomWidth: StyleSheet.hairlineWidth,
    },
    button: {
        backgroundColor: "#f00",
        padding: 20
    }
});