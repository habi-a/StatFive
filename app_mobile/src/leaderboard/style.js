const React = require("react-native");

const { StyleSheet } = React;


export default {

    header: {
      backgroundColor: "#0090F8",
      height:160,
    },
    icon_home: {
      position: 'absolute',
      left: 20,
      top: 40,
      color: 'white',
    },
    name_board: {
      position: 'absolute',
      right: 20,
      top: 30,
      color: 'white',
      fontWeight: 'bold',
      fontSize: 28,
    },
    position: {
      position: 'absolute',
      right: 20,
      top: 70,
      color: 'white',
      fontWeight: 'bold',
      fontSize: 28,
    },
    avatar: {
      width: 130,
      height: 130,
      borderRadius: 63,
      borderWidth: 4,
      borderColor: "white",
      marginBottom: 10,
      alignSelf: 'center',
      position: 'absolute',
      marginTop: 90
    },
    bodyContent: {
      alignItems: 'center',
      padding: 18,
    },
    rankStyle: {
      fontWeight: 'bold',
      fontSize: 24,
      color: 'white',
    },
    labelStyle: {
      fontWeight: 'normal',
      fontSize: 22,
      color: 'black',
    },
    scoreStyle: {
      fontWeight: 'normal',
      fontSize: 22,
      color: 'black'
    },
};
