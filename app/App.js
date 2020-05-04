import React, { Component, useState, useEffect } from 'react';
import { ActivityIndicator, FlatList, Text, View, StyleSheet, SafeAreaView, Alert, Button } from 'react-native';
import axios from 'axios';
import RNAndroidNotificationListener from 'react-native-android-notification-listener';
import Constants from 'expo-constants';

function Separator() {
    return <View style={styles.separator} />;
}

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
            isLoading: true,
            hasPermission: false,
            lastNotification: null
        };
    }

    handleOnPressPermissionButton = async () => {
        RNAndroidNotificationListener.requestPermission();
    };

    handleAppStateChange = async nextAppState => {
        RNAndroidNotificationListener.getPermissionStatus().then(status => {
            setHasPermission(status !== 'denied');
        });
    };

    
    handleNotificationReceived = notification => {
        setLastNotification(notification);
    };

    // useEffect(() => {
    //     RNAndroidNotificationListener.getPermissionStatus().then(status => {
    //       setHasPermission(status !== 'denied');
    //     });
    
    //     RNAndroidNotificationListener.onNotificationReceived(
    //       handleNotificationReceived,
    //     );
    
    //     AppState.addEventListener('change', handleAppStateChange);
    
    //     return () => {
    //       AppState.removeEventListener('change', handleAppStateChange);
    //     };
    //   }, []); 

    sendData = (props) => {
        console.log("Getting data");
        axios.post("http://192.168.1.191", props).then((response) => {
            // console.log(response.data);
        })
    }

    componentDidMount() {
        fetch('https://reactnative.dev/movies.json')
            .then((response) => response.json())
            .then((json) => {
                this.setState({ data: json.movies });
            })
            .catch((error) => console.error(error))
            .finally(() => {
                this.setState({ isLoading: false });
            });
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
                    {/* <FlatList
                        data={data}
                        keyExtractor={({ id }, index) => id}
                        renderItem={({ item }) => (
                            <Text>{item.title}, {item.releaseYear}</Text>
                        )}
                    /> */}
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