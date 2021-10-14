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
    icon_logout: {
      position: 'absolute',
      right: 20,
      top: 40,
      color: 'white',
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
    body: {
      marginTop:40,
    },
    bodyContent: {
      alignItems: 'center',
      padding:30,
    },
    name:{
      fontWeight: 'bold',
      fontSize:28,
      color: "#696969",
      fontWeight: "600"
    },
    info: {
      fontSize:16,
      color: "#0090F8",
      marginTop:10
    },
    description: {
      fontSize:16,
      color: "#696969",
      marginTop:10,
      textAlign: 'center'
    },
    email: {
      fontWeight: 'bold',
      fontSize: 20,
      color: "#696969",
      marginTop:10,
      textAlign: 'center'
    },
    titre: {
      fontWeight: 'bold',
      fontSize:20,
      color: "#0090F8",
      marginTop:10,
      textAlign: 'left'
    },
    nbr_matchs: {
      fontSize:20,
      fontWeight: 'bold',
      color: "#696969",
      marginTop:10,
      textAlign: 'center'
    },
};
