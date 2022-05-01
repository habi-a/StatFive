const React = require("react-native");

const { StyleSheet, Dimensions } = React;
const window = Dimensions.get('window');

export default {

    containerView: {
        flex: 1,
        height: '100%',
        justifyContent: 'space-around',
        left: 0,
        position: 'absolute',
        top: 0,
        width: '100%',
        backgroundColor: '#f6f6f6'
    },
    ScrollView: {
        backgroundColor: '#F6F6F6'
    },
    registerScreenContainer: {
        flex: 1,
    },
    registerFormView: {
        flex: 1
    },
    registerFormTextInput: {
        height: 44,
        fontSize: 18,
        borderRadius: 8,
        borderWidth: 1.2,
        borderColor: '#000000',
        backgroundColor: '#f6f6f6',
        marginLeft: 35,
        marginRight: 35,
        marginTop: 5,
        marginBottom: 5,
        opacity: 0.8,
        fontWeight: 'bold',
        textAlign: 'center',
    },
    registerButton: {
        backgroundColor: '#0090F8',
        borderRadius: 15,
        borderWidth: 1.2,
        height: 45,
        marginTop: 30,
        marginLeft: 15,
        marginRight: 15,
        marginBottom: 30,
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
    },
};
