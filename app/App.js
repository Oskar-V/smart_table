import React, { Component, useState, useEffect } from 'react';
import { ActivityIndicator, FlatList, Text, View, StyleSheet, SafeAreaView, Alert, Button, PermissionsAndroid } from 'react-native';
import axios from 'axios';
import Constants from 'expo-constants';

function Separator() {
    return <View style={styles.separator} />;
}

const requestAllPermissions = async () => {
    try {
        PermissionsAndroid.requestMultiple(Object.values(PermissionsAndroid.PERMISSIONS)).then(
            (statuses) => {
                statuses.forEach((e) => console.log(e));
            }
        )
        // const granted = await PermissionsAndroid.request(
        //     PermissionsAndroid.PERMISSIONS.CAMERA,
        //     {
        //         title: "Cool Photo App Camera Permission",
        //         message:
        //             "Cool Photo App needs access to your camera " +
        //             "so you can take awesome pictures.",
        //         buttonNeutral: "Ask Me Later",
        //         buttonNegative: "Cancel",
        //         buttonPositive: "OK"
        //     }
        // );
        // if (granted === PermissionsAndroid.RESULTS.GRANTED) {
        //     console.log("You can use the camera");
        // } else {
        //     console.log("Camera permission denied");
        // }
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
            data: [],
            isLoading: false,
        };
    }

    sendData = (props) => {
        console.log("Getting data");
        axios.post("http://192.168.1.191", props).then((response) => {
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
                    <Text style={{ backgroundColor: `rgb(${colors.red},${colors.green},${colors.blue})` }}></Text>
                    <Separator />
                    <Button
                        title="request permissions"
                        onPress={requestAllPermissions}
                        style={styles.button} />
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