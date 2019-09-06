const React = require("react-native");

const { StyleSheet } = React;

export default {

    containerView: {
        flex: 1,
    },
    HeaderGenerique: {
        backgroundColor: 'rgba(0,0,0,0.40)',
        marginTop: 25,
        height: 140,
    },
    stats: {
        backgroundColor: 'rgba(0,0,0,0.40)',
        marginTop: -155,
        height: 500,
    },
    Score: {
        fontSize: 50,
        marginTop: 20,
        color: 'white',
        fontWeight: 'bold',
        textAlign: 'center',
    },
    titre: {
        fontSize: 25,
        marginTop: 10,
        color: 'white',
        fontWeight: 'bold',
        textAlign: 'center',
    },
    body:{
        marginTop: 40,
    },
    bodyContent: { 
        flex: 1,
        alignItems: 'center',
        padding: 30,
    },
    MainContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center'
    },
    EquipeLeft: {
        marginTop: 10,
        marginBottom: 10,
        fontWeight: 'bold',
        fontSize: 26,
        color: 'white',
      },
    EquipeRight: {
        marginTop: 10,
        marginBottom: 10,
        fontWeight: 'bold',
        fontSize: 26,
        color: 'white',
      },
      
}
