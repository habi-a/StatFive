const React = require("react-native");

const { StyleSheet } = React;

export default {

    containerView: {
        flex: 1,
    },
    logoText: {
        fontSize: 30,
        fontWeight: "800",
        marginTop: 30,
        marginBottom: 10,
        marginLeft: 20,
    },
    logoName: {
        fontSize: 30,
        fontWeight: "800",
        marginTop: -50,
        marginLeft: 250,
        marginBottom: 10,
        color: 'white'
    },
    HeaderGenerique: {
        backgroundColor: 'rgba(0,0,0,0.40)',
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
        color: '#196F3D',
        fontWeight: 'bold',
        alignItems: 'center'
    },
    listItems: {
        fontSize: 18,
        color:'white',
        fontWeight: 'bold',
    },
}
