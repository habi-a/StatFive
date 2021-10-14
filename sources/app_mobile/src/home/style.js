const React = require("react-native");

const { StyleSheet } = React;

export default {

    containerView: {
        flex: 1,
    },
    logoText: {
        fontSize: 30,
        fontWeight: 'bold',
        marginTop: 40,
        marginBottom: 10,
        marginLeft: 20,
    },
    icon_trophy: {
      position: 'absolute',
      right: 100,
      top: 40,
      color: 'white',
    },
    icon_profil: {
      position: 'absolute',
      right: 40,
      top: 40,
      color: 'white',
    },
    header: {
      backgroundColor: "#0090F8",
      height:100,
    },
    body:{
        marginTop:40,
    },
    bodyContent: {
        flex: 1,
        alignItems: 'center',
        padding:30,
    },
    item: {
        padding: 10,
        fontSize: 18,
        height: 44,
    },
    MainContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center'
    },
    FirstLetter: {
        fontSize: 25,
        color: '#0090F8',
        fontWeight: 'bold',
        alignItems: 'center'
    },
    listItems: {
        fontSize: 18,
        color: '#696969',
        fontWeight: 'bold',
    },
}
