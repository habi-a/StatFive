const React = require("react-native");

const { StyleSheet } = React;

export default {

    containerView: {
        flex: 1,
        height: '100%',
        justifyContent: 'space-around',
        left: 0,
        position: 'absolute',
        top: 0,
        width: '100%'
    },
    loginScreenContainer: {
        flex: 1,
    },
    logoText: {
        fontSize: 50,
        fontWeight: 'bold',
        marginTop: 50,
        marginBottom: 160,
        textAlign: 'center',
        color: '#196F3D',
    },
    loginFormView: {
        flex: 1
    },
    loginFormTextInput: {
        height: 44,
        fontSize: 18,
        borderRadius: 8,
        borderWidth: 1.2,
        borderColor: '#000000',
        backgroundColor: '#eeeeee',
        marginLeft: 35,
        marginRight: 35,
        marginTop: 5,
        marginBottom: 5,
        opacity:0.8,
        fontWeight: 'bold',
        textAlign: 'center',
    },
    loginButton: {
        borderColor: '#000000',
        backgroundColor: '#196F3D',
        borderRadius: 15,
        borderWidth: 1.2,
        height: 45,
        marginTop: 40,
        marginLeft: 110,
        marginRight: 110,
        marginBottom: 20,
    },
    MainContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center'
    },
    TextStyle: {
        color: '#E91E63',
        fontSize: 18,
        textDecorationLine: 'underline'
    }
};
