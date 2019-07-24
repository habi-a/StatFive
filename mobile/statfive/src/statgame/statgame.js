import React, { Component } from "react";
import styles from './style'
import annexe from '../../annexe'

import {Keyboard, 
    Text, 
    View, 
    TouchableWithoutFeedback, 
    KeyboardAvoidingView,
    RefreshControl,
    ScrollView,
    ImageBackground} from 'react-native';

export default class StatGameScreen extends Component {

    static navigationOptions = {
        header:null,
      };
  
      constructor(props){
            super(props)
            this.state={
                refreshing: false,
        }
    }

    _onRefresh = () => {
        this.setState({refreshing: true});
        this.fetchData().then(() => {
            this.setState({refreshing: false});
          });
    }

    render() {
        return (
        <ImageBackground blurRadius={2} source={require('../../assets/background-home.png')} style={{width: '100%', height: '100%', opacity: 0.95}}>
            <KeyboardAvoidingView style={styles.containerView} behavior="padding">
                <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
                    <View style={styles.HeaderGenerique}>
                        
                    </View>
                </TouchableWithoutFeedback>
                <View>
                    <ScrollView
                            refreshControl={
                                <RefreshControl
                                    refreshing={this.state.refreshing}
                                    onRefresh={this._onRefresh.bind(this)}
                                />} >


                    </ScrollView>
                </View>
            </KeyboardAvoidingView>
        </ImageBackground>
        );
    }
}